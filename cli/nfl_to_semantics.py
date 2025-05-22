"""Conversions from NFL graphs to semantic web formats."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def convert_to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-LD representation of *nfl*."""
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
        graph.append({
            "@id": node.get("name"),
            "@type": "Node",
            "name": node.get("name"),
            "type": node.get("type"),
        })

    for edge in nfl.get("edges", []):
        graph.append({
            "@type": "Edge",
            "from": edge.get("from"),
            "to": edge.get("to"),
        })

    return {"@context": context, "@graph": graph}


def convert_to_owl(nfl: Dict[str, Any]) -> str:
    """Return a very small OWL/Turtle representation of *nfl*."""
    lines: List[str] = [
        "@prefix : <http://example.org/nfl#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "",
        ":Ontology a owl:Ontology .",
    ]

    for node in nfl.get("nodes", []):
        lines.append(f":{node.get('name')} a owl:NamedIndividual ;")
        lines.append(f"    :type \"{node.get('type')}\" .")

    for edge in nfl.get("edges", []):
        lines.append(f":{edge.get('from')} :connectedTo :{edge.get('to')} .")

    return "\n".join(lines)


def convert_to_geojson(nfl: Dict[str, Any]) -> Dict[str, Any]:
    """Return a GeoJSON FeatureCollection if nodes have ``lat`` and ``lon``."""
    features: List[Dict[str, Any]] = []
    for node in nfl.get("nodes", []):
        if "lat" in node and "lon" in node:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [node["lon"], node["lat"]],
                },
                "properties": {k: v for k, v in node.items() if k not in {"lat", "lon"}},
            })
    return {"type": "FeatureCollection", "features": features}


def convert_to_ifc(nfl: Dict[str, Any]) -> str:
    """Return a placeholder IFC representation of *nfl*."""
    lines = ["// IFC export is domain specific; placeholder only"]
    for node in nfl.get("nodes", []):
        lines.append(f"IFCENTITY({node.get('name')})")
    return "\n".join(lines)


def convert_file(path: str) -> Dict[str, Any]:
    """Load an NFL JSON file and return semantic conversions."""
    with open(path, "r", encoding="utf-8") as fh:
        nfl = json.load(fh)
    return {
        "jsonld": convert_to_jsonld(nfl),
        "owl": convert_to_owl(nfl),
        "geojson": convert_to_geojson(nfl),
        "ifc": convert_to_ifc(nfl),
    }


__all__ = [
    "convert_to_jsonld",
    "convert_to_owl",
    "convert_to_geojson",
    "convert_to_ifc",
    "convert_file",
]
