"""Wave 3 deployment, security, backup, and reset contracts."""

from __future__ import annotations

from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
POSTGRES_IMAGE = (
    "postgres:18.4-bookworm@sha256:"
    "1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296"
)


def _yaml(name: str):
    return yaml.safe_load((REPOSITORY_ROOT / name).read_text(encoding="utf-8"))


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
