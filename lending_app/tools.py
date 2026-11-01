"""Custom MCP tool: catalogue search. Results pass the same mask-and-scan gate as built-in tools."""

from typing import Any, Dict, List

from omnicode_core.tools import tool

CATALOG: List[Dict[str, Any]] = [
    {"book_id": "BK-101", "title": "Design Patterns", "author": "Gang of Four", "available": True},
    {"book_id": "BK-102", "title": "Clean Code", "author": "Robert C. Martin", "available": True},
    {"book_id": "BK-103", "title": "Refactoring", "author": "Martin Fowler", "available": False},
]


@tool(name="catalog_search", description="Search the library catalogue by title or author.")
def catalog_search(query: str) -> Dict[str, Any]:
    needle = query.strip().lower()
    results = [
        book for book in CATALOG
        if needle and (needle in book["title"].lower() or needle in book["author"].lower())
    ]
    return {"query": query, "results": results}
