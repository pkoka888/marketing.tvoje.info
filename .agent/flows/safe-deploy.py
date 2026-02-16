from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

# Define the state of our deployment process
class DeployState(TypedDict):
    build_status: str  # "pending", "success", "failed"
    test_status: str   # "pending", "success", "failed"
    deploy_status: str # "pending", "success", "failed", "aborted"
    logs: list[str]

# --- NODE 1: BUILD ---
def build_node(state: DeployState):
    print("🚀 Starting Build...")
    # Simulate build process (e.g., npm run build)
    # In real scenario: subprocess.run(["npm", "run", "build"])
    state["logs"].append("Build completed successfully.")
    return {"build_status": "success"}

# --- NODE 2: TEST ---
def test_node(state: DeployState):
    print("🧪 Running Tests...")
    # Simulate testing (e.g., npm run test)
    state["logs"].append("Tests passed.")
    return {"test_status": "success"}

# --- NODE 3: DEPLOY ---
def deploy_node(state: DeployState):
    print("🚢 Deploying to Production...")
    # Simulate deploy (e.g., git push or scp)
    state["logs"].append("Deployment successful.")
    return {"deploy_status": "success"}

# --- CONDITION: GATEKEEPER ---
def check_safety(state: DeployState) -> Literal["deploy", "abort"]:
    if state["build_status"] == "success" and state["test_status"] == "success":
        return "deploy"
    return "abort"

# --- GRAVEYARD (Abort) ---
def abort_node(state: DeployState):
    print("🛑 Deployment Aborted due to failures.")
    return {"deploy_status": "aborted"}

# --- GRAPH DEFINITION ---
workflow = StateGraph(DeployState)

# Add nodes
workflow.add_node("build", build_node)
workflow.add_node("test", test_node)
workflow.add_node("deploy", deploy_node)
workflow.add_node("abort", abort_node)

# Add edges
workflow.set_entry_point("build")
workflow.add_edge("build", "test")

# Conditional edge from test -> deploy or abort
workflow.add_conditional_edges(
    "test",
    check_safety,
    {
        "deploy": "deploy",
        "abort": "abort"
    }
)

workflow.add_edge("deploy", END)
workflow.add_edge("abort", END)

# Compile
app = workflow.compile()

if __name__ == "__main__":
    # Test run
    initial_state = {
        "build_status": "pending",
        "test_status": "pending",
        "deploy_status": "pending",
        "logs": []
    }
    result = app.invoke(initial_state)
    print("\nFinal State:", result)
