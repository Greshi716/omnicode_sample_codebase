"""Lending-specific rules used by the library hooks in hooks.py."""

import re
from typing import Any

_CARD_NUMBER = re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")
_DESTRUCTIVE_SQL = re.compile(r"\b(TRUNCATE|DROP\s+(DATABASE|TABLE|SCHEMA))\b", re.IGNORECASE)


def contains_card_number(text: str) -> bool:
    return bool(_CARD_NUMBER.search(text))


def contains_destructive_sql(value: Any) -> bool:
    """True if any string inside a (possibly nested) value holds destructive DDL."""
    if isinstance(value, str):
        return bool(_DESTRUCTIVE_SQL.search(value))
    if isinstance(value, dict):
        return any(contains_destructive_sql(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(contains_destructive_sql(v) for v in value)
    return False
