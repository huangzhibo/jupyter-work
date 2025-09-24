# Repository Guidelines

## Project Structure & Module Organization
`main.py` currently contains the CLI-like entry point; keep quick experiments there only temporarily. As features grow, create a `jupyter_work/` package for reusable modules and keep files grouped by responsibility (e.g., `jupyter_work/notebooks.py`). Store datasets or notebooks under a `data/` or `notebooks/` directory and avoid committing large artifacts. Add tests under `tests/` mirroring the module hierarchy (e.g., `tests/test_notebooks.py` for `jupyter_work/notebooks.py`) so discovery remains predictable.

## Build, Test, and Development Commands
- `uv sync` – install or update the local virtual environment from `pyproject.toml` and `uv.lock`.
- `uv run python main.py` – execute the current entry point exactly as CI would.
- `uv run pytest` – run the automated test suite; add `-k "<pattern>"` to target specific tests.
- `uv add <package>` – add a runtime or dev dependency while keeping both manifests in sync.

## Coding Style & Naming Conventions
Write Python 3.13 code following PEP 8 with 4-space indentation and a maximum line length of 88 characters. Use descriptive snake_case for functions and modules, PascalCase for classes, and SCREAMING_SNAKE_CASE for constants. Prefer explicit imports over star imports. Include type hints on public functions and keep docstrings concise using Google-style formatting when documentation is needed.

## Testing Guidelines
Adopt `pytest` for all new tests. Name files `test_<feature>.py` and structure tests with clear arrange-act-assert sections. Provide fixture helpers in `tests/conftest.py` once shared setup emerges. Target meaningful edge cases, and ensure tests remain deterministic so they can run in isolation. Run `uv run pytest` before pushing and add regression tests alongside bug fixes.

## Commit & Pull Request Guidelines
Commits should use short, imperative summaries (e.g., `add data loader`). Group related changes and avoid mixing refactors with feature work. For pull requests, describe the motivation, summarize key changes, list how you validated them (commands, screenshots, or notebooks), and link any related issues. Request a review once CI passes and respond to feedback promptly.
