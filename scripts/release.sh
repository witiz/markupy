#!/bin/bash

set -euo pipefail

. ${BASH_SOURCE%/*}/test.sh

. ${BASH_SOURCE%/*}/docs.sh

echo --- pypi publish ----
uv run flit publish