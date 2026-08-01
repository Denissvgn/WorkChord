#!/usr/bin/env python3
"""Validate and reproducibly package WorkChord role skills."""

from __future__ import annotations

import argparse
import binascii
import ctypes
import hashlib
import io
import ipaddress
import json
import os
import re
import shutil
import stat
import struct
import sys
import tarfile
import tempfile
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator
from urllib.parse import unquote, urlsplit

try:  # POSIX advisory locks are released automatically when a process exits.
    import fcntl
except ImportError:  # pragma: no cover - exercised only on Windows
    fcntl = None  # type: ignore[assignment]

try:  # Windows fallback for the same one-byte non-blocking advisory lock.
    import msvcrt
except ImportError:  # pragma: no cover - exercised only on POSIX
    msvcrt = None  # type: ignore[assignment]


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = REPOSITORY_ROOT / "agent-skills"
CATALOG_FILENAME = "catalog.json"
CHECKSUMS_FILENAME = "checksums.json"
RELEASE_BASELINE_FILENAME = "release-baseline.json"
CATALOG_SCHEMA = "workchord-agent-skills/v1"
RELEASE_SCHEMA = "workchord-agent-skills-release/v1"
RELEASE_BASELINE_SCHEMA = "workchord-agent-skills-baseline/v2"
CATALOG_VERSION = "1.7.0"
API_CONTRACT = "workchord-agent/v1"
SERVER_COMPATIBILITY = ">=1.7.0,<2.0.0"
MODEL_AWARE_ROUTING_FEATURE = "model-aware-routing-v1"
AGENT_TEAM_MASTER_FEATURE = "agent-team-master-v1"
ARTIFACT_LICENSE = "MIT"
NORMALIZED_FILE_MODE = 0o644

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COMPATIBILITY_RE = re.compile(
    r"^>=(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*),"
    r"<(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s<>\]\[)\"']+", re.IGNORECASE)

ASSIGNED_WORK_CONTRACT_SCHEMA = "workchord-assigned-work/v1"
ASSIGNED_WORK_CONTRACT_BEGIN = (
    "<!-- BEGIN GENERATED: WORKCHORD-ASSIGNED-WORK-V1 -->"
)
ASSIGNED_WORK_CONTRACT_END = (
    "<!-- END GENERATED: WORKCHORD-ASSIGNED-WORK-V1 -->"
)
ASSIGNED_WORK_CONTRACT_DOCUMENTS = (
    "agent-skills/workchord-pm/references/api-and-mcp.md",
    "agent-skills/workchord-worker/references/api-and-mcp.md",
)


def _contract_parameters(
    required: Iterable[str] = (), optional: Iterable[str] = ()
) -> list[dict[str, Any]]:
    """Build an ordered, JSON-compatible operation-parameter declaration."""
    return [
        *({"name": name, "required": True} for name in required),
        *({"name": name, "required": False} for name in optional),
    ]


def _assigned_work_operation(
    operation_id: str,
    audience: str,
    method: str,
    path: str,
    tool: str,
    summary: str,
    *,
    body_model: str | None = None,
    body_required: Iterable[str] = (),
    body_optional: Iterable[str] = (),
    path_required: Iterable[str] = (),
    query_optional: Iterable[str] = (),
    header_required: Iterable[str] = (),
    header_optional: Iterable[str] = (),
    tool_required: Iterable[str] = (),
    tool_optional: Iterable[str] = (),
    required_feature: str | None = None,
) -> dict[str, Any]:
    """Build one canonical REST/Pydantic/MCP operation declaration."""
    body = None
    if body_model is not None:
        body = {
            "model": body_model,
            "fields": _contract_parameters(body_required, body_optional),
        }
    operation = {
        "id": operation_id,
        "audience": audience,
        "summary": summary,
        "rest": {
            "method": method,
            "path": path,
            "body": body,
            "path_parameters": _contract_parameters(path_required),
            "query_parameters": _contract_parameters(optional=query_optional),
            "header_parameters": _contract_parameters(
                header_required, header_optional
            ),
        },
        "mcp": {
            "tool": tool,
            "parameters": _contract_parameters(tool_required, tool_optional),
        },
    }
    if required_feature is not None:
        operation["required_feature"] = required_feature
    return operation


# This JSON-compatible value is the single authored operation contract. Generated
# role/integration references are projections; focused tests compare every declared
# REST/Pydantic/MCP field below with the live application surfaces.
ASSIGNED_WORK_V1_CONTRACT: dict[str, Any] = {
    "schema_version": ASSIGNED_WORK_CONTRACT_SCHEMA,
    "operations": [
        _assigned_work_operation(
            "capabilities",
            "PM/worker",
            "GET",
            "/api/agent/capabilities",
            "agent_get_capabilities",
            "Read identity, authority, limits, features, and compatibility first.",
        ),
        _assigned_work_operation(
            "agent-team-status",
            "PM/operator",
            "GET",
            "/api/agent/team-setup/status",
            "agent_get_team_setup_status",
            "Read the caller-bound topology revision, handoff, and backend-derived "
            "runtime readiness without inferring task availability.",
            query_optional=("topology_key",),
            required_feature=AGENT_TEAM_MASTER_FEATURE,
        ),
        _assigned_work_operation(
            "actor-roster",
            "PM",
            "GET",
            "/api/agent/actors",
            "agent_list_actor_roster",
            "Read enabled secret-free dispatch targets.",
            query_optional=("include_disabled",),
            tool_optional=("include_disabled",),
        ),
        _assigned_work_operation(
            "model-catalog",
            "PM",
            "GET",
            "/api/agent/model-catalog",
            "agent_list_model_catalog",
            "Read provider-neutral model capability declarations.",
            query_optional=("include_disabled",),
            tool_optional=("include_disabled",),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "routing-assessment-current",
            "PM",
            "GET",
            "/api/agent/planning/tasks/{task_id}/routing-assessment",
            "agent_get_task_routing_assessment",
            "Read the current task-version-bound routing assessment.",
            path_required=("task_id",),
            tool_required=("task_id",),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "routing-assessment-history",
            "PM",
            "GET",
            "/api/agent/planning/tasks/{task_id}/routing-assessments",
            "agent_list_task_routing_assessments",
            "Read bounded immutable assessment history newest first.",
            path_required=("task_id",),
            query_optional=("limit",),
            tool_required=("task_id",),
            tool_optional=("limit",),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "routing-assessment-create",
            "PM",
            "POST",
            "/api/agent/planning/tasks/{task_id}/routing-assessment",
            "agent_create_task_routing_assessment",
            "Append an audited assessment for the current task version.",
            body_model="TaskRoutingAssessmentCommand",
            body_required=(
                "expected_task_version",
                "band",
                "axes",
                "required_model",
                "review_mode",
                "confidence",
                "rationale",
            ),
            body_optional=("required_skill_levels", "reason_codes"),
            path_required=("task_id",),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "task_id",
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "routing-preview",
            "PM",
            "POST",
            "/api/agent/tasks/{task_id}/routing-preview",
            "agent_preview_task_routing",
            "Preview candidates without mutating task or assignment state; "
            "shadow may append bounded audit evidence.",
            body_model="AgentRoutingPreviewCreate",
            body_required=("purpose", "assessment_id", "expected_task_version"),
            body_optional=("reviewer_profile_id",),
            path_required=("task_id",),
            tool_required=("task_id", "payload"),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "assignment-list",
            "PM",
            "GET",
            "/api/agent/assignments",
            "agent_list_assignments",
            "Reconcile durable queue ownership and order.",
            query_optional=("task_id", "actor_id", "purpose", "state", "limit"),
            tool_optional=("task_id", "actor_id", "purpose", "state", "limit"),
        ),
        _assigned_work_operation(
            "assignment-create",
            "PM",
            "POST",
            "/api/agent/assignments",
            "agent_create_assignment",
            "Dispatch one task to one exact actor.",
            body_model="AgentTaskAssignmentCreate",
            body_required=("task_id", "actor_id", "expected_task_version"),
            body_optional=(
                "purpose",
                "team_member_id",
                "reviewer_profile_id",
                "queue_class",
                "queue_rank",
                "not_before",
                "reason",
                "routing_snapshot",
            ),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
        ),
        _assigned_work_operation(
            "assignment-update",
            "PM",
            "PATCH",
            "/api/agent/assignments/{assignment_id}",
            "agent_update_assignment",
            "Reassign, reorder, defer, or cancel queued work.",
            body_model="AgentTaskAssignmentUpdate",
            body_required=("expected_queue_revision",),
            body_optional=(
                "actor_id",
                "reviewer_profile_id",
                "queue_rank",
                "not_before",
                "state",
                "reason",
            ),
            path_required=("assignment_id",),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "assignment_id",
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
        ),
        _assigned_work_operation(
            "model-aware-assignment-create",
            "PM",
            "POST",
            "/api/agent/assignments",
            "agent_create_assignment",
            "Dispatch one preview-selected actor/binding with server-owned evidence.",
            body_model="ModelAwareAgentTaskAssignmentCreate",
            body_required=(
                "task_id",
                "actor_id",
                "expected_task_version",
                "purpose",
                "assessment_id",
                "model_binding_id",
                "model_binding_revision",
                "routing_preview_id",
                "routing_preview_digest",
            ),
            body_optional=(
                "team_member_id",
                "reviewer_profile_id",
                "queue_class",
                "queue_rank",
                "not_before",
                "reason",
            ),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "model-aware-assignment-update",
            "PM",
            "PATCH",
            "/api/agent/assignments/{assignment_id}",
            "agent_update_assignment",
            "Reroute queued work only through a fresh preview-bound selection.",
            body_model="ModelAwareAgentTaskAssignmentUpdate",
            body_required=(
                "expected_queue_revision",
                "assessment_id",
                "model_binding_id",
                "model_binding_revision",
                "routing_preview_id",
                "routing_preview_digest",
            ),
            body_optional=(
                "actor_id",
                "reviewer_profile_id",
                "queue_rank",
                "not_before",
                "state",
                "reason",
            ),
            path_required=("assignment_id",),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "assignment_id",
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "work-decision",
            "worker",
            "GET",
            "/api/agent/me/work",
            "agent_get_my_work",
            "Obey the authoritative resume/start/wait/no-work/attention decision.",
            query_optional=("limit", "cursor"),
            header_optional=("If-None-Match",),
            tool_optional=("limit", "cursor"),
        ),
        _assigned_work_operation(
            "complete-context",
            "worker/verifier",
            "GET",
            "/api/agent/tasks/{task_id}/context",
            "agent_get_complete_task_context",
            "Refresh the assignment-bound brief, dependencies, and timeline.",
            path_required=("task_id",),
            query_optional=("assignment_id",),
            tool_required=("task_id",),
            tool_optional=("assignment_id",),
        ),
        _assigned_work_operation(
            "my-claims",
            "worker",
            "GET",
            "/api/agent/me/claims",
            "agent_list_my_claims",
            "Re-read live ownership fences.",
        ),
        _assigned_work_operation(
            "my-runs",
            "worker",
            "GET",
            "/api/agent/me/runs",
            "agent_list_my_runs",
            "Re-read recent actor-owned attempts.",
            query_optional=("limit",),
            tool_optional=("limit",),
        ),
        _assigned_work_operation(
            "begin",
            "worker",
            "POST",
            "/api/agent/me/work/begin",
            "agent_begin_my_work",
            (
                "Atomically begin the selected assignment; the server revalidates its "
                "task, so the client sends no task ID or task version."
            ),
            body_model="AgentWorkBegin",
            body_required=("assignment_id", "queue_revision"),
            body_optional=(
                "lease_seconds",
                "trace_id",
                "model",
                "tool_name",
                "metadata",
            ),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
        ),
        _assigned_work_operation(
            "model-aware-begin",
            "worker",
            "POST",
            "/api/agent/me/work/begin",
            "agent_begin_my_work",
            "Begin only the selected binding and report the observed runtime model.",
            body_model="ModelAwareAgentWorkBegin",
            body_required=(
                "assignment_id",
                "queue_revision",
                "model_binding_id",
                "model_binding_revision",
                "resolved_model_id",
            ),
            body_optional=("lease_seconds", "trace_id", "tool_name", "metadata"),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
            required_feature=MODEL_AWARE_ROUTING_FEATURE,
        ),
        _assigned_work_operation(
            "renew",
            "worker",
            "POST",
            "/api/agent/me/work/renew",
            "agent_renew_my_work",
            "Atomically extend the current assignment fence and heartbeat.",
            body_model="AgentWorkRenew",
            body_required=(
                "assignment_id",
                "run_id",
                "claim_id",
                "claim_generation",
                "expected_task_version",
            ),
            body_optional=("lease_seconds",),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
        ),
        _assigned_work_operation(
            "task-event",
            "worker",
            "POST",
            "/api/agent/tasks/{task_id}/events",
            "agent_append_task_event",
            (
                "Append a bounded claim-fenced progress/checkpoint/blocker event; "
                "assigned workers always supply the compatibility-optional key."
            ),
            body_model="TaskEventCreate",
            body_required=("event_type",),
            body_optional=(
                "payload",
                "trace_id",
                "span_id",
                "correlation_id",
                "claim_id",
                "claim_generation",
            ),
            path_required=("task_id",),
            header_optional=("Idempotency-Key",),
            tool_required=("task_id", "payload"),
            tool_optional=("idempotency_key",),
        ),
        _assigned_work_operation(
            "run-event",
            "worker",
            "POST",
            "/api/agent/runs/{run_id}/events",
            "agent_append_run_event",
            (
                "Append a bounded running-attempt event; assignment-bound writes "
                "supply body idempotency and claim fencing."
            ),
            body_model="AgentRunEventCreate",
            body_required=("event_type",),
            body_optional=(
                "message",
                "payload",
                "trace_id",
                "span_id",
                "correlation_id",
                "idempotency_key",
                "claim_id",
                "claim_generation",
            ),
            path_required=("run_id",),
            tool_required=("run_id", "payload"),
        ),
        _assigned_work_operation(
            "discovery",
            "worker",
            "POST",
            "/api/agent/discoveries",
            "agent_report_discovery",
            "Route out-of-scope findings into claim-bound PM triage.",
            body_model="AgentDiscoveryTriageCreate",
            body_required=(
                "task_id",
                "assignment_id",
                "run_id",
                "claim_id",
                "claim_generation",
                "expected_task_version",
                "title",
                "description",
            ),
            body_optional=(
                "blocking",
                "evidence",
                "suggested_labels",
                "priority_hint",
            ),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
        ),
        _assigned_work_operation(
            "submit",
            "worker",
            "POST",
            "/api/agent/me/work/submit",
            "agent_submit_my_work",
            "Atomically attach evidence, resolve, fulfill, and release.",
            body_model="AgentWorkSubmit",
            body_required=(
                "assignment_id",
                "run_id",
                "claim_id",
                "claim_generation",
                "expected_task_version",
                "summary",
                "evidence",
            ),
            body_optional=("artifact_links", "commit_url", "pr_url"),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
        ),
        _assigned_work_operation(
            "fail",
            "worker",
            "POST",
            "/api/agent/me/work/fail",
            "agent_fail_my_work",
            "Atomically fail/cancel, release, and signal recovery.",
            body_model="AgentWorkTerminal",
            body_required=(
                "assignment_id",
                "run_id",
                "claim_id",
                "claim_generation",
                "expected_task_version",
                "status",
                "evidence",
            ),
            body_optional=("summary", "error"),
            header_required=("Idempotency-Key",),
            tool_required=("payload", "idempotency_key"),
        ),
        _assigned_work_operation(
            "review-queue",
            "verifier",
            "GET",
            "/api/agent/me/reviews",
            "agent_get_my_reviews",
            "Read the independent verification queue.",
            query_optional=("limit", "cursor"),
            tool_optional=("limit", "cursor"),
        ),
        _assigned_work_operation(
            "review-verdict",
            "verifier",
            "POST",
            "/api/agent/me/reviews/verdict",
            "agent_submit_review_verdict",
            "Record pass/reject evidence and an optional ordered rework handoff.",
            body_model="AgentReviewVerdict",
            body_required=(
                "assignment_id",
                "verdict",
                "expected_task_version",
                "evidence",
            ),
            body_optional=("reason", "rework_actor_id", "rework_queue_rank"),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
        ),
        _assigned_work_operation(
            "recovery-list",
            "PM",
            "GET",
            "/api/agent/recovery",
            "agent_list_recovery_tasks",
            "Read typed stale-ownership diagnoses and optimistic tuples.",
            query_optional=("limit", "cursor"),
            tool_optional=("limit", "cursor"),
        ),
        _assigned_work_operation(
            "recovery-requeue",
            "PM",
            "POST",
            "/api/agent/recovery/{task_id}/requeue",
            "agent_requeue_recovery",
            "Reconcile stale ownership and dispatch fresh ordered work.",
            body_model="AgentRecoveryRequeue",
            body_required=(
                "actor_id",
                "expected_task_version",
                "expected_live_assignment_ids",
                "expected_running_run_ids",
                "expected_claim_generation",
                "reason",
            ),
            body_optional=("queue_rank",),
            path_required=("task_id",),
            header_required=(
                "Idempotency-Key",
                "X-Agent-Rationale",
                "X-Correlation-ID",
            ),
            tool_required=(
                "task_id",
                "payload",
                "idempotency_key",
                "rationale",
                "correlation_id",
            ),
        ),
        _assigned_work_operation(
            "pipeline",
            "PM",
            "GET",
            "/api/agent/pipeline",
            "agent_get_pipeline",
            "Inspect definition through verification and recovery.",
        ),
        _assigned_work_operation(
            "run-detail",
            "PM",
            "GET",
            "/api/agent/runs/{run_id}",
            "agent_get_run_detail",
            "Inspect one attempt and its chronological evidence.",
            path_required=("run_id",),
            tool_required=("run_id",),
        ),
    ],
}

ROLE_METADATA: dict[str, dict[str, Any]] = {
    "workchord-pm": {
        "role": "pm",
        "version": "1.7.0",
        "required_features": [
            "agent-capabilities-v1",
            AGENT_TEAM_MASTER_FEATURE,
            "actor-roster-v1",
            "actor-task-assignments",
            "atomic-begin-submit",
            "atomic-renew-v1",
            "complete-task-context",
            "fenced-claims",
            "my-work-v1",
            "pm-control-v1",
            "snapshot-pagination-v1",
            "typed-rework-recovery",
            "agent-discovery-triage-v1",
            "verification-v1",
            "work-etag-v1",
        ],
        "required_scopes": [
            "assignments:read",
            "assignments:write",
            "planning:read",
            "planning:write",
            "recovery:read",
            "recovery:write",
            "reports:write",
            "team:read",
            "team:write",
            "tasks:read",
        ],
        "optional_scopes": [
            "events:write",
            "skills:read",
            "verification:read",
            "verification:write",
        ],
    },
    "workchord-worker": {
        "role": "worker",
        "version": "1.6.0",
        "required_features": [
            "agent-capabilities-v1",
            AGENT_TEAM_MASTER_FEATURE,
            "actor-task-assignments",
            "agent-discovery-triage-v1",
            "atomic-begin-submit",
            "atomic-renew-v1",
            "complete-task-context",
            "fenced-claims",
            "my-work-v1",
            "snapshot-pagination-v1",
            "typed-rework-recovery",
            "work-etag-v1",
        ],
        "required_scopes": [
            "assignments:read",
            "events:write",
            "runs:write",
            "triage:write",
            "work:execute",
        ],
        "optional_scopes": ["skills:read", "tasks:read"],
    },
}

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    (
        "assigned credential",
        re.compile(
            r"(?im)^\s*(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)"
            r"\s*[:=]\s*['\"]?(?!\s*(?:<[^>]+>|\$\{?[A-Z][A-Z0-9_]*\}?|"
            r"REDACTED|CHANGEME|YOUR[_-]))[^\s'\"]{12,}"
        ),
    ),
)


class SkillPackError(ValueError):
    """Raised when skill source, catalog, or archive validation fails."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _validate_relative_path(path: str, *, context: str) -> PurePosixPath:
    if not path or "\x00" in path or "\\" in path:
        raise SkillPackError(f"{context} contains an invalid path: {path!r}")
    pure = PurePosixPath(path)
    if pure.is_absolute() or path.startswith("/"):
        raise SkillPackError(f"{context} contains an absolute path: {path!r}")
    if (
        not pure.parts
        or pure.as_posix() != path
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        raise SkillPackError(f"{context} contains traversal or a non-normal path: {path!r}")
    if any(
        ":" in part
        or part.endswith((".", " "))
        or any(ord(character) < 32 for character in part)
        for part in pure.parts
    ):
        raise SkillPackError(f"{context} contains a non-portable path: {path!r}")
    return pure


def _validate_semver(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not SEMVER_RE.fullmatch(value):
        raise SkillPackError(f"{field} must be a semantic version, got {value!r}")
    return value


def _validate_compatibility(value: Any) -> str:
    if not isinstance(value, str):
        raise SkillPackError("server_compatibility must be a string")
    match = COMPATIBILITY_RE.fullmatch(value)
    if match is None:
        raise SkillPackError(
            "server_compatibility must use the supported >=x.y.z,<x.y.z form"
        )
    lower = tuple(int(part) for part in match.groups()[:3])
    upper = tuple(int(part) for part in match.groups()[3:])
    if lower >= upper:
        raise SkillPackError("server_compatibility lower bound must precede upper bound")
    return value


def _collect_role_files(role_dir: Path) -> dict[str, bytes]:
    if not role_dir.is_dir():
        raise SkillPackError(f"Missing skill directory: {role_dir}")

    files: dict[str, bytes] = {}
    stack = [role_dir]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name, reverse=True):
                entry_path = Path(entry.path)
                relative = entry_path.relative_to(role_dir).as_posix()
                _validate_relative_path(relative, context=f"skill {role_dir.name}")
                if entry.is_symlink():
                    raise SkillPackError(f"Symlinks are forbidden in skills: {relative}")
                if entry.is_dir(follow_symlinks=False):
                    if relative not in {"agents", "references"}:
                        raise SkillPackError(f"Unexpected skill directory: {relative}")
                    stack.append(entry_path)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    raise SkillPackError(f"Only regular files are allowed: {relative}")
                if not (
                    relative == "SKILL.md"
                    or relative == "agents/openai.yaml"
                    or (
                        relative.startswith("references/")
                        and relative.endswith(".md")
                        and len(PurePosixPath(relative).parts) == 2
                    )
                ):
                    raise SkillPackError(f"Unexpected skill file: {relative}")
                files[relative] = entry_path.read_bytes()

    required = {"SKILL.md", "agents/openai.yaml"}
    missing = sorted(required.difference(files))
    if missing:
        raise SkillPackError(
            f"Skill {role_dir.name} is missing required files: {', '.join(missing)}"
        )
    return dict(sorted(files.items()))


def _parse_frontmatter(skill_bytes: bytes, *, folder_name: str) -> dict[str, str]:
    try:
        text = skill_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SkillPackError(f"{folder_name}/SKILL.md must be UTF-8") from exc
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise SkillPackError(f"{folder_name}/SKILL.md must start with YAML frontmatter")
    try:
        closing_index = lines.index("---", 1)
    except ValueError as exc:
        raise SkillPackError(f"{folder_name}/SKILL.md has unclosed frontmatter") from exc

    values: dict[str, str] = {}
    for line in lines[1:closing_index]:
        if not line.strip() or ":" not in line:
            raise SkillPackError(f"Invalid frontmatter line in {folder_name}/SKILL.md: {line!r}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if key in values:
            raise SkillPackError(f"Duplicate frontmatter field {key!r} in {folder_name}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value

    if set(values) != {"name", "description"}:
        raise SkillPackError(
            f"{folder_name}/SKILL.md frontmatter must contain only name and description"
        )
    name = values["name"]
    if name != folder_name:
        raise SkillPackError(
            f"Skill folder {folder_name!r} does not match frontmatter name {name!r}"
        )
    if len(name) > 64 or not SKILL_NAME_RE.fullmatch(name):
        raise SkillPackError(f"Invalid skill name: {name!r}")
    if not values["description"]:
        raise SkillPackError(f"{folder_name}/SKILL.md description must not be empty")
    if not any(line.strip() for line in lines[closing_index + 1 :]):
        raise SkillPackError(f"{folder_name}/SKILL.md body must not be empty")
    return values


def _local_markdown_targets(text: str) -> Iterable[str]:
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        if raw_target.startswith("<") and raw_target.endswith(">"):
            raw_target = raw_target[1:-1]
        if not raw_target or raw_target.startswith("#"):
            continue
        split = urlsplit(raw_target)
        if split.scheme or split.netloc:
            continue
        target = unquote(split.path)
        if target:
            yield target


def _validate_references(folder_name: str, files: dict[str, bytes]) -> None:
    direct_references: set[str] = set()
    for source_path, content in files.items():
        if not source_path.endswith(".md"):
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SkillPackError(f"{folder_name}/{source_path} must be UTF-8") from exc
        source_parent = PurePosixPath(source_path).parent
        for target in _local_markdown_targets(text):
            target_path = _validate_relative_path(
                target, context=f"Markdown link in {folder_name}/{source_path}"
            )
            resolved_parts: list[str] = []
            for part in (*source_parent.parts, *target_path.parts):
                if part == "..":
                    if not resolved_parts:
                        raise SkillPackError(
                            f"Markdown link escapes {folder_name}: {source_path} -> {target}"
                        )
                    resolved_parts.pop()
                elif part not in {"", "."}:
                    resolved_parts.append(part)
            resolved = PurePosixPath(*resolved_parts).as_posix()
            if resolved not in files:
                raise SkillPackError(
                    f"Missing Markdown target in {folder_name}: {source_path} -> {target}"
                )
            if source_path == "SKILL.md" and resolved.startswith("references/"):
                direct_references.add(resolved)

    reference_files = {path for path in files if path.startswith("references/")}
    missing_direct_links = sorted(reference_files.difference(direct_references))
    if missing_direct_links:
        raise SkillPackError(
            f"Every reference must be linked directly from {folder_name}/SKILL.md: "
            + ", ".join(missing_direct_links)
        )


def _is_private_url(raw_url: str) -> bool:
    parsed = urlsplit(raw_url.rstrip(".,;:"))
    if parsed.username or parsed.password:
        return True
    hostname = parsed.hostname
    if not hostname:
        return False
    lowered = hostname.rstrip(".").lower()
    if lowered == "localhost" or lowered.endswith(".localhost") or lowered.endswith(".local"):
        return True
    try:
        address = ipaddress.ip_address(lowered.strip("[]"))
    except ValueError:
        return False
    return not address.is_global


def _validate_content(folder_name: str, files: dict[str, bytes]) -> None:
    for relative, content in files.items():
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SkillPackError(f"{folder_name}/{relative} must be UTF-8") from exc
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                raise SkillPackError(
                    f"Potential {label} found in {folder_name}/{relative}"
                )
        for url in URL_RE.findall(text):
            if _is_private_url(url):
                raise SkillPackError(
                    f"Private or credential-bearing URL found in {folder_name}/{relative}"
                )


def validate_role_source(role_dir: Path) -> dict[str, bytes]:
    """Validate one canonical role folder and return its ordered file bytes."""
    files = _collect_role_files(role_dir)
    _parse_frontmatter(files["SKILL.md"], folder_name=role_dir.name)
    expected_adapter = render_openai_adapter(role_dir)
    if files["agents/openai.yaml"] != expected_adapter:
        raise SkillPackError(
            f"Generated adapter drift in {role_dir.name}/agents/openai.yaml; "
            "run sync-generated"
        )
    _validate_references(role_dir.name, files)
    _validate_content(role_dir.name, files)
    return files


def _format_generated_parameters(parameters: list[dict[str, Any]]) -> str:
    if not parameters:
        return "—"
    return ", ".join(
        f"`{parameter['name']}{'!' if parameter['required'] else '?'}`"
        for parameter in parameters
    )


def _format_generated_rest(operation: dict[str, Any]) -> str:
    rest = operation["rest"]
    lines = [f"`{rest['method']} {rest['path']}`"]
    body = rest["body"]
    if body is not None:
        lines.append(
            f"body `{body['model']}`: {_format_generated_parameters(body['fields'])}"
        )
    for label, key in (
        ("path", "path_parameters"),
        ("query", "query_parameters"),
        ("header", "header_parameters"),
    ):
        parameters = rest[key]
        if parameters:
            lines.append(f"{label}: {_format_generated_parameters(parameters)}")
    return "<br>".join(lines)


def _format_generated_mcp(operation: dict[str, Any]) -> str:
    mcp = operation["mcp"]
    parameters = _format_generated_parameters(mcp["parameters"])
    if parameters == "—":
        return f"`{mcp['tool']}()`"
    return f"`{mcp['tool']}`({parameters})"


def render_assigned_work_contract_markdown() -> str:
    """Render the canonical assigned-work contract as one reusable Markdown block."""
    rows = [
        ASSIGNED_WORK_CONTRACT_BEGIN,
        "**Generated assigned-work v1 contract**",
        "",
        (
            f"Canonical schema: `{ASSIGNED_WORK_CONTRACT_SCHEMA}`. This exact block is "
            "generated by `scripts/build_agent_skills.py sync-generated`; `!` marks a "
            "required input and `?` an optional input. A feature-gated row is usable "
            "only when the live capability response advertises that exact feature "
            "and the live operation metadata matches the row. For model-aware "
            "routing, catalog, assessment, and preview rows require effective "
            "`shadow` or `enforced` mode; model-aware assignment and begin rows "
            "require effective `enforced` mode."
        ),
        "",
        "| Operation | Feature gate | Audience | REST contract | MCP contract | Semantics |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for operation in ASSIGNED_WORK_V1_CONTRACT["operations"]:
        rows.append(
            "| "
            + " | ".join(
                (
                    f"`{operation['id']}`",
                    (
                        f"`{operation['required_feature']}`"
                        if operation.get("required_feature")
                        else "—"
                    ),
                    operation["audience"],
                    _format_generated_rest(operation),
                    _format_generated_mcp(operation),
                    operation["summary"],
                )
            )
            + " |"
        )
    rows.extend(
        (
            "",
            (
                "Begin invariant: send `assignment_id` and `queue_revision`, not "
                "`task_id`, `expected_task_version`, or any other client task-version "
                "field. The server revalidates the selected assignment and its current "
                "task version atomically."
            ),
            ASSIGNED_WORK_CONTRACT_END,
        )
    )
    return "\n".join(rows)


def _generated_contract_block(text: str, *, context: str) -> str:
    if text.count(ASSIGNED_WORK_CONTRACT_BEGIN) != 1 or text.count(
        ASSIGNED_WORK_CONTRACT_END
    ) != 1:
        raise SkillPackError(
            f"{context} must contain exactly one assigned-work generated block"
        )
    start = text.index(ASSIGNED_WORK_CONTRACT_BEGIN)
    end_marker = text.find(ASSIGNED_WORK_CONTRACT_END, start)
    if end_marker < 0:
        raise SkillPackError(f"{context} has reversed assigned-work block markers")
    end = end_marker + len(ASSIGNED_WORK_CONTRACT_END)
    return text[start:end]


def _replace_generated_contract_block(text: str, *, context: str) -> str:
    current = _generated_contract_block(text, context=context)
    return text.replace(current, render_assigned_work_contract_markdown(), 1)


def render_openai_adapter(role_dir: Path) -> bytes:
    """Derive deterministic optional UI metadata from one portable SKILL.md."""
    skill_path = role_dir / "SKILL.md"
    try:
        skill_bytes = skill_path.read_bytes()
    except OSError as exc:
        raise SkillPackError(f"Cannot read {skill_path}") from exc
    frontmatter = _parse_frontmatter(skill_bytes, folder_name=role_dir.name)
    text = skill_bytes.decode("utf-8")
    title_matches = [
        line.removeprefix("# ").strip()
        for line in text.splitlines()
        if line.startswith("# ")
    ]
    if len(title_matches) != 1 or not title_matches[0]:
        raise SkillPackError(f"{role_dir.name}/SKILL.md must contain exactly one H1 title")
    title = title_matches[0]
    short_description = frontmatter["description"].split(".", 1)[0].strip()
    if len(short_description) > 64:
        words: list[str] = []
        for word in short_description.split():
            candidate = " ".join((*words, word))
            if len(candidate) > 61:
                break
            words.append(word)
        short_description = " ".join(words) + "..."
    if not 25 <= len(short_description) <= 64:
        raise SkillPackError(
            f"Derived short_description for {role_dir.name} must be 25-64 characters"
        )
    default_prompt = (
        f"Use ${frontmatter['name']} to follow the {title} workflow for this work."
    )
    values = {
        "display_name": title,
        "short_description": short_description,
        "default_prompt": default_prompt,
    }
    lines = ["interface:"]
    lines.extend(
        f"  {key}: {json.dumps(value, ensure_ascii=False)}"
        for key, value in values.items()
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def sync_generated_skill_sources(
    repository_root: Path = REPOSITORY_ROOT,
    skills_dir: Path = DEFAULT_SKILLS_DIR,
) -> list[Path]:
    """Synchronize shared references and optional adapters from canonical sources."""
    updated: list[Path] = []
    for relative in ASSIGNED_WORK_CONTRACT_DOCUMENTS:
        path = repository_root / relative
        try:
            current = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise SkillPackError(f"Cannot read generated-contract target {path}") from exc
        rendered = _replace_generated_contract_block(current, context=relative)
        if rendered != current:
            path.write_text(rendered, encoding="utf-8")
            updated.append(path)
    for role_name in sorted(ROLE_METADATA):
        role_dir = skills_dir / role_name
        path = role_dir / "agents" / "openai.yaml"
        rendered = render_openai_adapter(role_dir)
        try:
            current = path.read_bytes()
        except OSError as exc:
            raise SkillPackError(f"Cannot read generated adapter {path}") from exc
        if rendered != current:
            path.write_bytes(rendered)
            updated.append(path)
    return updated


def validate_generated_skill_sources(
    repository_root: Path = REPOSITORY_ROOT,
    skills_dir: Path = DEFAULT_SKILLS_DIR,
) -> None:
    """Fail when generated role/manual blocks or adapters drift from their sources."""
    expected_block = render_assigned_work_contract_markdown()
    observed_blocks: list[str] = []
    for relative in ASSIGNED_WORK_CONTRACT_DOCUMENTS:
        path = repository_root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise SkillPackError(f"Cannot read generated-contract target {path}") from exc
        observed = _generated_contract_block(text, context=relative)
        observed_blocks.append(observed)
        if observed != expected_block:
            raise SkillPackError(
                f"Assigned-work contract drift in {relative}; run sync-generated"
            )
    if len(set(observed_blocks)) != 1:
        raise SkillPackError("Assigned-work role/manual generated blocks have diverged")
    for role_name in sorted(ROLE_METADATA):
        role_dir = skills_dir / role_name
        path = role_dir / "agents" / "openai.yaml"
        try:
            observed = path.read_bytes()
        except OSError as exc:
            raise SkillPackError(f"Cannot read generated adapter {path}") from exc
        if observed != render_openai_adapter(role_dir):
            raise SkillPackError(
                f"Generated adapter drift in {role_name}/agents/openai.yaml; "
                "run sync-generated"
            )


def _zip_bytes(folder_name: str, files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for relative, content in sorted(files.items()):
            info = zipfile.ZipInfo(
                filename=f"{folder_name}/{relative}",
                date_time=(1980, 1, 1, 0, 0, 0),
            )
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFREG | NORMALIZED_FILE_MODE) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, content, compress_type=zipfile.ZIP_STORED)
    return output.getvalue()


def _deterministic_gzip(data: bytes) -> bytes:
    """Return a gzip stream whose stored DEFLATE blocks do not depend on zlib."""
    output = bytearray(b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff")
    chunks = [data[index : index + 65535] for index in range(0, len(data), 65535)]
    if not chunks:
        chunks = [b""]
    for index, chunk in enumerate(chunks):
        output.append(1 if index == len(chunks) - 1 else 0)
        length = len(chunk)
        output.extend(struct.pack("<HH", length, length ^ 0xFFFF))
        output.extend(chunk)
    output.extend(struct.pack("<II", binascii.crc32(data) & 0xFFFFFFFF, len(data) & 0xFFFFFFFF))
    return bytes(output)


def _tar_gz_bytes(folder_name: str, files: dict[str, bytes]) -> bytes:
    raw_tar = io.BytesIO()
    with tarfile.open(fileobj=raw_tar, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for relative, content in sorted(files.items()):
            info = tarfile.TarInfo(name=f"{folder_name}/{relative}")
            info.size = len(content)
            info.mode = NORMALIZED_FILE_MODE
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(content))
    return _deterministic_gzip(raw_tar.getvalue())


def _archive_records(
    folder_name: str, version: str, files: dict[str, bytes]
) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    archive_bytes = {
        f"{folder_name}-{version}.tar.gz": _tar_gz_bytes(folder_name, files),
        f"{folder_name}-{version}.zip": _zip_bytes(folder_name, files),
    }
    records = [
        {
            "format": "tar.gz" if path.endswith(".tar.gz") else "zip",
            "path": path,
            "sha256": _sha256(content),
            "size": len(content),
        }
        for path, content in sorted(archive_bytes.items())
    ]
    return records, archive_bytes


def generate_catalog(skills_dir: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Generate the canonical catalog and reproducible role archive bytes."""
    if not skills_dir.is_dir():
        raise SkillPackError(f"Missing skills directory: {skills_dir}")
    actual_roles: list[str] = []
    with os.scandir(skills_dir) as entries:
        for entry in entries:
            if entry.is_symlink():
                raise SkillPackError(f"Symlinks are forbidden in agent-skills: {entry.name}")
            if entry.is_dir(follow_symlinks=False):
                actual_roles.append(entry.name)
            elif entry.is_file(follow_symlinks=False):
                if entry.name not in {CATALOG_FILENAME, RELEASE_BASELINE_FILENAME}:
                    raise SkillPackError(f"Unexpected top-level skill-pack file: {entry.name}")
            else:
                raise SkillPackError(f"Unsupported top-level skill-pack entry: {entry.name}")
    actual_roles.sort()
    expected_roles = sorted(ROLE_METADATA)
    if actual_roles != expected_roles:
        raise SkillPackError(
            f"Skill folders must be exactly {expected_roles}; found {actual_roles}"
        )

    skills: list[dict[str, Any]] = []
    all_archives: dict[str, bytes] = {}
    for folder_name in expected_roles:
        metadata = ROLE_METADATA[folder_name]
        version = _validate_semver(metadata["version"], field=f"{folder_name}.version")
        files = validate_role_source(skills_dir / folder_name)
        file_records = [
            {"path": path, "sha256": _sha256(content), "size": len(content)}
            for path, content in files.items()
        ]
        archives, archive_bytes = _archive_records(folder_name, version, files)
        all_archives.update(archive_bytes)
        skills.append(
            {
                "name": folder_name,
                "role": metadata["role"],
                "version": version,
                "path": folder_name,
                "entrypoint": "SKILL.md",
                "license": ARTIFACT_LICENSE,
                "api_contract": API_CONTRACT,
                "server_compatibility": SERVER_COMPATIBILITY,
                "required_features": sorted(metadata["required_features"]),
                "required_scopes": sorted(metadata["required_scopes"]),
                "optional_scopes": sorted(metadata["optional_scopes"]),
                "files": file_records,
                "archives": archives,
            }
        )

    source_tree = [
        {
            "name": skill["name"],
            "version": skill["version"],
            "files": skill["files"],
        }
        for skill in skills
    ]
    source_revision = f"sha256:{_sha256(_canonical_json(source_tree))}"
    catalog = {
        "schema_version": CATALOG_SCHEMA,
        "catalog_version": CATALOG_VERSION,
        "source_revision": source_revision,
        "api_contract": API_CONTRACT,
        "skills": skills,
    }
    return catalog, all_archives


def write_catalog(skills_dir: Path) -> Path:
    """Regenerate catalog.json from validated canonical skill folders."""
    catalog, _ = generate_catalog(skills_dir)
    path = skills_dir / CATALOG_FILENAME
    path.write_bytes(_canonical_json(catalog))
    return path


def _catalog_skill_files(
    catalog: dict[str, Any], folder_name: str
) -> dict[str, dict[str, Any]]:
    matches = [skill for skill in catalog.get("skills", []) if skill.get("name") == folder_name]
    if len(matches) != 1:
        raise SkillPackError(f"Catalog must contain exactly one {folder_name!r} entry")
    records = matches[0].get("files")
    if not isinstance(records, list):
        raise SkillPackError(f"Catalog files for {folder_name} must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise SkillPackError(f"Invalid file record for {folder_name}")
        path = record["path"]
        _validate_relative_path(path, context=f"catalog entry {folder_name}")
        if path in indexed:
            raise SkillPackError(f"Duplicate catalog path for {folder_name}: {path}")
        indexed[path] = record
    return indexed


def _catalog_entry_digest(skill: dict[str, Any]) -> str:
    """Return the immutable content identity for one independently versioned role."""
    return _sha256(_canonical_json(skill))


def _catalog_release_digest(catalog: dict[str, Any]) -> str:
    """Return the immutable identity shared by one catalog and plugin version."""
    return _sha256(_canonical_json(catalog))


def _load_release_baseline(skills_dir: Path) -> dict[str, Any] | None:
    """Load and strictly validate the append-only published-version baseline."""
    path = skills_dir / RELEASE_BASELINE_FILENAME
    try:
        stat_result = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(stat_result.st_mode) or not stat.S_ISREG(stat_result.st_mode):
        raise SkillPackError("Release baseline must be a regular non-symlink file")
    try:
        baseline = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise SkillPackError("Release baseline is invalid") from exc
    if not isinstance(baseline, dict) or set(baseline) != {
        "schema_version",
        "releases",
        "catalogs",
    }:
        raise SkillPackError(
            "Release baseline must contain schema_version, releases, and catalogs"
        )
    if baseline["schema_version"] != RELEASE_BASELINE_SCHEMA:
        raise SkillPackError("Release baseline schema is unsupported")
    releases = baseline["releases"]
    if not isinstance(releases, list):
        raise SkillPackError("Release baseline releases must be a list")
    seen: set[tuple[str, str]] = set()
    for record in releases:
        if not isinstance(record, dict) or set(record) != {
            "name",
            "version",
            "catalog_entry_sha256",
        }:
            raise SkillPackError("Release baseline contains an invalid record")
        name = record["name"]
        version = _validate_semver(
            record["version"], field="release_baseline.version"
        )
        digest = record["catalog_entry_sha256"]
        if name not in ROLE_METADATA or not isinstance(digest, str) or not re.fullmatch(
            r"[0-9a-f]{64}", digest
        ):
            raise SkillPackError("Release baseline contains invalid identity metadata")
        identity = (name, version)
        if identity in seen:
            raise SkillPackError(f"Duplicate release baseline identity: {name}@{version}")
        seen.add(identity)
    catalogs = baseline["catalogs"]
    if not isinstance(catalogs, list):
        raise SkillPackError("Release baseline catalogs must be a list")
    seen_catalog_versions: set[str] = set()
    for record in catalogs:
        if not isinstance(record, dict) or set(record) != {
            "version",
            "catalog_sha256",
        }:
            raise SkillPackError("Release baseline contains an invalid catalog record")
        version = _validate_semver(
            record["version"], field="release_baseline.catalog.version"
        )
        digest = record["catalog_sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise SkillPackError("Release baseline contains invalid catalog metadata")
        if version in seen_catalog_versions:
            raise SkillPackError(
                f"Duplicate release baseline catalog version: {version}"
            )
        seen_catalog_versions.add(version)
    if path.read_bytes() != _canonical_json(baseline):
        raise SkillPackError("Release baseline is not canonical deterministic JSON")
    return baseline


def _validate_release_baseline(
    skills_dir: Path,
    catalog: dict[str, Any],
    *,
    require_current: bool,
) -> None:
    """Prevent published role/version bytes from being changed in place."""
    baseline = _load_release_baseline(skills_dir)
    if baseline is None:
        if require_current:
            raise SkillPackError(
                "Missing release-baseline.json; freeze exact versions before building"
            )
        return
    indexed = {
        (record["name"], record["version"]): record
        for record in baseline["releases"]
    }
    for skill in catalog["skills"]:
        identity = (skill["name"], skill["version"])
        record = indexed.get(identity)
        if record is None:
            if require_current:
                raise SkillPackError(
                    f"Unfrozen role version {skill['name']}@{skill['version']}; "
                    "run freeze-release before building"
                )
            continue
        if record["catalog_entry_sha256"] != _catalog_entry_digest(skill):
            raise SkillPackError(
                f"Immutable published role drift for {skill['name']}@{skill['version']}; "
                "bump the role version instead of replacing released bytes"
            )
    catalog_version = catalog["catalog_version"]
    catalog_record = next(
        (
            record
            for record in baseline["catalogs"]
            if record["version"] == catalog_version
        ),
        None,
    )
    if catalog_record is None:
        if require_current:
            raise SkillPackError(
                f"Unfrozen catalog/plugin version {catalog_version}; "
                "bump the catalog version and run freeze-release"
            )
        return
    if catalog_record["catalog_sha256"] != _catalog_release_digest(catalog):
        raise SkillPackError(
            f"Immutable published catalog/plugin drift for {catalog_version}; "
            "bump the catalog version before freezing changed role bytes"
        )


def validate_catalog(
    skills_dir: Path, *, require_frozen: bool = True
) -> dict[str, Any]:
    """Validate catalog fields, file coverage, digests, and generated archive metadata."""
    if skills_dir.resolve() == DEFAULT_SKILLS_DIR.resolve():
        validate_generated_skill_sources(REPOSITORY_ROOT, skills_dir)
    catalog_path = skills_dir / CATALOG_FILENAME
    try:
        raw = catalog_path.read_bytes()
    except FileNotFoundError as exc:
        raise SkillPackError(f"Missing {catalog_path}; run the generate command") from exc
    try:
        catalog = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SkillPackError(f"Invalid JSON in {catalog_path}: {exc}") from exc
    if not isinstance(catalog, dict):
        raise SkillPackError("Catalog root must be an object")
    if catalog.get("schema_version") != CATALOG_SCHEMA:
        raise SkillPackError(f"Unsupported catalog schema: {catalog.get('schema_version')!r}")
    _validate_semver(catalog.get("catalog_version"), field="catalog_version")
    if catalog.get("api_contract") != API_CONTRACT:
        raise SkillPackError(f"Unsupported API contract: {catalog.get('api_contract')!r}")
    source_revision = catalog.get("source_revision")
    if not isinstance(source_revision, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", source_revision):
        raise SkillPackError("source_revision must be a sha256 content revision")
    if not isinstance(catalog.get("skills"), list):
        raise SkillPackError("Catalog skills must be a list")

    catalog_names: list[str] = []
    for skill in catalog["skills"]:
        if not isinstance(skill, dict):
            raise SkillPackError("Each catalog skill entry must be an object")
        name = skill.get("name")
        if not isinstance(name, str):
            raise SkillPackError("Each catalog skill must have a string name")
        catalog_names.append(name)
        if skill.get("path") != name:
            raise SkillPackError(f"Catalog path must match skill name for {name}")
        if skill.get("entrypoint") != "SKILL.md":
            raise SkillPackError(f"Unsupported entrypoint for {name}")
        if skill.get("api_contract") != API_CONTRACT:
            raise SkillPackError(f"Unsupported API contract for {name}")
        _validate_semver(skill.get("version"), field=f"{name}.version")
        _validate_compatibility(skill.get("server_compatibility"))
        files = validate_role_source(skills_dir / name)
        records = _catalog_skill_files(catalog, name)
        if set(records) != set(files):
            unlisted = sorted(set(files).difference(records))
            missing = sorted(set(records).difference(files))
            raise SkillPackError(
                f"Catalog file coverage mismatch for {name}; unlisted={unlisted}, missing={missing}"
            )
        for path, content in files.items():
            record = records[path]
            if record.get("sha256") != _sha256(content):
                raise SkillPackError(f"Digest mismatch for {name}/{path}")
            if record.get("size") != len(content):
                raise SkillPackError(f"Size mismatch for {name}/{path}")

    if len(catalog_names) != len(set(catalog_names)):
        raise SkillPackError("Catalog contains duplicate skill names")
    if sorted(catalog_names) != sorted(ROLE_METADATA):
        raise SkillPackError(
            f"Catalog skill set mismatch; expected {sorted(ROLE_METADATA)}, found {sorted(catalog_names)}"
        )

    expected, _ = generate_catalog(skills_dir)
    if catalog != expected:
        raise SkillPackError(
            "Catalog metadata or archive digests are stale; run the generate command"
        )
    if raw != _canonical_json(catalog):
        raise SkillPackError("catalog.json is not in canonical deterministic JSON form")
    _validate_release_baseline(
        skills_dir, catalog, require_current=require_frozen
    )
    return catalog


def freeze_release(skills_dir: Path) -> Path:
    """Append each current role/version identity to the immutable baseline."""
    catalog = validate_catalog(skills_dir, require_frozen=False)
    baseline = _load_release_baseline(skills_dir) or {
        "schema_version": RELEASE_BASELINE_SCHEMA,
        "releases": [],
        "catalogs": [],
    }
    indexed = {
        (record["name"], record["version"]): record
        for record in baseline["releases"]
    }
    for skill in catalog["skills"]:
        identity = (skill["name"], skill["version"])
        digest = _catalog_entry_digest(skill)
        existing = indexed.get(identity)
        if existing is not None:
            if existing["catalog_entry_sha256"] != digest:
                raise SkillPackError(
                    f"Immutable published role drift for {skill['name']}@{skill['version']}; "
                    "bump the role version before freezing"
                )
            continue
        record = {
            "name": skill["name"],
            "version": skill["version"],
            "catalog_entry_sha256": digest,
        }
        baseline["releases"].append(record)
        indexed[identity] = record
    catalog_version = catalog["catalog_version"]
    catalog_digest = _catalog_release_digest(catalog)
    indexed_catalogs = {
        record["version"]: record for record in baseline["catalogs"]
    }
    existing_catalog = indexed_catalogs.get(catalog_version)
    if existing_catalog is not None:
        if existing_catalog["catalog_sha256"] != catalog_digest:
            raise SkillPackError(
                f"Immutable published catalog/plugin drift for {catalog_version}; "
                "bump the catalog version before freezing changed role bytes"
            )
    else:
        baseline["catalogs"].append(
            {
                "version": catalog_version,
                "catalog_sha256": catalog_digest,
            }
        )
    baseline["releases"].sort(key=lambda item: (item["name"], item["version"]))
    baseline["catalogs"].sort(key=lambda item: item["version"])
    path = skills_dir / RELEASE_BASELINE_FILENAME
    path.write_bytes(_canonical_json(baseline))
    _validate_release_baseline(skills_dir, catalog, require_current=True)
    return path


def _expected_archive_members(
    catalog: dict[str, Any], folder_name: str
) -> dict[str, dict[str, Any]]:
    return {
        f"{folder_name}/{path}": record
        for path, record in _catalog_skill_files(catalog, folder_name).items()
    }


def _validate_member_names(names: Iterable[str], *, context: str) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for name in names:
        pure = _validate_relative_path(name, context=context)
        canonical = pure.as_posix()
        if canonical in seen:
            raise SkillPackError(f"Duplicate archive path: {canonical}")
        seen.add(canonical)
        normalized.append(canonical)
    return normalized


def _validated_archive_members(
    archive_name: str,
    archive_bytes: bytes,
    catalog: dict[str, Any],
    folder_name: str,
) -> dict[str, bytes]:
    """Return validated regular-file members read from one in-memory snapshot."""
    expected = _expected_archive_members(catalog, folder_name)
    observed: dict[str, bytes] = {}
    source = io.BytesIO(archive_bytes)
    if archive_name.endswith(".zip"):
        try:
            with zipfile.ZipFile(source) as archive:
                infos = archive.infolist()
                names = _validate_member_names(
                    (info.filename for info in infos), context=f"archive {archive_name}"
                )
                for info, name in zip(infos, names, strict=True):
                    mode = (info.external_attr >> 16) & 0o170000
                    if info.is_dir() or mode == stat.S_IFLNK or mode not in {0, stat.S_IFREG}:
                        raise SkillPackError(f"Archive contains a non-regular file: {name}")
                    if name not in expected:
                        raise SkillPackError(f"Archive contains an unlisted file: {name}")
                    if info.file_size != expected[name].get("size"):
                        raise SkillPackError(f"Archive size mismatch for {name}")
                    observed[name] = archive.read(info)
        except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
            raise SkillPackError(f"Invalid zip archive {archive_name}: {exc}") from exc
    elif archive_name.endswith(".tar.gz"):
        try:
            with tarfile.open(fileobj=source, mode="r:gz") as archive:
                members = archive.getmembers()
                names = _validate_member_names(
                    (member.name for member in members), context=f"archive {archive_name}"
                )
                for member, name in zip(members, names, strict=True):
                    if not member.isfile() or member.issym() or member.islnk():
                        raise SkillPackError(f"Archive contains a non-regular file: {name}")
                    if name not in expected:
                        raise SkillPackError(f"Archive contains an unlisted file: {name}")
                    if member.size != expected[name].get("size"):
                        raise SkillPackError(f"Archive size mismatch for {name}")
                    extracted = archive.extractfile(member)
                    if extracted is None:
                        raise SkillPackError(f"Cannot read archive member: {name}")
                    observed[name] = extracted.read()
        except (tarfile.TarError, OSError) as exc:
            raise SkillPackError(f"Invalid tar archive {archive_name}: {exc}") from exc
    else:
        raise SkillPackError(f"Unsupported archive format: {archive_name}")

    if set(observed) != set(expected):
        extra = sorted(set(observed).difference(expected))
        missing = sorted(set(expected).difference(observed))
        raise SkillPackError(
            f"Archive member mismatch for {folder_name}; extra={extra}, missing={missing}"
        )
    for path, content in observed.items():
        record = expected[path]
        if len(content) != record.get("size") or _sha256(content) != record.get("sha256"):
            raise SkillPackError(f"Archive digest mismatch for {path}")
    return observed


def validate_archive(
    archive_path: Path, catalog: dict[str, Any], folder_name: str
) -> None:
    """Validate an exact role archive without extracting it."""
    try:
        archive_bytes = archive_path.read_bytes()
    except OSError as exc:
        raise SkillPackError(f"Archive is unavailable: {archive_path}") from exc
    _validated_archive_members(
        archive_path.name, archive_bytes, catalog, folder_name
    )


def build_release(skills_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Build and validate deterministic role archives plus their checksum index."""
    catalog = validate_catalog(skills_dir)
    _, archives = generate_catalog(skills_dir)
    catalog_bytes = (skills_dir / CATALOG_FILENAME).read_bytes()
    artifacts: list[dict[str, Any]] = []
    for filename, content in sorted(archives.items()):
        artifacts.append(
            {"path": filename, "sha256": _sha256(content), "size": len(content)}
        )

    checksum_index = {
        "schema_version": RELEASE_SCHEMA,
        "catalog": {
            "path": CATALOG_FILENAME,
            "sha256": _sha256(catalog_bytes),
            "size": len(catalog_bytes),
        },
        "artifacts": artifacts,
    }
    expected_files = {CATALOG_FILENAME, CHECKSUMS_FILENAME, *archives}

    def populate(stage: Path) -> None:
        (stage / CATALOG_FILENAME).write_bytes(catalog_bytes)
        for filename, content in sorted(archives.items()):
            path = stage / filename
            path.write_bytes(content)
            folder_name = next(
                name for name in ROLE_METADATA if filename.startswith(f"{name}-")
            )
            validate_archive(path, catalog, folder_name)
        (stage / CHECKSUMS_FILENAME).write_bytes(_canonical_json(checksum_index))

    _replace_built_tree(output_dir, expected_files, populate)
    return checksum_index


def build_codex_plugin(skills_dir: Path, output_dir: Path) -> Path:
    """Generate a Codex plugin adapter from the canonical validated role folders."""
    catalog = validate_catalog(skills_dir)
    manifest = {
        "name": "workchord-agent-roles",
        "version": catalog["catalog_version"],
        "license": ARTIFACT_LICENSE,
        "description": "Installable WorkChord PM and worker operating roles.",
        "author": {"name": "WorkChord maintainers"},
        "skills": "./skills/",
        "interface": {
            "displayName": "WorkChord Agent Roles",
            "shortDescription": "Operate WorkChord as a PM or assigned worker.",
            "longDescription": (
                "Adds the canonical WorkChord PM controller and low-freedom "
                "worker skills generated from the versioned generic role pack."
            ),
            "developerName": "WorkChord maintainers",
            "category": "Productivity",
            "capabilities": ["Planning", "Task execution", "Verification"],
            "defaultPrompt": "Use the appropriate WorkChord role skill for this work.",
        },
    }
    role_files: dict[str, dict[str, bytes]] = {}
    expected_files = {".codex-plugin/plugin.json"}
    for skill in catalog["skills"]:
        name = skill["name"]
        files = _collect_role_files(skills_dir / skill["path"])
        expected_records = {
            record["path"]: (record["sha256"], record["size"])
            for record in skill["files"]
        }
        observed_records = {
            path: (_sha256(content), len(content)) for path, content in files.items()
        }
        if observed_records != expected_records:
            raise SkillPackError(f"Canonical role changed while building plugin: {name}")
        role_files[name] = files
        expected_files.update(f"skills/{name}/{path}" for path in files)

    def populate(stage: Path) -> None:
        manifest_dir = stage / ".codex-plugin"
        manifest_dir.mkdir()
        (manifest_dir / "plugin.json").write_bytes(_canonical_json(manifest))
        for name, files in sorted(role_files.items()):
            role_dir = stage / "skills" / name
            for relative, content in files.items():
                path = role_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

    _replace_built_tree(output_dir, expected_files, populate)
    return output_dir


def _inspect_regular_tree(root: Path) -> set[str]:
    """Return a tree inventory while rejecting links and special entries."""
    if root.is_symlink() or not root.is_dir():
        raise SkillPackError(f"Build destination must be a regular directory: {root}")
    files: set[str] = set()
    stack = [root]
    while stack:
        directory = stack.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                relative = path.relative_to(root).as_posix()
                if entry.is_symlink():
                    raise SkillPackError(f"Symlinked build entry is forbidden: {relative}")
                if entry.is_dir(follow_symlinks=False):
                    stack.append(path)
                elif entry.is_file(follow_symlinks=False):
                    files.add(relative)
                else:
                    raise SkillPackError(f"Non-regular build entry is forbidden: {relative}")
    return files


def _fsync_tree(root: Path) -> None:
    """Flush staged regular files and directories before publication."""
    directories = [root]
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as stream:
                os.fsync(stream.fileno())
        elif path.is_dir() and not path.is_symlink():
            directories.append(path)
    for directory in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        descriptor = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _rename_exchange(first: Path, second: Path) -> bool:
    """Atomically exchange two trees on Linux; return false when unavailable."""
    if sys.platform != "linux":
        return False
    rename_exchange = 2
    at_fdcwd = -100
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = getattr(libc, "renameat2", None)
    if renameat2 is None:
        return False
    result = renameat2(
        at_fdcwd,
        os.fsencode(first),
        at_fdcwd,
        os.fsencode(second),
        rename_exchange,
    )
    if result == 0:
        return True
    error = ctypes.get_errno()
    if error in {38, 22, 95}:  # ENOSYS, EINVAL, EOPNOTSUPP
        return False
    raise OSError(error, os.strerror(error))


def _replace_built_tree(
    destination: Path,
    expected_files: set[str],
    populate: Any,
) -> None:
    """Publish one validated allowlisted tree without exposing partial output."""
    parent = destination.parent
    parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink() or not parent.is_dir():
        raise SkillPackError(f"Build destination parent is unsafe: {parent}")
    if destination.exists() or destination.is_symlink():
        observed = _inspect_regular_tree(destination)
        if any((destination / path).is_symlink() for path in observed):
            raise SkillPackError("Existing build output contains a symlink")

    stage = Path(tempfile.mkdtemp(prefix=f".{destination.name}.stage-", dir=parent))
    published = False
    try:
        populate(stage)
        observed = _inspect_regular_tree(stage)
        if observed != expected_files:
            raise SkillPackError(
                "Built output inventory differs from allowlist; "
                f"extra={sorted(observed - expected_files)}, "
                f"missing={sorted(expected_files - observed)}"
            )
        _fsync_tree(stage)
        if destination.exists():
            if _rename_exchange(stage, destination):
                published = True
                shutil.rmtree(stage)
            else:
                previous = Path(
                    tempfile.mkdtemp(prefix=f".{destination.name}.previous-", dir=parent)
                )
                previous.rmdir()
                os.replace(destination, previous)
                try:
                    os.replace(stage, destination)
                    published = True
                except BaseException:
                    os.replace(previous, destination)
                    raise
                shutil.rmtree(previous)
        else:
            os.replace(stage, destination)
            published = True
        descriptor = os.open(parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        if not published and stage.exists() and not stage.is_symlink():
            shutil.rmtree(stage)


INSTALL_LOCK_FILENAME = ".workchord-agent-skills-lock.json"
INSTALL_LOCK_SCHEMA = "workchord-agent-skills-install/v1"
BACKUP_DIRNAME = ".workchord-agent-skill-backups"
MUTATION_LOCK_FILENAME = ".workchord-agent-skills-operation.lock"
TRANSACTION_FILENAME = ".workchord-agent-skills-transaction.json"
TRANSACTION_SCHEMA = "workchord-agent-skills-transaction/v1"


def _load_release(release_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate release metadata and every declared artifact checksum."""
    try:
        catalog_bytes = (release_dir / CATALOG_FILENAME).read_bytes()
        checksums_bytes = (release_dir / CHECKSUMS_FILENAME).read_bytes()
        catalog = json.loads(catalog_bytes)
        checksums = json.loads(checksums_bytes)
    except (OSError, json.JSONDecodeError) as exc:
        raise SkillPackError("Release metadata is missing or invalid") from exc
    if catalog.get("schema_version") != CATALOG_SCHEMA:
        raise SkillPackError("Release catalog schema is unsupported")
    if checksums.get("schema_version") != RELEASE_SCHEMA:
        raise SkillPackError("Release checksum schema is unsupported")
    catalog_record = checksums.get("catalog", {})
    if (
        catalog_record.get("path") != CATALOG_FILENAME
        or catalog_record.get("size") != len(catalog_bytes)
        or catalog_record.get("sha256") != _sha256(catalog_bytes)
    ):
        raise SkillPackError("Release catalog checksum does not match")
    records: dict[str, dict[str, Any]] = {}
    for record in checksums.get("artifacts", []):
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise SkillPackError("Release artifact record is invalid")
        name = _validate_relative_path(record["path"], context="release artifact")
        if len(name.parts) != 1 or record["path"] in records:
            raise SkillPackError("Release artifact path is unsafe or duplicated")
        try:
            content = (release_dir / record["path"]).read_bytes()
        except OSError as exc:
            raise SkillPackError("Release artifact is unavailable") from exc
        if record.get("size") != len(content) or record.get("sha256") != _sha256(content):
            raise SkillPackError(f"Release artifact checksum mismatch: {record['path']}")
        records[record["path"]] = record
    declared = {
        archive["path"]
        for skill in catalog.get("skills", [])
        for archive in skill.get("archives", [])
    }
    if set(records) != declared:
        raise SkillPackError("Release checksum and catalog artifact sets differ")
    return catalog, checksums


def _release_skill(
    catalog: dict[str, Any], skill_name: str, version: str
) -> dict[str, Any]:
    matches = [
        skill
        for skill in catalog.get("skills", [])
        if skill.get("name") == skill_name and skill.get("version") == version
    ]
    if len(matches) != 1:
        raise SkillPackError("Requested exact skill version is not in the release")
    return matches[0]


def _read_install_lock(destination: Path) -> dict[str, Any]:
    path = destination / INSTALL_LOCK_FILENAME
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except FileNotFoundError:
        try:
            os.stat(path, follow_symlinks=False)
        except FileNotFoundError:
            return {"schema_version": INSTALL_LOCK_SCHEMA, "installations": {}}
        except OSError as exc:
            raise SkillPackError("Installed skill lock record is unsafe") from exc
        raise SkillPackError("Installed skill lock record is unsafe")
    except OSError as exc:
        raise SkillPackError("Installed skill lock record is unsafe") from exc
    try:
        opened_stat = os.fstat(descriptor)
        try:
            path_stat = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            raise SkillPackError("Installed skill lock record changed while reading") from exc
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or not stat.S_ISREG(path_stat.st_mode)
            or opened_stat.st_dev != path_stat.st_dev
            or opened_stat.st_ino != path_stat.st_ino
        ):
            raise SkillPackError("Installed skill lock record must be a regular file")
        try:
            with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
                descriptor = -1
                payload = json.load(stream)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SkillPackError("Installed skill lock record is invalid") from exc
        try:
            final_path_stat = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            raise SkillPackError(
                "Installed skill lock record changed while reading"
            ) from exc
        if (
            not stat.S_ISREG(final_path_stat.st_mode)
            or opened_stat.st_dev != final_path_stat.st_dev
            or opened_stat.st_ino != final_path_stat.st_ino
        ):
            raise SkillPackError("Installed skill lock record changed while reading")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if (
        not isinstance(payload, dict)
        or
        payload.get("schema_version") != INSTALL_LOCK_SCHEMA
        or not isinstance(payload.get("installations"), dict)
    ):
        raise SkillPackError("Installed skill lock schema is unsupported")
    return payload


def _fsync_directory(path: Path) -> None:
    """Persist directory-entry changes where the platform exposes directory fsync."""
    if os.name != "posix":  # pragma: no cover - Windows has no directory fsync
        return
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_atomic_json(destination: Path, filename: str, payload: dict[str, Any]) -> None:
    path = destination / filename
    if path.is_symlink():
        raise SkillPackError(f"Refusing to replace symlinked metadata: {filename}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{filename}.", suffix=".tmp", dir=destination
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(destination)
    finally:
        temporary.unlink(missing_ok=True)


def _write_install_lock(destination: Path, payload: dict[str, Any]) -> None:
    _write_atomic_json(destination, INSTALL_LOCK_FILENAME, payload)


def _read_transaction(destination: Path) -> dict[str, Any] | None:
    path = destination / TRANSACTION_FILENAME
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except FileNotFoundError:
        try:
            os.stat(path, follow_symlinks=False)
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise SkillPackError("Agent skill transaction journal is unsafe") from exc
        raise SkillPackError("Agent skill transaction journal is unsafe")
    except OSError as exc:
        raise SkillPackError("Agent skill transaction journal is unsafe") from exc
    try:
        opened_stat = os.fstat(descriptor)
        try:
            path_stat = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            raise SkillPackError(
                "Agent skill transaction journal changed while reading"
            ) from exc
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or not stat.S_ISREG(path_stat.st_mode)
            or opened_stat.st_dev != path_stat.st_dev
            or opened_stat.st_ino != path_stat.st_ino
        ):
            raise SkillPackError(
                "Agent skill transaction journal must be a regular file"
            )
        try:
            with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
                descriptor = -1
                payload = json.load(stream)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SkillPackError("Agent skill transaction journal is invalid") from exc
        try:
            final_path_stat = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            raise SkillPackError(
                "Agent skill transaction journal changed while reading"
            ) from exc
        if (
            not stat.S_ISREG(final_path_stat.st_mode)
            or opened_stat.st_dev != final_path_stat.st_dev
            or opened_stat.st_ino != final_path_stat.st_ino
        ):
            raise SkillPackError(
                "Agent skill transaction journal changed while reading"
            )
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if not isinstance(payload, dict):
        raise SkillPackError("Agent skill transaction journal is invalid")
    return payload


def _write_transaction(destination: Path, payload: dict[str, Any]) -> None:
    _write_atomic_json(destination, TRANSACTION_FILENAME, payload)


def _clear_transaction(destination: Path) -> None:
    path = destination / TRANSACTION_FILENAME
    if path.is_symlink():
        raise SkillPackError("Agent skill transaction journal must not be a symlink")
    path.unlink(missing_ok=True)
    _fsync_directory(destination)


@contextmanager
def _destination_mutation_lock(
    destination: Path, *, create: bool = False
) -> Iterator[None]:
    """Hold a process-lifetime advisory lock while mutating one destination.

    The regular lock file deliberately persists. The operating system releases
    its advisory lock when a process exits, so a crash cannot leave a stale
    sentinel that permanently blocks later installers.
    """
    if create:
        destination.mkdir(parents=True, exist_ok=True)
    elif not destination.is_dir():
        raise SkillPackError(f"Skill destination does not exist: {destination}")

    lock_path = destination / MUTATION_LOCK_FILENAME
    flags = os.O_CREAT | os.O_RDWR
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise SkillPackError("Destination mutation lock is unsafe or unavailable") from exc

    lock_kind: str | None = None
    try:
        opened_stat = os.fstat(descriptor)
        try:
            path_stat = os.stat(lock_path, follow_symlinks=False)
        except OSError as exc:
            raise SkillPackError(
                "Destination mutation lock changed while it was opened"
            ) from exc
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or not stat.S_ISREG(path_stat.st_mode)
            or opened_stat.st_dev != path_stat.st_dev
            or opened_stat.st_ino != path_stat.st_ino
        ):
            raise SkillPackError("Destination mutation lock is not a regular file")
        if fcntl is not None:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise SkillPackError(
                    "Another agent skill mutation is already in progress for this destination"
                ) from exc
            lock_kind = "posix"
        elif msvcrt is not None:  # pragma: no cover - exercised only on Windows
            if os.fstat(descriptor).st_size == 0:
                os.write(descriptor, b"\0")
                os.fsync(descriptor)
            os.lseek(descriptor, 0, os.SEEK_SET)
            try:
                msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise SkillPackError(
                    "Another agent skill mutation is already in progress for this destination"
                ) from exc
            lock_kind = "windows"
        else:  # pragma: no cover - Python supports one branch on target platforms
            raise SkillPackError(
                "Cross-process destination locking is unsupported on this platform"
            )
        locked_path_stat = os.stat(lock_path, follow_symlinks=False)
        if (
            not stat.S_ISREG(locked_path_stat.st_mode)
            or opened_stat.st_dev != locked_path_stat.st_dev
            or opened_stat.st_ino != locked_path_stat.st_ino
        ):
            raise SkillPackError(
                "Destination mutation lock changed while it was acquired"
            )
        yield
    finally:
        if lock_kind == "posix":
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        elif lock_kind == "windows":  # pragma: no cover - exercised only on Windows
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
        os.close(descriptor)


def _extract_validated_archive(
    archive_path: Path,
    archive_record: dict[str, Any],
    catalog: dict[str, Any],
    skill_name: str,
    destination: Path,
) -> Path:
    """Validate and extract one immutable in-memory snapshot into staging."""
    try:
        archive_bytes = archive_path.read_bytes()
    except OSError as exc:
        raise SkillPackError(f"Release artifact is unavailable: {archive_path}") from exc
    if (
        archive_record.get("size") != len(archive_bytes)
        or archive_record.get("sha256") != _sha256(archive_bytes)
    ):
        raise SkillPackError(
            f"Release artifact checksum mismatch: {archive_path.name}"
        )
    members = _validated_archive_members(
        archive_path.name, archive_bytes, catalog, skill_name
    )
    target = destination / skill_name
    target.mkdir(parents=True)
    target_root = target.resolve()
    for member_name, content in members.items():
        member = _validate_relative_path(member_name, context="validated archive member")
        if len(member.parts) < 2 or member.parts[0] != skill_name:
            raise SkillPackError(
                f"Archive member is outside the requested skill: {member_name}"
            )
        relative = PurePosixPath(*member.parts[1:])
        output = target.joinpath(*relative.parts)
        try:
            output.resolve().relative_to(target_root)
        except ValueError as exc:
            raise SkillPackError(
                f"Archive output escapes the staging directory: {member_name}"
            ) from exc
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(content)
        output.chmod(NORMALIZED_FILE_MODE)
    return target


def _validate_installed(
    destination: Path, catalog: dict[str, Any], skill_name: str, version: str
) -> None:
    skill = _release_skill(catalog, skill_name, version)
    files = validate_role_source(destination / skill_name)
    records = {record["path"]: record for record in skill["files"]}
    if set(files) != set(records):
        raise SkillPackError("Installed skill file set does not match its lock version")
    for path, content in files.items():
        if (
            records[path].get("size") != len(content)
            or records[path].get("sha256") != _sha256(content)
        ):
            raise SkillPackError(f"Installed skill digest mismatch: {skill_name}/{path}")


def _validate_recorded_install(
    role_dir: Path, skill_name: str, file_records: Any
) -> None:
    """Validate a managed current or backup copy against its locked file hashes."""
    if not isinstance(file_records, list):
        raise SkillPackError("Installed skill lock is missing file integrity records")
    files = _collect_role_files(role_dir)
    _parse_frontmatter(files["SKILL.md"], folder_name=skill_name)
    _validate_references(skill_name, files)
    _validate_content(skill_name, files)
    records = {
        record.get("path"): record
        for record in file_records
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }
    if set(files) != set(records):
        raise SkillPackError(f"Managed {skill_name} file set does not match its lock")
    for path, content in files.items():
        record = records[path]
        if (
            record.get("size") != len(content)
            or record.get("sha256") != _sha256(content)
        ):
            raise SkillPackError(f"Managed skill digest mismatch: {skill_name}/{path}")


def _remove_managed_path(path: Path) -> None:
    """Remove one managed path without following a substituted symlink."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def _validated_backup_root(
    destination: Path, *, require_exists: bool = False
) -> Path:
    """Return the real backup directory only when it is directly contained."""
    destination_root = destination.resolve()
    backups = destination / BACKUP_DIRNAME
    if backups.is_symlink():
        raise SkillPackError("Managed rollback directory must not be a symlink")
    if backups.exists():
        if not backups.is_dir():
            raise SkillPackError("Managed rollback path is not a directory")
    elif require_exists:
        raise SkillPackError("Managed rollback directory is missing")
    if backups.resolve() != destination_root / BACKUP_DIRNAME:
        raise SkillPackError("Managed rollback directory escapes the destination")
    return backups


def _validated_backup_child(backups: Path, child_name: str) -> Path:
    """Return one non-symlink direct child of the validated backup root."""
    child = backups / child_name
    if child.is_symlink():
        raise SkillPackError("Managed rollback child path must not be a symlink")
    backup_root = backups.resolve()
    if child.parent != backups or child.resolve().parent != backup_root:
        raise SkillPackError("Managed rollback child escapes the rollback directory")
    return child


def _path_present(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _validate_role_record(path: Path, skill_name: str, record: Any) -> None:
    if not isinstance(record, dict) or not path.is_dir() or path.is_symlink():
        raise SkillPackError(f"Managed {skill_name} transaction path is invalid")
    _validate_recorded_install(path, skill_name, record.get("files"))


def _validated_stage_paths(
    destination: Path, stage_name: Any, skill_name: str
) -> tuple[Path, Path]:
    if not isinstance(stage_name, str):
        raise SkillPackError("Install transaction is missing its staging directory")
    stage_part = _validate_relative_path(stage_name, context="install transaction stage")
    if len(stage_part.parts) != 1 or not stage_name.startswith(".workchord-skill-stage-"):
        raise SkillPackError("Install transaction staging directory is unsafe")
    stage = destination / stage_name
    if stage.is_symlink() or stage.resolve().parent != destination.resolve():
        raise SkillPackError("Install transaction staging directory escapes destination")
    staged_skill = stage / skill_name
    if staged_skill.is_symlink() or staged_skill.resolve().parent != stage.resolve():
        raise SkillPackError("Install transaction staged skill is unsafe")
    return stage, staged_skill


TRANSACTION_PHASES: dict[str, set[str]] = {
    "install": {
        "prepared",
        "remove_old_backup",
        "save_current",
        "place_new",
        "filesystem_committed",
    },
    "rollback": {
        "prepared",
        "move_current_to_swap",
        "move_previous_to_target",
        "move_current_to_backup",
        "filesystem_committed",
    },
    "uninstall": {
        "prepared",
        "remove_target",
        "remove_backup",
        "filesystem_committed",
    },
}


def _validate_transaction(payload: dict[str, Any]) -> tuple[str, str]:
    if payload.get("schema_version") != TRANSACTION_SCHEMA:
        raise SkillPackError("Agent skill transaction journal schema is unsupported")
    operation = payload.get("operation")
    skill_name = payload.get("skill_name")
    phase = payload.get("phase")
    if operation not in TRANSACTION_PHASES or phase not in TRANSACTION_PHASES[operation]:
        raise SkillPackError("Agent skill transaction operation or phase is invalid")
    if not isinstance(skill_name, str) or not SKILL_NAME_RE.fullmatch(skill_name):
        raise SkillPackError("Agent skill transaction skill name is invalid")
    for field in ("before_lock", "after_lock"):
        snapshot = payload.get(field)
        if (
            not isinstance(snapshot, dict)
            or snapshot.get("schema_version") != INSTALL_LOCK_SCHEMA
            or not isinstance(snapshot.get("installations"), dict)
        ):
            raise SkillPackError(f"Agent skill transaction {field} is invalid")
    return operation, skill_name


def _set_transaction_phase(
    destination: Path, payload: dict[str, Any], phase: str
) -> None:
    operation = str(payload["operation"])
    if phase not in TRANSACTION_PHASES[operation]:
        raise SkillPackError("Agent skill transaction phase transition is invalid")
    payload["phase"] = phase
    _write_transaction(destination, payload)


def _begin_transaction(
    destination: Path,
    *,
    operation: str,
    skill_name: str,
    before_lock: dict[str, Any],
    after_lock: dict[str, Any],
    stage_name: str | None = None,
) -> dict[str, Any]:
    if _read_transaction(destination) is not None:
        raise SkillPackError("An earlier agent skill transaction must be recovered first")
    payload: dict[str, Any] = {
        "schema_version": TRANSACTION_SCHEMA,
        "operation": operation,
        "skill_name": skill_name,
        "phase": "prepared",
        "before_lock": before_lock,
        "after_lock": after_lock,
    }
    if stage_name is not None:
        payload["stage_name"] = stage_name
    _validate_transaction(payload)
    _write_transaction(destination, payload)
    return payload


def _clone_json_object(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload))


def _validate_install_final(
    destination: Path, payload: dict[str, Any], skill_name: str
) -> None:
    before_record = payload["before_lock"]["installations"].get(skill_name)
    after_record = payload["after_lock"]["installations"].get(skill_name)
    target = destination / skill_name
    backups = _validated_backup_root(destination, require_exists=True)
    backup = _validated_backup_child(backups, skill_name)
    _validate_role_record(target, skill_name, after_record)
    if before_record is None:
        if _path_present(backup):
            raise SkillPackError("Initial install unexpectedly created a rollback copy")
    else:
        _validate_role_record(backup, skill_name, before_record)


def _recover_install_transaction(
    destination: Path, payload: dict[str, Any], skill_name: str
) -> None:
    before_record = payload["before_lock"]["installations"].get(skill_name)
    after_record = payload["after_lock"]["installations"].get(skill_name)
    if not isinstance(after_record, dict):
        raise SkillPackError("Install transaction has no resulting lock record")
    target = destination / skill_name
    backups = _validated_backup_root(destination, require_exists=True)
    backup = _validated_backup_child(backups, skill_name)
    stage, staged_skill = _validated_stage_paths(
        destination, payload.get("stage_name"), skill_name
    )

    while True:
        phase = payload["phase"]
        if phase == "prepared":
            _set_transaction_phase(destination, payload, "remove_old_backup")
        elif phase == "remove_old_backup":
            if _path_present(backup):
                _remove_managed_path(backup)
                _fsync_directory(backups)
            _set_transaction_phase(destination, payload, "save_current")
        elif phase == "save_current":
            if before_record is None:
                if _path_present(target) or _path_present(backup):
                    raise SkillPackError("Initial install transaction paths are inconsistent")
            elif _path_present(target) and not _path_present(backup):
                _validate_role_record(target, skill_name, before_record)
                os.replace(target, backup)
                _fsync_directory(destination)
                _fsync_directory(backups)
            elif not _path_present(target) and _path_present(backup):
                _validate_role_record(backup, skill_name, before_record)
            else:
                raise SkillPackError("Install transaction could not save current skill")
            _set_transaction_phase(destination, payload, "place_new")
        elif phase == "place_new":
            if not _path_present(target) and _path_present(staged_skill):
                _validate_role_record(staged_skill, skill_name, after_record)
                os.replace(staged_skill, target)
                _fsync_directory(stage)
                _fsync_directory(destination)
            elif _path_present(target) and not _path_present(staged_skill):
                _validate_role_record(target, skill_name, after_record)
            else:
                raise SkillPackError("Install transaction could not place staged skill")
            _set_transaction_phase(destination, payload, "filesystem_committed")
        elif phase == "filesystem_committed":
            _validate_install_final(destination, payload, skill_name)
            _write_install_lock(destination, payload["after_lock"])
            if _path_present(stage):
                _remove_managed_path(stage)
                _fsync_directory(destination)
            _clear_transaction(destination)
            return


def _validate_rollback_final(
    destination: Path, payload: dict[str, Any], skill_name: str
) -> None:
    before_record = payload["before_lock"]["installations"].get(skill_name)
    after_record = payload["after_lock"]["installations"].get(skill_name)
    target = destination / skill_name
    backups = _validated_backup_root(destination, require_exists=True)
    backup = _validated_backup_child(backups, skill_name)
    swap = _validated_backup_child(backups, f"{skill_name}.swap")
    _validate_role_record(target, skill_name, after_record)
    _validate_role_record(backup, skill_name, before_record)
    if _path_present(swap):
        raise SkillPackError("Rollback transaction left a swap path behind")


def _recover_rollback_transaction(
    destination: Path, payload: dict[str, Any], skill_name: str
) -> None:
    before_record = payload["before_lock"]["installations"].get(skill_name)
    after_record = payload["after_lock"]["installations"].get(skill_name)
    if not isinstance(before_record, dict) or not isinstance(after_record, dict):
        raise SkillPackError("Rollback transaction lock records are incomplete")
    target = destination / skill_name
    backups = _validated_backup_root(destination, require_exists=True)
    backup = _validated_backup_child(backups, skill_name)
    swap = _validated_backup_child(backups, f"{skill_name}.swap")

    while True:
        phase = payload["phase"]
        if phase == "prepared":
            _set_transaction_phase(destination, payload, "move_current_to_swap")
        elif phase == "move_current_to_swap":
            if _path_present(target) and not _path_present(swap):
                _validate_role_record(target, skill_name, before_record)
                _validate_role_record(backup, skill_name, after_record)
                os.replace(target, swap)
                _fsync_directory(destination)
                _fsync_directory(backups)
            elif not _path_present(target) and _path_present(swap):
                _validate_role_record(swap, skill_name, before_record)
                _validate_role_record(backup, skill_name, after_record)
            else:
                raise SkillPackError("Rollback transaction current-to-swap state is invalid")
            _set_transaction_phase(destination, payload, "move_previous_to_target")
        elif phase == "move_previous_to_target":
            if not _path_present(target) and _path_present(backup):
                _validate_role_record(backup, skill_name, after_record)
                _validate_role_record(swap, skill_name, before_record)
                os.replace(backup, target)
                _fsync_directory(backups)
                _fsync_directory(destination)
            elif _path_present(target) and not _path_present(backup):
                _validate_role_record(target, skill_name, after_record)
                _validate_role_record(swap, skill_name, before_record)
            else:
                raise SkillPackError("Rollback transaction previous-to-target state is invalid")
            _set_transaction_phase(destination, payload, "move_current_to_backup")
        elif phase == "move_current_to_backup":
            if not _path_present(backup) and _path_present(swap):
                _validate_role_record(swap, skill_name, before_record)
                _validate_role_record(target, skill_name, after_record)
                os.replace(swap, backup)
                _fsync_directory(backups)
            elif _path_present(backup) and not _path_present(swap):
                _validate_role_record(backup, skill_name, before_record)
                _validate_role_record(target, skill_name, after_record)
            else:
                raise SkillPackError("Rollback transaction swap-to-backup state is invalid")
            _set_transaction_phase(destination, payload, "filesystem_committed")
        elif phase == "filesystem_committed":
            _validate_rollback_final(destination, payload, skill_name)
            _write_install_lock(destination, payload["after_lock"])
            _clear_transaction(destination)
            return


def _recover_uninstall_transaction(
    destination: Path, payload: dict[str, Any], skill_name: str
) -> None:
    target = destination / skill_name
    backups = _validated_backup_root(destination)
    backup = _validated_backup_child(backups, skill_name)
    before_record = payload["before_lock"]["installations"].get(skill_name)
    if not isinstance(before_record, dict):
        raise SkillPackError("Uninstall transaction lock record is invalid")
    previous_record = before_record.get("previous")
    if previous_record is not None and not isinstance(previous_record, dict):
        raise SkillPackError("Uninstall transaction backup record is invalid")
    while True:
        phase = payload["phase"]
        if phase == "prepared":
            _set_transaction_phase(destination, payload, "remove_target")
        elif phase == "remove_target":
            if _path_present(target):
                _validate_role_record(target, skill_name, before_record)
                _remove_managed_path(target)
                _fsync_directory(destination)
            _set_transaction_phase(destination, payload, "remove_backup")
        elif phase == "remove_backup":
            if _path_present(target):
                raise SkillPackError(
                    "Uninstall transaction target was replaced after removal"
                )
            if _path_present(backup):
                if previous_record is None:
                    raise SkillPackError(
                        "Uninstall transaction found an unmanaged rollback copy"
                    )
                _validate_role_record(backup, skill_name, previous_record)
                _remove_managed_path(backup)
                _fsync_directory(backups)
            _set_transaction_phase(destination, payload, "filesystem_committed")
        elif phase == "filesystem_committed":
            if _path_present(target) or _path_present(backup):
                raise SkillPackError("Uninstall transaction paths remain present")
            _write_install_lock(destination, payload["after_lock"])
            _clear_transaction(destination)
            return


def _recover_interrupted_transaction(destination: Path) -> None:
    payload = _read_transaction(destination)
    if payload is None:
        return
    operation, skill_name = _validate_transaction(payload)
    current_lock = _read_install_lock(destination)
    if current_lock == payload["after_lock"]:
        if operation == "install":
            _validate_install_final(destination, payload, skill_name)
            stage, _ = _validated_stage_paths(
                destination, payload.get("stage_name"), skill_name
            )
            if _path_present(stage):
                _remove_managed_path(stage)
                _fsync_directory(destination)
        elif operation == "rollback":
            _validate_rollback_final(destination, payload, skill_name)
        elif operation == "uninstall":
            target = destination / skill_name
            backups = _validated_backup_root(destination)
            backup = _validated_backup_child(backups, skill_name)
            if _path_present(target) or _path_present(backup):
                raise SkillPackError("Committed uninstall transaction is inconsistent")
        _clear_transaction(destination)
        return
    if current_lock != payload["before_lock"]:
        raise SkillPackError("Agent skill lock does not match interrupted transaction")
    if operation == "install":
        _recover_install_transaction(destination, payload, skill_name)
    elif operation == "rollback":
        _recover_rollback_transaction(destination, payload, skill_name)
    else:
        _recover_uninstall_transaction(destination, payload, skill_name)


def install_skill(
    release_dir: Path,
    destination: Path,
    skill_name: str,
    version: str,
    archive_format: str,
) -> None:
    """Atomically install or upgrade one exact skill and retain one rollback copy."""
    catalog, _ = _load_release(release_dir)
    skill = _release_skill(catalog, skill_name, version)
    archive = next(
        (item for item in skill["archives"] if item.get("format") == archive_format),
        None,
    )
    if archive is None:
        raise SkillPackError("Requested archive format is not published")
    archive_path = release_dir / archive["path"]
    with _destination_mutation_lock(destination, create=True):
        _recover_interrupted_transaction(destination)
        lock = _read_install_lock(destination)
        old_record = lock["installations"].get(skill_name)
        target = destination / skill_name
        backups = _validated_backup_root(destination)
        backup = _validated_backup_child(backups, skill_name)
        target_present = target.exists() or target.is_symlink()
        if target_present and old_record is None:
            raise SkillPackError(
                "Refusing to replace an unmanaged skill directory; import or move it first"
            )
        if old_record is not None:
            if not target.is_dir() or target.is_symlink():
                raise SkillPackError("Managed skill path is missing or unsafe")
            _validate_recorded_install(
                target, skill_name, old_record.get("files")
            )
        backups.mkdir(exist_ok=True)
        backups = _validated_backup_root(destination, require_exists=True)
        backup = _validated_backup_child(backups, skill_name)
        stage = Path(tempfile.mkdtemp(prefix=".workchord-skill-stage-", dir=destination))
        try:
            staged_skill = _extract_validated_archive(
                archive_path, archive, catalog, skill_name, stage
            )
            _validate_installed(stage, catalog, skill_name, version)
            previous = None
            if old_record is not None:
                previous = {
                    "version": old_record.get("version"),
                    "source": old_record.get("source"),
                    "archive": old_record.get("archive"),
                    "archive_sha256": old_record.get("archive_sha256"),
                    "files": old_record.get("files"),
                    "installed_at": old_record.get("installed_at"),
                }
            after_lock = _clone_json_object(lock)
            after_lock["installations"][skill_name] = {
                "version": version,
                "source": str(release_dir),
                "archive": archive["path"],
                "archive_sha256": archive["sha256"],
                "files": skill["files"],
                "installed_at": datetime.now(timezone.utc).isoformat(),
                "previous_version": old_record.get("version") if old_record else None,
                "previous": previous,
                "backup": f"{BACKUP_DIRNAME}/{skill_name}" if old_record else None,
            }
            _begin_transaction(
                destination,
                operation="install",
                skill_name=skill_name,
                before_lock=_clone_json_object(lock),
                after_lock=after_lock,
                stage_name=stage.name,
            )
            _recover_interrupted_transaction(destination)
        except Exception:
            if _read_transaction(destination) is None and _path_present(stage):
                _remove_managed_path(stage)
                _fsync_directory(destination)
            raise


def validate_installed_skill(
    release_dir: Path, destination: Path, skill_name: str
) -> None:
    """Validate an installed role against the exact version in its lock record."""
    catalog, _ = _load_release(release_dir)
    lock = _read_install_lock(destination)
    record = lock["installations"].get(skill_name)
    if not record:
        raise SkillPackError("Skill is not recorded as installed")
    _validate_installed(destination, catalog, skill_name, str(record["version"]))


def rollback_skill(destination: Path, skill_name: str) -> None:
    """Swap the current installation with its retained rollback copy."""
    with _destination_mutation_lock(destination):
        _recover_interrupted_transaction(destination)
        lock = _read_install_lock(destination)
        record = lock["installations"].get(skill_name)
        target = destination / skill_name
        backups = _validated_backup_root(destination, require_exists=True)
        backup = _validated_backup_child(backups, skill_name)
        swap = _validated_backup_child(backups, f"{skill_name}.swap")
        previous = record.get("previous") if isinstance(record, dict) else None
        if (
            not record
            or not isinstance(previous, dict)
            or not target.is_dir()
            or target.is_symlink()
            or not backup.is_dir()
            or backup.is_symlink()
        ):
            raise SkillPackError("No rollback copy is available for this skill")
        _validate_recorded_install(target, skill_name, record.get("files"))
        _validate_recorded_install(backup, skill_name, previous.get("files"))
        if _path_present(swap):
            _remove_managed_path(swap)
        current = {
            "version": record.get("version"),
            "source": record.get("source"),
            "archive": record.get("archive"),
            "archive_sha256": record.get("archive_sha256"),
            "files": record.get("files"),
            "installed_at": record.get("installed_at"),
        }
        after_lock = _clone_json_object(lock)
        after_record = after_lock["installations"][skill_name]
        after_record.update(previous)
        after_record["previous_version"] = current["version"]
        after_record["previous"] = current
        after_record["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
        _begin_transaction(
            destination,
            operation="rollback",
            skill_name=skill_name,
            before_lock=_clone_json_object(lock),
            after_lock=after_lock,
        )
        _recover_interrupted_transaction(destination)


def uninstall_skill(destination: Path, skill_name: str) -> None:
    """Remove one managed skill, its rollback copy, and its lock entry."""
    with _destination_mutation_lock(destination):
        _recover_interrupted_transaction(destination)
        lock = _read_install_lock(destination)
        record = lock["installations"].get(skill_name)
        if not isinstance(record, dict):
            raise SkillPackError("Skill is not recorded as installed")
        target = destination / skill_name
        backups = _validated_backup_root(destination, require_exists=True)
        backup = _validated_backup_child(backups, skill_name)
        _validate_role_record(target, skill_name, record)
        previous = record.get("previous")
        if previous is None:
            if _path_present(backup):
                raise SkillPackError(
                    "Managed rollback copy exists without a lock integrity record"
                )
        else:
            _validate_role_record(backup, skill_name, previous)
        after_lock = _clone_json_object(lock)
        del after_lock["installations"][skill_name]
        _begin_transaction(
            destination,
            operation="uninstall",
            skill_name=skill_name,
            before_lock=_clone_json_object(lock),
            after_lock=after_lock,
        )
        _recover_interrupted_transaction(destination)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help="Canonical agent-skills directory (default: repository agent-skills)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "sync-generated",
        help="Synchronize shared contract blocks and role openai.yaml adapters",
    )
    subparsers.add_parser(
        "contract-json",
        help="Print the canonical machine-readable assigned-work v1 contract",
    )
    subparsers.add_parser("generate", help="Regenerate catalog.json from role folders")
    subparsers.add_parser(
        "freeze-release",
        help="Append current exact role versions to the immutable release baseline",
    )
    subparsers.add_parser("validate", help="Validate role folders and catalog.json")
    build_parser = subparsers.add_parser("build", help="Build reproducible role archives")
    build_parser.add_argument("--output-dir", type=Path, required=True)
    archive_parser = subparsers.add_parser("validate-archive", help="Validate one role archive")
    archive_parser.add_argument("archive", type=Path)
    archive_parser.add_argument("--skill", choices=sorted(ROLE_METADATA), required=True)
    codex_parser = subparsers.add_parser(
        "build-codex-plugin", help="Generate the Codex adapter from canonical roles"
    )
    codex_parser.add_argument("--output-dir", type=Path, required=True)
    install_parser = subparsers.add_parser(
        "install", help="Install or upgrade one exact role from a built release"
    )
    install_parser.add_argument("--release-dir", type=Path, required=True)
    install_parser.add_argument("--dest", type=Path, required=True)
    install_parser.add_argument("--skill", choices=sorted(ROLE_METADATA), required=True)
    install_parser.add_argument("--version", required=True)
    install_parser.add_argument("--format", choices=["zip", "tar.gz"], default="zip")
    installed_parser = subparsers.add_parser(
        "validate-installed", help="Validate an installed skill against its lock"
    )
    installed_parser.add_argument("--release-dir", type=Path, required=True)
    installed_parser.add_argument("--dest", type=Path, required=True)
    installed_parser.add_argument("--skill", choices=sorted(ROLE_METADATA), required=True)
    rollback_parser = subparsers.add_parser(
        "rollback", help="Swap an installed skill with its retained prior copy"
    )
    rollback_parser.add_argument("--dest", type=Path, required=True)
    rollback_parser.add_argument("--skill", choices=sorted(ROLE_METADATA), required=True)
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Remove one managed role skill and its lock entry"
    )
    uninstall_parser.add_argument("--dest", type=Path, required=True)
    uninstall_parser.add_argument("--skill", choices=sorted(ROLE_METADATA), required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    skills_dir = args.skills_dir.resolve()
    try:
        if args.command == "sync-generated":
            if skills_dir != DEFAULT_SKILLS_DIR.resolve():
                raise SkillPackError(
                    "sync-generated operates only on the canonical repository skill sources"
                )
            updated = sync_generated_skill_sources(REPOSITORY_ROOT, skills_dir)
            print(f"Synchronized {len(updated)} generated skill source files")
        elif args.command == "contract-json":
            sys.stdout.buffer.write(_canonical_json(ASSIGNED_WORK_V1_CONTRACT))
        elif args.command == "generate":
            path = write_catalog(skills_dir)
            print(f"Generated {path}")
        elif args.command == "freeze-release":
            path = freeze_release(skills_dir)
            print(f"Froze exact role versions in {path}")
        elif args.command == "validate":
            validate_catalog(skills_dir)
            print(f"Validated {skills_dir}")
        elif args.command == "build":
            index = build_release(skills_dir, args.output_dir.resolve())
            print(
                f"Built {len(index['artifacts'])} archives in {args.output_dir.resolve()}"
            )
        elif args.command == "validate-archive":
            catalog = validate_catalog(skills_dir)
            validate_archive(args.archive.resolve(), catalog, args.skill)
            print(f"Validated {args.archive}")
        elif args.command == "build-codex-plugin":
            path = build_codex_plugin(skills_dir, args.output_dir.resolve())
            print(f"Built Codex plugin adapter in {path}")
        elif args.command == "install":
            install_skill(
                args.release_dir.resolve(),
                args.dest.resolve(),
                args.skill,
                args.version,
                args.format,
            )
            print(f"Installed {args.skill}@{args.version} in {args.dest.resolve()}")
        elif args.command == "validate-installed":
            validate_installed_skill(
                args.release_dir.resolve(), args.dest.resolve(), args.skill
            )
            print(f"Validated installed {args.skill}")
        elif args.command == "rollback":
            rollback_skill(args.dest.resolve(), args.skill)
            print(f"Rolled back {args.skill}")
        elif args.command == "uninstall":
            uninstall_skill(args.dest.resolve(), args.skill)
            print(f"Uninstalled {args.skill}")
        else:  # pragma: no cover - argparse enforces commands
            raise AssertionError(args.command)
    except (OSError, SkillPackError) as exc:
        print(f"agent skill packaging error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
