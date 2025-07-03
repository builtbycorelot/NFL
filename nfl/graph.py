from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, List, Dict


@dataclass
class Node:
    name: str
    type: str
    traits: List[str] = field(default_factory=list)
    state: Dict[str, Any] | None = None
    impl: Dict[str, Any] | None = None


@dataclass
class Edge:
    from_: str
    to: str
    traits: List[str] = field(default_factory=list)
    impl: Dict[str, Any] | None = None


class Graph:
    def __init__(self, pack: str, nodes: List[Node], edges: List[Edge]):
        self.pack = pack
        self.nodes = nodes
        self.edges = edges

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Graph":
        validate_graph(data)
        nodes = [
            Node(
                **{
                    (k if k != "from" else "from_"): v
                    for k, v in n.items()
                    if k in {"name", "type", "traits", "state", "impl"}
                }
            )
            for n in data.get("nodes", [])
        ]
        edges = [
            Edge(
                **{
                    (k if k != "from" else "from_"): v
                    for k, v in e.items()
                    if k in {"from", "to", "traits", "impl"}
                }
            )
            for e in data.get("edges", [])
        ]
        return cls(data.get("pack", ""), nodes, edges)

    @classmethod
    def load(cls, path: str) -> "Graph":
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pack": self.pack,
            "nodes": [self._node_to_dict(n) for n in self.nodes],
            "edges": [self._edge_to_dict(e) for e in self.edges],
        }

    @staticmethod
    def _node_to_dict(node: Node) -> Dict[str, Any]:
        d = {"name": node.name, "type": node.type}
        if node.traits:
            d["traits"] = node.traits
        if node.state is not None:
            d["state"] = node.state
        if node.impl is not None:
            d["impl"] = node.impl
        return d

    @staticmethod
    def _edge_to_dict(edge: Edge) -> Dict[str, Any]:
        d = {"from": edge.from_, "to": edge.to}
        if edge.traits:
            d["traits"] = edge.traits
        if edge.impl is not None:
            d["impl"] = edge.impl
        return d


def validate_graph(data: Dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise TypeError("Graph must be a dict")
    if "pack" not in data:
        raise ValueError("Missing 'pack'")

    nodes = data.get("nodes", [])
    if not isinstance(nodes, list):
        raise TypeError("'nodes' must be a list")
    for node in nodes:
        if not isinstance(node, dict):
            raise TypeError("Node must be a dict")
        if "name" not in node or "type" not in node:
            raise ValueError("Node missing required fields")

    node_names = {n["name"] for n in nodes}

    edges = data.get("edges", [])
    if not isinstance(edges, list):
        raise TypeError("'edges' must be a list")
    for edge in edges:
        if not isinstance(edge, dict):
            raise TypeError("Edge must be a dict")
        if "from" not in edge or "to" not in edge:
            raise ValueError("Edge missing required fields")
        if edge["from"] not in node_names or edge["to"] not in node_names:
            raise ValueError(f"Edge references undefined nodes: {edge}")
