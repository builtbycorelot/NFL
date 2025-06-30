import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from conformance_tests.src.ngl_parser import NGLParser


def test_valid_json_parsing():
    parser = NGLParser()
    content = '{"nodes": [{"id": "node1"}]}'
    result = parser.parse(content, format="json")
    assert result.valid
    assert result.errors == []
    assert result.nodes[0]["id"] == "node1"
