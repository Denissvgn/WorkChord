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
    "is_deferred", "tags", "sort_order", "brief", "execution_mode", "nominal_day_hours",
    "estimate_provenance", "ownership_provenance", "brief_revision",
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


# The dry run holds the workspace-wide planning reservation (on SQLite, the writer lock)
# while the import runs, so a planner can only preview a bounded file. The shape caps
# are checked before the reservation; they keep ordinary plans well inside the time
# budget and the response reviewable. Whatever still runs long is cut off by the budget.
# A larger plan is reviewed in parts, or applied by the operator without a review.
# The caps keep typical files well inside the budget (100 tasks as 20 chains five levels
# deep measured about 2.7 s on SQLite and 4.1 s on PostgreSQL per request). They do not
# guarantee it: every cap at once, or a large target iteration, can still overrun, and the
# budget below is the hard bound.
MAX_DRY_RUN_IMPORT_TASKS = 100
MAX_DRY_RUN_IMPORT_MEMBERS = 50
MAX_DRY_RUN_IMPORT_DEPTH = 5
MAX_DRY_RUN_IMPORT_DEPENDENCIES = 200
MAX_DRY_RUN_IMPORT_VACATIONS = 100
# Wall-clock budget for the import inside the dry run, enforced as an asyncio deadline
# and, on PostgreSQL, as a per-statement timeout for the rest of the rolled-back transaction.
DRY_RUN_BUDGET_SECONDS = 5.0
# One dry run at a time per server process, so planners cannot stack reservations.
_dry_run_active = False


class ImportFileInvalid(ValueError):
    """An import file field has the wrong type."""

    def detail(self):
        return {"code": "import_file_invalid", "message": str(self)}


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


def diff_import_state(before, after, *, created_profiles: dict[int, dict]) -> dict[str, Any]:
    """Describe exactly what changed, naming rows the import creates by stable local references.

    ``created_profiles`` holds the profiles this command inserted, so a profile another
    session committed meanwhile is never reported as created by the import.
    """
    task_refs = {task_id: f"new-task-{index}" for index, task_id in enumerate(sorted(set(after["tasks"]) - set(before["tasks"])), 1)}
    member_refs = {member_id: f"new-member-{index}" for index, member_id in enumerate(sorted(set(after["members"]) - set(before["members"])), 1)}
    profiles = created_profiles
    new_profiles = sorted(profiles)
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
        "profiles": {"created": [{"ref": profile_refs[pid], **profiles[pid]} for pid in new_profiles]},
    }


def summarize_changes(changes: dict) -> dict[str, int]:
    summary = {}
    for section in ("tasks", "dependencies", "links", "team_members", "profiles"):
        for kind, rows in changes[section].items():
            summary[f"{section}_{kind}"] = len(rows)
    summary["dates_changed"] = len(changes["dates"])
    return summary


@contextmanager
def _track_created_profiles(db):
    """Collect the profiles this session inserts while the writer runs."""
    from app.models.team_member import TeamMemberProfile
    created: list[TeamMemberProfile] = []

    def persisted(_session, instance):
        if isinstance(instance, TeamMemberProfile):
            created.append(instance)

    event.listen(db.sync_session, "pending_to_persistent", persisted)
    try:
        yield created
    finally:
        event.remove(db.sync_session, "pending_to_persistent", persisted)


async def run_import_with_changes(db, iteration_id, data, *, expected_revisions):
    """Run the import writer and return its receipt with the exact change set it made."""
    from app.routers.export import write_iteration_import, write_new_iteration_import

    with _track_created_profiles(db) as created:
        if iteration_id is None:
            before = EMPTY_STATE
            result, target = await write_new_iteration_import(db, data, expected_revisions=expected_revisions)
        else:
            before = await capture_import_state(db, iteration_id)
            result = await write_iteration_import(db, iteration_id, data, expected_revisions=expected_revisions)
            target = iteration_id
        await db.flush()
    after = await capture_import_state(db, target)
    profiles = {profile.id: {"display_name": profile.display_name, "email": profile.email, "profile_kind": profile.profile_kind}
                for profile in created}
    return result, diff_import_state(before, after, created_profiles=profiles)


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


def _file_tasks_with_depth(data):
    stack = [(task, 1) for task in data.get("tasks", [])]
    while stack:
        task, depth = stack.pop()
        yield task, depth
        stack.extend((child, depth + 1) for child in task.get("children", []))


def _file_tasks(data):
    for task, _depth in _file_tasks_with_depth(data):
        yield task


def _list_field(row, name, where):
    value = row.get(name, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ImportFileInvalid(f"{where}.{name} must be a list")
    return value


async def _bound_dry_run(db, iteration_id, data):
    """Refuse a file too large to preview before any planning reservation is taken."""
    from app.models.task import Task
    from app.query_limits import MAX_ITERATION_TREE_TASKS
    tasks = depth = references = 0
    for task, task_depth in _file_tasks_with_depth(data):
        tasks += 1
        depth = max(depth, task_depth)
        references += len(_list_field(task, "dependencies", "task")) + len(_list_field(task, "dependency_external_keys", "task"))
    members = data.get("team_members", [])
    vacations = sum(len(_list_field(member, "vacations", "team_member")) for member in members)
    limits = (
        (tasks, MAX_DRY_RUN_IMPORT_TASKS, "tasks"),
        (len(members), MAX_DRY_RUN_IMPORT_MEMBERS, "team members"),
        (depth, MAX_DRY_RUN_IMPORT_DEPTH, "levels of subtasks"),
        (references, MAX_DRY_RUN_IMPORT_DEPENDENCIES, "dependency references"),
        (vacations, MAX_DRY_RUN_IMPORT_VACATIONS, "vacations"),
    )
    for count, limit, label in limits:
        if count > limit:
            raise PlanningConflict("import_dry_run_too_large",
                f"A dry run previews at most {limit} {label}; this file has {count}. Review the plan in smaller files.")
    existing = 0
    if iteration_id is not None:
        with internal_authority(db):
            existing = await db.scalar(select(func.count(Task.id)).where(Task.iteration_id == iteration_id)) or 0
    if existing + tasks > MAX_ITERATION_TREE_TASKS:
        raise PlanningConflict("import_iteration_tree_too_large",
            f"The iteration would hold more than {MAX_ITERATION_TREE_TASKS} tasks after this import.")


def _profile_reference(value, where) -> int:
    if isinstance(value, bool):
        raise ImportFileInvalid(f"{where} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value)
    raise ImportFileInvalid(f"{where} must be an integer")


def _explicit_profile_ids(data) -> set[int]:
    ids = set()
    for member in data.get("team_members", []):
        if member.get("profile_id") is not None:
            ids.add(_profile_reference(member["profile_id"], "team_member.profile_id"))
    for task in _file_tasks(data):
        if task.get("owner_profile_id") is not None:
            ids.add(_profile_reference(task["owner_profile_id"], "task.owner_profile_id"))
    return ids


def _resolved_profile_ids(changes) -> set[int]:
    """Existing profiles the change set points at (created profiles carry string references)."""
    ids = set()
    for row in changes["team_members"]["created"]:
        ids.add(row["profile_id"])
    for row in changes["tasks"]["created"]:
        ids.add(row["owner_profile_id"])
    for section, field in (("team_members", "profile_id"), ("tasks", "owner_profile_id")):
        for row in changes[section]["changed"]:
            if field in row["changes"]:
                ids.add(row["changes"][field]["to"])
    return {value for value in ids if isinstance(value, int)}


async def _team_profiles(db) -> set[int]:
    """Profiles of team members in iterations the caller can read, taken before the import runs."""
    from app.models.team_member import TeamMember
    return set((await db.scalars(select(TeamMember.profile_id).where(TeamMember.profile_id.is_not(None)).distinct())).all())


async def _require_readable_profiles(db, profile_ids, team_profiles: set[int]):
    """Under the caller's own authority: every profile the import refers to must be readable.

    A profile is readable when the caller's scope shows it directly (a workspace member
    reads every profile, anyone else only their own) or when it belongs to a team member
    of an iteration the caller can read, as the iteration team view shows it. Missing and
    unreadable profiles are refused alike, so no profile id leaks.
    """
    from app.authority import AuthorityError
    from app.models.team_member import TeamMemberProfile
    wanted = set(profile_ids) - team_profiles
    if not wanted:
        return
    readable = set((await db.scalars(select(TeamMemberProfile.id).where(TeamMemberProfile.id.in_(sorted(wanted))))).all())
    if readable != wanted:
        raise AuthorityError("incomplete_authorized_graph", "This import refers to a team member profile you cannot read.")


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


def _too_slow() -> PlanningConflict:
    return PlanningConflict("import_dry_run_too_slow",
        f"The dry run exceeded its {DRY_RUN_BUDGET_SECONDS:g}-second budget and was rolled back. "
        "Review the plan in smaller files, or try again if the planning reservation was busy with another command.")


async def _run_within_budget(db, operator, iteration_id, data, revisions):
    """Run the writer as the operator under a wall-clock budget; any overrun is refused and rolled back."""
    import asyncio
    from sqlalchemy import text
    from sqlalchemy.exc import DBAPIError

    try:
        async with asyncio.timeout(DRY_RUN_BUDGET_SECONDS):
            with _operator_simulation(db, operator):
                if db.bind.dialect.name == "postgresql":
                    # SET LOCAL ends with this transaction, which the preview always rolls back.
                    await db.execute(text(f"SET LOCAL statement_timeout = {max(1, int(DRY_RUN_BUDGET_SECONDS * 1000))}"))
                _, changes = await run_import_with_changes(db, iteration_id, data, expected_revisions=revisions)
                await db.flush()
                return changes
    except TimeoutError as exc:
        raise _too_slow() from exc
    except DBAPIError as exc:
        if getattr(exc.orig, "sqlstate", None) == "57014":
            raise _too_slow() from exc
        raise
    except HTTPException as exc:
        raise ValueError(str(exc.detail)) from exc
    except KeyError as exc:
        raise ValueError(f"Import entry is missing required field {exc}") from exc


async def dry_run_import(db, iteration_id, data) -> dict[str, Any]:
    """Return the exact changes an import of this file would make, and write nothing."""
    from app.services.import_planning_service import import_file_sha256, import_scope_revisions

    global _dry_run_active
    command = current_command(db)
    if command is None or command.mode != "preview":
        raise RuntimeError("A plan-import dry run must own a rollback-only command")
    if _dry_run_active:
        raise PlanningConflict("import_dry_run_busy", "Another plan-import dry run is running. Try again shortly.")
    _dry_run_active = True
    try:
        # Everything up to the writer reads without taking the planning reservation.
        await _authorize_reviewer(db, iteration_id, data)
        await _bound_dry_run(db, iteration_id, data)
        team_profiles = await _team_profiles(db)
        await _require_readable_profiles(db, _explicit_profile_ids(data), team_profiles)
        # Read under the reviewer's own authority: it must see every scheduling input the import reserves.
        revisions = await import_scope_revisions(db, iteration_id, data)
        if len(_canonical(revisions)) > 16384:
            raise PlanningConflict("planning_scope_oversized", "The complete import revision context exceeds the supported header limit.")
        operator = await _operator_authority(db, db.info.get("authority"))
        changes = await _run_within_budget(db, operator, iteration_id, data, revisions)
        # Back under the caller's authority: a profile matched by name or email must be one it can read.
        await _require_readable_profiles(db, _resolved_profile_ids(changes), team_profiles)
    finally:
        _dry_run_active = False
    # Work the root command does on exit (delivery reconciliation, discussion enqueueing)
    # runs after this diff and is rolled back with everything else.
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
