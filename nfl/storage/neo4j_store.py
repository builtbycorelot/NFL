from __future__ import annotations

from typing import Any

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover - offline stub
    from offline_stubs.neo4j import GraphDatabase


class Neo4jStore:
    """Tiny helper for running Cypher queries."""

    def __init__(self, uri: str, user: str, password: str) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, cypher: str, params: dict[str, Any] | None = None) -> list[Any]:
        with self.driver.session() as session:
            result = session.run(cypher, parameters=params)
            return list(result)
