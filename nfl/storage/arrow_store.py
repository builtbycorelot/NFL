from __future__ import annotations

from typing import Any


class ArrowStore:
    """Placeholder compressed storage using Arrow."""

    def __init__(self) -> None:
        self.tables: dict[str, Any] = {}

    def put(self, key: str, table: Any) -> None:
        self.tables[key] = table

    def get(self, key: str) -> Any:
        return self.tables.get(key)
