import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from nfl import validate_graph, to_jsonld, to_owl, to_xml, to_sql

VALID_GRAPH = {
    "pack": "test",
    "nodes": [{"name": "n1", "type": "Thing", "state": {"x": 1}}],
    "edges": [{"from": "n1", "to": "n1"}],
}


def test_validate_ok():
    validate_graph(VALID_GRAPH)


def test_validate_fail():
    bad = {"pack": "x", "nodes": [{}], "edges": []}
    with pytest.raises(ValueError):
        validate_graph(bad)


def test_to_jsonld():
    data = to_jsonld(VALID_GRAPH)
    assert "@context" in data
    assert len(data.get("@graph", [])) == 2


def test_to_owl():
    ttl = to_owl(VALID_GRAPH)
    assert "Ontology" in ttl
    assert "connectedTo" in ttl


def test_to_xml():
    xml = to_xml(VALID_GRAPH)
    assert "<graph" in xml
    assert "<node" in xml


def test_to_sql():
    sql = to_sql(VALID_GRAPH)
    assert "INSERT INTO nodes" in sql
    assert "INSERT INTO edges" in sql
