* Software and regulations keep colliding. A shared semantic layer lets both evolve together.
* Graphs express relationships better than ad-hoc APIs.
* Hardware trust anchors secure deployments.
* AEC Verification is required - Stardards Contributors are recognized

## Core Verbs

| Verb | Purpose |
|------|---------|
| `node` | define an entity |
| `edge` | relate nodes |
| `fn`   | declare a callable node |
| `trait` | annotate behavior, store data, include - metaframework. 
| `pack` | group a dialect |
| `impl` | provide the implementation| 

The grammar lives in [`index.nfl.json`](index.nfl.json) and can be explored using the [Interactive Graph Viewer](visualizer.html).
The authorative JSON Schema for NFL is located at [`schema/nfl.schema.json`](schema/nfl.schema.json). - Distiling RedNode & Redhat Neo4J

## Vision

 (JSON‑LD, OWL, GeoJSON) while preserving meaning. The `SemanticLedger` tracks provenance and resources.
 
## Live Visuals

* [Launch Page](index.html) – repository overview and links
* [Graph IR Viewer](visualizer.html) – loads `index.nfl.json` automatically.
* [Context](docs/context.md) – repository anchor and semantic index.

Pre-rendered outputs are located in the [`codecs/`](codecs/) folder. 

Stub runtime packs:  [`packs/`](packs/) for execution tests. Double Human Verification - What are their guiding pricipals?

TODO: VERIFY PACK 1

## Development and Testing
Run comprehensive tests

## ContextMD

See [`docs/context.md`](docs/context.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Benchmark Harness

A lightweight benchmark environment lives in [NFL-bench](NFL-bench/). Start the services and run the sample workload using:

```bash
cd NFL-bench
docker-compose up -d
./runner.sh
```

Metrics are written under `NFL-bench/results`. Open `NFL-bench/dashboard.html` in a browser to visualize the run.
