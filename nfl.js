export function executeNFL(src) {
  const nodes = {};
  const edges = [];
  if (!src) return { nodes, edges };
  const lines = src.split(/\r?\n/);
  for (let raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    let m;
    if ((m = line.match(/^(node|fn|pack):([^|]+)(?:\|(.*))?$/))) {
      const id = m[2].trim();
      const props = parseProps(m[3]);
      const label = props.etikedo || props.label || id;
      delete props.etikedo;
      delete props.label;
      nodes[id] = { label, traits: props };
    } else if ((m = line.match(/^trait:([^|]+)(?:\|(.*))?$/))) {
      const id = m[1].trim();
      const props = parseProps(m[2]);
      if (!nodes[id]) nodes[id] = { label: id, traits: {} };
      Object.assign(nodes[id].traits, props);
    } else if ((m = line.match(/^edge:([^\s]+)\s*->\s*([^|\s]+)(?:\|(.*))?$/))) {
      const source = m[1].trim();
      const target = m[2].trim();
      const props = parseProps(m[3]);
      const rel = props.rilato || props.relationship || props.rel || '';
      edges.push({ source, target, relationship_type: rel });
    }
  }
  return { nodes, edges };
}

function parseProps(str) {
  const props = {};
  if (!str) return props;
  const parts = str.split('|');
  for (let part of parts) {
    const t = part.trim();
    if (!t) continue;
    const idx = t.indexOf(':');
    if (idx === -1) continue;
    const key = t.slice(0, idx).trim();
    let val = t.slice(idx + 1).trim();
    if (val.startsWith('"') && val.endsWith('"')) {
      val = val.slice(1, -1);
    }
    props[key] = val;
  }
  return props;
}

export function convertFromNFL(content, format) {
  const graph = typeof content === 'string' ? executeNFL(content) : content;
  switch (format) {
    case 'jsonld': {
      const items = [];
      for (const [id, n] of Object.entries(graph.nodes)) {
        const obj = { '@id': id, '@type': 'Thing', name: n.label, ...n.traits };
        if (n.state !== undefined) {
          obj.state = n.state;
        }
        items.push(obj);
      }
      for (const e of graph.edges) {
        items.push({ '@type': 'Relationship', from: e.source, to: e.target, relationship: e.relationship_type });
      }
      return JSON.stringify({ '@context': 'http://schema.org', '@graph': items }, null, 2);
    }
    case 'csv': {
      const lines = ['id,etikedo'];
      for (const [id, n] of Object.entries(graph.nodes)) {
        lines.push(`${id},${n.label}`);
      }
      return lines.join('\n');
    }
    case 'yaml': {
      let out = '';
      for (const [id, n] of Object.entries(graph.nodes)) {
        out += `${id}:\n  label: "${n.label}"`;
        for (const [k, v] of Object.entries(n.traits)) {
          out += `\n  ${k}: "${v}"`;
        }
        if (n.state !== undefined) {
          out += `\n  state: ${JSON.stringify(n.state)}`;
        }
        out += `\n`;
      }
      return out;
    }
    case 'geojson': {
      const features = [];
      for (const [id, n] of Object.entries(graph.nodes)) {
        const props = { id, label: n.label, ...n.traits };
        if (n.state !== undefined) {
          props.state = n.state;
        }
        features.push({ type: 'Feature', properties: props, geometry: null });
      }
      return JSON.stringify({ type: 'FeatureCollection', features }, null, 2);
    }
    case 'xml': {
      let xml = '';
      for (const [id, n] of Object.entries(graph.nodes)) {
        xml += `<thing id="${id}"><name>${n.label}</name></thing>\n`;
      }
      return xml;
    }
    case 'rdf': {
      let ttl = '';
      for (const [id, n] of Object.entries(graph.nodes)) {
        ttl += `<${id}> a schema:Thing ; schema:name "${n.label}" .\n`;
      }
      return ttl;
    }
    default:
      throw new Error(`Unsupported format: ${format}`);
  }
}

export function convertToNFL(content, format) {
  switch (format) {
    case 'nfl':
      return content;
    case 'jsonld': {
      const data = JSON.parse(content);
      const graph = data['@graph'] || [];
      const lines = [];
      for (const item of graph) {
        if (item.from && item.to) {
          const rel = item.relationship || '';
          lines.push(`edge:${item.from} -> ${item.to}${rel ? ' | rilato:"' + rel + '"' : ''}`);
        } else if (item['@id']) {
          const id = item['@id'];
          const label = item.name || item.label || id;
          lines.push(`node:${id} | etikedo:"${label}"`);
        }
      }
      return lines.join('\n');
    }
    case 'csv': {
      const rows = content.trim().split(/\r?\n/);
      const [header, ...lines] = rows;
      const cols = header.split(',');
      const idxId = cols.indexOf('id');
      const idxLab = cols.indexOf('etikedo');
      const out = [];
      for (const row of lines) {
        const cells = row.split(',');
        const id = cells[idxId];
        const lab = cells[idxLab];
        out.push(`node:${id} | etikedo:"${lab}"`);
      }
      return out.join('\n');
    }
    case 'geojson': {
      const gj = JSON.parse(content);
      const features = gj.features || [];
      const lines = [];
      for (const f of features) {
        const id = f.properties?.id || f.properties?.name;
        if (!id) continue;
        const label = f.properties.name || id;
        lines.push(`node:${id} | etikedo:"${label}"`);
      }
      return lines.join('\n');
    }
    case 'xml': {
      const parser = new DOMParser();
      const doc = parser.parseFromString(content, 'application/xml');
      const nodes = doc.getElementsByTagName('thing');
      const out = [];
      for (const n of nodes) {
        const id = n.getAttribute('id');
        const label = n.getElementsByTagName('name')[0]?.textContent || id;
        out.push(`node:${id} | etikedo:"${label}"`);
      }
      return out.join('\n');
    }
    case 'yaml': {
      const yaml = require('js-yaml');
      const doc = yaml.load(content);
      return Object.entries(doc)
        .map(([id, { name }]) => `node:${id} | etikedo:"${name}"`)
        .join('\n');
    }
    default:
      throw new Error(`Unsupported format: ${format}`);
  }
}
