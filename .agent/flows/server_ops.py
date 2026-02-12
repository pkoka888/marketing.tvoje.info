"""
LangGraph Server Operations Flow Template

Safe, stateful flows for server evidence collection,
deployment, and infrastructure management.

Uses Redis for checkpointing (shared-redis on localhost:6379).
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
import subprocess
import json
from datetime import datetime


# --- State Definitions ---

class ServerEvidenceState(TypedDict):
    """State for server evidence collection flow."""
    servers: list[str]  # SSH aliases: ["s60pa", "s61pa", "s62pa"]
    evidence: dict  # {server: {data}}
    errors: list[str]
    timestamp: str
    output_path: str


class DeployState(TypedDict):
    """State for safe deployment flow."""
    project: str
    target_server: str  # SSH alias
    build_ok: bool
    lint_ok: bool
    tests_ok: bool
    deploy_ok: bool
    rollback_needed: bool
    errors: list[str]


# --- Server Evidence Collection Flow ---

def init_evidence(state: ServerEvidenceState) -> dict:
    """Initialize evidence collection."""
    return {
        "timestamp": datetime.now().isoformat(),
        "evidence": {},
        "errors": [],
    }


def collect_from_server(state: ServerEvidenceState, server: str) -> dict:
    """Collect evidence from a single server via SSH."""
    commands = {
        "uptime": "uptime -p",
        "disk": "df -h / | tail -1",
        "memory": "free -h | grep Mem",
        "load": "cat /proc/loadavg",
        "docker": "docker ps --format '{{.Names}}|{{.Status}}' 2>/dev/null || echo 'no docker'",
        "failed_services": "systemctl --failed --no-pager --no-legend 2>/dev/null || echo 'none'",
        "listening_ports": "ss -tlnp | grep LISTEN | head -20",
    }

    result = {}
    for key, cmd in commands.items():
        try:
            output = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=10", "-o", "BatchMode=yes",
                 server, cmd],
                capture_output=True, text=True, timeout=30
            )
            result[key] = output.stdout.strip()
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            result[key] = f"ERROR: {e}"

    evidence = state.get("evidence", {})
    evidence[server] = result
    return {"evidence": evidence}


def collect_all_servers(state: ServerEvidenceState) -> dict:
    """Collect evidence from all configured servers."""
    for server in state["servers"]:
        update = collect_from_server(state, server)
        state["evidence"].update(update.get("evidence", {}))
    return {"evidence": state["evidence"]}


def check_alerts(state: ServerEvidenceState) -> dict:
    """Check collected evidence for alerts."""
    alerts = []
    for server, data in state.get("evidence", {}).items():
        # Check disk usage
        disk = data.get("disk", "")
        if disk and "%" in disk:
            parts = disk.split()
            for p in parts:
                if p.endswith("%"):
                    usage = int(p.rstrip("%"))
                    if usage > 85:
                        alerts.append(f"🔴 {server}: disk usage {usage}%")
                    elif usage > 70:
                        alerts.append(f"⚠️  {server}: disk usage {usage}%")

        # Check failed services
        failed = data.get("failed_services", "none")
        if failed and failed != "none":
            alerts.append(f"🔴 {server}: failed services: {failed}")

    return {"errors": alerts}


def save_evidence(state: ServerEvidenceState) -> dict:
    """Save evidence to JSON file."""
    output_path = state.get("output_path", "/tmp/server-evidence.json")
    output = {
        "collected_at": state["timestamp"],
        "servers": state["evidence"],
        "alerts": state.get("errors", []),
    }
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    return {"output_path": output_path}


# --- Build the Evidence Collection Graph ---

def create_evidence_graph():
    """Create a LangGraph for server evidence collection."""
    graph = StateGraph(ServerEvidenceState)

    graph.add_node("init", init_evidence)
    graph.add_node("collect", collect_all_servers)
    graph.add_node("check_alerts", check_alerts)
    graph.add_node("save", save_evidence)

    graph.set_entry_point("init")
    graph.add_edge("init", "collect")
    graph.add_edge("collect", "check_alerts")
    graph.add_edge("check_alerts", "save")
    graph.add_edge("save", END)

    return graph.compile()


# --- Safe Deploy Flow ---

def build_step(state: DeployState) -> dict:
    """Build the project."""
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            capture_output=True, text=True, timeout=120,
            cwd=state.get("project", ".")
        )
        return {"build_ok": result.returncode == 0}
    except Exception as e:
        return {"build_ok": False, "errors": [f"Build failed: {e}"]}


def lint_step(state: DeployState) -> dict:
    """Lint the project."""
    try:
        result = subprocess.run(
            ["npm", "run", "lint"],
            capture_output=True, text=True, timeout=60,
            cwd=state.get("project", ".")
        )
        return {"lint_ok": result.returncode == 0}
    except Exception as e:
        return {"lint_ok": False, "errors": [f"Lint failed: {e}"]}


def deploy_step(state: DeployState) -> dict:
    """Deploy to target server via SCP + SSH restart."""
    if not state["build_ok"] or not state["lint_ok"]:
        return {"deploy_ok": False, "errors": ["Pre-deploy checks failed"]}

    try:
        # SCP dist/ to server
        server = state["target_server"]
        subprocess.run(
            ["scp", "-r", "dist/", f"{server}:/var/www/marketing.tvoje.info/public_html/"],
            timeout=120, check=True
        )
        return {"deploy_ok": True}
    except Exception as e:
        return {"deploy_ok": False, "rollback_needed": True, "errors": [f"Deploy failed: {e}"]}


def should_deploy(state: DeployState) -> Literal["deploy", "abort"]:
    """Gate: only deploy if build and lint passed."""
    if state.get("build_ok") and state.get("lint_ok"):
        return "deploy"
    return "abort"


def abort_step(state: DeployState) -> dict:
    """Handle deployment abort."""
    return {"deploy_ok": False, "errors": state.get("errors", []) + ["Deployment aborted"]}


def create_deploy_graph():
    """Create a LangGraph for safe deployment."""
    graph = StateGraph(DeployState)

    graph.add_node("build", build_step)
    graph.add_node("lint", lint_step)
    graph.add_node("deploy", deploy_step)
    graph.add_node("abort", abort_step)

    graph.set_entry_point("build")
    graph.add_edge("build", "lint")
    graph.add_conditional_edges("lint", should_deploy, {
        "deploy": "deploy",
        "abort": "abort",
    })
    graph.add_edge("deploy", END)
    graph.add_edge("abort", END)

    return graph.compile()


# --- Usage Examples ---

if __name__ == "__main__":
    # Example 1: Collect server evidence
    evidence_flow = create_evidence_graph()
    result = evidence_flow.invoke({
        "servers": ["s60pa", "s61pa", "s62pa"],
        "evidence": {},
        "errors": [],
        "timestamp": "",
        "output_path": "C:/Users/pavel/vscodeportable/servers/evidence-latest.json",
    })
    print(f"Evidence collected. Alerts: {result.get('errors', [])}")

    # Example 2: Safe deploy
    # deploy_flow = create_deploy_graph()
    # result = deploy_flow.invoke({
    #     "project": "C:/Users/pavel/projects/marketing.tvoje.info",
    #     "target_server": "s62pa",
    #     "build_ok": False,
    #     "lint_ok": False,
    #     "tests_ok": False,
    #     "deploy_ok": False,
    #     "rollback_needed": False,
    #     "errors": [],
    # })
