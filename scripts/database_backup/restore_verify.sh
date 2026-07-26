#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_RESTORE_URL:?DATABASE_RESTORE_URL is required}"
: "${RESTORE_AUTHORIZED_TARGET:?RESTORE_AUTHORIZED_TARGET is required}"
: "${RESTORE_TARGET_IDENTIFIER:?RESTORE_TARGET_IDENTIFIER is required}"
: "${BACKUP_PATH:?BACKUP_PATH is required}"
: "${BACKUP_SHA256:?BACKUP_SHA256 is required}"

resolved_backup=$(realpath -e -- "${BACKUP_PATH}" 2>/dev/null || true)
if [[ ! -f "${resolved_backup}" || "${resolved_backup}" != /backups/logical/* ]]; then
  echo "Backup path must resolve to an existing logical backup under /backups/logical" >&2
  exit 2
fi
actual_sha256=$(sha256sum "${resolved_backup}" | awk '{print $1}')
if [[ "${actual_sha256}" != "${BACKUP_SHA256}" ]]; then
  echo "Backup checksum mismatch" >&2
  exit 2
fi

read -r actual_host actual_port database_name < <(
  psql "${DATABASE_RESTORE_URL}" -X -A -t -v ON_ERROR_STOP=1 \
    -c '\echo :HOST :PORT :DBNAME'
)
actual_target_identifier="${actual_host}:${actual_port}/${database_name}"
if [[ "${RESTORE_TARGET_IDENTIFIER}" != "${actual_target_identifier}" ]]; then
  echo "Restore target identifier does not match the resolved connection" >&2
  exit 2
fi
if [[ "${RESTORE_AUTHORIZED_TARGET}" != "${actual_target_identifier}" ]]; then
  echo "Restore authorization does not match the resolved operator target" >&2
  exit 2
fi
if [[ ! "${database_name}" =~ ^workchord_restore_[a-z0-9]{8,64}$ ]]; then
  echo "Restore target must use workchord_restore_<isolated-id>" >&2
  exit 2
fi
application_tables=$(psql "${DATABASE_RESTORE_URL}" -X -A -t -v ON_ERROR_STOP=1 -c \
  "SELECT count(*) FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')")
if [[ "${application_tables}" != "0" ]]; then
  echo "Restore target is not empty; no destructive cleanup will be attempted" >&2
  exit 2
fi

pg_restore \
  --dbname="${DATABASE_RESTORE_URL}" \
  --exit-on-error \
  --single-transaction \
  --no-owner \
  --no-acl \
  "${resolved_backup}"
psql "${DATABASE_RESTORE_URL}" -X -A -t -v ON_ERROR_STOP=1 \
  -c 'SELECT version_num FROM workchord.alembic_version' >/dev/null
echo "Restore completed into isolated target ${RESTORE_TARGET_IDENTIFIER}; application reconciliation is still required"
