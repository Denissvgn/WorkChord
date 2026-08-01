#!/usr/bin/env python3
"""Validate the tracked model-aware routing closure inventory."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tomllib
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
DEFAULT_INVENTORY = (
    REPOSITORY_ROOT / "config" / "model-aware-routing-closeout.json"
)
EXPECTED_TASK_IDS = {
    "MAR-CON-001",
    "MAR-CON-002",
    "MAR-QA-001",
    "MAR-DATA-001",
    "MAR-DATA-002",
    "MAR-API-001",
    "MAR-API-002",
    "MAR-ROUTE-001",
    "MAR-ROUTE-002",
    "MAR-ROUTE-003",
    "MAR-RUN-001",
    "MAR-SKILL-001",
    "MAR-SKILL-002",
    "MAR-PKG-001",
    "MAR-UI-001",
    "MAR-UI-002",
    "MAR-QA-002",
    "MAR-OPS-001",
    "MAR-SETUP-001",
    "MAR-SETUP-002",
    "MAR-SETUP-003",
    "MAR-SETUP-QA-001",
    "MAR-CLOSE-001",
}
EXPECTED_GATE_IDS = {f"G{index}" for index in range(1, 14)}
EXPECTED_VERSION = "1.7.0"
MAX_RECEIPT_BYTES = 16_384


class CloseoutContractError(RuntimeError):
    """Raised when closure evidence is incomplete, stale, or overclaimed."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the model-aware routing closure inventory.",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=DEFAULT_INVENTORY,
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write a bounded local closure receipt.",
    )
    parser.add_argument(
        "--require-tracked",
        action="store_true",
        help="Require every evidence path to be present in the Git index.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CloseoutContractError(f"Cannot read JSON contract {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CloseoutContractError(f"JSON contract must be an object: {path}")
    return value


def _exact_ids(
    entries: Any,
    *,
    label: str,
    expected: set[str],
    required_status: str,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(entries, list):
        raise CloseoutContractError(f"{label} must be an array")
    normalized: list[dict[str, Any]] = []
    ids: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise CloseoutContractError(f"Every {label} entry must be an object")
        item_id = entry.get("id")
        if not isinstance(item_id, str):
            raise CloseoutContractError(f"Every {label} entry needs a string id")
        if entry.get("status") != required_status:
            raise CloseoutContractError(
                f"{item_id} must have status {required_status!r}"
            )
        evidence = entry.get("evidence")
        if (
            not isinstance(evidence, list)
            or len(evidence) < 2
            or any(not isinstance(path, str) for path in evidence)
        ):
            raise CloseoutContractError(
                f"{item_id} needs at least two evidence paths"
            )
        ids.append(item_id)
        normalized.append(entry)
    if len(ids) != len(set(ids)):
        raise CloseoutContractError(f"{label} contains duplicate ids")
    actual = set(ids)
    if actual != expected:
        raise CloseoutContractError(
            f"{label} id mismatch; missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )
    return tuple(normalized)


def _evidence_path(raw_path: str) -> Path:
    pure = PurePosixPath(raw_path)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise CloseoutContractError(f"Unsafe evidence path: {raw_path!r}")
    resolved = (REPOSITORY_ROOT / pure).resolve()
    if not resolved.is_relative_to(REPOSITORY_ROOT.resolve()):
        raise CloseoutContractError(f"Evidence escapes repository: {raw_path!r}")
    if not resolved.is_file():
        raise CloseoutContractError(f"Evidence file does not exist: {raw_path}")
    return resolved


def _require_tracked(paths: set[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", *sorted(paths)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise CloseoutContractError(
            "Evidence must be present in the Git index"
            + (f": {detail}" if detail else "")
        )


def _validate_versions(inventory: dict[str, Any]) -> dict[str, str]:
    release = inventory.get("release")
    if not isinstance(release, dict):
        raise CloseoutContractError("release must be an object")
    expected_release = {
        "agent_team_report_schema": "agent-team-setup-report-v1",
        "backend_version": EXPECTED_VERSION,
        "frontend_version": EXPECTED_VERSION,
        "model_aware_routing_feature": "model-aware-routing-v1",
        "setup_feature": "agent-team-master-v1",
    }
    if release != expected_release:
        raise CloseoutContractError(
            f"Release declaration mismatch: expected {expected_release}"
        )

    backend = tomllib.loads(
        (REPOSITORY_ROOT / "backend" / "pyproject.toml").read_text(
            encoding="utf-8"
        )
    )
    frontend = _load_json(REPOSITORY_ROOT / "frontend" / "package.json")
    if backend["project"]["version"] != EXPECTED_VERSION:
        raise CloseoutContractError("Backend package version is stale")
    if frontend.get("version") != EXPECTED_VERSION:
        raise CloseoutContractError("Frontend package version is stale")

    sys.path.insert(0, str(BACKEND_ROOT))
    from app.agent_contract import (
        AGENT_TEAM_MASTER_FEATURE,
        MODEL_AWARE_ROUTING_FEATURE,
        agent_contract_features,
    )
    from app.main import app
    from app.schemas.agent_team_setup import AGENT_TEAM_REPORT_SCHEMA_VERSION

    if app.version != EXPECTED_VERSION:
        raise CloseoutContractError("FastAPI version is stale")
    if AGENT_TEAM_REPORT_SCHEMA_VERSION != release["agent_team_report_schema"]:
        raise CloseoutContractError("Setup-report schema declaration is stale")
    off_features = agent_contract_features(
        include_skill_bundles=True,
        model_aware_routing_mode="off",
    )
    enforced_features = agent_contract_features(
        include_skill_bundles=True,
        model_aware_routing_mode="enforced",
    )
    if AGENT_TEAM_MASTER_FEATURE not in off_features:
        raise CloseoutContractError("Complete setup feature is not advertised")
    if MODEL_AWARE_ROUTING_FEATURE in off_features:
        raise CloseoutContractError("Routing feature is advertised while off")
    if MODEL_AWARE_ROUTING_FEATURE not in enforced_features:
        raise CloseoutContractError("Routing feature is absent while enforced")
    return expected_release


def _validate_master(inventory: dict[str, Any]) -> dict[str, Any]:
    declaration = inventory.get("representative_master")
    if not isinstance(declaration, dict):
        raise CloseoutContractError("representative_master must be an object")
    path_value = declaration.get("path")
    expected_digest = declaration.get("expected_digest")
    if not isinstance(path_value, str) or not isinstance(expected_digest, str):
        raise CloseoutContractError(
            "representative_master needs path and expected_digest"
        )
    path = _evidence_path(path_value)

    sys.path.insert(0, str(BACKEND_ROOT))
    from app.schemas.agent_team_setup import AgentTeamMaster

    master = AgentTeamMaster.model_validate_json(path.read_text(encoding="utf-8"))
    if master.digest() != expected_digest:
        raise CloseoutContractError("Representative master digest drifted")
    required = {"agent-team-master-v1", "model-aware-routing-v1"}
    if not required.issubset(master.required_server_features):
        raise CloseoutContractError(
            "Representative master omits required routing/setup features"
        )

    catalog = _load_json(REPOSITORY_ROOT / "agent-skills" / "catalog.json")
    packages = {
        (item["name"], item["version"]): {
            archive["sha256"] for archive in item["archives"]
        }
        for item in catalog.get("skills", [])
    }
    for member in master.all_members:
        key = (member.skill_package.name, member.skill_package.version)
        if member.skill_package.sha256 not in packages.get(key, set()):
            raise CloseoutContractError(
                f"Representative package is absent from catalog: {key}"
            )
    return {
        "digest": master.digest(),
        "member_count": len(master.all_members),
        "path": path_value,
        "topology_key": master.topology_key,
    }


def _validate_external_truth(inventory: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "deployment_acceptance": {
            "accepted": False,
            "status": "not_performed",
        },
        "provider_catalog_truth": {
            "accepted": False,
            "status": "not_performed",
        },
    }
    if inventory.get("external_validation") != expected:
        raise CloseoutContractError(
            "External validation must remain explicitly unaccepted when absent"
        )
    return expected


def validate_closeout(
    inventory_path: Path,
    *,
    require_tracked: bool,
) -> dict[str, Any]:
    inventory = _load_json(inventory_path)
    if inventory.get("schema_version") != "model-aware-routing-closeout-v1":
        raise CloseoutContractError("Unsupported closeout schema_version")
    if inventory.get("decision") != "local_implementation_complete":
        raise CloseoutContractError("Closeout decision is not locally complete")

    tasks = _exact_ids(
        inventory.get("tasks"),
        label="tasks",
        expected=EXPECTED_TASK_IDS,
        required_status="implemented",
    )
    gates = _exact_ids(
        inventory.get("release_gates"),
        label="release_gates",
        expected=EXPECTED_GATE_IDS,
        required_status="pass",
    )
    evidence_paths = {
        path
        for entry in (*tasks, *gates)
        for path in entry["evidence"]
    }
    inventory_relative = inventory_path.resolve().relative_to(
        REPOSITORY_ROOT.resolve()
    ).as_posix()
    evidence_paths.add(inventory_relative)
    for path in sorted(evidence_paths):
        _evidence_path(path)
    if require_tracked:
        _require_tracked(evidence_paths)

    release = _validate_versions(inventory)
    representative_master = _validate_master(inventory)
    external_validation = _validate_external_truth(inventory)
    canonical_inventory = json.dumps(
        inventory,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "decision": "LOCAL-IMPLEMENTATION-COMPLETE",
        "evidence_file_count": len(evidence_paths),
        "evidence_inventory_digest": sha256(canonical_inventory).hexdigest(),
        "external_validation": external_validation,
        "release": release,
        "release_gate_count": len(gates),
        "representative_master": representative_master,
        "schema_version": "model-aware-routing-closeout-receipt-v1",
        "task_count": len(tasks),
    }


def main() -> int:
    args = parse_args()
    try:
        receipt = validate_closeout(
            args.inventory.resolve(),
            require_tracked=args.require_tracked,
        )
    except (CloseoutContractError, KeyError, TypeError, ValueError) as exc:
        print(f"Model-aware routing closeout failed: {exc}", file=sys.stderr)
        return 1
    encoded = (
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if len(encoded) > MAX_RECEIPT_BYTES:
        print("Model-aware routing closeout receipt is oversized", file=sys.stderr)
        return 1
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(encoded)
    print(
        "Model-aware routing closeout passed "
        f"({receipt['task_count']} tasks, "
        f"{receipt['release_gate_count']} gates, "
        f"{receipt['evidence_file_count']} evidence files)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
