#!/bin/bash

set -euo pipefail

. ${BASH_SOURCE%/*}/test.sh

echo --- pypi publish ----
uv run flit publish