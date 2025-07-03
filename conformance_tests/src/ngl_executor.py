from dataclasses import dataclass
from typing import Any, List


@dataclass
class ExecutionResult:
    success: bool
    output: Any
    errors: List[str]


class NGLExecutor:
    def execute(self, func, *args, **kwargs) -> ExecutionResult:
        try:
            result = func(*args, **kwargs)
            return ExecutionResult(True, result, [])
        except Exception as exc:
            return ExecutionResult(False, None, [str(exc)])
