#!/usr/bin/env python3
import concurrent.futures
import json
import os
import subprocess
import time


def run_kilo(task):
    print(f"🚀 [Orchestrator] Starting Kilo task: {task}")
    start = time.time()
    # Kilo CLI assumes it has access to the project
    cmd = f'kilo run --prompt "{task}"'
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=300
        )
        return {
            "agent": "kilo",
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "duration": time.time() - start,
        }
    except Exception as e:
        return {"agent": "kilo", "success": False, "error": str(e)}


def run_cline(task):
    print(f"🚀 [Orchestrator] Starting Cline task: {task}")
    start = time.time()
    # Cline CLI might have different args, assuming 'run' or similar exists
    # If not, we might need to use a different approach
    cmd = f'cline "{task}"'
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=300
        )
        return {
            "agent": "cline",
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "duration": time.time() - start,
        }
    except Exception as e:
        return {"agent": "cline", "success": False, "error": str(e)}


def main():
    tasks = [
        {
            "agent": "kilo",
            "prompt": "Audit the current MCP configuration in .kilocode/mcp.json and check for missing servers.",
        },
        {
            "agent": "cline",
            "prompt": "Analyze the npm auth issue ('Access token expired or revoked') and suggest a workaround for installing new packages globally.",
        },
    ]

    print("--- 🤖 Parallel Orchestration (Kilo & Cline) ---")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        if any(t["agent"] == "kilo" for t in tasks):
            futures.append(
                executor.submit(
                    run_kilo, next(t["prompt"] for t in tasks if t["agent"] == "kilo")
                )
            )
        if any(t["agent"] == "cline" for t in tasks):
            futures.append(
                executor.submit(
                    run_cline, next(t["prompt"] for t in tasks if t["agent"] == "cline")
                )
            )

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    print("\n--- 🏁 Performance Summary ---")
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"{status} {r['agent']} completed in {r.get('duration', 0):.2f}s")
        if not r["success"]:
            print(f"   Error: {r['error']}")

    # Aggregating results into a report
    report_path = "plans/agent-shared/orchestration_results.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        f.write("# Parallel Orchestration Results\n\n")
        for r in results:
            f.write(f"## Agent: {r['agent']}\n")
            f.write(f"Status: {'Success' if r['success'] else 'Failure'}\n")
            f.write(f"Duration: {r.get('duration', 0):.2f}s\n\n")
            f.write("### Output\n")
            f.write(f"```\n{r.get('output', 'No output')}\n```\n\n")
            if r.get("error"):
                f.write("### Error\n")
                f.write(f"```\n{r['error']}\n```\n\n")

    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()
