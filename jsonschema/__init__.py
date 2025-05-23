class ValidationError(Exception):
    """Raised when validation fails."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class SchemaError(Exception):
    """Raised for invalid schemas."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

def validate(instance, schema):
    if not isinstance(schema, dict):
        raise SchemaError("Schema must be a dictionary")
    if not isinstance(instance, dict):
        raise ValidationError("Instance must be a dictionary")
    # Minimal checks: require 'pack' key to exist
    if "pack" not in instance:
        raise ValidationError("'pack' property missing")
    # optional: if nodes present, must be list
    if "nodes" in instance and not isinstance(instance["nodes"], list):
        raise ValidationError("'nodes' must be a list")
    if "edges" in instance and not isinstance(instance["edges"], list):
        raise ValidationError("'edges' must be a list")
