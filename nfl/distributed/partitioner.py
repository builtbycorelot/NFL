from __future__ import annotations

from typing import Dict, List

from nfl.graph import Graph


class Partitioner:
    """Simple consistent hash partitioner."""

    def __init__(self, shards: int):
        self.shards = shards

    def assign(self, node: str) -> int:
        return hash(node) % self.shards

    def partition(self, graph: Graph) -> Dict[int, List[str]]:
        result: Dict[int, List[str]] = {i: [] for i in range(self.shards)}
        for n in graph.nodes:
            result[self.assign(n.name)].append(n.name)
        return result
