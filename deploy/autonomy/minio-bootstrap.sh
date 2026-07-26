#!/bin/sh
set -eu

: "${MINIO_ROOT_USER:?MINIO_ROOT_USER is required}"
: "${MINIO_ROOT_PASSWORD:?MINIO_ROOT_PASSWORD is required}"
: "${AUTONOMY_MINIO_ACCESS_KEY:?AUTONOMY_MINIO_ACCESS_KEY is required}"
: "${AUTONOMY_MINIO_SECRET_KEY:?AUTONOMY_MINIO_SECRET_KEY is required}"
: "${AUTONOMY_MINIO_EVIDENCE_BUCKET:=workchord-server-acceptance}"
: "${AUTONOMY_MINIO_RETENTION:=1d}"

endpoint="${AUTONOMY_MINIO_ENDPOINT:-http://minio:9000}"
alias_name=workchord

attempt=0
until mc alias set \
    "$alias_name" \
    "$endpoint" \
    "$MINIO_ROOT_USER" \
    "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
        echo "MinIO did not become ready" >&2
        exit 1
    fi
    sleep 1
done

mc mb \
    --ignore-existing \
    --with-lock \
    "$alias_name/$AUTONOMY_MINIO_EVIDENCE_BUCKET" >/dev/null
mc retention set \
    --default \
    COMPLIANCE \
    "$AUTONOMY_MINIO_RETENTION" \
    "$alias_name/$AUTONOMY_MINIO_EVIDENCE_BUCKET" >/dev/null
mc anonymous set \
    none \
    "$alias_name/$AUTONOMY_MINIO_EVIDENCE_BUCKET" >/dev/null
mc admin user add \
    "$alias_name" \
    "$AUTONOMY_MINIO_ACCESS_KEY" \
    "$AUTONOMY_MINIO_SECRET_KEY" >/dev/null
mc admin policy create \
    "$alias_name" \
    workchord-server-acceptance \
    /opt/workchord/minio-acceptance-policy.json >/dev/null
mc admin policy attach \
    "$alias_name" \
    workchord-server-acceptance \
    --user "$AUTONOMY_MINIO_ACCESS_KEY" >/dev/null
mc version info "$alias_name/$AUTONOMY_MINIO_EVIDENCE_BUCKET" >/dev/null
mc retention info "$alias_name/$AUTONOMY_MINIO_EVIDENCE_BUCKET" >/dev/null
