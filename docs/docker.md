# Docker Deployment

Follow these steps to run the NFL stack with Docker.

## Prerequisites

Ensure Docker and Docker Compose are installed. Verify with:

```bash
docker --version
docker-compose --version
```

Both commands should print version information.

## Start Services

From the repository root run:

```bash
docker-compose up
```

This builds the `nfl` image and starts Neo4j, PostgreSQL and Apache. The first run may take a few minutes.

## Verify

Check the status of the containers:

```bash
docker-compose ps
```

All services should be listed as `Up`. You can then browse to [http://localhost](http://localhost) to see the web pages served by Apache. Neo4j is available on port `7474` and PostgreSQL on `5432`.

## Shutdown

Press `Ctrl+C` and then run:

```bash
docker-compose down
```

This stops and removes the containers.
