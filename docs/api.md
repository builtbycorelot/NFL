# API Server

The API container exposes HTTP endpoints for querying the local Neo4j and SQLite
instances. It starts automatically when running `docker-compose up` and listens
on port `10000`.

## Endpoints

- `GET /health` – simple health check returning service status.
- `POST /api/cypher` – execute Cypher queries against Neo4j.
- `POST /api/sql` – run read-only SQL against the bundled SQLite database.
- `POST /api/import` – import NFL JSON data into both databases.
- `GET /api/examples` – sample requests for each API.

All endpoints accept and return JSON. Environment variables control database
locations and credentials when running inside Docker.
