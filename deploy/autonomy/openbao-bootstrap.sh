#!/bin/sh
set -eu

: "${OPENBAO_DEV_ROOT_TOKEN:?OPENBAO_DEV_ROOT_TOKEN is required}"
: "${AUTONOMY_SIGNER_KEY:=workchord-server-acceptance}"
: "${AUTONOMY_SIGNER_TOKEN_FILE:=/run/workchord-autonomy/openbao-token}"
: "${AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE:=/run/workchord-autonomy/openbao-signer-public-key.b64}"

export BAO_ADDR="${BAO_ADDR:-http://openbao:8200}"
export BAO_TOKEN="$OPENBAO_DEV_ROOT_TOKEN"

attempt=0
until bao status >/dev/null 2>&1; do
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 60 ]; then
        echo "OpenBao did not become ready" >&2
        exit 1
    fi
    sleep 1
done

bao secrets enable transit >/dev/null 2>&1 || true
if ! bao read "transit/keys/$AUTONOMY_SIGNER_KEY" >/dev/null 2>&1; then
    bao write "transit/keys/$AUTONOMY_SIGNER_KEY" \
        type=ed25519 \
        exportable=false \
        allow_plaintext_backup=false >/dev/null
fi

signer_key_response="$(bao read -format=json "transit/keys/$AUTONOMY_SIGNER_KEY")"
signer_public_key="$(
    printf '%s' "$signer_key_response" \
        | tr -d '\n' \
        | sed -n 's/.*"public_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
)"
if [ -z "$signer_public_key" ]; then
    echo "OpenBao signer public key was not returned" >&2
    exit 1
fi

bao policy write workchord-server-acceptance \
    /opt/workchord/openbao-acceptance-policy.hcl >/dev/null

if [ -s "$AUTONOMY_SIGNER_TOKEN_FILE" ]; then
    previous_token="$(sed -n '1p' "$AUTONOMY_SIGNER_TOKEN_FILE")"
    if [ -n "$previous_token" ]; then
        bao token revoke "$previous_token" >/dev/null 2>&1 || true
    fi
fi

acceptance_token="$(
    bao token create \
        -orphan \
        -no-default-policy \
        -ttl=15m \
        -explicit-max-ttl=30m \
        -policy=workchord-server-acceptance \
        -field=token
)"

umask 077
mkdir -p "$(dirname "$AUTONOMY_SIGNER_TOKEN_FILE")"
printf '%s\n' "$acceptance_token" >"$AUTONOMY_SIGNER_TOKEN_FILE"
printf '%s\n' "$signer_public_key" >"$AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE"
chmod 0444 "$AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE"
if [ -n "${AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_OUTPUT:-}" ]; then
    mkdir -p "$(dirname "$AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_OUTPUT")"
    printf '%s\n' "$signer_public_key" \
        >"$AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_OUTPUT"
    chmod 0444 "$AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_OUTPUT"
fi
