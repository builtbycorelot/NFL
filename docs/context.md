# Node Form Language Context

NFL is a minimalist graph notation for describing knowledge and processes. It revolves around six verbs that define how graphs are constructed and executed:

| Verb | Purpose |
|------|---------|
| `node` | define an entity |
| `edge` | relate two nodes |
| `fn` | declare a callable node |
| `trait` | annotate behavior or attach data |
| `pack` | group a dialect or namespace |
| `impl` | provide the implementation |

Graphs built from these verbs can be validated and executed across runtimes. The repository provides examples, a JSON schema, and tooling to explore NFL data.
