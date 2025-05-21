import json
import os
import unittest

from nfl_converters import to_json, to_jsonld, to_owl, to_cityjson, to_geojson


class TestConverters(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "..", "examples", "naics.json")
        with open(path, "r", encoding="utf-8") as fh:
            self.nfl = json.load(fh)

    def test_json(self):
        text = to_json(self.nfl)
        data = json.loads(text)
        self.assertEqual(data["pack"], "naics")
        self.assertTrue(len(data["nodes"]) > 0)

    def test_jsonld(self):
        data = to_jsonld(self.nfl)
        self.assertIn("@graph", data)
        ids = [n.get("@id") for n in data["@graph"]]
        self.assertIn("11", ids)

    def test_owl(self):
        ttl = to_owl(self.nfl)
        self.assertIn("nfl:11 a nfl:Sector", ttl)

    def test_cityjson(self):
        cj = to_cityjson(self.nfl)
        self.assertIn("CityObjects", cj)
        self.assertIn("11", cj["CityObjects"])

    def test_geojson(self):
        gj = to_geojson(self.nfl)
        self.assertEqual(gj["type"], "FeatureCollection")
        ids = [f["properties"]["id"] for f in gj["features"]]
        self.assertIn("11", ids)


if __name__ == "__main__":
    unittest.main()
