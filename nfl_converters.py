"""Minimal converters from NFL graphs to various formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def to_json(nfl: Dict[str, Any]) -> str:
    """Return the NFL graph as pretty JSON."""
    return json.dumps(nfl, indent=2, sort_keys=True)


def to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a very small JSON-LD structure."""
    graph: List[Dict[str, Any]] = []
    for node in nfl.get("nodes", []):
        entry = {"@id": node["name"], "@type": node["type"]}
        for k, v in node.items():
            if k not in ("name", "type"):
                entry[k] = v
        graph.append(entry)
    for edge in nfl.get("edges", []):
        graph.append({
            "@id": f"{edge['from']}_to_{edge['to']}",
            "from": edge["from"],
            "to": edge["to"],
        })
    return {"@context": "https://example.org/nfl", "@graph": graph}


def to_owl(nfl: Dict[str, Any]) -> str:
    """Convert *nfl* to a trivial Turtle representation."""
    lines = ["@prefix nfl: <https://example.org/nfl#> .", ""]
    for node in nfl.get("nodes", []):
        lines.append(f"nfl:{node['name']} a nfl:{node['type']} .")
    for edge in nfl.get("edges", []):
        lines.append(f"nfl:{edge['from']} nfl:relatedTo nfl:{edge['to']} .")
    return "\n".join(lines)


def to_cityjson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a minimal CityJSON object."""
    city_objects = {}
    for node in nfl.get("nodes", []):
        city_objects[node["name"]] = {
            "type": "GenericCityObject",
            "attributes": {"type": node["type"]},
        }
    return {"type": "CityJSON", "version": "1.1", "CityObjects": city_objects}


def to_geojson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Convert *nfl* to a minimal GeoJSON FeatureCollection."""
    features = []
    for node in nfl.get("nodes", []):
        features.append({
            "type": "Feature",
            "geometry": None,
            "properties": {"id": node["name"], "type": node["type"]},
        })
    return {"type": "FeatureCollection", "features": features}


__all__ = [
    "to_json",
    "to_jsonld",
    "to_owl",
    "to_cityjson",
    "to_geojson",
]
