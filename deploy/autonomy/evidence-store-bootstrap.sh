#!/bin/sh
set -eu

: "${EVIDENCE_STORE_ROOT_ACCESS_KEY:?EVIDENCE_STORE_ROOT_ACCESS_KEY is required}"
: "${EVIDENCE_STORE_ROOT_SECRET_KEY:?EVIDENCE_STORE_ROOT_SECRET_KEY is required}"
: "${AUTONOMY_EVIDENCE_ACCESS_KEY:?AUTONOMY_EVIDENCE_ACCESS_KEY is required}"
: "${AUTONOMY_EVIDENCE_BUCKET:=workchord-server-acceptance}"
: "${AUTONOMY_EVIDENCE_RETENTION_DAYS:=1}"
: "${AUTONOMY_EVIDENCE_REGION:=us-east-1}"

endpoint="${AUTONOMY_EVIDENCE_ENDPOINT:-http://evidence-store:7070}"
policy_template=/opt/workchord/evidence-store-acceptance-policy.json

case "$AUTONOMY_EVIDENCE_ACCESS_KEY" in
    ""|*[!A-Za-z0-9]*)
        echo "AUTONOMY_EVIDENCE_ACCESS_KEY must be alphanumeric" >&2
        exit 1
        ;;
esac
case "$AUTONOMY_EVIDENCE_RETENTION_DAYS" in
    ""|0*|*[!0-9]*)
        echo "AUTONOMY_EVIDENCE_RETENTION_DAYS must be a positive whole number of days" >&2
        exit 1
        ;;
esac

export AWS_ACCESS_KEY_ID="$EVIDENCE_STORE_ROOT_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$EVIDENCE_STORE_ROOT_SECRET_KEY"
export AWS_DEFAULT_REGION="$AUTONOMY_EVIDENCE_REGION"
bucket="$AUTONOMY_EVIDENCE_BUCKET"

s3api() {
    aws --endpoint-url "$endpoint" --output text s3api "$@"
}

attempt=0
until s3api list-buckets >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
        echo "The evidence store did not become ready" >&2
        exit 1
    fi
    sleep 1
done

# Object lock can only be enabled when the bucket is created; it also turns
# on versioning, which can never be suspended afterwards.
if ! s3api head-bucket --bucket "$bucket" >/dev/null 2>&1; then
    s3api create-bucket \
        --bucket "$bucket" \
        --object-lock-enabled-for-bucket >/dev/null
fi
s3api put-object-lock-configuration \
    --bucket "$bucket" \
    --object-lock-configuration \
    "{\"ObjectLockEnabled\":\"Enabled\",\"Rule\":{\"DefaultRetention\":{\"Mode\":\"COMPLIANCE\",\"Days\":$AUTONOMY_EVIDENCE_RETENTION_DAYS}}}" \
    >/dev/null

policy_file="$(mktemp)"
trap 'rm -f "$policy_file"' EXIT
sed "s/WORKCHORD_ACCEPTANCE_PRINCIPAL/$AUTONOMY_EVIDENCE_ACCESS_KEY/" \
    "$policy_template" >"$policy_file"
s3api put-bucket-policy --bucket "$bucket" --policy "file://$policy_file" >/dev/null

versioning="$(s3api get-bucket-versioning --bucket "$bucket" --query Status)"
if [ "$versioning" != "Enabled" ]; then
    echo "The evidence bucket is not versioned" >&2
    exit 1
fi
retention="$(
    s3api get-object-lock-configuration \
        --bucket "$bucket" \
        --query '[ObjectLockConfiguration.ObjectLockEnabled, ObjectLockConfiguration.Rule.DefaultRetention.Mode, ObjectLockConfiguration.Rule.DefaultRetention.Days]'
)"
if [ "$(printf '%s' "$retention" | tr -s '[:space:]' ' ')" != "Enabled COMPLIANCE $AUTONOMY_EVIDENCE_RETENTION_DAYS" ]; then
    echo "The evidence bucket lacks its default COMPLIANCE retention" >&2
    exit 1
fi
if aws --endpoint-url "$endpoint" --no-sign-request s3api list-objects-v2 \
    --bucket "$bucket" --max-items 1 >/dev/null 2>&1; then
    echo "The evidence bucket accepts anonymous requests" >&2
    exit 1
fi
