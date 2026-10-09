#!/usr/bin/env python3
"""Export only bounded public acceptance evidence, including dependency failures."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--outcome", choices=["success", "failure"], default="failure")
    args = parser.parse_args()
    try:
        from app.autonomy.acceptance_artifacts import export_artifacts
    except ImportError:
        # No receipt bytes are portable until their validators are available.
        args.output.mkdir(parents=True, exist_ok=False)
        payload = (json.dumps({"schema_version": 1, "run_outcome": "failure", "complete": False,
            "status": "export-validator-unavailable", "accepted_as_production_evidence": False},
            sort_keys=True, indent=2) + "\n").encode()
        (args.output / "failure-summary.json").write_bytes(payload)
        index = {"schema_version": 1, "receipts": [], "files": [
            {"file": "failure-summary.json", "bytes": len(payload), "sha256": sha256(payload).hexdigest()}]}
        (args.output / "candidate-checksums.json").write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")
        return 2
    result = export_artifacts(args.reports, args.output, outcome=args.outcome)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
