"""Real PostgreSQL loader and fail-closed reconciliation tests."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Event, current_thread
from typing import Any

from cryptography.fernet import Fernet
import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.database_migration import transfer as transfer_module
from app.database_migration.catalog import transfer_order, transfer_tables
from app.database_migration.manifest import write_document
from app.database_migration.source import preflight_source
from app.database_migration.source import MigrationDataError
from app.database_migration.transfer import (
    load_snapshot,
    reconcile_snapshot,
    target_identifier,
)
from app.services.upgrade_service import (
    bootstrap_database_schema,
    database_configuration,
)
from app.models.agent import AgentActor
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.system_settings import SystemSetting
from app.models.task import Task
from app.models.user_session import UserSession


def _source_artifacts(
    tmp_path: Path, configure_database
) -> tuple[Path, Path, str]:
    source = tmp_path / "transfer-source.db"
    configure_database(f"sqlite+aiosqlite:///{source}")
    bootstrap_database_schema()
    encryption_key = Fernet.generate_key()
    engine = create_engine(f"sqlite:///{source}")
    try:
        with Session(engine) as session:
            calendar = Calendar(
                name="Migration 東京",
                year=2026,
                holidays=["2026-01-01"],
                weekend_days=[5, 6],
                short_days=["2026-12-31"],
            )
            iteration = Iteration(
                name="Wave Бета",
                start_date=datetime(2026, 7, 1).date(),
                end_date=datetime(2026, 7, 31).date(),
                calendar=calendar,
            )
            parent = Task(
                title="Parent ✓",
                iteration=iteration,
                tags='["unicode", "東京"]',
            )
            child = Task(
                title="Child",
                iteration=iteration,
                parent=parent,
                description="x" * 8192,
            )
            session.add_all(
                [
                    calendar,
                    iteration,
                    parent,
                    child,
                    AgentActor(
                        name="transfer-agent",
                        display_name="Transfer Agent",
                        api_key_hash="a" * 64,
                        scopes='["tasks:read", "unicode:Бета"]',
                    ),
                    UserSession(
                        public_id="transferpub1",
                        session_token_hash="b" * 64,
                        ip_address="192.0.2.10",
                    ),
                    SystemSetting(
                        key="migration.unicode",
                        category="migration",
                        value_json={"labels": ["Бета", "東京"], "enabled": True},
                        is_secret=False,
                    ),
                    SystemSetting(
                        key="migration.secret",
                        category="migration",
                        secret_ciphertext=Fernet(encryption_key)
                        .encrypt(b"migration-secret")
                        .decode(),
                        is_secret=True,
                    ),
                ]
            )
            session.commit()
    finally:
        engine.dispose()
    fingerprint = "d" * 64
    evidence = tmp_path / "writer-drain.json"
    write_document(
        evidence,
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
                        "revision": "transfer-test",
                        "replica_id": "sqlite-source",
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
    snapshot = tmp_path / "transfer-snapshot.db"
    manifest = tmp_path / "source-manifest.json"
    preflight_source(
        source_path=source,
        snapshot_path=snapshot,
        writer_drain_evidence_path=evidence,
        manifest_path=manifest,
    )
    return snapshot, manifest, encryption_key.decode()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_loader_rejects_concurrent_attempt_for_the_same_target(
    tmp_path: Path,
    postgres_database,
    configure_database,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    snapshot, manifest, _encryption_key = _source_artifacts(
        tmp_path, configure_database
    )
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    configuration = database_configuration()
    authorized_target = target_identifier(configuration)
    manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
    expected_counts = {
        table_name: int(details["row_count"])
        for table_name, details in manifest_payload["tables"].items()
    }
    contender_manifest_payload = dict(manifest_payload)
    contender_manifest_payload.pop("document_sha256")
    contender_manifest_payload["migration_run_id"] = (
        f"{manifest_payload['migration_run_id']}-contender"
    )
    contender_manifest = tmp_path / "source-manifest-contender.json"
    write_document(contender_manifest, contender_manifest_payload)
    contender_report_path = tmp_path / "load-contender.json"

    owner_entered_loader = Event()
    release_owner = Event()
    original_load_table = transfer_module._load_table

    def event_controlled_load_table(
        connection: Connection,
        source: Any,
        table: Any,
        *,
        chunk_size: int,
    ) -> int:
        if current_thread().name.startswith("migration-loader-owner"):
            owner_entered_loader.set()
            if not release_owner.wait(timeout=30):
                raise AssertionError("timed out waiting to release migration loader")
        return original_load_table(
            connection,
            source,
            table,
            chunk_size=chunk_size,
        )

    monkeypatch.setattr(
        transfer_module,
        "_load_table",
        event_controlled_load_table,
    )

    with (
        ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="migration-loader-owner",
        ) as owner_pool,
        ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="migration-loader-contender",
        ) as contender_pool,
    ):
        owner = owner_pool.submit(
            transfer_module.load_snapshot,
            snapshot_path=snapshot,
            source_manifest_path=manifest,
            report_path=tmp_path / "load-owner.json",
            authorized_target=authorized_target,
            chunk_size=7,
        )
        assert owner_entered_loader.wait(timeout=20)

        contender = contender_pool.submit(
            transfer_module.load_snapshot,
            snapshot_path=snapshot,
            source_manifest_path=contender_manifest,
            report_path=contender_report_path,
            authorized_target=authorized_target,
            chunk_size=7,
        )
        try:
            with pytest.raises(MigrationDataError) as contention:
                contender.result(timeout=5)
            assert contention.value.code == "migration_loader_busy"
            assert not owner.done()
            assert not contender_report_path.exists()

            engine = create_engine(postgres_database.url)
            try:
                with engine.connect() as connection:
                    gate_status, failure_code = connection.execute(
                        text(
                            "SELECT status, failure_code "
                            "FROM database_migration_gates"
                        )
                    ).one()
            finally:
                engine.dispose()
            assert gate_status == "loading"
            assert failure_code is None
        finally:
            release_owner.set()

        owner_report = owner.result(timeout=30)

    assert owner_report["status"] == "loaded_closed_to_traffic"
    assert {
        table_name: int(result["row_count"])
        for table_name, result in owner_report["tables"].items()
    } == expected_counts

    engine = create_engine(postgres_database.url)
    try:
        with engine.connect() as connection:
            gate_status, failure_code = connection.execute(
                text(
                    "SELECT status, failure_code "
                    "FROM database_migration_gates"
                )
            ).one()
            target_counts = {
                table_name: int(
                    connection.execute(
                        select(func.count()).select_from(
                            transfer_tables()[table_name]
                        )
                    ).scalar_one()
                )
                for table_name in transfer_order()
            }
    finally:
        engine.dispose()
    assert gate_status == "loaded"
    assert failure_code is None
    assert target_counts == expected_counts

    resumed_report = transfer_module.load_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=manifest,
        report_path=tmp_path / "load-after-unlock.json",
        authorized_target=authorized_target,
        chunk_size=7,
    )
    assert resumed_report["status"] == "loaded_closed_to_traffic"
    assert resumed_report["tables"]
    assert all(result["resumed"] for result in resumed_report["tables"].values())


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_loader_is_idempotent_and_gate_opens_only_after_final_reconciliation(
    tmp_path: Path,
    postgres_database,
    configure_database,
) -> None:
    snapshot, manifest, encryption_key = _source_artifacts(tmp_path, configure_database)
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    configuration = database_configuration()
    authorized_target = target_identifier(configuration)

    with pytest.raises(MigrationDataError) as interruption:
        load_snapshot(
            snapshot_path=snapshot,
            source_manifest_path=manifest,
            report_path=tmp_path / "load-interrupted.json",
            authorized_target=authorized_target,
            chunk_size=7,
            _failure_after_table="agent_actors",
        )
    assert interruption.value.code == "loader_exception"

    load_report = load_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=manifest,
        report_path=tmp_path / "load.json",
        authorized_target=authorized_target,
        chunk_size=7,
    )
    assert load_report["status"] == "loaded_closed_to_traffic"
    assert load_report["analyze_completed"] is True
    assert load_report["tables"]["agent_actors"]["resumed"] is True
    assert load_report["sequences"]
    assert all(
        result["collision_safe"] and result["probe_rolled_back"]
        for result in load_report["sequences"].values()
    )
    assert any(
        result["maximum"] is None for result in load_report["sequences"].values()
    )
    assert any(
        result["maximum"] is not None for result in load_report["sequences"].values()
    )

    engine = create_engine(postgres_database.url)
    try:
        with engine.begin() as connection:
            drifted_id, original_title = connection.execute(
                text("SELECT id, title FROM tasks ORDER BY id LIMIT 1")
            ).one()
            connection.execute(
                text(
                    "UPDATE tasks SET title = 'deliberate-reconciliation-drift' "
                    "WHERE id = :task_id"
                ),
                {"task_id": drifted_id},
            )
        with pytest.raises(MigrationDataError) as drift:
            reconcile_snapshot(
                snapshot_path=snapshot,
                source_manifest_path=manifest,
                report_path=tmp_path / "drift-reconciliation.json",
                authorized_target=authorized_target,
                phase="raw",
                encryption_key=encryption_key,
            )
        assert drift.value.code == "table_reconciliation_mismatch"
        with engine.begin() as connection:
            status = connection.execute(
                text("SELECT status FROM database_migration_gates")
            ).scalar_one()
            assert status == "failed"
            connection.execute(
                text("UPDATE tasks SET title = :title WHERE id = :task_id"),
                {"title": original_title, "task_id": drifted_id},
            )
    finally:
        engine.dispose()

    raw_report_path = tmp_path / "raw-reconciliation.json"
    raw_report = reconcile_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=manifest,
        report_path=raw_report_path,
        authorized_target=authorized_target,
        phase="raw",
        encryption_key=encryption_key,
    )
    assert raw_report["status"] == "passed_target_still_closed"

    repair_report_path = tmp_path / "repairs.json"
    source_manifest = json.loads(manifest.read_text())
    repair_environment = os.environ.copy()
    repair_environment.update(
        DATABASE_URL=postgres_database.url,
        DATABASE_SSL_MODE="disable",
        DATABASE_PROCESS_ROLE="repair",
        DATABASE_POOL_SIZE="1",
        DATABASE_MAX_OVERFLOW="0",
        DEPLOYMENT_ENVIRONMENT="test",
        MAINTENANCE_MODE="off",
        SETTINGS_ENCRYPTION_KEY=encryption_key,
    )
    repair_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "app.cli.database_migration",
            "repairs",
            "--manifest",
            str(manifest),
            "--report",
            str(repair_report_path),
            "--authorize-target",
            authorized_target,
        ],
        cwd=Path(__file__).resolve().parents[2],
        env=repair_environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert repair_result.returncode == 0, repair_result.stderr
    repair_report = json.loads(repair_report_path.read_text(encoding="utf-8"))
    assert repair_report["status"] == "repairs_recorded_target_still_closed"
    assert repair_report["transformations"]
    alternate_raw = dict(raw_report)
    alternate_raw.pop("document_sha256")
    alternate_raw["operator_note"] = "not-the-report-sealed-by-the-gate"
    alternate_raw_path = tmp_path / "alternate-raw-reconciliation.json"
    write_document(alternate_raw_path, alternate_raw)
    with pytest.raises(MigrationDataError) as raw_gate_mismatch:
        reconcile_snapshot(
            snapshot_path=snapshot,
            source_manifest_path=manifest,
            report_path=tmp_path / "invalid-final-reconciliation.json",
            authorized_target=authorized_target,
            phase="final",
            raw_report_path=alternate_raw_path,
            repair_report_path=repair_report_path,
            encryption_key=encryption_key,
        )
    assert raw_gate_mismatch.value.code == "raw_report_gate_mismatch"

    final_report = reconcile_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=manifest,
        report_path=tmp_path / "final-reconciliation.json",
        authorized_target=authorized_target,
        phase="final",
        raw_report_path=raw_report_path,
        repair_report_path=repair_report_path,
        encryption_key=encryption_key,
    )
    assert final_report["status"] == "passed_target_ready"
    assert final_report["zero_unexplained_differences"] is True

    repeated = load_snapshot(
        snapshot_path=snapshot,
        source_manifest_path=manifest,
        report_path=tmp_path / "load-repeated.json",
        authorized_target=authorized_target,
    )
    assert repeated["status"] == "already_reconciled"

    engine = create_engine(postgres_database.url)
    try:
        with engine.connect() as connection:
            gate = connection.execute(
                text(
                    "SELECT status FROM database_migration_gates "
                    "WHERE run_id = :run_id"
                ),
                {"run_id": source_manifest["migration_run_id"]},
            ).scalar_one()
        assert gate == "reconciled"
    finally:
        engine.dispose()
