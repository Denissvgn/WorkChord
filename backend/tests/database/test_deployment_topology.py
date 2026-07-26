"""Wave 3 deployment, security, backup, and reset contracts."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
POSTGRES_IMAGE = (
    "postgres:18.4-bookworm@sha256:"
    "1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296"
)
OPENBAO_IMAGE = (
    "openbao/openbao:2.6.1@sha256:"
    "5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0"
)
MINIO_IMAGE = (
    "minio/minio:RELEASE.2025-09-07T16-13-09Z@sha256:"
    "14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e"
)
VALKEY_IMAGE = (
    "valkey/valkey:8.1.9-alpine@sha256:"
    "a038175878d66b9d274fbf8be73c0305e93798b83917647f167e18cef3c71eec"
)


def _yaml(name: str):
    return yaml.safe_load((REPOSITORY_ROOT / name).read_text(encoding="utf-8"))


def test_github_actions_run_scripts_have_valid_bash_syntax() -> None:
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("bash is unavailable")

    workflow = _yaml(".github/workflows/ci.yml")
    for job_name, job in workflow["jobs"].items():
        for step_index, step in enumerate(job.get("steps", [])):
            script = step.get("run")
            if not isinstance(script, str):
                continue
            result = subprocess.run(
                [bash, "-n"],
                input=script,
                text=True,
                capture_output=True,
                check=False,
            )
            step_name = step.get("name", f"step[{step_index}]")
            assert result.returncode == 0, (
                f"{job_name}/{step_name} failed bash -n:\n{result.stderr}"
            )


def test_local_compose_makes_postgresql_the_integration_database() -> None:
    compose = _yaml("docker-compose.yml")
    services = compose["services"]

    assert services["postgres"]["image"] == POSTGRES_IMAGE
    assert services["postgres"]["environment"]["PGDATA"] == "/var/lib/postgresql/18/docker"
    assert services["postgres"]["entrypoint"] == [
        "/bin/bash",
        "/opt/workchord/postgresql-entrypoint.sh",
    ]
    assert any(
        "workchord_postgresql_wal_archive:/var/lib/postgresql/wal-archive" in volume
        for volume in services["postgres"]["volumes"]
    )
    command = services["postgres"]["command"]
    for setting in (
        "shared_preload_libraries=pg_stat_statements",
        "pg_stat_statements.track=all",
        "track_io_timing=on",
        "track_wal_io_timing=on",
        "log_lock_waits=on",
    ):
        assert setting in command
    assert services["postgres"]["healthcheck"]["test"] == [
        "CMD-SHELL",
        "pg_isready -U postgres -d workchord",
    ]
    assert services["migration"]["depends_on"]["postgres"]["condition"] == "service_healthy"
    assert services["backend"]["depends_on"]["repair"]["condition"] == "service_completed_successfully"
    for service_name in ("migration", "repair", "backend", "delivery-worker"):
        environment = "\n".join(services[service_name]["environment"])
        assert "postgresql+psycopg" in environment
        assert "DATABASE_POSTGRESQL_REQUIRED=true" in environment
        assert "sqlite" not in environment.lower()
        assert all("/app/data" not in volume for volume in services[service_name].get("volumes", []))
    assert services["logical-backup"]["image"] == POSTGRES_IMAGE
    assert services["base-backup"]["image"] == POSTGRES_IMAGE
    initialization = (
        REPOSITORY_ROOT / "deploy/postgresql/init-development.sql"
    ).read_text(encoding="utf-8")
    assert "CREATE EXTENSION IF NOT EXISTS pg_stat_statements" in initialization


def test_rehearsal_and_production_topologies_have_multiple_bounded_replicas() -> None:
    rehearsal = _yaml("docker-compose.rehearsal.yml")["services"]
    production_text = (REPOSITORY_ROOT / "docker-compose.prod.yml").read_text()
    gateway = (
        REPOSITORY_ROOT / "deploy/nginx.production.conf.template"
    ).read_text()

    assert rehearsal["backend"]["deploy"]["replicas"] == 2
    assert rehearsal["delivery-worker"]["deploy"]["replicas"] == 2
    assert "DATABASE_MIGRATION_URL" in production_text
    assert "DATABASE_RUNTIME_URL" in production_text
    assert "DATABASE_BACKUP_URL" in production_text
    assert "DATABASE_POSTGRESQL_REQUIRED: \"true\"" in production_text
    assert "workchord_data" not in production_text
    assert "replicas: ${WORKCHORD_WEB_REPLICAS:-2}" in production_text
    assert "replicas: ${WORKCHORD_WORKER_REPLICAS:-2}" in production_text
    assert "server backend:8001 resolve" in gateway
    assert "limit_req zone=workchord_api_rate" in gateway
    assert "proxy_next_upstream_tries 2" in gateway


def test_self_hosted_server_acceptance_uses_internal_pinned_analogues() -> None:
    compose = _yaml("docker-compose.server.yml")
    services = compose["services"]

    assert services["openbao"]["image"] == OPENBAO_IMAGE
    assert services["minio"]["image"] == MINIO_IMAGE
    assert services["valkey"]["image"] == VALKEY_IMAGE
    assert compose["networks"]["autonomy"]["internal"] is True
    for service_name in (
        "database-bootstrap",
        "openbao",
        "openbao-bootstrap",
        "minio",
        "minio-bootstrap",
        "valkey",
        "autonomy-acceptance",
    ):
        assert services[service_name]["profiles"] == ["autonomy"]
        assert "ports" not in services[service_name]

    acceptance = services["autonomy-acceptance"]
    assert acceptance["environment"]["DEPLOYMENT_ENVIRONMENT"] == "development"
    assert acceptance["restart"] == "no"
    assert "workchord-server-acceptance" in acceptance["command"]
    assert set(acceptance["networks"]) == {"workchord", "autonomy"}
    assert acceptance["environment"]["AUTONOMY_GATEWAY_URL"] == "http://frontend"
    assert "WORKCHORD_SOURCE_REVISION" not in acceptance["environment"]
    assert (
        acceptance["environment"]["AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE"]
        == "/run/workchord-autonomy/openbao-signer-public-key.b64"
    )
    assert (
        acceptance["environment"]["AUTONOMY_MINIO_ACCESS_KEY"]
        == "${AUTONOMY_MINIO_ACCESS_KEY:?Set AUTONOMY_MINIO_ACCESS_KEY}"
    )
    assert "MINIO_ROOT_PASSWORD" not in acceptance["environment"]
    assert (
        services["minio-bootstrap"]["environment"]["AUTONOMY_MINIO_RETENTION"]
        == "${AUTONOMY_MINIO_RETENTION:-1d}"
    )
    assert services["backend"]["volumes"] == [
        "workchord_server_data:/app/data"
    ]
    assert (
        services["migration"]["environment"]["DATABASE_URL"]
        == "${DATABASE_MIGRATION_URL:?Set DATABASE_MIGRATION_URL}"
    )
    assert (
        services["migration"]["depends_on"]["database-bootstrap"]["condition"]
        == "service_completed_successfully"
    )
    assert (
        services["backend"]["environment"]["DATABASE_URL"]
        == "${DATABASE_RUNTIME_URL:?Set DATABASE_RUNTIME_URL}"
    )
    assert (
        services["backend"]["environment"]["SESSION_COOKIE_SECURE"]
        == "${WORKCHORD_SESSION_COOKIE_SECURE:-true}"
    )
    assert services["backend"]["environment"]["MCP_DNS_REBINDING_PROTECTION"] == "true"
    assert "MCP_ALLOWED_HOSTS" in services["backend"]["environment"]
    assert "MCP_ALLOWED_ORIGINS" in services["backend"]["environment"]
    assert services["backend"]["environment"]["MCP_UNSAFE_ALLOW_PUBLIC_BINDING"] == "false"


def test_public_proxy_keeps_detailed_readiness_and_metrics_internal() -> None:
    local_gateway = (REPOSITORY_ROOT / "frontend/nginx.conf").read_text()
    production_gateway = (
        REPOSITORY_ROOT / "deploy/nginx.production.conf.template"
    ).read_text()

    for gateway in (local_gateway, production_gateway):
        assert "location = /health" in gateway
        assert "location ^~ /health/" not in gateway
        for private_path in ("/health/live", "/health/ready", "/metrics"):
            assert (
                f"location = {private_path} {{\n"
                "        return 404;\n"
                "    }"
            ) in gateway
    assert "$workchord_forwarded_proto" in local_gateway


def test_security_and_recovery_scripts_are_fail_closed() -> None:
    security = (
        REPOSITORY_ROOT / "deploy/postgresql/apply-security.sql"
    ).read_text()
    logical = (
        REPOSITORY_ROOT / "scripts/database_backup/logical_backup.sh"
    ).read_text()
    restore = (
        REPOSITORY_ROOT / "scripts/database_backup/restore_verify.sh"
    ).read_text()
    reset = (
        REPOSITORY_ROOT / "scripts/database_migration/reset_local_postgresql.sh"
    ).read_text()
    server_roles = (
        REPOSITORY_ROOT / "deploy/postgresql/init-server-roles.sh"
    ).read_text()
    server_entrypoint = (
        REPOSITORY_ROOT / "scripts/server/accept_self_hosted.sh"
    ).read_text()
    dockerignore = (REPOSITORY_ROOT / ".dockerignore").read_text().splitlines()
    minio_policy = json.loads(
        (
            REPOSITORY_ROOT / "deploy/autonomy/minio-acceptance-policy.json"
        ).read_text()
    )

    for role in ("owner_role", "migrator_role", "runtime_role", "readonly_role", "backup_role"):
        assert f":{{?{role}}}" in security
    assert "REVOKE CREATE ON SCHEMA public FROM PUBLIC" in security
    assert "GRANT SELECT, INSERT, UPDATE, DELETE" in security
    assert "workchord.database_migration_gates" in security
    assert "REVOKE INSERT, UPDATE, DELETE" in security
    assert "ALTER DEFAULT PRIVILEGES" in security
    assert "REVOKE %I FROM %I" in security
    assert "BACKUP_ENCRYPTION_CONFIRMED" in logical
    assert "pg_restore --list" in logical
    assert "sha256sum" in logical
    assert "workchord_restore_" in restore
    assert "actual_target_identifier" in restore
    assert "realpath -e" in restore
    assert "Restore target is not empty" in restore
    assert "--clean" not in restore
    assert "WORKCHORD_ALLOW_LOCAL_DATABASE_RESET=YES" in reset
    assert '== "production"' in reset
    assert "CREATE ROLE workchord_runtime LOGIN NOINHERIT NOSUPERUSER" in server_roles
    assert (
        "ALTER ROLE workchord_backup LOGIN NOINHERIT NOSUPERUSER "
        "NOCREATEDB NOCREATEROLE REPLICATION NOBYPASSRLS"
    ) in server_roles
    assert "namespace.nspname = 'workchord'" in server_roles
    assert "ALTER %s %I.%I OWNER TO workchord_owner" in server_roles
    assert "ALTER ROUTINE %I.%I(%s) OWNER TO workchord_owner" in server_roles
    assert "GRANT workchord_owner TO workchord_migrator" in server_roles
    assert "GRANT workchord_owner TO workchord_runtime" not in server_roles
    assert ': "${WORKCHORD_HTTP_BIND:=127.0.0.1}"' in server_entrypoint
    assert "WORKCHORD_ALLOW_INSECURE_HTTP" in server_entrypoint
    assert "missing_durable_values" in server_entrypoint
    assert "MCP_ALLOWED_HOSTS" in server_entrypoint
    assert "MCP_ALLOWED_ORIGINS" in server_entrypoint
    assert "previous-" in server_entrypoint
    assert "pending-" in server_entrypoint
    assert "docker volume inspect" in server_entrypoint
    assert ".runtime" in dockerignore
    minio_actions = set(minio_policy["Statement"][0]["Action"])
    assert minio_actions == {
        "s3:PutObject",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetObjectRetention",
        "s3:DeleteObjectVersion",
    }


def test_server_image_identity_is_baked_and_not_runtime_overridable() -> None:
    backend_dockerfile = (REPOSITORY_ROOT / "Dockerfile.backend").read_text()
    frontend_dockerfile = (REPOSITORY_ROOT / "Dockerfile.frontend").read_text()
    backend_main = (REPOSITORY_ROOT / "backend/app/main.py").read_text()
    compose = _yaml("docker-compose.server.yml")["services"]

    assert "python -m app.build_identity" in backend_dockerfile
    assert "ENV WORKCHORD_BUILD_REVISION" not in backend_dockerfile
    assert "build_frontend_image_identity.mjs" in frontend_dockerfile
    assert "load_backend_build_identity" in backend_main
    assert "os.getenv(\"WORKCHORD_BUILD_REVISION\"" not in backend_main
    assert "WORKCHORD_BUILD_REVISION" not in compose["backend"]["environment"]


def test_cutover_runbook_names_authority_timers_and_point_of_no_return() -> None:
    cutover = (
        REPOSITORY_ROOT / "docs/runbooks/sqlite-to-postgresql-cutover.md"
    ).read_text()
    normalized = " ".join(cutover.split())

    for authority in (
        "change commander",
        "database operator",
        "application operator",
        "observer/evidence recorder",
        "product owner",
        "incident commander",
    ):
        assert authority in normalized
    assert "180 min total" in normalized
    assert "Mandatory stop conditions" in cutover
    assert "Rollback before writes reopen" in cutover
    assert "Recovery after writes reopen" in cutover
    assert (
        "first accepted PostgreSQL application write is the point of no return"
        in normalized
    )
    assert "There is no reverse synchronization" in normalized
