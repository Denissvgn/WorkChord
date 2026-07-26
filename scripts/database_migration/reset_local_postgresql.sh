#!/usr/bin/env bash
set -euo pipefail

repository_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
if [[ "${DEPLOYMENT_ENVIRONMENT:-development}" == "production" ]]; then
  echo "Local reset is disabled in production" >&2
  exit 2
fi
if [[ "${WORKCHORD_ALLOW_LOCAL_DATABASE_RESET:-}" != "YES" ]]; then
  echo "Set WORKCHORD_ALLOW_LOCAL_DATABASE_RESET=YES to confirm the local reset" >&2
  exit 2
fi
if [[ ! -f "${repository_root}/docker-compose.yml" ]]; then
  echo "Could not resolve the WorkChord repository" >&2
  exit 2
fi

docker compose \
  --project-name workchord \
  --file "${repository_root}/docker-compose.yml" \
  down --volumes --remove-orphans
echo "Removed only the workchord local Compose containers and named volumes"
