"""Read-only SQLite snapshot and manifest safety tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import sqlite3

import pytest

from app.database_migration.manifest import verify_document, write_document
from app.database_migration.source import MigrationDataError, preflight_source
from app.services.upgrade_service import bootstrap_database_schema, head_revision


def _drain_evidence(path: Path, *, captured_at: datetime | None = None) -> Path:
    fingerprint = "a" * 64
    write_document(
        path,
        {
            "kind": "workchord-writer-drain-evidence",
            "schema_version": 1,
            "captured_at": (captured_at or datetime.now(UTC)).isoformat(),
            "controller": {
                "sqlite_owners_stopped": True,
                "source_connection_count": 0,
            },
            "replicas": [
                {
                    "maintenance": {
                        "mode": "validation-only",
                        "revision": "wave3-test",
                        "replica_id": "backend-test-1",
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
    return path


def _current_source(path: Path, configure_database) -> Path:
    configure_database(f"sqlite+aiosqlite:///{path}")
    bootstrap_database_schema()
    return path


def _seed_task_graph(connection: sqlite3.Connection) -> None:
    connection.execute(
        "INSERT INTO calendars "
        "(id, name, year, holidays, weekend_days, short_days) "
        "VALUES (1, 'Source', 2026, '[]', '[5, 6]', '[]')"
    )
    connection.execute(
        "INSERT INTO iterations "
        "(id, name, start_date, end_date, calendar_id) "
        "VALUES (1, 'Source', '2026-07-01', '2026-07-31', 1)"
    )
    for task_id in (1, 2):
        connection.execute(
            "INSERT INTO tasks "
            "(id, title, priority, effort_days, effort_hours, status, "
            "is_optional, is_deferred, sort_order, iteration_id) "
            "VALUES (?, ?, 5, 1.0, 8.0, 'planned', 0, 0, 0, 1)",
            (task_id, f"Task {task_id}"),
        )
    connection.execute(
        "INSERT INTO agent_actors "
        "(id, name, display_name, api_key_hash, scopes, enabled, created_at, "
        "role, work_policy, max_parallel_work, queue_revision) "
        "VALUES (1, 'source-agent', 'Source Agent', ?, '[]', 1, ?, "
        "'worker', 'assigned_only', 1, 1)",
        ("a" * 64, "2026-07-18 12:00:00"),
    )


@pytest.mark.sqlite
def test_preflight_creates_deterministic_secret_free_manifest(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source.db", configure_database)
    evidence = _drain_evidence(tmp_path / "drain.json")

    first = preflight_source(
        source_path=source,
        snapshot_path=tmp_path / "snapshot-one.db",
        writer_drain_evidence_path=evidence,
        manifest_path=tmp_path / "manifest-one.json",
    )
    second = preflight_source(
        source_path=source,
        snapshot_path=tmp_path / "snapshot-two.db",
        writer_drain_evidence_path=evidence,
        manifest_path=tmp_path / "manifest-two.json",
    )

    assert verify_document(first) == first["document_sha256"]
    assert first == second
    assert first["source_revision"] == head_revision()
    assert first["snapshot"]["read_only_recheck"] is True
    assert len(first["tables"]) == 45
    assert first["repair_policy"]["automatic_source_repairs"] == []
    assert {
        entry["table"]: entry["disposition"] for entry in first["catalog"]
    }["alembic_version"] == "target_owned"
    assert not any(
        entry["table"] == "database_migration_gates"
        and entry["disposition"] != "target_owned"
        for entry in first["catalog"]
    )
    encoded = json.dumps(first)
    assert str(tmp_path) not in encoded
    assert "DATABASE_URL" not in encoded


@pytest.mark.sqlite
def test_preflight_refuses_invalid_boolean_before_target_mutation(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source-invalid.db", configure_database)
    with sqlite3.connect(source) as connection:
        connection.execute(
            """
            INSERT INTO agent_actors (
                name, display_name, api_key_hash, scopes, enabled, role,
                work_policy, max_parallel_work, queue_revision, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "invalid-boolean",
                "Invalid Boolean",
                "a" * 64,
                "[]",
                2,
                "worker",
                "assigned_only",
                1,
                1,
                "2026-07-18 12:00:00",
            ),
        )
    evidence = _drain_evidence(tmp_path / "drain-invalid.json")

    with pytest.raises(MigrationDataError, match="enabled has invalid values") as exc_info:
        preflight_source(
            source_path=source,
            snapshot_path=tmp_path / "snapshot-invalid.db",
            writer_drain_evidence_path=evidence,
            manifest_path=tmp_path / "manifest-invalid.json",
        )

    assert exc_info.value.code == "invalid_boolean"
    assert not (tmp_path / "manifest-invalid.json").exists()


@pytest.mark.sqlite
def test_preflight_refuses_values_that_postgresql_varchar_cannot_store(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source-overflow.db", configure_database)
    with sqlite3.connect(source) as connection:
        connection.execute(
            "INSERT INTO calendars (name, year, holidays, weekend_days, short_days) "
            "VALUES (?, ?, ?, ?, ?)",
            ("x" * 256, 2026, "[]", "[5, 6]", "[]"),
        )
    evidence = _drain_evidence(tmp_path / "drain-overflow.json")

    with pytest.raises(MigrationDataError) as exc_info:
        preflight_source(
            source_path=source,
            snapshot_path=tmp_path / "snapshot-overflow.db",
            writer_drain_evidence_path=evidence,
            manifest_path=tmp_path / "manifest-overflow.json",
        )

    assert exc_info.value.code == "string_length_overflow"
    assert not (tmp_path / "manifest-overflow.json").exists()


@pytest.mark.sqlite
def test_preflight_refuses_corrupt_sqlite_source(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source-corrupt.db", configure_database)
    source.write_bytes(b"not-a-sqlite-database")
    evidence = _drain_evidence(tmp_path / "drain-corrupt.json")

    with pytest.raises(MigrationDataError) as exc_info:
        preflight_source(
            source_path=source,
            snapshot_path=tmp_path / "snapshot-corrupt.db",
            writer_drain_evidence_path=evidence,
            manifest_path=tmp_path / "manifest-corrupt.json",
        )

    assert exc_info.value.code == "sqlite_snapshot_failure"
    assert not (tmp_path / "manifest-corrupt.json").exists()


@pytest.mark.sqlite
def test_preflight_refuses_orphans_and_malformed_text_json(
    tmp_path: Path,
    configure_database,
) -> None:
    orphan = _current_source(tmp_path / "source-orphan.db", configure_database)
    with sqlite3.connect(orphan) as connection:
        connection.execute("PRAGMA foreign_keys=OFF")
        connection.execute(
            "INSERT INTO task_status_logs "
            "(id, task_id, from_status, to_status, changed_at, triggered_by) "
            "VALUES (1, 999, 'planned', 'active', ?, 'user')",
            ("2026-07-18 12:00:00",),
        )
    with pytest.raises(MigrationDataError) as orphan_error:
        preflight_source(
            source_path=orphan,
            snapshot_path=tmp_path / "snapshot-orphan.db",
            writer_drain_evidence_path=_drain_evidence(tmp_path / "drain-orphan.json"),
            manifest_path=tmp_path / "manifest-orphan.json",
        )
    assert orphan_error.value.code == "sqlite_foreign_key_failure"

    malformed = _current_source(tmp_path / "source-malformed.db", configure_database)
    with sqlite3.connect(malformed) as connection:
        connection.execute(
            "INSERT INTO agent_actors "
            "(name, display_name, api_key_hash, scopes, enabled, role, "
            "work_policy, max_parallel_work, queue_revision, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "malformed-json",
                "Malformed JSON",
                "b" * 64,
                "{",
                1,
                "worker",
                "assigned_only",
                1,
                1,
                "2026-07-18 12:00:00",
            ),
        )
    with pytest.raises(MigrationDataError) as malformed_error:
        preflight_source(
            source_path=malformed,
            snapshot_path=tmp_path / "snapshot-malformed.db",
            writer_drain_evidence_path=_drain_evidence(
                tmp_path / "drain-malformed.json"
            ),
            manifest_path=tmp_path / "manifest-malformed.json",
        )
    assert malformed_error.value.code == "invalid_text_json"


@pytest.mark.sqlite
def test_preflight_refuses_stale_revision_and_live_writer_claim(
    tmp_path: Path,
    configure_database,
) -> None:
    stale = _current_source(tmp_path / "source-revision.db", configure_database)
    with sqlite3.connect(stale) as connection:
        connection.execute(
            "UPDATE alembic_version SET version_num = '20260718_0031'"
        )
    with pytest.raises(MigrationDataError) as revision_error:
        preflight_source(
            source_path=stale,
            snapshot_path=tmp_path / "snapshot-revision.db",
            writer_drain_evidence_path=_drain_evidence(
                tmp_path / "drain-revision.json"
            ),
            manifest_path=tmp_path / "manifest-revision.json",
        )
    assert revision_error.value.code == "unsupported_source_revision"

    live = _current_source(tmp_path / "source-live.db", configure_database)
    evidence_path = _drain_evidence(tmp_path / "drain-live.json")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence.pop("document_sha256")
    evidence["controller"]["source_connection_count"] = 1
    evidence_path.unlink()
    write_document(evidence_path, evidence)
    with pytest.raises(MigrationDataError) as writer_error:
        preflight_source(
            source_path=live,
            snapshot_path=tmp_path / "snapshot-live.db",
            writer_drain_evidence_path=evidence_path,
            manifest_path=tmp_path / "manifest-live.json",
        )
    assert writer_error.value.code == "source_may_be_writable"
    assert not (tmp_path / "snapshot-live.db").exists()


@pytest.mark.sqlite
def test_preflight_refuses_partial_unique_duplicates_and_task_cycles(
    tmp_path: Path,
    configure_database,
) -> None:
    duplicate = _current_source(tmp_path / "source-duplicate.db", configure_database)
    with sqlite3.connect(duplicate) as connection:
        _seed_task_graph(connection)
        connection.execute("DROP INDEX uq_agent_task_assignments_live_purpose")
        for assignment_id in (1, 2):
            connection.execute(
                "INSERT INTO agent_task_assignments "
                "(id, task_id, actor_id, purpose, queue_class, state, queue_rank, "
                "task_version, routing_snapshot, created_at, updated_at) "
                "VALUES (?, 1, 1, 'execution', 'normal', 'queued', 1000, "
                "1, '{}', ?, ?)",
                (
                    assignment_id,
                    "2026-07-18 12:00:00",
                    "2026-07-18 12:00:00",
                ),
            )
    with pytest.raises(MigrationDataError) as duplicate_error:
        preflight_source(
            source_path=duplicate,
            snapshot_path=tmp_path / "snapshot-duplicate.db",
            writer_drain_evidence_path=_drain_evidence(
                tmp_path / "drain-duplicate.json"
            ),
            manifest_path=tmp_path / "manifest-duplicate.json",
        )
    assert duplicate_error.value.code == "duplicate_unique_key"

    cyclic = _current_source(tmp_path / "source-cycle.db", configure_database)
    with sqlite3.connect(cyclic) as connection:
        _seed_task_graph(connection)
        connection.execute(
            "INSERT INTO task_dependencies (id, task_id, depends_on_id) "
            "VALUES (1, 1, 2)"
        )
        connection.execute(
            "INSERT INTO task_dependencies (id, task_id, depends_on_id) "
            "VALUES (2, 2, 1)"
        )
    with pytest.raises(MigrationDataError) as cycle_error:
        preflight_source(
            source_path=cyclic,
            snapshot_path=tmp_path / "snapshot-cycle.db",
            writer_drain_evidence_path=_drain_evidence(tmp_path / "drain-cycle.json"),
            manifest_path=tmp_path / "manifest-cycle.json",
        )
    assert cycle_error.value.code == "task_dependency_cycle"


@pytest.mark.sqlite
def test_preflight_refuses_stale_or_unfenced_writer_evidence(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source-stale.db", configure_database)
    evidence = _drain_evidence(
        tmp_path / "drain-stale.json",
        captured_at=datetime.now(UTC) - timedelta(hours=1),
    )

    with pytest.raises(MigrationDataError) as exc_info:
        preflight_source(
            source_path=source,
            snapshot_path=tmp_path / "snapshot-stale.db",
            writer_drain_evidence_path=evidence,
            manifest_path=tmp_path / "manifest-stale.json",
        )

    assert exc_info.value.code == "stale_writer_drain_evidence"
    assert not (tmp_path / "snapshot-stale.db").exists()


@pytest.mark.sqlite
def test_preflight_refuses_target_owned_source_state(
    tmp_path: Path,
    configure_database,
) -> None:
    source = _current_source(tmp_path / "source-gated.db", configure_database)
    with sqlite3.connect(source) as connection:
        connection.execute(
            """
            INSERT INTO database_migration_gates (
                run_id, source_manifest_sha256, source_snapshot_sha256,
                target_identity_sha256, status, completed_tables, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "old-run",
                "a" * 64,
                "b" * 64,
                "c" * 64,
                "reconciled",
                "[]",
                "2026-07-18 12:00:00",
                "2026-07-18 12:00:00",
            ),
        )
    evidence = _drain_evidence(tmp_path / "drain-gated.json")

    with pytest.raises(MigrationDataError) as exc_info:
        preflight_source(
            source_path=source,
            snapshot_path=tmp_path / "snapshot-gated.db",
            writer_drain_evidence_path=evidence,
            manifest_path=tmp_path / "manifest-gated.json",
        )

    assert exc_info.value.code == "target_owned_source_rows"
