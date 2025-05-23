# NodeForm Language (NFL)

NodeForm Language is a minimal graph notation for declaring computation and policy together. Nodes and edges build a self-describing graph that can execute across runtimes while tracking provenance and risk.

## Why NFL and Why Now?

* Software and regulations keep colliding. A shared semantic layer lets both evolve together.
* Graphs express relationships better than ad-hoc APIs.
* Hardware trust anchors such as **PLight.token** allow verified execution of graph logic.

## Core Verbs

| Verb | Purpose |
|------|---------|
| `node` | define an entity |
| `edge` | relate nodes |
| `fn`   | declare a callable node |
| `trait` | annotate behavior |
| `pack` | group a dialect |
| `impl` | provide the implementation |

The grammar lives in [`index.nfl.json`](index.nfl.json) and can be explored using the [Interactive Graph Viewer](visualizer.html).
The canonical JSON Schema for NFL is located at [`schema/nfl.schema.json`](schema/nfl.schema.json).

## Vision

NFL graphs compile to multiple targets (JSON‑LD, OWL, GeoJSON) while preserving meaning. The `SemanticLedger` and `CostModel` nodes track provenance and resources. Combined with `PLight.token` hardware, the system supports transparent and trusted execution.

Session: **NFL_Launch_Visual_IR_Stack_0522**

## Live Visuals

* [Launch Page](index.html) – repository overview and links
* [Graph IR Viewer](visualizer.html) – loads `index.nfl.json` automatically.
* [Context](docs/context.md) – repository anchor and semantic index.

Pre-rendered outputs are located in the [`codecs/`](codecs/) folder. A lightweight GitHub Pages site is hosted at [builtbycorelot.github.io/NFL](https://builtbycorelot.github.io/NFL) for quick access to the viewer.

Stub runtime packs are provided in [`packs/`](packs/) for future execution tests.

## ContextMD

See [`docs/context.md`](docs/context.md) for a high level summary and links to related documents.

## License

This project is licensed under the [MIT License](LICENSE).
