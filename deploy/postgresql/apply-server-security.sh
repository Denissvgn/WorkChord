#!/bin/sh
set -eu

: "${PGHOST:=postgres}"
: "${PGPORT:=5432}"
: "${PGDATABASE:=workchord}"
: "${PGUSER:=postgres}"
: "${PGPASSWORD:?PGPASSWORD is required}"

exec psql \
    -X \
    -v ON_ERROR_STOP=1 \
    -v owner_role=workchord_owner \
    -v migrator_role=workchord_migrator \
    -v runtime_role=workchord_runtime \
    -v readonly_role=workchord_readonly \
    -v backup_role=workchord_backup \
    -f /opt/workchord/apply-security.sql
