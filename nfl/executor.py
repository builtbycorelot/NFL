from __future__ import annotations

from typing import Any

from .cost_model import CostModel
from .ledger import SemanticLedger
from .graph import Graph


class Executor:
    def __init__(self, graph: Graph, ledger: SemanticLedger | None = None):
        self.graph = graph
        self.cost_model = CostModel()
        self.ledger = ledger or SemanticLedger()

    def execute(self, node_id: str, context: Any | None = None) -> None:
        # Placeholder execution
        cost = self.cost_model.cost(node_id)
        self.ledger.record(node_id, cost, context)
