"""Minimal rule engine for NFL 'logic' trait."""
from __future__ import annotations
from typing import Any, Dict


def evaluate_logic(logic: Dict[str, Any] | None, scope: Dict[str, Any]) -> bool:
    """Evaluate logic against the provided scope.

    The logic format is a simple dictionary supporting:
    - {'expr': '<python expression>'}
    - {'all': [logic, ...]}
    - {'any': [logic, ...]}
    - {'not': logic}
    - {'equals': [left, right]}
    Variables referenced by string names are looked up in scope.
    """
    if not logic:
        return True
    if 'expr' in logic:
        return bool(eval(str(logic['expr']), {}, {'scope': scope}))
    if 'all' in logic:
        return all(evaluate_logic(item, scope) for item in logic['all'])
    if 'any' in logic:
        return any(evaluate_logic(item, scope) for item in logic['any'])
    if 'not' in logic:
        return not evaluate_logic(logic['not'], scope)
    if 'equals' in logic:
        left, right = logic['equals']
        lv = scope.get(left, left) if isinstance(left, str) else left
        rv = scope.get(right, right) if isinstance(right, str) else right
        return lv == rv
    return False


class RuleEngine:
    """Rule engine evaluating logic objects against a scope."""

    def __init__(self, scope: Dict[str, Any] | None = None) -> None:
        self.scope = scope or {}

    def evaluate(self, logic: Dict[str, Any] | None) -> bool:
        return evaluate_logic(logic, self.scope)
