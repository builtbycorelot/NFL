# NodeForm Language (NFL)

This repository contains the early notes for the **NodeForm Language**. NFL aims to unify computation and policy through a semantics-first graph syntax.

## Distilled Essence

```
pack meta.core            # zero-th dialect

# define primitive meaning
type ℝ        { doc = "real-32" }
type Spike    { doc = "0|1 event" }

# found-object: pure function node
fn ⊕ (a:ℝ, b:ℝ) -> ℝ { impl = { op = "add" } }

# neuromorphic: spike neuron with STDP plasticity
fn Neuron(id:Int) -> Spike {
  traits = [spike, stdp]
  impl   = { v_th=1.0, leak=0.1 }
}

edge ⊕ -> Neuron { @mcp.topic("lab.snn.input") }
```

NFL graphs are validated via JSON Schema and can compile to diverse runtimes (WASM, CUDA, neuromorphic).

## Core Lexicon

* `node` – declare a node
* `edge` – relate nodes
* `pack` – import dialects
* `fn` – alias for node
* `@call` – invoke a node
* `trait` – qualify behavior
* `impl` – provide the implementation

This syntax keeps the language minimal while remaining expressive across domains.

## Mapping NFL to API Protocols

NFL graphs can be serialized to other messaging or API specifications. The
following outlines how common NFL concepts translate.

### Anthropic MCP

`@mcp.topic` annotations attach an MCP message topic to a node or edge. When the
graph executes, the annotation signals where MCP messages should be published or
consumed, allowing NFL flows to integrate with Anthropic's messaging bus.

### Swagger/OpenAPI

Nodes with HTTP metadata in their `impl` section correspond to OpenAPI
operations. The node's type can map to a schema in the `components` section, and
edges describe the ordering of those operations.

### OpenAIP

OpenAIP models agent actions. When compiling from NFL, each node becomes an
`Action` definition and edges represent the triggers between actions.

### Example graph

```nfl
pack meta.core

fn getUser(id:Int) -> User {
  impl = { http = { method = "GET", path = "/users/{id}" } }
}

fn log(msg:String) -> Void { impl = { op = "log" } }

edge getUser -> log { @mcp.topic("log.http") }
```

- **MCP** – the edge publishes a message to `log.http`.
- **OpenAPI** – `getUser` becomes a `GET /users/{id}` operation and `User`
  defines a schema.
- **OpenAIP** – the two nodes translate to actions with a transition between
  them.
