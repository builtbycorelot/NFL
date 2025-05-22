"""Minimal converters from NFL graphs to various formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def to_json(nfl: Dict[str, Any]) -> str:
    """Return the NFL graph as pretty JSON."""
    if not isinstance(nfl, dict) or not all(k in nfl for k in ["nodes", "edges"]):
        raise ValueError("Input must be a valid NFL graph with 'nodes' and 'edges' keys")
    return json.dumps(nfl, indent=2, sort_keys=True)


__all__ = [
    "to_json",
    "to_jsonld",
    "to_owl",
    "to_cityjson",
    "to_geojson",
]
