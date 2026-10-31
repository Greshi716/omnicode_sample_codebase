"""
Main entry point for the Library Lending application using omnicode-core as a library.
Demonstrates:
  1. Loading app workspace configuration.
  2. Registering app plugins (custom @tool and @hook).
  3. Starting OmniCode MCP server or launching the AI diagnostic Agent.
"""

import sys
import os
from pathlib import Path

# Resolve omnicode library from environment, installed site-packages, or sibling directory
try:
    import omnicode_core
except ImportError:
    candidate = os.getenv("OMNICODE_CORE_PATH") or (Path(__file__).parent.parent / "Project")
    if Path(candidate).exists():
        sys.path.insert(0, str(Path(candidate).resolve()))

from omnicode_core.workspace import load_workspace, set_active_workspace
from omnicode_core.server import create_mcp_server
from omnicode_core.agent import Agent
from omnicode_core.tools import get_tool_registry

# Import local application plugin (registers @tool and @hook)
import plugin


def run_app():
    app_root = Path(__file__).parent.resolve()
    ws_file = app_root / "omnicode.workspace.yaml"
    
    print(f"Loading workspace config from: {ws_file}")
    workspace = load_workspace(ws_file)
    set_active_workspace(workspace)
    print(f"Active Workspace: {workspace.name}")
    print(f"Registered Custom Tools: {[t.name for t in get_tool_registry().list_tools()]}")

    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        print("\nStarting FastMCP server on stdio...")
        mcp_server = create_mcp_server(repo_root=app_root)
        mcp_server.run(transport="stdio")
    elif len(sys.argv) > 1 and sys.argv[1] == "--diagnose":
        query = sys.argv[2] if len(sys.argv) > 2 else "Analyze why loan overdue fine is charging $1.50 extra on due date"
        print(f"\nRunning AI Diagnostic Agent on inquiry: '{query}'")
        agent = Agent(workspace=workspace)
        result = agent.run(prompt=query)
        print("\n=== Agent Resolution ===")
        print(result.get("response", result))
    else:
        print("\nUsage:")
        print("  python main.py --serve         # Launch FastMCP server on stdio for Claude Code / MCP clients")
        print("  python main.py --diagnose [Q]  # Run omnicode-core programmatic diagnostic Agent")


if __name__ == "__main__":
    run_app()
