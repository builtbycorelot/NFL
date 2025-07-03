import os
import unittest

class TestNeo4jSchema(unittest.TestCase):
    def test_schema_file_exists(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'schema', 'neo4j_schema.cypher')
        self.assertTrue(os.path.exists(path))
        with open(path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        self.assertIn('Team', text)
        self.assertIn('CONSTRAINT', text.upper())

if __name__ == '__main__':
    unittest.main()
