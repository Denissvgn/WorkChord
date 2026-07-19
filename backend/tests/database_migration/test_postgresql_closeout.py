"""Contracts for DBM-DOC-002 publication and DBM-CLOSE-001 decisions."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import tomllib

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from app.database_migration.closeout import (
    AUDIT_CHECK_IDS,
    AVAILABILITY_OBJECTIVE_PERCENT,
    CAPACITY_WORDING,
    CLOSEOUT_INPUT_ATTESTATION,
    DBM_TASK_IDS,
    RELEASE_GATE_IDS,
    CloseoutEvidenceError,
    _validate_availability,
    finalize_closeout,
    publish_postcutover_release,
    render_release_notes,
    verify_closeout_report,
)
from app.database_migration.cutover import (
    authorize_production,
    finalize_production,
    finalize_rehearsal_series,
    seal_execution,
)
from tests.database_migration.test_cutover_evidence import (
    _execution,
    _finalize_one_rehearsal,
    _key_pair,
    _operators,
    _release_reference,
    _target,
    _timestamp,
    _trusted_inputs,
    _write_raw,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def _production_chain(tmp_path: Path) -> tuple[dict, dict]:
    trusted = _trusted_inputs(tmp_path)
    base = datetime.now(UTC) - timedelta(hours=10)
    _finalize_one_rehearsal(
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
    _finalize_one_rehearsal(
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
    _finalize_one_rehearsal(
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

    production_base = datetime.now(UTC) - timedelta(hours=4)
    intent = {
        "kind": "workchord-postgresql-production-cutover-authorization",
        "schema_version": 1,
        "authorization_id": "production-authorization-closeout-test",
        "change_id": "CHG-PG-CLOSEOUT-TEST",
        "created_at": _timestamp(production_base - timedelta(hours=1)),
        "status": "authorized",
        "valid_from": _timestamp(production_base - timedelta(minutes=30)),
        "expires_at": _timestamp(production_base + timedelta(hours=6)),
        "release": _release_reference(trusted["release"]),
        "dependencies": {
            "qualification_report_sha256": trusted["qualification"]["document_sha256"],
            "documentation_walkthrough_sha256": trusted["documentation"]["document_sha256"],
            "rehearsal_series_sha256": series["document_sha256"],
        },
        "source_scope": {
            "deployment_id": "workchord-primary",
            "sqlite_identifier": "/srv/workchord/workchord.db",
            "revision": "20260718_0032",
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
    execution = _execution(
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
    execution["change_id"] = intent["change_id"]
    _write_raw(tmp_path / "production-execution-raw.json", execution)
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
    return trusted, production


def _publication(tmp_path: Path, trusted: dict, production: dict) -> tuple[dict, Path, Path]:
    private_key, public_key = _key_pair(tmp_path, "publication")
    version = tomllib.loads(
        (REPOSITORY_ROOT / "backend/pyproject.toml").read_text(encoding="utf-8")
    )["project"]["version"]
    raw = {
        "kind": "workchord-postgresql-postcutover-publication-input",
        "schema_version": 1,
        "publication_id": f"workchord-postgresql-release-{version}",
        "published_at": _timestamp(datetime.now(UTC) - timedelta(hours=1)),
        "status": "approved_for_publication",
        "application_version": version,
        "postgresql_version": "18.4",
        "postgresql_version_evidence_sha256": "1" * 64,
        "release_boundary": f"workchord-{version}",
        "artifact_references": [
            {
                "kind": "precutover_qualification",
                "public_uri": "urn:workchord:evidence:qualification:test",
                "sha256": trusted["qualification"]["document_sha256"],
            },
            {
                "kind": "production_cutover",
                "public_uri": "https://evidence.example.test/workchord/cutover/test",
                "sha256": production["document_sha256"],
            },
        ],
        "operational_exceptions": [],
        "approval": {
            "product_owner": "Product owner",
            "release_owner": "Post-cutover publication owner",
            "evidence_sha256": "2" * 64,
        },
    }
    _write_raw(tmp_path / "publication-input.json", raw)
    document = publish_postcutover_release(
        input_path=tmp_path / "publication-input.json",
        repository_root=REPOSITORY_ROOT,
        release_manifest_path=tmp_path / "release.json",
        qualification_report_path=tmp_path / "qualification.json",
        qualification_public_key=trusted["qualification_public"],
        production_cutover_path=tmp_path / "production-cutover.json",
        production_public_key=trusted["production_public"],
        signing_key=private_key,
        signer="Post-cutover publication owner",
        output_path=tmp_path / "publication.json",
    )
    return document, private_key, public_key


def _complete_closeout(
    trusted: dict,
    production: dict,
    publication: dict,
) -> dict:
    audited_at = datetime.now(UTC) - timedelta(minutes=1)
    production_completed = datetime.fromisoformat(production["execution"]["completed_at"])
    stabilization_started = datetime.fromisoformat(
        production["execution"]["outcome"]["stabilization_started_at"]
    )
    tasks = {
        task_id: {
            "status": "complete",
            "evidence_sha256": f"{index + 16:02x}" * 32,
            "exception_id": None,
        }
        for index, task_id in enumerate(DBM_TASK_IDS)
    }
    gates = {
        gate_id: {
            "status": "passed",
            "evidence_sha256": f"{index + 80:02x}" * 32,
            "exception_id": None,
        }
        for index, gate_id in enumerate(RELEASE_GATE_IDS)
    }
    for task_id, gate_id, evidence in (
        ("DBM-QUAL-001", "G10", trusted["qualification"]),
        ("DBM-CUT-002", "G13", production),
        ("DBM-DOC-002", "G15", publication),
    ):
        tasks[task_id]["evidence_sha256"] = evidence["document_sha256"]
        gates[gate_id]["evidence_sha256"] = evidence["document_sha256"]
    return {
        "kind": "workchord-postgresql-closeout-observations",
        "schema_version": 1,
        "audit_id": "postgresql-closeout-independent-test",
        "audited_at": _timestamp(audited_at),
        "auditor": {
            "identity": "Independent closure auditor",
            "independent": True,
        },
        "task_evidence": tasks,
        "release_gates": gates,
        "stabilization": {
            "status": "passed",
            "started_at": _timestamp(stabilization_started),
            "completed_at": _timestamp(stabilization_started + timedelta(hours=2)),
            "approved_duration_hours": 1,
            "approval_evidence_sha256": "a" * 64,
            "evidence_sha256": "b" * 64,
        },
        "post_cutover_verification": {
            "status": "passed",
            "profile_id": "controlled-postcutover-test",
            "started_at": _timestamp(production_completed + timedelta(minutes=10)),
            "completed_at": _timestamp(production_completed + timedelta(minutes=20)),
            "result_sha256": "c" * 64,
            "production_path": True,
            "all_applicable_slo_gates_passed": True,
            "unexplained_integrity_differences": 0,
        },
        "backup_restore": {
            "status": "passed",
            "backup_completed_at": _timestamp(production_completed + timedelta(minutes=30)),
            "restore_completed_at": _timestamp(production_completed + timedelta(minutes=50)),
            "backup_sha256": "d" * 64,
            "restore_report_sha256": "e" * 64,
            "rpo_seconds": 240,
            "rto_seconds": 1200,
            "schema_head": trusted["release"]["schema_head"],
            "isolated_target": True,
            "reconciled": True,
        },
        "operational_audit": {
            check_id: {"status": "passed", "evidence_sha256": f"{index + 112:02x}" * 32}
            for index, check_id in enumerate(AUDIT_CHECK_IDS)
        },
        "availability": {
            "status": "pending",
            "observation_started_at": _timestamp(stabilization_started),
            "observation_completed_at": None,
            "eligible_attempts": None,
            "successful_attempts": None,
            "objective_percent": AVAILABILITY_OBJECTIVE_PERCENT,
            "objective_claimed": False,
            "denominator_complete": False,
            "evidence_sha256": None,
        },
        "sqlite_snapshot": {
            "state": "retained_read_only",
            "snapshot_sha256": production["execution"]["source"]["snapshot_sha256"],
            "retention_approval_sha256": "f" * 64,
            "retain_until": _timestamp(audited_at + timedelta(days=35)),
            "disposed_at": None,
            "disposal_evidence_sha256": None,
            "writable": False,
        },
        "exceptions": [],
        "evidence_index_sha256": "9" * 64,
        "no_omission_attestation": CLOSEOUT_INPUT_ATTESTATION,
    }


def _not_started_closeout() -> dict:
    audited_at = datetime.now(UTC) - timedelta(minutes=1)
    scope = [*DBM_TASK_IDS, *RELEASE_GATE_IDS]
    return {
        "kind": "workchord-postgresql-closeout-observations",
        "schema_version": 1,
        "audit_id": "postgresql-closeout-no-production-test",
        "audited_at": _timestamp(audited_at),
        "auditor": {
            "identity": "Independent closure auditor",
            "independent": True,
        },
        "task_evidence": {
            task_id: {
                "status": "incomplete",
                "evidence_sha256": None,
                "exception_id": "missing-production-evidence",
            }
            for task_id in DBM_TASK_IDS
        },
        "release_gates": {
            gate_id: {
                "status": "pending",
                "evidence_sha256": None,
                "exception_id": "missing-production-evidence",
            }
            for gate_id in RELEASE_GATE_IDS
        },
        "stabilization": {
            "status": "not_started",
            "started_at": None,
            "completed_at": None,
            "approved_duration_hours": None,
            "approval_evidence_sha256": None,
            "evidence_sha256": None,
        },
        "post_cutover_verification": {
            "status": "not_started",
            "profile_id": None,
            "started_at": None,
            "completed_at": None,
            "result_sha256": None,
            "production_path": None,
            "all_applicable_slo_gates_passed": None,
            "unexplained_integrity_differences": None,
        },
        "backup_restore": {
            "status": "not_started",
            "backup_completed_at": None,
            "restore_completed_at": None,
            "backup_sha256": None,
            "restore_report_sha256": None,
            "rpo_seconds": None,
            "rto_seconds": None,
            "schema_head": None,
            "isolated_target": None,
            "reconciled": None,
        },
        "operational_audit": {
            check_id: {"status": "not_started", "evidence_sha256": None}
            for check_id in AUDIT_CHECK_IDS
        },
        "availability": {
            "status": "not_started",
            "observation_started_at": None,
            "observation_completed_at": None,
            "eligible_attempts": None,
            "successful_attempts": None,
            "objective_percent": AVAILABILITY_OBJECTIVE_PERCENT,
            "objective_claimed": False,
            "denominator_complete": False,
            "evidence_sha256": None,
        },
        "sqlite_snapshot": {
            "state": "not_created",
            "snapshot_sha256": None,
            "retention_approval_sha256": None,
            "retain_until": None,
            "disposed_at": None,
            "disposal_evidence_sha256": None,
            "writable": None,
        },
        "exceptions": [
            {
                "id": "missing-production-evidence",
                "status": "open",
                "owner": "Migration program owner",
                "expires_at": _timestamp(audited_at + timedelta(days=7)),
                "scope": scope,
                "rationale": "Required external qualification and production evidence is absent",
                "approval_evidence_sha256": None,
            }
        ],
        "evidence_index_sha256": "8" * 64,
        "no_omission_attestation": CLOSEOUT_INPUT_ATTESTATION,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_postcutover_publication_and_ship_decision_are_bound_to_production(
    tmp_path: Path,
) -> None:
    trusted, production = _production_chain(tmp_path)
    publication, _, publication_public = _publication(tmp_path, trusted, production)
    assert publication["status"] == "published"
    assert CAPACITY_WORDING in publication["release_notes"]["content"]
    assert verify_closeout_report(
        report_path=tmp_path / "publication.json",
        trusted_public_key=publication_public,
    ) == publication["document_sha256"]

    rendered = tmp_path / "postgresql-production-transition.md"
    assert render_release_notes(
        publication_path=tmp_path / "publication.json",
        publication_public_key=publication_public,
        output_path=rendered,
    ) == publication["release_notes"]["sha256"]
    assert rendered.read_text(encoding="utf-8") == publication["release_notes"]["content"]
    with pytest.raises(CloseoutEvidenceError, match="will not be overwritten"):
        render_release_notes(
            publication_path=tmp_path / "publication.json",
            publication_public_key=publication_public,
            output_path=rendered,
        )

    observations = _complete_closeout(trusted, production, publication)
    _write_json(tmp_path / "closeout-observations.json", observations)
    closure_private, closure_public = _key_pair(tmp_path, "closure")
    decision = finalize_closeout(
        input_path=tmp_path / "closeout-observations.json",
        repository_root=REPOSITORY_ROOT,
        release_manifest_path=tmp_path / "release.json",
        qualification_report_path=tmp_path / "qualification.json",
        qualification_public_key=trusted["qualification_public"],
        production_cutover_path=tmp_path / "production-cutover.json",
        production_public_key=trusted["production_public"],
        publication_path=tmp_path / "publication.json",
        publication_public_key=publication_public,
        signing_key=closure_private,
        signer="Independent closure auditor",
        output_path=tmp_path / "closure-decision.json",
    )
    assert decision["verdict"] == "SHIP"
    assert decision["availability_claim"] == "pending"
    assert decision["blockers"] == []
    assert verify_closeout_report(
        report_path=tmp_path / "closure-decision.json",
        trusted_public_key=closure_public,
    ) == decision["document_sha256"]


def test_missing_production_evidence_is_signed_no_ship(tmp_path: Path) -> None:
    observations = _not_started_closeout()
    _write_json(tmp_path / "no-ship-observations.json", observations)
    private_key, public_key = _key_pair(tmp_path, "no-ship-closure")
    decision = finalize_closeout(
        input_path=tmp_path / "no-ship-observations.json",
        repository_root=None,
        release_manifest_path=None,
        qualification_report_path=None,
        qualification_public_key=None,
        production_cutover_path=None,
        production_public_key=None,
        publication_path=None,
        publication_public_key=None,
        signing_key=private_key,
        signer="Independent closure auditor",
        output_path=tmp_path / "no-ship-decision.json",
    )
    assert decision["verdict"] == "NO-SHIP"
    assert decision["plan_status"] == "open"
    assert any("DBM-CUT-002" in blocker for blocker in decision["blockers"])
    assert verify_closeout_report(
        report_path=tmp_path / "no-ship-decision.json",
        trusted_public_key=public_key,
    ) == decision["document_sha256"]


def test_availability_claim_and_external_evidence_cannot_be_fabricated(
    tmp_path: Path,
) -> None:
    trusted, production = _production_chain(tmp_path)
    publication, _, publication_public = _publication(tmp_path, trusted, production)
    observations = _complete_closeout(trusted, production, publication)
    observations["availability"]["objective_claimed"] = True
    _write_json(tmp_path / "false-availability.json", observations)
    closure_private, _ = _key_pair(tmp_path, "false-availability-closure")
    with pytest.raises(CloseoutEvidenceError, match="Pending availability"):
        finalize_closeout(
            input_path=tmp_path / "false-availability.json",
            repository_root=REPOSITORY_ROOT,
            release_manifest_path=tmp_path / "release.json",
            qualification_report_path=tmp_path / "qualification.json",
            qualification_public_key=trusted["qualification_public"],
            production_cutover_path=tmp_path / "production-cutover.json",
            production_public_key=trusted["production_public"],
            publication_path=tmp_path / "publication.json",
            publication_public_key=publication_public,
            signing_key=closure_private,
            signer="Independent closure auditor",
            output_path=tmp_path / "false-availability-decision.json",
        )

    missing = _not_started_closeout()
    missing["task_evidence"]["DBM-CUT-002"] = {
        "status": "complete",
        "evidence_sha256": "a" * 64,
        "exception_id": None,
    }
    _write_json(tmp_path / "fake-production.json", missing)
    with pytest.raises(CloseoutEvidenceError, match="claims completion without"):
        finalize_closeout(
            input_path=tmp_path / "fake-production.json",
            repository_root=None,
            release_manifest_path=None,
            qualification_report_path=None,
            qualification_public_key=None,
            production_cutover_path=None,
            production_public_key=None,
            publication_path=None,
            publication_public_key=None,
            signing_key=closure_private,
            signer="Independent closure auditor",
            output_path=tmp_path / "fake-production-decision.json",
        )


def test_closeout_entrypoint_is_packaged() -> None:
    project = tomllib.loads(
        (REPOSITORY_ROOT / "backend/pyproject.toml").read_text(encoding="utf-8")
    )
    assert project["project"]["scripts"]["workchord-db-closeout"] == (
        "app.cli.closeout:main"
    )


def test_postcutover_input_schemas_match_runtime_examples() -> None:
    schema_root = REPOSITORY_ROOT / "backend/app/database_migration"
    publication_schema = json.loads(
        (schema_root / "postgresql-postcutover-publication-input-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    closeout_schema = json.loads(
        (schema_root / "postgresql-closeout-observations-v1.schema.json").read_text(
            encoding="utf-8"
        )
    )
    for schema in (publication_schema, closeout_schema):
        Draft202012Validator.check_schema(schema)

    publication_input = {
        "kind": "workchord-postgresql-postcutover-publication-input",
        "schema_version": 1,
        "publication_id": "workchord-postgresql-release-1.6.2",
        "published_at": _timestamp(datetime.now(UTC) - timedelta(minutes=1)),
        "status": "approved_for_publication",
        "application_version": "1.6.2",
        "postgresql_version": "18.4",
        "postgresql_version_evidence_sha256": "1" * 64,
        "release_boundary": "workchord-1.6.2",
        "artifact_references": [
            {
                "kind": "precutover_qualification",
                "public_uri": "urn:workchord:evidence:qualification:test",
                "sha256": "2" * 64,
            },
            {
                "kind": "production_cutover",
                "public_uri": "urn:workchord:evidence:cutover:test",
                "sha256": "3" * 64,
            },
        ],
        "operational_exceptions": [],
        "approval": {
            "product_owner": "Product owner",
            "release_owner": "Release owner",
            "evidence_sha256": "4" * 64,
        },
    }
    assert list(
        Draft202012Validator(
            publication_schema, format_checker=FormatChecker()
        ).iter_errors(publication_input)
    ) == []
    assert list(
        Draft202012Validator(
            closeout_schema, format_checker=FormatChecker()
        ).iter_errors(_not_started_closeout())
    ) == []


def test_availability_objective_requires_complete_thirty_day_denominator() -> None:
    started = datetime.now(UTC) - timedelta(days=31)
    production = {"stabilization_started_at": _timestamp(started)}
    pending = {
        "status": "pending",
        "observation_started_at": _timestamp(started),
        "observation_completed_at": None,
        "eligible_attempts": None,
        "successful_attempts": None,
        "objective_percent": AVAILABILITY_OBJECTIVE_PERCENT,
        "objective_claimed": False,
        "denominator_complete": False,
        "evidence_sha256": None,
    }
    _, blockers, claim = _validate_availability(
        pending,
        audited_at=datetime.now(UTC),
        production=production,
    )
    assert claim == "pending"
    assert blockers == ["G14: 30-day availability denominator is overdue"]

    complete = {
        **pending,
        "status": "met",
        "observation_completed_at": _timestamp(started + timedelta(days=30)),
        "eligible_attempts": 10_000,
        "successful_attempts": 9_990,
        "objective_claimed": True,
        "denominator_complete": True,
        "evidence_sha256": "7" * 64,
    }
    normalized, blockers, claim = _validate_availability(
        complete,
        audited_at=datetime.now(UTC),
        production=production,
    )
    assert normalized["observed_percent"] == 99.9
    assert blockers == []
    assert claim == "met"

    complete["status"] = "missed"
    complete["successful_attempts"] = 9_989
    complete["objective_claimed"] = False
    _, blockers, claim = _validate_availability(
        complete,
        audited_at=datetime.now(UTC),
        production=production,
    )
    assert blockers == ["G14: 30-day availability objective was missed"]
    assert claim == "missed"
