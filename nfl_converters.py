"""Minimal converters from NFL graphs to various formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def to_json(nfl: Dict[str, Any]) -> str:
    """Return the NFL graph as pretty JSON."""
    if not isinstance(nfl, dict) or not all(k in nfl for k in ["nodes", "edges"]):
        raise ValueError("Input must be a valid NFL graph with 'nodes' and 'edges' keys")
    return json.dumps(nfl, indent=2, sort_keys=True)


def to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a very small JSON-LD structure."""
    graph: List[Dict[str, Any]] = []
    for node in nfl.get("nodes", []):
        entry = {"@id": node.get("name"), "@type": node.get("type")}
        for k, v in node.items():
            if k not in {"name", "type"}:
                entry[k] = v
        graph.append(entry)
    for edge in nfl.get("edges", []):
        graph.append({
            "@id": f"{edge.get('from')}_to_{edge.get('to')}",
            "from": edge.get("from"),
            "to": edge.get("to"),
        })
    return {"@context": "https://example.org/nfl", "@graph": graph}


def to_owl(nfl: Dict[str, Any]) -> str:
    """Convert *nfl* to a trivial Turtle representation."""
    lines: List[str] = ["@prefix nfl: <https://example.org/nfl#> .", ""]
    for node in nfl.get("nodes", []):
        lines.append(f"nfl:{node.get('name')} a nfl:{node.get('type')} .")
    for edge in nfl.get("edges", []):
        lines.append(f"nfl:{edge.get('from')} nfl:relatedTo nfl:{edge.get('to')} .")
    return "\n".join(lines)


def to_cityjson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a minimal CityJSON object."""
    city_objects: Dict[str, Any] = {}
    for node in nfl.get("nodes", []):
        city_objects[node.get("name")] = {
            "type": "GenericCityObject",
            "attributes": {"type": node.get("type")},
        }
    return {"type": "CityJSON", "version": "1.1", "CityObjects": city_objects}


def to_geojson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a minimal GeoJSON FeatureCollection."""
    features: List[Dict[str, Any]] = []
    for node in nfl.get("nodes", []):
        features.append({
            "type": "Feature",
            "geometry": None,
            "properties": {"id": node.get("name"), "type": node.get("type")},
        })
    return {"type": "FeatureCollection", "features": features}


__all__ = [
    "to_json",
    "to_jsonld",
    "to_owl",
    "to_cityjson",
    "to_geojson",
]
