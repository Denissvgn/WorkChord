#!/usr/bin/env python3
"""Qualify the installed backend wheel across the SQLite/PostgreSQL boundary.

The coordinator intentionally imports no ``app`` modules.  Each phase runs in a
fresh interpreter with its database configuration frozen before the installed
package is imported.  CI invokes this file from the repository checkout while
the phase interpreters run with a temporary working directory, so an editable
source tree cannot accidentally satisfy the wheel boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit, urlunsplit

import psycopg
from psycopg import sql


def _psycopg_url(sqlalchemy_url: str) -> str:
    return sqlalchemy_url.replace("postgresql+psycopg://", "postgresql://", 1)


def _database_url(admin_url: str, database_name: str) -> str:
    parsed = urlsplit(admin_url)
    return urlunsplit(
        (parsed.scheme, parsed.netloc, f"/{database_name}", parsed.query, parsed.fragment)
    )


def _target_identifier(database_url: str) -> str:
    parsed = urlsplit(database_url)
    return f"{parsed.hostname or 'local-socket'}:{parsed.port or 5432}{parsed.path}"


def _phase_environment(*, database_url: str, role: str) -> dict[str, str]:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.update(
        DATABASE_URL=database_url,
        DATABASE_SSL_MODE="disable",
        DATABASE_PROCESS_ROLE=role,
        DATABASE_POOL_SIZE="1",
        DATABASE_MAX_OVERFLOW="0",
        DEPLOYMENT_ENVIRONMENT="test",
        OUTBOUND_DELIVERY_WORKER_ENABLED="false",
    )
    return environment


def _run_phase(
    phase: str,
    *,
    workspace: Path,
    database_url: str,
    role: str,
    target: str | None = None,
    maintenance_mode: str = "off",
) -> None:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--phase",
        phase,
        "--workspace",
        str(workspace),
    ]
    if target is not None:
        command.extend(["--authorize-target", target])
    environment = _phase_environment(database_url=database_url, role=role)
    environment.update(
        MAINTENANCE_MODE=maintenance_mode,
        MAINTENANCE_REVISION=f"installed-wheel-{maintenance_mode}",
        MAINTENANCE_REPLICA_ID="installed-wheel-ci",
    )
    result = subprocess.run(
        command,
        cwd=workspace,
        env=environment,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"Installed-wheel {phase} phase failed ({result.returncode})\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def _create_database(
    admin_url: str,
    database_name: str,
    runtime_role: str,
) -> None:
    with psycopg.connect(_psycopg_url(admin_url), autocommit=True) as connection:
        connection.execute(
            sql.SQL(
                "CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8' "
                "LOCALE_PROVIDER builtin BUILTIN_LOCALE 'PG_UNICODE_FAST'"
            ).format(sql.Identifier(database_name))
        )
        connection.execute(
            sql.SQL("CREATE ROLE {} NOLOGIN").format(sql.Identifier(runtime_role))
        )
        connection.execute(
            sql.SQL("ALTER ROLE {} IN DATABASE {} SET timezone TO 'UTC'").format(
                sql.Identifier(runtime_role),
                sql.Identifier(database_name),
            )
        )
        connection.execute(
            sql.SQL(
                "ALTER ROLE {} IN DATABASE {} SET search_path TO "
                "workchord, pg_catalog"
            ).format(
                sql.Identifier(runtime_role),
                sql.Identifier(database_name),
            )
        )

    database_url = _database_url(admin_url, database_name)
    with psycopg.connect(_psycopg_url(database_url), autocommit=True) as connection:
        migration_role = connection.execute("SELECT current_user").fetchone()[0]
        connection.execute("CREATE SCHEMA workchord")
        connection.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
        connection.execute(
            sql.SQL("GRANT USAGE ON SCHEMA workchord TO {}").format(
                sql.Identifier(runtime_role)
            )
        )
        connection.execute(
            sql.SQL(
                "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA workchord "
                "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {}"
            ).format(
                sql.Identifier(migration_role),
                sql.Identifier(runtime_role),
            )
        )
        connection.execute(
            sql.SQL(
                "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA workchord "
                "GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO {}"
            ).format(
                sql.Identifier(migration_role),
                sql.Identifier(runtime_role),
            )
        )
        connection.execute(
            sql.SQL("ALTER DATABASE {} SET timezone TO 'UTC'").format(
                sql.Identifier(database_name)
            )
        )
        connection.execute(
            sql.SQL(
                "ALTER DATABASE {} SET search_path TO workchord, pg_catalog"
            ).format(sql.Identifier(database_name))
        )


def _drop_database(
    admin_url: str,
    database_name: str,
    runtime_role: str,
) -> None:
    with psycopg.connect(_psycopg_url(admin_url), autocommit=True) as connection:
        connection.execute(
            sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                sql.Identifier(database_name)
            )
        )
        connection.execute(
            sql.SQL("DROP ROLE IF EXISTS {}").format(sql.Identifier(runtime_role))
        )


def _assert_installed_package() -> None:
    import app
    from app.cli.closeout import build_parser as build_closeout_parser
    from app.cli.cutover import build_parser as build_cutover_parser

    package_path = Path(app.__file__).resolve()
    if "site-packages" not in package_path.parts:
        raise RuntimeError(f"app resolved outside the installed wheel: {package_path}")
    cutover_help = build_cutover_parser().format_help()
    for command in (
        "finalize-rehearsal",
        "finalize-rehearsal-series",
        "authorize-production",
        "finalize-production",
        "verify",
    ):
        if command not in cutover_help:
            raise RuntimeError(
                f"Installed wheel is missing cutover evidence command {command}"
            )
    closeout_help = build_closeout_parser().format_help()
    for command in (
        "publish-release",
        "render-release-notes",
        "finalize-closeout",
        "verify",
    ):
        if command not in closeout_help:
            raise RuntimeError(
                f"Installed wheel is missing post-cutover command {command}"
            )


def _source_phase(workspace: Path) -> None:
    _assert_installed_package()

    from datetime import UTC, date, datetime, timedelta

    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from app.database_migration.manifest import write_document
    from app.database_migration.source import preflight_source
    from app.models.agent import AgentActor
    from app.models.calendar import Calendar
    from app.models.iteration import Iteration
    from app.models.project import Project
    from app.models.task import Task
    from app.models.user_session import UserSession
    from app.services.upgrade_service import bootstrap_database_schema

    before, backup, after = bootstrap_database_schema()
    if before.state != "empty" or backup is not None or not after.is_current:
        raise RuntimeError("SQLite schema-only bootstrap did not reach packaged head")

    source_path = workspace / "source.db"
    sync_engine = create_engine(f"sqlite:///{source_path}")
    try:
        with Session(sync_engine) as session:
            calendar = Calendar(
                name="Installed wheel 東京",
                year=2026,
                holidays=["2026-01-01"],
                weekend_days=[5, 6],
                short_days=[],
            )
            project = Project(name="Installed wheel project")
            iteration = Iteration(
                name="Installed wheel iteration",
                start_date=date(2026, 7, 1),
                end_date=date(2026, 7, 31),
                calendar=calendar,
                project=project,
            )
            task = Task(
                title="Installed wheel transfer task ✓",
                description=(
                    "Scope: prove the packaged source-copy boundary.\n"
                    "- Acceptance: preserve Unicode and timestamps.\n"
                    "- Verification: final reconciliation opens the target gate."
                ),
                iteration=iteration,
                project=project,
                tags='["agent", "cap:test", "東京"]',
                start_date=date(2026, 7, 1),
                end_date=date(2026, 7, 2),
            )
            raw_agent_key = "installed-wheel-agent-key"
            raw_session_token = "A" * 43
            session.add_all(
                [
                    task,
                    AgentActor(
                        name="installed-wheel-agent",
                        display_name="Installed Wheel Agent",
                        api_key_hash=hashlib.sha256(
                            raw_agent_key.encode("utf-8")
                        ).hexdigest(),
                        scopes='["tasks:read", "events:write"]',
                    ),
                    UserSession(
                        public_id="wheelproof01",
                        session_token_hash=hashlib.sha256(
                            raw_session_token.encode("utf-8")
                        ).hexdigest(),
                        ip_address="192.0.2.10",
                        expires_at=datetime.now(UTC) + timedelta(days=1),
                    ),
                ]
            )
            session.commit()
    finally:
        sync_engine.dispose()

    fingerprint = "1" * 64
    drain_path = workspace / "writer-drain.json"
    write_document(
        drain_path,
        {
            "kind": "workchord-writer-drain-evidence",
            "schema_version": 1,
            "captured_at": datetime.now(UTC).isoformat(),
            "controller": {
                "sqlite_owners_stopped": True,
                "source_connection_count": 0,
            },
            "replicas": [
                {
                    "maintenance": {
                        "mode": "validation-only",
                        "revision": "installed-wheel-ci",
                        "replica_id": "installed-wheel-source",
                        "configuration_fingerprint": fingerprint,
                    },
                    "writer_drain": {
                        "drained": True,
                        "replica_agreement_required": True,
                        "configuration_fingerprint": fingerprint,
                    },
                }
            ],
        },
    )
    preflight_source(
        source_path=source_path,
        snapshot_path=workspace / "snapshot.db",
        writer_drain_evidence_path=drain_path,
        manifest_path=workspace / "source-manifest.json",
    )


def _target_phase(workspace: Path, authorized_target: str) -> None:
    _assert_installed_package()

    from sqlalchemy import create_engine, text

    from app.database_migration.transfer import (
        load_snapshot,
        reconcile_snapshot,
        record_post_copy_repairs,
        target_identifier,
    )
    from app.services.upgrade_service import (
        bootstrap_database_schema,
        database_configuration,
        head_revision,
    )

    before, backup, after = bootstrap_database_schema()
    if before.state != "empty" or backup is not None or not after.is_current:
        raise RuntimeError("PostgreSQL schema-only bootstrap did not reach packaged head")
    configuration = database_configuration()
    if target_identifier(configuration) != authorized_target:
        raise RuntimeError("Resolved installed-wheel target differs from authorization")

    snapshot = workspace / "snapshot.db"
    source_manifest = workspace / "source-manifest.json"
    load_report = load_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=source_manifest,
        report_path=workspace / "load-report.json",
        authorized_target=authorized_target,
        chunk_size=7,
    )
    raw_report = reconcile_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=source_manifest,
        report_path=workspace / "raw-reconciliation.json",
        authorized_target=authorized_target,
        phase="raw",
    )
    repair_report = record_post_copy_repairs(
        source_manifest_path=source_manifest,
        report_path=workspace / "repair-report.json",
        authorized_target=authorized_target,
    )
    final_report = reconcile_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=source_manifest,
        report_path=workspace / "final-reconciliation.json",
        authorized_target=authorized_target,
        phase="final",
        raw_report_path=workspace / "raw-reconciliation.json",
        repair_report_path=workspace / "repair-report.json",
    )
    if load_report["status"] != "loaded_closed_to_traffic":
        raise RuntimeError("Installed-wheel load did not remain fail-closed")
    if raw_report["status"] != "passed_target_still_closed":
        raise RuntimeError("Installed-wheel raw reconciliation did not stay closed")
    if repair_report["status"] != "repairs_recorded_target_still_closed":
        raise RuntimeError("Installed-wheel repairs did not stay closed")
    if final_report["status"] != "passed_target_ready":
        raise RuntimeError("Installed-wheel final reconciliation did not open target")

    sync_engine = create_engine(
        configuration.sync_url,
        connect_args=dict(configuration.connect_args),
    )
    runtime_role = (workspace / "runtime-role.txt").read_text(
        encoding="utf-8"
    ).strip()
    try:
        with sync_engine.connect() as connection:
            values = connection.execute(
                text(
                    "SELECT (SELECT count(*) FROM tasks), "
                    "(SELECT count(*) FROM user_sessions), "
                    "(SELECT count(*) FROM agent_actors), "
                    "(SELECT status FROM database_migration_gates)"
                )
            ).one()
            if tuple(values) != (1, 1, 1, "reconciled"):
                raise RuntimeError(f"Installed-wheel transfer counts differ: {values}")
            search_path = connection.execute(text("SHOW search_path")).scalar_one()
            if [part.strip() for part in search_path.split(",")] != [
                "workchord",
                "pg_catalog",
            ]:
                raise RuntimeError(
                    f"Installed-wheel target search_path differs: {search_path!r}"
                )

            database_facts = connection.execute(
                text(
                    "SELECT pg_encoding_to_char(encoding), datlocprovider, "
                    "datlocale, datcollversion FROM pg_database "
                    "WHERE datname = current_database()"
                )
            ).one()
            if tuple(database_facts) != (
                "UTF8",
                "b",
                "PG_UNICODE_FAST",
                "1",
            ):
                raise RuntimeError(
                    "Installed-wheel PostgreSQL locale policy differs: "
                    f"{database_facts!r}"
                )
            timezone = connection.execute(text("SHOW timezone")).scalar_one()
            if timezone not in {"UTC", "Etc/UTC"}:
                raise RuntimeError(
                    f"Installed-wheel target timezone differs: {timezone!r}"
                )

            role_settings = dict(
                setting.split("=", 1)
                for (setting,) in connection.execute(
                    text(
                        "SELECT unnest(settings.setconfig) "
                        "FROM pg_db_role_setting AS settings "
                        "JOIN pg_roles AS role ON role.oid = settings.setrole "
                        "JOIN pg_database AS database "
                        "ON database.oid = settings.setdatabase "
                        "WHERE role.rolname = :runtime_role "
                        "AND database.datname = current_database()"
                    ),
                    {"runtime_role": runtime_role},
                )
            )
            normalized_settings = {
                key.lower(): value for key, value in role_settings.items()
            }
            if normalized_settings.get("timezone") not in {"UTC", "Etc/UTC"}:
                raise RuntimeError(
                    "Installed-wheel runtime role timezone policy differs: "
                    f"{normalized_settings!r}"
                )
            if normalized_settings.get("search_path", "").replace(" ", "") != (
                "workchord,pg_catalog"
            ):
                raise RuntimeError(
                    "Installed-wheel runtime role search_path policy differs: "
                    f"{normalized_settings!r}"
                )

            schema_privileges = connection.execute(
                text(
                    "SELECT has_schema_privilege(:runtime_role, 'public', 'CREATE'), "
                    "has_schema_privilege(:runtime_role, 'workchord', 'CREATE')"
                ),
                {"runtime_role": runtime_role},
            ).one()
            if any(schema_privileges):
                raise RuntimeError(
                    "Installed-wheel runtime role can create in an application "
                    "search-path schema"
                )

            default_privileges = connection.execute(
                text(
                    "SELECT defaults.defaclobjtype, expanded.privilege_type "
                    "FROM pg_default_acl AS defaults "
                    "JOIN pg_namespace AS namespace "
                    "ON namespace.oid = defaults.defaclnamespace "
                    "CROSS JOIN LATERAL aclexplode(defaults.defaclacl) AS expanded "
                    "JOIN pg_roles AS grantee ON grantee.oid = expanded.grantee "
                    "WHERE namespace.nspname = 'workchord' "
                    "AND grantee.rolname = :runtime_role "
                    "ORDER BY defaults.defaclobjtype, expanded.privilege_type"
                ),
                {"runtime_role": runtime_role},
            ).all()
            by_type: dict[str, list[str]] = {"r": [], "S": []}
            for object_type, privilege in default_privileges:
                by_type.setdefault(str(object_type), []).append(str(privilege))
            if tuple(by_type["r"]) != ("DELETE", "INSERT", "SELECT", "UPDATE"):
                raise RuntimeError(
                    "Installed-wheel default table privileges differ: "
                    f"{by_type['r']!r}"
                )
            if tuple(by_type["S"]) != ("SELECT", "UPDATE", "USAGE"):
                raise RuntimeError(
                    "Installed-wheel default sequence privileges differ: "
                    f"{by_type['S']!r}"
                )
    finally:
        sync_engine.dispose()

    from alembic.config import Config
    from alembic.script import ScriptDirectory
    from importlib.resources import as_file, files

    migrations = files("app.migrations")
    with as_file(migrations) as migration_path:
        config = Config(str(migration_path / "alembic.ini"))
        config.set_main_option("script_location", str(migration_path))
        heads = ScriptDirectory.from_config(config).get_heads()
    if heads != [head_revision()]:
        raise RuntimeError(f"Installed wheel contains unexpected Alembic heads: {heads}")


def _maintenance_phase(expected_mode: str) -> None:
    _assert_installed_package()

    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        liveness = client.get("/health/live")
        readiness = client.get("/health/ready")
        project_read = client.get("/api/projects")
        project_write = client.post("/api/projects", json={"name": "blocked"})

    if liveness.status_code != 200 or readiness.status_code != 200:
        raise RuntimeError("Installed-wheel maintenance probes are not healthy")
    if project_write.status_code != 503:
        raise RuntimeError("Installed-wheel maintenance mode accepted a REST write")
    if expected_mode == "validation-only" and project_read.status_code != 503:
        raise RuntimeError("Validation-only mode accepted a non-allowlisted read")
    if expected_mode == "read-only-maintenance" and project_read.status_code != 200:
        raise RuntimeError("Read-only maintenance rejected an ordinary safe read")


def _coordinate(admin_url: str) -> None:
    with tempfile.TemporaryDirectory(prefix="workchord-wheel-qa-") as temporary:
        workspace = Path(temporary).resolve()
        database_name = f"workchord_test_{os.urandom(16).hex()}"
        runtime_role = f"workchord_runtime_test_{os.urandom(16).hex()}"
        (workspace / "runtime-role.txt").write_text(
            runtime_role,
            encoding="utf-8",
        )
        target_url = _database_url(admin_url, database_name)
        target = _target_identifier(target_url)
        try:
            _create_database(admin_url, database_name, runtime_role)
            source_url = f"sqlite+aiosqlite:///{workspace / 'source.db'}"
            _run_phase(
                "source",
                workspace=workspace,
                database_url=source_url,
                role="migration",
            )
            _run_phase(
                "target",
                workspace=workspace,
                database_url=target_url,
                role="repair",
                target=target,
            )
            for mode in ("validation-only", "read-only-maintenance"):
                _run_phase(
                    "maintenance",
                    workspace=workspace,
                    database_url=target_url,
                    role="web",
                    target=mode,
                    maintenance_mode=mode,
                )
        finally:
            _drop_database(admin_url, database_name, runtime_role)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin-url")
    parser.add_argument(
        "--phase",
        choices=("source", "target", "maintenance"),
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--workspace", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--authorize-target", help=argparse.SUPPRESS)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.phase is None:
        if not args.admin_url:
            raise SystemExit("--admin-url is required")
        _coordinate(args.admin_url)
        return 0
    if args.workspace is None:
        raise SystemExit("--workspace is required for an internal phase")
    if args.phase == "source":
        _source_phase(args.workspace)
    elif args.phase == "target":
        if not args.authorize_target:
            raise SystemExit("--authorize-target is required for target phase")
        _target_phase(args.workspace, args.authorize_target)
    else:
        if args.authorize_target not in {
            "validation-only",
            "read-only-maintenance",
        }:
            raise SystemExit("maintenance phase requires its expected mode")
        _maintenance_phase(args.authorize_target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
