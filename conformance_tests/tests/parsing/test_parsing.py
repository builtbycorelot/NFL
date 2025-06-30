from conformance_tests.src.ngl_parser import NGLParser


def test_valid_json_parsing():
    parser = NGLParser()
    content = '{"nodes": [{"id": "node1"}]}'
    result = parser.parse(content, format="json")
    assert result.valid
    assert result.errors == []
    assert result.nodes[0]["id"] == "node1"
