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

## CLI Usage

The repository provides a small command line tool for validating NFL graphs and
exporting them as an OpenAPI specification:

```bash
$ python -m cli.nfl_cli examples/simple.json --export-openapi graph.openapi.json
```

The generated `graph.openapi.json` contains a basic OpenAPI 3.0 document with
`/nodes` and `/edges` endpoints that describe the graph structure.

## Pilot Platform Mappings

The repository also includes a more complete example under the `pilot` file.
This schema combines the minimal `open_permit.json` and `open_tax.json`
concepts into a unified model with nodes such as `Party`, `Task`,
`Transaction`, and `PermitApplication`. Each of these nodes contains
`@platform` sections that map its fields to specific SaaS providers,
demonstrating how the same semantics can synchronize data across Smartsheet,
Intuit QuickBooks Online, and HubSpot.

## Running Tests

The project uses `pytest` for its test suite. After installing the
requirements (only `pytest` is needed), run the tests from the repository
root:

```bash
$ pytest
```
