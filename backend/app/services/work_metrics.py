"""Canonical leaf work, acceptance and distinct calendar-based schedule signals."""

from datetime import datetime
from zoneinfo import ZoneInfo

from app.utils.time import as_utc, utc_now


def working_today(timezone="UTC", now: datetime | None = None):
    return as_utc(now or utc_now()).astimezone(ZoneInfo(timezone or "UTC")).date()


def effective_work_flags(task, *, by_id=None):
    """Use complete ancestry for inherited work policy; unknown links fail closed."""
    deferred = optional = False
    current, seen = task, set()
    while current is not None:
        if current.id in seen:
            raise ValueError("Task ancestry contains a cycle")
        seen.add(current.id)
        deferred = deferred or bool(current.is_deferred)
        optional = optional or bool(current.is_optional)
        parent_id = getattr(current, "parent_id", None)
        if parent_id is None:
            break
        parent = by_id.get(parent_id) if by_id is not None else current.__dict__.get("parent")
        if parent is None or parent.id != parent_id:
            raise ValueError("Task ancestry is incomplete")
        current = parent
    return {"effective_is_deferred": deferred, "effective_is_optional": optional}


def task_signals(task, *, iteration_end=None, project_target=None, timezone="UTC", now=None, composite=False, effective_flags=None):
    today = working_today(timezone, now)
    flags = effective_flags if effective_flags is not None else effective_work_flags(task)
    deferred, optional = flags["effective_is_deferred"], flags["effective_is_optional"]
    excluded = composite or deferred or bool(getattr(task, "canceled_at", None))
    implemented = task.status in {"resolved", "closed"}
    accepted = (task.status == "closed" and getattr(task, "accepted_at", None) is not None
                and getattr(task, "accepted_by_principal_id", None) is not None
                and getattr(task, "accepted_version", None) == task.version)
    baseline_start = getattr(task, "baseline_start_date", None)
    actual_start = getattr(task, "actual_start_date", None)
    start = baseline_start or task.start_date
    late_start = bool(start and (actual_start > start if actual_start else task.status == "planned" and start < today))
    return {"metric_contract_version": 2,
            "effective_is_deferred": deferred, "effective_is_optional": optional,
            "is_late_start": not excluded and late_start,
            "is_overdue": not excluded and not implemented and bool(task.end_date and task.end_date < today),
            "is_iteration_overflow": not excluded and bool(task.end_date and iteration_end and task.end_date > iteration_end),
            "is_project_target_overflow": not excluded and bool(task.end_date and project_target and task.end_date > project_target),
            "is_implemented": not excluded and implemented, "is_accepted": not excluded and accepted,
            "acceptance_unknown": not excluded and task.status == "closed" and not accepted}


def leaf_metrics(tasks, *, iteration_end=None, project_target=None, timezone="UTC", now=None):
    """Use a complete scoped task set; parents never contribute additional delivered work."""
    by_id = {}
    pending = list(tasks)
    while pending:
        task = pending.pop()
        if task.id in by_id:
            continue
        by_id[task.id] = task
        pending.extend(task.__dict__.get("children", []) or [])
    parents = {task.parent_id for task in by_id.values() if task.parent_id is not None}
    parents.update(task.id for task in by_id.values() if getattr(task, "is_summary", False))
    result = {key: 0 for key in ["total_tasks", "required_tasks", "optional_tasks", "deferred_tasks", "structural_tasks",
              "implemented_tasks", "accepted_tasks", "required_implemented_tasks", "required_accepted_tasks",
              "overdue_tasks", "late_start_tasks", "iteration_overflow_tasks", "project_target_overflow_tasks", "acceptance_unknown_tasks", "unknown_estimate_tasks"]}
    result.update(total_effort_days=0.0, remaining_effort_days=0.0, required_effort_days=0.0,
                  metric_contract_version=2, tasks_by_status={state: 0 for state in ["planned", "active", "resolved", "closed"]})
    for task in by_id.values():
        if task.id in parents:
            result["structural_tasks"] += 1
            continue
        flags = effective_work_flags(task, by_id=by_id)
        deferred, optional = flags["effective_is_deferred"], flags["effective_is_optional"]
        if getattr(task, "canceled_at", None):
            continue
        if deferred:
            result["deferred_tasks"] += 1
            continue
        signals = task_signals(task, iteration_end=iteration_end, project_target=project_target, timezone=timezone, now=now, effective_flags=flags)
        result["total_tasks"] += 1
        result["optional_tasks" if optional else "required_tasks"] += 1
        result["tasks_by_status"][task.status] = result["tasks_by_status"].get(task.status, 0) + 1
        for source, target in [("is_implemented", "implemented_tasks"), ("is_accepted", "accepted_tasks"),
                               ("is_overdue", "overdue_tasks"), ("is_late_start", "late_start_tasks"),
                               ("is_iteration_overflow", "iteration_overflow_tasks"), ("is_project_target_overflow", "project_target_overflow_tasks"),
                               ("acceptance_unknown", "acceptance_unknown_tasks")]:
            result[target] += int(signals[source])
        if not optional:
            result["required_implemented_tasks"] += int(signals["is_implemented"])
            result["required_accepted_tasks"] += int(signals["is_accepted"])
        effort = task.effort_days
        if effort is None:
            result["unknown_estimate_tasks"] += 1
        else:
            result["total_effort_days"] += effort
            if not optional:
                result["required_effort_days"] += effort
            if not signals["is_implemented"]:
                result["remaining_effort_days"] += effort
    result["completed_tasks"] = result["implemented_tasks"]
    result["completion_percent"] = round(result["implemented_tasks"] * 100 / result["total_tasks"], 1) if result["total_tasks"] else 0.0
    result["accepted_percent"] = round(result["required_accepted_tasks"] * 100 / result["required_tasks"], 1) if result["required_tasks"] else 0.0
    return result


async def scoped_metric_tasks(db, *, project_id=None, iteration_id=None):
    from sqlalchemy import select
    from app.models.task import Task
    from app.query_limits import CollectionLimitExceededError, MAX_PROJECT_TREE_TASKS
    statement = select(Task)
    if project_id is not None:
        statement = statement.where(Task.project_id == project_id)
    if iteration_id is not None:
        statement = statement.where(Task.iteration_id == iteration_id)
    rows = list((await db.scalars(statement.order_by(Task.id).limit(MAX_PROJECT_TREE_TASKS + 1))).all())
    if len(rows) > MAX_PROJECT_TREE_TASKS:
        raise CollectionLimitExceededError("canonical work metrics", MAX_PROJECT_TREE_TASKS)
    return rows


async def aggregate_metrics(db, *, project_id=None, iteration_id=None, project_ids=None, group_by=None, task_ids=None, zone_map=None):
    """Aggregate all authorized leaves in SQL, including inherited scheduling facets."""
    from sqlalchemy import select, case, func, or_, and_, false, literal
    from app.models.task import Task, TaskDependency
    from app.models.project import Project
    from app.models.iteration import Iteration
    from app.authority import _scope_conditions

    t, iterations, projects = Task.__table__, Iteration.__table__, Project.__table__
    authority = db.info.get("authority")
    scope = _scope_conditions(authority).get(Task) if authority is not None and not authority.operator and not authority.local else None
    roots = select(t.c.id, t.c.parent_id, t.c.project_id, t.c.iteration_id,
                   t.c.is_deferred.label("deferred"), t.c.is_optional.label("optional")).where(t.c.parent_id.is_(None))
    if scope is not None:
        roots = roots.where(scope)
    if project_id is not None:
        roots = roots.where(t.c.project_id == project_id)
    if project_ids is not None:
        roots = roots.where(t.c.project_id.in_(project_ids))
    if iteration_id is not None:
        roots = roots.where(t.c.iteration_id == iteration_id)
    tree = roots.cte("scoped_work_tree", recursive=True)
    child = t.alias("metric_child")
    tree = tree.union_all(select(child.c.id, child.c.parent_id, child.c.project_id, child.c.iteration_id,
        or_(tree.c.deferred, child.c.is_deferred), or_(tree.c.optional, child.c.is_optional)).join(tree, child.c.parent_id == tree.c.id)
        .where(child.c.iteration_id.is_not_distinct_from(tree.c.iteration_id),
               or_(child.c.project_id == tree.c.project_id, and_(child.c.project_id.is_(None), tree.c.project_id.is_(None)))))
    visible = select(func.count()).select_from(t)
    if scope is not None:
        visible = visible.where(scope)
    if project_id is not None:
        visible = visible.where(t.c.project_id == project_id)
    if project_ids is not None:
        visible = visible.where(t.c.project_id.in_(project_ids))
    if iteration_id is not None:
        visible = visible.where(t.c.iteration_id == iteration_id)
    visible_count = visible.correlate(None).scalar_subquery()
    reached_count = select(func.count()).select_from(tree).scalar_subquery()
    from app.models.calendar import Calendar
    if zone_map is None:
        zones = (await db.execute(select(literal("project"), Project.id, Project.timezone).union_all(
            select(literal("calendar"), Calendar.id, Calendar.timezone)))).all()
        dates = {identifier: working_today(zone) for kind, identifier, zone in zones if kind == "project"}
        calendar_dates = {identifier: working_today(zone) for kind, identifier, zone in zones if kind == "calendar"}
    else:
        dates, calendar_dates = {pid: working_today(zone) for pid, zone in zone_map.items()}, {}
    fallback = case(calendar_dates, value=iterations.c.calendar_id, else_=working_today()) if calendar_dates else working_today()
    today = case(dates, value=t.c.project_id, else_=fallback) if dates else fallback
    descendants = t.alias("metric_descendant")
    composite = or_(t.c.is_summary, select(descendants.c.id).where(descendants.c.parent_id == t.c.id).exists())
    leaf = ~composite
    included = and_(leaf, ~tree.c.deferred, t.c.canceled_at.is_(None))
    required = and_(included, ~tree.c.optional)
    implemented = t.c.status.in_(["resolved", "closed"])
    accepted = and_(t.c.status == "closed", t.c.accepted_at.is_not(None), t.c.accepted_by_principal_id.is_not(None), t.c.accepted_version == t.c.version)
    accepted = func.coalesce(accepted, false())
    overdue = and_(~implemented, t.c.end_date < today)
    start = func.coalesce(t.c.baseline_start_date, t.c.start_date)
    late = or_(and_(t.c.actual_start_date.is_not(None), t.c.actual_start_date > start),
               and_(t.c.actual_start_date.is_(None), t.c.status == "planned", start < today))
    dependency, target = TaskDependency.__table__, t.alias("metric_dependency")
    visible_ids = select(t.c.id).where(scope) if scope is not None else select(t.c.id)
    visible_ids = visible_ids.correlate(None)
    unavailable_dependency = select(dependency.c.id).outerjoin(target, target.c.id == dependency.c.depends_on_id).where(dependency.c.task_id == t.c.id,
        or_(target.c.id.is_(None), dependency.c.depends_on_id.notin_(visible_ids),
            target.c.status.notin_(["resolved", "closed"]), target.c.canceled_at.is_not(None))).exists()
    blocked = or_(and_(t.c.blocked_reason.is_not(None), t.c.blocked_reason != ""), unavailable_dependency)
    def count(predicate, name):
        return func.coalesce(func.sum(case((predicate, 1), else_=0)), 0).label(name)
    columns = [count(included, "total_tasks"), count(required, "required_tasks"), count(and_(included, tree.c.optional), "optional_tasks"),
        count(and_(leaf, tree.c.deferred), "deferred_tasks"), count(composite, "structural_tasks"),
        count(and_(included, implemented), "implemented_tasks"), count(and_(included, accepted), "accepted_tasks"),
        count(and_(required, implemented), "required_implemented_tasks"), count(and_(required, accepted), "required_accepted_tasks"),
        count(and_(included, overdue), "overdue_tasks"), count(and_(included, late), "late_start_tasks"),
        count(and_(included, t.c.end_date > iterations.c.end_date), "iteration_overflow_tasks"),
        count(and_(included, t.c.end_date > projects.c.target_date), "project_target_overflow_tasks"),
        count(and_(included, t.c.status == "closed", ~accepted), "acceptance_unknown_tasks"),
        count(and_(included, (t.c.effort_hours / t.c.nominal_day_hours).is_(None)), "unknown_estimate_tasks"), count(and_(included, blocked), "blocked_tasks"),
        func.coalesce(func.sum(case((included, (t.c.effort_hours / t.c.nominal_day_hours)), else_=0.0)), 0.0).label("total_effort_days"),
        func.coalesce(func.sum(case((and_(included, ~implemented), (t.c.effort_hours / t.c.nominal_day_hours)), else_=0.0)), 0.0).label("remaining_effort_days"),
        func.min(case((included, t.c.start_date))).label("task_start_date"), func.max(case((included, t.c.end_date))).label("task_end_date"),
        *[count(and_(included, t.c.status == state), "status_" + state) for state in ["planned", "active", "resolved", "closed"]]]
    grouping = {"project": t.c.project_id, "milestone": t.c.milestone_id}.get(group_by)
    if grouping is not None:
        columns.insert(0, grouping.label("group_id"))
    validation = [visible_count.label("_visible"), reached_count.label("_reachable")]
    query = select(*columns, *validation, literal(False).label("_validation_only")).select_from(t.join(tree, tree.c.id == t.c.id).outerjoin(iterations, iterations.c.id == t.c.iteration_id).outerjoin(projects, projects.c.id == t.c.project_id))
    if task_ids is not None:
        query = query.where(t.c.id.in_(task_ids))
    if grouping is not None:
        query = query.group_by(grouping)
    if grouping is not None:
        empty = [literal(None if column.name in {"group_id", "task_start_date", "task_end_date"} else 0).label(column.name) for column in columns]
        query = query.union_all(select(*empty, *validation, literal(True).label("_validation_only")))
    rows = (await db.execute(query)).mappings().all()
    results = []
    for row in rows:
        values = dict(row)
        if values.pop("_visible") != values.pop("_reachable"):
            from app.commands import HierarchyScopeError
            raise HierarchyScopeError()
        if values.pop("_validation_only"):
            continue
        values["status_counts"] = {state: int(values.pop("status_" + state)) for state in ["planned", "active", "resolved", "closed"]}
        values["completed_tasks"] = values["implemented_tasks"]
        values["completion_percent"] = round(values["implemented_tasks"] * 100 / values["total_tasks"], 1) if values["total_tasks"] else 0.0
        values["accepted_percent"] = round(values["required_accepted_tasks"] * 100 / values["required_tasks"], 1) if values["required_tasks"] else 0.0
        values["metric_contract_version"] = 2
        results.append(values)
    return results if grouping is not None else results[0]
