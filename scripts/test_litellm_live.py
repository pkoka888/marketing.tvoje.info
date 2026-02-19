#!/usr/bin/env python3
"""LiteLLM live functional test suite.

Tests all tiers, fallback chains, and concurrent requests.
Reusable by all agents for parallel orchestration validation.

Usage:
    python scripts/test_litellm_live.py
    python scripts/test_litellm_live.py --tier T1
    python scripts/test_litellm_live.py --fallbacks-only
    python scripts/test_litellm_live.py --concurrent

Exit codes: 0 = all pass, 1 = failures, 2 = proxy unreachable
"""
import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Optional

BASE_URL = "http://localhost:4000"
MASTER_KEY = os.environ.get(
    "LITELLM_MASTER_KEY", "sk-local-dev-1234"
)
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {MASTER_KEY}",
}
PROMPT = [{"role": "user", "content": "Reply with one word: OK"}]

# Model registry matching proxy_config.yaml
MODELS = [
    ("minimax-free", "T1-FREE", "OpenRouter minimax"),
    ("glm4-free", "T1-FREE", "OpenRouter glm4.7"),
    ("gemma-free", "T1-FREE", "OpenRouter gemma"),
    ("gemini-flash", "T2-COMPLEX", "Gemini 2.5 Flash"),
    ("gemini-pro", "T3-ARCHITECT", "Gemini 1.5 Pro"),
    ("groq-llama-70b", "T4-PAID", "Groq llama-3.3-70b"),
    ("groq-llama-8b", "T4-PAID", "Groq llama-3.1-8b"),
    ("gpt-4o-mini", "T4-PAID", "OpenAI gpt-4o-mini"),
]

# Fallback chains from router_settings
FALLBACK_CHAINS = {
    "minimax-free": [
        "glm4-free", "gemma-free",
        "gemini-flash", "groq-llama-8b",
    ],
    "glm4-free": [
        "minimax-free", "gemma-free",
        "gemini-flash", "groq-llama-8b",
    ],
    "gemini-flash": [
        "minimax-free", "glm4-free",
        "groq-llama-8b", "groq-llama-70b",
    ],
    "gemini-pro": [
        "gemini-flash", "groq-llama-70b", "gpt-4o-mini",
    ],
    "groq-llama-70b": ["groq-llama-8b", "gpt-4o-mini"],
}

# Expected substrings in model_used for each model_name
MODEL_PATTERNS = {
    "minimax-free": "minimax",
    "glm4-free": "glm",
    "gemma-free": "gemma",
    "gemini-flash": "gemini",
    "gemini-pro": "gemini",
    "groq-llama-70b": "llama-3.3-70b",
    "groq-llama-8b": "llama-3.1-8b",
    "gpt-4o-mini": "gpt-4o-mini",
}


@dataclass
class TestResult:
    """Single test result."""

    model: str
    tier: str
    test_type: str   # direct | fallback | concurrent
    status: str      # PASS | FAIL | FALLBACK
    latency_ms: int = 0
    response_text: str = ""
    model_used: str = ""
    error: str = ""
    http_status: int = 0


def post_json(url, data, timeout=60):
    """Send POST request and return (status, body)."""
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=payload, headers=HEADERS, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {"error": {"message": str(e)}}
        return e.code, body
    except Exception as e:
        return 0, {"error": {"message": str(e)}}


def get_json(url):
    """Send GET request and return (status, body)."""
    req = urllib.request.Request(
        url, headers=HEADERS, method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except Exception as e:
        return 0, {"error": str(e)}


def test_model(
    model_name: str,
    tier: str,
    test_type: str = "direct",
    max_tokens: int = 10,
) -> TestResult:
    """Test a single model via the proxy."""
    t0 = time.monotonic()
    code, body = post_json(
        f"{BASE_URL}/v1/chat/completions",
        {
            "model": model_name,
            "messages": PROMPT,
            "max_tokens": max_tokens,
            "temperature": 0,
        },
    )
    ms = int((time.monotonic() - t0) * 1000)

    if code == 200:
        try:
            text = body["choices"][0]["message"]["content"]
            used = body.get("model", "unknown")
            st = "PASS"
            if test_type == "direct":
                pat = MODEL_PATTERNS.get(model_name, "")
                if pat and pat not in used.lower():
                    st = "FALLBACK"
            return TestResult(
                model_name, tier, test_type, st,
                ms, text.strip()[:80], used,
                http_status=code,
            )
        except (KeyError, IndexError) as e:
            return TestResult(
                model_name, tier, test_type, "FAIL",
                ms, error=f"Bad response: {e}",
                http_status=code,
            )

    err = body.get("error", {})
    if isinstance(err, dict):
        msg = err.get("message", str(body))[:200]
    else:
        msg = str(err)[:200]
    return TestResult(
        model_name, tier, test_type, "FAIL",
        ms, error=msg, http_status=code,
    )


def check_proxy() -> tuple:
    """Return (is_healthy, model_list)."""
    code, _ = get_json(f"{BASE_URL}/health")
    if code not in (200, 401):
        return False, []
    code2, body2 = get_json(f"{BASE_URL}/v1/models")
    models = []
    if code2 == 200:
        models = [m["id"] for m in body2.get("data", [])]
    return True, models


def run_direct_tests(
    tier_filter: Optional[str] = None,
) -> list:
    """Test each model directly."""
    results = []
    models = MODELS
    if tier_filter:
        tiers = tier_filter.upper().split(",")
        models = [
            (n, t, d) for n, t, d in MODELS
            if any(x in t for x in tiers)
        ]

    for name, tier, _desc in models:
        r = test_model(name, tier)
        icon = {"PASS": "+", "FAIL": "X", "FALLBACK": "~"}
        sym = icon.get(r.status, "?")
        if r.status == "PASS":
            print(
                f"  [{sym}] {tier:12s} {name:18s}"
                f" {r.latency_ms:5d}ms"
                f"  '{r.response_text[:30]}'"
            )
        elif r.status == "FALLBACK":
            print(
                f"  [{sym}] {tier:12s} {name:18s}"
                f" {r.latency_ms:5d}ms"
                f"  -> {r.model_used}"
            )
        else:
            print(
                f"  [{sym}] {tier:12s} {name:18s}"
                f" HTTP {r.http_status}"
                f" | {r.error[:50]}"
            )
        results.append(r)
        time.sleep(0.3)
    return results


def run_fallback_tests() -> list:
    """Test fallback chain scenarios."""
    results = []
    print(
        "\n  Testing fallback chains"
        " (requested -> responded):"
    )

    for source in FALLBACK_CHAINS:
        r = test_model(source, "FALLBACK", "fallback")
        if r.status in ("PASS", "FALLBACK"):
            used = r.model_used
            if source not in used.lower():
                tag = f"FALLBACK -> {used}"
            else:
                tag = f"DIRECT ({used})"
            print(
                f"  [+] {source:18s} -> {tag}"
                f" ({r.latency_ms}ms)"
            )
        else:
            print(
                f"  [X] {source:18s}"
                f" -> EXHAUSTED | {r.error[:50]}"
            )
        results.append(r)
        time.sleep(0.5)
    return results


def run_concurrent_tests(count: int = 4) -> list:
    """Send concurrent requests to test load balancing."""
    results = []
    print(f"\n  Sending {count} concurrent requests...")

    def _call(_):
        return test_model(
            "groq-llama-8b", "CONCURRENT", "concurrent"
        )

    with concurrent.futures.ThreadPoolExecutor(count) as p:
        futs = [p.submit(_call, i) for i in range(count)]
        for f in concurrent.futures.as_completed(futs):
            results.append(f.result())

    ok = sum(1 for r in results if r.status == "PASS")
    lats = [r.latency_ms for r in results if r.status == "PASS"]
    avg = sum(lats) // len(lats) if lats else 0
    print(f"  [{ok}/{count}] passed | avg: {avg}ms")
    return results


def write_results(results, output_path):
    """Write JSON results for other agents."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tiers = [
        "T1-FREE", "T2-COMPLEX", "T3-ARCHITECT",
        "T4-PAID", "FALLBACK", "CONCURRENT",
    ]
    breakdown = {}
    for tier in tiers:
        tier_r = [r for r in results if r.tier == tier]
        if tier_r:
            breakdown[tier] = {
                "total": len(tier_r),
                "passed": sum(
                    1 for r in tier_r
                    if r.status in ("PASS", "FALLBACK")
                ),
                "failed": sum(
                    1 for r in tier_r if r.status == "FAIL"
                ),
            }
    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "proxy_url": BASE_URL,
        "total": len(results),
        "passed": sum(
            1 for r in results if r.status == "PASS"
        ),
        "failed": sum(
            1 for r in results if r.status == "FAIL"
        ),
        "fallbacks": sum(
            1 for r in results if r.status == "FALLBACK"
        ),
        "tier_breakdown": breakdown,
        "results": [asdict(r) for r in results],
    }
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    return summary


def print_summary(results, summary):
    """Print test summary."""
    p = summary["passed"]
    fb = summary["fallbacks"]
    fl = summary["failed"]
    t = summary["total"]

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"RESULTS: {p} pass | {fb} fallback | {fl} fail | {t} total")
    for tier, data in summary["tier_breakdown"].items():
        tag = "OK" if data["failed"] == 0 else "FAIL"
        print(
            f"  {tier:14s}:"
            f" {data['passed']}/{data['total']} ({tag})"
        )

    if fl > 0:
        print("\nFailed models:")
        for r in results:
            if r.status == "FAIL":
                print(f"  {r.model}: {r.error[:70]}")


def main():
    """Run the test suite."""
    parser = argparse.ArgumentParser(
        description="LiteLLM Live Test Suite"
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=4000)
    parser.add_argument("--tier", help="Filter: T1,T2,T3,T4")
    parser.add_argument(
        "--fallbacks-only", action="store_true"
    )
    parser.add_argument(
        "--concurrent", action="store_true"
    )
    parser.add_argument(
        "--output",
        default="plans/agent-shared/litellm-test-results.json",
    )
    args = parser.parse_args()

    global BASE_URL  # noqa: PLW0603
    BASE_URL = f"http://{args.host}:{args.port}"

    sep = "=" * 60
    print(sep)
    print(f"LiteLLM Test Suite | {BASE_URL}")
    print(sep)

    healthy, registered = check_proxy()
    if not healthy:
        print(f"\nERROR: Proxy unreachable at {BASE_URL}")
        print("Start: python litellm/start_litellm.py")
        sys.exit(2)
    print(f"\nProxy: OK | {len(registered)} models")
    print(f"Models: {', '.join(registered)}")

    all_results = []

    if args.fallbacks_only:
        print("\n[Fallback Chain Tests]")
        all_results.extend(run_fallback_tests())
    elif args.concurrent:
        print("\n[Concurrent Load Tests]")
        all_results.extend(run_concurrent_tests(8))
    else:
        print("\n[Direct Model Tests]")
        all_results.extend(run_direct_tests(args.tier))
        print("\n[Fallback Chain Tests]")
        all_results.extend(run_fallback_tests())
        print("\n[Concurrent Tests]")
        all_results.extend(run_concurrent_tests())

    summary = write_results(all_results, args.output)
    print_summary(all_results, summary)
    print(f"\nResults: {args.output}")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
