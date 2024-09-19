#!/bin/bash

set -euo pipefail

. ${BASH_SOURCE%/*}/test.sh

uv run flit publish