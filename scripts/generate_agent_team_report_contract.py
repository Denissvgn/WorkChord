#!/usr/bin/env python3
"""Generate the JSON Schema for the bounded agent-team setup report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
DEFAULT_OUTPUT = (
    REPOSITORY_ROOT
    / "docs"
    / "contracts"
    / "agent-team-setup-report-v1.schema.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the agent-team-setup-report-v1 JSON Schema.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=(
            "Output path (defaults to "
            f"{DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)})."
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero when the existing output differs.",
    )
    return parser.parse_args()


def rendered_schema() -> bytes:
    sys.path.insert(0, str(BACKEND_ROOT))
    from app.schemas.agent_team_setup import AgentTeamSetupReport

    schema = AgentTeamSetupReport.model_json_schema(
        ref_template="#/$defs/{model}",
        mode="validation",
    )
    schema["$id"] = (
        "https://workchord.local/contracts/"
        "agent-team-setup-report-v1.schema.json"
    )
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return (
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    expected = rendered_schema()
    if args.check:
        try:
            actual = output.read_bytes()
        except OSError:
            return 1
        return 0 if actual == expected else 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
