"""Claude Code UserPromptSubmit hook: no payment data, no real repository identifiers. Fails closed."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lending_app.policy import contains_card_number  # noqa: E402


def main() -> int:
    try:
        prompt = str(json.load(sys.stdin).get("prompt", ""))
    except Exception:
        print("Blocked: prompt payload could not be parsed.", file=sys.stderr)
        return 2
    if contains_card_number(prompt):
        print("Blocked by lending policy: payment card data in prompt.", file=sys.stderr)
        return 2
    try:
        from lending_app.config import ROOT, WORKSPACE
        from omnicode_mcp.core.privacy.leak_scanner import LeakScanner

        scanner = LeakScanner.from_env(
            ROOT, extra_terms=WORKSPACE.masking.org_terms, allowlist=WORKSPACE.masking.allowlist
        )
        leaks = scanner.find(prompt)
    except Exception as exc:
        print(f"Blocked: leak scanner unavailable ({type(exc).__name__}). Build the index first.", file=sys.stderr)
        return 2
    if leaks:
        print(f"Blocked: prompt contains {len(leaks)} real repository identifier(s).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
