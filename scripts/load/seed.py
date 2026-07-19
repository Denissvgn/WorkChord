#!/usr/bin/env python3
"""Create the deterministic, resumable PostgreSQL qualification data set."""

from __future__ import annotations

import argparse
import base64
from datetime import UTC, datetime, timedelta
import hashlib
import math
import os
from pathlib import Path
import sys
from typing import Any, Callable, Mapping

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Connection, Engine, make_url

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    CAPACITY_CONTRACT_PATH,
    QualificationInputError,
    atomic_write_json,
    capacity_contract,
    contract_sha256,
    read_json_object,
    sha256_file,
    utc_now_text,
)


SEED_SCHEMA_VERSION = 1
FIXED_TIME = "2026-07-18T00:00:00+00:00"
TARGET_TABLES = (
    "calendars",
    "projects",
    "iterations",
    "team_members",
    "vacations",
    "tasks",
    "task_dependencies",
    "user_sessions",
    "task_status_logs",
    "agent_actors",
    "agent_task_assignments",
    "agent_runs",
    "agent_run_events",
    "outbound_webhook_events",
    "outbound_webhook_deliveries",
)
SEQUENCED_TABLES = TARGET_TABLES


SMALL_CARDINALITIES = {
    "browser_identities": 25,
    "projects": 5,
    "iterations": 20,
    "tasks": 500,
    "task_status_audit_events": 2_000,
    "agent_run_events": 4_000,
    "outbound_delivery_rows": 500,
    "hot_iteration_tasks": 50,
    "hot_iteration_dependency_edges": 75,
    "hot_project_linked_tasks": 100,
}


def _token(seed: int, kind: str, index: int, *, prefix: str = "") -> str:
    digest = hashlib.sha256(f"{seed}:{kind}:{index}".encode("utf-8")).digest()
    encoded = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    return f"{prefix}{encoded}"


def _token_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _profile_cardinalities(profile: str) -> dict[str, int]:
    if profile == "small":
        return dict(SMALL_CARDINALITIES)
    contract = capacity_contract()
    return {
        key: int(value)
        for key, value in contract["seed"]["cardinalities"].items()
    }


def _derived_cardinalities(cardinalities: Mapping[str, int]) -> dict[str, int]:
    agent_clients = int(capacity_contract()["identity_claim"]["concurrent_agent_clients"])
    if cardinalities["browser_identities"] < 100:
        agent_clients = 5
    runs = math.ceil(cardinalities["agent_run_events"] / 10)
    assignment_capacity = max(
        0,
        cardinalities["tasks"] - cardinalities["hot_project_linked_tasks"],
    )
    assignments = min(assignment_capacity, agent_clients * 600)
    return {
        "agent_actors": agent_clients,
        "agent_runs": runs,
        "agent_assignments": assignments,
        "outbound_webhook_events": cardinalities["outbound_delivery_rows"],
        "team_members": cardinalities["iterations"] * 2,
        "vacations": max(1, cardinalities["iterations"] // 5),
    }


def _target_identifier(database_url: str) -> str:
    url = make_url(database_url)
    return f"{url.host or 'local-socket'}:{url.port or 5432}/{url.database}"


def _validate_target(database_url: str, authorized_target: str) -> str:
    url = make_url(database_url)
    if url.drivername != "postgresql+psycopg":
        raise QualificationInputError(
            "Qualification seed requires postgresql+psycopg"
        )
    environment = os.getenv("DEPLOYMENT_ENVIRONMENT", "").strip().lower()
    if environment not in {"test", "rehearsal"}:
        raise QualificationInputError(
            "Qualification seed is prohibited outside test or rehearsal"
        )
    database_name = url.database or ""
    if not database_name.startswith(("workchord_test_", "workchord_qualification_")):
        raise QualificationInputError(
            "Qualification seed requires an isolated workchord_test_* or "
            "workchord_qualification_* database"
        )
    actual = _target_identifier(database_url)
    if actual != authorized_target:
        raise QualificationInputError(
            f"Resolved target {actual!r} differs from --authorize-target"
        )
    return actual


def _empty_checkpoint(
    *, profile: str, seed: int, target: str, as_of: str
) -> dict[str, Any]:
    return {
        "kind": "workchord-qualification-seed-checkpoint",
        "schema_version": SEED_SCHEMA_VERSION,
        "profile": profile,
        "seed": seed,
        "target_identifier": target,
        "as_of": as_of,
        "capacity_contract_sha256": contract_sha256(),
        "stages": {},
        "complete": False,
        "updated_at": utc_now_text(),
    }


def _load_checkpoint(
    path: Path, *, profile: str, seed: int, target: str, as_of: str
) -> dict[str, Any]:
    if not path.exists():
        return _empty_checkpoint(
            profile=profile, seed=seed, target=target, as_of=as_of
        )
    checkpoint = read_json_object(path, sealed=True)
    expected = {
        "kind": "workchord-qualification-seed-checkpoint",
        "schema_version": SEED_SCHEMA_VERSION,
        "profile": profile,
        "seed": seed,
        "target_identifier": target,
        "as_of": as_of,
        "capacity_contract_sha256": contract_sha256(),
    }
    differences = {
        key: (checkpoint.get(key), value)
        for key, value in expected.items()
        if checkpoint.get(key) != value
    }
    if differences:
        raise QualificationInputError(
            f"Seed checkpoint identity differs: {differences}"
        )
    if not isinstance(checkpoint.get("stages"), dict):
        raise QualificationInputError("Seed checkpoint stages must be an object")
    return checkpoint


def _save_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    payload = dict(checkpoint)
    payload.pop("document_sha256", None)
    payload["updated_at"] = utc_now_text()
    written = atomic_write_json(path, payload)
    checkpoint.clear()
    checkpoint.update(written)


def _count(connection: Connection, table: str) -> int:
    if table not in TARGET_TABLES:
        raise QualificationInputError(f"Unsupported seed table: {table}")
    return int(connection.execute(text(f'SELECT count(*) FROM "{table}"')).scalar_one())


def _require_initial_target(
    connection: Connection,
    checkpoint: Mapping[str, Any],
) -> None:
    from app.services.upgrade_service import head_revision

    inspector = inspect(connection)
    actual_tables = set(inspector.get_table_names())
    required = set(TARGET_TABLES) | {"alembic_version"}
    if not required.issubset(actual_tables):
        raise QualificationInputError(
            f"Target is not a WorkChord schema; missing={sorted(required - actual_tables)}"
        )
    revisions = list(
        connection.execute(
            text("SELECT version_num FROM alembic_version ORDER BY version_num")
        ).scalars()
    )
    if revisions != [head_revision()]:
        raise QualificationInputError(
            f"Target must be at packaged Alembic head {head_revision()}; found {revisions}"
        )
    if not checkpoint["stages"]:
        nonempty = {table: _count(connection, table) for table in TARGET_TABLES}
        nonempty = {table: count for table, count in nonempty.items() if count}
        if nonempty:
            raise QualificationInputError(
                f"Uncheckpointed qualification target is not empty: {nonempty}"
            )


def _record_stage(
    checkpoint_path: Path,
    checkpoint: dict[str, Any],
    stage: str,
    completed: int,
) -> None:
    checkpoint["stages"][stage] = completed
    _save_checkpoint(checkpoint_path, checkpoint)


def _single_stage(
    engine: Engine,
    checkpoint_path: Path,
    checkpoint: dict[str, Any],
    *,
    stage: str,
    expected: int,
    action: Callable[[Connection], None],
) -> None:
    recorded = int(checkpoint["stages"].get(stage, 0))
    with engine.connect() as connection:
        actual = _count(connection, stage)
    if actual == expected:
        if recorded != expected:
            _record_stage(checkpoint_path, checkpoint, stage, expected)
        return
    if recorded or actual:
        raise QualificationInputError(
            f"Non-resumable partial stage {stage}: checkpoint={recorded}, rows={actual}"
        )
    with engine.begin() as connection:
        action(connection)
        actual = _count(connection, stage)
        if actual != expected:
            raise QualificationInputError(
                f"Seed stage {stage} produced {actual}, expected {expected}"
            )
    _record_stage(checkpoint_path, checkpoint, stage, expected)


def _chunk_stage(
    engine: Engine,
    checkpoint_path: Path,
    checkpoint: dict[str, Any],
    *,
    stage: str,
    expected: int,
    chunk_size: int,
    action: Callable[[Connection, int, int], None],
) -> None:
    recorded = int(checkpoint["stages"].get(stage, 0))
    with engine.connect() as connection:
        actual = _count(connection, stage)
    if actual < recorded or actual > expected:
        raise QualificationInputError(
            f"Seed stage {stage} drifted: checkpoint={recorded}, rows={actual}, expected={expected}"
        )
    completed = actual
    if completed != recorded:
        _record_stage(checkpoint_path, checkpoint, stage, completed)
    while completed < expected:
        end = min(expected, completed + chunk_size)
        with engine.begin() as connection:
            action(connection, completed + 1, end)
            actual = _count(connection, stage)
            if actual != end:
                raise QualificationInputError(
                    f"Seed stage {stage} produced {actual}, expected checkpoint {end}"
                )
        completed = end
        _record_stage(checkpoint_path, checkpoint, stage, completed)


def _insert_calendar(connection: Connection) -> None:
    connection.execute(
        text(
            "INSERT INTO calendars "
            "(id, name, year, holidays, weekend_days, short_days) VALUES "
            "(1, 'Qualification calendar', 2026, "
            "CAST('[]' AS JSON), CAST('[5,6]' AS JSON), CAST('[]' AS JSON))"
        )
    )


def _insert_projects(connection: Connection, count: int) -> None:
    connection.execute(
        text(
            "INSERT INTO projects "
            "(id, name, description, status, health, sort_order, created_at, updated_at) "
            "SELECT value, 'Qualification project ' || value, "
            "'Deterministic production-shaped qualification project', "
            "'active', 'on_track', value, CAST(:fixed_time AS timestamptz), "
            "CAST(:fixed_time AS timestamptz) "
            "FROM generate_series(1::integer, CAST(:count AS integer)) value"
        ),
        {"count": count, "fixed_time": FIXED_TIME},
    )


def _insert_iterations(connection: Connection, count: int, projects: int) -> None:
    connection.execute(
        text(
            "INSERT INTO iterations "
            "(id, name, start_date, end_date, calendar_id, project_id) "
            "SELECT value, 'Qualification iteration ' || value, "
            "DATE '2026-01-01' + ((value - 1) % 365), "
            "DATE '2026-01-14' + ((value - 1) % 365), 1, "
            "1 + ((value - 1) % :projects) "
            "FROM generate_series(1::integer, CAST(:count AS integer)) value"
        ),
        {"count": count, "projects": projects},
    )


def _insert_team_members(connection: Connection, count: int) -> None:
    connection.execute(
        text(
            "INSERT INTO team_members "
            "(id, name, position, availability_percent, "
            "professionalism_coefficient, operational_utilization, iteration_id) "
            "SELECT value, 'Qualification member ' || value, 'Engineer', "
            "90.0, 1.0, 20.0, 1 + ((value - 1) / 2) "
            "FROM generate_series(1::integer, CAST(:count AS integer)) value"
        ),
        {"count": count},
    )


def _insert_vacations(connection: Connection, count: int, members: int) -> None:
    connection.execute(
        text(
            "INSERT INTO vacations (id, start_date, end_date, team_member_id) "
            "SELECT value, DATE '2026-06-01' + ((value - 1) % 30), "
            "DATE '2026-06-02' + ((value - 1) % 30), "
            "1 + ((value * 10 - 1) % :members) "
            "FROM generate_series(1::integer, CAST(:count AS integer)) value"
        ),
        {"count": count, "members": members},
    )


def _insert_tasks(
    connection: Connection,
    start: int,
    end: int,
    *,
    projects: int,
    iterations: int,
    hot_iteration_tasks: int,
    hot_project_tasks: int,
) -> None:
    connection.execute(
        text(
            "INSERT INTO tasks ("
            "id, title, description, priority, effort_days, effort_hours, status, "
            "start_date, end_date, calculated_effort_days, is_optional, is_deferred, "
            "tags, sort_order, version, claim_generation, updated_at, iteration_id, "
            "project_id, assignee_id"
            ") WITH generated AS ("
            "SELECT value, CASE "
            "WHEN value <= :hot_iteration_tasks THEN 1 "
            "WHEN value <= :hot_project_tasks THEN "
            "1 + (1 + ((value - :hot_iteration_tasks - 1) % "
            "GREATEST(1, ((:iterations - 1) / :projects)))) * :projects "
            "ELSE 2 + ((value - :hot_project_tasks - 1) % (:iterations - 1)) END "
            "AS iteration_id FROM generate_series("
            "CAST(:start AS integer), CAST(:end AS integer)) value"
            ") SELECT value, 'Qualification task ' || value, "
            "'Scope: execute a deterministic WorkChord qualification item. ' || "
            "'Acceptance: preserve concurrency and integrity. ' || "
            "'Verification: report exact API and database evidence.', "
            "1 + ((value - 1) % 10), 1.0, 8.0, 'planned', "
            "DATE '2026-01-01' + ((value - 1) % 365), "
            "DATE '2026-01-02' + ((value - 1) % 365), 1.0, false, false, "
            "'[\"agent\",\"cap:code\",\"qualification\"]', value, 1, 0, "
            "CAST(:fixed_time AS timestamptz), "
            "iteration_id, 1 + ((iteration_id - 1) % :projects), "
            "1 + ((iteration_id - 1) * 2) + ((value - 1) % 2) FROM generated"
        ),
        {
            "start": start,
            "end": end,
            "projects": projects,
            "iterations": iterations,
            "hot_iteration_tasks": hot_iteration_tasks,
            "hot_project_tasks": hot_project_tasks,
            "fixed_time": FIXED_TIME,
        },
    )


def _dependency_edges(task_count: int, edge_count: int) -> list[dict[str, int]]:
    if task_count < 2:
        return []
    edges: list[tuple[int, int]] = []
    distance = 1
    while len(edges) < edge_count and distance < task_count:
        for task_id in range(distance + 1, task_count + 1):
            edges.append((task_id, task_id - distance))
            if len(edges) == edge_count:
                break
        distance += 1
    if len(edges) != edge_count:
        raise QualificationInputError(
            f"Cannot create {edge_count} unique acyclic edges for {task_count} tasks"
        )
    return [
        {"id": index, "task_id": task_id, "depends_on_id": depends_on_id}
        for index, (task_id, depends_on_id) in enumerate(edges, start=1)
    ]


def _insert_dependencies(
    connection: Connection, hot_tasks: int, edge_count: int
) -> None:
    connection.execute(
        text(
            "INSERT INTO task_dependencies (id, task_id, depends_on_id) "
            "VALUES (:id, :task_id, :depends_on_id)"
        ),
        _dependency_edges(hot_tasks, edge_count),
    )


def _session_rows(
    seed: int,
    count: int,
    *,
    as_of: str = FIXED_TIME,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reference = datetime.fromisoformat(as_of)
    if reference.tzinfo is None:
        raise QualificationInputError("Seed --as-of must include a timezone")
    distribution = [
        ("new", 5),
        ("active", 75),
        ("nearly_expired", 10),
        ("expired", 5),
        ("revoked", 5),
    ]
    exact = [count * percent / 100 for _, percent in distribution]
    counts = [math.floor(value) for value in exact]
    remainder = count - sum(counts)
    order = sorted(
        range(len(distribution)),
        key=lambda index: (exact[index] - counts[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        counts[index] += 1
    states = [
        state
        for (state, _percent), state_count in zip(distribution, counts)
        for _ in range(state_count)
    ]
    database_rows: list[dict[str, Any]] = []
    credentials: list[dict[str, Any]] = []
    for index in range(1, count + 1):
        state = states[index - 1]
        token = _token(seed, "browser", index)
        expires_at = (reference + timedelta(days=30)).isoformat()
        revoked_at = None
        if state == "nearly_expired":
            expires_at = (reference + timedelta(minutes=5)).isoformat()
        elif state == "expired":
            expires_at = (reference - timedelta(days=1)).isoformat()
        elif state == "revoked":
            revoked_at = reference.isoformat()
        public_id = hashlib.sha256(
            f"{seed}:public:{index}".encode("utf-8")
        ).hexdigest()[:12]
        database_rows.append(
            {
                "id": index,
                "public_id": public_id,
                "token_hash": _token_hash(token),
                "ip_address": f"198.51.{(index // 254) % 255}.{1 + (index % 254)}",
                "user_agent": "WorkChordQualification/1",
                "created_at": (reference - timedelta(days=1)).isoformat(),
                "last_seen_at": reference.isoformat(),
                "expires_at": expires_at,
                "revoked_at": revoked_at,
            }
        )
        credentials.append(
            {"id": index, "public_id": public_id, "token": token, "state": state}
        )
    return database_rows, credentials


def _insert_sessions(connection: Connection, rows: list[dict[str, Any]]) -> None:
    connection.execute(
        text(
            "INSERT INTO user_sessions "
            "(id, public_id, session_token_hash, ip_address, user_agent, created_at, "
            "last_seen_at, expires_at, revoked_at) VALUES "
            "(:id, :public_id, :token_hash, :ip_address, :user_agent, "
            "CAST(:created_at AS timestamptz), CAST(:last_seen_at AS timestamptz), "
            "CAST(:expires_at AS timestamptz), CAST(:revoked_at AS timestamptz))"
        ),
        rows,
    )


def _insert_status_logs(
    connection: Connection, start: int, end: int, tasks: int
) -> None:
    connection.execute(
        text(
            "INSERT INTO task_status_logs "
            "(id, task_id, from_status, to_status, changed_at, reason, triggered_by, "
            "affected_task_ids) SELECT value, 1 + ((value - 1) % :tasks), "
            "CASE WHEN value % 2 = 0 THEN 'planned' ELSE 'active' END, "
            "CASE WHEN value % 2 = 0 THEN 'active' ELSE 'resolved' END, "
            "CAST(:fixed_time AS timestamptz) - ((value % 730) * INTERVAL '1 day'), "
            "'qualification history', 'system', '[]' "
            "FROM generate_series(CAST(:start AS integer), CAST(:end AS integer)) value"
        ),
        {"start": start, "end": end, "tasks": tasks, "fixed_time": FIXED_TIME},
    )


def _actor_rows(seed: int, count: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    database_rows: list[dict[str, Any]] = []
    credentials: list[dict[str, Any]] = []
    scopes = (
        '["assignments:read","tasks:read","verification:read",'
        '"verification:write","work:execute","events:write","runs:write"]'
    )
    for index in range(1, count + 1):
        api_key = _token(seed, "agent", index, prefix="wq_")
        database_rows.append(
            {
                "id": index,
                "name": f"qualification-agent-{index:04d}",
                "display_name": f"Qualification Agent {index:04d}",
                "api_key_hash": _token_hash(api_key),
                "scopes": scopes,
                "created_at": FIXED_TIME,
            }
        )
        credentials.append(
            {
                "id": index,
                "name": f"qualification-agent-{index:04d}",
                "api_key": api_key,
            }
        )
    return database_rows, credentials


def _insert_actors(connection: Connection, rows: list[dict[str, Any]]) -> None:
    connection.execute(
        text(
            "INSERT INTO agent_actors "
            "(id, name, display_name, api_key_hash, scopes, enabled, role, work_policy, "
            "max_parallel_work, queue_revision, created_at) VALUES "
            "(:id, :name, :display_name, :api_key_hash, :scopes, true, 'worker', "
            "'assigned_only', 1, 1, CAST(:created_at AS timestamptz))"
        ),
        rows,
    )


def _insert_agent_runs(
    connection: Connection,
    start: int,
    end: int,
    *,
    tasks: int,
    actors: int,
) -> None:
    connection.execute(
        text(
            "INSERT INTO agent_runs "
            "(id, task_id, actor_id, status, model, tool_name, run_metadata, "
            "artifact_links, summary, started_at, ended_at) SELECT value, "
            "1 + ((value - 1) % :tasks), 1 + ((value - 1) % :actors), 'completed', "
            "'qualification-model', 'qualification-runner', '{}', '[]', "
            "'deterministic historical run', "
            "CAST(:fixed_time AS timestamptz) - ((value % 365) * INTERVAL '1 day'), "
            "CAST(:fixed_time AS timestamptz) - ((value % 365) * INTERVAL '1 day') "
            "+ INTERVAL '1 minute' FROM generate_series("
            "CAST(:start AS integer), CAST(:end AS integer)) value"
        ),
        {
            "start": start,
            "end": end,
            "tasks": tasks,
            "actors": actors,
            "fixed_time": FIXED_TIME,
        },
    )


def _insert_agent_events(
    connection: Connection, start: int, end: int, runs: int
) -> None:
    connection.execute(
        text(
            "INSERT INTO agent_run_events "
            "(id, run_id, event_type, message, payload, trace_id, correlation_id, created_at) "
            "SELECT value, 1 + ((value - 1) % :runs), 'progress', "
            "'qualification event', json_build_object('progress', 50), "
            "'trace-' || value, 'qualification-' || value, "
            "CAST(:fixed_time AS timestamptz) - ((value % 365) * INTERVAL '1 day') "
            "FROM generate_series(CAST(:start AS integer), CAST(:end AS integer)) value"
        ),
        {"start": start, "end": end, "runs": runs, "fixed_time": FIXED_TIME},
    )


def _insert_outbound_events(connection: Connection, start: int, end: int, tasks: int) -> None:
    connection.execute(
        text(
            "INSERT INTO outbound_webhook_events "
            "(id, event_id, event_type, entity_type, entity_id, payload_json, occurred_at) "
            "SELECT value, lpad(to_hex(value), 64, '0'), 'task.updated', 'task', "
            "1 + ((value - 1) % :tasks), json_build_object('qualification', true), "
            "CAST(:fixed_time AS timestamptz) - ((value % 180) * INTERVAL '1 day') "
            "FROM generate_series(CAST(:start AS integer), CAST(:end AS integer)) value"
        ),
        {"start": start, "end": end, "tasks": tasks, "fixed_time": FIXED_TIME},
    )


def _insert_deliveries(connection: Connection, start: int, end: int) -> None:
    connection.execute(
        text(
            "INSERT INTO outbound_webhook_deliveries "
            "(id, event_id, target_name, target_url, channel, payload_json, status, "
            "attempt_count, max_attempts, last_http_status, terminal_at, delivered_at, "
            "created_at, updated_at) SELECT value, value, 'qualification-sink', "
            "'https://qualification.invalid/webhook', 'webhook', "
            "json_build_object('qualification', true), 'delivered', 1, 5, 204, "
            "CAST(:fixed_time AS timestamptz), CAST(:fixed_time AS timestamptz), "
            "CAST(:fixed_time AS timestamptz) - ((value % 90) * INTERVAL '1 day'), "
            "CAST(:fixed_time AS timestamptz) FROM generate_series("
            "CAST(:start AS integer), CAST(:end AS integer)) value"
        ),
        {"start": start, "end": end, "fixed_time": FIXED_TIME},
    )


def _insert_assignments(
    connection: Connection,
    count: int,
    *,
    tasks: int,
    actors: int,
) -> None:
    first_task = tasks - count + 1
    connection.execute(
        text(
            "INSERT INTO agent_task_assignments "
            "(id, task_id, actor_id, purpose, queue_class, state, queue_rank, "
            "task_version, routing_snapshot, reason, created_at, updated_at) "
            "SELECT value, :first_task + value - 1, 1 + ((value - 1) % :actors), "
            "'execution', 'normal', 'queued', value, 1, '{}', "
            "'qualification lifecycle assignment', CAST(:fixed_time AS timestamptz), "
            "CAST(:fixed_time AS timestamptz) FROM generate_series("
            "1::integer, CAST(:count AS integer)) value"
        ),
        {
            "first_task": first_task,
            "actors": actors,
            "count": count,
            "fixed_time": FIXED_TIME,
        },
    )


def _repair_sequences(connection: Connection) -> None:
    for table in SEQUENCED_TABLES:
        sequence = connection.execute(
            text("SELECT pg_get_serial_sequence(:table_name, 'id')"),
            {"table_name": table},
        ).scalar_one_or_none()
        if sequence is None:
            continue
        maximum = connection.execute(
            text(f'SELECT max(id) FROM "{table}"')
        ).scalar_one_or_none()
        if maximum is None:
            connection.execute(
                text("SELECT setval(CAST(:sequence AS regclass), 1, false)"),
                {"sequence": sequence},
            )
        else:
            connection.execute(
                text("SELECT setval(CAST(:sequence AS regclass), :value, true)"),
                {"sequence": sequence, "value": int(maximum)},
            )


def _database_facts(connection: Connection) -> dict[str, Any]:
    row = connection.execute(
        text(
            "SELECT current_setting('server_version'), current_database(), "
            "current_schema(), current_setting('TimeZone'), "
            "pg_database_size(current_database())"
        )
    ).one()
    table_sizes = {
        str(name): int(size)
        for name, size in connection.execute(
            text(
                "SELECT relname, pg_total_relation_size(relid) "
                "FROM pg_catalog.pg_statio_user_tables ORDER BY relname"
            )
        )
    }
    return {
        "postgresql_version": str(row[0]),
        "database": str(row[1]),
        "schema": str(row[2]),
        "timezone": str(row[3]),
        "database_size_bytes": int(row[4]),
        "table_total_bytes": table_sizes,
    }


def _write_credentials(
    path: Path,
    *,
    seed: int,
    browsers: list[dict[str, Any]],
    agents: list[dict[str, Any]],
    cardinalities: Mapping[str, int],
    agent_assignments: int,
) -> None:
    atomic_write_json(
        path,
        {
            "kind": "workchord-qualification-credentials",
            "schema_version": 1,
            "seed": seed,
            "cookie_name": "workchord_session",
            "browsers": browsers,
            "agents": agents,
            "entities": {
                "project_ids": [1, cardinalities["projects"]],
                "iteration_ids": [1, cardinalities["iterations"]],
                "task_ids": [1, cardinalities["tasks"]],
                "hot_project_id": 1,
                "hot_iteration_id": 1,
                "hot_iteration_tasks": cardinalities["hot_iteration_tasks"],
                "hot_project_linked_tasks": cardinalities[
                    "hot_project_linked_tasks"
                ],
                "agent_assignment_first_task_id": (
                    cardinalities["tasks"] - agent_assignments + 1
                ),
            },
        },
        mode=0o600,
    )


def seed_database(args: argparse.Namespace) -> dict[str, Any]:
    contract = capacity_contract()
    cardinalities = _profile_cardinalities(args.profile)
    derived = _derived_cardinalities(cardinalities)
    target = _validate_target(args.database_url, args.authorize_target)
    checkpoint = _load_checkpoint(
        args.checkpoint,
        profile=args.profile,
        seed=args.seed,
        target=target,
        as_of=args.as_of,
    )
    engine = create_engine(args.database_url, pool_pre_ping=True)
    session_rows, browser_credentials = _session_rows(
        args.seed,
        cardinalities["browser_identities"],
        as_of=args.as_of,
    )
    actor_rows, agent_credentials = _actor_rows(
        args.seed, derived["agent_actors"]
    )
    try:
        with engine.connect() as connection:
            _require_initial_target(connection, checkpoint)

        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="calendars",
            expected=1,
            action=_insert_calendar,
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="projects",
            expected=cardinalities["projects"],
            action=lambda connection: _insert_projects(
                connection, cardinalities["projects"]
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="iterations",
            expected=cardinalities["iterations"],
            action=lambda connection: _insert_iterations(
                connection,
                cardinalities["iterations"],
                cardinalities["projects"],
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="team_members",
            expected=derived["team_members"],
            action=lambda connection: _insert_team_members(
                connection, derived["team_members"]
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="vacations",
            expected=derived["vacations"],
            action=lambda connection: _insert_vacations(
                connection,
                derived["vacations"],
                derived["team_members"],
            ),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="tasks",
            expected=cardinalities["tasks"],
            chunk_size=args.chunk_size,
            action=lambda connection, start, end: _insert_tasks(
                connection,
                start,
                end,
                projects=cardinalities["projects"],
                iterations=cardinalities["iterations"],
                hot_iteration_tasks=cardinalities["hot_iteration_tasks"],
                hot_project_tasks=cardinalities["hot_project_linked_tasks"],
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="task_dependencies",
            expected=cardinalities["hot_iteration_dependency_edges"],
            action=lambda connection: _insert_dependencies(
                connection,
                cardinalities["hot_iteration_tasks"],
                cardinalities["hot_iteration_dependency_edges"],
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="user_sessions",
            expected=cardinalities["browser_identities"],
            action=lambda connection: _insert_sessions(connection, session_rows),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="task_status_logs",
            expected=cardinalities["task_status_audit_events"],
            chunk_size=args.chunk_size,
            action=lambda connection, start, end: _insert_status_logs(
                connection, start, end, cardinalities["tasks"]
            ),
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="agent_actors",
            expected=derived["agent_actors"],
            action=lambda connection: _insert_actors(connection, actor_rows),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="agent_runs",
            expected=derived["agent_runs"],
            chunk_size=args.chunk_size,
            action=lambda connection, start, end: _insert_agent_runs(
                connection,
                start,
                end,
                tasks=cardinalities["tasks"],
                actors=derived["agent_actors"],
            ),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="agent_run_events",
            expected=cardinalities["agent_run_events"],
            chunk_size=args.chunk_size,
            action=lambda connection, start, end: _insert_agent_events(
                connection, start, end, derived["agent_runs"]
            ),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="outbound_webhook_events",
            expected=derived["outbound_webhook_events"],
            chunk_size=args.chunk_size,
            action=lambda connection, start, end: _insert_outbound_events(
                connection, start, end, cardinalities["tasks"]
            ),
        )
        _chunk_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="outbound_webhook_deliveries",
            expected=cardinalities["outbound_delivery_rows"],
            chunk_size=args.chunk_size,
            action=_insert_deliveries,
        )
        _single_stage(
            engine,
            args.checkpoint,
            checkpoint,
            stage="agent_task_assignments",
            expected=derived["agent_assignments"],
            action=lambda connection: _insert_assignments(
                connection,
                derived["agent_assignments"],
                tasks=cardinalities["tasks"],
                actors=derived["agent_actors"],
            ),
        )
        with engine.begin() as connection:
            _repair_sequences(connection)
            connection.execute(text("ANALYZE"))
        checkpoint["complete"] = True
        _save_checkpoint(args.checkpoint, checkpoint)
        _write_credentials(
            args.credentials,
            seed=args.seed,
            browsers=browser_credentials,
            agents=agent_credentials,
            cardinalities=cardinalities,
            agent_assignments=derived["agent_assignments"],
        )
        with engine.connect() as connection:
            actual = {table: _count(connection, table) for table in TARGET_TABLES}
            hot_iteration = int(
                connection.execute(
                    text("SELECT count(*) FROM tasks WHERE iteration_id = 1")
                ).scalar_one()
            )
            hot_project = int(
                connection.execute(
                    text("SELECT count(*) FROM tasks WHERE project_id = 1")
                ).scalar_one()
            )
            database_facts = _database_facts(connection)
    finally:
        engine.dispose()

    if hot_iteration != cardinalities["hot_iteration_tasks"]:
        raise QualificationInputError(
            f"Hot iteration has {hot_iteration}, expected {cardinalities['hot_iteration_tasks']}"
        )
    if hot_project < cardinalities["hot_project_linked_tasks"]:
        raise QualificationInputError(
            f"Hot project has {hot_project}, expected at least "
            f"{cardinalities['hot_project_linked_tasks']}"
        )
    manifest = atomic_write_json(
        args.manifest,
        {
            "kind": "workchord-qualification-seed-manifest",
            "schema_version": SEED_SCHEMA_VERSION,
            "profile": args.profile,
            "qualification_eligible": args.profile == "full",
            "seed": args.seed,
            "as_of": args.as_of,
            "created_at": utc_now_text(),
            "target_identifier": target,
            "capacity_contract": str(CAPACITY_CONTRACT_PATH.relative_to(CAPACITY_CONTRACT_PATH.parents[2])),
            "capacity_contract_sha256": contract_sha256(),
            "declared_cardinalities": cardinalities,
            "derived_cardinalities": derived,
            "actual_table_rows": actual,
            "hot_iteration_tasks": hot_iteration,
            "hot_project_linked_tasks": hot_project,
            "credentials_sha256": sha256_file(args.credentials),
            "database": database_facts,
        },
    )
    return manifest


def _dry_manifest(args: argparse.Namespace) -> dict[str, Any]:
    cardinalities = _profile_cardinalities(args.profile)
    manifest = {
        "kind": "workchord-qualification-seed-plan",
        "schema_version": SEED_SCHEMA_VERSION,
        "profile": args.profile,
        "qualification_eligible": args.profile == "full",
        "seed": args.seed,
        "capacity_contract_sha256": contract_sha256(),
        "declared_cardinalities": cardinalities,
        "derived_cardinalities": _derived_cardinalities(cardinalities),
        "production_execution_allowed": False,
    }
    if args.manifest:
        return atomic_write_json(args.manifest, manifest)
    return manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seed an isolated PostgreSQL qualification database."
    )
    parser.add_argument("--profile", choices=("small", "full"), required=True)
    parser.add_argument("--seed", type=int, default=20260718)
    parser.add_argument(
        "--as-of",
        help="Timezone-aware deterministic reference time for session states",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    parser.add_argument("--authorize-target")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--credentials", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--chunk-size", type=int, default=50_000)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if not 1_000 <= args.chunk_size <= 250_000:
            raise QualificationInputError(
                "--chunk-size must be between 1000 and 250000"
            )
        if args.dry_run:
            document = _dry_manifest(args)
        else:
            required = {
                "--database-url": args.database_url,
                "--authorize-target": args.authorize_target,
                "--checkpoint": args.checkpoint,
                "--credentials": args.credentials,
                "--manifest": args.manifest,
                "--as-of": args.as_of,
            }
            missing = [name for name, value in required.items() if not value]
            if missing:
                raise QualificationInputError(
                    f"Live seed requires: {', '.join(missing)}"
                )
            document = seed_database(args)
        print(
            f"Seed {document['kind']} profile={args.profile} "
            f"sha256={document.get('document_sha256', 'dry-stdout')}"
        )
        return 0
    except QualificationInputError as exc:
        print(f"Qualification seed refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
