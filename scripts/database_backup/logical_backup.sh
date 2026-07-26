#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_BACKUP_URL:?DATABASE_BACKUP_URL is required}"
: "${DEPLOYMENT_ENVIRONMENT:?DEPLOYMENT_ENVIRONMENT is required}"
: "${BACKUP_ENCRYPTION_CONFIRMED:?BACKUP_ENCRYPTION_CONFIRMED is required}"

if [[ "${BACKUP_ENCRYPTION_CONFIRMED}" != "true" ]]; then
  echo "Backup destination encryption has not been confirmed" >&2
  exit 2
fi

backup_root=/backups/logical
if [[ "${backup_root}" != /backups/logical ]]; then
  echo "Unexpected backup root" >&2
  exit 2
fi
mkdir -p "${backup_root}"
umask 077

timestamp=$(date -u +%Y%m%dT%H%M%SZ)
temporary=$(mktemp "${backup_root}/.workchord-${timestamp}-XXXXXX.dump")
final="${backup_root}/workchord-${timestamp}.dump"
manifest="${final}.manifest.json"
trap 'rm -f "${temporary}"' EXIT

if [[ -e "${final}" || -e "${manifest}" ]]; then
  echo "Refusing to overwrite an existing backup artifact" >&2
  exit 2
fi

pg_dump \
  --dbname="${DATABASE_BACKUP_URL}" \
  --format=custom \
  --compress=gzip:6 \
  --no-owner \
  --no-acl \
  --file="${temporary}"
pg_restore --list "${temporary}" >/dev/null
sync -f "${temporary}"

dump_sha256=$(sha256sum "${temporary}" | awk '{print $1}')
dump_bytes=$(stat -c '%s' "${temporary}")
server_version=$(psql "${DATABASE_BACKUP_URL}" -X -A -t -v ON_ERROR_STOP=1 -c 'SHOW server_version')
client_version=$(pg_dump --version | awk '{print $NF}')
mv "${temporary}" "${final}"
trap - EXIT

printf '{\n  "backup_sha256": "%s",\n  "bytes": %s,\n  "client_version": "%s",\n  "created_at": "%s",\n  "encryption_at_rest_confirmed": true,\n  "format": "pg_dump-custom",\n  "kind": "workchord-logical-backup",\n  "server_version": "%s"\n}\n' \
  "${dump_sha256}" "${dump_bytes}" "${client_version}" "${timestamp}" "${server_version}" \
  > "${manifest}"
chmod 600 "${final}" "${manifest}"
sync -f "${final}" "${manifest}" "${backup_root}"

if [[ "${BACKUP_RETENTION_DAYS:-}" =~ ^[0-9]+$ ]]; then
  find "${backup_root}" -maxdepth 1 -type f \
    \( -name 'workchord-*.dump' -o -name 'workchord-*.dump.manifest.json' \) \
    -mtime "+${BACKUP_RETENTION_DAYS}" -delete
fi

echo "Logical backup complete: $(basename "${final}") sha256=${dump_sha256}"
