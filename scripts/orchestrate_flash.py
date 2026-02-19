#!/usr/bin/env python3
"""
Parallel Orchestrator (Flash)
Uses Gemini 1.5 Flash via LiteLLM to run parallel subagent tasks.
"""
import concurrent.futures
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

# Ensure we can import from the scripts directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent_tools import AgentResponse, ask_groq


def run_flash_task(
    task_name: str, prompt: str, system_prompt: str = ""
) -> Dict[str, Any]:
    """Runs a single task using the Gemini Flash model."""
    print(f"🚀 Starting task: {task_name}")
    start_time = datetime.now()

    # Using 'flash' model as defined in agent_tools.py
    response = ask_groq(prompt=prompt, model="flash", system_prompt=system_prompt)

    duration = (datetime.now() - start_time).total_seconds()

    return {
        "task": task_name,
        "success": response.success,
        "content": response.content,
        "duration": duration,
        "error": response.error,
    }


def orchestrate_parallel(tasks: List[Dict[str, str]], max_workers: int = 5):
    """Orchestrates multiple tasks in parallel."""
    results = []

    print(f"--- 🤖 Parallel Orchestrator (Model: Gemini Flash) ---")
    print(f"Workers: {max_workers} | Tasks: {len(tasks)}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                run_flash_task, t["name"], t["prompt"], t.get("system", "")
            ): t
            for t in tasks
        }

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return results


def main():
    # Example usage for verification
    test_tasks = [
        {
            "name": "Market Research",
            "prompt": "List 3 top digital marketing trends for 2026 in the Czech Republic.",
            "system": "You are a senior marketing strategist.",
        },
        {
            "name": "Audit Fix",
            "prompt": "Generate a brief summary of how to prevent tool call failures in agentic systems.",
            "system": "You are a system architect.",
        },
    ]

    results = orchestrate_parallel(test_tasks)

    print("\n--- 🏁 Orchestration Results ---")
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"{status} {r['task']} ({r['duration']:.2f}s)")
        if not r["success"]:
            print(f"   Error: {r['error']}")


if __name__ == "__main__":
    main()
