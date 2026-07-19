"""Command-line interface for PostgreSQL release publication and closeout."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from app.database_migration.closeout import (
    finalize_closeout,
    publish_postcutover_release,
    render_release_notes,
    verify_closeout_report,
)
from app.database_migration.cutover import CutoverEvidenceError
from app.database_migration.manifest import ManifestError


def _signing_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--signing-key", type=Path, required=True)
    parser.add_argument("--signer", required=True)
    parser.add_argument("--output", type=Path, required=True)


def _optional_closeout_dependencies(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument("--qualification-report", type=Path)
    parser.add_argument("--qualification-public-key", type=Path)
    parser.add_argument("--production-cutover", type=Path)
    parser.add_argument("--production-public-key", type=Path)
    parser.add_argument("--publication", type=Path)
    parser.add_argument("--publication-public-key", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fail-closed DBM-DOC-002 and DBM-CLOSE-001 evidence. This command "
            "does not mutate a database, deployment, or existing release document."
        )
    )
    commands = parser.add_subparsers(dest="command", required=True)

    publication = commands.add_parser(
        "publish-release",
        help="Sign post-cutover release facts after verifying the production chain.",
    )
    publication.add_argument("--input", type=Path, required=True)
    publication.add_argument("--repository-root", type=Path, required=True)
    publication.add_argument("--release-manifest", type=Path, required=True)
    publication.add_argument("--qualification-report", type=Path, required=True)
    publication.add_argument("--qualification-public-key", type=Path, required=True)
    publication.add_argument("--production-cutover", type=Path, required=True)
    publication.add_argument("--production-public-key", type=Path, required=True)
    _signing_arguments(publication)

    render = commands.add_parser(
        "render-release-notes",
        help="Verify a signed publication and write its immutable Markdown once.",
    )
    render.add_argument("--publication", type=Path, required=True)
    render.add_argument("--publication-public-key", type=Path, required=True)
    render.add_argument("--output", type=Path, required=True)

    closeout = commands.add_parser(
        "finalize-closeout",
        help=(
            "Sign an independently derived SHIP or NO-SHIP decision. Dependency "
            "arguments are optional only so missing production evidence can be "
            "recorded as NO-SHIP."
        ),
    )
    closeout.add_argument("--input", type=Path, required=True)
    _optional_closeout_dependencies(closeout)
    _signing_arguments(closeout)

    verify = commands.add_parser(
        "verify",
        help="Verify a signed post-cutover publication or closure decision.",
    )
    verify.add_argument("--report", type=Path, required=True)
    verify.add_argument("--trusted-public-key", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "publish-release":
            document = publish_postcutover_release(
                input_path=args.input,
                repository_root=args.repository_root,
                release_manifest_path=args.release_manifest,
                qualification_report_path=args.qualification_report,
                qualification_public_key=args.qualification_public_key,
                production_cutover_path=args.production_cutover,
                production_public_key=args.production_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "render-release-notes":
            checksum = render_release_notes(
                publication_path=args.publication,
                publication_public_key=args.publication_public_key,
                output_path=args.output,
            )
            print(f"Post-cutover release notes rendered sha256={checksum}")
            return 0
        elif args.command == "finalize-closeout":
            document = finalize_closeout(
                input_path=args.input,
                repository_root=args.repository_root,
                release_manifest_path=args.release_manifest,
                qualification_report_path=args.qualification_report,
                qualification_public_key=args.qualification_public_key,
                production_cutover_path=args.production_cutover,
                production_public_key=args.production_public_key,
                publication_path=args.publication,
                publication_public_key=args.publication_public_key,
                signing_key=args.signing_key,
                signer=args.signer,
                output_path=args.output,
            )
        elif args.command == "verify":
            checksum = verify_closeout_report(
                report_path=args.report,
                trusted_public_key=args.trusted_public_key,
            )
            print(f"PostgreSQL closeout report signature valid sha256={checksum}")
            return 0
        else:  # pragma: no cover - argparse enforces the command set.
            return 2
        print(
            f"PostgreSQL closeout evidence kind={document['kind']} "
            f"status={document['status']} sha256={document['document_sha256']}"
        )
        return 0
    except (
        CutoverEvidenceError,
        ManifestError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        print(f"PostgreSQL closeout refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
