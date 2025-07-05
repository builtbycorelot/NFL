import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nfl.rules import evaluate_logic, RuleEngine


def test_rule_expr():
    assert evaluate_logic({"expr": "scope['a'] > 1"}, {"a": 2})
    assert not evaluate_logic({"expr": "scope['a'] > 1"}, {"a": 0})


def test_rule_engine_all_any():
    engine = RuleEngine({"x": 1, "y": 2})
    logic = {"all": [{"equals": ["x", 1]}, {"equals": ["y", 2]}]}
    assert engine.evaluate(logic)
