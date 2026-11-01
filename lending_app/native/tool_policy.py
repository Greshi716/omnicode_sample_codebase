"""Claude Code PreToolUse hook: only omnicode MCP tools, and no destructive SQL. Fails closed."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lending_app.policy import contains_destructive_sql  # noqa: E402

ALLOWED_PREFIX = "mcp__omnicode__"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("Blocked: tool call payload could not be parsed.", file=sys.stderr)
        return 2
    tool_name = str(payload.get("tool_name", ""))
    if not tool_name.startswith(ALLOWED_PREFIX):
        print(f"Blocked: '{tool_name}' is not an omnicode tool.", file=sys.stderr)
        return 2
    if contains_destructive_sql(payload.get("tool_input", {})):
        print("Blocked by lending policy: destructive DDL is forbidden.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
