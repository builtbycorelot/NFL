# NFL

Node Form Language (NFL) is a minimal syntax for describing graphs of nodes and edges. This repository focuses on validating those graphs and converting them to common standards.

## Quick start

```bash
pip install -e .
pytest
```

## Core Verbs

| Verb   | Purpose                         |
|-------|---------------------------------|
| `node` | define an entity               |
| `edge` | relate nodes                   |
| `fn`   | declare a callable node        |
| `trait`| annotate behavior or metadata  |
| `pack` | group a dialect                |
| `impl` | provide the implementation     |

Think of this as distilling ideas from RedNode and Neo4j into a tiny set of verbs.

## Vision

NFL maps graph descriptions to common standards such as JSON-LD, OWL (Turtle), XML and SQL while preserving meaning.

## Converters

Use these helper functions to transform a validated graph:

```
from nfl import to_jsonld, to_owl, to_xml, to_sql
```

The `to_owl` function outputs a Turtle string suitable for RDF tooling.

## Documentation

* [NFL Syntax](docs/NFL_Syntax.md)
* [Execution Semantics](docs/NFL_Semantics.md)

## License

This project is licensed under the [MIT License](LICENSE).

## Node.js Conversion Utility

A `nfl_conversions.js` script provides conversions between NFL text and various other
formats (JSON-LD, CSV, YAML, Turtle, GraphQL and more). Install dependencies
using `npm install` and run `node nfl_conversions.js` to experiment with converting
a `sample.nfl` file across these representations.
