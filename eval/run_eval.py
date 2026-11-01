"""Seeded-bug benchmark for the library lending sample app.

For each bug in eval/bugs.json the benchmark asks the retrieval tools the question a
developer would ask (the symptom) and measures, against the known culprit:

  - method hit@1 / hit@3 and class hit@3 among the masked search_code results
    (decoded locally with the session vault, so the check never leaves this machine);
  - whether analyze_logs finds an error anchor in a stack trace for the culprit;
  - leak count: scanner hits across every tool output. This is a hard gate.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List

from omnicode_core.workspace import set_active_workspace
from omnicode_mcp.server import OmniCodeMCPServer

from lending_app.config import ROOT, WORKSPACE

TOP_K = 3


def _trace(bug: Dict[str, Any]) -> str:
    fqn = bug["culprit_file"].removeprefix("src/main/java/").removesuffix(".java").replace("/", ".")
    method = bug["culprit_method"].split("(")[0]
    return f"java.lang.Exception: {bug['symptom']}\n    at {fqn}.{method}({Path(bug['culprit_file']).name}:1)\n"


def _hit(server: OmniCodeMCPServer, sid: str, items: List[Any], needle: str, k: int) -> bool:
    needle = needle.lower()
    return any(
        needle in server.session_manager.decode_masked_text(sid, json.dumps(item, default=str)).lower()
        for item in items[:k]
    )


def run_benchmark() -> Dict[str, Any]:
    set_active_workspace(WORKSPACE)
    server = OmniCodeMCPServer(repo_root=ROOT)
    bugs = json.loads((ROOT / "eval" / "bugs.json").read_text(encoding="utf-8"))["bugs"]

    rows = []
    for bug in bugs:
        sid = f"eval_{bug['bug_id']}"
        method = bug["culprit_method"].split("(")[0]
        cls = Path(bug["culprit_file"]).stem
        t0 = time.time()

        logs = server.safe_call("analyze_logs", raw_trace=_trace(bug), session_id=sid)
        search = server.safe_call("search_code", query=bug["symptom"], limit=10, session_id=sid)
        items = search.get("candidates", []) if isinstance(search, dict) else []

        leaks = len(server.leak_scanner.find(json.dumps([logs, search], default=str)))
        rows.append({
            "bug_id": bug["bug_id"],
            "title": bug["title"],
            "method_hit_at_1": _hit(server, sid, items, method, 1),
            "method_hit_at_3": _hit(server, sid, items, method, TOP_K),
            "class_hit_at_3": _hit(server, sid, items, cls, TOP_K),
            "anchor_found": bool(isinstance(logs, dict) and logs.get("error_anchor")),
            "leaks": leaks,
            "latency_ms": round((time.time() - t0) * 1000.0, 1),
        })

    def rate(key: str) -> float:
        return round(sum(1 for r in rows if r[key]) / len(rows), 3)

    summary = {
        "bugs": len(rows),
        "method_hit_at_1": rate("method_hit_at_1"),
        "method_hit_at_3": rate("method_hit_at_3"),
        "class_hit_at_3": rate("class_hit_at_3"),
        "anchor_found": rate("anchor_found"),
        "leaks": sum(r["leaks"] for r in rows),
        "rows": rows,
    }
    _write_report(summary)
    return summary


def _write_report(summary: Dict[str, Any]) -> None:
    yes = lambda b: "yes" if b else "no"  # noqa: E731
    lines = [
        "# Seeded-bug benchmark",
        "",
        f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')} | bugs: {summary['bugs']} | leaks: {summary['leaks']}",
        "",
        "| Bug | Method hit@1 | Method hit@3 | Class hit@3 | Anchor | Leaks | Latency (ms) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | ---: |",
    ]
    for r in summary["rows"]:
        lines.append(
            f"| {r['bug_id']} | {yes(r['method_hit_at_1'])} | {yes(r['method_hit_at_3'])} | "
            f"{yes(r['class_hit_at_3'])} | {yes(r['anchor_found'])} | {r['leaks']} | {r['latency_ms']} |"
        )
    lines += [
        "",
        f"Rates: method hit@1 {summary['method_hit_at_1']}, hit@3 {summary['method_hit_at_3']}, "
        f"class hit@3 {summary['class_hit_at_3']}, anchor {summary['anchor_found']}.",
        "Three bugs is a smoke test, not a statistically meaningful sample.",
    ]
    (ROOT / "eval" / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    raise SystemExit(0 if run_benchmark()["leaks"] == 0 else 1)
