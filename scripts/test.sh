#!/bin/bash

set -euo pipefail

echo ---- ruff format ----
uv run ruff format --check src
echo

echo ----- ruff lint -----
uv run ruff check src
echo

echo ------ pytest -------
uv run pytest
echo

echo ------- mypy --------
uv run mypy src
echo

echo ----- pyright -------
uv run pyright
echo

echo ====== SUCCESS ======