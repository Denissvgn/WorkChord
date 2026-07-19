"""Fail-closed local diagnostic for the autonomous PostgreSQL start gate."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from app.autonomy.contracts.postgresql import load_postgresql_contract_bundle
from app.autonomy.preflight import evaluate_agent_preflight


def _release_fingerprint() -> str:
    try:
        value = subprocess.run(
            ["git", "rev-parse", "HEAD^{tree}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        value = ""
    if len(value) == 40 and all(char in "0123456789abcdef" for char in value):
        # The preflight contract consistently uses SHA-256 fingerprints. Bind a
        # legacy SHA-1 Git tree through a SHA-256 wrapper rather than relabeling it.
        from app.autonomy.canonical import sha256_hex

        return sha256_hex(f"git-sha1-tree:{value}")
    return "0" * 64


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the locally discoverable PostgreSQL autonomous-start inputs. "
            "This diagnostic never substitutes for the required remote-signed preflight."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for the unsigned diagnostic JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    bundle = load_postgresql_contract_bundle()
    report = evaluate_agent_preflight(
        release_fingerprint=_release_fingerprint(),
        bundle=bundle,
        charter_receipt=None,
    )
    payload = {
        "diagnostic_unsigned": True,
        "accepted_as_autonomy_evidence": False,
        "report": report.model_dump(mode="json"),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
