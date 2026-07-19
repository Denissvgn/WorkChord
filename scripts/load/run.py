#!/usr/bin/env python3
"""Run deterministic, production-shaped REST and MCP load through public APIs."""

from __future__ import annotations

import argparse
import asyncio
from collections import Counter, defaultdict
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from datetime import UTC, datetime
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import random
import sys
from time import monotonic
from typing import Any, Mapping
from urllib.parse import urlsplit
from uuid import uuid4

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    HTTP_TOOL,
    MCP_TOOL,
    QualificationInputError,
    authorized_base_url,
    capacity_contract,
    contract_sha256,
    read_json_object,
    sha256_file,
    traffic_profile,
    utc_now_text,
)
from scripts.load.result import (
    evaluate_client_gates,
    evaluate_external_gates,
    evaluate_workload_gates,
    latency_summary,
    measurement,
    result_status,
    write_result,
)


PHASE_DEFAULTS = {
    "dry": (0.0, 0.0),
    "small": (60.0, 2.0),
    "warmup": (15 * 60.0, None),
    "steady": (60 * 60.0, None),
    "burst": (10 * 60.0, "burst"),
    "soak": (8 * 60 * 60.0, "soak"),
    "external_wait": (60.0, None),
}
MAX_ERROR_SAMPLES = 1_000
RETRYABLE_STATUSES = frozenset({429, 502, 503, 504, 599})


@dataclass
class Attempt:
    operation_id: str
    classification: str
    status: int
    latency_ms: float
    request_bytes: int
    response_bytes: int
    response_cardinality: int
    entity_category: str
    payload_profile: str
    response_profile: str
    client_kind: str


@dataclass
class Recorder:
    attempts: list[Attempt] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    in_flight: int = 0
    in_flight_peak: int = 0
    open_connections_peak: int = 0
    session_state_counts: Counter[str] = field(default_factory=Counter)
    client_last_started: dict[str, float] = field(default_factory=dict)
    client_intervals: dict[str, list[float]] = field(
        default_factory=lambda: defaultdict(list)
    )
    poll_guidance_responses: int = 0
    poll_guidance_parsed: int = 0
    poll_guidance_respected: int = 0
    poll_guidance_outstanding: int = 0
    logical_attempts_completed: int = 0
    retry_attempts: int = 0
    retry_exhausted: int = 0
    physical_attempts_per_logical_peak: int = 0
    connection_ramp_seconds: float | None = None

    def begin(self, client: "VirtualClient | None" = None) -> None:
        self.in_flight += 1
        self.in_flight_peak = max(self.in_flight_peak, self.in_flight)
        if client is not None:
            now = monotonic()
            key = f"{client.kind}:{client.credential['id']}"
            previous = self.client_last_started.get(key)
            if previous is not None:
                self.client_intervals[client.kind].append(now - previous)
            self.client_last_started[key] = now

    def finish(self, attempt: Attempt) -> None:
        self.attempts.append(attempt)
        self.in_flight = max(0, self.in_flight - 1)

    def error(self, operation_id: str, exc: BaseException) -> None:
        if len(self.errors) >= MAX_ERROR_SAMPLES:
            return
        message = " ".join(str(exc).split())[:500]
        self.errors.append(
            {
                "operation_id": operation_id,
                "kind": type(exc).__name__,
                "message": message or type(exc).__name__,
            }
        )


def _validated_retry_policy(
    profile: Mapping[str, Any],
) -> dict[str, Any] | None:
    raw = profile.get("retry_policy")
    if raw is None:
        return None
    if not isinstance(raw, Mapping):
        raise QualificationInputError("Retry policy must be an object")
    maximum_attempts = int(raw.get("maximum_attempts", 0))
    backoffs = raw.get("backoff_seconds")
    jitter = float(raw.get("jitter_percent", -1))
    if not 1 <= maximum_attempts <= 10:
        raise QualificationInputError("Retry maximum_attempts must be between 1 and 10")
    if (
        not isinstance(backoffs, list)
        or len(backoffs) < maximum_attempts - 1
        or any(not isinstance(value, (int, float)) or value <= 0 for value in backoffs)
    ):
        raise QualificationInputError(
            "Retry backoff_seconds must cover every permitted retry"
        )
    if not 0 <= jitter <= 100:
        raise QualificationInputError("Retry jitter_percent must be between 0 and 100")
    return {
        "maximum_attempts": maximum_attempts,
        "backoff_seconds": [float(value) for value in backoffs],
        "jitter_percent": jitter,
    }


def _retry_delay_seconds(
    policy: Mapping[str, Any],
    *,
    seed: int,
    logical_index: int,
    retry_index: int,
) -> float:
    backoffs = policy["backoff_seconds"]
    base = float(backoffs[min(retry_index, len(backoffs) - 1)])
    jitter_fraction = float(policy["jitter_percent"]) / 100
    randomizer = random.Random(
        f"{seed}:retry:{logical_index}:{retry_index}"
    )
    return base * randomizer.uniform(1 - jitter_fraction, 1 + jitter_fraction)


def _response_cardinality(
    profile: str,
    value: Any,
    *,
    status: int,
) -> int:
    if status >= 400 or value is None:
        return 0
    if profile == "single":
        return 1

    current = value
    for _ in range(3):
        if isinstance(current, list):
            return len(current)
        if not isinstance(current, Mapping):
            return 1
        preferred = (
            ("tasks", "decisions")
            if profile in {"task_tree", "hot_gantt"}
            else (
                "items",
                "projects",
                "iterations",
                "team_members",
                "members",
                "cards",
                "events",
                "claims",
                "reviews",
                "assignments",
                "tasks",
                "work",
            )
        )
        for key in preferred:
            candidate = current.get(key)
            if isinstance(candidate, list):
                return len(candidate)
        nested = current.get("result", current.get("data"))
        if nested is current or nested is None:
            return 1
        current = nested
    return 1


class OperationBuilder:
    """Build bounded, deterministic request payloads without response lookups."""

    def __init__(
        self,
        credentials: Mapping[str, Any],
        seed: int,
        *,
        entity_plan: list[str] | None = None,
        run_namespace: str = "local",
    ) -> None:
        entities = credentials["entities"]
        self.project_max = int(entities["project_ids"][1])
        self.iteration_max = int(entities["iteration_ids"][1])
        self.task_max = int(entities["task_ids"][1])
        self.hot_project_id = int(entities["hot_project_id"])
        self.hot_iteration_id = int(entities["hot_iteration_id"])
        self.hot_iteration_tasks = int(entities.get("hot_iteration_tasks", 1))
        self.hot_project_tasks = int(
            entities.get("hot_project_linked_tasks", self.hot_iteration_tasks)
        )
        self.agent_assignment_first_task = int(
            entities.get("agent_assignment_first_task_id", self.task_max + 1)
        )
        self.seed = seed
        self.run_namespace = hashlib.sha256(
            run_namespace.encode("utf-8")
        ).hexdigest()[:16]
        self.counters: Counter[str] = Counter()
        self.entity_counter = 0
        self.entity_plan = entity_plan or []
        self.last_entity_categories: dict[str, str] = {}

    def _next(self, operation_id: str) -> int:
        self.counters[operation_id] += 1
        return self.counters[operation_id]

    def _next_entity(self, operation_id: str) -> int:
        self.entity_counter += 1
        self.last_entity_categories[operation_id] = self._category(
            self.entity_counter
        )
        return self.entity_counter

    def _category(self, counter: int) -> str:
        if 0 < counter <= len(self.entity_plan):
            return self.entity_plan[counter - 1]
        bucket = (counter - 1) % 100
        if bucket < 20:
            return "hot_project"
        if bucket < 40:
            return "hot_iteration"
        if bucket < 50:
            return "same_key_contention"
        return "cold_long_tail"

    def _project(self, counter: int, *, avoid_hot: bool = False) -> int:
        if not avoid_hot and self._category(counter) in {
            "hot_project",
            "same_key_contention",
        }:
            return self.hot_project_id
        if self.project_max <= 1:
            return 1
        return 2 + ((counter - 1) % (self.project_max - 1))

    def _iteration(self, counter: int, *, avoid_hot: bool = False) -> int:
        if not avoid_hot and self._category(counter) in {
            "hot_iteration",
            "same_key_contention",
        }:
            return self.hot_iteration_id
        if self.iteration_max <= 1:
            return 1
        return 2 + ((counter - 1) % (self.iteration_max - 1))

    def _task(self, counter: int, *, partition: int = 0) -> int:
        if self.task_max < 10_000:
            partition_size = max(1, self.task_max // 3)
            lower = min(self.task_max, 1 + (partition * partition_size))
            upper = min(self.task_max, lower + partition_size - 1)
            if partition == 0:
                # The small seed assigns its high task-id tail to agent
                # lifecycles and its hot-iteration prefix carries the dense
                # dependency graph. Keep ordinary REST transitions between
                # those two regions so they exercise planned leaf tasks
                # without manufacturing unrelated lifecycle conflicts.
                lower = min(upper, max(lower, self.hot_iteration_tasks + 1))
                upper = min(upper, max(lower, self.hot_project_tasks))
        else:
            lower = min(
                self.task_max,
                max(1, self.hot_project_tasks + 1 + (partition * 20_000)),
            )
            upper = self.task_max
            if partition == 0:
                upper = min(
                    upper,
                    max(lower, self.agent_assignment_first_task - 1),
                )
        available = max(1, upper - lower + 1)
        if self._category(counter) == "same_key_contention":
            return lower
        return lower + ((counter - 1) % available)

    def rest_request(
        self, operation: Mapping[str, Any]
    ) -> tuple[str, str, dict[str, Any], str]:
        operation_id = str(operation["id"])
        counter = self._next(operation_id)
        entity_counter = self._next_entity(operation_id)
        project_id = self._project(entity_counter)
        iteration_id = self._iteration(entity_counter)
        task_id = self._task(entity_counter)
        dependency_id = max(1, task_id - 1)
        path = str(operation["operation"]).format(
            project_id=project_id,
            iteration_id=iteration_id,
            task_id=task_id,
            dependency_id=dependency_id,
        )
        kwargs: dict[str, Any] = {}

        if operation_id == "rest_iterations_list":
            kwargs["params"] = {"limit": min(500, self.iteration_max)}
        elif operation_id == "rest_dashboard_cards":
            kwargs["params"] = {"iteration_id": iteration_id}
        elif operation_id == "rest_schedule_preview":
            kwargs["json"] = {"changes": []}
        elif operation_id == "rest_task_update":
            kwargs["json"] = {
                "expected_version": 1,
                "title": f"Qualification updated task {counter}",
                "description": (
                    "Scope: exercise an optimistic task update. "
                    "Acceptance: exactly one version wins. "
                    "Verification: conflicts remain typed."
                ),
            }
        elif operation_id == "rest_task_status":
            kwargs["json"] = {
                "status": "active",
                "reason": "qualification transition",
                "expected_version": 1,
            }
        elif operation_id == "rest_task_create":
            kwargs["json"] = {
                "title": f"Qualification created task {counter}",
                "description": (
                    "Scope: exercise normal task creation. "
                    "Acceptance: persist through the public API. "
                    "Verification: response is typed."
                ),
                "priority": 5,
                "effort_days": 1,
                "tags": ["qualification"],
            }
        elif operation_id == "rest_dependency_add":
            # Tasks in the seeded hot-project band repeat an iteration every
            # floor((iterations - 1) / projects) ids.  Select both ends of the
            # edge from that band with exactly that stride: this keeps the
            # dependency inside one iteration while staying clear of the
            # dense, pre-seeded hot-iteration graph and the agent-assignment
            # tail.
            iteration_stride = max(
                1,
                (self.iteration_max - 1) // max(1, self.project_max),
            )
            dependency_upper = min(
                self.task_max,
                max(1, self.agent_assignment_first_task - 1),
            )
            pair_upper = min(dependency_upper, self.hot_project_tasks)
            available_pairs = max(
                1,
                (pair_upper - self.hot_iteration_tasks - 1)
                // iteration_stride,
            )
            pair_index = (counter - 1) % available_pairs
            task_id = pair_upper - (pair_index * iteration_stride)
            dependency_id = task_id - iteration_stride
            if dependency_id <= self.hot_iteration_tasks:
                raise QualificationInputError(
                    "Seed does not provide a safe hot-project dependency pair"
                )
            path = f"/api/tasks/{task_id}/dependencies"
            kwargs["json"] = {"depends_on_id": dependency_id}
        elif operation_id == "rest_saved_view_create":
            kwargs["json"] = {
                "name": (
                    f"Qualification view {self.run_namespace}-{counter}"
                ),
                "view_type": "tasks",
                "scope": "personal",
                "filters_json": {"iteration_id": iteration_id},
                "sort_json": {"field": "id", "direction": "asc"},
                "columns_json": {"visible": ["title", "status"]},
            }
        elif operation_id == "rest_dependency_delete":
            hot_tasks = max(2, min(self.task_max, 2_500))
            distance = 1 + ((counter - 1) // max(1, hot_tasks - 1))
            task_id = 1 + distance + ((counter - 1) % max(1, hot_tasks - distance))
            dependency_id = task_id - distance
            path = f"/api/tasks/{task_id}/dependencies/{dependency_id}"
        elif operation_id == "llm_formalize":
            kwargs["json"] = {"context": "qualification provider wait"}
        elif operation_id == "llm_improve":
            kwargs["json"] = {
                "current_description": "Qualification description",
                "context": "qualification provider wait",
            }
        elif operation_id == "llm_suggest":
            kwargs["json"] = {
                "title": f"Qualification suggestion {counter}",
                "description": "Measure the configured provider wait boundary.",
                "project_id": project_id,
            }
        elif operation_id == "llm_explain_schedule":
            kwargs["json"] = {"detail_level": "brief"}

        category = self.last_entity_categories[operation_id]
        return str(operation["method"]), path, kwargs, category

    def mcp_arguments(
        self,
        operation_id: str,
        client: "VirtualClient",
    ) -> dict[str, Any]:
        counter = self._next(operation_id)
        entity_counter = self._next_entity(operation_id)
        actor_id = int(client.credential["id"])
        actor_count = max(1, int(client.actor_count))
        assignment_index = client.assignment_index
        assignment_id = client.next_assignment_id or (
            actor_id + (assignment_index * actor_count)
        )
        task_id = client.next_task_id or max(
            1,
            self.task_max - max(0, client.assignment_capacity - assignment_id),
        )
        idempotency_key = (
            f"load-{self.run_namespace}-{actor_id}-{operation_id}-{counter}"
        )

        if operation_id == "mcp_agent_get_my_work":
            return {"limit": 20}
        if operation_id == "mcp_agent_complete_context":
            active = client.live_work or {}
            return {
                "task_id": int(active.get("task_id", task_id)),
                "assignment_id": int(
                    active.get("assignment_id", assignment_id)
                ),
            }
        if operation_id == "mcp_agent_list_claims":
            return {}
        if operation_id == "mcp_agent_reviews":
            return {"limit": 20}
        if operation_id == "mcp_project_tasks":
            return {"project_id": self._project(entity_counter, avoid_hot=True)}
        if operation_id == "mcp_agent_begin":
            return {
                "payload": {
                    "assignment_id": assignment_id,
                    "queue_revision": client.queue_revision,
                    "lease_seconds": 3600,
                    "trace_id": f"qualification-{actor_id}-{counter}",
                    "model": "qualification-model",
                    "tool_name": "workchord-load-v1",
                    "metadata": {"qualification": True},
                },
                "idempotency_key": idempotency_key,
            }
        live = client.live_work or {
            "assignment_id": assignment_id,
            "run_id": actor_id,
            "claim_id": "qualification0000",
            "claim_generation": 1,
            "expected_task_version": 1,
        }
        task_id = int(live.get("task_id", task_id))
        fence = {
            key: live[key]
            for key in (
                "assignment_id",
                "run_id",
                "claim_id",
                "claim_generation",
                "expected_task_version",
            )
        }
        if operation_id == "mcp_agent_renew":
            return {
                "payload": {**fence, "lease_seconds": 3600},
                "idempotency_key": idempotency_key,
            }
        if operation_id == "mcp_run_event":
            return {
                "run_id": int(live["run_id"]),
                "payload": {
                    "event_type": "progress",
                    "message": "qualification progress",
                    "payload": {"percent": 50},
                    "trace_id": f"qualification-{actor_id}",
                    "correlation_id": idempotency_key,
                },
            }
        if operation_id == "mcp_task_event":
            return {
                "task_id": task_id,
                "payload": {
                    "event_type": "qualification_progress",
                    "payload": {"summary": "qualification progress"},
                    "trace_id": f"qualification-{actor_id}",
                    "span_id": f"span-{counter}",
                    "correlation_id": idempotency_key,
                },
                "idempotency_key": idempotency_key,
            }
        if operation_id == "mcp_agent_submit":
            return {
                "payload": {
                    **fence,
                    "summary": "Qualification lifecycle submission",
                    "evidence": {"load_run": self.seed, "verified": True},
                    "artifact_links": [],
                },
                "idempotency_key": idempotency_key,
            }
        if operation_id == "mcp_agent_fail":
            return {
                "payload": {
                    **fence,
                    "status": "failed",
                    "summary": "Qualification deliberate failure path",
                    "error": "injected qualification failure",
                    "evidence": {"load_run": self.seed, "injected": True},
                },
                "idempotency_key": idempotency_key,
            }
        raise QualificationInputError(f"Unsupported MCP operation: {operation_id}")


class VirtualClient:
    def __init__(
        self,
        *,
        kind: str,
        credential: Mapping[str, Any],
        base_url: str,
        cookie_name: str,
        timeout: float,
        actor_count: int,
        assignment_capacity: int,
    ) -> None:
        self.kind = kind
        self.credential = dict(credential)
        self.actor_count = actor_count
        self.assignment_capacity = assignment_capacity
        self.queue_revision = 1
        self.assignment_index = 0
        self.live_work: dict[str, Any] | None = None
        self.next_assignment_id: int | None = None
        self.next_task_id: int | None = None
        self.next_poll_after: str | None = None
        self.next_poll_not_before: float | None = None
        self.poll_guidance_outstanding = False
        self.lock = asyncio.Lock()
        headers = {"User-Agent": "WorkChordQualification/1"}
        cookies: dict[str, str] = {}
        if kind == "agent":
            headers["Authorization"] = f"Bearer {credential['api_key']}"
        elif credential.get("state") != "new":
            cookies[cookie_name] = str(credential["token"])
        self.http = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            cookies=cookies,
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
            follow_redirects=False,
        )
        self.stack: AsyncExitStack | None = None
        self.mcp: ClientSession | None = None

    async def open(self, mcp_url: str) -> None:
        if self.kind == "agent":
            self.stack = AsyncExitStack()
            await self.stack.__aenter__()
            read_stream, write_stream, _session_id = await self.stack.enter_async_context(
                streamable_http_client(mcp_url, http_client=self.http)
            )
            self.mcp = await self.stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            await self.mcp.initialize()
        else:
            response = await self.http.get("/health/live")
            response.raise_for_status()

    async def close(self) -> None:
        if self.stack is not None:
            await self.stack.aclose()
        await self.http.aclose()

    def open_connection_count(self) -> int:
        transport = getattr(self.http, "_transport", None)
        pool = getattr(transport, "_pool", None)
        connections = getattr(pool, "connections", ())
        try:
            return len(connections)
        except TypeError:
            return 0

    def set_poll_guidance(self, value: str) -> bool:
        """Parse one server deadline and arm the next get-work poll."""
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return False
        if parsed.tzinfo is None:
            return False
        delay = max(0.0, (parsed.astimezone(UTC) - datetime.now(UTC)).total_seconds())
        maximum = float(
            capacity_contract()["traffic"]["agent_poll_intervals_seconds"][
                "retry_maximum"
            ]
        )
        if delay > maximum + 1:
            return False
        self.next_poll_after = value
        self.next_poll_not_before = monotonic() + delay
        self.poll_guidance_outstanding = True
        return True


def _phase_shape(
    profile: Mapping[str, Any],
    phase: str,
    *,
    duration_override: float | None,
    rps_override: float | None,
) -> tuple[float, float]:
    default_duration, rate_mode = PHASE_DEFAULTS[phase]
    if phase == "dry":
        return 0.0, 0.0
    if phase == "external_wait":
        default_rps = float(profile.get("concurrent_calls", 25)) / 5
    elif rate_mode == "burst":
        default_rps = float(profile["burst_rps"])
    elif rate_mode == "soak":
        default_rps = float(profile["steady_rps"]) * 0.60
    else:
        default_rps = float(profile["steady_rps"])
    if phase == "small":
        default_rps = 2.0
    duration = duration_override if duration_override is not None else default_duration
    rps = rps_override if rps_override is not None else default_rps
    if duration <= 0 or rps <= 0:
        raise QualificationInputError("Live phase duration and RPS must be positive")
    return float(duration), float(rps)


def _weighted_plan(
    operations: list[Mapping[str, Any]], attempts: int, seed: int
) -> list[Mapping[str, Any]]:
    if attempts <= 0:
        return []
    exact = [attempts * float(item["weight_percent"]) / 100 for item in operations]
    counts = [math.floor(value) for value in exact]
    remainder = attempts - sum(counts)
    order = sorted(
        range(len(operations)),
        key=lambda index: (exact[index] - counts[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        counts[index] += 1
    plan = [operation for operation, count in zip(operations, counts) for _ in range(count)]
    random.Random(seed).shuffle(plan)
    return plan


def _distribution_plan(
    distribution: Mapping[str, Any], attempts: int, seed: int
) -> list[str]:
    categories = list(distribution)
    exact = [attempts * float(distribution[name]) / 100 for name in categories]
    counts = [math.floor(value) for value in exact]
    remainder = attempts - sum(counts)
    order = sorted(
        range(len(categories)),
        key=lambda index: (exact[index] - counts[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        counts[index] += 1
    plan = [
        category
        for category, count in zip(categories, counts)
        for _ in range(count)
    ]
    random.Random(seed).shuffle(plan)
    return plan


def _request_class(operation: Mapping[str, Any]) -> str:
    operation_id = str(operation["id"])
    if operation_id == "rest_schedule_preview":
        return "schedule_preview"
    if operation_id == "rest_schedule_apply":
        return "schedule_apply"
    if operation_id in {"rest_iteration_tasks", "rest_iteration_gantt"}:
        return "hot_read"
    classification = str(operation["classification"])
    if classification == "read":
        return "core_read"
    if classification == "write":
        return "core_write"
    return classification


def _result_payload(
    *,
    args: argparse.Namespace,
    contract: Mapping[str, Any],
    seed_manifest: Mapping[str, Any] | None,
    release: Mapping[str, Any],
    duration: float,
    target_rps: float,
    target_clients: int,
    actual_duration: float,
    recorder: Recorder,
    snapshots: Mapping[str, Any],
    external_metrics: Mapping[str, Any],
    integrity: Mapping[str, Any],
    operation_plan: list[Mapping[str, Any]],
) -> dict[str, Any]:
    by_operation: dict[str, list[Attempt]] = defaultdict(list)
    by_class: dict[str, list[Attempt]] = defaultdict(list)
    for attempt in recorder.attempts:
        by_operation[attempt.operation_id].append(attempt)
        by_class[attempt.classification].append(attempt)

    operations = {
        str(operation["id"]): measurement(
            [item.latency_ms for item in by_operation[str(operation["id"])]],
            [item.status for item in by_operation[str(operation["id"])]],
        )
        for operation in traffic_profile(contract, args.profile)["operations"]
    }
    class_names = {
        "core_read",
        "core_write",
        "hot_read",
        "schedule_preview",
        "schedule_apply",
        "external_wait",
    }
    classifications = {
        name: measurement(
            [item.latency_ms for item in by_class[name]],
            [item.status for item in by_class[name]],
        )
        for name in sorted(class_names)
    }
    operation_counts = Counter(item.operation_id for item in recorder.attempts)
    status_counts = Counter(str(item.status) for item in recorder.attempts)
    completed = recorder.logical_attempts_completed
    eligible_attempts = len(recorder.attempts)
    entity_counts = Counter(item.entity_category for item in recorder.attempts)
    entity_total = sum(entity_counts.values())
    request_sizes: dict[str, list[int]] = defaultdict(list)
    response_sizes: dict[str, list[int]] = defaultdict(list)
    response_cardinalities: dict[str, list[int]] = defaultdict(list)
    for item in recorder.attempts:
        request_sizes[item.payload_profile].append(item.request_bytes)
        response_sizes[item.response_profile].append(item.response_bytes)
        response_cardinalities[item.response_profile].append(
            item.response_cardinality
        )
    session_total = sum(recorder.session_state_counts.values())
    workload_evidence = {
        "entity_distribution_counts": dict(sorted(entity_counts.items())),
        "entity_distribution_percent": {
            key: round(value / entity_total * 100, 4) if entity_total else 0
            for key, value in sorted(entity_counts.items())
        },
        "session_state_counts": dict(sorted(recorder.session_state_counts.items())),
        "session_state_percent": {
            key: round(value / session_total * 100, 4) if session_total else 0
            for key, value in sorted(recorder.session_state_counts.items())
        },
        "request_payloads": {
            key: {"samples": len(values), "bytes": latency_summary(values)}
            for key, values in sorted(request_sizes.items())
        },
        "response_payloads": {
            key: {"samples": len(values), "bytes": latency_summary(values)}
            for key, values in sorted(response_sizes.items())
        },
        "response_cardinalities": {
            key: {"samples": len(values), "items": latency_summary(values)}
            for key, values in sorted(response_cardinalities.items())
        },
        "think_time_seconds": {
            key: latency_summary(values)
            for key, values in sorted(recorder.client_intervals.items())
        },
        "client_mechanics": {
            "real_cookie_tokens": True,
            "optimistic_versions": True,
            "idempotency_keys": True,
            "poll_guidance_responses": recorder.poll_guidance_responses,
            "poll_guidance_parsed": recorder.poll_guidance_parsed,
            "poll_guidance_respected": recorder.poll_guidance_respected,
            "poll_guidance_outstanding": recorder.poll_guidance_outstanding,
            "retry_policy": _validated_retry_policy(
                traffic_profile(contract, args.profile)
            ),
            "retry_attempts": recorder.retry_attempts,
            "retry_exhausted": recorder.retry_exhausted,
            "physical_attempts_per_logical_peak": (
                recorder.physical_attempts_per_logical_peak
            ),
        },
        "connection_ramp_seconds": recorder.connection_ramp_seconds,
    }
    qualification_candidate = bool(
        args.qualification_candidate
        and seed_manifest
        and seed_manifest.get("qualification_eligible") is True
        and args.phase in {"warmup", "steady", "burst", "soak", "external_wait"}
        and args.duration_seconds is None
        and args.rps is None
    )
    payload: dict[str, Any] = {
        "kind": "workchord-postgresql-load-result",
        "schema_version": 1,
        "run_id": args.run_id,
        "created_at": utc_now_text(),
        "qualification_candidate": qualification_candidate,
        "status": "dry_run" if args.phase == "dry" else "incomplete",
        "capacity_contract": {
            "id": contract["contract_id"],
            "sha256": contract_sha256(),
        },
        "toolchain": {
            "runner": "workchord-load-v1",
            "http": {
                **HTTP_TOOL,
                "version": importlib.metadata.version("httpx"),
            },
            "mcp": {
                **MCP_TOOL,
                "version": importlib.metadata.version("mcp"),
            },
            "python": sys.version.split()[0],
        },
        "target": {
            "base_url": args.base_url,
            "authorized_host": args.authorize_host,
            "environment": args.environment,
            "change_id": args.change_id,
        },
        "release": dict(release),
        "seed": {
            "manifest_sha256": (
                str(seed_manifest["document_sha256"]) if seed_manifest else None
            ),
            "qualification_eligible": bool(
                seed_manifest and seed_manifest.get("qualification_eligible") is True
            ),
        },
        "traffic": {
            "profile_id": args.profile,
            "phase": args.phase,
            "target_duration_seconds": duration,
            "actual_duration_seconds": round(actual_duration, 6),
            "target_rps": target_rps,
            "actual_rps": (
                round(eligible_attempts / actual_duration, 6)
                if actual_duration
                else 0
            ),
            "target_virtual_users": target_clients,
            "active_clients_peak": target_clients if args.phase != "dry" else 0,
            "open_connections_peak": recorder.open_connections_peak,
            "in_flight_requests_peak": recorder.in_flight_peak,
            "scheduled_attempts": len(operation_plan),
            "completed_attempts": completed,
            "eligible_attempts": eligible_attempts,
            "operation_counts": {
                str(key): value for key, value in sorted(operation_counts.items())
            },
            "status_counts": dict(sorted(status_counts.items())),
        },
        "operations": operations,
        "classifications": classifications,
        "workload_evidence": workload_evidence,
        "snapshots": dict(snapshots),
        "external_metrics": dict(external_metrics),
        "integrity": dict(integrity),
        "gates": {},
        "errors": recorder.errors,
    }
    if args.phase != "dry":
        payload["gates"].update(evaluate_client_gates(payload))
        payload["gates"].update(evaluate_workload_gates(payload))
        payload["gates"].update(evaluate_external_gates(external_metrics, integrity))
        payload["status"] = result_status(
            payload["gates"], qualification_candidate=qualification_candidate
        )
    return payload


def _decode_tool_result(result: Any) -> tuple[int, dict[str, Any] | None, int]:
    structured = getattr(result, "structuredContent", None)
    if not isinstance(structured, dict):
        structured = getattr(result, "structured_content", None)
    text_blocks = [
        str(getattr(block, "text", ""))
        for block in getattr(result, "content", [])
        if getattr(block, "text", None)
    ]
    response_bytes = len("".join(text_blocks).encode("utf-8"))
    if structured is not None:
        response_bytes += len(json.dumps(structured, default=str).encode("utf-8"))
    if not getattr(result, "isError", getattr(result, "is_error", False)):
        return 200, structured, response_bytes
    combined = " ".join(text_blocks)
    status = 422
    mappings = {
        "agent_state_conflict": 409,
        "task_version_conflict": 409,
        "database_transaction_conflict": 409,
        "agent_resource_not_found": 404,
        "agent_permission_denied": 403,
        "agent_authentication_failed": 401,
        "maintenance_mode": 503,
        "rate_limit": 429,
        "throttl": 429,
    }
    for marker, mapped in mappings.items():
        if marker in combined:
            status = mapped
            break
    return status, structured, response_bytes


def _update_agent_state(
    client: VirtualClient,
    operation_id: str,
    status: int,
    structured: Mapping[str, Any] | None,
) -> bool:
    if status != 200 or not structured:
        return False
    value: Mapping[str, Any] = structured
    if isinstance(structured.get("result"), dict):
        value = structured["result"]
    if operation_id == "mcp_agent_get_my_work":
        revision = value.get("queue_revision")
        if isinstance(revision, int):
            client.queue_revision = revision
        current = value.get("current")
        if isinstance(current, Mapping):
            assignment = current.get("assignment") or {}
            task = current.get("task") or {}
            run = current.get("run") or {}
            claim = current.get("claim") or {}
            required = (
                assignment.get("id"),
                run.get("id"),
                claim.get("claim_id"),
                claim.get("claim_generation"),
                task.get("version"),
                task.get("id"),
            )
            if all(required):
                client.live_work = {
                    "assignment_id": int(required[0]),
                    "run_id": int(required[1]),
                    "claim_id": str(required[2]),
                    "claim_generation": int(required[3]),
                    "expected_task_version": int(required[4]),
                    "task_id": int(required[5]),
                }
                client.next_assignment_id = None
                client.next_task_id = None
        elif value.get("state") == "start_assigned":
            next_item = value.get("next")
            if isinstance(next_item, Mapping):
                assignment = next_item.get("assignment") or {}
                task = next_item.get("task") or {}
                if assignment.get("id") and task.get("id"):
                    client.next_assignment_id = int(assignment["id"])
                    client.next_task_id = int(task["id"])
        guidance = value.get("next_poll_after")
        if isinstance(guidance, str) and guidance:
            return client.set_poll_guidance(guidance)
    elif operation_id == "mcp_agent_begin":
        assignment = value.get("assignment") or {}
        task = value.get("task") or {}
        run = value.get("run") or {}
        required = (
            assignment.get("id"),
            run.get("id"),
            value.get("claim_id"),
            value.get("claim_generation"),
            task.get("version"),
            task.get("id"),
        )
        if all(required):
            client.live_work = {
                "assignment_id": int(required[0]),
                "run_id": int(required[1]),
                "claim_id": str(required[2]),
                "claim_generation": int(required[3]),
                "expected_task_version": int(required[4]),
                "task_id": int(required[5]),
            }
            client.next_assignment_id = None
            client.next_task_id = None
        revision = value.get("queue_revision")
        if isinstance(revision, int):
            client.queue_revision = revision
    elif operation_id in {"mcp_agent_submit", "mcp_agent_fail"}:
        completed_assignment = (
            int(client.live_work["assignment_id"])
            if client.live_work is not None
            else None
        )
        client.live_work = None
        if completed_assignment is not None:
            actor_id = int(client.credential["id"])
            client.assignment_index = max(
                client.assignment_index + 1,
                ((completed_assignment - actor_id) // max(1, client.actor_count))
                + 1,
            )
        else:
            client.assignment_index += 1
        client.next_assignment_id = None
        client.next_task_id = None
        client.queue_revision += 1
    return False


async def _perform_attempt(
    operation: Mapping[str, Any],
    *,
    builder: OperationBuilder,
    browser_clients: list[VirtualClient],
    agent_clients: list[VirtualClient],
    recorder: Recorder,
    client_counter: Counter[str],
    logical_index: int,
    retry_policy: Mapping[str, Any] | None,
) -> None:
    operation_id = str(operation["id"])
    transport = str(operation["transport"])
    clients = browser_clients if transport == "REST" else agent_clients
    if not clients:
        recorder.begin()
        recorder.error(operation_id, QualificationInputError("No eligible virtual client"))
        recorder.finish(
            Attempt(
                operation_id,
                _request_class(operation),
                599,
                0,
                0,
                0,
                0,
                "cold_long_tail",
                str(operation["payload_profile"]),
                str(operation["response_profile"]),
                "none",
            )
        )
        recorder.logical_attempts_completed += 1
        recorder.physical_attempts_per_logical_peak = max(
            recorder.physical_attempts_per_logical_peak,
            1,
        )
        return
    index = client_counter[transport] % len(clients)
    client_counter[transport] += 1
    client = clients[index]
    classification = _request_class(operation)
    request_bytes = 0
    entity_category = "cold_long_tail"
    maximum_attempts = (
        int(retry_policy["maximum_attempts"])
        if retry_policy is not None
        else 1
    )
    async with client.lock:
        if (
            operation_id == "mcp_agent_get_my_work"
            and client.poll_guidance_outstanding
        ):
            delay = max(
                0.0,
                (client.next_poll_not_before or monotonic()) - monotonic(),
            )
            if delay:
                await asyncio.sleep(delay)
            client.poll_guidance_outstanding = False
            client.next_poll_not_before = None
            recorder.poll_guidance_respected += 1

        method = ""
        path = ""
        kwargs: dict[str, Any] = {}
        arguments: dict[str, Any] = {}
        try:
            if transport == "REST":
                method, path, kwargs, entity_category = builder.rest_request(operation)
                if "json" in kwargs:
                    request_bytes = len(
                        json.dumps(kwargs["json"], separators=(",", ":")).encode("utf-8")
                    )
            else:
                if client.mcp is None:
                    raise QualificationInputError("MCP client was not initialized")
                arguments = builder.mcp_arguments(operation_id, client)
                entity_category = builder.last_entity_categories[operation_id]
                request_bytes = len(
                    json.dumps(arguments, separators=(",", ":"), default=str).encode("utf-8")
                )
            if operation["payload_profile"] == "none":
                request_bytes = 0
        except Exception as exc:
            recorder.begin(client)
            recorder.error(operation_id, exc)
            recorder.finish(
                Attempt(
                    operation_id=operation_id,
                    classification=classification,
                    status=599,
                    latency_ms=0,
                    request_bytes=request_bytes,
                    response_bytes=0,
                    response_cardinality=0,
                    entity_category=entity_category,
                    payload_profile=str(operation["payload_profile"]),
                    response_profile=str(operation["response_profile"]),
                    client_kind=client.kind,
                )
            )
            recorder.logical_attempts_completed += 1
            recorder.physical_attempts_per_logical_peak = max(
                recorder.physical_attempts_per_logical_peak,
                1,
            )
            return

        physical_attempts = 0
        for physical_index in range(maximum_attempts):
            recorder.begin(client if physical_index == 0 else None)
            started = monotonic()
            status = 599
            response_bytes = 0
            response_value: Any = None
            try:
                if transport == "REST":
                    response = await client.http.request(method, path, **kwargs)
                    status = response.status_code
                    response_bytes = len(response.content)
                    if response.content:
                        try:
                            response_value = response.json()
                        except (ValueError, UnicodeDecodeError):
                            response_value = None
                else:
                    assert client.mcp is not None
                    result = await client.mcp.call_tool(
                        str(operation["operation"]), arguments=arguments
                    )
                    status, structured, response_bytes = _decode_tool_result(result)
                    response_value = structured
                    guidance_parsed = _update_agent_state(
                        client,
                        operation_id,
                        status,
                        structured,
                    )
                    if operation_id == "mcp_agent_get_my_work" and status == 200:
                        recorder.poll_guidance_responses += 1
                        if guidance_parsed:
                            recorder.poll_guidance_parsed += 1
            except Exception as exc:
                recorder.error(operation_id, exc)
            recorder.finish(
                Attempt(
                    operation_id=operation_id,
                    classification=classification,
                    status=status,
                    latency_ms=(monotonic() - started) * 1000,
                    request_bytes=request_bytes,
                    response_bytes=response_bytes,
                    response_cardinality=_response_cardinality(
                        str(operation["response_profile"]),
                        response_value,
                        status=status,
                    ),
                    entity_category=entity_category,
                    payload_profile=str(operation["payload_profile"]),
                    response_profile=str(operation["response_profile"]),
                    client_kind=client.kind,
                )
            )
            physical_attempts += 1
            if status not in RETRYABLE_STATUSES:
                break
            if physical_index + 1 >= maximum_attempts:
                if maximum_attempts > 1:
                    recorder.retry_exhausted += 1
                break
            assert retry_policy is not None
            recorder.retry_attempts += 1
            await asyncio.sleep(
                _retry_delay_seconds(
                    retry_policy,
                    seed=builder.seed,
                    logical_index=logical_index,
                    retry_index=physical_index,
                )
            )

        recorder.logical_attempts_completed += 1
        recorder.physical_attempts_per_logical_peak = max(
            recorder.physical_attempts_per_logical_peak,
            physical_attempts,
        )


async def _snapshot(client: httpx.AsyncClient) -> tuple[dict[str, Any] | None, str | None]:
    readiness: dict[str, Any] | None = None
    metrics: str | None = None
    try:
        response = await client.get("/health/ready")
        if response.headers.get("content-type", "").startswith("application/json"):
            value = response.json()
            readiness = value if isinstance(value, dict) else None
    except Exception:
        readiness = None
    try:
        response = await client.get("/metrics")
        if response.status_code == 200:
            metrics = response.text
    except Exception:
        metrics = None
    return readiness, metrics


def _select_browser_credentials(
    credentials: list[Mapping[str, Any]], count: int
) -> list[Mapping[str, Any]]:
    distribution = capacity_contract()["traffic"]["session_state_percent"]
    state_order = list(distribution)
    exact = [count * float(distribution[state]) / 100 for state in state_order]
    counts = [math.floor(value) for value in exact]
    remainder = count - sum(counts)
    order = sorted(
        range(len(state_order)),
        key=lambda index: (exact[index] - counts[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        counts[index] += 1
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for credential in credentials:
        grouped[str(credential.get("state"))].append(credential)
    selected: list[Mapping[str, Any]] = []
    for state, desired in zip(state_order, counts):
        if len(grouped[state]) < desired:
            raise QualificationInputError(
                f"Only {len(grouped[state])} browser credentials are in state {state}; "
                f"{desired} are required"
            )
        selected.extend(grouped[state][:desired])
    random.Random(20260718 + count).shuffle(selected)
    return selected


async def _run_live(
    *,
    args: argparse.Namespace,
    profile: Mapping[str, Any],
    credentials: Mapping[str, Any],
    duration: float,
    target_rps: float,
    target_clients: int,
    seed: int,
) -> tuple[Recorder, dict[str, Any], float, list[Mapping[str, Any]]]:
    browser_credentials = list(credentials["browsers"])
    agent_credentials = list(credentials["agents"])
    profile_id = str(profile["id"])
    if profile_id == "human_peak_v1":
        desired_agents = 0
        desired_browsers = target_clients
    elif profile_id == "external_llm_wait_v1":
        desired_agents = 0
        desired_browsers = target_clients
    else:
        desired_agents = min(
            int(capacity_contract()["identity_claim"]["concurrent_agent_clients"]),
            len(agent_credentials),
            target_clients,
        )
        desired_browsers = target_clients - desired_agents
    if not browser_credentials and desired_browsers:
        raise QualificationInputError("Browser credentials are empty")
    if not agent_credentials and desired_agents:
        raise QualificationInputError("Agent credentials are empty")
    browser_selected = _select_browser_credentials(
        browser_credentials, desired_browsers
    )
    agent_selected = [
        agent_credentials[index % len(agent_credentials)]
        for index in range(desired_agents)
    ]
    assignment_capacity = int(
        credentials.get("assignment_capacity", max(1, desired_agents * 600))
    )
    clients = [
        VirtualClient(
            kind="browser",
            credential=credential,
            base_url=args.base_url,
            cookie_name=str(credentials["cookie_name"]),
            timeout=args.request_timeout_seconds,
            actor_count=max(1, len(agent_credentials)),
            assignment_capacity=assignment_capacity,
        )
        for credential in browser_selected
    ]
    agents = [
        VirtualClient(
            kind="agent",
            credential=credential,
            base_url=args.base_url,
            cookie_name=str(credentials["cookie_name"]),
            timeout=args.request_timeout_seconds,
            actor_count=max(1, len(agent_credentials)),
            assignment_capacity=assignment_capacity,
        )
        for credential in agent_selected
    ]
    all_clients = [*clients, *agents]
    monitor = httpx.AsyncClient(
        base_url=args.base_url,
        timeout=httpx.Timeout(args.request_timeout_seconds),
    )
    recorder = Recorder()
    recorder.session_state_counts.update(
        str(credential["state"]) for credential in browser_selected
    )
    operation_plan = _weighted_plan(
        list(profile["operations"]), round(duration * target_rps), seed
    )
    retry_policy = _validated_retry_policy(profile)
    builder = OperationBuilder(
        credentials,
        seed,
        entity_plan=_distribution_plan(
            capacity_contract()["traffic"]["entity_distribution_percent"],
            len(operation_plan),
            seed ^ 0xE1717,
        ),
        run_namespace=args.run_id,
    )
    client_counter: Counter[str] = Counter()
    try:
        ramp_started = monotonic()
        batch_size = 10 if profile_id == "connection_surge_v1" else 50
        for batch_start in range(0, len(all_clients), batch_size):
            if profile_id == "connection_surge_v1" and all_clients:
                target_elapsed = (
                    120.0 * batch_start / max(1, len(all_clients) - 1)
                )
                delay = target_elapsed - (monotonic() - ramp_started)
                if delay > 0:
                    await asyncio.sleep(delay)
            await asyncio.gather(
                *(
                    client.open(f"{args.base_url}/api/mcp")
                    for client in all_clients[batch_start : batch_start + batch_size]
                )
            )
        if profile_id == "connection_surge_v1":
            recorder.connection_ramp_seconds = monotonic() - ramp_started
        readiness_before, metrics_before = await _snapshot(monitor)
        run_started = monotonic()
        pending: set[asyncio.Task[None]] = set()
        randomizer = random.Random(seed ^ 0x5A17)
        raw_intervals = [
            randomizer.expovariate(target_rps) for _ in operation_plan
        ]
        raw_total = sum(raw_intervals) or 1
        scale = duration / raw_total
        scheduled_at = run_started

        async def sample_connections() -> None:
            while monotonic() - run_started <= duration or pending:
                recorder.open_connections_peak = max(
                    recorder.open_connections_peak,
                    sum(client.open_connection_count() for client in all_clients),
                )
                await asyncio.sleep(0.25)

        sampler = asyncio.create_task(sample_connections())
        for logical_index, (operation, raw_interval) in enumerate(
            zip(operation_plan, raw_intervals),
            start=1,
        ):
            scheduled_at += raw_interval * scale
            delay = scheduled_at - monotonic()
            if delay > 0:
                await asyncio.sleep(delay)
            task = asyncio.create_task(
                _perform_attempt(
                    operation,
                    builder=builder,
                    browser_clients=clients,
                    agent_clients=agents,
                    recorder=recorder,
                    client_counter=client_counter,
                    logical_index=logical_index,
                    retry_policy=retry_policy,
                )
            )
            pending.add(task)
            task.add_done_callback(pending.discard)
        if pending:
            await asyncio.gather(*pending)
        actual_duration = monotonic() - run_started
        await sampler
        recorder.poll_guidance_outstanding = sum(
            int(client.poll_guidance_outstanding) for client in agents
        )
        readiness_after, metrics_after = await _snapshot(monitor)
        snapshots = {
            "readiness_before": readiness_before,
            "readiness_after": readiness_after,
            "metrics_before": metrics_before,
            "metrics_after": metrics_after,
        }
        return recorder, snapshots, actual_duration, operation_plan
    finally:
        await monitor.aclose()
        await asyncio.gather(*(client.close() for client in all_clients), return_exceptions=True)


def _load_optional(path: Path | None, *, sealed: bool = True) -> dict[str, Any]:
    return read_json_object(path, sealed=sealed) if path else {}


def _load_external_metrics(path: Path | None) -> dict[str, Any]:
    document = _load_optional(path)
    metrics = document.get("metrics", document)
    if not isinstance(metrics, dict):
        raise QualificationInputError("External evidence metrics must be an object")
    return dict(metrics)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the WorkChord production-shaped public API load profile."
    )
    parser.add_argument(
        "--profile",
        choices=(
            "human_peak_v1",
            "mixed_peak_v1",
            "connection_surge_v1",
            "external_llm_wait_v1",
        ),
        required=True,
    )
    parser.add_argument("--phase", choices=tuple(PHASE_DEFAULTS), required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--authorize-host", required=True)
    parser.add_argument(
        "--environment", choices=("test", "rehearsal", "production"), required=True
    )
    parser.add_argument("--production-authorization")
    parser.add_argument("--change-id")
    parser.add_argument("--credentials", type=Path)
    parser.add_argument("--seed-manifest", type=Path)
    parser.add_argument("--release-manifest", type=Path)
    parser.add_argument("--external-metrics", type=Path)
    parser.add_argument("--integrity-evidence", type=Path)
    parser.add_argument(
        "--defer-external-evidence",
        action="store_true",
        help=(
            "Return success for a sealed client result whose only incomplete "
            "gates require post-run external evidence"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", default=f"load-{uuid4().hex}")
    parser.add_argument("--random-seed", type=int, default=20260718)
    parser.add_argument("--duration-seconds", type=float)
    parser.add_argument("--rps", type=float)
    parser.add_argument("--virtual-users", type=int)
    parser.add_argument("--request-timeout-seconds", type=float, default=30)
    parser.add_argument("--qualification-candidate", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        args.base_url = authorized_base_url(
            args.base_url,
            authorize_host=args.authorize_host,
            environment=args.environment,
            production_authorization=args.production_authorization,
            change_id=args.change_id,
        )
        contract = capacity_contract()
        profile = traffic_profile(contract, args.profile)
        if args.phase == "external_wait" and args.profile != "external_llm_wait_v1":
            raise QualificationInputError(
                "external_wait phase requires external_llm_wait_v1"
            )
        if args.profile == "external_llm_wait_v1" and args.phase not in {
            "dry",
            "small",
            "external_wait",
        }:
            raise QualificationInputError(
                "external_llm_wait_v1 supports only dry, small, or external_wait"
            )
        duration, target_rps = _phase_shape(
            profile,
            args.phase,
            duration_override=args.duration_seconds,
            rps_override=args.rps,
        )
        declared_clients = int(
            profile.get("virtual_users") or profile.get("concurrent_calls") or 0
        )
        target_clients = args.virtual_users or declared_clients
        if args.phase == "small" and args.virtual_users is None:
            target_clients = min(10, declared_clients)
        if args.phase == "dry":
            target_clients = declared_clients
        if target_clients < 1 and args.phase != "dry":
            raise QualificationInputError("At least one virtual client is required")
        if args.qualification_candidate and (
            args.phase in {"dry", "small"}
            or args.duration_seconds is not None
            or args.rps is not None
            or args.virtual_users is not None
        ):
            raise QualificationInputError(
                "Qualification candidates cannot override phase duration, rate, or clients"
            )
        if args.defer_external_evidence and (
            args.phase == "dry"
            or args.external_metrics is not None
            or args.integrity_evidence is not None
        ):
            raise QualificationInputError(
                "Deferred external evidence requires a live run without preloaded evidence"
            )

        seed_manifest = (
            read_json_object(args.seed_manifest, sealed=True)
            if args.seed_manifest
            else None
        )
        credentials = (
            read_json_object(args.credentials, sealed=True)
            if args.credentials
            else None
        )
        if args.phase != "dry" and (seed_manifest is None or credentials is None):
            raise QualificationInputError(
                "Live load requires --seed-manifest and --credentials"
            )
        if seed_manifest and credentials:
            if sha256_file(args.credentials) != seed_manifest.get("credentials_sha256"):
                raise QualificationInputError(
                    "Credentials file differs from the seed manifest"
                )
            credentials = dict(credentials)
            credentials["assignment_capacity"] = int(
                seed_manifest.get("derived_cardinalities", {}).get(
                    "agent_assignments", 0
                )
            )
        release = _load_optional(args.release_manifest)
        external_metrics = _load_external_metrics(args.external_metrics)
        integrity = _load_optional(args.integrity_evidence)
        if args.qualification_candidate and not release:
            raise QualificationInputError(
                "Qualification candidate requires a sealed release manifest"
            )

        if args.phase == "dry":
            recorder = Recorder()
            snapshots = {
                "readiness_before": None,
                "readiness_after": None,
                "metrics_before": None,
                "metrics_after": None,
            }
            actual_duration = 0.0
            plan: list[Mapping[str, Any]] = []
        else:
            assert credentials is not None
            recorder, snapshots, actual_duration, plan = asyncio.run(
                _run_live(
                    args=args,
                    profile=profile,
                    credentials=credentials,
                    duration=duration,
                    target_rps=target_rps,
                    target_clients=target_clients,
                    seed=args.random_seed,
                )
            )
        payload = _result_payload(
            args=args,
            contract=contract,
            seed_manifest=seed_manifest,
            release=release,
            duration=duration,
            target_rps=target_rps,
            target_clients=target_clients,
            actual_duration=actual_duration,
            recorder=recorder,
            snapshots=snapshots,
            external_metrics=external_metrics,
            integrity=integrity,
            operation_plan=plan,
        )
        document = write_result(args.output, payload)
        print(
            f"Load result status={document['status']} run={document['run_id']} "
            f"sha256={document['document_sha256']}"
        )
        if args.defer_external_evidence and document["status"] == "incomplete":
            missing = {
                name
                for name, gate in document["gates"].items()
                if gate.get("status") == "missing"
            }
            external_gate_names = set(evaluate_external_gates({}, {}))
            if missing and missing.issubset(external_gate_names):
                print(
                    "Client workload gates passed; external evidence is deferred "
                    "to scripts/load/finalize.py"
                )
                return 0
        return 0 if document["status"] in {"passed", "dry_run"} else 2
    except (QualificationInputError, httpx.HTTPError) as exc:
        print(f"Load run refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
