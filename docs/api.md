# API Server

The API container exposes HTTP endpoints for querying the local Neo4j and
PostgreSQL instances. It starts automatically when running `docker-compose up`
and listens
on port `8080`.

When using `docker-compose` locally the Apache container serves this
documentation under the `/docs` path. On Render the API is hosted at the root
domain instead, so `/health` is reachable at `https://your-app.onrender.com/health`.

## Endpoints

- `GET /health` – simple health check returning service status.
- `POST /api/cypher` – execute Cypher queries against Neo4j.
- `POST /api/sql` – run read-only SQL against PostgreSQL.
- `POST /api/import` – import NFL JSON data into both databases.
- `GET /api/examples` – sample requests for each API.

All endpoints accept and return JSON. Environment variables control database
locations and credentials when running inside Docker.

## Quick Test

Verify the server is reachable:

```bash
curl http://localhost:8080/health
```

The command should return `{"status":"healthy","service":"NFL Query API"}`.

### Add a Node

Use the Cypher endpoint to create a team node in Neo4j:

```bash
curl -X POST http://localhost:8080/api/cypher \
  -H 'Content-Type: application/json' \
  -d '{"query":"CREATE (:Team {id: $id, name: $name})","parameters":{"id":"TB","name":"Tampa Bay"}}'
```

### Add a Relationship

Create a relationship between teams:

```bash
curl -X POST http://localhost:8080/api/cypher \
  -H 'Content-Type: application/json' \
  -d '{"query":"MATCH (a:Team {id:$a}),(b:Team {id:$b}) CREATE (a)-[:RIVAL]->(b)","parameters":{"a":"TB","b":"NO"}}'
```

These commands assume `NEO4J_URI` points at a running Neo4j instance.
