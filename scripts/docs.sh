#!/bin/bash

set -euo pipefail

. ${BASH_SOURCE%/*}/test.sh

echo ---- docs deploy ----
uv run mkdocs gh-deploy --force
