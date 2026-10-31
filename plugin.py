"""
Custom OmniCode Plugin for omnicode-sample-app.
Demonstrates custom @tool and @hook integration with omnicode-core public API.
"""

from typing import Dict, Any
from omnicode_core.tools import tool
from omnicode_core.hooks import hook, Allow, Block, Modify, HookDecision


@tool(name="catalog_search", description="Search available library books by title or author.")
def catalog_search(query: str) -> Dict[str, Any]:
    """Custom developer tool: searches the sample library catalog."""
    # In production, queries database or local repository
    return {
        "query": query,
        "results": [
            {"book_id": "BK-101", "title": "Design Patterns", "author": "Gang of Four", "available": True},
            {"book_id": "BK-102", "title": "Clean Code", "author": "Robert C. Martin", "available": True}
        ]
    }


@hook("before_tool")
def security_checkout_audit(tool_name: str, arguments: Dict[str, Any], session_id: str) -> HookDecision:
    """Security hook verifying tool calls before execution."""
    if tool_name == "catalog_search":
        q = arguments.get("query", "")
        if "DROP TABLE" in q.upper():
            return Block(reason="Blocked malicious SQL injection in catalog query")
    return Allow()
