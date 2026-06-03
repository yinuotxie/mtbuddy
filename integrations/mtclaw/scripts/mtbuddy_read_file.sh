#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${MTBUDDY_PYTHON:-python3}"
exec "$PYTHON_BIN" -m mtbuddy.mtclaw_tools mtbuddy_read_file
