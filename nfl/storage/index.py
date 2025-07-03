from __future__ import annotations


class AttributeIndex:
    """Simple in-memory index."""

    def __init__(self) -> None:
        self.index: dict[str, set[str]] = {}

    def add(self, attr: str, node: str) -> None:
        self.index.setdefault(attr, set()).add(node)

    def search(self, attr: str) -> list[str]:
        return sorted(self.index.get(attr, set()))
