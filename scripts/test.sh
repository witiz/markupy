#!/bin/bash

set -euo pipefail

echo ---- ruff format ----
uv run ruff format --check .
echo

echo ----- ruff lint -----
uv run ruff check .
echo

echo ------ pytest -------
uv run pytest
echo

echo ------- mypy --------
uv run mypy src/markupy
echo

echo ----- pyright -------
uv run pyright
echo

echo ====== SUCCESS ======