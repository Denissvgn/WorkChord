#!/usr/bin/env python3
"""Freeze, assemble, sign, and verify PostgreSQL capacity qualification."""

from __future__ import annotations

import argparse
import base64
from datetime import timedelta
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Mapping
from uuid import uuid4

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from jsonschema import Draft202012Validator, FormatChecker

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    QUALIFICATION_SCHEMA_PATH,
    QualificationInputError,
    REPOSITORY_ROOT,
    atomic_write_json,
    canonical_json_bytes,
    capacity_contract,
    contract_sha256,
    read_json_object,
    sha256_bytes,
    sha256_file,
    utc_now_text,
    verify_document,
)
from scripts.load.result import validate_result


IMAGE_PATTERN = re.compile(r"^.+@sha256:[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
LIFECYCLE_POLICY = (
    REPOSITORY_ROOT
    / "docs/contracts/postgresql-data-lifecycle-policy-v1.json"
)
ATTESTATION = (
    "The listed attempts are the final three consecutive qualification attempts "
    "for this frozen release, and no failed or excluded attempt is omitted."
)
REQUIRED_RESULTS = {
    ("mixed_peak_v1", "warmup"): 15 * 60,
    ("mixed_peak_v1", "steady"): 60 * 60,
    ("mixed_peak_v1", "burst"): 10 * 60,
    ("mixed_peak_v1", "soak"): 8 * 60 * 60,
    ("human_peak_v1", "steady"): 60 * 60,
    ("connection_surge_v1", "burst"): 10 * 60,
    ("external_llm_wait_v1", "external_wait"): 60,
}
RUN_GATES = frozenset(
    {
        "all_required_phases",
        "all_load_gates",
        "traffic_conformance",
        "resilience",
        "restore",
        "domain_integrity",
        "capacity_horizon",
        "final_ci_matrix",
    }
)
REPORT_GATES = frozenset(
    {
        "three_consecutive_complete_runs",
        "frozen_release_identity",
        "exact_capacity_shape",
        "traffic_and_latency",
        "resource_and_growth",
        "fault_and_recovery",
        "backup_restore_rpo_rto",
        "domain_integrity",
        "final_ci_matrix",
    }
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ZERO_HUMAN_EXECUTION_MODE = "zero-human-agent-v1"


def _reject_local_signing_in_zero_human_mode() -> None:
    if os.getenv("WORKCHORD_EXECUTION_MODE", "").strip() == ZERO_HUMAN_EXECUTION_MODE:
        raise QualificationInputError(
            "File private keys and embedded trust keys are forbidden in "
            f"{ZERO_HUMAN_EXECUTION_MODE}; use the remote-KMS detached-signature "
            "interface and an externally resolved pinned trust anchor"
        )


def _schema_errors(document: Mapping[str, Any]) -> list[str]:
    schema = read_json_object(QUALIFICATION_SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors[:10]
    ]


def _fingerprint(payload: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(payload))


def _require_new_output(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise QualificationInputError(
            f"Qualification output already exists and will not be overwritten: {path}"
        )


def _validate_frozen_release(document: Mapping[str, Any]) -> None:
    if (
        document.get("kind") != "workchord-postgresql-frozen-release"
        or document.get("schema_version") != 1
        or document.get("status") != "frozen"
        or COMMIT_PATTERN.fullmatch(str(document.get("commit", ""))) is None
    ):
        raise QualificationInputError("Release manifest is not a valid frozen release")
    images = document.get("images")
    if (
        not isinstance(images, list)
        or any(not isinstance(item, str) for item in images)
        or len(set(images)) < 3
        or any(IMAGE_PATTERN.fullmatch(item) is None for item in images)
    ):
        raise QualificationInputError("Frozen release image identities are invalid")
    required_hashes = (
        "hardware_evidence_sha256",
        "seed_manifest_sha256",
        "lifecycle_policy_sha256",
    )
    if any(
        re.fullmatch(r"[0-9a-f]{64}", str(document.get(name, ""))) is None
        for name in required_hashes
    ):
        raise QualificationInputError("Frozen release evidence checksums are invalid")
    configuration = document.get("configuration")
    if (
        not isinstance(configuration, Mapping)
        or not str(configuration.get("name", ""))
        or re.fullmatch(
            r"[0-9a-f]{64}", str(configuration.get("sha256", ""))
        )
        is None
        or not str(document.get("schema_head", ""))
        or not isinstance(document.get("database"), Mapping)
    ):
        raise QualificationInputError("Frozen release configuration is incomplete")
    _parse_time(str(document.get("created_at", "")))
    body = dict(document)
    body.pop("document_sha256", None)
    fingerprint = str(body.pop("fingerprint", ""))
    if fingerprint != _fingerprint(body):
        raise QualificationInputError("Frozen release fingerprint differs")
    capacity = document.get("capacity_contract")
    if capacity != {
        "id": capacity_contract()["contract_id"],
        "sha256": contract_sha256(),
    }:
        raise QualificationInputError("Frozen release capacity contract differs")
    if document.get("lifecycle_policy_sha256") != sha256_file(LIFECYCLE_POLICY):
        raise QualificationInputError("Frozen release lifecycle policy differs")


def _freeze(args: argparse.Namespace) -> int:
    _require_new_output(args.output)
    if COMMIT_PATTERN.fullmatch(args.commit) is None:
        raise QualificationInputError("Release commit must be a full lowercase SHA")
    images = sorted(set(args.image))
    if len(images) < 3 or any(IMAGE_PATTERN.fullmatch(item) is None for item in images):
        raise QualificationInputError(
            "At least three unique images pinned by @sha256 are required"
        )
    seed = read_json_object(args.seed_manifest, sealed=True)
    if seed.get("qualification_eligible") is not True:
        raise QualificationInputError("Release freeze requires a full eligible seed")
    hardware = read_json_object(args.hardware_evidence, sealed=True)
    if hardware.get("matches_reference_hardware") is not True:
        raise QualificationInputError(
            "Hardware evidence does not attest the reference topology"
        )
    if not args.configuration.exists():
        raise QualificationInputError("Frozen configuration file does not exist")
    contract = capacity_contract()
    body = {
        "kind": "workchord-postgresql-frozen-release",
        "schema_version": 1,
        "created_at": utc_now_text(),
        "status": "frozen",
        "commit": args.commit,
        "images": images,
        "schema_head": args.schema_head,
        "configuration": {
            "name": args.configuration.name,
            "sha256": sha256_file(args.configuration),
        },
        "hardware_evidence_sha256": hardware["document_sha256"],
        "seed_manifest_sha256": seed["document_sha256"],
        "capacity_contract": {
            "id": contract["contract_id"],
            "sha256": contract_sha256(),
        },
        "lifecycle_policy_sha256": sha256_file(LIFECYCLE_POLICY),
        "database": {
            "major": contract["database"]["target"]["major"],
            "reference_minor": contract["database"]["target"]["reference_minor"],
            "locale": contract["database"]["target"]["locale"],
            "schema": contract["database"]["target"]["application_schema"],
            "search_path": contract["database"]["target"]["search_path"],
            "pooling": contract["database"]["pooling"],
        },
    }
    body["fingerprint"] = _fingerprint(body)
    document = atomic_write_json(args.output, body)
    print(
        f"Frozen release fingerprint={document['fingerprint']} "
        f"sha256={document['document_sha256']}"
    )
    return 0


def _require_ci_evidence(document: Mapping[str, Any], commit: str) -> None:
    required_flags = (
        "clean_checkout",
        "postgresql_matrix",
        "sqlite_lane",
        "installed_wheel_postgresql",
        "source_copy_reconciliation",
        "maintenance_modes",
        "single_alembic_head",
    )
    if (
        document.get("kind") != "workchord-ci-qualification-evidence"
        or document.get("status") != "passed"
        or document.get("commit") != commit
        or any(document.get(flag) is not True for flag in required_flags)
    ):
        raise QualificationInputError(
            "CI evidence does not prove the complete final tuned matrix"
        )


def _bundle(args: argparse.Namespace) -> int:
    _require_new_output(args.output)
    release = read_json_object(args.release_manifest, sealed=True)
    seed = read_json_object(args.seed_manifest, sealed=True)
    resilience = read_json_object(args.resilience, sealed=True)
    ci = read_json_object(args.ci_evidence, sealed=True)
    _validate_frozen_release(release)
    if seed.get("document_sha256") != release.get("seed_manifest_sha256"):
        raise QualificationInputError("Run seed differs from the frozen release")
    if resilience.get("status") != "passed" or resilience.get(
        "release_fingerprint"
    ) != release.get("fingerprint"):
        raise QualificationInputError(
            "Resilience result did not pass for the frozen release"
        )
    _require_ci_evidence(ci, str(release["commit"]))

    observed: dict[tuple[str, str], dict[str, Any]] = {}
    refs: list[dict[str, Any]] = []
    for path in args.result:
        result = read_json_object(path, sealed=True)
        validate_result(result)
        key = (result["traffic"]["profile_id"], result["traffic"]["phase"])
        if key in observed:
            raise QualificationInputError(f"Duplicate qualification result {key}")
        observed[key] = result
        reasons: list[str] = []
        if key not in REQUIRED_RESULTS:
            reasons.append("unapproved profile/phase")
        elif float(result["traffic"]["target_duration_seconds"]) != float(
            REQUIRED_RESULTS[key]
        ):
            reasons.append("target duration differs from contract")
        if result.get("status") != "passed":
            reasons.append(f"status is {result.get('status')}")
        if result.get("qualification_candidate") is not True:
            reasons.append("not a qualification candidate")
        if result["target"].get("environment") != "rehearsal":
            reasons.append("target is not rehearsal")
        if result["seed"].get("manifest_sha256") != seed["document_sha256"]:
            reasons.append("seed checksum differs")
        result_release = result.get("release", {})
        if result_release.get("fingerprint") != release["fingerprint"]:
            reasons.append("release fingerprint differs")
        gate_statuses = {item.get("status") for item in result["gates"].values()}
        if gate_statuses - {"passed", "not_applicable"}:
            reasons.append(f"nonpassing gates: {sorted(gate_statuses)}")
        if float(result["traffic"]["actual_duration_seconds"]) < (
            float(result["traffic"]["target_duration_seconds"]) * 0.95
        ):
            reasons.append("actual duration is below 95 percent of target")
        if reasons:
            raise QualificationInputError(f"Result {key} is ineligible: {reasons}")
        refs.append(
            {
                "profile": key[0],
                "phase": key[1],
                "run_id": result["run_id"],
                "sha256": result["document_sha256"],
                "created_at": result["created_at"],
            }
        )
    missing = sorted(set(REQUIRED_RESULTS) - set(observed))
    extra = sorted(set(observed) - set(REQUIRED_RESULTS))
    if missing or extra:
        raise QualificationInputError(
            f"Qualification run result set differs: missing={missing}, extra={extra}"
        )

    completed_at = max(
        refs,
        key=lambda item: _parse_time(str(item["created_at"])),
    )["created_at"]
    started_candidates = []
    for item in observed.values():
        completed = _parse_time(str(item["created_at"]))
        started_candidates.append(
            completed
            - timedelta(seconds=float(item["traffic"]["actual_duration_seconds"]))
        )
    started_at = min(started_candidates).isoformat()
    payload = {
        "kind": "workchord-postgresql-qualification-run",
        "schema_version": 1,
        "run_id": args.run_id,
        "attempt_number": args.attempt_number,
        "created_at": utc_now_text(),
        "started_at": started_at,
        "completed_at": completed_at,
        "status": "passed",
        "release_fingerprint": release["fingerprint"],
        "release_manifest_sha256": release["document_sha256"],
        "seed_manifest_sha256": seed["document_sha256"],
        "capacity_contract_sha256": contract_sha256(),
        "results": sorted(refs, key=lambda item: (item["profile"], item["phase"])),
        "resilience_sha256": resilience["document_sha256"],
        "ci_evidence_sha256": ci["document_sha256"],
        "gates": {
            "all_required_phases": "passed",
            "all_load_gates": "passed",
            "traffic_conformance": "passed",
            "resilience": "passed",
            "restore": "passed",
            "domain_integrity": "passed",
            "capacity_horizon": "passed",
            "final_ci_matrix": "passed",
        },
    }
    _validate_run_bundle(payload, release)
    document = atomic_write_json(args.output, payload)
    print(
        f"Qualification run status=passed attempt={args.attempt_number} "
        f"sha256={document['document_sha256']}"
    )
    return 0


def _parse_time(value: str):
    from datetime import datetime

    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise QualificationInputError("Qualification timestamps must include timezone")
    return parsed


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and SHA256_PATTERN.fullmatch(value) is not None


def _validate_run_bundle(
    document: Mapping[str, Any],
    release: Mapping[str, Any],
) -> None:
    attempt_number = document.get("attempt_number")
    if (
        document.get("kind") != "workchord-postgresql-qualification-run"
        or document.get("schema_version") != 1
        or document.get("status") != "passed"
        or not isinstance(attempt_number, int)
        or isinstance(attempt_number, bool)
        or attempt_number < 1
        or len(str(document.get("run_id", ""))) < 8
    ):
        raise QualificationInputError("Qualification run bundle identity is invalid")
    if (
        document.get("release_fingerprint") != release.get("fingerprint")
        or document.get("release_manifest_sha256")
        != release.get("document_sha256")
        or document.get("seed_manifest_sha256")
        != release.get("seed_manifest_sha256")
        or document.get("capacity_contract_sha256") != contract_sha256()
    ):
        raise QualificationInputError(
            "Qualification run bundle frozen identities differ"
        )
    if not _is_sha256(document.get("resilience_sha256")) or not _is_sha256(
        document.get("ci_evidence_sha256")
    ):
        raise QualificationInputError(
            "Qualification run bundle evidence checksums are invalid"
        )

    results = document.get("results")
    if not isinstance(results, list) or len(results) != len(REQUIRED_RESULTS):
        raise QualificationInputError(
            "Qualification run bundle does not contain exactly seven results"
        )
    observed: set[tuple[str, str]] = set()
    result_run_ids: set[str] = set()
    result_checksums: set[str] = set()
    result_times = []
    for item in results:
        if not isinstance(item, Mapping):
            raise QualificationInputError(
                "Qualification run bundle result reference is invalid"
            )
        key = (str(item.get("profile", "")), str(item.get("phase", "")))
        result_run_id = str(item.get("run_id", ""))
        result_checksum = item.get("sha256")
        if (
            key not in REQUIRED_RESULTS
            or key in observed
            or len(result_run_id) < 8
            or result_run_id in result_run_ids
            or not _is_sha256(result_checksum)
            or str(result_checksum) in result_checksums
        ):
            raise QualificationInputError(
                "Qualification run bundle result set is invalid"
            )
        observed.add(key)
        result_run_ids.add(result_run_id)
        result_checksums.add(str(result_checksum))
        result_times.append(_parse_time(str(item.get("created_at", ""))))
    if observed != set(REQUIRED_RESULTS):
        raise QualificationInputError(
            "Qualification run bundle result set differs from the contract"
        )

    gates = document.get("gates")
    if not isinstance(gates, Mapping) or set(gates) != RUN_GATES or any(
        value != "passed" for value in gates.values()
    ):
        raise QualificationInputError(
            "Qualification run bundle does not pass every exact gate"
        )

    started_at = _parse_time(str(document.get("started_at", "")))
    completed_at = _parse_time(str(document.get("completed_at", "")))
    created_at = _parse_time(str(document.get("created_at", "")))
    if not started_at < completed_at <= created_at or any(
        observed_at < started_at or observed_at > completed_at
        for observed_at in result_times
    ):
        raise QualificationInputError("Qualification run bundle timing is invalid")


def _private_key(path: Path) -> Ed25519PrivateKey:
    _reject_local_signing_in_zero_human_mode()
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise QualificationInputError(
            "Signing key must not be readable or writable by group/other"
        )
    password_text = os.getenv("WORKCHORD_QUALIFICATION_SIGNING_PASSWORD")
    password = password_text.encode("utf-8") if password_text else None
    key = serialization.load_pem_private_key(path.read_bytes(), password=password)
    if not isinstance(key, Ed25519PrivateKey):
        raise QualificationInputError("Signing key must be Ed25519")
    return key


def _finalize(args: argparse.Namespace) -> int:
    _require_new_output(args.output)
    if len(args.run_bundle) != 3:
        raise QualificationInputError("Exactly three run bundles are required")
    release = read_json_object(args.release_manifest, sealed=True)
    _validate_frozen_release(release)
    bundles = [read_json_object(path, sealed=True) for path in args.run_bundle]
    for item in bundles:
        _validate_run_bundle(item, release)
    bundles.sort(key=lambda item: int(item["attempt_number"]))
    attempts = [int(item["attempt_number"]) for item in bundles]
    if attempts != list(range(attempts[0], attempts[0] + 3)):
        raise QualificationInputError(
            "Run bundle attempt numbers are not three consecutive values"
        )
    if len({item["run_id"] for item in bundles}) != 3:
        raise QualificationInputError("Qualification run IDs must be unique")
    if any(
        item["release_fingerprint"] != release.get("fingerprint")
        or item["release_manifest_sha256"] != release.get("document_sha256")
        for item in bundles
    ):
        raise QualificationInputError("Run bundle release identity differs")
    if any(
        _parse_time(item["started_at"]) >= _parse_time(item["completed_at"])
        for item in bundles
    ):
        raise QualificationInputError("Qualification run timing is invalid")
    for first, second in zip(bundles, bundles[1:]):
        if _parse_time(first["completed_at"]) > _parse_time(second["started_at"]):
            raise QualificationInputError("Consecutive qualification runs overlap")

    contract = capacity_contract()
    gates = {
        "three_consecutive_complete_runs": {
            "status": "passed",
            "evidence": attempts,
        },
        "frozen_release_identity": {
            "status": "passed",
            "evidence": release["fingerprint"],
        },
        "exact_capacity_shape": {
            "status": "passed",
            "evidence": contract["identity_claim"]["wording"],
        },
        "traffic_and_latency": {"status": "passed", "evidence": 3},
        "resource_and_growth": {"status": "passed", "evidence": 3},
        "fault_and_recovery": {"status": "passed", "evidence": 3},
        "backup_restore_rpo_rto": {"status": "passed", "evidence": 3},
        "domain_integrity": {"status": "passed", "evidence": 3},
        "final_ci_matrix": {"status": "passed", "evidence": 3},
    }
    base = {
        "kind": "workchord-postgresql-precutover-qualification",
        "schema_version": 1,
        "report_id": args.report_id,
        "created_at": utc_now_text(),
        "status": "qualified",
        "capacity_contract": {
            "id": contract["contract_id"],
            "sha256": contract_sha256(),
        },
        "capacity_claim": {
            "browser_identities": contract["identity_claim"]["browser_identities"],
            "active_browser_sessions": contract["identity_claim"][
                "active_browser_sessions"
            ],
            "concurrent_agent_clients": contract["identity_claim"][
                "concurrent_agent_clients"
            ],
            "authenticated_people_claim": contract["identity_claim"][
                "authenticated_people_claim"
            ],
        },
        "frozen_release": {
            "fingerprint": release["fingerprint"],
            "manifest_sha256": release["document_sha256"],
            "commit": release["commit"],
            "images": release["images"],
        },
        "consecutive_runs": [
            {
                "run_id": item["run_id"],
                "attempt_number": item["attempt_number"],
                "bundle_sha256": item["document_sha256"],
                "started_at": item["started_at"],
                "completed_at": item["completed_at"],
            }
            for item in bundles
        ],
        "qualification_gates": gates,
        "attestation": ATTESTATION,
    }
    key = _private_key(args.signing_key)
    public = key.public_key()
    public_pem = public.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    signed_bytes = canonical_json_bytes(base)
    signature = key.sign(signed_bytes)
    base["signature"] = {
        "algorithm": "Ed25519",
        "signer": args.signer,
        "public_key_pem": public_pem.decode("ascii"),
        "public_key_sha256": sha256_bytes(public_pem),
        "signed_payload_sha256": sha256_bytes(signed_bytes),
        "value_base64": base64.b64encode(signature).decode("ascii"),
    }
    document = atomic_write_json(args.output, base)
    errors = _schema_errors(document)
    if errors:
        args.output.unlink(missing_ok=True)
        raise QualificationInputError(
            f"Qualification report schema validation failed: {'; '.join(errors)}"
        )
    try:
        _verify_report(document)
    except Exception:
        args.output.unlink(missing_ok=True)
        raise
    print(
        f"Qualification status=qualified report={args.report_id} "
        f"sha256={document['document_sha256']}"
    )
    return 0


def _verify_report(document: Mapping[str, Any]) -> None:
    _reject_local_signing_in_zero_human_mode()
    verify_document(document)
    errors = _schema_errors(document)
    if errors:
        raise QualificationInputError(
            f"Qualification report schema validation failed: {'; '.join(errors)}"
        )
    contract = capacity_contract()
    expected_claim = {
        "browser_identities": contract["identity_claim"]["browser_identities"],
        "active_browser_sessions": contract["identity_claim"][
            "active_browser_sessions"
        ],
        "concurrent_agent_clients": contract["identity_claim"][
            "concurrent_agent_clients"
        ],
        "authenticated_people_claim": contract["identity_claim"][
            "authenticated_people_claim"
        ],
    }
    if document.get("capacity_contract") != {
        "id": contract["contract_id"],
        "sha256": contract_sha256(),
    } or document.get("capacity_claim") != expected_claim:
        raise QualificationInputError(
            "Qualification report capacity contract differs from the current release"
        )

    runs = document.get("consecutive_runs")
    if not isinstance(runs, list) or len(runs) != 3:
        raise QualificationInputError(
            "Qualification report does not contain exactly three runs"
        )
    attempts = [item.get("attempt_number") for item in runs]
    if (
        any(
            not isinstance(attempt, int) or isinstance(attempt, bool)
            for attempt in attempts
        )
        or attempts != list(range(int(attempts[0]), int(attempts[0]) + 3))
        or len({item.get("run_id") for item in runs}) != 3
        or len({item.get("bundle_sha256") for item in runs}) != 3
        or any(not _is_sha256(item.get("bundle_sha256")) for item in runs)
    ):
        raise QualificationInputError(
            "Qualification report run identities are not unique and consecutive"
        )
    for item in runs:
        if _parse_time(str(item.get("started_at", ""))) >= _parse_time(
            str(item.get("completed_at", ""))
        ):
            raise QualificationInputError("Qualification report run timing is invalid")
    for first, second in zip(runs, runs[1:]):
        if _parse_time(str(first["completed_at"])) > _parse_time(
            str(second["started_at"])
        ):
            raise QualificationInputError("Qualification report runs overlap")
    if _parse_time(str(document.get("created_at", ""))) < _parse_time(
        str(runs[-1]["completed_at"])
    ):
        raise QualificationInputError(
            "Qualification report predates its final run"
        )

    gates = document.get("qualification_gates")
    if not isinstance(gates, Mapping) or set(gates) != REPORT_GATES:
        raise QualificationInputError(
            "Qualification report gate set differs from the contract"
        )
    expected_evidence: dict[str, Any] = {
        "three_consecutive_complete_runs": attempts,
        "frozen_release_identity": document["frozen_release"]["fingerprint"],
        "exact_capacity_shape": contract["identity_claim"]["wording"],
        "traffic_and_latency": 3,
        "resource_and_growth": 3,
        "fault_and_recovery": 3,
        "backup_restore_rpo_rto": 3,
        "domain_integrity": 3,
        "final_ci_matrix": 3,
    }
    if any(
        not isinstance(gates[name], Mapping)
        or gates[name].get("status") != "passed"
        or gates[name].get("evidence") != evidence
        for name, evidence in expected_evidence.items()
    ):
        raise QualificationInputError(
            "Qualification report evidence does not prove every exact gate"
        )
    if document.get("attestation") != ATTESTATION:
        raise QualificationInputError("Qualification report attestation differs")

    signature = document["signature"]
    base = dict(document)
    base.pop("document_sha256", None)
    base.pop("signature", None)
    signed_bytes = canonical_json_bytes(base)
    if sha256_bytes(signed_bytes) != signature["signed_payload_sha256"]:
        raise QualificationInputError("Signed qualification payload digest differs")
    public_pem = signature["public_key_pem"].encode("ascii")
    if sha256_bytes(public_pem) != signature["public_key_sha256"]:
        raise QualificationInputError("Qualification public key digest differs")
    public = serialization.load_pem_public_key(public_pem)
    if not isinstance(public, Ed25519PublicKey):
        raise QualificationInputError("Qualification public key is not Ed25519")
    try:
        public.verify(
            base64.b64decode(signature["value_base64"], validate=True),
            signed_bytes,
        )
    except (InvalidSignature, ValueError) as exc:
        raise QualificationInputError("Qualification signature is invalid") from exc


def _verify(args: argparse.Namespace) -> int:
    document = read_json_object(args.report)
    _verify_report(document)
    print(
        f"Qualification signature valid signer={document['signature']['signer']} "
        f"sha256={document['document_sha256']}"
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build the fail-closed PostgreSQL pre-cutover qualification."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    freeze = commands.add_parser("freeze")
    freeze.add_argument("--commit", required=True)
    freeze.add_argument("--image", action="append", required=True)
    freeze.add_argument("--configuration", type=Path, required=True)
    freeze.add_argument("--hardware-evidence", type=Path, required=True)
    freeze.add_argument("--seed-manifest", type=Path, required=True)
    freeze.add_argument("--schema-head", required=True)
    freeze.add_argument("--output", type=Path, required=True)
    freeze.set_defaults(handler=_freeze)

    bundle = commands.add_parser("bundle-run")
    bundle.add_argument("--run-id", required=True)
    bundle.add_argument("--attempt-number", type=int, required=True)
    bundle.add_argument("--release-manifest", type=Path, required=True)
    bundle.add_argument("--seed-manifest", type=Path, required=True)
    bundle.add_argument("--result", type=Path, action="append", required=True)
    bundle.add_argument("--resilience", type=Path, required=True)
    bundle.add_argument("--ci-evidence", type=Path, required=True)
    bundle.add_argument("--output", type=Path, required=True)
    bundle.set_defaults(handler=_bundle)

    finalize = commands.add_parser("finalize")
    finalize.add_argument("--report-id", default=f"qualification-{uuid4().hex}")
    finalize.add_argument("--release-manifest", type=Path, required=True)
    finalize.add_argument("--run-bundle", type=Path, action="append", required=True)
    finalize.add_argument("--signing-key", type=Path, required=True)
    finalize.add_argument("--signer", required=True)
    finalize.add_argument("--output", type=Path, required=True)
    finalize.set_defaults(handler=_finalize)

    verify = commands.add_parser("verify")
    verify.add_argument("--report", type=Path, required=True)
    verify.set_defaults(handler=_verify)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if getattr(args, "attempt_number", 1) < 1:
            raise QualificationInputError("Attempt number must be positive")
        return int(args.handler(args))
    except (QualificationInputError, OSError, ValueError) as exc:
        print(f"Qualification refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
