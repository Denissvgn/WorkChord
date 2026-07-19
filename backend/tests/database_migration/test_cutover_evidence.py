"""Fail-closed contracts for rehearsal and production cutover evidence."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import tomllib

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jsonschema import Draft202012Validator, FormatChecker

from app.database_migration.cutover import (
    CAPACITY_CLAIM,
    DOCUMENTATION_CHECKS,
    GATE_IDS,
    GATE_OWNER_ROLES,
    QUALIFICATION_ATTESTATION,
    QUALIFICATION_GATES,
    CutoverEvidenceError,
    _sign_document,
    attest_documentation,
    authorize_production,
    finalize_production,
    finalize_rehearsal,
    finalize_rehearsal_series,
    seal_execution,
    verify_report,
)
from app.database_migration.manifest import (
    canonical_json_bytes,
    read_document,
    sha256_bytes,
    write_document,
)


def _key_pair(directory: Path, name: str) -> tuple[Path, Path]:
    key = Ed25519PrivateKey.generate()
    private_path = directory / f"{name}-private.pem"
    public_path = directory / f"{name}-public.pem"
    private_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    private_path.chmod(0o600)
    public_path.write_bytes(
        key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    return private_path, public_path


def test_zero_human_mode_rejects_file_signing_and_file_trust(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    private_key, public_key = _key_pair(tmp_path, "zero-human")
    monkeypatch.setenv("WORKCHORD_EXECUTION_MODE", "zero-human-agent-v1")

    with pytest.raises(CutoverEvidenceError, match="File private keys"):
        _sign_document(
            tmp_path / "forbidden.json",
            {"kind": "test"},
            signing_key=private_key,
            signer="test-signer",
        )

    with pytest.raises(CutoverEvidenceError, match="file/embedded trust keys"):
        from app.database_migration.cutover import verify_signed_document

        verify_signed_document({}, trusted_public_key=public_key)


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat()


def _release(tmp_path: Path) -> dict:
    body = {
        "kind": "workchord-postgresql-frozen-release",
        "schema_version": 1,
        "created_at": _timestamp(datetime.now(UTC) - timedelta(days=2)),
        "status": "frozen",
        "commit": "f" * 40,
        "images": [
            f"registry.example.test/{name}@sha256:{value * 64}"
            for name, value in (
                ("backend", "1"),
                ("frontend", "2"),
                ("gateway", "3"),
            )
        ],
        "schema_head": "20260719_0033",
        "configuration": {"name": "release.env", "sha256": "4" * 64},
        "hardware_evidence_sha256": "5" * 64,
        "seed_manifest_sha256": "6" * 64,
        "capacity_contract": {
            "id": "workchord-postgresql-capacity-v1",
            "sha256": "7" * 64,
        },
        "lifecycle_policy_sha256": "8" * 64,
        "database": {"major": 18},
    }
    body["fingerprint"] = sha256_bytes(canonical_json_bytes(body))
    return write_document(tmp_path / "release.json", body)


def _release_reference(release: dict) -> dict:
    return {
        "fingerprint": release["fingerprint"],
        "manifest_sha256": release["document_sha256"],
        "commit": release["commit"],
        "images": sorted(release["images"]),
    }


def _qualification(
    tmp_path: Path,
    release: dict,
    private_key: Path,
) -> dict:
    now = datetime.now(UTC) - timedelta(days=1)
    payload = {
        "kind": "workchord-postgresql-precutover-qualification",
        "schema_version": 1,
        "report_id": "qualification-wave-5-test",
        "created_at": _timestamp(now),
        "status": "qualified",
        "capacity_contract": dict(release["capacity_contract"]),
        "capacity_claim": dict(CAPACITY_CLAIM),
        "frozen_release": {
            "fingerprint": release["fingerprint"],
            "manifest_sha256": release["document_sha256"],
            "commit": release["commit"],
            "images": list(release["images"]),
        },
        "consecutive_runs": [
            {
                "run_id": f"qualification-attempt-{attempt}",
                "attempt_number": attempt,
                "bundle_sha256": str(attempt) * 64,
                "started_at": _timestamp(now - timedelta(hours=6 - attempt)),
                "completed_at": _timestamp(
                    now - timedelta(hours=6 - attempt) + timedelta(minutes=30)
                ),
            }
            for attempt in range(1, 4)
        ],
        "qualification_gates": {
            name: {"status": "passed", "evidence": "test"}
            for name in sorted(QUALIFICATION_GATES)
        },
        "attestation": QUALIFICATION_ATTESTATION,
    }
    return _sign_document(
        tmp_path / "qualification.json",
        payload,
        signing_key=private_key,
        signer="Independent qualification owner",
    )


def _documentation(
    tmp_path: Path,
    release: dict,
    private_key: Path,
) -> dict:
    raw_path = tmp_path / "documentation-raw.json"
    raw_path.write_text(
        json.dumps(
            {
                "kind": "workchord-postgresql-documentation-walkthrough",
                "schema_version": 1,
                "walkthrough_id": "documentation-walkthrough-test",
                "completed_at": _timestamp(datetime.now(UTC) - timedelta(hours=8)),
                "status": "passed",
                "release": _release_reference(release),
                "reviewer": {
                    "identity": "Independent documentation reviewer",
                    "independent": True,
                },
                "checks": {name: "passed" for name in sorted(DOCUMENTATION_CHECKS)},
                "unresolved_steps": [],
                "evidence_sha256": ["9" * 64],
            }
        ),
        encoding="utf-8",
    )
    return attest_documentation(
        input_path=raw_path,
        release_manifest_path=tmp_path / "release.json",
        signing_key=private_key,
        signer="Independent documentation reviewer",
        output_path=tmp_path / "documentation.json",
    )


def _source(seed: str) -> dict:
    return {
        "deployment_id": "workchord-primary",
        "sqlite_identifier": "/srv/workchord/workchord.db",
        "revision": "20260719_0033",
        "snapshot_sha256": seed * 64,
        "manifest_sha256": chr(ord(seed) + 1) * 64,
    }


def _target() -> dict:
    return {
        "identifier": "postgres.internal:5432/workchord",
        "identity_sha256": "b" * 64,
        "managed_resource_id": "postgres-cluster-primary",
        "revision": "20260719_0033",
    }


def _operators() -> dict:
    return {
        "change_commander": "commander-1",
        "product_owner": "product-owner-1",
        "database_operator": "database-operator-1",
        "application_operator": "application-operator-1",
        "observer": "observer-1",
        "incident_commander": "incident-commander-1",
    }


def _execution(
    *,
    release: dict,
    qualification: dict,
    documentation: dict,
    base: datetime,
    mode: str,
    sequence: int,
    source_seed: str,
    environment: str = "rehearsal",
    authorization_sha256: str | None = None,
) -> dict:
    operators = _operators()
    gate_times: dict[str, tuple[datetime, datetime]] = {}
    for index, gate_id in enumerate(GATE_IDS):
        started = base + timedelta(minutes=index)
        gate_times[gate_id] = (started, started + timedelta(minutes=1))

    if mode == "abort_drill":
        abort_index = 6
        gates = {}
        for index, gate_id in enumerate(GATE_IDS):
            if index < abort_index:
                status = "passed"
            elif index == abort_index:
                status = "abort"
            else:
                status = "not_started"
            if status == "not_started":
                gates[gate_id] = {
                    "status": status,
                    "started_at": None,
                    "completed_at": None,
                    "evidence_sha256": None,
                    "signed_by": None,
                }
            else:
                gates[gate_id] = {
                    "status": status,
                    "started_at": _timestamp(gate_times[gate_id][0]),
                    "completed_at": _timestamp(gate_times[gate_id][1]),
                    "evidence_sha256": f"{index + 16:02x}" * 32,
                    "signed_by": operators[GATE_OWNER_ROLES[gate_id]],
                }
        completed_at = gate_times["C07"][1] + timedelta(minutes=10)
        decision_at = gate_times["C07"][1]
        point = {
            "postgresql_write_accepted": False,
            "accepted_at": None,
            "correlation_id": None,
            "writer_identity": None,
            "observer": None,
            "change_commander": None,
        }
        outcome = {
            "status": "aborted_as_planned",
            "downtime_seconds": (
                completed_at - gate_times["C02"][0]
            ).total_seconds(),
            "restore_rto_seconds": 600,
            "rollback_seconds": 600,
            "unexplained_reconciliation_differences": 0,
            "critical_smoke_passed": True,
            "steady_smoke_passed": False,
            "burst_smoke_passed": False,
            "rollback_demonstrated": True,
            "sqlite_state": "sole_writable",
            "postgresql_state": "closed",
            "writes_reopened_after_signoff": True,
            "stabilization_started_at": None,
            "manual_steps": [],
            "deviations": [],
            "final_evidence_index_sha256": "c" * 64,
        }
    else:
        gates = {
            gate_id: {
                "status": "passed",
                "started_at": _timestamp(gate_times[gate_id][0]),
                "completed_at": _timestamp(gate_times[gate_id][1]),
                "evidence_sha256": f"{index + 16:02x}" * 32,
                "signed_by": operators[GATE_OWNER_ROLES[gate_id]],
            }
            for index, gate_id in enumerate(GATE_IDS)
        }
        c13_started, c13_completed = gate_times["C13"]
        point_at = c13_started + timedelta(seconds=15)
        completed_at = c13_completed + timedelta(minutes=1)
        decision_at = c13_started
        point = {
            "postgresql_write_accepted": True,
            "accepted_at": _timestamp(point_at),
            "correlation_id": f"first-write-{environment}-{sequence}",
            "writer_identity": "postgresql-runtime-writer",
            "observer": operators["observer"],
            "change_commander": operators["change_commander"],
        }
        outcome = {
            "status": "cutover_complete" if environment == "production" else "passed",
            "downtime_seconds": (
                c13_completed - gate_times["C02"][0]
            ).total_seconds(),
            "restore_rto_seconds": 1200,
            "rollback_seconds": None,
            "unexplained_reconciliation_differences": 0,
            "critical_smoke_passed": True,
            "steady_smoke_passed": True,
            "burst_smoke_passed": True,
            "rollback_demonstrated": False,
            "sqlite_state": "frozen_read_only",
            "postgresql_state": "sole_writable",
            "writes_reopened_after_signoff": True,
            "stabilization_started_at": _timestamp(point_at + timedelta(seconds=10)),
            "manual_steps": [],
            "deviations": [],
            "final_evidence_index_sha256": "d" * 64,
        }
    return {
        "kind": "workchord-postgresql-cutover-execution",
        "schema_version": 1,
        "execution_id": f"execution-{environment}-{mode}-{sequence}",
        "change_id": "CHG-PG-2026-001",
        "environment": environment,
        "mode": mode,
        "sequence_number": sequence,
        "started_at": _timestamp(base),
        "completed_at": _timestamp(completed_at),
        "release": _release_reference(release),
        "dependencies": {
            "qualification_report_sha256": qualification["document_sha256"],
            "documentation_walkthrough_sha256": documentation["document_sha256"],
            "authorization_sha256": authorization_sha256,
        },
        "source": _source(source_seed),
        "target": _target(),
        "operators": operators,
        "gates": gates,
        "decision": {
            "value": "ABORT" if mode == "abort_drill" else "GO",
            "decided_at": _timestamp(decision_at),
            "change_commander": operators["change_commander"],
            "database_operator": operators["database_operator"],
            "application_operator": operators["application_operator"],
            "stop_conditions_read": True,
            "evidence_sha256": "e" * 64,
        },
        "point_of_no_return": point,
        "outcome": outcome,
    }


def _write_raw(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def _trusted_inputs(tmp_path: Path) -> dict:
    qualification_private, qualification_public = _key_pair(tmp_path, "qualification")
    documentation_private, documentation_public = _key_pair(tmp_path, "documentation")
    rehearsal_private, rehearsal_public = _key_pair(tmp_path, "rehearsal")
    authorization_private, authorization_public = _key_pair(tmp_path, "authorization")
    production_private, production_public = _key_pair(tmp_path, "production")
    release = _release(tmp_path)
    qualification = _qualification(tmp_path, release, qualification_private)
    documentation = _documentation(tmp_path, release, documentation_private)
    return {
        "release": release,
        "qualification": qualification,
        "documentation": documentation,
        "qualification_public": qualification_public,
        "documentation_public": documentation_public,
        "rehearsal_private": rehearsal_private,
        "rehearsal_public": rehearsal_public,
        "authorization_private": authorization_private,
        "authorization_public": authorization_public,
        "production_private": production_private,
        "production_public": production_public,
    }


def _finalize_one_rehearsal(
    tmp_path: Path,
    trusted: dict,
    execution: dict,
    name: str,
) -> dict:
    raw = tmp_path / f"{name}-raw.json"
    sealed = tmp_path / f"{name}-execution.json"
    report = tmp_path / f"{name}-report.json"
    _write_raw(raw, execution)
    seal_execution(input_path=raw, output_path=sealed)
    return finalize_rehearsal(
        execution_path=sealed,
        release_manifest_path=tmp_path / "release.json",
        qualification_report_path=tmp_path / "qualification.json",
        qualification_public_key=trusted["qualification_public"],
        documentation_walkthrough_path=tmp_path / "documentation.json",
        documentation_public_key=trusted["documentation_public"],
        signing_key=trusted["rehearsal_private"],
        signer="Migration rehearsal owner",
        output_path=report,
    )


def test_abort_two_rehearsals_and_production_cutover_are_cryptographically_bound(
    tmp_path: Path,
) -> None:
    trusted = _trusted_inputs(tmp_path)
    base = datetime.now(UTC) - timedelta(hours=6)
    abort = _finalize_one_rehearsal(
        tmp_path,
        trusted,
        _execution(
            release=trusted["release"],
            qualification=trusted["qualification"],
            documentation=trusted["documentation"],
            base=base,
            mode="abort_drill",
            sequence=0,
            source_seed="1",
        ),
        "abort",
    )
    first = _finalize_one_rehearsal(
        tmp_path,
        trusted,
        _execution(
            release=trusted["release"],
            qualification=trusted["qualification"],
            documentation=trusted["documentation"],
            base=base + timedelta(hours=1),
            mode="full",
            sequence=1,
            source_seed="3",
        ),
        "rehearsal-1",
    )
    second = _finalize_one_rehearsal(
        tmp_path,
        trusted,
        _execution(
            release=trusted["release"],
            qualification=trusted["qualification"],
            documentation=trusted["documentation"],
            base=base + timedelta(hours=2),
            mode="full",
            sequence=2,
            source_seed="5",
        ),
        "rehearsal-2",
    )
    series = finalize_rehearsal_series(
        abort_report_path=tmp_path / "abort-report.json",
        rehearsal_report_paths=[
            tmp_path / "rehearsal-1-report.json",
            tmp_path / "rehearsal-2-report.json",
        ],
        rehearsal_public_key=trusted["rehearsal_public"],
        signing_key=trusted["rehearsal_private"],
        signer="Migration rehearsal owner",
        output_path=tmp_path / "rehearsal-series.json",
    )
    assert abort["status"] == "abort_drill_passed"
    assert first["status"] == second["status"] == "rehearsal_passed"
    assert series["status"] == "qualified_for_production_cutover"

    production_base = datetime.now(UTC) - timedelta(hours=1)
    intent = {
        "kind": "workchord-postgresql-production-cutover-authorization",
        "schema_version": 1,
        "authorization_id": "production-authorization-001",
        "change_id": "CHG-PG-2026-001",
        "created_at": _timestamp(production_base - timedelta(hours=1)),
        "status": "authorized",
        "valid_from": _timestamp(production_base - timedelta(minutes=30)),
        "expires_at": _timestamp(production_base + timedelta(hours=4)),
        "release": _release_reference(trusted["release"]),
        "dependencies": {
            "qualification_report_sha256": trusted["qualification"]["document_sha256"],
            "documentation_walkthrough_sha256": trusted["documentation"]["document_sha256"],
            "rehearsal_series_sha256": series["document_sha256"],
        },
        "source_scope": {
            "deployment_id": "workchord-primary",
            "sqlite_identifier": "/srv/workchord/workchord.db",
            "revision": "20260719_0033",
        },
        "target": _target(),
        "authorities": _operators(),
        "decision": {
            "approved": True,
            "downtime_budget_minutes": 180,
            "rollback_before_first_write": True,
            "reverse_sync_available": False,
            "sqlite_retention": "read_only",
            "evidence_sha256": "f" * 64,
        },
    }
    _write_raw(tmp_path / "production-intent.json", intent)
    authorization = authorize_production(
        intent_path=tmp_path / "production-intent.json",
        release_manifest_path=tmp_path / "release.json",
        qualification_report_path=tmp_path / "qualification.json",
        qualification_public_key=trusted["qualification_public"],
        documentation_walkthrough_path=tmp_path / "documentation.json",
        documentation_public_key=trusted["documentation_public"],
        rehearsal_series_path=tmp_path / "rehearsal-series.json",
        rehearsal_public_key=trusted["rehearsal_public"],
        signing_key=trusted["authorization_private"],
        signer="Authorized change approver",
        output_path=tmp_path / "production-authorization.json",
    )
    production_execution = _execution(
        release=trusted["release"],
        qualification=trusted["qualification"],
        documentation=trusted["documentation"],
        base=production_base,
        mode="full",
        sequence=1,
        source_seed="7",
        environment="production",
        authorization_sha256=authorization["document_sha256"],
    )
    _write_raw(tmp_path / "production-execution-raw.json", production_execution)
    seal_execution(
        input_path=tmp_path / "production-execution-raw.json",
        output_path=tmp_path / "production-execution.json",
    )
    production = finalize_production(
        execution_path=tmp_path / "production-execution.json",
        release_manifest_path=tmp_path / "release.json",
        qualification_report_path=tmp_path / "qualification.json",
        qualification_public_key=trusted["qualification_public"],
        documentation_walkthrough_path=tmp_path / "documentation.json",
        documentation_public_key=trusted["documentation_public"],
        rehearsal_series_path=tmp_path / "rehearsal-series.json",
        rehearsal_public_key=trusted["rehearsal_public"],
        authorization_path=tmp_path / "production-authorization.json",
        authorization_public_key=trusted["authorization_public"],
        signing_key=trusted["production_private"],
        signer="Production evidence recorder",
        output_path=tmp_path / "production-cutover.json",
    )
    assert production["status"] == "completed"
    assert verify_report(
        report_path=tmp_path / "production-cutover.json",
        trusted_public_key=trusted["production_public"],
    ) == production["document_sha256"]


def test_execution_refuses_manual_steps_hard_stop_and_secret_material(
    tmp_path: Path,
) -> None:
    trusted = _trusted_inputs(tmp_path)
    execution = _execution(
        release=trusted["release"],
        qualification=trusted["qualification"],
        documentation=trusted["documentation"],
        base=datetime.now(UTC) - timedelta(hours=1),
        mode="full",
        sequence=1,
        source_seed="1",
    )
    execution["outcome"]["manual_steps"] = ["ran an undocumented repair"]
    _write_raw(tmp_path / "manual.json", execution)
    with pytest.raises(CutoverEvidenceError, match="Manual or undocumented"):
        seal_execution(input_path=tmp_path / "manual.json", output_path=tmp_path / "manual-sealed.json")

    execution["outcome"]["manual_steps"] = []
    c13_start = datetime.fromisoformat(execution["gates"]["C13"]["started_at"])
    execution["gates"]["C13"]["completed_at"] = _timestamp(
        c13_start + timedelta(hours=4)
    )
    _write_raw(tmp_path / "late.json", execution)
    with pytest.raises(CutoverEvidenceError, match="C13 crossed"):
        seal_execution(input_path=tmp_path / "late.json", output_path=tmp_path / "late-sealed.json")

    execution = _execution(
        release=trusted["release"],
        qualification=trusted["qualification"],
        documentation=trusted["documentation"],
        base=datetime.now(UTC) - timedelta(hours=1),
        mode="full",
        sequence=1,
        source_seed="1",
    )
    execution["target"]["identifier"] = "postgresql://operator:password@db/workchord"
    _write_raw(tmp_path / "secret.json", execution)
    with pytest.raises(CutoverEvidenceError, match="Credential-bearing URL"):
        seal_execution(input_path=tmp_path / "secret.json", output_path=tmp_path / "secret-sealed.json")


def test_trusted_key_pin_and_abort_drill_are_mandatory(tmp_path: Path) -> None:
    trusted = _trusted_inputs(tmp_path)
    wrong_private, wrong_public = _key_pair(tmp_path, "wrong")
    del wrong_private
    with pytest.raises(CutoverEvidenceError, match="not the trusted public key"):
        verify_report(
            report_path=tmp_path / "documentation.json",
            trusted_public_key=wrong_public,
        )

    base = datetime.now(UTC) - timedelta(hours=3)
    first = _finalize_one_rehearsal(
        tmp_path,
        trusted,
        _execution(
            release=trusted["release"],
            qualification=trusted["qualification"],
            documentation=trusted["documentation"],
            base=base,
            mode="full",
            sequence=1,
            source_seed="1",
        ),
        "first",
    )
    second = _finalize_one_rehearsal(
        tmp_path,
        trusted,
        _execution(
            release=trusted["release"],
            qualification=trusted["qualification"],
            documentation=trusted["documentation"],
            base=base + timedelta(hours=1),
            mode="full",
            sequence=2,
            source_seed="3",
        ),
        "second",
    )
    assert read_document(tmp_path / "first-report.json") == first
    assert read_document(tmp_path / "second-report.json") == second
    with pytest.raises(CutoverEvidenceError, match="one abort drill"):
        finalize_rehearsal_series(
            abort_report_path=tmp_path / "first-report.json",
            rehearsal_report_paths=[
                tmp_path / "first-report.json",
                tmp_path / "second-report.json",
            ],
            rehearsal_public_key=trusted["rehearsal_public"],
            signing_key=trusted["rehearsal_private"],
            signer="Migration rehearsal owner",
            output_path=tmp_path / "invalid-series.json",
        )


def test_execution_schema_and_installed_entrypoint_match_runtime_contract(
    tmp_path: Path,
) -> None:
    trusted = _trusted_inputs(tmp_path)
    execution = _execution(
        release=trusted["release"],
        qualification=trusted["qualification"],
        documentation=trusted["documentation"],
        base=datetime.now(UTC) - timedelta(hours=1),
        mode="full",
        sequence=1,
        source_seed="1",
    )
    repository_root = Path(__file__).resolve().parents[3]
    schema = json.loads(
        (
            repository_root
            / "backend/app/database_migration/postgresql-cutover-execution-v1.schema.json"
        ).read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    errors = list(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(execution)
    )
    assert errors == []

    project = tomllib.loads(
        (repository_root / "backend/pyproject.toml").read_text(encoding="utf-8")
    )
    assert project["project"]["scripts"]["workchord-db-cutover"] == (
        "app.cli.cutover:main"
    )
