from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]

class NGLValidator:
    def validate(self, nodes: List[Dict[str, Any]]) -> ValidationResult:
        errors = []
        ids = set()
        for node in nodes:
            node_id = node.get("id")
            if not node_id:
                errors.append("missing id")
            elif node_id in ids:
                errors.append(f"duplicate id: {node_id}")
            ids.add(node_id)
        return ValidationResult(not errors, errors)
