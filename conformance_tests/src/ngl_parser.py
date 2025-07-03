import json
from dataclasses import dataclass
from typing import Any, List

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None


@dataclass
class ParseResult:
    valid: bool
    errors: List[str]
    nodes: Any = None


class NGLParser:
    def parse(self, content: str, format: str = "json") -> ParseResult:
        try:
            if format == "json":
                data = json.loads(content)
            elif yaml is not None:
                data = yaml.safe_load(content)
            else:
                raise ImportError("pyyaml required for YAML parsing")
        except Exception as exc:
            return ParseResult(False, [str(exc)], None)
        return ParseResult(True, [], data.get("nodes", []))
