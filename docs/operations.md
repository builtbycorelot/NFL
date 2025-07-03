# NFL Public API – Operational Spec (v0.3)

This document outlines how to run the NFL stack with Neo4j, PostgreSQL and
the browser based visualizers.

## Quick-Start

Use Docker Compose to start all services:

```bash
docker-compose up
```

This brings up the API server (`nfl-server`), PostgreSQL, Neo4j and a Jupyter
`visualizer` container. The API listens on `:8000` and the Neo4j browser is
accessible on `:7474`.

Smoke test:

```bash
curl http://localhost:8000/health  # -> {"status":"ok"}
```

### Seed Data

Run the Cypher statements in `schema/neo4j_schema.cypher` to create indexes in
Neo4j. Sample graphs in `examples/` can be imported via `POST /import`.

## Runtime Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `PORT` | `8000` | API port |
| `NEO4J_URI` | `bolt://neo4j:7687` | Neo4j connection |
| `POSTGRES_URI` | `dbname=nfldb user=nfl password=secret host=postgres` | PostgreSQL connection |

## REST Endpoints

- `GET /health`
- `POST /import`
- `GET /export/jsonld`
- `GET /export/owl`
- `GET /export/geojson`

Use these in the notebooks inside the `visualizer` service to feed the
`schema_org_visualizer` or `home_visualizer` packs.

## Exploring the Graph

Open [http://localhost:7474](http://localhost:7474) to access the Neo4j browser.
The default credentials are `neo4j/secret`.

## Launch Visualizers

Attach to the `visualizer` service and start Jupyter:

```bash
docker-compose exec visualizer start-notebook.sh --NotebookApp.token=''
```

Open the printed URL in your browser to run the example notebooks shipped in the
`packs/` directory.
