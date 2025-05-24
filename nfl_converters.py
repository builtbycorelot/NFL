"""Minimal converters from NFL graphs to various formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from cli.nfl_to_semantics import convert_to_jsonld


def _validate_graph(nfl: Dict[str, Any]) -> None:
    """Raise :class:`ValueError` if *nfl* doesn't look like a graph."""
    if not isinstance(nfl, dict) or not all(k in nfl for k in ["nodes", "edges"]):
        raise ValueError("Input must be a valid NFL graph with 'nodes' and 'edges' keys")


def to_json(nfl: Dict[str, Any]) -> str:
    """Return the NFL graph as pretty JSON."""
    _validate_graph(nfl)
    return json.dumps(nfl, indent=2, sort_keys=True)


def to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-LD representation of *nfl*."""
    _validate_graph(nfl)
    return convert_to_jsonld(nfl)


def to_owl(nfl: Dict[str, Any]) -> str:
    """Return a tiny OWL/Turtle representation of *nfl*."""
    _validate_graph(nfl)

    lines = [
        "@prefix nfl: <http://example.org/nfl#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "",
        "nfl:Ontology a owl:Ontology .",
    ]

    for node in nfl.get("nodes", []):
        name = node.get("name")
        typ = node.get("type", "Node")
        if name:
            lines.append(f"nfl:{name} a nfl:{typ} .")

    for edge in nfl.get("edges", []):
        from_node = edge.get("from")
        to_node = edge.get("to")
        if from_node and to_node:
            lines.append(f"nfl:{from_node} nfl:connectedTo nfl:{to_node} .")

    return "\n".join(lines)


def to_cityjson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a simple CityJSON representation of *nfl*."""
    _validate_graph(nfl)

    city = {
        "type": "CityJSON",
        "version": "1.0",
        "CityObjects": {},
        "vertices": [],
    }

    for node in nfl.get("nodes", []):
        name = node.get("name")
        if not name:
            continue
        attrs = {k: v for k, v in node.items() if k not in {"name", "type"}}
        city["CityObjects"][name] = {
            "type": node.get("type", "Generic"),
            "attributes": attrs,
        }

    return city


def to_geojson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a GeoJSON ``FeatureCollection`` for the graph."""
    _validate_graph(nfl)

    features: List[Dict[str, Any]] = []
    for node in nfl.get("nodes", []):
        geometry = None
        if "lat" in node and "lon" in node:
            geometry = {
                "type": "Point",
                "coordinates": [node["lon"], node["lat"]],
            }

        props = {k: v for k, v in node.items() if k not in {"lat", "lon"}}
        props.setdefault("id", node.get("name"))
        features.append({"type": "Feature", "geometry": geometry, "properties": props})

    return {"type": "FeatureCollection", "features": features}


__all__ = [
    "to_json",
    "to_jsonld",
    "to_owl",
    "to_cityjson",
    "to_geojson",
]
