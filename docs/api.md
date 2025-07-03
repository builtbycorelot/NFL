# API Server

The API container exposes HTTP endpoints for querying the local Neo4j and
PostgreSQL instances. It starts automatically when running `docker-compose up`
and listens
on port `8080`.

When using `docker-compose` locally the Apache container serves this
documentation under the `/docs` path. On Render the API is hosted at the root
domain instead, so `/health` is reachable at `https://your-app.onrender.com/health`.

## Endpoints

The table below lists all public routes exposed by the API.

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET`  | `/health` | Basic service heartbeat |
| `GET`  | `/db/health` | Connectivity check for Neo4j and PostgreSQL |
| `GET`  | `/info` | Build metadata and start time |
| `POST` | `/api/cypher` | Execute Cypher queries against Neo4j |
| `POST` | `/api/sql` | Run read-only SQL against PostgreSQL |
| `POST` | `/api/import` | Import a NodeForm JSON document into both databases |
| `GET`  | `/api/examples` | Example queries for reference |

All endpoints accept and return JSON. Environment variables control database
locations and credentials when running inside Docker.

## Quick Test

Verify the server is reachable:

```bash
curl http://localhost:8080/health
```

The command should return `{"status":"healthy","service":"NodeForm Query API"}`.

### Add a Node

Use the Cypher endpoint to create an entity node in Neo4j:

```bash
curl -X POST http://localhost:8080/api/cypher \
  -H 'Content-Type: application/json' \
  -d '{"query":"CREATE (:Entity {id: $id, name: $name})","parameters":{"id":"E1","name":"Example"}}'
```

### Add a Relationship

Create a relationship between entities:

```bash
curl -X POST http://localhost:8080/api/cypher \
  -H 'Content-Type: application/json' \
  -d '{"query":"MATCH (a:Entity {id:$a}),(b:Entity {id:$b}) CREATE (a)-[:RELATED_TO]->(b)","parameters":{"a":"E1","b":"E2"}}'
```

These commands assume `NEO4J_URI` points at a running Neo4j instance.

### Check Database Connectivity

```bash
curl http://localhost:8080/db/health
```

Example response:

```json
{
  "neo4j": "ok",
  "postgres": "ok",
  "latency_ms": {"neo4j": 0.5, "postgres": 0.2}
}
```

### Retrieve Build Info

```bash
curl http://localhost:8080/info
```

### Run a SQL Query

```bash
curl -X POST http://localhost:8080/api/sql \
  -H 'Content-Type: application/json' \
  -d '{"query":"SELECT * FROM entities","parameters":[]}'
```

### Import Data

```bash
curl -X POST http://localhost:8080/api/import \
  -H 'Content-Type: application/json' \
  -d @examples/simple.json
```
