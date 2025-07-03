import json
import pytest
from nfl.graph import validate_graph

SCHEMA_PATH = "schema/nfl.schema.json"


def test_validate_file_valid():
    with open("examples/simple.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    validate_graph(data)


def test_validate_file_invalid(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    with pytest.raises(Exception):
        with open(invalid, "r", encoding="utf-8") as fh:
            validate_graph(json.load(fh))


def test_validate_unknown_edge(tmp_path):
    graph = {
        "pack": "bad",
        "nodes": [{"name": "a", "type": "X"}],
        "edges": [{"from": "a", "to": "b"}],
    }
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(graph), encoding="utf-8")
    with pytest.raises(ValueError):
        with open(path, "r", encoding="utf-8") as fh:
            validate_graph(json.load(fh))
