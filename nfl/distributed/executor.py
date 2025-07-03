from __future__ import annotations

from typing import Any

from nfl.executor import Executor
from nfl.graph import Graph


class DistributedExecutor(Executor):
    """Placeholder distributed executor using a partitioner."""

    def __init__(self, graph: Graph, backend: str = "local", shards: int = 1):
        super().__init__(graph)
        self.backend = backend
        self.shards = shards

    def execute(self, node_id: str, context: Any | None = None) -> None:
        # In real implementation this would dispatch to workers
        super().execute(node_id, context)
