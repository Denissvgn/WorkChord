#!/bin/sh
set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
repository_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"
cd "$repository_root"

for command_name in docker git openssl; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "Required command is unavailable: $command_name" >&2
        exit 1
    fi
done

if ! docker compose version >/dev/null 2>&1; then
    echo "Docker Compose v2 is required" >&2
    exit 1
fi

worktree_status="$(git status --porcelain --untracked-files=normal)"
if [ -n "$worktree_status" ]; then
    echo "Refusing to build an acceptance receipt from a dirty checkout:" >&2
    printf '%s\n' "$worktree_status" >&2
    exit 1
fi

runtime_dir="$repository_root/.runtime/autonomy"
report_dir="$runtime_dir/reports"
env_file="$runtime_dir/server.env"
mkdir -p "$report_dir"
chmod 700 "$repository_root/.runtime" "$runtime_dir" "$report_dir"

if [ -f "$report_dir/latest.json" ]; then
    previous_stem="$report_dir/previous-$(date -u +%Y%m%dT%H%M%SZ)-$$"
    previous_receipt="$previous_stem.json"
    mv "$report_dir/latest.json" "$previous_receipt"
    if [ -f "$report_dir/trusted-signer-public-key.b64" ]; then
        mv "$report_dir/trusted-signer-public-key.b64" \
            "$previous_stem.trusted-signer-public-key.b64"
    fi
    echo "Archived the previous receipt at $previous_receipt"
fi

server_database_volume_exists=false
if docker volume inspect \
    workchord-server_workchord_postgresql18_data >/dev/null 2>&1; then
    server_database_volume_exists=true
fi

if [ "$server_database_volume_exists" = "true" ] && [ ! -f "$env_file" ]; then
    echo "Refusing to generate new credentials for an existing server database." >&2
    echo "Restore .runtime/autonomy/server.env from backup and rerun." >&2
    echo "If the server data is intentionally disposable, remove the stack and" >&2
    echo "volumes with the documented Docker Compose teardown before rerunning." >&2
    exit 1
fi

if [ "$server_database_volume_exists" = "true" ]; then
    missing_durable_values=""
    for durable_name in \
        POSTGRES_PASSWORD \
        WORKCHORD_MIGRATOR_PASSWORD \
        WORKCHORD_RUNTIME_PASSWORD \
        WORKCHORD_BACKUP_PASSWORD \
        MINIO_ROOT_USER \
        MINIO_ROOT_PASSWORD \
        AUTONOMY_MINIO_ACCESS_KEY \
        AUTONOMY_MINIO_SECRET_KEY \
        OPENBAO_DEV_ROOT_TOKEN \
        SETTINGS_ENCRYPTION_KEY \
        AGENT_BOOTSTRAP_API_KEY \
        WORKCHORD_ADMIN_API_KEY
    do
        durable_value="$(
            sed -n "s/^${durable_name}=//p" "$env_file"
        )"
        if [ -z "$durable_value" ]; then
            missing_durable_values="$missing_durable_values $durable_name"
        fi
    done
    if [ -n "$missing_durable_values" ]; then
        echo "Refusing to rotate missing durable server values:$missing_durable_values" >&2
        echo "Restore the complete server.env or perform an explicit reviewed rotation." >&2
        exit 1
    fi
fi

if [ -f "$env_file" ]; then
    # The file is generated below with shell-safe alphanumeric/base64 values.
    # shellcheck disable=SC1090
    . "$env_file"
fi

random_hex() {
    openssl rand -hex "$1"
}

: "${POSTGRES_PASSWORD:=$(random_hex 24)}"
: "${WORKCHORD_MIGRATOR_PASSWORD:=$(random_hex 24)}"
: "${WORKCHORD_RUNTIME_PASSWORD:=$(random_hex 24)}"
: "${WORKCHORD_BACKUP_PASSWORD:=$(random_hex 24)}"
: "${MINIO_ROOT_USER:=wc$(random_hex 8)}"
: "${MINIO_ROOT_PASSWORD:=$(random_hex 24)}"
: "${AUTONOMY_MINIO_ACCESS_KEY:=wcaccept$(random_hex 8)}"
: "${AUTONOMY_MINIO_SECRET_KEY:=$(random_hex 24)}"
: "${OPENBAO_DEV_ROOT_TOKEN:=$(random_hex 24)}"
: "${SETTINGS_ENCRYPTION_KEY:=$(openssl rand -base64 32 | tr '/+' '_-')}"
: "${AGENT_BOOTSTRAP_API_KEY:=wcboot_$(random_hex 24)}"
: "${WORKCHORD_ADMIN_API_KEY:=wcadmin_$(random_hex 24)}"
: "${WORKCHORD_HTTP_BIND:=127.0.0.1}"
: "${WORKCHORD_HTTP_PORT:=8080}"
: "${POSTGRES_HOST_PORT:=55432}"
: "${WORKCHORD_ALLOW_INSECURE_HTTP:=false}"
: "${WORKCHORD_SESSION_COOKIE_SECURE:=true}"
default_mcp_allowed_hosts='["localhost:*","127.0.0.1:*","[::1]:*"]'
default_mcp_allowed_origins='["http://localhost:*","http://127.0.0.1:*"]'
: "${MCP_ALLOWED_HOSTS:=$default_mcp_allowed_hosts}"
: "${MCP_ALLOWED_ORIGINS:=$default_mcp_allowed_origins}"

if [ "$WORKCHORD_HTTP_BIND" != "127.0.0.1" ] \
    && [ "$WORKCHORD_ALLOW_INSECURE_HTTP" != "true" ]; then
    echo "Refusing a non-loopback plaintext bind. Terminate TLS at a reverse proxy" >&2
    echo "or set WORKCHORD_ALLOW_INSECURE_HTTP=true for an explicitly trusted network." >&2
    exit 1
fi
if [ "$WORKCHORD_HTTP_BIND" != "127.0.0.1" ] \
    && { [ "$MCP_ALLOWED_HOSTS" = "$default_mcp_allowed_hosts" ] \
        || [ "$MCP_ALLOWED_ORIGINS" = "$default_mcp_allowed_origins" ]; }
then
    echo "Refusing a non-loopback bind with loopback-only MCP allowlists." >&2
    echo "Set exact MCP_ALLOWED_HOSTS and HTTPS MCP_ALLOWED_ORIGINS values." >&2
    exit 1
fi

WORKCHORD_SOURCE_REVISION="$(git rev-parse HEAD)"
WORKCHORD_ACCEPTANCE_REPORT_DIR="$report_dir"
DATABASE_MIGRATION_URL="postgresql+psycopg://workchord_migrator:${WORKCHORD_MIGRATOR_PASSWORD}@postgres:5432/workchord"
DATABASE_RUNTIME_URL="postgresql+psycopg://workchord_runtime:${WORKCHORD_RUNTIME_PASSWORD}@postgres:5432/workchord"
POSTGRES_DATABASE_URL="$DATABASE_RUNTIME_URL"
POSTGRES_BACKUP_URL="postgresql://workchord_backup:${WORKCHORD_BACKUP_PASSWORD}@postgres:5432/workchord"

umask 077
temporary_env="$env_file.tmp"
{
    printf 'WORKCHORD_SOURCE_REVISION=%s\n' "$WORKCHORD_SOURCE_REVISION"
    printf 'WORKCHORD_ACCEPTANCE_REPORT_DIR=%s\n' "$WORKCHORD_ACCEPTANCE_REPORT_DIR"
    printf 'WORKCHORD_HTTP_BIND=%s\n' "$WORKCHORD_HTTP_BIND"
    printf 'WORKCHORD_HTTP_PORT=%s\n' "$WORKCHORD_HTTP_PORT"
    printf 'POSTGRES_HOST_PORT=%s\n' "$POSTGRES_HOST_PORT"
    printf 'POSTGRES_PASSWORD=%s\n' "$POSTGRES_PASSWORD"
    printf 'WORKCHORD_MIGRATOR_PASSWORD=%s\n' "$WORKCHORD_MIGRATOR_PASSWORD"
    printf 'WORKCHORD_RUNTIME_PASSWORD=%s\n' "$WORKCHORD_RUNTIME_PASSWORD"
    printf 'WORKCHORD_BACKUP_PASSWORD=%s\n' "$WORKCHORD_BACKUP_PASSWORD"
    printf 'DATABASE_MIGRATION_URL=%s\n' "$DATABASE_MIGRATION_URL"
    printf 'DATABASE_RUNTIME_URL=%s\n' "$DATABASE_RUNTIME_URL"
    printf 'POSTGRES_DATABASE_URL=%s\n' "$POSTGRES_DATABASE_URL"
    printf 'POSTGRES_BACKUP_URL=%s\n' "$POSTGRES_BACKUP_URL"
    printf 'MINIO_ROOT_USER=%s\n' "$MINIO_ROOT_USER"
    printf 'MINIO_ROOT_PASSWORD=%s\n' "$MINIO_ROOT_PASSWORD"
    printf 'AUTONOMY_MINIO_ACCESS_KEY=%s\n' "$AUTONOMY_MINIO_ACCESS_KEY"
    printf 'AUTONOMY_MINIO_SECRET_KEY=%s\n' "$AUTONOMY_MINIO_SECRET_KEY"
    printf 'OPENBAO_DEV_ROOT_TOKEN=%s\n' "$OPENBAO_DEV_ROOT_TOKEN"
    printf 'SETTINGS_ENCRYPTION_KEY=%s\n' "$SETTINGS_ENCRYPTION_KEY"
    printf 'AGENT_BOOTSTRAP_API_KEY=%s\n' "$AGENT_BOOTSTRAP_API_KEY"
    printf 'WORKCHORD_ADMIN_API_KEY=%s\n' "$WORKCHORD_ADMIN_API_KEY"
    printf 'WORKCHORD_ALLOW_INSECURE_HTTP=%s\n' "$WORKCHORD_ALLOW_INSECURE_HTTP"
    printf 'WORKCHORD_SESSION_COOKIE_SECURE=%s\n' "$WORKCHORD_SESSION_COOKIE_SECURE"
    printf "MCP_ALLOWED_HOSTS='%s'\n" "$MCP_ALLOWED_HOSTS"
    printf "MCP_ALLOWED_ORIGINS='%s'\n" "$MCP_ALLOWED_ORIGINS"
} >"$temporary_env"
mv "$temporary_env" "$env_file"
chmod 600 "$env_file"

compose() {
    docker compose \
        --project-name workchord-server \
        --env-file "$env_file" \
        -f docker-compose.yml \
        -f docker-compose.server.yml \
        --profile autonomy \
        "$@"
}

compose config --quiet
compose pull openbao minio minio-bootstrap valkey
compose build backend frontend
compose up --detach --wait --wait-timeout 180 postgres openbao minio valkey
compose stop frontend delivery-worker backend
compose run --rm --no-deps database-bootstrap
compose run --rm --no-deps migration
compose run --rm --no-deps database-security
compose run --rm --no-deps repair
compose run --rm --no-deps openbao-bootstrap
compose run --rm --no-deps minio-bootstrap
compose up --detach --wait --wait-timeout 240 --no-deps \
    backend delivery-worker frontend
pending_name="pending-${WORKCHORD_SOURCE_REVISION}-$$.json"
pending_container_path="/var/lib/workchord/acceptance/$pending_name"
pending_host_path="$report_dir/$pending_name"
compose run --rm --no-deps autonomy-acceptance \
    workchord-server-acceptance \
    --output "$pending_container_path"
compose run --rm --no-deps autonomy-acceptance \
    workchord-server-acceptance \
    --verify-receipt "$pending_container_path"
mv "$pending_host_path" "$report_dir/latest.json"

echo "WorkChord is running at http://${WORKCHORD_HTTP_BIND}:${WORKCHORD_HTTP_PORT}"
echo "Acceptance receipt: $report_dir/latest.json"
echo "Trusted signer public key: $report_dir/trusted-signer-public-key.b64"
