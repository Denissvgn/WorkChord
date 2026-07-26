"""Operational database upgrade command."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from app.config import get_settings
from app.services.upgrade_service import (
    UpgradeError,
    bootstrap_database_schema,
    inspect_database,
    run_alembic_upgrade,
    run_database_repairs,
)


def _print_status(prefix: str) -> None:
    status = inspect_database()
    print(
        f"{prefix}: state={status.state}, "
        f"revision={status.current_revision or 'none'}, "
        f"head={status.head_revision}, tables={status.table_count}"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Upgrade WorkChord database schema safely.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Inspect schema state and exit without changing the database.",
    )
    mode.add_argument(
        "--schema-only",
        action="store_true",
        help="Bootstrap an empty target to head without application rows or seed repairs.",
    )
    mode.add_argument(
        "--repairs-only",
        action="store_true",
        help="Run serialized post-copy seed and compatibility repairs on a current schema.",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help=(
            "Do not create an automatic SQLite backup. This never bypasses the "
            "PostgreSQL external backup/PITR gate."
        ),
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=None,
        help="Directory for SQLite backups. Defaults to ./backups next to the DB file.",
    )
    parser.add_argument(
        "--external-backup-reference",
        default=None,
        help=(
            "Operator-provided backup/PITR recovery-point reference required before "
            "upgrading a non-empty PostgreSQL database."
        ),
    )
    parser.add_argument(
        "--no-repairs",
        action="store_true",
        help="Run migrations only; skip idempotent seed/compatibility repairs.",
    )
    parser.add_argument(
        "--no-stamp-unversioned-current",
        action="store_true",
        help="Refuse to stamp an unversioned database that already has the current table set.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the upgrade command."""
    args = build_parser().parse_args(argv)

    try:
        if args.check:
            _print_status("Database status")
            return 0

        settings = get_settings()
        if args.repairs_only:
            if settings.database_process_role != "repair":
                raise UpgradeError(
                    "--repairs-only requires DATABASE_PROCESS_ROLE=repair"
                )
            before, after = run_database_repairs()
            print(
                f"Before repairs: state={before.state}, "
                f"revision={before.current_revision or 'none'}"
            )
            print(
                f"After repairs: state={after.state}, "
                f"revision={after.current_revision or 'none'}"
            )
            return 0

        if settings.database_process_role != "migration":
            raise UpgradeError(
                "Schema mutation requires DATABASE_PROCESS_ROLE=migration"
            )
        if not args.schema_only and not args.no_repairs:
            raise UpgradeError(
                "Migration and repair are separate process roles; rerun the "
                "migration with --no-repairs, then run a repair role with "
                "--repairs-only"
            )

        if args.schema_only:
            before, backup_path, after = bootstrap_database_schema()
        else:
            before, backup_path, after = run_alembic_upgrade(
                backup=not args.skip_backup,
                backup_dir=args.backup_dir,
                stamp_unversioned_current=not args.no_stamp_unversioned_current,
                run_repairs=not args.no_repairs,
                external_backup_reference=args.external_backup_reference,
            )

        print(
            f"Before: state={before.state}, "
            f"revision={before.current_revision or 'none'}, head={before.head_revision}"
        )
        if backup_path:
            print(f"Backup: {backup_path}")
        elif args.external_backup_reference:
            print(f"External backup/PITR gate: {args.external_backup_reference}")
        else:
            print("Backup: not created")
        print(
            f"After: state={after.state}, "
            f"revision={after.current_revision or 'none'}, head={after.head_revision}"
        )
        if after.current_revision != after.head_revision:
            raise UpgradeError("Upgrade finished but database is not at Alembic head")
        return 0
    except UpgradeError as exc:
        print(f"Upgrade failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
