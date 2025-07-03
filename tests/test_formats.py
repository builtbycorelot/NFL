import json
import os
import unittest

from nfl.converters import to_jsonld, to_owl


class TestConverters(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "..", "examples", "naics.json")
        with open(path, "r", encoding="utf-8") as fh:
            self.nfl = json.load(fh)

    def test_jsonld(self):
        data = to_jsonld(self.nfl)
        self.assertIn("@graph", data)

    def test_owl(self):
        ttl = to_owl(self.nfl)
        self.assertIn("Ontology", ttl)


if __name__ == "__main__":
    unittest.main()
