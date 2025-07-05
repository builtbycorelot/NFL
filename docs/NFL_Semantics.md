NFL Execution Model
===================

1. Event Dispatch
-----------------
• The system watches for external or internal events.  
• For each Organization node ‘O’,
  for each edge  (O --executes_workflow→ W):
      if  event.name == W.traits.trigger
          then enqueue Workflow W instance scoped to O.

2. Workflow Interpreter
-----------------------
Input: Workflow node W, Organization scope S
for each edge (W --step→ Si) in **file order**:    # sequential semantics
    run Step(Si, scope=S)

3. Step Execution
-----------------
A Step node S has traits:
    action_py | action_js | action_ai | action
The runtime chooses the first implementation available
for its environment:

    if python‑runtime and S.traits.action_py:
         importlib.invoke(S.traits.action_py, scope)
    elif nodejs‑runtime and S.traits.action_js:
         require(...)(scope)
    elif llm‑runtime and S.traits.action_ai:
         openai.call_function(S.traits.action_ai, scope)
    else:
         raise RuntimeError("No implementation")

Trait “logic” inside a Step can now be evaluated by a simple
rule engine.  The engine interprets JSON objects describing
boolean expressions.  Supported forms are:

* `{"expr": "<python expression>"}` – evaluated with the
  step scope bound to ``scope``.
* `{"all": [rule, ...]}` – all nested rules must pass.
* `{"any": [rule, ...]}` – at least one nested rule must pass.
* `{"not": rule}` – negation.
* `{"equals": [a, b]}` – compares values or scope keys.

If a Step defines ``logic`` and the evaluation returns ``False``
the Step implementation is skipped.

4. Failure & Idempotency
------------------------
• Each Step must be idempotent – implementation is responsible.  
• On exception, the interpreter records the error and stops
  further steps; restart logic is left to the orchestrator.

5. Metadata Traits
------------------
Traits such as `label`, `category`, `capabilities`
affect UI and documentation only; they do *not*
change execution.
