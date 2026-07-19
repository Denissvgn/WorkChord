#!/usr/bin/env python3
"""Bind post-run external evidence to one sealed client load result."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    QualificationInputError,
    atomic_write_json,
    read_json_object,
)
from scripts.load.result import (
    evaluate_client_gates,
    evaluate_external_gates,
    evaluate_workload_gates,
    result_status,
    validate_result,
)


def _load_reference(document: Mapping[str, Any]) -> Mapping[str, Any]:
    reference = document.get("load_result")
    if not isinstance(reference, dict):
        raise QualificationInputError(
            "External evidence is not bound to a client load result"
        )
    return reference


def finalize_result(
    client_result_path: Path,
    external_metrics_path: Path,
    integrity_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Re-evaluate every gate with evidence captured after the client run."""
    if output_path.resolve() == client_result_path.resolve():
        raise QualificationInputError(
            "Final output must not overwrite the immutable client result"
        )

    client = read_json_object(client_result_path, sealed=True)
    validate_result(client)
    if client["status"] == "dry_run":
        raise QualificationInputError("Dry-run results cannot be finalized")

    external = read_json_object(external_metrics_path, sealed=True)
    integrity = read_json_object(integrity_path, sealed=True)
    if external.get("kind") != "workchord-external-qualification-metrics":
        raise QualificationInputError("External evidence kind is not approved")
    if integrity.get("kind") != "workchord-domain-integrity-evidence":
        raise QualificationInputError("Integrity evidence kind is not approved")

    expected_reference = {
        "run_id": client["run_id"],
        "sha256": client["document_sha256"],
        "created_at": client["created_at"],
    }
    if dict(_load_reference(external)) != expected_reference:
        raise QualificationInputError("External metrics reference another load result")
    if dict(_load_reference(integrity)) != expected_reference:
        raise QualificationInputError("Integrity evidence references another load result")
    if external.get("phase") != client["traffic"]["phase"]:
        raise QualificationInputError("External evidence phase differs from the client run")

    metrics = external.get("metrics")
    if not isinstance(metrics, dict):
        raise QualificationInputError("External evidence metrics must be an object")

    payload = dict(client)
    payload.pop("document_sha256", None)
    payload["external_metrics"] = {
        **metrics,
        "_evidence": {
            "document_sha256": external["document_sha256"],
            "client_result_sha256": client["document_sha256"],
            "snapshot_sources": external.get("snapshot_sources"),
        },
    }
    payload["integrity"] = dict(integrity)
    payload["gates"] = {}
    payload["gates"].update(evaluate_client_gates(payload))
    payload["gates"].update(evaluate_workload_gates(payload))
    payload["gates"].update(evaluate_external_gates(metrics, integrity))
    payload["status"] = result_status(
        payload["gates"],
        qualification_candidate=bool(payload["qualification_candidate"]),
    )

    finalized = atomic_write_json(output_path, payload)
    validate_result(finalized)
    return finalized


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Finalize a sealed load result with post-run evidence."
    )
    parser.add_argument("--client-result", type=Path, required=True)
    parser.add_argument("--external-metrics", type=Path, required=True)
    parser.add_argument("--integrity-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = finalize_result(
            args.client_result,
            args.external_metrics,
            args.integrity_evidence,
            args.output,
        )
        print(
            f"Final load result status={result['status']} run={result['run_id']} "
            f"sha256={result['document_sha256']}"
        )
        return 0 if result["status"] == "passed" else 2
    except (QualificationInputError, OSError, ValueError) as exc:
        print(f"Load result finalization refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
