import app
from app import app as flask_app


def test_health_endpoint():
    client = flask_app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'status' in data


def test_db_health_endpoint():
    client = flask_app.test_client()
    resp = client.get('/db/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'neo4j' in data
    assert 'sqlite' in data


def test_info_endpoint():
    client = flask_app.test_client()
    resp = client.get('/info')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'version' in data
    assert 'start_time' in data


def test_cypher_disabled(monkeypatch):
    """Cypher endpoint should return 503 when Neo4j is disabled."""
    monkeypatch.setattr(app, 'driver', None)
    client = flask_app.test_client()
    resp = client.post('/api/cypher', json={'query': 'RETURN 1'})
    assert resp.status_code == 503

