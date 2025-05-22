# Pilot DSL Overview

The `pilot` file in this repository demonstrates a richer dialect of the NodeForm Language.  
It introduces a few constructs on top of the minimal syntax shown in the root
`README.md`.

## Constructs

| Construct | Description |
|-----------|-------------|
| `namespace` | Sets the package/graph name. The resulting JSON `pack` value is taken from this identifier. |
| `@context` | Declares a JSON‑LD context URL for semantic tooling. |
| `node` | Defines a record type with fields. Platform mapping sections can appear inside. |
| `@platform(name)` | Maps the fields of a node to a specific SaaS provider such as Smartsheet or HubSpot. |
| `edge` | Declares a reactive rule. The example uses edges to create tasks and update applications when statuses change. |
| `function` | Describes higher level operations. In the pilot file they synchronise data across platforms. |

Fields inside a `node` are written using `name type` syntax and may reference
other nodes. The DSL is purposely light weight and is intended to compile down
to the JSON format accepted by the CLI tools.

## Converting to JSON

A small parser is provided under `cli/dsl_to_json.py`. It handles the subset of
the language used by `pilot` and produces a JSON structure that can be validated
with `nfl_cli`:

```bash
$ python -m cli.dsl_to_json pilot -o pilot.json
$ python -m cli.nfl_cli pilot.json
```

The generated `pilot.json` contains a `pack` entry, a list of `nodes` and any
`edges` discovered in the DSL file.
