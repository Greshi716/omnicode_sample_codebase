import json

from omnicode_core.hooks import HookType, get_hook_registry

from lending_app import hooks, tools  # noqa: F401  (importing registers the handlers)
from lending_app.config import ROOT, WORKSPACE
from lending_app.tools import catalog_search


def test_workspace_is_defined_in_python():
    assert WORKSPACE.name == "omnicode-sample-app"
    assert "com.example.library" in WORKSPACE.masking.package_prefixes
    assert "^LIB_" in WORKSPACE.masking.table_patterns
    assert "LibraryCorp" in WORKSPACE.masking.org_terms
    assert WORKSPACE.host.mcp_command[-1] == "serve"


def test_mcp_config_launches_the_app_entry_point():
    cfg = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = cfg["mcpServers"]["omnicode"]
    assert server["args"] == ["main.py", "serve"]


def test_seeded_bugs_point_at_real_methods_and_do_not_leak_answers():
    bugs = json.loads((ROOT / "eval" / "bugs.json").read_text(encoding="utf-8"))["bugs"]
    assert [b["bug_id"] for b in bugs] == ["BUG-001", "BUG-002", "BUG-003"]
    for bug in bugs:
        source = (ROOT / bug["culprit_file"]).read_text(encoding="utf-8")
        assert bug["culprit_method"].split("(")[0] in source
    for java in (ROOT / "src").rglob("*.java"):
        text = java.read_text(encoding="utf-8")
        assert "SEEDED" not in text and "// BUG" not in text, f"{java.name} reveals the answer"


def test_catalog_search_filters():
    assert [b["book_id"] for b in catalog_search("design")["results"]] == ["BK-101"]
    assert catalog_search("")["results"] == []


def test_before_tool_hook_blocks_destructive_sql():
    registry = get_hook_registry()
    blocked = registry.trigger(HookType.BEFORE_TOOL, "s", {"tool": "t", "arguments": {"q": "DROP TABLE LIB_LOANS"}})
    allowed = registry.trigger(HookType.BEFORE_TOOL, "s", {"tool": "t", "arguments": {"q": "overdue fine"}})
    assert blocked.action == "BLOCK"
    assert allowed.action != "BLOCK"


def test_before_prompt_hook_blocks_card_numbers():
    res = get_hook_registry().trigger(HookType.BEFORE_PROMPT, "s", "card 4111 1111 1111 1111")
    assert res.action == "BLOCK"


def test_log_analysis_zero_leak():
    from omnicode_mcp.server import OmniCodeMCPServer
    server = OmniCodeMCPServer(repo_root=ROOT)
    trace = (
        "java.lang.NullPointerException: Cannot invoke MemberTier.getPriority()\n"
        "    at com.example.library.service.ReservationService.enqueueReservation(ReservationService.java:32)\n"
    )
    res = server.safe_call("analyze_logs", raw_trace=trace)
    assert "error_anchor" in res
    assert server.leak_scanner.find(json.dumps(res, default=str)) == []
