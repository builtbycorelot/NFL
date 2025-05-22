# Contributing to NFL

Thank you for considering contributing to the NodeForm Language (NFL) tools.

## Reporting Issues

If you encounter a problem or have a feature request, please open an issue on the
project's issue tracker. When reporting a bug include:

- Your operating system and Python version
- Steps to reproduce the issue
- Any relevant error messages or log output

## Development Setup

1. Clone the repository and create a virtual environment.
2. Install the developer requirements:

   ```bash
   pip install -r requirements.txt
   ```

This installs the dependencies listed in [`requirements.txt`](requirements.txt).

## Running Tests

Tests are written with `pytest`. After installing the requirements, run all tests
from the repository root with:

```bash
pytest
```

All new features and fixes should include appropriate tests.

## Coding Style

Code in this repository follows standard Python style conventions (PEP 8). Use
four spaces per indentation level and keep lines reasonably short. When in
doubt, match the style of the existing code.

## Submitting Pull Requests

1. Fork the repository and create a new branch for your change.
2. Add tests that cover your modifications.
3. Ensure `pytest` runs without failures.
4. Submit a pull request describing your changes and the issue it addresses.

Thank you for helping improve NFL!

