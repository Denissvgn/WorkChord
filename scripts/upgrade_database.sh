#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR/backend"
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
case "${DEBUG:-}" in
  true|false|True|False|1|0|yes|no|on|off) ;;
  *) export DEBUG=false ;;
esac
exec "$ROOT_DIR/.venv/bin/python" -m app.cli.upgrade "$@"
