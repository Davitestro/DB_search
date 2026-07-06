# Contributing

Thanks for helping improve this project.

## Development setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
3. Run a quick smoke test:
   ```bash
   python -c "from main import SmartSearchSystem; print(SmartSearchSystem.__name__)"
   ```

## Coding guidelines

- Keep code readable and documented.
- Prefer small, focused functions and type hints where practical.
- Preserve the existing package structure under the `data`, `models`, `search`, and `config` modules.
- Avoid introducing new dependencies unless they are clearly needed.

## Pull request checklist

- Describe the problem you are solving.
- Include relevant examples or usage notes.
- Verify the package still installs locally with `pip install -e .`.
- If you change behavior, update the documentation in this repository.

## Questions

Open an issue or start a discussion if you need clarification about architecture, design, or contribution steps.
