"""Unit contracts for deterministic, sealed, fail-closed load tooling."""

from __future__ import annotations

from argparse import Namespace
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
import sys

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.load.collect import _derive
from scripts.load.common import (
    QualificationInputError,
    atomic_write_json,
    authorized_base_url,
    capacity_contract,
    contract_sha256,
    read_json_object,
    sha256_file,
    traffic_profile,
)
from scripts.load.qualify import (
    LIFECYCLE_POLICY,
    REQUIRED_RESULTS,
    RUN_GATES,
    _finalize,
    _fingerprint,
    _verify_report,
)
from scripts.load.resilience import evaluate
from scripts.load.run import (
    OperationBuilder,
    _retry_delay_seconds,
    _select_browser_credentials,
    _update_agent_state,
    _validated_retry_policy,
    _weighted_plan,
)
from scripts.load.seed import (
    _dry_manifest,
    _session_rows,
    _validate_target,
)


def test_load_target_and_seed_safety_fences_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(QualificationInputError, match="differs"):
        authorized_base_url(
            "https://rehearsal.example.test",
            authorize_host="wrong.example.test",
            environment="rehearsal",
            production_authorization=None,
            change_id=None,
        )
    with pytest.raises(QualificationInputError, match="Production load"):
        authorized_base_url(
            "https://workchord.example.test",
            authorize_host="workchord.example.test",
            environment="production",
            production_authorization=None,
            change_id=None,
        )
    monkeypatch.setenv("WORKCHORD_PRODUCTION_LOAD_AUTHORIZATION", "exact-token")
    assert authorized_base_url(
        "https://workchord.example.test/",
        authorize_host="workchord.example.test",
        environment="production",
        production_authorization="exact-token",
        change_id="CHG-42",
    ) == "https://workchord.example.test"

    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "production")
    with pytest.raises(QualificationInputError, match="prohibited"):
        _validate_target(
            "postgresql+psycopg://postgres:secret@localhost/workchord_test_safe",
            "localhost:5432/workchord_test_safe",
        )
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "test")
    with pytest.raises(QualificationInputError, match="isolated"):
        _validate_target(
            "postgresql+psycopg://postgres:secret@localhost/workchord",
            "localhost:5432/workchord",
        )


def test_weight_plan_and_browser_state_selection_are_deterministic() -> None:
    operations = [
        {"id": "one", "weight_percent": 41},
        {"id": "two", "weight_percent": 34},
        {"id": "three", "weight_percent": 25},
    ]
    first = _weighted_plan(operations, 10_000, 42)
    second = _weighted_plan(operations, 10_000, 42)
    assert [item["id"] for item in first] == [item["id"] for item in second]
    assert Counter(item["id"] for item in first) == {
        "one": 4100,
        "two": 3400,
        "three": 2500,
    }

    _, credentials = _session_rows(20260718, 1250)
    selected = _select_browser_credentials(credentials, 250)
    assert Counter(item["state"] for item in selected) == {
        "new": 13,
        "active": 188,
        "nearly_expired": 25,
        "expired": 12,
        "revoked": 12,
    }
    assert [item["id"] for item in selected] == [
        item["id"] for item in _select_browser_credentials(credentials, 250)
    ]

    builder = OperationBuilder(
        {
            "entities": {
                "project_ids": [1, 5],
                "iteration_ids": [1, 20],
                "task_ids": [1, 500],
                "hot_project_id": 1,
                "hot_iteration_id": 1,
                "hot_iteration_tasks": 50,
                "hot_project_linked_tasks": 100,
                "agent_assignment_first_task_id": 101,
            }
        },
        42,
    )
    ordinary_ids = {builder._task(counter) for counter in range(1, 501)}
    assert min(ordinary_ids) == 51
    assert max(ordinary_ids) == 100

    dependency_operation = {
        "id": "rest_dependency_add",
        "operation": "/api/tasks/{task_id}/dependencies",
        "method": "POST",
    }
    dependency_pairs = []
    for _ in range(10):
        _, path, kwargs, _ = builder.rest_request(dependency_operation)
        dependency_pairs.append(
            (int(path.split("/")[3]), int(kwargs["json"]["depends_on_id"]))
        )
    assert all(
        50 < dependency_id < task_id <= 100
        for task_id, dependency_id in dependency_pairs
    )
    assert all(task_id - dependency_id == 3 for task_id, dependency_id in dependency_pairs)


def test_runtime_agent_poll_guidance_matches_capacity_contract() -> None:
    from app.services.agent_work_service import (
        AGENT_BUSY_POLL_SECONDS,
        AGENT_IDLE_POLL_SECONDS,
        AGENT_RETRY_MAX_SECONDS,
    )

    polling = capacity_contract()["traffic"]["agent_poll_intervals_seconds"]
    assert AGENT_BUSY_POLL_SECONDS == polling["busy"]
    assert AGENT_IDLE_POLL_SECONDS == polling["idle"]
    assert AGENT_RETRY_MAX_SECONDS == polling["retry_maximum"]


def test_connection_surge_retry_policy_is_bounded_and_deterministic() -> None:
    profile = traffic_profile(capacity_contract(), "connection_surge_v1")
    policy = _validated_retry_policy(profile)
    assert policy is not None
    assert policy["maximum_attempts"] == 3

    first = _retry_delay_seconds(
        policy,
        seed=20260718,
        logical_index=42,
        retry_index=0,
    )
    second = _retry_delay_seconds(
        policy,
        seed=20260718,
        logical_index=42,
        retry_index=1,
    )
    assert 0.75 <= first <= 1.25
    assert 1.5 <= second <= 2.5
    assert first == _retry_delay_seconds(
        policy,
        seed=20260718,
        logical_index=42,
        retry_index=0,
    )


def test_agent_client_tracks_server_selected_assignment_and_live_fence() -> None:
    class ClientState:
        credential = {"id": 2}
        actor_count = 5
        queue_revision = 1
        assignment_index = 0
        live_work = None
        next_assignment_id = None
        next_task_id = None

        def set_poll_guidance(self, value: str) -> bool:
            return bool(value)

    client = ClientState()
    assert _update_agent_state(
        client,
        "mcp_agent_get_my_work",
        200,
        {
            "queue_revision": 7,
            "state": "start_assigned",
            "next": {
                "assignment": {"id": 202},
                "task": {"id": 130202},
            },
            "next_poll_after": "2026-07-18T00:00:05+00:00",
        },
    )
    assert client.queue_revision == 7
    assert client.next_assignment_id == 202
    assert client.next_task_id == 130202

    _update_agent_state(
        client,
        "mcp_agent_begin",
        200,
        {
            "assignment": {"id": 202},
            "run": {"id": 902},
            "task": {"id": 130202, "version": 3},
            "claim_id": "qualification-claim",
            "claim_generation": 4,
            "queue_revision": 8,
        },
    )
    assert client.live_work == {
        "assignment_id": 202,
        "run_id": 902,
        "claim_id": "qualification-claim",
        "claim_generation": 4,
        "expected_task_version": 3,
        "task_id": 130202,
    }
    assert client.next_assignment_id is None

    _update_agent_state(client, "mcp_agent_submit", 200, {"accepted": True})
    assert client.live_work is None
    assert client.assignment_index == 41


def test_seed_dry_manifest_is_sealed_and_reproducible(tmp_path: Path) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    base = {
        "profile": "small",
        "seed": 20260718,
    }
    first = _dry_manifest(Namespace(**base, manifest=first_path))
    second = _dry_manifest(Namespace(**base, manifest=second_path))
    assert first["document_sha256"] == second["document_sha256"]
    assert first["declared_cardinalities"]["tasks"] == 500
    assert first["production_execution_allowed"] is False
    assert read_json_object(first_path, sealed=True) == first


def _timestamp(offset_seconds: int) -> str:
    return (datetime(2026, 7, 18, tzinfo=UTC) + timedelta(seconds=offset_seconds)).isoformat()


def test_resilience_observations_derive_all_fault_metrics(
    tmp_path: Path,
) -> None:
    observations = {
        "kind": "workchord-postgresql-resilience-observations",
        "schema_version": 1,
        "release_fingerprint": "a" * 64,
        "scenarios": {
            "backend_replica_loss": {
                "fault_at": _timestamp(0),
                "first_success_at": _timestamp(5),
                "eligible_attempts": 1000,
                "unexpected_failures": 1,
            },
            "worker_loss": {
                "fault_at": _timestamp(10),
                "replacement_ready_at": _timestamp(20),
                "queue_drained_at": _timestamp(40),
                "oldest_ready_seconds_max": 20,
                "ready_backlog_max": 100,
            },
            "database_failover": {
                "fault_at": _timestamp(50),
                "unready_at": _timestamp(55),
                "writer_ready_at": _timestamp(100),
                "eligible_attempts": 1000,
                "unexpected_failures": 10,
            },
            "pool_saturation": {
                "checkout_samples_ms": [10.0] * 100,
                "timeouts": 0,
                "database_connections_peak": 80,
                "database_max_connections": 150,
            },
            "slow_query": {
                "ordinary_lock_wait_samples_ms": [20.0] * 100,
                "deadlocks": 0,
                "ranked_query_ids": ["123", "456"],
                "explained_query_ids": ["123"],
            },
            "restore": {
                "failure_at": _timestamp(500),
                "restore_started_at": _timestamp(510),
                "restore_ready_at": _timestamp(700),
                "restored_latest_event_at": _timestamp(480),
                "integrity_failures": 0,
                "backup_artifact_sha256": "b" * 64,
                "restore_report_sha256": "c" * 64,
            },
        },
    }
    sealed = atomic_write_json(tmp_path / "resilience.json", observations)
    result = evaluate(sealed)
    assert result["status"] == "passed"
    assert result["metrics"]["database_failover_seconds"] == 50
    assert result["metrics"]["backup_rpo_seconds"] == 20
    assert all(gate["status"] == "passed" for gate in result["gates"].values())


def _snapshot(
    path: Path,
    *,
    created_at: str,
    size: int,
    wal: int,
    deadlocks: int,
    table_size: int,
) -> dict:
    return atomic_write_json(
        path,
        {
            "kind": "workchord-postgresql-metrics-snapshot",
            "schema_version": 1,
            "snapshot_id": path.stem,
            "created_at": created_at,
            "target": {"host": "db:5432", "database": "qualification", "environment": "rehearsal", "change_id": "CHG-1"},
            "capacity_contract": {"id": "workchord-postgresql-capacity-v1", "sha256": "d" * 64},
            "facts": {"database_size_bytes": size},
            "database": {"deadlocks": deadlocks},
            "wal": {"wal_bytes": wal},
            "tables": [
                {
                    "schemaname": "workchord",
                    "relname": "agent_run_events",
                    "n_live_tup": 1000,
                    "n_dead_tup": 10,
                    "total_bytes": table_size,
                    "last_analyze": created_at,
                    "last_autoanalyze": None,
                }
            ],
            "integrity": {"failures": 0, "checks": [{"name": "orphans", "failures": 0, "passed": True}]},
        },
    )


def test_snapshot_derivation_projects_capacity_only_from_eight_hour_sample(
    tmp_path: Path,
) -> None:
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    _snapshot(before, created_at=_timestamp(0), size=10_000_000, wal=20_000, deadlocks=3, table_size=5_000_000)
    _snapshot(after, created_at=_timestamp(8 * 3600), size=20_000_000, wal=40_000, deadlocks=3, table_size=15_000_000)
    external = tmp_path / "external.json"
    integrity = tmp_path / "integrity.json"
    load_result = tmp_path / "load-result.json"
    atomic_write_json(
        load_result,
        {
            "kind": "workchord-postgresql-load-result",
            "run_id": "qualification-soak-test",
            "created_at": _timestamp((8 * 3600) - 1),
            "traffic": {
                "phase": "soak",
                "actual_duration_seconds": (8 * 3600) - 2,
            },
        },
    )
    assert _derive(
        Namespace(
            before=before,
            after=after,
            load_result=load_result,
            phase="soak",
            evidence=[],
            external_output=external,
            integrity_output=integrity,
        )
    ) == 0
    metrics = read_json_object(external, sealed=True)
    assert metrics["metrics"]["capacity_horizon_months"] >= 12
    assert metrics["metrics"]["deadlocks"] == 0
    assert read_json_object(integrity, sealed=True)["failures"] == 0


def test_final_report_requires_and_verifies_ed25519_signature(tmp_path: Path) -> None:
    release_body = {
        "kind": "workchord-postgresql-frozen-release",
        "schema_version": 1,
        "created_at": _timestamp(0),
        "status": "frozen",
        "commit": "f" * 40,
        "schema_head": "qualification-head",
        "configuration": {
            "name": "qualification.env",
            "sha256": "a" * 64,
        },
        "hardware_evidence_sha256": "b" * 64,
        "seed_manifest_sha256": "c" * 64,
        "images": [
            f"example.test/{name}@sha256:{value * 64}"
            for name, value in (
                ("backend", "1"),
                ("gateway", "2"),
                ("postgres", "3"),
            )
        ],
        "capacity_contract": {
            "id": "workchord-postgresql-capacity-v1",
            "sha256": contract_sha256(),
        },
        "lifecycle_policy_sha256": sha256_file(LIFECYCLE_POLICY),
        "database": {"major": 18},
    }
    release_body["fingerprint"] = _fingerprint(release_body)
    release = atomic_write_json(
        tmp_path / "release.json",
        release_body,
    )
    bundles = []
    for attempt in range(1, 4):
        start = -200_000 + ((attempt - 1) * 40_000)
        result_references = []
        for index, (profile, phase) in enumerate(sorted(REQUIRED_RESULTS), start=1):
            result_references.append(
                {
                    "profile": profile,
                    "phase": phase,
                    "run_id": f"qualification-{attempt}-{profile}-{phase}",
                    "sha256": f"{attempt:02x}{index:02x}" * 16,
                    "created_at": _timestamp(start + 1_000 + index),
                }
            )
        bundles.append(
            atomic_write_json(
                tmp_path / f"run-{attempt}.json",
                {
                    "kind": "workchord-postgresql-qualification-run",
                    "schema_version": 1,
                    "run_id": f"qualification-run-{attempt}",
                    "attempt_number": attempt,
                    "created_at": _timestamp(start + 39_001),
                    "status": "passed",
                    "release_fingerprint": release["fingerprint"],
                    "release_manifest_sha256": release["document_sha256"],
                    "seed_manifest_sha256": release["seed_manifest_sha256"],
                    "capacity_contract_sha256": contract_sha256(),
                    "started_at": _timestamp(start),
                    "completed_at": _timestamp(start + 39_000),
                    "results": result_references,
                    "resilience_sha256": f"{attempt + 16:02x}" * 32,
                    "ci_evidence_sha256": f"{attempt + 32:02x}" * 32,
                    "gates": {name: "passed" for name in sorted(RUN_GATES)},
                },
            )
        )
    key = Ed25519PrivateKey.generate()
    key_path = tmp_path / "qualification-key.pem"
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    key_path.chmod(0o600)
    report_path = tmp_path / "qualification.json"
    assert _finalize(
        Namespace(
            run_bundle=[tmp_path / f"run-{attempt}.json" for attempt in range(1, 4)],
            release_manifest=tmp_path / "release.json",
            report_id="qualification-test",
            signing_key=key_path,
            signer="Test qualification owner",
            output=report_path,
        )
    ) == 0
    report = read_json_object(report_path)
    _verify_report(report)
    assert report["status"] == "qualified"
    assert len(report["consecutive_runs"]) == 3

    with pytest.raises(QualificationInputError, match="will not be overwritten"):
        _finalize(
            Namespace(
                run_bundle=[
                    tmp_path / f"run-{attempt}.json" for attempt in range(1, 4)
                ],
                release_manifest=tmp_path / "release.json",
                report_id="qualification-test",
                signing_key=key_path,
                signer="Test qualification owner",
                output=report_path,
            )
        )

    incomplete = read_json_object(tmp_path / "run-2.json", sealed=True)
    incomplete.pop("document_sha256")
    incomplete["gates"].pop("restore")
    atomic_write_json(tmp_path / "run-incomplete.json", incomplete)
    with pytest.raises(QualificationInputError, match="every exact gate"):
        _finalize(
            Namespace(
                run_bundle=[
                    tmp_path / "run-1.json",
                    tmp_path / "run-incomplete.json",
                    tmp_path / "run-3.json",
                ],
                release_manifest=tmp_path / "release.json",
                report_id="qualification-incomplete",
                signing_key=key_path,
                signer="Test qualification owner",
                output=tmp_path / "qualification-incomplete.json",
            )
        )
