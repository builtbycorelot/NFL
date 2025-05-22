# SemanticLedger

The SemanticLedger records execution of NFL graphs. Each transaction references nodes and edges with timestamps and optional signatures.

1. Node or edge invoked
2. Cost evaluated via `CostModel`
3. Entry written to immutable log
4. Tokenized proof (see `p-light.md`)

This forms the basis for auditable graph processing.
