from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import psycopg2
import psycopg2.extras
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
POSTGRES_URI = os.getenv('POSTGRES_URI', 'dbname=nfl user=nfl password=nfl host=localhost')

# Neo4j driver (optional)
if NEO4J_URI:
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        def init_neo4j_schema():
            """Create indexes and constraints required by the API."""
            schema_path = os.path.join(os.path.dirname(__file__), 'schema', 'neo4j_schema.cypher')
            if not os.path.exists(schema_path):
                return
            with open(schema_path, 'r', encoding='utf-8') as fh:
                statements = [s.strip() for s in fh.read().split(';') if s.strip()]
            with driver.session() as session:
                for stmt in statements:
                    session.run(stmt)
        init_neo4j_schema()
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

# Initialize PostgreSQL database if enabled
def init_postgres():
    if not POSTGRES_URI:
        return
    try:
        conn = psycopg2.connect(POSTGRES_URI)
    except Exception:
        return
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            conference TEXT,
            division TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
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
        """
    )
    cursor.execute(
        """
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
        """
    )
    conn.commit()
    conn.close()

# Initialize on startup
init_postgres()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'NodeForm Query API'})


@app.route('/db/health', methods=['GET'])
def db_health():
    """Check connectivity to Neo4j and PostgreSQL."""
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
    if POSTGRES_URI:
        try:
            conn = psycopg2.connect(POSTGRES_URI)
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            status['postgres'] = 'ok'
        except Exception:
            status['postgres'] = 'error'
    else:
        status['postgres'] = 'disabled'
    latency['postgres'] = round((time.perf_counter() - start) * 1000, 2)

    return jsonify({
        'neo4j': status['neo4j'],
        'postgres': status['postgres'],
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
    Execute Cypher queries against the Neo4j graph database

    Expected JSON payload:
    {
        "query": "MATCH (g:Group)-[:HAS_MEMBER]->(m:Member) WHERE g.name = $group_name RETURN m",
        "parameters": {"group_name": "ExampleGroup"}
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
    Execute SQL queries against the PostgreSQL database

    Expected JSON payload:
    {
        "query": "SELECT * FROM teams WHERE conference = %s",
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

        if not POSTGRES_URI:
            return jsonify({'error': 'PostgreSQL disabled'}), 503

        conn = psycopg2.connect(POSTGRES_URI)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(query, parameters)
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        results = [dict(row) for row in rows]

        cursor.close()
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
def import_graph_data():
    """
    Import NodeForm JSON data into both databases
    """
    try:
        data = request.json

        # Validate against NFL schema first
        # ... validation logic ...

        # Import to PostgreSQL
        if POSTGRES_URI:
            conn = psycopg2.connect(POSTGRES_URI)
            cursor = conn.cursor()

            # Import entities
            for team in data.get('teams', []):
                cursor.execute(
                    """
                    INSERT INTO teams (id, name, city, conference, division)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        city = EXCLUDED.city,
                        conference = EXCLUDED.conference,
                        division = EXCLUDED.division
                    """,
                    (
                        team['id'],
                        team['name'],
                        team.get('city'),
                        team.get('conference'),
                        team.get('division'),
                    ),
                )

            conn.commit()
            cursor.close()
            conn.close()

        # Import to Neo4j if available
        if driver is not None:
            with driver.session() as session:
                # Clear existing data
                session.run("MATCH (n) DETACH DELETE n")

                # Import entities as nodes
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
                'description': 'Find all members of a particular group',
                'query': 'MATCH (g:Group {name: $group})-[:HAS_MEMBER]->(m:Member) RETURN m.name, m.role',
                'parameters': {'group': 'ExampleGroup'}
            },
            {
                'description': 'Find groups in the same category',
                'query': 'MATCH (g1:Group)-[:IN_CATEGORY]->(c:Category)<-[:IN_CATEGORY]-(g2:Group) WHERE g1.name = $group RETURN g2.name',
                'parameters': {'group': 'GroupA'}
            },
            {
                'description': 'Member connections through interactions',
                'query': 'MATCH path = (m1:Member)-[:INTERACTED_WITH*1..3]-(m2:Member) WHERE m1.name = $member RETURN path',
                'parameters': {'member': 'Alice'}
            }
        ],
        'sql_examples': [
            {
                'description': 'Get group counts by category',
                'query': 'SELECT name, category FROM groups WHERE category = %s ORDER BY name',
                'parameters': ['Category1']
            },
            {
                'description': 'Find events by metric difference',
                'query': 'SELECT * FROM events WHERE ABS(metric_a - metric_b) > %s ORDER BY event_date DESC',
                'parameters': [20]
            },
            {
                'description': 'Member stats by role',
                'query': 'SELECT role, COUNT(*) as count, AVG(value) as avg_value FROM members GROUP BY role',
                'parameters': []
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
