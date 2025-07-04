# NFL

Node Form Language (NFL) is a small toolkit for describing graphs of nodes and edges. This repository provides a core Python library, a REST API built with FastAPI and a command line interface.

## Quick start

```bash
pip install -r requirements.txt
# Validate a graph file
python -m cli.nfl_cli validate path/to/graph.json
# Start the API
uvicorn api:app --reload
```

## Core Verbs

| Verb | Purpose |
|------|---------|
| `node` | define an entity |
| `edge` | relate nodes |
| `fn`   | declare a callable node |
| `trait` | annotate behavior, store data, include - metaframework. 
| `pack` | group a dialect |
| `impl` | provide the implementation| 


Think of this as distilling ideas from RedNode and Neo4j into a tiny set of verbs.

## Vision

 (JSON‑LD, OWL, GeoJSON) while preserving meaning. The `SemanticLedger` tracks provenance and resources.
 
## Visuals

* [OpenAPI Spec](openapi.json) – generate interactive docs with Swagger UI.

## License

This project is licensed under the [MIT License](LICENSE).

## Docker Compose

To launch the NFL application together with Neo4j, PostgreSQL and an Apache server run:

```bash
docker-compose up
```

This builds the project image and starts all services for a local deployment.

After the containers come up you can verify everything is running with:

```bash
docker-compose ps
```

You should see `nfl`, `api`, `neo4j`, `postgres` and `apache` listed as `Up`.
The API server listens on `http://localhost:8080` for requests. Open
`http://localhost` to confirm the HTML pages load.
Run the Cypher statements in `schema/neo4j_schema.cypher` to create
basic indexes and load sample groups via the `/api/import` endpoint.

## Deploy on Render

```
Service type: Web Service
Build Command: (leave blank)
Start Command: (leave blank)
Health Check path: /health
Env vars: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, POSTGRES_URI
```

Render maps `$PORT` to `8080` automatically. Create a second service if you
need a private Neo4j container or point the variables at an AuraDB instance.
The API routes live at the root domain on Render, so navigate to
`https://your-app.onrender.com/health` instead of `/api/health`.

## Quickstart

Install the package in editable mode and run the CLI:

```bash
pip install -e .
nfl-cli validate path/to/graph.json
nfl-cli exec --file path/to/graph.json start
```

Open `openapi.json` in [Swagger UI](https://petstore.swagger.io/) for interactive API docs.

Open a browser at `http://localhost` after running `docker-compose up` to view the HTML pages served by Apache. Neo4j is available on port `7474` and PostgreSQL on `5432`.

## Differentiation

| Feature | NFL | RedNode | Neo4j |
|---------|-----|---------|-------|
| Minimal language | ✅ | ❌ | ❌ |
| Built-in provenance | ✅ | ❌ | ❌ |
| Hardware trust anchors | ✅ | ❌ | ❌ |

## Example Use Cases

1. **Supply chain tracking** – model suppliers and shipments to trace provenance.
2. **AI knowledge graph** – capture domain knowledge and function calls in a single graph.
3. **Regulatory compliance** – express policy as graph traits alongside code.

