"""Command-line coordinator for signed PostgreSQL cutover evidence."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from app.database_migration.cutover import (
    CutoverEvidenceError,
    attest_documentation,
    authorize_production,
    finalize_production,
    finalize_rehearsal,
    finalize_rehearsal_series,
    seal_execution,
    verify_report,
)
from app.database_migration.manifest import ManifestError


def _trusted_dependency_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--release-manifest", type=Path, required=True)
    parser.add_argument("--qualification-report", type=Path, required=True)
    parser.add_argument("--qualification-public-key", type=Path, required=True)
    parser.add_argument("--documentation-walkthrough", type=Path, required=True)
    parser.add_argument("--documentation-public-key", type=Path, required=True)


def _signing_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--signing-key", type=Path, required=True)
    parser.add_argument("--signer", required=True)
    parser.add_argument("--output", type=Path, required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fail-closed PostgreSQL rehearsal and production-cutover evidence. "
            "This command records evidence; it never mutates a database or deployment."
        )
    )
    commands = parser.add_subparsers(dest="command", required=True)

    documentation = commands.add_parser(
        "attest-documentation",
        help="Sign an independently reviewed pre-cutover documentation walkthrough.",
    )
    documentation.add_argument("--input", type=Path, required=True)
    documentation.add_argument("--release-manifest", type=Path, required=True)
    _signing_arguments(documentation)

    seal = commands.add_parser(
        "seal-execution",
        help="Validate and checksum a reviewed C01-C13 execution record.",
    )
    seal.add_argument("--input", type=Path, required=True)
    seal.add_argument("--output", type=Path, required=True)

    rehearsal = commands.add_parser(
        "finalize-rehearsal",
        help="Sign one eligible rehearsal abort drill or full rehearsal.",
    )
    rehearsal.add_argument("--execution", type=Path, required=True)
    _trusted_dependency_arguments(rehearsal)
    _signing_arguments(rehearsal)

    series = commands.add_parser(
        "finalize-rehearsal-series",
        help="Bind one abort drill and exactly two consecutive successful rehearsals.",
    )
    series.add_argument("--abort-report", type=Path, required=True)
    series.add_argument("--rehearsal-report", type=Path, action="append", required=True)
    series.add_argument("--rehearsal-public-key", type=Path, required=True)
    _signing_arguments(series)

    authorization = commands.add_parser(
        "authorize-production",
        help="Sign a bounded production intent after every pre-cutover dependency passes.",
    )
    authorization.add_argument("--intent", type=Path, required=True)
    _trusted_dependency_arguments(authorization)
    authorization.add_argument("--rehearsal-series", type=Path, required=True)
    authorization.add_argument("--rehearsal-public-key", type=Path, required=True)
    _signing_arguments(authorization)

    production = commands.add_parser(
        "finalize-production",
        help="Sign a completed production change record after validating every gate.",
    )
    production.add_argument("--execution", type=Path, required=True)
    _trusted_dependency_arguments(production)
    production.add_argument("--rehearsal-series", type=Path, required=True)
    production.add_argument("--rehearsal-public-key", type=Path, required=True)
    production.add_argument("--authorization", type=Path, required=True)
    production.add_argument("--authorization-public-key", type=Path, required=True)
    _signing_arguments(production)

    verify = commands.add_parser(
        "verify",
        help="Verify a signed report against an independently supplied public key.",
    )
    verify.add_argument("--report", type=Path, required=True)
    verify.add_argument("--trusted-public-key", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "attest-documentation":
            document = attest_documentation(
                input_path=args.input,
                release_manifest_path=args.release_manifest,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "seal-execution":
            document = seal_execution(input_path=args.input, output_path=args.output)
        elif args.command == "finalize-rehearsal":
            document = finalize_rehearsal(
                execution_path=args.execution,
                release_manifest_path=args.release_manifest,
                qualification_report_path=args.qualification_report,
                qualification_public_key=args.qualification_public_key,
                documentation_walkthrough_path=args.documentation_walkthrough,
                documentation_public_key=args.documentation_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "finalize-rehearsal-series":
            document = finalize_rehearsal_series(
                abort_report_path=args.abort_report,
                rehearsal_report_paths=args.rehearsal_report,
                rehearsal_public_key=args.rehearsal_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "authorize-production":
            document = authorize_production(
                intent_path=args.intent,
                release_manifest_path=args.release_manifest,
                qualification_report_path=args.qualification_report,
                qualification_public_key=args.qualification_public_key,
                documentation_walkthrough_path=args.documentation_walkthrough,
                documentation_public_key=args.documentation_public_key,
                rehearsal_series_path=args.rehearsal_series,
                rehearsal_public_key=args.rehearsal_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "finalize-production":
            document = finalize_production(
                execution_path=args.execution,
                release_manifest_path=args.release_manifest,
                qualification_report_path=args.qualification_report,
                qualification_public_key=args.qualification_public_key,
                documentation_walkthrough_path=args.documentation_walkthrough,
                documentation_public_key=args.documentation_public_key,
                rehearsal_series_path=args.rehearsal_series,
                rehearsal_public_key=args.rehearsal_public_key,
                authorization_path=args.authorization,
                authorization_public_key=args.authorization_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "verify":
            checksum = verify_report(
                report_path=args.report,
                trusted_public_key=args.trusted_public_key,
            )
            print(f"Cutover report signature valid sha256={checksum}")
            return 0
        else:  # pragma: no cover - argparse enforces the command set.
            return 2
        print(
            f"Cutover evidence kind={document['kind']} "
            f"sha256={document['document_sha256']}"
        )
        return 0
    except (
        CutoverEvidenceError,
        ManifestError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        print(f"Cutover evidence refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
