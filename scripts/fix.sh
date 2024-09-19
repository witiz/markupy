#!/bin/bash

set -euo pipefail

uv run ruff format .
uv run ruff check --fix .