from api import app


def test_openapi_paths():
    spec = app.openapi()
    assert "/nodes" in spec["paths"]
    assert "/edges" in spec["paths"]
