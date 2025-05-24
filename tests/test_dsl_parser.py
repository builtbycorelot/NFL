from cli.dsl_to_json import parse_file


def test_parse_node_fields(tmp_path):
    dsl = tmp_path / "sample.dsl"
    dsl.write_text(
        """
namespace demo

node Person {
    name: string
    age: int
}

node Task {
    title: string
}

edge Person -> Task
edge Task:title -> Person
""",
        encoding="utf-8",
    )

    data = parse_file(str(dsl))
    assert data["pack"] == "demo"
    names = [n["name"] for n in data["nodes"]]
    assert "Person" in names and "Task" in names

    person = next(n for n in data["nodes"] if n["name"] == "Person")
    fields = {f["name"]: f["type"] for f in person["fields"]}
    assert fields == {"name": "string", "age": "int"}

    edges = data["edges"]
    assert {"from": "Person", "to": "Task"} in edges
    assert {"from": "Task", "from_field": "title", "to": "Person"} in edges

