from __future__ import annotations

import json
from typing import Any, Dict, List


def to_owl(nfl: Dict[str, Any]) -> str:
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
        type_line = f"    :type \"{node.get('type')}\""
        if "state" in node:
            lines.append(type_line + " ;")
            lines.append(f"    :state '{json.dumps(node['state'])}' .")
        else:
            lines.append(type_line + " .")
    for edge in nfl.get("edges", []):
        lines.append(f":{edge.get('from')} :connectedTo :{edge.get('to')} .")
    return "\n".join(lines)
