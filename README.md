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

## Examples

The `examples` directory provides small NFL graphs:

* `simple.json` – minimal nodes and an edge
* `open_permit.json` – basic Open Permit workflow
* `open_tax.json` – property tax relationship

Validate an example with the CLI:

```bash
python3 cli/nfl_cli.py examples/open_permit.json
```
