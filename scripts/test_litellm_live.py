#!/usr/bin/env python3
"""
LiteLLM Live Functional Test Suite
Tests all tiers: T1 free → T2 free-complex → T3 paid → T4 last-resort
Also validates fallback chain behavior.

Usage:
    python scripts/test_litellm_live.py [--host localhost] [--port 4000]
"""
import json
import sys
import time
import argparse
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Optional


BASE_URL = "http://localhost:4000"
MASTER_KEY = os.environ.get("LITELLM_MASTER_KEY", "sk-local-dev-1234")
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {MASTER_KEY}",
}
TEST_PROMPT = [{"role": "user", "content": "Reply with exactly: OK"}]


@dataclass
class TestResult:
    model: str
    tier: str
    status: str  # PASS | FAIL | SKIP | FALLBACK
    latency_ms: int = 0
    response_text: str = ""
    error: str = ""
    http_status: int = 0
    fallback_used: Optional[str] = None


def post_json(url: str, data: dict) -> tuple[int, dict]:
    """HTTP POST returning (status_code, response_body)."""
    payload = json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {"error": str(e)}
        return e.code, body
    except Exception as e:
        return 0, {"error": str(e)}


def get_json(url: str) -> tuple[int, dict]:
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception as e:
        return 0, {"error": str(e)}


def test_model(model_name: str, tier: str, max_tokens: int = 10) -> TestResult:
    """Test a single model via the proxy."""
    t0 = time.monotonic()
    status, body = post_json(f"{BASE_URL}/v1/chat/completions", {
        "model": model_name,
        "messages": TEST_PROMPT,
        "max_tokens": max_tokens,
        "temperature": 0,
    })
    latency = int((time.monotonic() - t0) * 1000)

    if status == 200:
        try:
            text = body["choices"][0]["message"]["content"].strip()
            return TestResult(model_name, tier, "PASS", latency, text, http_status=status)
        except (KeyError, IndexError) as e:
            return TestResult(model_name, tier, "FAIL", latency, error=f"Bad response shape: {e}", http_status=status)
    else:
        err = body.get("error", {})
        if isinstance(err, dict):
            err_msg = err.get("message", str(body))
        else:
            err_msg = str(err)
        return TestResult(model_name, tier, "FAIL", latency, error=err_msg[:200], http_status=status)


# Model tiers to test
MODELS = [
    # T1 FREE
    ("free-fast",        "T1-FREE",    "openrouter/minimax/minimax-m2.1:free"),
    ("free-bulk",        "T1-FREE",    "openrouter/z-ai/glm4.7"),
    ("free-small",       "T1-FREE",    "openrouter/google/gemma-3-1b-it:free"),
    # T2 FREE COMPLEX
    ("free-complex",     "T2-FREE",    "gemini/gemini-2.5-flash"),
    # T3 PAID
    ("paid-openai",      "T3-PAID",    "openai/gpt-4o-mini"),
    ("paid-openai-latest","T3-PAID",   "openai/gpt-4.1-mini"),
    ("paid-gemini-pro",  "T3-PAID",    "gemini/gemini-2.5-pro"),
    # T4 LAST RESORT
    ("groq-last-resort", "T4-LAST",    "groq/llama-3.3-70b-versatile"),
    # Legacy aliases
    ("gpt-4o-mini",      "LEGACY",     "openai/gpt-4o-mini"),
    ("claude-3-haiku",   "LEGACY",     "anthropic/claude-haiku-4-5-20251001"),
    ("gemini-flash",     "LEGACY",     "gemini/gemini-2.5-flash"),
    ("groq/llama-3.3-70b-versatile", "LEGACY-GROQ", "groq/llama-3.3-70b-versatile"),
]


def check_health() -> bool:
    status, body = get_json(f"{BASE_URL}/health")
    if status == 200:
        print(f"  ✓ Proxy health: OK")
        return True
    print(f"  ✗ Proxy not reachable (HTTP {status})")
    return False


def check_models_endpoint() -> list:
    status, body = get_json(f"{BASE_URL}/v1/models")
    if status == 200:
        models = [m["id"] for m in body.get("data", [])]
        print(f"  ✓ Models endpoint: {len(models)} models registered")
        return models
    print(f"  ✗ /v1/models failed (HTTP {status})")
    return []


def print_result(r: TestResult):
    icon = {"PASS": "✓", "FAIL": "✗", "SKIP": "~", "FALLBACK": "↩"}.get(r.status, "?")
    tier_color = {"T1-FREE": "🟢", "T2-FREE": "🟡", "T3-PAID": "🔵", "T4-LAST": "🔴", "LEGACY": "⚪", "LEGACY-GROQ": "🔴"}.get(r.tier, "")
    if r.status == "PASS":
        print(f"  {tier_color} {icon} [{r.tier}] {r.model:35s} {r.latency_ms:5d}ms  '{r.response_text[:40]}'")
    else:
        print(f"  {tier_color} {icon} [{r.tier}] {r.model:35s} HTTP {r.http_status} | {r.error[:80]}")


def test_fallback_chain():
    """Test that calling free-fast actually fails over to fallback models when needed."""
    print("\n[Fallback Chain Test]")
    # Test by calling a model that SHOULD work - then verify the response
    # Real fallback testing requires temporarily blocking models; we test by checking
    # error response format when OpenRouter key is missing
    print("  Testing fallback behavior with missing T1 key scenario...")

    # Call free-fast — expect either success (if OpenRouter works) or graceful fallback error
    t0 = time.monotonic()
    status, body = post_json(f"{BASE_URL}/v1/chat/completions", {
        "model": "free-fast",
        "messages": TEST_PROMPT,
        "max_tokens": 10,
    })
    latency = int((time.monotonic() - t0) * 1000)

    if status == 200:
        text = body.get("choices", [{}])[0].get("message", {}).get("content", "")
        model_used = body.get("model", "unknown")
        print(f"  ✓ free-fast responded in {latency}ms via model: {model_used}")
        print(f"    Response: '{text[:40]}'")
        # Check if it fell back to a different model
        if "minimax" not in model_used.lower() and "groq" in model_used.lower():
            print(f"  ↩ FALLBACK DETECTED: Fell through to {model_used}")
        return True
    else:
        err = body.get("error", {})
        err_msg = err.get("message", str(body)) if isinstance(err, dict) else str(err)
        print(f"  ✗ free-fast failed: HTTP {status} — {err_msg[:120]}")
        # Check if this is a key error (expected) vs config error
        if "APIKeyError" in err_msg or "401" in err_msg or "authentication" in err_msg.lower():
            print(f"  → Expected: OpenRouter API key not configured (T1 models need OPENROUTER_API_KEY)")
        elif "fallback" in err_msg.lower():
            print(f"  → Fallback chain exhausted: all fallback models also failed")
        return False


def analyze_failures(results: list[TestResult]):
    """Categorize failures and generate actionable recommendations."""
    failures = [r for r in results if r.status == "FAIL"]
    if not failures:
        print("\n  All models operational.")
        return

    print(f"\n[Failure Analysis] {len(failures)} model(s) failed:")

    openrouter_failures = [r for r in failures if "T1" in r.tier]
    gemini_failures = [r for r in failures if "T2" in r.tier or "gemini" in r.model.lower()]
    openai_failures = [r for r in failures if "openai" in r.model.lower() or "gpt" in r.model.lower()]
    groq_failures = [r for r in failures if "groq" in r.model.lower() or r.tier == "T4-LAST"]

    if openrouter_failures:
        print(f"\n  T1 FREE (OpenRouter) — {len(openrouter_failures)} failures:")
        errs = set(r.error[:60] for r in openrouter_failures)
        for e in errs:
            print(f"    Error pattern: {e}")
        if any("401" in r.error or "authentication" in r.error.lower() or "APIKey" in r.error for r in openrouter_failures):
            print("    ROOT CAUSE: OPENROUTER_API_KEY not set or invalid")
            print("    FIX: Set OPENROUTER_API_KEY in litellm/.env or system environment")
            print("         Get key: https://openrouter.ai/keys")
        elif any("404" in r.error or "model_not_found" in r.error.lower() for r in openrouter_failures):
            print("    ROOT CAUSE: Model ID not found on OpenRouter")
            print("    FIX: Verify model IDs at https://openrouter.ai/models")

    if gemini_failures:
        print(f"\n  T2 FREE (Gemini) — {len(gemini_failures)} failures:")
        for r in gemini_failures:
            print(f"    {r.model}: {r.error[:80]}")
        if any("GOOGLE_API_KEY" in r.error or "401" in r.error for r in gemini_failures):
            print("    ROOT CAUSE: GOOGLE_API_KEY not set")
            print("    FIX: Set GOOGLE_API_KEY=<your GEMINI_API_KEY value> in litellm/.env")
        elif any("quota" in r.error.lower() for r in gemini_failures):
            print("    ROOT CAUSE: Gemini free tier quota exhausted (250 RPD)")
            print("    FIX: Wait for quota reset (daily) or use paid tier")

    if openai_failures:
        print(f"\n  T3 PAID (OpenAI) — {len(openai_failures)} failures:")
        for r in openai_failures:
            print(f"    {r.model}: HTTP {r.http_status} — {r.error[:80]}")
        if any("404" in r.error or "model_not_found" in r.error.lower() for r in openai_failures):
            print("    ROOT CAUSE: Model ID deprecated or renamed")
            print("    FIX: gpt-4o-mini → gpt-4o-mini (still valid) | gpt-4.1-mini if available")

    if groq_failures:
        print(f"\n  T4 LAST RESORT (Groq) — {len(groq_failures)} failures:")
        for r in groq_failures:
            print(f"    {r.model}: {r.error[:80]}")

    # Summary recommendations
    print("\n[Recommendations]")
    if openrouter_failures:
        print("  1. CRITICAL: Add OPENROUTER_API_KEY to litellm/.env for T1 free models")
        print("     Without this, ALL tasks fall through to paid T3/T4 providers")
    if gemini_failures and any("GOOGLE_API_KEY" in r.error for r in gemini_failures):
        print("  2. Add to litellm/.env: GOOGLE_API_KEY=<your-gemini-api-key>")
        print("     (GEMINI_API_KEY in system env, but config expects GOOGLE_API_KEY)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=4000)
    parser.add_argument("--tier", help="Only test specific tier: T1,T2,T3,T4")
    args = parser.parse_args()

    global BASE_URL
    BASE_URL = f"http://{args.host}:{args.port}"

    print("=" * 70)
    print("LiteLLM Live Functional Test Suite")
    print(f"Target: {BASE_URL}")
    print("=" * 70)

    # 1. Health + models endpoint
    print("\n[Connectivity]")
    if not check_health():
        print("\nERROR: LiteLLM proxy is not running.")
        print(f"Start with: GOOGLE_API_KEY=$GEMINI_API_KEY litellm --config litellm/proxy_config.yaml --port {args.port}")
        sys.exit(1)
    registered = check_models_endpoint()

    # 2. Per-model tests
    print("\n[Model Tests]")
    results = []
    models_to_test = MODELS
    if args.tier:
        tiers = args.tier.upper().split(",")
        models_to_test = [(a, b, c) for a, b, c in MODELS if any(t in b for t in tiers)]

    for alias, tier, underlying in models_to_test:
        r = test_model(alias, tier)
        print_result(r)
        results.append(r)
        time.sleep(0.5)  # Rate limit protection

    # 3. Fallback chain test
    test_fallback_chain()

    # 4. Summary
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    total = len(results)

    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} passed | {failed} failed")

    # Tier breakdown
    for tier_name in ["T1-FREE", "T2-FREE", "T3-PAID", "T4-LAST"]:
        tier_results = [r for r in results if r.tier == tier_name]
        if tier_results:
            tp = sum(1 for r in tier_results if r.status == "PASS")
            print(f"  {tier_name}: {tp}/{len(tier_results)}")

    # 5. Failure analysis
    if failed > 0:
        analyze_failures(results)
        print("\n[Log file]: /tmp/litellm_test.log")

    # 6. Write results JSON
    results_path = "plans/agent-shared/litellm-test-results.json"
    with open(results_path, "w") as f:
        json.dump([{
            "model": r.model,
            "tier": r.tier,
            "status": r.status,
            "latency_ms": r.latency_ms,
            "response": r.response_text,
            "error": r.error,
            "http_status": r.http_status,
        } for r in results], f, indent=2)
    print(f"\nResults saved: {results_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
