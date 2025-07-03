import sys
import importlib

# If real packages are missing, fall back to stubs
packages = {
    'flask': 'offline_stubs.flask',
    'flask_cors': 'offline_stubs.flask_cors',
    'psycopg2': 'offline_stubs.psycopg2',
    'psycopg2.extras': 'offline_stubs.psycopg2.extras',
    'neo4j': 'offline_stubs.neo4j',
}

for pkg, stub in packages.items():
    try:
        importlib.import_module(pkg)
    except Exception:
        sys.modules[pkg] = importlib.import_module(stub)
