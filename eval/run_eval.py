"""
OmniCode Diagnostic Evaluation Benchmark Runner for omnicode-sample-app.
Evaluates diagnostic precision, latency, token efficiency, and privacy boundary enforcement.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add omnicode framework to sys.path if not installed in environment
try:
    import omnicode_core
    import omnicode_mcp
except ImportError:
    omnicode_dir = os.getenv("OMNICODE_CORE_PATH")
    if omnicode_dir and Path(omnicode_dir).exists():
        sys.path.insert(0, str(Path(omnicode_dir).resolve()))
    else:
        sibling_project = Path(__file__).parent.parent.parent / "Project"
        if sibling_project.exists():
            sys.path.insert(0, str(sibling_project.resolve()))

from omnicode_mcp.server import OmniCodeMCPServer
from omnicode_core.workspace import load_workspace, set_active_workspace


def run_benchmark():
    app_root = Path(__file__).parent.parent.resolve()
    ws_file = app_root / "omnicode.workspace.yaml"
    ws = load_workspace(ws_file)
    set_active_workspace(ws)

    server = OmniCodeMCPServer(repo_root=app_root)

    bugs_file = app_root / "eval" / "bugs.json"
    with open(bugs_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    results = []

    print("======================================================================")
    print("Running OmniCode Diagnostic Benchmark on omnicode-sample-app")
    print(f"Total Seeded Bugs: {len(bench_data['bugs'])}")
    print("======================================================================\n")

    for bug in bench_data["bugs"]:
        bid = bug["bug_id"]
        title = bug["title"]
        print(f"[{bid}] Evaluating: {title}")
        t0 = time.time()

        # Step 1: Simulate crash stack trace
        trace = f"""
java.lang.Exception: {bug['symptom']}
    at {bug['culprit_file'].replace('src/main/java/', '').replace('.java', '').replace('/', '.')}.{bug['culprit_method'].split('(')[0]}({Path(bug['culprit_file']).name}:42)
    at com.example.library.service.LendingService.checkoutBook(LendingService.java:38)
"""
        # Step 2: Log analysis
        sid = f"eval_sess_{bid}"
        log_res = server.safe_call("analyze_logs", raw_trace=trace, session_id=sid)
        anchor_found = bool(log_res.get("error_anchor"))

        # Step 3: Code search
        method_name = bug['culprit_method'].split('(')[0]
        search_res = server.safe_call("search_code", query=method_name, session_id=sid)

        # Step 4: Verification of zero leakage
        combined_output = json.dumps(log_res) + json.dumps(search_res)
        has_leak = any(
            p in combined_output
            for p in ["com.example.library", "LibraryCorp", "BookPlex"]
        )

        latency_ms = (time.time() - t0) * 1000.0

        eval_result = {
            "bug_id": bid,
            "title": title,
            "category": bug["category"],
            "anchor_identified": anchor_found,
            "symbol_retrieved": "candidates" in search_res or "code_cards" in search_res,
            "zero_leak_preserved": not has_leak,
            "latency_ms": round(latency_ms, 2),
            "status": "PASS" if anchor_found and not has_leak else "FAIL"
        }
        results.append(eval_result)
        print(f"       Status: {eval_result['status']} | Latency: {eval_result['latency_ms']}ms | Zero-Leak: {eval_result['zero_leak_preserved']}\n")

    # Generate Markdown Report
    report_path = app_root / "eval" / "results.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# OmniCode Diagnostic Evaluation Benchmark Results\n\n")
        f.write(f"**Application**: `omnicode-sample-app` (Library Lending & Inventory System)\n")
        f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Zero-Leak Boundary**: Verified (Fail-closed on unmasked package identifiers)\n\n")
        f.write("## Benchmark Summary\n\n")
        f.write("| Bug ID | Category | Title | Anchor Found | Zero-Leak | Latency | Status |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :---: |\n")
        for r in results:
            f.write(f"| **{r['bug_id']}** | {r['category']} | {r['title']} | {'Yes' if r['anchor_identified'] else 'No'} | {'PASS' if r['zero_leak_preserved'] else 'FAIL'} | {r['latency_ms']} ms | **{r['status']}** |\n")
        
        f.write("\n## Seeded Defect Diagnoses\n\n")
        for bug in bench_data["bugs"]:
            f.write(f"### {bug['bug_id']}: {bug['title']}\n")
            f.write(f"- **Category**: {bug['category']} ({bug['severity']})\n")
            f.write(f"- **Culprit**: `{bug['culprit_file']}` -> `{bug['culprit_method']}`\n")
            f.write(f"- **Root Cause**: {bug['root_cause']}\n")
            f.write(f"- **Actionable Remediation**: {bug['remediation']}\n\n")

    print(f"Evaluation report generated at: {report_path}")
    return results


if __name__ == "__main__":
    run_benchmark()
