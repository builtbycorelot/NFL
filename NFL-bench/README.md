# NFL Bench Harness

This directory provides a lightweight benchmarking harness for the NodeForm Language runtime.

## Prerequisites

* Docker and Docker Compose installed locally.

## Running

1. Start the services and run the default synthetic workload:

```bash
cd NFL-bench
docker-compose up -d
./runner.sh
```

2. Generate a custom workload (optional):

```bash
python workloads/generate_workload.py custom.json -n 100
./runner.sh custom.json
```

3. After the run completes, open `dashboard.html` in a browser to view metrics.
Results are written as CSV files under the `results/` directory.

Use `docker-compose down` to stop and remove containers when finished.
