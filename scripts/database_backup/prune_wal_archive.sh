#!/usr/bin/env bash
# Prune archived WAL segments that point-in-time recovery no longer needs.
#
# The oldest segment still needed is the one named by `START WAL LOCATION` in
# the backup_label of the Nth newest verified base backup (default N=1). A base
# backup counts as verified only when base_backup.sh finished it: the final
# directory exists (it is renamed into place after pg_verifybackup passes) and
# holds both backup_label and workchord-files.sha256. With no verified base
# backup nothing is deleted. Safe to run repeatedly.
#
# Usage: prune_wal_archive.sh [--dry-run]
# Environment:
#   WAL_ARCHIVE_DIR          archive directory (default /var/lib/postgresql/wal-archive)
#   BASE_BACKUP_ROOT         base backup directory (default /backups/base)
#   WAL_PRUNE_KEEP_BACKUPS   how many newest verified base backups stay
#                            recoverable to the present (default 1)
#   WAL_PRUNE_DRY_RUN=true   same as --dry-run
#   PG_ARCHIVECLEANUP        pg_archivecleanup binary (default pg_archivecleanup)
set -euo pipefail

archive_dir=${WAL_ARCHIVE_DIR:-/var/lib/postgresql/wal-archive}
backup_root=${BASE_BACKUP_ROOT:-/backups/base}
keep=${WAL_PRUNE_KEEP_BACKUPS:-1}
cleanup=${PG_ARCHIVECLEANUP:-pg_archivecleanup}
dry_run=${WAL_PRUNE_DRY_RUN:-false}

for argument in "$@"; do
  case "${argument}" in
    --dry-run) dry_run=true ;;
    *) echo "Unknown argument: ${argument}" >&2; exit 2 ;;
  esac
done

if [[ ! "${keep}" =~ ^[1-9][0-9]*$ ]]; then
  echo "WAL_PRUNE_KEEP_BACKUPS must be a positive integer" >&2
  exit 2
fi
if [[ ! -d "${archive_dir}" ]]; then
  echo "WAL archive directory not found: ${archive_dir}" >&2
  exit 2
fi
if [[ ! -d "${backup_root}" ]]; then
  echo "No base backup directory at ${backup_root}; nothing deleted"
  exit 0
fi

# Completed backups are named workchord-<UTC timestamp>, so name order is age
# order. Temporary ".workchord-*" directories are in-progress and ignored.
verified=()
while IFS= read -r candidate; do
  if [[ -f "${candidate}/backup_label" && -f "${candidate}/workchord-files.sha256" ]]; then
    verified+=("${candidate}")
  fi
done < <(find "${backup_root}" -mindepth 1 -maxdepth 1 -type d -name 'workchord-*' | sort -r)

if (( ${#verified[@]} == 0 )); then
  echo "No verified base backup under ${backup_root}; nothing deleted"
  exit 0
fi

index=$(( keep < ${#verified[@]} ? keep - 1 : ${#verified[@]} - 1 ))
anchor=${verified[${index}]}
oldest_needed=$(sed -n 's/^START WAL LOCATION: .* (file \([0-9A-F]\{24\}\))$/\1/p' "${anchor}/backup_label" | head -n 1)
if [[ -z "${oldest_needed}" ]]; then
  echo "Cannot read START WAL LOCATION from ${anchor}/backup_label; nothing deleted" >&2
  exit 3
fi

# Refuse to prune an archive that does not belong to this backup: the segment
# the backup starts from must be there, otherwise recovery is already broken
# and deleting more would hide it.
if [[ ! -e "${archive_dir}/${oldest_needed}" ]]; then
  echo "Segment ${oldest_needed} from $(basename "${anchor}") is missing from ${archive_dir}; nothing deleted" >&2
  exit 3
fi

echo "Keeping WAL from ${oldest_needed} onward (base backup $(basename "${anchor}"), ${#verified[@]} verified)"
candidates=$("${cleanup}" -n "${archive_dir}" "${oldest_needed}")
if [[ "${dry_run}" == "true" ]]; then
  echo "Dry run: files that would be removed:"
  [[ -z "${candidates}" ]] || sed 's/^/  /' <<< "${candidates}"
  exit 0
fi
if ! "${cleanup}" "${archive_dir}" "${oldest_needed}"; then
  echo "pg_archivecleanup failed; the archive may be only partly pruned" >&2
  exit 4
fi
removed=0
while IFS= read -r candidate; do
  if [[ -n "${candidate}" && ! -e "${candidate}" ]]; then removed=$(( removed + 1 )); fi
done <<< "${candidates}"
echo "Removed ${removed} archived file(s)"
