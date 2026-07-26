#!/usr/bin/env python3
"""Create a sealed, machine-readable baseline versus tuned load comparison."""

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
    utc_now_text,
)
from scripts.load.result import validate_result


def _delta(before: float, after: float) -> dict[str, float | None]:
    return {
        "baseline": before,
        "tuned": after,
        "absolute": after - before,
        "percent": ((after - before) / before * 100) if before else None,
    }


def _measurement_deltas(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for name in sorted(set(before) | set(after)):
        baseline = before.get(name, {}).get("latency_ms", {})
        tuned = after.get(name, {}).get("latency_ms", {})
        output[name] = {
            quantile: _delta(
                float(baseline.get(quantile, 0)),
                float(tuned.get(quantile, 0)),
            )
            for quantile in ("p50", "p95", "p99", "max")
        }
    return output


def _main(args: argparse.Namespace) -> int:
    baseline = read_json_object(args.baseline, sealed=True)
    tuned = read_json_object(args.tuned, sealed=True)
    validate_result(baseline)
    validate_result(tuned)
    baseline_shape = (
        baseline["traffic"]["profile_id"],
        baseline["traffic"]["phase"],
        baseline["traffic"]["target_duration_seconds"],
        baseline["traffic"]["target_rps"],
        baseline["traffic"]["target_virtual_users"],
    )
    tuned_shape = (
        tuned["traffic"]["profile_id"],
        tuned["traffic"]["phase"],
        tuned["traffic"]["target_duration_seconds"],
        tuned["traffic"]["target_rps"],
        tuned["traffic"]["target_virtual_users"],
    )
    if baseline_shape != tuned_shape:
        raise QualificationInputError(
            "Baseline and tuned results do not use the same workload shape"
        )
    if not args.change:
        raise QualificationInputError("At least one tuning change must be named")

    gate_transitions: dict[str, Any] = {}
    regressions: list[str] = []
    improvements: list[str] = []
    for name in sorted(set(baseline["gates"]) | set(tuned["gates"])):
        before = baseline["gates"].get(name, {}).get("status", "missing")
        after = tuned["gates"].get(name, {}).get("status", "missing")
        gate_transitions[name] = {"baseline": before, "tuned": after}
        if after in {"failed", "missing"} and before not in {"failed", "missing"}:
            regressions.append(name)
        if before in {"failed", "missing"} and after == "passed":
            improvements.append(name)

    verdict = "regressed" if regressions else (
        "improved" if improvements else "no_gate_regression"
    )
    document = atomic_write_json(
        args.output,
        {
            "kind": "workchord-postgresql-load-comparison",
            "schema_version": 1,
            "created_at": utc_now_text(),
            "verdict": verdict,
            "changes": args.change,
            "workload_shape": {
                "profile": baseline_shape[0],
                "phase": baseline_shape[1],
                "duration_seconds": baseline_shape[2],
                "target_rps": baseline_shape[3],
                "virtual_users": baseline_shape[4],
            },
            "sources": {
                "baseline": {
                    "run_id": baseline["run_id"],
                    "sha256": baseline["document_sha256"],
                    "release_fingerprint": baseline.get("release", {}).get(
                        "fingerprint"
                    ),
                },
                "tuned": {
                    "run_id": tuned["run_id"],
                    "sha256": tuned["document_sha256"],
                    "release_fingerprint": tuned.get("release", {}).get(
                        "fingerprint"
                    ),
                },
            },
            "operation_latency": _measurement_deltas(
                baseline["operations"], tuned["operations"]
            ),
            "classification_latency": _measurement_deltas(
                baseline["classifications"], tuned["classifications"]
            ),
            "gate_transitions": gate_transitions,
            "improvements": improvements,
            "regressions": regressions,
        },
    )
    print(
        f"Comparison verdict={verdict} sha256={document['document_sha256']}"
    )
    return 2 if regressions else 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two sealed load results.")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--tuned", type=Path, required=True)
    parser.add_argument("--change", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        return _main(args)
    except (QualificationInputError, OSError) as exc:
        print(f"Comparison refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
