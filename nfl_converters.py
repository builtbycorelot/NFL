"""Minimal converters from NFL graphs to various formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def to_json(nfl: Dict[str, Any]) -> str:
    """Return the NFL graph as pretty JSON."""
    if not isinstance(nfl, dict) or not all(k in nfl for k in ["nodes", "edges"]):
        raise ValueError("Input must be a valid NFL graph with 'nodes' and 'edges' keys")
    return json.dumps(nfl, indent=2, sort_keys=True)


def _validate_graph(nfl: Dict[str, Any]) -> None:
    """Raise :class:`ValueError` if *nfl* doesn't look like a graph."""
    if not isinstance(nfl, dict) or not all(k in nfl for k in ["nodes", "edges"]):
        raise ValueError("Input must be a valid NFL graph with 'nodes' and 'edges' keys")


def to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-LD representation of *nfl*."""
    _validate_graph(nfl)

    context = {
        "name": "http://schema.org/name",
        "type": "http://schema.org/additionalType",
        "from": {"@id": "http://schema.org/from", "@type": "@id"},
        "to": {"@id": "http://schema.org/to", "@type": "@id"},
        "Node": "http://schema.org/Thing",
        "Edge": "http://schema.org/ActionRelationship",
    }

    graph: List[Dict[str, Any]] = []

    for node in nfl.get("nodes", []):
        graph.append(
            {
                "@id": node.get("name"),
                "@type": "Node",
                "name": node.get("name"),
                "type": node.get("type"),
            }
        )

    for edge in nfl.get("edges", []):
        graph.append({"@type": "Edge", "from": edge.get("from"), "to": edge.get("to")})

    return {"@context": context, "@graph": graph}


def to_owl(nfl: Dict[str, Any]) -> str:
    """Return a very small OWL/Turtle representation of *nfl*."""
    _validate_graph(nfl)

    lines: List[str] = [
        "@prefix nfl: <http://example.org/nfl#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "",
        "nfl:Ontology a owl:Ontology .",
    ]

    for node in nfl.get("nodes", []):
        name = node.get("name")
        typ = node.get("type", "Node")
        lines.append(f"nfl:{name} a nfl:{typ} .")

    for edge in nfl.get("edges", []):
        lines.append(f"nfl:{edge.get('from')} nfl:connectedTo nfl:{edge.get('to')} .")

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
        node_name = node.get("name")
        if not node_name:
            raise ValueError("Node missing required 'name' field")
        city["CityObjects"][node_name] = {
            "type": node.get("type", "Generic"),
            "attributes": {k: v for k, v in node.items() if k not in {"name", "type"}},
        }

    return city


def to_geojson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a GeoJSON FeatureCollection for *nfl*."""
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
