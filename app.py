from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sqlite3
from neo4j import GraphDatabase
import os
from datetime import datetime
import time

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configuration
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
SQLITE_DB = os.getenv('SQLITE_DB', 'nfl.db')

# Neo4j driver (optional)
if NEO4J_URI:
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    except Exception:
        driver = None
else:
    driver = None

@app.route('/')
def root_page():
    """Serve the index.html landing page with health metrics."""
    return app.send_static_file('index.html')

# Service metadata
VERSION = os.getenv("NFL_VERSION", "0.2.0")
BUILD_SHA = os.getenv("BUILD_SHA", "dev")
START_TIME = datetime.utcnow()

# Initialize SQLite database
def init_sqlite():
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # Create tables for NFL data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            conference TEXT,
            division TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            team_id TEXT,
            position TEXT,
            jersey_number INTEGER,
            height REAL,
            weight REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_id) REFERENCES teams(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            home_team_id TEXT,
            away_team_id TEXT,
            home_score INTEGER,
            away_score INTEGER,
            game_date DATE,
            season INTEGER,
            week INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (home_team_id) REFERENCES teams(id),
            FOREIGN KEY (away_team_id) REFERENCES teams(id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize on startup
init_sqlite()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'NFL Query API'})


@app.route('/db/health', methods=['GET'])
def db_health():
    """Check connectivity to Neo4j and SQLite."""
    status = {}
    latency = {}

    start = time.perf_counter()
    if driver is not None:
        try:
            with driver.session() as session:
                session.run("RETURN 1")
            status['neo4j'] = 'ok'
        except Exception:
            status['neo4j'] = 'error'
    else:
        status['neo4j'] = 'disabled'
    latency['neo4j'] = round((time.perf_counter() - start) * 1000, 2)

    start = time.perf_counter()
    try:
        conn = sqlite3.connect(SQLITE_DB)
        conn.execute("SELECT 1")
        conn.close()
        status['sqlite'] = 'ok'
    except Exception:
        status['sqlite'] = 'error'
    latency['sqlite'] = round((time.perf_counter() - start) * 1000, 2)

    return jsonify({
        'neo4j': status['neo4j'],
        'sqlite': status['sqlite'],
        'latency_ms': latency,
    })


@app.route('/info', methods=['GET'])
def info():
    """Return build and runtime metadata."""
    return jsonify({
        'version': VERSION,
        'build_sha': BUILD_SHA,
        'start_time': START_TIME.isoformat(),
    })

@app.route('/api/cypher', methods=['POST'])
def execute_cypher():
    """
    Execute Cypher queries against Neo4j graph database

    Expected JSON payload:
    {
        "query": "MATCH (t:Team)-[:HAS_PLAYER]->(p:Player) WHERE t.name = $team_name RETURN p",
        "parameters": {"team_name": "Cowboys"}
    }
    """
    try:
        data = request.json
        query = data.get('query')
        parameters = data.get('parameters', {})

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Security: Basic query validation (expand as needed)
        forbidden_keywords = ['DELETE', 'DROP', 'CREATE INDEX', 'CREATE CONSTRAINT']
        if any(keyword in query.upper() for keyword in forbidden_keywords):
            return jsonify({'error': 'Forbidden operation'}), 403

        if driver is None:
            return jsonify({'error': 'Neo4j disabled'}), 503

        results = []
        with driver.session() as session:
            result = session.run(query, parameters)
            for record in result:
                results.append(dict(record))

        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'query': query,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'type': 'cypher_error'
        }), 500

@app.route('/api/sql', methods=['POST'])
def execute_sql():
    """
    Execute SQL queries against SQLite database

    Expected JSON payload:
    {
        "query": "SELECT * FROM teams WHERE conference = ?",
        "parameters": ["NFC"]
    }
    """
    try:
        data = request.json
        query = data.get('query')
        parameters = data.get('parameters', [])

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Security: Only allow SELECT queries
        if not query.strip().upper().startswith('SELECT'):
            return jsonify({'error': 'Only SELECT queries are allowed'}), 403

        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()

        cursor.execute(query, parameters)
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        results = [dict(row) for row in rows]

        conn.close()

        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'query': query,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'type': 'sql_error'
        }), 500

@app.route('/api/import', methods=['POST'])
def import_nfl_data():
    """
    Import NFL JSON data into both databases
    """
    try:
        data = request.json

        # Validate against NFL schema first
        # ... validation logic ...

        # Import to SQLite
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()

        # Import teams
        for team in data.get('teams', []):
            cursor.execute('''
                INSERT OR REPLACE INTO teams (id, name, city, conference, division)
                VALUES (?, ?, ?, ?, ?)
            ''', (team['id'], team['name'], team.get('city'),
                  team.get('conference'), team.get('division')))

        conn.commit()
        conn.close()

        # Import to Neo4j if available
        if driver is not None:
            with driver.session() as session:
                # Clear existing data
                session.run("MATCH (n) DETACH DELETE n")

                # Import teams as nodes
                for team in data.get('teams', []):
                    session.run("""
                        CREATE (t:Team {
                            id: $id,
                            name: $name,
                            city: $city,
                            conference: $conference,
                            division: $division
                        })
                    """, team)

        return jsonify({
            'success': True,
            'message': 'Data imported successfully',
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Example queries endpoint for documentation
@app.route('/api/examples', methods=['GET'])
def get_examples():
    return jsonify({
        'cypher_examples': [
            {
                'description': 'Find all players on a specific team',
                'query': 'MATCH (t:Team {name: $team})-[:HAS_PLAYER]->(p:Player) RETURN p.name, p.position',
                'parameters': {'team': 'Cowboys'}
            },
            {
                'description': 'Find teams in same division',
                'query': 'MATCH (t1:Team)-[:IN_DIVISION]->(d:Division)<-[:IN_DIVISION]-(t2:Team) WHERE t1.name = $team RETURN t2.name',
                'parameters': {'team': 'Eagles'}
            },
            {
                'description': 'Player connections through trades',
                'query': 'MATCH path = (p1:Player)-[:TRADED_WITH*1..3]-(p2:Player) WHERE p1.name = $player RETURN path',
                'parameters': {'player': 'Tom Brady'}
            }
        ],
        'sql_examples': [
            {
                'description': 'Get team standings by conference',
                'query': 'SELECT name, city, division FROM teams WHERE conference = ? ORDER BY division, name',
                'parameters': ['AFC']
            },
            {
                'description': 'Find games by score difference',
                'query': 'SELECT * FROM games WHERE ABS(home_score - away_score) > ? ORDER BY game_date DESC',
                'parameters': [20]
            },
            {
                'description': 'Player stats by position',
                'query': 'SELECT position, COUNT(*) as count, AVG(height) as avg_height FROM players GROUP BY position',
                'parameters': []
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
