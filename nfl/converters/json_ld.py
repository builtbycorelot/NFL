from __future__ import annotations

from typing import Any, Dict, List


def to_jsonld(nfl: Dict[str, Any]) -> Dict[str, Any]:
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
        entry = {
            "@id": node.get("name"),
            "@type": "Node",
            "name": node.get("name"),
            "type": node.get("type"),
        }
        if "state" in node:
            entry["state"] = node["state"]
        graph.append(entry)
    for edge in nfl.get("edges", []):
        graph.append(
            {
                "@type": "Edge",
                "from": edge.get("from"),
                "to": edge.get("to"),
            }
        )
    return {"@context": context, "@graph": graph}
