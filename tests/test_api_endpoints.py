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
