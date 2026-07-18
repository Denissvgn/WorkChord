"""Operational SQLite-to-PostgreSQL migration command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from app.database_migration.manifest import ManifestError, write_document
from app.database_migration.source import MigrationDataError, preflight_source
from app.database_migration.transfer import (
    load_snapshot,
    reconcile_snapshot,
    record_post_copy_repairs,
    target_identifier,
)
from app.services.upgrade_service import database_configuration


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed WorkChord SQLite-to-PostgreSQL migration tooling."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    preflight = commands.add_parser(
        "preflight", help="Create and validate a read-only SQLite snapshot."
    )
    preflight.add_argument("--source", type=Path, required=True)
    preflight.add_argument("--snapshot", type=Path, required=True)
    preflight.add_argument("--writer-drain-evidence", type=Path, required=True)
    preflight.add_argument("--manifest", type=Path, required=True)

    commands.add_parser(
        "target-identity", help="Print the exact secret-free target authorization value."
    )

    load = commands.add_parser("load", help="Load a manifested snapshot into PostgreSQL.")
    load.add_argument("--snapshot", type=Path, required=True)
    load.add_argument("--manifest", type=Path, required=True)
    load.add_argument("--report", type=Path, required=True)
    load.add_argument("--authorize-target", required=True)
    load.add_argument("--capacity-evidence", type=Path)
    load.add_argument("--loader-method-evidence", type=Path)
    load.add_argument("--chunk-size", type=int, default=1000)

    repairs = commands.add_parser(
        "repairs", help="Run and record versioned post-copy repairs."
    )
    repairs.add_argument("--manifest", type=Path, required=True)
    repairs.add_argument("--report", type=Path, required=True)
    repairs.add_argument("--authorize-target", required=True)

    reconcile = commands.add_parser(
        "reconcile", help="Run raw or final cross-dialect reconciliation."
    )
    reconcile.add_argument("--snapshot", type=Path, required=True)
    reconcile.add_argument("--manifest", type=Path, required=True)
    reconcile.add_argument("--report", type=Path, required=True)
    reconcile.add_argument("--authorize-target", required=True)
    reconcile.add_argument("--phase", choices=("raw", "final"), required=True)
    reconcile.add_argument("--raw-report", type=Path)
    reconcile.add_argument("--repair-report", type=Path)

    seal = commands.add_parser(
        "seal-document",
        help="Checksum an operator evidence JSON object without exposing credentials.",
    )
    seal.add_argument("--input", type=Path, required=True)
    seal.add_argument("--output", type=Path, required=True)
    return parser


def _seal(input_path: Path, output_path: Path) -> dict[str, object]:
    try:
        value = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError("Evidence input must be a readable JSON object") from exc
    if not isinstance(value, dict):
        raise ManifestError("Evidence input root must be an object")
    value.pop("document_sha256", None)
    allowed_kinds = {
        "workchord-writer-drain-evidence",
        "workchord-target-capacity-evidence",
        "workchord-loader-method-evidence",
    }
    if value.get("kind") not in allowed_kinds:
        raise ManifestError(f"Evidence kind must be one of {sorted(allowed_kinds)}")
    return write_document(output_path, value)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "preflight":
            document = preflight_source(
                source_path=args.source,
                snapshot_path=args.snapshot,
                writer_drain_evidence_path=args.writer_drain_evidence,
                manifest_path=args.manifest,
            )
            print(
                f"Preflight passed: run={document['migration_run_id']} "
                f"manifest_sha256={document['document_sha256']}"
            )
            return 0
        if args.command == "target-identity":
            configuration = database_configuration()
            if configuration.backend != "postgresql":
                raise MigrationDataError(
                    "invalid_target_dialect", "Configured target is not PostgreSQL"
                )
            print(target_identifier(configuration))
            return 0
        if args.command == "load":
            document = load_snapshot(
                snapshot_path=args.snapshot,
                source_manifest_path=args.manifest,
                report_path=args.report,
                authorized_target=args.authorize_target,
                capacity_evidence_path=args.capacity_evidence,
                loader_method_evidence_path=args.loader_method_evidence,
                chunk_size=args.chunk_size,
            )
            print(
                f"Load status={document['status']} "
                f"report_sha256={document['document_sha256']}"
            )
            return 0
        if args.command == "repairs":
            document = record_post_copy_repairs(
                source_manifest_path=args.manifest,
                report_path=args.report,
                authorized_target=args.authorize_target,
            )
            print(
                f"Repairs recorded: transformations={len(document['transformations'])} "
                f"report_sha256={document['document_sha256']}"
            )
            return 0
        if args.command == "reconcile":
            document = reconcile_snapshot(
                snapshot_path=args.snapshot,
                source_manifest_path=args.manifest,
                report_path=args.report,
                authorized_target=args.authorize_target,
                phase=args.phase,
                raw_report_path=args.raw_report,
                repair_report_path=args.repair_report,
            )
            print(
                f"Reconciliation phase={args.phase} status={document['status']} "
                f"report_sha256={document['document_sha256']}"
            )
            return 0
        if args.command == "seal-document":
            document = _seal(args.input, args.output)
            print(f"Evidence sealed: document_sha256={document['document_sha256']}")
            return 0
    except (ManifestError, MigrationDataError) as exc:
        code = getattr(exc, "code", "invalid_manifest")
        print(f"Database migration failed [{code}]: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
