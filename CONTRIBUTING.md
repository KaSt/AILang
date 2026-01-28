# Contributing to AILANG

Thank you for your interest in contributing to AILANG! 

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ailang.git
   cd ailang
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```

## Development

### Project Structure

```
ailang/
├── src/ailang/
│   ├── __init__.py      # Package exports
│   ├── core.py          # Main AILANG class
│   ├── parser.py        # AILANG syntax parser
│   ├── transpiler.py    # AILANG ↔ natural language
│   ├── providers.py     # AI provider adapters
│   ├── cli.py           # Command line interface
│   └── server.py        # REST API server
├── docs/
│   ├── SPECIFICATION.md # Language specification
│   ├── COMMANDS.md      # Command dictionary
│   └── API.md           # API reference
├── examples/            # Usage examples
├── tests/               # Test suite
└── pyproject.toml       # Package config
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=ailang

# Specific test file
pytest tests/test_parser.py
```

### Code Style

We use:
- `ruff` for linting
- `black` for formatting
- `mypy` for type checking

```bash
# Format
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

## Adding Features

### New Commands

1. Add the command to `ACTION_TEMPLATES` in `transpiler.py`
2. Add to the appropriate category in `docs/COMMANDS.md`
3. Add validation in `parser.py` if needed
4. Write tests

### New Modifiers

1. Add to the appropriate expansion dict in `transpiler.py`:
   - `MUST_EXPANSIONS` for `!` modifiers
   - `PRIORITY_EXPANSIONS` for `^` modifiers
   - `AVOID_EXPANSIONS` for `_` modifiers
2. Document in `docs/COMMANDS.md`
3. Write tests

### New Providers

1. Create a new class extending `Provider` in `providers.py`
2. Implement `complete()` and optionally `complete_with_image()`
3. Add to the `PROVIDERS` dict
4. Document in README

## Pull Requests

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests: `pytest`
4. Run linting: `ruff check . && black --check .`
5. Commit with a clear message
6. Push and create a PR

## Reporting Issues

When reporting bugs, please include:
- AILANG version (`ailang --version`)
- Python version
- Full error message/traceback
- Minimal reproduction example

## Questions?

Open a discussion on GitHub or reach out to the maintainers.

Thank you for contributing! 🚀
