# NFL Public API – Operational Spec (v0.2)

This document mirrors the operational reference used to run and test the HTTP API.
It outlines the quick start steps, runtime configuration, API surface and test
matrix.

## Quick-Start

```bash
# build & run API on :8080
$ docker build -t nfl-api .
$ docker run -it --rm -p 8080:8080 \
      -e PORT=8080 \
      -e NEO4J_URI=bolt://host.docker.internal:7687 \
      nfl-api
```

Smoke test:

```bash
curl http://localhost:8080/health  # -> {"status":"ok"}
```

### Seed Data

Run the Cypher statements in `schema/neo4j_schema.cypher` to create
indexes in Neo4j. The example file `examples/groups.json` can then be
imported via `POST /api/import` to populate sample groups for testing.

## Runtime Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `PORT` | `8080` | Required on Render. TCP port the API binds. |
| `WORKERS` | `2` | Gunicorn worker count. |
| `LOG_LEVEL` | `info` | debug/info/warning/error |
| `NEO4J_URI` | *(empty – Neo4j disabled)* | Bolt URI; if unset, Neo4j routes are disabled. |
| `POSTGRES_URI` | `dbname=nfl user=nfl password=nfl host=localhost` | Connection string for PostgreSQL. |

## API Surface

- `GET /health`
- `GET /db/health`
- `GET /info`
- `POST /import`
- `GET /export/{format}`
- `POST /query/cypher`
- `POST /query/sql`

All responses return `{ "ok": true, "data": …, "duration_ms": 42 }` when successful.

## Tests & Coverage

Install dependencies with test extras and run the suite with:

```bash
pip install -e .[test]
pytest -q
```

Neo4j tests automatically skip if `NEO4J_URI` is unset. Coverage results are
published via Codecov.

## Changelog

*0.2 – Fix `${PORT}` bug; add DB health endpoint; full docs & badges.*
