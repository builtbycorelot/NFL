# Node Form Language Syntax

The Node Form Language (NFL) expresses graphs using a small set of verbs.
Each node is represented with a `name` and `type` while edges connect them
using `from` and `to` fields.

Example JSON snippet:

```json
{
  "pack": "groups",
  "nodes": [
    {"name": "Example", "type": "Team", "id": "EX"}
  ],
  "edges": [
    {"from": "EX", "to": "Other", "trait": ["rival"]}
  ]
}
```

See `schema/nfl.schema.json` for the formal JSON schema.
