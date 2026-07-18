#!/usr/bin/env bash
set -euo pipefail

archive_root=/var/lib/postgresql/wal-archive
if [[ "${archive_root}" != "/var/lib/postgresql/wal-archive" ]]; then
  echo "Unexpected PostgreSQL WAL archive path" >&2
  exit 2
fi

mkdir -p "${archive_root}"
chown postgres:postgres "${archive_root}"
chmod 0700 "${archive_root}"

exec /usr/local/bin/docker-entrypoint.sh "$@"
