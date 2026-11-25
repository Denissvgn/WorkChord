#!/bin/sh
set -eu

: "${EVIDENCE_STORE_ROOT_ACCESS_KEY:?EVIDENCE_STORE_ROOT_ACCESS_KEY is required}"
: "${EVIDENCE_STORE_ROOT_SECRET_KEY:?EVIDENCE_STORE_ROOT_SECRET_KEY is required}"
: "${AUTONOMY_EVIDENCE_ACCESS_KEY:?AUTONOMY_EVIDENCE_ACCESS_KEY is required}"
: "${AUTONOMY_EVIDENCE_SECRET_KEY:?AUTONOMY_EVIDENCE_SECRET_KEY is required}"

endpoint="${AUTONOMY_EVIDENCE_ENDPOINT:-http://evidence-store:7070}"

case "$AUTONOMY_EVIDENCE_ACCESS_KEY" in
    "$EVIDENCE_STORE_ROOT_ACCESS_KEY")
        echo "The acceptance identity must differ from the store root identity" >&2
        exit 1
        ;;
    *[!A-Za-z0-9]*)
        echo "AUTONOMY_EVIDENCE_ACCESS_KEY must be alphanumeric" >&2
        exit 1
        ;;
esac

# Credentials travel through the environment, never through argv.
export ADMIN_ACCESS_KEY="$EVIDENCE_STORE_ROOT_ACCESS_KEY"
export ADMIN_SECRET_KEY="$EVIDENCE_STORE_ROOT_SECRET_KEY"
export ADMIN_ENDPOINT_URL="$endpoint"

attempt=0
until users="$(versitygw admin list-users 2>/dev/null)"; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
        echo "The evidence store did not become ready" >&2
        exit 1
    fi
    sleep 1
done

# The acceptance identity has the plain user role: it cannot create, list,
# configure, or delete buckets. The bucket policy grants its object actions.
if printf '%s\n' "$users" | awk '{ print $1 }' | grep -qx "$AUTONOMY_EVIDENCE_ACCESS_KEY"; then
    action=update-user
else
    action=create-user
fi
versitygw admin "$action" \
    --access "$AUTONOMY_EVIDENCE_ACCESS_KEY" \
    --secret "$AUTONOMY_EVIDENCE_SECRET_KEY" \
    --role user >/dev/null
versitygw admin list-users \
    | awk -v key="$AUTONOMY_EVIDENCE_ACCESS_KEY" '$1 == key && $2 == "user" { found = 1 } END { exit !found }'
