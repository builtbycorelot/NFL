from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_import_and_list():
    data = {"pack": "demo", "nodes": [{"name": "n", "type": "X"}], "edges": []}
    resp = client.post("/import", json=data)
    assert resp.status_code == 200
    resp = client.get("/nodes")
    assert resp.json()[0]["name"] == "n"


def test_edges_listing():
    data = {
        "pack": "demo",
        "nodes": [
            {"name": "a", "type": "X"},
            {"name": "b", "type": "X"},
        ],
        "edges": [{"from": "a", "to": "b"}],
    }
    resp = client.post("/import", json=data)
    assert resp.status_code == 200
    resp = client.get("/edges")
    edges = resp.json()
    assert edges
    assert edges[0]["from"] == "a"


def test_export_formats():
    data = {"pack": "demo", "nodes": [{"name": "n", "type": "X"}], "edges": []}
    client.post("/import", json=data)
    resp = client.get("/export/jsonld")
    assert resp.status_code == 200
    assert resp.json()["pack"] == "demo"

    resp = client.get("/export/owl")
    assert resp.status_code == 200
    assert "ttl" in resp.json()

    resp = client.get("/export/geojson")
    assert resp.status_code == 200
    assert resp.json()["type"] == "FeatureCollection"
