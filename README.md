# NFL

Node Form Language (NFL) is a small toolkit for describing graphs of nodes and edges. This repository provides a core Python library, a REST API built with FastAPI and a command line interface.

## Quick start

```bash
pip install -r requirements.txt
# Validate an example graph
python -m cli.nfl_cli validate examples/simple.json
# Start the API
uvicorn api:app --reload
```
