'use strict';
const fs = require('fs').promises;
const yaml = require('js-yaml');
const { Parser, Writer } = require('n3'); // For Turtle/RDF
const neo4j = require('neo4j-driver');
const { Database } = require('arangojs');
const csvStringify = require('csv-stringify/sync');

// NFL Parser
async function parseNFL(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const lines = content.split('\n');
  let pack = { metadata: {}, nodes: {}, edges: [] };
  let currentNode = null;
  let currentTrait = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;

    if (line.startsWith('pack:')) {
      pack.metadata.name = trimmed.split(' ')[1];
    } else if (line.startsWith('  | title:')) {
      pack.metadata.title = trimmed.match(/: "(.*)"/)[1];
    } else if (line.startsWith('  | version:')) {
      pack.metadata.version = trimmed.match(/: "(.*)"/)[1];
    } else if (line.startsWith('node:')) {
      const id = trimmed.split(' ')[1];
      currentNode = { id, properties: {}, traits: {} };
      pack.nodes[id] = currentNode;
    } else if (line.startsWith('edge:')) {
      const edgeMatch = trimmed.match(/^edge:\s+(\S+)\s+->\s+(?:([^\s]+)\s+->\s+)?(\S+)/);
      if (edgeMatch) {
        const [, src, rel, tgt] = edgeMatch;
        pack.edges.push({ source: src, relationship: rel || 'relatedTo', target: tgt, properties: {} });
      }
      currentNode = null;
    } else if (line.startsWith('  | trait.')) {
      currentTrait = trimmed.match(/trait\.(\w+)/)[1];
      currentNode.traits[currentTrait] = {};
    } else if (line.startsWith('  | ') || line.startsWith('    | ')) {
      const text = trimmed.slice(2);
      const idx = text.indexOf(':');
      const key = text.slice(0, idx).trim();
      let value = text.slice(idx + 1).trim();
      value = value.replace(/^"|"$/g, '');
      if (line.startsWith('    | ')) {
        currentNode.traits[currentTrait][key] = value;
      } else if (currentNode) {
        currentNode.properties[key] = value;
      } else {
        pack.edges[pack.edges.length - 1].properties[key] = value;
      }
    }
  }
  return pack;
}

// NFL to JSON-LD
function toJSONLD(nflData) {
  const jsonld = {
    '@context': 'http://schema.org',
    '@graph': []
  };
  for (const [id, node] of Object.entries(nflData.nodes)) {
    const nodeObj = {
      '@id': `urn:nfl:${id}`,
      '@type': node.properties.isa || 'Thing',
      name: node.properties.name,
      description: node.properties.description
    };
    for (const [trait, props] of Object.entries(node.traits)) {
      nodeObj[`${trait}_trait`] = props;
    }
    jsonld['@graph'].push(nodeObj);
  }
  for (const edge of nflData.edges) {
    jsonld['@graph'].push({
      '@id': `urn:nfl:edge_${edge.source}_${edge.relationship}_${edge.target}`,
      '@type': 'Relationship',
      source: `urn:nfl:${edge.source}`,
      target: `urn:nfl:${edge.target}`,
      relationship: edge.relationship,
      ...edge.properties
    });
  }
  return jsonld;
}

// JSON-LD to NFL
function fromJSONLD(jsonld) {
  let nfl = `pack: Converted_Pack\n  | title: "Converted from JSON-LD"\n  | version: "2025-07-04"\n\n`;
  for (const item of jsonld['@graph']) {
    if (item['@type'] !== 'Relationship') {
      const id = item['@id'].replace('urn:nfl:', '');
      nfl += `node: ${id}\n`;
      nfl += `  | isa: "${item['@type']}"\n`;
      if (item.name) nfl += `  | name: "${item.name}"\n`;
      if (item.description) nfl += `  | description: "${item.description}"\n`;
      for (const [key, props] of Object.entries(item)) {
        if (key.endsWith('_trait')) {
          const traitName = key.replace('_trait', '');
          nfl += `  | trait.${traitName}\n`;
          for (const [prop, value] of Object.entries(props)) {
            nfl += `    | ${prop}: ${value}\n`;
          }
        }
      }
      nfl += '\n';
    } else {
      const source = item.source.replace('urn:nfl:', '');
      const target = item.target.replace('urn:nfl:', '');
      nfl += `edge: ${source} -> ${item.relationship} -> ${target}\n`;
      for (const [key, value] of Object.entries(item)) {
        if (!['@id', '@type', 'source', 'target', 'relationship'].includes(key)) {
          nfl += `  | ${key}: "${value}"\n`;
        }
      }
      nfl += '\n';
    }
  }
  return nfl;
}

// NFL to CSV
function toCSV(nflData) {
  const nodes = [];
  const edges = [];
  for (const [id, node] of Object.entries(nflData.nodes)) {
    const row = { id, isa: node.properties.isa, name: node.properties.name, description: node.properties.description };
    for (const [trait, props] of Object.entries(node.traits)) {
      for (const [key, value] of Object.entries(props)) {
        row[`${trait}_${key}`] = value;
      }
    }
    nodes.push(row);
  }
  for (const edge of nflData.edges) {
    edges.push({ source: edge.source, relationship: edge.relationship, target: edge.target, ...edge.properties });
  }
  return {
    nodes: csvStringify(nodes, { header: true }),
    edges: csvStringify(edges, { header: true })
  };
}

// CSV to NFL
function fromCSV({ nodes, edges }) {
  const [nodeHeader, ...nodeLines] = nodes.trim().split('\n');
  const nodeHeaders = nodeHeader.split(',');
  const [edgeHeader, ...edgeLines] = edges.trim().split('\n');
  const edgeHeaders = edgeHeader.split(',');
  let nfl = `pack: Converted_Pack\n  | title: "Converted from CSV"\n  | version: "2025-07-04"\n\n`;

  for (const line of nodeLines) {
    if (!line) continue;
    const values = line.split(',').map(s => s.replace(/^"|"$/g, ''));
    const row = {};
    nodeHeaders.forEach((h, idx) => { row[h] = values[idx]; });
    const { id, isa, name, description, ...rest } = row;
    nfl += `node: ${id}\n`;
    nfl += `  | isa: "${isa}"\n`;
    if (name) nfl += `  | name: "${name}"\n`;
    if (description) nfl += `  | description: "${description}"\n`;
    const stats = {};
    for (const [key, val] of Object.entries(rest)) {
      if (val && key.startsWith('stats_')) {
        stats[key.replace('stats_', '')] = val;
      }
    }
    if (Object.keys(stats).length) {
      nfl += `  | trait.stats\n`;
      for (const [key, value] of Object.entries(stats)) {
        nfl += `    | ${key}: ${value}\n`;
      }
    }
    nfl += '\n';
  }
  
  for (const line of edgeLines) {
    if (!line) continue;
    const values = line.split(',').map(s => s.replace(/^"|"$/g, ''));
    const row = {};
    edgeHeaders.forEach((h, idx) => { row[h] = values[idx]; });
    const { source, relationship, target, ...props } = row;
    nfl += `edge: ${source} -> ${relationship} -> ${target}\n`;
    for (const [k, v] of Object.entries(props)) {
      if (v) nfl += `  | ${k}: "${v}"\n`;
    }
    nfl += '\n';
  }
  return nfl;
}

// NFL to YAML
function toYAML(nflData) {
  const yamlData = { nodes: {}, edges: [] };
  for (const [id, node] of Object.entries(nflData.nodes)) {
    yamlData.nodes[id] = { ...node.properties, traits: node.traits };
  }
  yamlData.edges = nflData.edges;
  return yaml.safeDump(yamlData, { indent: 2 });
}

// YAML to NFL
function fromYAML(yamlStr) {
  const yamlData = yaml.safeLoad(yamlStr);
  let nfl = `pack: Converted_Pack\n  | title: "Converted from YAML"\n  | version: "2025-07-04"\n\n`;
  for (const [id, node] of Object.entries(yamlData.nodes)) {
    nfl += `node: ${id}\n`;
    for (const [key, value] of Object.entries(node)) {
      if (key !== 'traits') nfl += `  | ${key}: "${value}"\n`;
    }
    for (const [trait, props] of Object.entries(node.traits || {})) {
      nfl += `  | trait.${trait}\n`;
      for (const [key, value] of Object.entries(props)) {
        nfl += `    | ${key}: ${value}\n`;
      }
    }
    nfl += '\n';
  }
  for (const edge of yamlData.edges) {
    nfl += `edge: ${edge.source} -> ${edge.relationship} -> ${edge.target}\n`;
    for (const [key, value] of Object.entries(edge.properties)) {
      nfl += `  | ${key}: "${value}"\n`;
    }
    nfl += '\n';
  }
  return nfl;
}

// NFL to Turtle
async function toTurtle(nflData) {
  const writer = new Writer({ prefixes: { nfl: 'http://example.org/nfl#' } });
  for (const [id, node] of Object.entries(nflData.nodes)) {
    writer.addTriple(`nfl:${id}`, 'rdf:type', `nfl:${node.properties.isa}`);
    writer.addTriple(`nfl:${id}`, 'schema:name', `"${node.properties.name}"`);
    writer.addTriple(`nfl:${id}`, 'schema:description', `"${node.properties.description}"`);
    for (const [trait, props] of Object.entries(node.traits)) {
      for (const [key, value] of Object.entries(props)) {
        writer.addTriple(`nfl:${id}`, `nfl:${trait}_${key}`, value);
      }
    }
  }
  for (const edge of nflData.edges) {
    writer.addTriple(`nfl:${edge.source}`, `nfl:${edge.relationship}`, `nfl:${edge.target}`);
    for (const [key, value] of Object.entries(edge.properties)) {
      writer.addTriple(`nfl:edge_${edge.source}_${edge.relationship}_${edge.target}`, `nfl:${key}`, `"${value}"`);
    }
  }
  return new Promise(resolve => writer.end((err, result) => resolve(result)));
}

// Turtle to NFL
async function fromTurtle(turtleStr) {
  const parser = new Parser();
  const triples = [];
  parser.parse(turtleStr, (err, triple) => { if (triple) triples.push(triple); });
  let nfl = `pack: Converted_Pack\n  | title: "Converted from Turtle"\n  | version: "2025-07-04"\n\n`;
  const nodes = {};
  const edges = {};

  for (const triple of triples) {
    const subject = triple.subject.id.replace('http://example.org/nfl#', '');
    const predicate = triple.predicate.id.replace('http://example.org/nfl#', '');
    const object = triple.object.id.startsWith('http://example.org/nfl#') 
      ? triple.object.id.replace('http://example.org/nfl#', '') 
      : triple.object.id.replace(/^"|"$/g, '');

    if (!nodes[subject]) nodes[subject] = { properties: {}, traits: {} };
    if (predicate === 'rdf:type') {
      nodes[subject].properties.isa = object;
    } else if (predicate === 'schema:name') {
      nodes[subject].properties.name = object;
    } else if (predicate === 'schema:description') {
      nodes[subject].properties.description = object;
    } else if (predicate.startsWith('stats_')) {
      nodes[subject].traits.stats = nodes[subject].traits.stats || {};
      nodes[subject].traits.stats[predicate.replace('stats_', '')] = object;
    } else if (!predicate.includes('_')) {
      edges[`${subject}_${predicate}_${object}`] = { source: subject, relationship: predicate, target: object, properties: {} };
    } else if (predicate !== 'since') {
      const edgeId = Object.keys(edges).find(k => k.includes(subject));
      if (edgeId) edges[edgeId].properties[predicate] = object;
    }
  }

  for (const [id, node] of Object.entries(nodes)) {
    nfl += `node: ${id}\n`;
    for (const [key, value] of Object.entries(node.properties)) {
      nfl += `  | ${key}: "${value}"\n`;
    }
    for (const [trait, props] of Object.entries(node.traits)) {
      nfl += `  | trait.${trait}\n`;
      for (const [key, value] of Object.entries(props)) {
        nfl += `    | ${key}: ${value}\n`;
      }
    }
    nfl += '\n';
  }
  for (const edge of Object.values(edges)) {
    nfl += `edge: ${edge.source} -> ${edge.relationship} -> ${edge.target}\n`;
    for (const [key, value] of Object.entries(edge.properties)) {
      nfl += `  | ${key}: "${value}"\n`;
    }
    nfl += '\n';
  }
  return nfl;
}

// NFL to GraphQL Schema
function toGraphQL(nflData) {
  let schema = `
 type Query {
  nodes: [Node]
  edges: [Edge]
 }
 type Node {
  id: ID!
  isa: String
  name: String
  description: String
  stats: Stats
 }
 type Edge {
  source: ID!
  relationship: String!
  target: ID!
  since: String
 }
 type Stats {
  passing_yards: Int
  rushing_yards: Int
  touchdowns: Int
 }
 `;
  const data = { nodes: [], edges: [] };
  for (const [id, node] of Object.entries(nflData.nodes)) {
    data.nodes.push({ id, ...node.properties, stats: node.traits.stats || {} });
  }
  data.edges = nflData.edges;
  return { schema, data };
}

// GraphQL to NFL (assumes data, not schema)
function fromGraphQL({ nodes, edges }) {
  let nfl = `pack: Converted_Pack\n  | title: "Converted from GraphQL"\n  | version: "2025-07-04"\n\n`;
  for (const node of nodes) {
    nfl += `node: ${node.id}\n`;
    for (const [key, value] of Object.entries(node)) {
      if (key !== 'id' && key !== 'stats' && value) nfl += `  | ${key}: "${value}"\n`;
    }
    if (node.stats && Object.keys(node.stats).length) {
      nfl += `  | trait.stats\n`;
      for (const [key, value] of Object.entries(node.stats)) {
        nfl += `    | ${key}: ${value}\n`;
      }
    }
    nfl += '\n';
  }
  for (const edge of edges) {
    nfl += `edge: ${edge.source} -> ${edge.relationship} -> ${edge.target}\n`;
    for (const [key, value] of Object.entries(edge)) {
      if (!['source', 'relationship', 'target'].includes(key) && value) {
        nfl += `  | ${key}: "${value}"\n`;
      }
    }
    nfl += '\n';
  }
  return nfl;
}

// NFL to Neo4j
async function toNeo4j(nflData, uri, user, password) {
  const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  const session = driver.session();
  try {
    for (const [id, node] of Object.entries(nflData.nodes)) {
      const labels = [node.properties.isa || 'Thing'];
      if (!labels.includes('Thing')) labels.push('Thing');
      const props = { id, ...node.properties, stats: node.traits.stats || {} };
      await session.run(
        `CREATE (n:${labels.join(':')} $props)`,
        { props }
      );
    }
    for (const edge of nflData.edges) {
      await session.run(
        `MATCH (s {id: $source}), (t {id: $target})
         CREATE (s)-[r:${edge.relationship.toUpperCase()} $props]->(t)`,
        { source: edge.source, target: edge.target, props: edge.properties }
      );
    }
  } finally {
    await session.close();
    await driver.close();
  }
}

// Neo4j to NFL
async function fromNeo4j(uri, user, password) {
  const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  const session = driver.session();
  let nfl = `pack: Converted_Pack\n  | title: "Converted from Neo4j"\n  | version: "2025-07-04"\n\n`;
  try {
    const nodesResult = await session.run('MATCH (n) RETURN n');
    for (const record of nodesResult.records) {
      const node = record.get('n').properties;
      const labels = record.get('n').labels;
      const isa = labels.find(l => l !== 'Thing') || 'Thing';
      nfl += `node: ${node.id}\n`;
      nfl += `  | isa: "${isa}"\n`;
      if (node.name) nfl += `  | name: "${node.name}"\n`;
      if (node.description) nfl += `  | description: "${node.description}"\n`;
      if (node.stats && Object.keys(node.stats).length) {
        nfl += `  | trait.stats\n`;
        for (const [key, value] of Object.entries(node.stats)) {
          nfl += `    | ${key}: ${value}\n`;
        }
      }
      nfl += '\n';
    }
    const edgesResult = await session.run('MATCH ()-[r]->() RETURN r, startNode(r).id AS source, endNode(r).id AS target');
    for (const record of edgesResult.records) {
      const rel = record.get('r');
      const source = record.get('source');
      const target = record.get('target');
      nfl += `edge: ${source} -> ${rel.type.toLowerCase()} -> ${target}\n`;
      for (const [key, value] of Object.entries(rel.properties)) {
        nfl += `  | ${key}: "${value}"\n`;
      }
      nfl += '\n';
    }
  } finally {
    await session.close();
    await driver.close();
  }
  return nfl;
}

// NFL to ArangoDB
async function toArangoDB(nflData, url, database, user, password) {
  const db = new Database({ url, databaseName: database });
  db.useBasicAuth(user, password);
  const nodes = await db.collection('nodes');
  const edges = await db.collection('edges');
  for (const [id, node] of Object.entries(nflData.nodes)) {
    await nodes.save({ _key: id, ...node.properties, traits: node.traits });
  }
  for (const edge of nflData.edges) {
    await edges.save({
      _from: `nodes/${edge.source}`,
      _to: `nodes/${edge.target}`,
      relationship: edge.relationship,
      ...edge.properties
    });
  }
}

// ArangoDB to NFL
async function fromArangoDB(url, database, user, password) {
  const db = new Database({ url, databaseName: database });
  db.useBasicAuth(user, password);
  let nfl = `pack: Converted_Pack\n  | title: "Converted from ArangoDB"\n  | version: "2025-07-04"\n\n`;
  const nodes = await db.collection('nodes').all();
  for await (const node of nodes) {
    nfl += `node: ${node._key}\n`;
    for (const [key, value] of Object.entries(node)) {
      if (key !== '_key' && key !== '_id' && key !== '_rev' && key !== 'traits' && value) {
        nfl += `  | ${key}: "${value}"\n`;
      }
    }
    for (const [trait, props] of Object.entries(node.traits || {})) {
      nfl += `  | trait.${trait}\n`;
      for (const [key, value] of Object.entries(props)) {
        nfl += `    | ${key}: ${value}\n`;
      }
    }
    nfl += '\n';
  }
  const edges = await db.collection('edges').all();
  for await (const edge of edges) {
    const source = edge._from.replace('nodes/', '');
    const target = edge._to.replace('nodes/', '');
    nfl += `edge: ${source} -> ${edge.relationship} -> ${target}\n`;
    for (const [key, value] of Object.entries(edge)) {
      if (!['_from', '_to', 'relationship', '_id', '_key', '_rev'].includes(key)) {
        nfl += `  | ${key}: "${value}"\n`;
      }
    }
    nfl += '\n';
  }
  return nfl;
}

// Example Usage
async function main() {
  const nflFile = 'sample.nfl';
  const nflData = await parseNFL(nflFile);

  // To JSON-LD
  const jsonld = toJSONLD(nflData);
  await fs.writeFile('output.jsonld', JSON.stringify(jsonld, null, 2));
  const nflFromJSONLD = fromJSONLD(jsonld);
  await fs.writeFile('from_jsonld.nfl', nflFromJSONLD);

  // To CSV
  const csv = toCSV(nflData);
  await fs.writeFile('nodes.csv', csv.nodes);
  await fs.writeFile('edges.csv', csv.edges);
  const nflFromCSV = fromCSV(csv);
  await fs.writeFile('from_csv.nfl', nflFromCSV);

  // To YAML
  const yamlStr = toYAML(nflData);
  await fs.writeFile('output.yaml', yamlStr);
  const nflFromYAML = fromYAML(yamlStr);
  await fs.writeFile('from_yaml.nfl', nflFromYAML);

  // To Turtle
  const turtle = await toTurtle(nflData);
  await fs.writeFile('output.ttl', turtle);
  const nflFromTurtle = await fromTurtle(turtle);
  await fs.writeFile('from_turtle.nfl', nflFromTurtle);

  // To GraphQL
  const { schema, data } = toGraphQL(nflData);
  await fs.writeFile('schema.graphql', schema);
  await fs.writeFile('data.json', JSON.stringify(data, null, 2));
  const nflFromGraphQL = fromGraphQL(data);
  await fs.writeFile('from_graphql.nfl', nflFromGraphQL);

  // To Neo4j
  await toNeo4j(nflData, 'bolt://localhost:7687', 'neo4j', 'password');
  const nflFromNeo4j = await fromNeo4j('bolt://localhost:7687', 'neo4j', 'password');
  await fs.writeFile('from_neo4j.nfl', nflFromNeo4j);

  // To ArangoDB
  await toArangoDB(nflData, 'http://localhost:8529', 'nfl_db', 'root', 'password');
  const nflFromArangoDB = await fromArangoDB('http://localhost:8529', 'nfl_db', 'root', 'password');
  await fs.writeFile('from_arangodb.nfl', nflFromArangoDB);
}

main().catch(console.error);
