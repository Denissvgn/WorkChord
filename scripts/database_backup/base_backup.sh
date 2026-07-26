#!/usr/bin/env bash
set -euo pipefail

: "${DATABASE_BACKUP_URL:?DATABASE_BACKUP_URL is required}"
: "${DEPLOYMENT_ENVIRONMENT:?DEPLOYMENT_ENVIRONMENT is required}"
: "${BACKUP_ENCRYPTION_CONFIRMED:?BACKUP_ENCRYPTION_CONFIRMED is required}"

if [[ "${BACKUP_ENCRYPTION_CONFIRMED}" != "true" ]]; then
  echo "Base-backup destination encryption has not been confirmed" >&2
  exit 2
fi

backup_root=/backups/base
mkdir -p "${backup_root}"
umask 077
timestamp=$(date -u +%Y%m%dT%H%M%SZ)
temporary=$(mktemp -d "${backup_root}/.workchord-${timestamp}-XXXXXX")
final="${backup_root}/workchord-${timestamp}"
trap 'rm -rf -- "${temporary}"' EXIT

if [[ -e "${final}" ]]; then
  echo "Refusing to overwrite an existing base backup" >&2
  exit 2
fi

pg_basebackup \
  --dbname="${DATABASE_BACKUP_URL}" \
  --pgdata="${temporary}" \
  --format=plain \
  --wal-method=stream \
  --checkpoint=fast \
  --manifest-checksums=SHA256
pg_verifybackup "${temporary}"

(
  cd "${temporary}"
  find . -type f ! -name 'workchord-files.sha256' -print0 \
    | sort -z \
    | xargs -0 sha256sum > workchord-files.sha256
)
sync -f "${temporary}/workchord-files.sha256" "${temporary}"

mv "${temporary}" "${final}"
trap - EXIT
chmod -R go-rwx "${final}"
sync -f "${final}" "${backup_root}"
echo "Base backup complete: $(basename "${final}")"
