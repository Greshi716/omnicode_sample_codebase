"""
Custom Project PreToolUse Hook: Library Lending Domain Guard.
Demonstrates consumer-layer extensibility: developers can define custom rules
on their own Claude layer that execute alongside the base OmniCode SDD plugin hooks.
"""
import sys
import json

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # Pass through if unreadable

tool_name = payload.get("tool_name", "")
tool_args = payload.get("tool_input", {})

# Example custom domain policy:
# Intercepts db queries or search queries attempting destructive operations on the lending catalog
if "sql" in tool_args:
    sql_text = str(tool_args["sql"]).upper()
    if "TRUNCATE" in sql_text or "DROP DATABASE" in sql_text:
        print("Blocked by Custom Lending Policy: Destructive DDL statements are forbidden in consumer workspace.", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
