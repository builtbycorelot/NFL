import json
import os

from nfl_converters import to_cityjson, to_geojson


def load_example(name="simple.json"):
    path = os.path.join(os.path.dirname(__file__), "..", "examples", name)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def test_cityjson_features():
    data = load_example()
    cj = to_cityjson(data)
    assert cj["type"] == "CityJSON"
    assert "CityObjects" in cj
    assert list(cj["CityObjects"].keys()) == ["x", "y"]


def test_geojson_features():
    data = load_example()
    gj = to_geojson(data)
    assert gj["type"] == "FeatureCollection"
    assert len(gj["features"]) == 2
