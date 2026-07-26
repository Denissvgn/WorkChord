"""Installed-resource loader for the PostgreSQL machine contract bundle."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Literal, Protocol, runtime_checkable

from pydantic import Field, model_validator

from app.autonomy.canonical import StrictContractModel, canonical_json_bytes, sha256_hex


SHA256_PATTERN = r"^[0-9a-f]{64}$"
SAFE_MEMBER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,254}$"

EXPECTED_AUT_TASKS = {
    "AUT-GOV-001", "AUT-BOOT-001", "AUT-IAM-001", "AUT-EVD-001",
    "AUT-ORCH-001", "AUT-CON-001", "AUT-QA-001", "AUT-INF-001",
    "AUT-COL-001", "AUT-SAN-001", "AUT-SEC-001", "AUT-REC-001",
    "AUT-QUAL-001", "AUT-CUT-001", "AUT-CLOSE-001", "AUT-ADV-001",
}
EXPECTED_DBC_TASKS = {
    "DBC-GOV-001", "DBC-QA-001", "DBC-ENV-001", "DBC-CAL-001",
    "DBC-SEC-001", "DBC-REC-001", "DBC-RES-001", "DBC-FREEZE-001",
    "DBC-DOC-001", "DBC-QUAL-001", "DBC-REHEARSE-001", "DBC-CUT-001",
    "DBC-HANDOFF-001", "DBC-STAB-001", "DBC-CLOSE-001", "DBC-AVAIL-001",
    "DBC-RET-001",
}
EXPECTED_DBM_TASKS = {
    "DBM-CON-001", "DBM-QA-001", "DBM-DEP-001", "DBM-CFG-001",
    "DBM-MIG-001", "DBM-MIG-002", "DBM-QA-002", "DBM-RUN-001",
    "DBM-RUN-002", "DBM-RUN-003", "DBM-PERF-001", "DBM-PERF-002",
    "DBM-WORK-001", "DBM-OBS-001", "DBM-MAINT-001", "DBM-DATA-001",
    "DBM-DATA-002", "DBM-DATA-003", "DBM-DEPLOY-001", "DBM-DEPLOY-002",
    "DBM-SEC-001", "DBM-BACKUP-001", "DBM-CUT-001", "DBM-QA-003",
    "DBM-SCALE-001", "DBM-RES-001", "DBM-DOC-001", "DBM-QUAL-001",
    "DBM-REHEARSE-001", "DBM-CUT-002", "DBM-DOC-002", "DBM-CLOSE-001",
}
EXPECTED_SOURCE_INPUTS = {
    "postgresql-source-plan-2026-07-18",
    "model-aware-routing-plan-2026-07-18",
    "postgresql-autonomous-plan-2026-07-19",
    "postgresql-capacity-contract-v1",
    "postgresql-data-lifecycle-policy-v1",
    "postgresql-load-result-v1",
    "postgresql-precutover-qualification-v1",
    "postgresql-resilience-observations-v1",
}
EXPECTED_MACHINE_MEMBERS = {
    "status-rules-v1.json",
    "autonomous-dag-v1.json",
    "postgresql-capacity-contract-v1.json",
    "postgresql-data-lifecycle-policy-v1.json",
    "postgresql-load-result-v1.schema.json",
    "postgresql-precutover-qualification-v1.schema.json",
    "postgresql-resilience-observations-v1.schema.json",
}


class ContractSourceInput(StrictContractModel):
    logical_key: str = Field(min_length=1, max_length=255)
    sha256: str = Field(pattern=SHA256_PATTERN)
    byte_length: int = Field(ge=1, le=100_000_000)
    media_type: str = Field(min_length=1, max_length=255)
    schema_version: str = Field(min_length=1, max_length=255)
    archive_requirement: Literal["charter-pinned-worm-object"]
    packaged_member: str | None = Field(default=None, pattern=SAFE_MEMBER_PATTERN)


class ContractMachineMember(StrictContractModel):
    path: str = Field(pattern=SAFE_MEMBER_PATTERN)
    sha256: str = Field(pattern=SHA256_PATTERN)
    byte_length: int = Field(ge=1, le=100_000_000)


class ContractTrace(StrictContractModel):
    aut_tasks: tuple[str, ...]
    dbc_tasks: tuple[str, ...]
    dbm_tasks: tuple[str, ...]
    gates: tuple[str, ...]
    manual_external: tuple[Literal["DBM-DOC-002", "G15"], ...]
    external_post_publication: tuple[Literal["DBM-CLOSE-001"], ...]


class PostgreSQLContractManifest(StrictContractModel):
    schema_version: Literal["workchord-postgresql-contract-manifest-v1"]
    bundle_state: Literal["implementation-seed-external-archive-required"]
    source_inputs: tuple[ContractSourceInput, ...] = Field(min_length=1, max_length=256)
    machine_members: tuple[ContractMachineMember, ...] = Field(
        min_length=1, max_length=256
    )
    trace: ContractTrace

    @model_validator(mode="after")
    def complete_unique_trace(self) -> "PostgreSQLContractManifest":
        source_keys = [item.logical_key for item in self.source_inputs]
        member_paths = [item.path for item in self.machine_members]
        if len(set(source_keys)) != len(source_keys):
            raise ValueError("Contract source logical keys must be unique")
        if len(set(member_paths)) != len(member_paths):
            raise ValueError("Contract machine member paths must be unique")
        if set(source_keys) != EXPECTED_SOURCE_INPUTS:
            raise ValueError("Contract manifest source-input set is incomplete")
        if set(member_paths) != EXPECTED_MACHINE_MEMBERS:
            raise ValueError("Contract manifest machine-member set is incomplete")
        expected_gates = {f"G{index}" for index in range(1, 16)}
        if set(self.trace.gates) != expected_gates:
            raise ValueError("Contract trace must contain G1-G15 exactly once")
        if len(set(self.trace.dbm_tasks)) != len(self.trace.dbm_tasks):
            raise ValueError("Contract DBM task trace contains duplicates")
        if len(set(self.trace.aut_tasks)) != len(self.trace.aut_tasks):
            raise ValueError("Contract AUT task trace contains duplicates")
        if len(set(self.trace.dbc_tasks)) != len(self.trace.dbc_tasks):
            raise ValueError("Contract DBC task trace contains duplicates")
        if set(self.trace.aut_tasks) != EXPECTED_AUT_TASKS:
            raise ValueError("Contract AUT task trace is incomplete")
        if set(self.trace.dbc_tasks) != EXPECTED_DBC_TASKS:
            raise ValueError("Contract DBC task trace is incomplete")
        if set(self.trace.dbm_tasks) != EXPECTED_DBM_TASKS:
            raise ValueError("Contract DBM task trace is incomplete")
        if self.trace.manual_external != ("DBM-DOC-002", "G15"):
            raise ValueError("Manual-publication boundary differs from the contract")
        if self.trace.external_post_publication != ("DBM-CLOSE-001",):
            raise ValueError("External post-publication boundary differs")
        by_path = {item.path: item for item in self.machine_members}
        for source in self.source_inputs:
            if source.packaged_member is None:
                continue
            member = by_path.get(source.packaged_member)
            if (
                member is None
                or member.sha256 != source.sha256
                or member.byte_length != source.byte_length
            ):
                raise ValueError("Packaged/source contract identity differs")
        return self


@runtime_checkable
class ImmutableContractArchive(Protocol):
    """Read exact charter-pinned immutable input bytes by logical key/digest."""

    def get_exact(self, *, logical_key: str, expected_sha256: str) -> bytes: ...


class ContractBundleError(ValueError):
    pass


@dataclass(frozen=True)
class PostgreSQLContractBundle:
    manifest: PostgreSQLContractManifest
    manifest_bytes: bytes
    manifest_digest: str
    members: dict[str, bytes]
    archive_verified: bool
    blocker_codes: tuple[str, ...]

    def member_json(self, path: str) -> object:
        try:
            payload = self.members[path]
        except KeyError as exc:
            raise ContractBundleError(f"Unknown contract member: {path}") from exc
        try:
            return json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ContractBundleError(f"Contract member is not JSON: {path}") from exc


def load_postgresql_contract_bundle(
    *,
    archive: ImmutableContractArchive | None = None,
    require_archive: bool = False,
) -> PostgreSQLContractBundle:
    """Load solely through package resources and optionally verify the WORM archive."""

    package_root = resources.files(__package__)
    try:
        raw_manifest = package_root.joinpath("contract-manifest-v1.json").read_bytes()
    except (FileNotFoundError, ModuleNotFoundError) as exc:
        raise ContractBundleError("Packaged PostgreSQL contract manifest is absent") from exc
    try:
        manifest = PostgreSQLContractManifest.model_validate_json(raw_manifest)
    except Exception as exc:
        raise ContractBundleError("Packaged PostgreSQL contract manifest is invalid") from exc
    canonical_manifest = canonical_json_bytes(manifest)
    members: dict[str, bytes] = {}
    for expected in manifest.machine_members:
        try:
            payload = package_root.joinpath(expected.path).read_bytes()
        except FileNotFoundError as exc:
            raise ContractBundleError(
                f"Packaged contract member is absent: {expected.path}"
            ) from exc
        if len(payload) != expected.byte_length:
            raise ContractBundleError(
                f"Packaged contract member length drifted: {expected.path}"
            )
        if sha256_hex(payload) != expected.sha256:
            raise ContractBundleError(
                f"Packaged contract member digest drifted: {expected.path}"
            )
        members[expected.path] = payload
    _validate_machine_semantics(manifest, members)

    blocker_codes: list[str] = []
    archive_verified = archive is not None
    if archive is None:
        blocker_codes.append("immutable-contract-archive-unavailable")
    else:
        for source in manifest.source_inputs:
            try:
                archived = archive.get_exact(
                    logical_key=source.logical_key,
                    expected_sha256=source.sha256,
                )
            except Exception as exc:
                raise ContractBundleError(
                    f"Immutable source archive unavailable: {source.logical_key}"
                ) from exc
            if len(archived) != source.byte_length or sha256_hex(archived) != source.sha256:
                raise ContractBundleError(
                    f"Immutable source archive mismatch: {source.logical_key}"
                )
            if source.packaged_member is not None:
                packaged = members.get(source.packaged_member)
                if packaged is None or packaged != archived:
                    raise ContractBundleError(
                        f"Packaged/WORM contract mismatch: {source.logical_key}"
                    )
    if require_archive and not archive_verified:
        raise ContractBundleError(
            "Charter-pinned immutable contract archive is required for execution"
        )
    return PostgreSQLContractBundle(
        manifest=manifest,
        manifest_bytes=canonical_manifest,
        manifest_digest=sha256_hex(canonical_manifest),
        members=members,
        archive_verified=archive_verified,
        blocker_codes=tuple(blocker_codes),
    )


def _validate_machine_semantics(
    manifest: PostgreSQLContractManifest,
    members: dict[str, bytes],
) -> None:
    parsed: dict[str, object] = {}
    for path, payload in members.items():
        try:
            parsed[path] = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ContractBundleError(f"Contract member is not JSON: {path}") from exc

    dag = parsed["autonomous-dag-v1.json"]
    if not isinstance(dag, dict) or dag.get("schema_version") != (
        "workchord-postgresql-autonomous-dag-template-v1"
    ):
        raise ContractBundleError("Autonomous DAG template schema differs")
    waves = dag.get("waves")
    dependencies = dag.get("dependencies")
    if not isinstance(waves, list) or not isinstance(dependencies, dict):
        raise ContractBundleError("Autonomous DAG waves/dependencies are invalid")
    wave_nodes: list[str] = []
    wave_ids: list[str] = []
    for wave in waves:
        if not isinstance(wave, dict) or not isinstance(wave.get("id"), str):
            raise ContractBundleError("Autonomous DAG wave is invalid")
        nodes = wave.get("nodes")
        if not isinstance(nodes, list) or not all(isinstance(item, str) for item in nodes):
            raise ContractBundleError("Autonomous DAG wave nodes are invalid")
        wave_ids.append(wave["id"])
        wave_nodes.extend(nodes)
    expected_nodes = set(manifest.trace.aut_tasks) | set(manifest.trace.dbc_tasks)
    if (
        len(set(wave_ids)) != len(wave_ids)
        or len(set(wave_nodes)) != len(wave_nodes)
        or set(wave_nodes) != expected_nodes
        or set(dependencies) != expected_nodes
    ):
        raise ContractBundleError("Autonomous DAG node registry is incomplete")
    for node_id, raw_dependencies in dependencies.items():
        if not isinstance(raw_dependencies, list) or not all(
            isinstance(item, str) and item in expected_nodes
            for item in raw_dependencies
        ):
            raise ContractBundleError(f"Autonomous DAG dependencies are invalid: {node_id}")
        if node_id in raw_dependencies or len(set(raw_dependencies)) != len(raw_dependencies):
            raise ContractBundleError(f"Autonomous DAG dependencies are cyclic/duplicate: {node_id}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise ContractBundleError("Autonomous DAG contains a dependency cycle")
        if node_id in visited:
            return
        visiting.add(node_id)
        for dependency in dependencies[node_id]:
            visit(dependency)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in sorted(expected_nodes):
        visit(node_id)
    if dag.get("manual_boundaries") != {
        "DBM-DOC-002": "manual_external",
        "G15": "manual_external",
        "DBM-CLOSE-001": "external_post_publication",
    }:
        raise ContractBundleError("Autonomous DAG manual boundary differs")

    status = parsed["status-rules-v1.json"]
    if not isinstance(status, dict) or status.get("waiver_policy") != "forbidden":
        raise ContractBundleError("Status rules waiver policy differs")
    task_rules = status.get("tasks")
    gate_rules = status.get("gates")
    if not isinstance(task_rules, list) or not isinstance(gate_rules, list):
        raise ContractBundleError("Status task/gate rules are invalid")
    if {item.get("id") for item in task_rules if isinstance(item, dict)} != set(
        manifest.trace.dbm_tasks
    ):
        raise ContractBundleError("Status rules DBM task registry is incomplete")
    if {item.get("id") for item in gate_rules if isinstance(item, dict)} != {
        f"G{index}" for index in range(1, 16)
    }:
        raise ContractBundleError("Status rules gate registry is incomplete")
    for rule in [*task_rules, *gate_rules]:
        if (
            not isinstance(rule, dict)
            or not isinstance(rule.get("required_evidence"), list)
            or not rule["required_evidence"]
            or len(set(rule["required_evidence"])) != len(rule["required_evidence"])
        ):
            raise ContractBundleError("Status rule evidence requirements are invalid")
