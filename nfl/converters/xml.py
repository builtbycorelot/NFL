from __future__ import annotations

import json
from typing import Any, Dict
from xml.etree.ElementTree import Element, SubElement, tostring


def to_xml(nfl: Dict[str, Any]) -> str:
    """Return an XML representation of *nfl*."""
    root = Element("graph", {"pack": nfl.get("pack", "")})
    for node in nfl.get("nodes", []):
        node_el = SubElement(
            root, "node", {"name": node.get("name", ""), "type": node.get("type", "")}
        )
        if "state" in node:
            state_el = SubElement(node_el, "state")
            state_el.text = json.dumps(node["state"])
    for edge in nfl.get("edges", []):
        SubElement(
            root, "edge", {"from": edge.get("from", ""), "to": edge.get("to", "")}
        )
    return tostring(root, encoding="unicode")
