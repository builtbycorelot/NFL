from __future__ import annotations

import json
from typing import Any, Dict, List


def to_sql(nfl: Dict[str, Any]) -> str:
    """Return basic SQL statements for *nfl*."""
    statements: List[str] = [
        "CREATE TABLE IF NOT EXISTS nodes (name TEXT PRIMARY KEY, type TEXT, state JSON);",
        "CREATE TABLE IF NOT EXISTS edges (from_node TEXT, to_node TEXT);",
    ]
    for node in nfl.get("nodes", []):
        state = json.dumps(node.get("state", {}))
        statements.append(
            f"INSERT INTO nodes (name, type, state) VALUES ('{node.get('name')}', '{node.get('type')}', '{state}');"
        )
    for edge in nfl.get("edges", []):
        statements.append(
            f"INSERT INTO edges (from_node, to_node) VALUES ('{edge.get('from')}', '{edge.get('to')}');"
        )
    return "\n".join(statements)
