from __future__ import annotations
import json
from typing import Any, Dict


def to_json(nfl: Dict[str, Any]) -> str:
    return json.dumps(nfl, indent=2)


def to_yaml(nfl: Dict[str, Any], indent: int = 0) -> str:
    def dump(obj, level=0):
        pad = '  ' * level
        if isinstance(obj, dict):
            lines = []
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{pad}{k}:")
                    lines.append(dump(v, level + 1))
                else:
                    lines.append(f"{pad}{k}: {v}")
            return '\n'.join(lines)
        elif isinstance(obj, list):
            lines = []
            for item in obj:
                if isinstance(item, (dict, list)):
                    lines.append(f"{pad}-")
                    lines.append(dump(item, level + 1))
                else:
                    lines.append(f"{pad}- {item}")
            return '\n'.join(lines)
        else:
            return f"{pad}{obj}"
    return dump(nfl, indent)


def to_owl(nfl: Dict[str, Any]) -> str:
    lines = ["@prefix : <http://example.org/nfl#> ."]
    for node in nfl.get('nodes', []):
        lines.append(f":{node['name']} a :Node .")
    for edge in nfl.get('edges', []):
        lines.append(f":{edge['from']} :relatesTo :{edge['to']} .")
    return '\n'.join(lines)


def to_geojson(nfl: Dict[str, Any]) -> str:
    features = []
    for node in nfl.get('nodes', []):
        if 'lat' in node and 'lon' in node:
            features.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [node['lon'], node['lat']]},
                'properties': {k: v for k, v in node.items() if k not in {'lat', 'lon'}},
            })
    geo = {'type': 'FeatureCollection', 'features': features}
    return json.dumps(geo, indent=2)
