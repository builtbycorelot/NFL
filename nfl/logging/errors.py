class NFLError(Exception):
    """Base class for NFL errors."""

    code = "NFL000"

    def __init__(self, message: str):
        super().__init__(f"[{self.code}] {message}")


class ValidationError(NFLError):
    code = "NFL100"


class ExecutionError(NFLError):
    code = "NFL200"
