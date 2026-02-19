#!/usr/bin/env python3
"""
Audit Fix Orchestrator
Executes audit fixes in parallel using subagents (Kilo Code free model).

Usage:
    python scripts/orchestrate_audit_fixes.py
    python scripts/orchestrate_audit_fixes.py --dry-run
"""

import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

# Configuration
MODEL = "x-ai/grok-code-fast-1:optimized:free"
TIMEOUT = 300  # 5 minutes per task


class AuditFixOrchestrator:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.results: List[Dict[str, Any]] = []
        
    def run_subagent(self, task: Dict[str, str]) -> Dict[str, Any]:
        """Execute a single subagent task via Kilo Code."""
        agent_name = task["agent"]
        prompt = task["prompt"]
        files = task.get("files", [])
        
        print(f"\n🚀 [{agent_name}] Starting task: {task['description']}")
        print(f"   Files: {', '.join(files)}")
        
        start_time = time.time()
        
        if self.dry_run:
            print(f"   ⚠️  DRY RUN - Would execute:")
            print(f"       {prompt[:200]}...")
            return {
                "agent": agent_name,
                "success": True,
                "duration": 0,
                "files": files,
                "status": "dry_run"
            }
        
        # Build Kilo command
        cmd = f'kilo run --model {MODEL} --prompt "{prompt}"'
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )
            
            success = result.returncode == 0
            duration = time.time() - start_time
            
            if success:
                print(f"   ✅ Completed in {duration:.2f}s")
            else:
                print(f"   ❌ Failed in {duration:.2f}s")
                print(f"   Error: {result.stderr[:200] if result.stderr else 'Unknown'}")
            
            return {
                "agent": agent_name,
                "success": success,
                "output": result.stdout[:500] if result.stdout else "",
                "error": result.stderr[:500] if result.stderr else "",
                "duration": duration,
                "files": files,
                "status": "completed"
            }
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"   ⏱️  Timeout after {duration:.2f}s")
            return {
                "agent": agent_name,
                "success": False,
                "error": "Timeout",
                "duration": duration,
                "files": files,
                "status": "timeout"
            }
        except Exception as e:
            duration = time.time() - start_time
            print(f"   ❌ Error: {str(e)[:100]}")
            return {
                "agent": agent_name,
                "success": False,
                "error": str(e),
                "duration": duration,
                "files": files,
                "status": "error"
            }
    
    def run_parallel(self, tasks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Execute all tasks in parallel using ThreadPoolExecutor."""
        print(f"\n{'='*60}")
        print(f"🎯 PARALLEL ORCHESTRATION - {len(tasks)} Subagents")
        print(f"   Model: {MODEL}")
        print(f"   Dry Run: {self.dry_run}")
        print(f"{'='*60}")
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            # Submit all tasks
            futures = {
                executor.submit(self.run_subagent, task): task 
                for task in tasks
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        "agent": task["agent"],
                        "success": False,
                        "error": str(e),
                        "files": task.get("files", []),
                        "status": "exception"
                    })
        
        return results
    
    def run_sequential_gate(self, gate_name: str, command: str) -> bool:
        """Execute a sequential gate (verification step)."""
        print(f"\n{'='*60}")
        print(f"🚪 SEQUENTIAL GATE: {gate_name}")
        print(f"   Command: {command}")
        print(f"{'='*60}")
        
        if self.dry_run:
            print(f"   ⚠️  DRY RUN - Would execute: {command}")
            return True
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            success = result.returncode == 0
            
            if success:
                print(f"   ✅ Gate passed (exit {result.returncode})")
                if result.stdout:
                    # Show last 10 lines of output
                    lines = result.stdout.strip().split('\n')
                    print(f"   Output: {' | '.join(lines[-3:])}")
            else:
                print(f"   ❌ Gate failed (exit {result.returncode})")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Gate timeout")
            return False
        except Exception as e:
            print(f"   ❌ Gate error: {str(e)[:100]}")
            return False
    
    def generate_report(self, results: List[Dict[str, Any]], gates_passed: bool) -> str:
        """Generate execution report."""
        report = []
        report.append("# Audit Fix Orchestration Report")
        report.append("")
        report.append(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Model**: {MODEL}")
        report.append(f"**Dry Run**: {self.dry_run}")
        report.append("")
        
        # Summary
        total = len(results)
        successful = sum(1 for r in results if r.get("success"))
        failed = total - successful
        
        report.append("## Summary")
        report.append("")
        report.append(f"| Metric | Value |")
        report.append(f"|--------|-------|")
        report.append(f"| Total Tasks | {total} |")
        report.append(f"| Successful | {successful} |")
        report.append(f"| Failed | {failed} |")
        report.append(f"| Gates Passed | {'✅ Yes' if gates_passed else '❌ No'} |")
        report.append("")
        
        # Task Results
        report.append("## Task Results")
        report.append("")
        for r in results:
            status = "✅" if r.get("success") else "❌"
            agent = r.get("agent", "unknown")
            files = ", ".join(r.get("files", []))
            duration = r.get("duration", 0)
            error = r.get("error", "")
            
            report.append(f"- {status} **{agent}** ({duration:.1f}s)")
            report.append(f"  - Files: {files}")
            if error:
                report.append(f"  - Error: {error[:100]}")
        report.append("")
        
        return "\n".join(report)
    
    def execute(self):
        """Main execution flow."""
        # Define parallel tasks (Phase 1 & 2)
        tasks = [
            {
                "agent": "bmad-fix-chinese",
                "description": "Fix Chinese character corruption in plan-approval-required",
                "prompt": "Fix the Chinese character corruption in all 4 copies of plan-approval-required. Find 'cannot胜任' and replace with 'cannot handle the task'. Files: .kilocode/rules/plan-approval-required, .agents/rules/plan-approval-required, .clinerules/skills/plan-approval-required, .gemini/rules/plan-approval-required",
                "files": [
                    ".kilocode/rules/plan-approval-required",
                    ".agents/rules/plan-approval-required",
                    ".clinerules/skills/plan-approval-required",
                    ".gemini/rules/plan-approval-required"
                ]
            },
            {
                "agent": "bmad-fix-tiers",
                "description": "Fix LiteLLM tier labels in cost-optimization",
                "prompt": "Fix the LiteLLM tier labels in all 4 copies of cost-optimization. Replace the LiteLLM section with: '### LiteLLM (Self-Hosted Proxy, port 4000)\nSee `litellm/proxy_config.yaml` for full config:\n- T1 FREE: `minimax-free`, `glm4-free`, `qwen3-coder-free`, `deepseek-r1-free` (OpenRouter)\n- T2 FREE: `gemini-flash` (15 RPM), `gemini-pro` (2 RPM) (Google free tier)\n- T3 PAID: `groq-llama-8b` ($0.05/$0.08), `groq-llama-70b` ($0.59/$0.79) (Groq)\n- T4 PAID: `gpt-4o-mini` (OpenAI — last resort)\nFallback chain: T1 → T2 → T3 → T4'. Files: .kilocode/rules/cost-optimization, .agents/rules/cost-optimization, .clinerules/skills/cost-optimization, .gemini/rules/cost-optimization",
                "files": [
                    ".kilocode/rules/cost-optimization",
                    ".agents/rules/cost-optimization",
                    ".clinerules/skills/cost-optimization",
                    ".gemini/rules/cost-optimization"
                ]
            },
            {
                "agent": "bmad-fix-agent-name",
                "description": "Fix new_plan.py agent name",
                "prompt": "In scripts/new_plan.py line 28, change `\"{{AGENT_NAME}}\": lambda: \"Cline\",` to `\"{{AGENT_NAME}}\": lambda: \"Agent\",",
                "files": ["scripts/new_plan.py"]
            },
            {
                "agent": "bmad-fix-typo",
                "description": "Fix GAP_ANALYSIS typo",
                "prompt": "In plans/templates/GAP_ANALYSIS.md, fix the typo: change 'RESEARCH_FFINDINGS' to 'RESEARCH_FINDINGS'",
                "files": ["plans/templates/GAP_ANALYSIS.md"]
            },
            {
                "agent": "bmad-update-context",
                "description": "Update memory-bank context",
                "prompt": "Update .kilocode/rules/memory-bank/context.md with: '# Context — Current Task\n\n- Phase: POST_IMPLEMENTATION_CLEANUP\n- Active tasks: Fix audit findings, prepare commit\n- Last verified: 2026-02-19 (verify_agentic_platform.py: PASS)\n- Uncommitted: 79 files (plan-approval-required, cost-opt, templates, API hardening)'",
                "files": [".kilocode/rules/memory-bank/context.md"]
            },
            {
                "agent": "bmad-create-readme",
                "description": "Create scripts/README.md",
                "prompt": "Create scripts/README.md with documentation for all scripts. Include a table with Script, Purpose, Creator columns. List: verify_agentic_platform.py (Cross-agent integrity check, Claude Code), verify_api_keys.py (API key verification, Kilo Code), validate_kilo_configs.py (YAML/JSON schema, Kilo Code), template_reference_manager.py (Template metadata, Claude Code), populate_template_references.py (Template cross-refs, Claude Code), validate_template_references.py (Template validation, Claude Code), template_index.py (Cross-reference table, Claude Code), new_plan.py (Plan creator, Cline + Kilo), generate_images.py (AI image generation, Claude Code), orchestrate_flash.py (Flash orchestration, Kilo Code), orchestrate_subagents.py (Subagent orchestration, Kilo Code), swarm_audit.py (Swarm audit, Kilo Code), update_free_models.py (Free model updater, Kilo Code), search_npm.py (NPM search, Kilo Code), setup_mcp_servers.py (MCP setup, Kilo Code), check_redis.py (Redis check, Claude Code), validate_env.py (Env validation, Kilo Code), protected/snapshot_config.py (Config drift, Kilo Code)",
                "files": ["scripts/README.md"]
            },
            {
                "agent": "bmad-refactor-dry",
                "description": "DRY refactor snapshot_config.py",
                "prompt": "Refactor scripts/protected/snapshot_config.py to import API_KEYS_CONFIG from scripts/verify_api_keys.py instead of hardcoding. Add try/except with fallback to hardcoded config for resilience.",
                "files": ["scripts/protected/snapshot_config.py"]
            }
        ]
        
        # Phase 1 & 2: Parallel execution
        results = self.run_parallel(tasks)
        
        # Phase 3: Sequential gates (verification)
        gates = [
            ("verify_agentic_platform", "python scripts/verify_agentic_platform.py"),
            ("validate_template_references", "python scripts/validate_template_references.py"),
            ("new_plan_list", "python scripts/new_plan.py --list")
        ]
        
        gates_passed = True
        for gate_name, command in gates:
            if not self.run_sequential_gate(gate_name, command):
                gates_passed = False
                print(f"\n⚠️  Gate '{gate_name}' failed - continuing with remaining gates")
        
        # Generate report
        report = self.generate_report(results, gates_passed)
        print(f"\n\n{report}")
        
        # Save report
        report_path = Path("plans/agent-shared/audit-fix-orchestration-report.md")
        report_path.write_text(report)
        print(f"\n📄 Report saved to: {report_path}")
        
        # Exit code
        all_success = all(r.get("success") for r in results)
        if all_success and gates_passed:
            print(f"\n🎉 ALL TASKS COMPLETED SUCCESSFULLY")
            return 0
        else:
            print(f"\n⚠️  SOME TASKS FAILED - Check report for details")
            return 1


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit Fix Orchestrator")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()
    
    orchestrator = AuditFixOrchestrator(dry_run=args.dry_run)
    return orchestrator.execute()


if __name__ == "__main__":
    sys.exit(main())
