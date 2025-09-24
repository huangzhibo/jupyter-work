# Repository Guidelines

## Project Structure & Module Organization
- Use `main.py` for light experiments only; promote stable code into the `jupyter_work/` package and group modules by feature (e.g., `jupyter_work/notebooks.py`).
- Keep notebooks and large artifacts in `notebooks/` or `data/`, and avoid committing generated outputs; add `.gitignore` rules when new data sources appear.
- Mirror the package layout under `tests/` so every module has a matching test file such as `tests/test_notebooks.py`.

## Build, Test, and Development Commands
- `uv sync`: create or update the virtual environment from `pyproject.toml` and `uv.lock`.
- `uv run python main.py`: execute the CLI entry point with environment isolation.
- `uv run pytest`: run the full test suite; combine with `-k "pattern"` to focus on a subset.
- `uv add <package>`: add dependencies while keeping both manifests synchronized.

## Coding Style & Naming Conventions
- Target Python 3.13 with PEP 8 formatting, 4-space indentation, and 88-character lines.
- Prefer descriptive snake_case for functions and modules, PascalCase for classes, and SCREAMING_SNAKE_CASE for constants.
- Add type hints to public APIs, keep imports explicit, and write concise Google-style docstrings where needed.

## Testing Guidelines
- Use `pytest` with arrange-act-assert structure; fixtures belong in `tests/conftest.py` when shared.
- Name tests `test_<feature>.py` and cover edge cases that keep notebooks deterministic.
- Run `uv run pytest` before every commit; add regression tests alongside bug fixes.

## Commit & Pull Request Guidelines
- Write short, imperative commit messages such as `add data loader`; group related edits and avoid mixing refactors with new features.
- Pull requests should explain motivation, summarize changes, list validation steps (commands, screenshots, notebooks), and link any relevant issues.
- Ensure CI passes before requesting review and respond promptly to feedback.
