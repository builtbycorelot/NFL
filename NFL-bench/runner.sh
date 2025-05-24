#!/usr/bin/env bash

# Orchestrate the benchmark harness.
# Usage: ./runner.sh [workload]
set -euo pipefail

COMPOSE="docker-compose"
WORKLOAD=${1:-workloads/synthetic.json}

$COMPOSE up -d

echo "Warm-up phase..."
sleep 5

NODE_RED_ID=$($COMPOSE ps -q node-red)

if [ -f "$WORKLOAD" ]; then
  echo "Streaming workload $WORKLOAD"
  docker cp "$WORKLOAD" "$NODE_RED_ID:/data/workload.json"
fi

# Placeholder for custom workload execution
# Here we just wait a fixed time to simulate processing
sleep 10

echo "Collecting metrics..."
echo "container,cpu,mem" > results/metrics.csv
docker stats --no-stream --format '{{.Name}},{{.CPUPerc}},{{.MemUsage}}' "$NODE_RED_ID" >> results/metrics.csv

$COMPOSE down
