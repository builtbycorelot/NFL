# Crosswalks

Mappings to external vocabularies help NFL interoperate with existing standards.
- **JSON** 
- **YAML** – simple key/value serialization
- **OWL** – semantic web ontology
- **CityJSON** – geospatial features
- **JSON-LD**
- **princeton wordnet**
- **schema.org** – web entities
- **node**

Example NFL graph in JSON:

```json
{
  "pack": "demo",
  "nodes": [{"name": "A", "type": "Thing"}],
  "edges": []
}
```

### JSON-LD

```json
{
  "@context": "http://schema.org",
  "@graph": [{"@id": "A", "@type": "Thing", "name": "A"}]
}
```

### OWL

```
:A a :Thing .
```

### CityJSON

```json
{
  "type": "CityJSON",
  "version": "1.1",
  "CityObjects": {"A": {"type": "Thing", "attributes": {}}}
}
```

NFL uses this graph format to describe itself in `nfl.schema.json`, which
specifies the required fields for nodes and edges.

