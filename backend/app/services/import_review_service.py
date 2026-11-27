"""Review a JSON plan import before it is applied, and apply only what was reviewed.

A dry run executes the real import writer inside a rollback-only command and
reports the difference between the target iteration before and after it, so
the proposal and the eventual write cannot drift apart. The review digest binds
three things: the canonical import file, the revisions of every iteration the
import reserves, and the exact change set. A write that carries the digest runs
the same writer, recomputes all three and is refused, and rolled back, unless
each one still matches.
"""

from contextlib import contextmanager
from dataclasses import replace
import hashlib
import json
import re
from typing import Any

from fastapi import HTTPException
from sqlalchemy import event, func, select

from app.authority import Authority, internal_authority, require_project
from app.commands import AggregateVersionConflict, PlanningConflict, current_command


REVIEW_DIGEST_VERSION = "ipr1"
_DIGEST_PATTERN = re.compile(rf"^{REVIEW_DIGEST_VERSION}:([0-9a-f]{{64}}):([0-9a-f]{{64}}):([0-9a-f]{{64}})$")

TASK_FIELDS = (
    "parent_id", "title", "description", "status", "priority", "effort_hours", "effort_days",
    "assignee_id", "owner_profile_id", "project_id", "milestone_id", "is_summary", "is_optional",
    "is_deferred", "tags", "sort_order", "brief", "execution_mode",
)
DATE_FIELDS = (
    "start_date", "end_date", "actual_start_date", "actual_end_date", "min_start_date",
    "max_end_date", "baseline_start_date", "baseline_end_date",
)
LINK_FIELDS = ("external_key", "source", "source_url")
MEMBER_FIELDS = (
    "name", "position", "email", "availability_percent", "professionalism_coefficient",
    "operational_utilization", "profile_id",
)
ITERATION_FIELDS = ("name", "start_date", "end_date", "calendar_id", "project_id")
EXTERNAL_LINK_FIELDS = ("provider", "external_key", "url", "title")


class ImportReviewRefused(PlanningConflict):
    """A reviewed import no longer matches what the reviewer saw."""


def _canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()


def _sha256(value) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def target_sha256(iteration_id, revisions: dict) -> str:
    """Digest of the import target and the revision of every iteration it reserves."""
    return _sha256({"iteration_id": iteration_id, "revisions": {str(key): value for key, value in sorted(revisions.items())}})


def changes_sha256(changes: dict) -> str:
    return _sha256(changes)


def compose_review_digest(file_sha: str, target_sha: str, change_sha: str) -> str:
    return f"{REVIEW_DIGEST_VERSION}:{file_sha}:{target_sha}:{change_sha}"


def parse_review_digest(value: str) -> tuple[str, str, str]:
    match = _DIGEST_PATTERN.fullmatch(value.strip()) if isinstance(value, str) else None
    if match is None:
        raise HTTPException(status_code=422, detail={
            "code": "import_review_digest_invalid",
            "message": "review_digest must be the review_digest returned by the plan-import dry run.",
        })
    return match.group(1), match.group(2), match.group(3)


def validate_import_payload(data) -> None:
    """Apply the upload bounds of the import routes to a payload that did not arrive as a file."""
    from app.routers.export import MAX_JSON_IMPORT_BYTES, _validate_import_data
    if not isinstance(data, dict):
        raise ValueError("Import file must contain a JSON object")
    if len(_canonical(data)) > MAX_JSON_IMPORT_BYTES:
        raise ValueError("Import file is too large")
    try:
        _validate_import_data(data)
    except HTTPException as exc:
        raise ValueError(str(exc.detail)) from exc


def _iso(value):
    return value.isoformat() if hasattr(value, "isoformat") else value


async def capture_import_state(db, iteration_id) -> dict[str, Any]:
    """Read every planning row an import can create or change in one iteration."""
    from app.models.external_link import ExternalLink
    from app.models.iteration import Iteration
    from app.models.task import Task, TaskDependency
    from app.models.team_member import TeamMember, Vacation

    tasks_table = Task.__table__
    task_columns = [tasks_table.c[name] for name in ("id", *TASK_FIELDS, *DATE_FIELDS, *LINK_FIELDS)]
    in_iteration = select(Task.id).where(Task.iteration_id == iteration_id)
    members_in_iteration = select(TeamMember.id).where(TeamMember.iteration_id == iteration_id)
    with internal_authority(db):
        iteration = (await db.execute(select(*[Iteration.__table__.c[name] for name in ITERATION_FIELDS])
            .where(Iteration.id == iteration_id))).mappings().one_or_none()
        tasks = (await db.execute(select(*task_columns).where(tasks_table.c.iteration_id == iteration_id))).mappings().all()
        dependencies = (await db.execute(select(TaskDependency.task_id, TaskDependency.depends_on_id).where(
            TaskDependency.task_id.in_(in_iteration) | TaskDependency.depends_on_id.in_(in_iteration)))).all()
        links = (await db.execute(select(ExternalLink.entity_id, *[ExternalLink.__table__.c[name] for name in EXTERNAL_LINK_FIELDS])
            .where(ExternalLink.entity_type == "task", ExternalLink.entity_id.in_(in_iteration)))).mappings().all()
        members = (await db.execute(select(*[TeamMember.__table__.c[name] for name in ("id", *MEMBER_FIELDS)])
            .where(TeamMember.iteration_id == iteration_id))).mappings().all()
        vacations = (await db.execute(select(Vacation.team_member_id, Vacation.start_date, Vacation.end_date)
            .where(Vacation.team_member_id.in_(members_in_iteration)))).all()
    member_vacations: dict[int, list] = {}
    for member_id, start, end in vacations:
        member_vacations.setdefault(member_id, []).append([start.isoformat(), end.isoformat()])
    return {
        "iteration": {name: _iso(iteration[name]) for name in ITERATION_FIELDS} if iteration else None,
        "tasks": {row["id"]: {name: _iso(row[name]) for name in (*TASK_FIELDS, *DATE_FIELDS, *LINK_FIELDS)} for row in tasks},
        "dependencies": {(task_id, depends_on_id) for task_id, depends_on_id in dependencies},
        "external_links": [{"task_id": row["entity_id"], **{name: row[name] for name in EXTERNAL_LINK_FIELDS}} for row in links],
        "members": {row["id"]: {**{name: row[name] for name in MEMBER_FIELDS},
                                "vacations": sorted(member_vacations.get(row["id"], []))} for row in members},
    }


EMPTY_STATE = {"iteration": None, "tasks": {}, "dependencies": set(), "external_links": [], "members": {}}


def _sort_key(value) -> str:
    return _canonical(value).decode()


def diff_import_state(before, after, *, profile_floor: int, profiles: dict[int, dict]) -> dict[str, Any]:
    """Describe exactly what changed, naming rows the import creates by stable local references."""
    task_refs = {task_id: f"new-task-{index}" for index, task_id in enumerate(sorted(set(after["tasks"]) - set(before["tasks"])), 1)}
    member_refs = {member_id: f"new-member-{index}" for index, member_id in enumerate(sorted(set(after["members"]) - set(before["members"])), 1)}
    referenced_profiles = {row["profile_id"] for row in after["members"].values()} | {row["owner_profile_id"] for row in after["tasks"].values()}
    new_profiles = sorted(pid for pid in referenced_profiles if pid is not None and pid > profile_floor)
    profile_refs = {profile_id: f"new-profile-{index}" for index, profile_id in enumerate(new_profiles, 1)}

    def task_ref(value):
        return task_refs.get(value, value)

    def mapped(name, value):
        if name == "parent_id":
            return task_ref(value)
        if name == "assignee_id":
            return member_refs.get(value, value)
        if name in {"owner_profile_id", "profile_id"}:
            return profile_refs.get(value, value)
        return value

    def changed_fields(old, new, names):
        return {name: {"from": mapped(name, old.get(name)), "to": mapped(name, new.get(name))}
                for name in names if old.get(name) != new.get(name)}

    tasks = {"created": [], "changed": [], "removed": []}
    links = {"created": [], "changed": [], "removed": []}
    dates = []
    for task_id, ref in sorted(task_refs.items()):
        row = after["tasks"][task_id]
        tasks["created"].append({"ref": ref, **{name: mapped(name, row[name]) for name in TASK_FIELDS}})
        if any(row[name] is not None for name in LINK_FIELDS):
            links["created"].append({"kind": "source", "task": ref, **{name: row[name] for name in LINK_FIELDS}})
        dates.extend({"task": ref, "field": name, "from": None, "to": row[name]} for name in DATE_FIELDS if row[name] is not None)
    for task_id in sorted(set(before["tasks"]) & set(after["tasks"])):
        old, new = before["tasks"][task_id], after["tasks"][task_id]
        if fields := changed_fields(old, new, TASK_FIELDS):
            tasks["changed"].append({"id": task_id, "changes": fields})
        if fields := changed_fields(old, new, LINK_FIELDS):
            links["changed"].append({"kind": "source", "task": task_id, "changes": fields})
        dates.extend({"task": task_id, "field": name, "from": old[name], "to": new[name]} for name in DATE_FIELDS if old[name] != new[name])
    for task_id in sorted(set(before["tasks"]) - set(after["tasks"])):
        old = before["tasks"][task_id]
        tasks["removed"].append({"id": task_id, "title": old["title"]})
        if any(old[name] is not None for name in LINK_FIELDS):
            links["removed"].append({"kind": "source", "task": task_id, **{name: old[name] for name in LINK_FIELDS}})

    def external(rows):
        return {_sort_key(item): item for item in ({"kind": "external_link", "task": task_ref(row["task_id"]),
                **{name: row[name] for name in EXTERNAL_LINK_FIELDS}} for row in rows)}
    old_links, new_links = external(before["external_links"]), external(after["external_links"])
    links["created"].extend(new_links[key] for key in sorted(set(new_links) - set(old_links)))
    links["removed"].extend(old_links[key] for key in sorted(set(old_links) - set(new_links)))

    def dependency(pair):
        return {"task": task_ref(pair[0]), "depends_on": task_ref(pair[1])}
    dependencies = {
        "created": sorted((dependency(pair) for pair in after["dependencies"] - before["dependencies"]), key=_sort_key),
        "removed": sorted((dependency(pair) for pair in before["dependencies"] - after["dependencies"]), key=_sort_key),
    }

    members = {"created": [], "changed": [], "removed": []}
    for member_id, ref in sorted(member_refs.items()):
        row = after["members"][member_id]
        members["created"].append({"ref": ref, **{name: mapped(name, row[name]) for name in MEMBER_FIELDS}, "vacations": row["vacations"]})
    for member_id in sorted(set(before["members"]) & set(after["members"])):
        if fields := changed_fields(before["members"][member_id], after["members"][member_id], (*MEMBER_FIELDS, "vacations")):
            members["changed"].append({"id": member_id, "changes": fields})
    for member_id in sorted(set(before["members"]) - set(after["members"])):
        members["removed"].append({"id": member_id, "name": before["members"][member_id]["name"]})

    iteration = None
    if before["iteration"] is None and after["iteration"] is not None:
        iteration = {"created": {"ref": "new-iteration", **after["iteration"]}}
    elif before["iteration"] is not None and after["iteration"] is not None:
        if fields := changed_fields(before["iteration"], after["iteration"], ITERATION_FIELDS):
            iteration = {"changed": fields}

    return {
        "iteration": iteration,
        "tasks": tasks,
        "dependencies": dependencies,
        "links": links,
        "dates": sorted(dates, key=lambda item: (isinstance(item["task"], str), _sort_key(item["task"]), DATE_FIELDS.index(item["field"]))),
        "team_members": members,
        "profiles": {"created": [{"ref": profile_refs[pid], **profiles[pid]} for pid in new_profiles if pid in profiles]},
    }


def summarize_changes(changes: dict) -> dict[str, int]:
    summary = {}
    for section in ("tasks", "dependencies", "links", "team_members", "profiles"):
        for kind, rows in changes[section].items():
            summary[f"{section}_{kind}"] = len(rows)
    summary["dates_changed"] = len(changes["dates"])
    return summary


async def _profile_floor(db) -> int:
    from app.models.team_member import TeamMemberProfile
    with internal_authority(db):
        return await db.scalar(select(func.max(TeamMemberProfile.id))) or 0


async def _new_profiles(db, floor) -> dict[int, dict]:
    from app.models.team_member import TeamMemberProfile
    with internal_authority(db):
        rows = (await db.execute(select(TeamMemberProfile.id, TeamMemberProfile.display_name, TeamMemberProfile.email,
            TeamMemberProfile.profile_kind).where(TeamMemberProfile.id > floor))).all()
    return {row.id: {"display_name": row.display_name, "email": row.email, "profile_kind": row.profile_kind} for row in rows}


async def run_import_with_changes(db, iteration_id, data, *, expected_revisions):
    """Run the import writer and return its receipt with the exact change set it made."""
    from app.routers.export import write_iteration_import, write_new_iteration_import

    floor = await _profile_floor(db)
    if iteration_id is None:
        before = EMPTY_STATE
        result, target = await write_new_iteration_import(db, data, expected_revisions=expected_revisions)
    else:
        before = await capture_import_state(db, iteration_id)
        result = await write_iteration_import(db, iteration_id, data, expected_revisions=expected_revisions)
        target = iteration_id
    await db.flush()
    after = await capture_import_state(db, target)
    return result, diff_import_state(before, after, profile_floor=floor, profiles=await _new_profiles(db, floor))


def _referenced_project_ids(iteration, data) -> set:
    from app.routers.export import _optional_int
    projects = set()
    if iteration is not None:
        projects.add(iteration.project_id)
    else:
        iteration_data = data.get("iteration")
        if not isinstance(iteration_data, dict):
            raise ValueError("Missing iteration data in export file")
        projects.add(_optional_int(iteration_data.get("project_id"), "iteration.project_id"))
    stack = list(data.get("tasks", []))
    while stack:
        task = stack.pop()
        if task.get("project_id") is not None:
            projects.add(_optional_int(task.get("project_id"), "task.project_id"))
        stack.extend(task.get("children", []))
    return projects


async def _authorize_reviewer(db, iteration_id, data):
    """The reviewer must be able to plan work in every project the import writes to."""
    from app.services.iteration_service import IterationService
    iteration = None
    if iteration_id is not None:
        iteration = await IterationService(db).get_by_id(iteration_id)
        if iteration is None:
            raise LookupError("Iteration not found or inaccessible")
    for project_id in sorted(_referenced_project_ids(iteration, data), key=lambda value: (value is not None, value or 0)):
        require_project(db, project_id, "create")


@contextmanager
def _operator_simulation(db, authority: Authority):
    """Run the writer as the operator who will apply it; the surrounding preview never commits."""
    previous = db.info.get("authority")

    def refuse_commit(_session):
        raise RuntimeError("A plan-import dry run cannot commit")

    event.listen(db.sync_session, "before_commit", refuse_commit)
    db.info["authority"] = authority
    try:
        yield
    finally:
        db.info["authority"] = previous
        event.remove(db.sync_session, "before_commit", refuse_commit)


async def _operator_authority(db, caller: Authority | None) -> Authority:
    from app.models.identity import WorkspaceAuthorityState
    with internal_authority(db):
        state = await db.get(WorkspaceAuthorityState, 1)
    principal_id = state.operator_principal_id if state is not None else None
    operator = Authority(principal_id, "system", workspace_role="operator")
    if caller is not None:
        operator = replace(operator, source=caller.source, correlation_id=caller.correlation_id)
    return operator


async def dry_run_import(db, iteration_id, data) -> dict[str, Any]:
    """Return the exact changes an import of this file would make, and write nothing."""
    from app.services.import_planning_service import import_file_sha256, import_scope_revisions

    command = current_command(db)
    if command is None or command.mode != "preview":
        raise RuntimeError("A plan-import dry run must own a rollback-only command")
    await _authorize_reviewer(db, iteration_id, data)
    # Read under the reviewer's own authority: it must see every scheduling input the import reserves.
    revisions = await import_scope_revisions(db, iteration_id, data)
    if len(_canonical(revisions)) > 16384:
        raise PlanningConflict("planning_scope_oversized", "The complete import revision context exceeds the supported header limit.")
    caller = db.info.get("authority")
    try:
        with _operator_simulation(db, await _operator_authority(db, caller)):
            result, changes = await run_import_with_changes(db, iteration_id, data, expected_revisions=revisions)
            await db.flush()
    except HTTPException as exc:
        raise ValueError(str(exc.detail)) from exc
    except KeyError as exc:
        raise ValueError(f"Import entry is missing required field {exc}") from exc
    del result
    file_sha = import_file_sha256(data)
    target_sha = target_sha256(iteration_id, revisions)
    return {
        "target_iteration_id": iteration_id,
        "file_sha256": file_sha,
        "expected_revisions": {str(key): value for key, value in revisions.items()},
        "changes": changes,
        "summary": summarize_changes(changes),
        "review_digest": compose_review_digest(file_sha, target_sha, changes_sha256(changes)),
        "written": False,
    }


async def apply_reviewed_import(db, iteration_id, data, review_digest: str):
    """Apply an import only when it would make exactly the reviewed change set."""
    from app.services.import_planning_service import import_file_sha256, import_scope_revisions

    file_sha, target_sha, change_sha = parse_review_digest(review_digest)
    if import_file_sha256(data) != file_sha:
        raise ImportReviewRefused("import_review_file_changed",
            "The import file differs from the reviewed one. Run the dry run again and review the new changes.")
    revisions = await import_scope_revisions(db, iteration_id, data)
    if target_sha256(iteration_id, revisions) != target_sha:
        raise ImportReviewRefused("import_review_target_changed",
            "The import target changed since the review. Run the dry run again and review the new changes.")
    try:
        result, changes = await run_import_with_changes(db, iteration_id, data, expected_revisions=revisions)
    except (AggregateVersionConflict, PlanningConflict) as exc:
        # The reviewed revisions are re-checked under the import's own locks; a change in
        # between, or a scope that grew, means the target changed after the review.
        if isinstance(exc, PlanningConflict) and exc.code != "planning_scope_changed":
            raise
        raise ImportReviewRefused("import_review_target_changed",
            "The import target changed since the review. Run the dry run again and review the new changes.") from exc
    if changes_sha256(changes) != change_sha:
        # Raising here rolls back the whole command, including the writes just made.
        raise ImportReviewRefused("import_review_changes_differ",
            "The import would no longer make the reviewed changes. Run the dry run again and review the new changes.")
    return result
