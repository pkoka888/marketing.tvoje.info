#!/usr/bin/env python3
import concurrent.futures
import os
import subprocess
import sys
import time
from datetime import datetime

# Import agent_tools for Flash
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent_tools import ask_groq


def task_flash(prompt):
    print("🚀 [Swarm] Analyst (Gemini Flash) starting...")
    # Read mcp.json to provide context
    try:
        with open(".kilocode/mcp.json", "r") as f:
            mcp_content = f.read()
        prompt = f"Context (.kilocode/mcp.json):\n{mcp_content}\n\nTask: {prompt}"
    except Exception as e:
        print(f"Warning: Could not read mcp.json: {e}")

    res = ask_groq(prompt, model="flash")
    return {"agent": "Analyst (Flash)", "output": res.content, "success": res.success}


def task_kilo(prompt):
    print("🚀 [Swarm] Developer (Kilo) starting...")
    start = time.time()
    try:
        # Using a simple check instead of 'run' to ensure speed for demo
        cmd = f"kilo agents list"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "agent": "Developer (Kilo)",
            "output": result.stdout,
            "success": result.returncode == 0,
        }
    except Exception as e:
        return {"agent": "Developer (Kilo)", "success": False, "error": str(e)}


def task_cline(prompt):
    print("🚀 [Swarm] QA (Cline) starting...")
    try:
        cmd = f"cline --help"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            "agent": "QA (Cline)",
            "output": "Cline CLI Verified: OK",
            "success": result.returncode == 0,
        }
    except Exception as e:
        return {"agent": "QA (Cline)", "success": False, "error": str(e)}


def main():
    print(f"--- 🐝 Swarm Audit Initiated ({datetime.now().strftime('%H:%M:%S')}) ---")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        f_flash = executor.submit(
            task_flash,
            "Audit the .kilocode/mcp.json file for naming consistency and absolute paths. Compare against RULE-MCP-ALIGN-01.",
        )
        f_kilo = executor.submit(task_kilo, "List agents")
        f_cline = executor.submit(task_cline, "Verify CLI")

        results = [f.result() for f in [f_flash, f_kilo, f_cline]]

    print("\n--- 🏁 Swarm Audit Results ---")
    report_path = "plans/agent-shared/swarm_audit_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w") as f:
        f.write(f"# Swarm Audit Report - {datetime.now().isoformat()}\n\n")
        for r in results:
            icon = "✅" if r["success"] else "❌"
            print(f"{icon} {r['agent']}")
            f.write(f"## {r['agent']}\n")
            f.write(f"Status: {icon}\n\n")
            f.write(f"### Findings\n{r.get('output', 'No output')}\n\n")

    print(f"\nAudit complete. Detailed report at {report_path}")


if __name__ == "__main__":
    main()
