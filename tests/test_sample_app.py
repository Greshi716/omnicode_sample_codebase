import sys
import os
import json
from pathlib import Path
import pytest

# Ensure omnicode-core is accessible
try:
    import omnicode_core
except ImportError:
    candidate = os.getenv("OMNICODE_CORE_PATH") or (Path(__file__).parent.parent.parent / "Project")
    if Path(candidate).exists():
        sys.path.insert(0, str(Path(candidate).resolve()))

from omnicode_core.workspace import load_workspace
from omnicode_core.tools import get_tool_registry
from omnicode_mcp.server import OmniCodeMCPServer

# Add sample app root to sys.path to import plugin
app_root = Path(__file__).parent.parent.resolve()
if str(app_root) not in sys.path:
    sys.path.insert(0, str(app_root))

import plugin


@pytest.fixture
def mcp_server():
    return OmniCodeMCPServer(repo_root=app_root)


def test_sample_app_workspace_config():
    ws_file = app_root / "omnicode.workspace.yaml"
    assert ws_file.exists()

    ws = load_workspace(ws_file)
    assert ws.name == "omnicode-sample-app"
    assert "com.example.library" in ws.masking.package_prefixes
    assert "^LIB_" in ws.masking.table_patterns
    assert "LibraryCorp" in ws.masking.org_terms


def test_sample_app_seeded_bugs_benchmark():
    bugs_path = app_root / "eval" / "bugs.json"
    assert bugs_path.exists()

    with open(bugs_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "bugs" in data
    assert len(data["bugs"]) == 3
    bug_ids = [b["bug_id"] for b in data["bugs"]]
    assert "BUG-001" in bug_ids
    assert "BUG-002" in bug_ids
    assert "BUG-003" in bug_ids


def test_sample_app_custom_plugin_and_tools():
    registry = get_tool_registry()
    tool_def = registry.get_tool("catalog_search")
    assert tool_def is not None
    assert tool_def.name == "catalog_search"

    res = tool_def.fn(query="Design Patterns")
    assert "results" in res
    assert len(res["results"]) == 2


def test_sample_app_log_analysis_zero_leak(mcp_server):
    trace = """
    java.lang.NullPointerException: Cannot invoke MemberTier.getPriority()
        at com.example.library.service.ReservationService.enqueueReservation(ReservationService.java:32)
        at com.example.library.service.LendingService.checkoutBook(LendingService.java:38)
    """
    res = mcp_server.safe_call("analyze_logs", raw_trace=trace)
    assert isinstance(res, dict)
    assert "error_anchor" in res
    assert "com.example.library" not in str(res)
