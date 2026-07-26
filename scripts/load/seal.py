#!/usr/bin/env python3
"""Seal a reviewed JSON evidence object with its canonical SHA-256."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    DOCUMENT_CHECKSUM_FIELD,
    QualificationInputError,
    atomic_write_json,
    read_json_object,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seal a reviewed qualification evidence JSON object."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise QualificationInputError(
                "Sealed output must not overwrite the reviewed source document"
            )
        payload = read_json_object(args.input)
        if DOCUMENT_CHECKSUM_FIELD in payload:
            raise QualificationInputError(
                "Input is already sealed; verify or copy it without resealing"
            )
        document = atomic_write_json(args.output, payload)
        print(
            f"Evidence sealed kind={document.get('kind', 'unspecified')} "
            f"sha256={document[DOCUMENT_CHECKSUM_FIELD]}"
        )
        return 0
    except (QualificationInputError, OSError) as exc:
        print(f"Evidence sealing refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
