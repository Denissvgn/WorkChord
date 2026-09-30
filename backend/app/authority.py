"""Principal-bound authorization shared by transport adapters and ORM commands."""

from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import uuid4

from sqlalchemy import and_, event, false, func, inspect, or_, select, true
from sqlalchemy.orm import Session, with_loader_criteria
from sqlalchemy.sql.elements import TextClause

from app.config import get_settings


class AuthorityError(RuntimeError):
    def __init__(self, code="permission_denied", message="You do not have permission for this action.", status=403):
        self.code, self.status = code, status
        super().__init__(message)

    def detail(self):
        return {"code": self.code, "message": str(self)}


@dataclass(frozen=True)
class Authority:
    principal_id: int | None
    kind: str
    workspace_role: str | None = None
    projects: dict[int, str] = field(default_factory=dict)
    actor_id: int | None = None
    actor_role: str | None = None
    session_id: int | None = None
    profile_id: int | None = None
    source: str = "rest"
    correlation_id: str = field(default_factory=lambda: uuid4().hex)
    reason: str | None = None
    review_override: bool = False
    local: bool = False
    scopes: frozenset[str] = frozenset()

    @property
    def operator(self):
        return (self.workspace_role in {"owner", "operator"} or self.kind == "system"
                or self.local and self.kind == "agent" and "admin" in self.scopes)

    def allows(self, project_id, action="read"):
        if self.kind == "agent":
            if action == "review" and self.actor_role != "verifier":
                return False
            required = {"read": {"tasks:read", "planning:read", "team:read", "work:execute", "verification:read"},
                        "create": {"tasks:write", "planning:write"}, "edit": {"tasks:write", "planning:write", "team:write"},
                        "execute": {"work:execute"}, "review": {"verification:write"}, "manage": {"planning:write"}}
            if "admin" not in self.scopes and not self.scopes.intersection(required.get(action, set())):
                return False
        if self.operator or self.local:
            return True
        role = self.projects.get(project_id)
        if project_id is None:
            return self.workspace_role == "member" and action in {"read", "create", "edit", "execute"}
        allowed = {
            "read": {"viewer", "editor", "executor", "reviewer", "manager"},
            "create": {"editor", "manager"}, "edit": {"editor", "manager"},
            "execute": {"editor", "executor", "manager"},
            "review": {"reviewer", "manager"}, "manage": {"manager"},
        }
        return role in allowed.get(action, set())


def require_project(db, project_id, action="read"):
    authority = db.info.get("authority")
    if authority is None:
        if get_settings().workchord_auth_mode == "trusted_local":
            return
        raise AuthorityError("authentication_required", "Sign in to continue.", 401)
    if not authority.allows(project_id, action):
        raise AuthorityError()


def require_operator(db):
    authority = db.info.get("authority")
    if authority is None or not authority.operator:
        raise AuthorityError("operator_required", "Workspace operator permission is required.")


@contextmanager
def internal_authority(db):
    """Allow identity resolution or verified automation inside a trusted server boundary."""
    previous = db.info.get("authority_internal", False)
    db.info["authority_internal"] = True
    try:
        yield
    finally:
        db.info["authority_internal"] = previous


def _scope_conditions(authority):
    from app.database import Base
    tables = Base.metadata.tables
    projects = tuple(pid for pid in authority.projects if authority.allows(pid, "read"))
    workspace_read = authority.workspace_role is not None
    iterations = tables["iterations"]
    task = tables["tasks"]
    project_condition = iterations.c.project_id.in_(projects)
    if workspace_read:
        project_condition = or_(project_condition, iterations.c.project_id.is_(None))
    iteration_ids = select(iterations.c.id).where(project_condition)
    task_condition = and_(or_(task.c.iteration_id.in_(iteration_ids), and_(task.c.iteration_id.is_(None), task.c.project_id.in_(projects))),
                          or_(task.c.project_id.in_(projects), task.c.project_id.is_(None)))
    task_ids = select(task.c.id).where(task_condition)
    conditions = {}
    for mapper in Base.registry.mappers:
        table = mapper.local_table
        c = table.c
        name = table.name
        condition = None
        if name == "task_deletion_fences":
            condition = false()
        elif name == "projects":
            condition = c.id.in_(projects)
        elif name == "iterations":
            condition = project_condition
        elif name == "tasks":
            condition = task_condition
        elif name == "task_dependencies":
            condition = and_(c.task_id.in_(task_ids), c.depends_on_id.in_(task_ids))
        elif name == "saved_views":
            condition = or_(c.owner_principal_id == authority.principal_id if authority.principal_id is not None else false(),
                            c.created_by_session_id == authority.session_id if authority.session_id is not None else false(),
                            c.scope.in_(["shared", "system"]) if workspace_read else false())
        elif name == "plan_shares":
            condition = or_(c.owner_principal_id == authority.principal_id if authority.principal_id is not None else false(),
                            c.created_by_session_id == authority.session_id if authority.session_id is not None else false())
        elif "project_id" in c:
            condition = c.project_id.in_(projects)
            if "iteration_id" in c:
                condition = or_(condition, and_(c.project_id.is_(None), c.iteration_id.in_(iteration_ids)))
            elif workspace_read:
                condition = or_(condition, c.project_id.is_(None))
        elif "iteration_id" in c:
            condition = c.iteration_id.in_(iteration_ids)
            if workspace_read and c.iteration_id.nullable:
                condition = or_(condition, c.iteration_id.is_(None))
        elif "original_task_id" in c:
            condition = c.original_task_id.in_(task_ids)
        elif "task_id" in c:
            condition = c.task_id.in_(task_ids)
        elif name == "triage_items":
            condition = or_(c.project_hint_id.in_(projects), c.iteration_hint_id.in_(iteration_ids))
            if workspace_read:
                condition = or_(condition, and_(c.project_hint_id.is_(None), c.iteration_hint_id.is_(None)))
        elif name == "user_sessions":
            condition = c.principal_id == authority.principal_id if authority.principal_id is not None else c.id == authority.session_id
        elif name == "calendars":
            condition = true() if workspace_read else c.id.in_(select(iterations.c.calendar_id).where(project_condition))
        elif name == "team_member_profiles":
            condition = true() if workspace_read else c.id == authority.profile_id
        elif name == "team_member_profile_skills":
            condition = true() if workspace_read else c.profile_id == authority.profile_id
        elif "team_member_id" in c:
            members = tables["team_members"]
            condition = c.team_member_id.in_(select(members.c.id).where(members.c.iteration_id.in_(iteration_ids)))
        elif name in {"initiatives", "work_templates", "labels", "label_groups", "request_sources", "agent_model_catalog"}:
            condition = true() if workspace_read else false()
        elif "principal_id" in c and name not in {"principals", "identity_subjects"}:
            condition = c.principal_id == authority.principal_id
        elif "actor_id" in c and not workspace_read:
            condition = c.actor_id == authority.actor_id
        if condition is not None:
            conditions[mapper.class_] = condition
    return conditions


@event.listens_for(Session, "do_orm_execute")
def scope_orm_operation(state):
    authority = state.session.info.get("authority")
    if authority is None or state.session.info.get("authority_internal"):
        return
    if isinstance(state.statement, TextClause) and not authority.operator and not authority.local:
        raise AuthorityError("unscoped_query_denied", "This operation requires an explicit resource scope.")
    if authority.operator or authority.local:
        if authority.kind == "agent" and (state.is_update or state.is_delete):
            _check_bulk_write(state, authority)
        return
    conditions = _scope_conditions(authority)
    if state.is_select:
        state.statement = state.statement.options(*[with_loader_criteria(model, predicate, include_aliases=True)
                                                    for model, predicate in conditions.items()])
    elif state.is_update or state.is_delete:
        _check_bulk_write(state, authority)
        mapper = state.bind_arguments.get("mapper")
        if mapper is not None and mapper.class_ in conditions:
            state.statement = state.statement.where(conditions[mapper.class_])
        elif not authority.operator:
            raise AuthorityError("unscoped_write_denied", "This write requires an explicit resource scope.")


def _check_bulk_write(state, authority):
    table = getattr(state.statement, "table", None)
    name = getattr(table, "name", "")
    action = "edit"
    if name == "tasks":
        values = getattr(state.statement, "_values", {}) or {}
        keys = {getattr(key, "name", str(key)) for key in values}
        if keys and keys <= {"version", "updated_at", "context_revision"}:
            if authority.kind == "agent":
                action = "review" if authority.actor_role == "verifier" else "execute"
        for column, value in values.items():
            if getattr(column, "name", str(column)) == "status" and getattr(value, "value", None) == "closed":
                action = "review"
                if authority.kind == "agent" and authority.actor_role != "verifier":
                    raise AuthorityError("independent_review_required", "Execution cannot accept its own work.")
            elif getattr(column, "name", str(column)) == "status" and getattr(value, "value", None) in {"active", "resolved"}:
                action = "execute"
    if not authority.operator and not authority.local and table is not None:
        from app.database import Base
        if "project_id" in table.c:
            project_column = table.c.project_id
            source = table
        elif name == "triage_items":
            target = Base.metadata.tables["iterations"]
            project_column = func.coalesce(table.c.project_hint_id, target.c.project_id)
            source = table.outerjoin(target, table.c.iteration_hint_id == target.c.id)
        elif "iteration_id" in table.c:
            target = Base.metadata.tables["iterations"]
            project_column = target.c.project_id
            source = table.join(target, table.c.iteration_id == target.c.id)
        elif "task_id" in table.c:
            target = Base.metadata.tables["tasks"]
            project_column = target.c.project_id
            source = table.join(target, table.c.task_id == target.c.id)
        else:
            raise AuthorityError("unscoped_write_denied", "This write requires explicit owner or operator authority.")
        projects = state.session.connection().execute(select(project_column).select_from(source).where(*state.statement._where_criteria).distinct()).scalars().all()
        keys = {getattr(key, "name", str(key)) for key in (getattr(state.statement, "_values", {}) or {})}
        reserved_only = name == "tasks" and keys and keys <= {"version", "updated_at", "context_revision"}
        derived_write = name in {"application_snapshots", "outbound_webhook_events", "outbound_webhook_deliveries", "task_events", "task_status_logs"}
        if name == "iterations" and keys == {"revision"} or reserved_only or derived_write:
            if any(not any(authority.allows(project_id, purpose) for purpose in ["edit", "execute", "review"]) for project_id in projects):
                raise AuthorityError()
            return
        if any(not authority.allows(project_id, action) for project_id in projects):
            raise AuthorityError()


def _object_project(session, obj):
    from app.database import Base
    table = inspect(type(obj)).local_table
    if table.name == "projects":
        return obj.id
    if table.name == "triage_items":
        if obj.project_hint_id is not None:
            return obj.project_hint_id
        if obj.iteration_hint_id is not None:
            iterations = Base.metadata.tables["iterations"]
            return session.connection().execute(select(iterations.c.project_id).where(iterations.c.id == obj.iteration_hint_id)).scalar_one_or_none()
    if table.name == "task_events" and obj.task_id is None:
        import json
        payload = json.loads(obj.payload or "{}")
        triage_id = payload.get("triage_item_id") if isinstance(payload, dict) else None
        if triage_id in session.info.get("command_triage_projects", {}):
            return session.info["command_triage_projects"][triage_id]
    value = getattr(obj, "project_id", None)
    if value is not None:
        return value
    entity_type, entity_id = getattr(obj, "entity_type", None), getattr(obj, "entity_id", None)
    if table.name == "outbound_webhook_deliveries":
        event_table = Base.metadata.tables["outbound_webhook_events"]
        row = session.connection().execute(select(event_table.c.entity_type, event_table.c.entity_id).where(event_table.c.id == obj.event_id)).first()
        if row:
            entity_type, entity_id = row
    if entity_type == "triage_item" and entity_id in session.info.get("command_triage_projects", {}):
        return session.info["command_triage_projects"][entity_id]
    targets = {"task": "tasks", "project": "projects", "iteration": "iterations", "release": "releases"}
    if entity_type in targets and entity_id is not None:
        target = Base.metadata.tables[targets[entity_type]]
        column = target.c.id if entity_type == "project" else target.c.project_id
        value = session.connection().execute(select(column).where(target.c.id == entity_id)).scalar_one_or_none()
        if value is None and entity_type == "task":
            value = session.info.get("command_task_projects", {}).get(entity_id)
        return value
    for key, target in (("iteration_id", "iterations"), ("task_id", "tasks"), ("milestone_id", "project_milestones"), ("release_id", "releases")):
        foreign_id = getattr(obj, key, None)
        if foreign_id is not None:
            target_table = Base.metadata.tables[target]
            if "project_id" in target_table.c:
                return session.connection().execute(select(target_table.c.project_id).where(target_table.c.id == foreign_id)).scalar_one_or_none()
    return None


@event.listens_for(Session, "before_flush")
def authorize_domain_writes(session, _flush_context, _instances):
    authority = session.info.get("authority")
    if authority is None or session.info.get("authority_internal"):
        return
    from app.models.identity import CommandAudit
    from app.models.task import Task
    from app.models.agent import AgentTaskAssignment
    protocol = authority.kind == "agent" and authority.source in {"agent_rest", "mcp"}
    rework_actors = {obj.actor_id for obj in session.new if isinstance(obj, AgentTaskAssignment) and obj.task_id in session.info.get("review_rework_tasks", set())}
    pending = session.info.setdefault("authority_audit_pending", [])
    seen = session.info.setdefault("authority_audited", set())
    for obj in list(session.new) + list(session.dirty) + list(session.deleted):
        if isinstance(obj, CommandAudit) or not session.is_modified(obj, include_collections=True) and obj not in session.deleted:
            continue
        table = inspect(type(obj)).local_table.name
        changed = {attr.key for attr in inspect(obj).attrs if attr.history.has_changes()}
        if table == "agent_actors" and changed <= {"queue_revision", "updated_at"} and obj.id in session.info.get("domain_queue_actors", set()):
            continue
        if protocol and table == "agent_actors" and changed <= {"queue_revision", "updated_at"} and (obj.id == authority.actor_id or obj.id in rework_actors):
            continue
        if table == "agent_actors" and obj.id == authority.actor_id and changed <= {"last_seen_at"} and obj not in session.deleted and obj not in session.new:
            continue
        owned_personal = (table == "user_sessions" and obj.principal_id == authority.principal_id and authority.principal_id is not None
                          or table == "saved_views" and obj.scope == "personal" and
                          (obj.owner_principal_id == authority.principal_id and authority.principal_id is not None or obj.created_by_session_id == authority.session_id and authority.session_id is not None))
        if protocol and table == "agent_idempotency_records" and obj.actor_id == authority.actor_id:
            owned_personal = True
        project_id = _object_project(session, obj)
        action = "edit"
        if protocol and table == "agent_runs" and obj.actor_id == authority.actor_id:
            action = "execute"
        if protocol and table == "agent_task_assignments":
            if obj.actor_id == authority.actor_id and obj not in session.new:
                action = "review" if obj.purpose == "verification" else "execute"
            elif obj in session.new and obj.task_id in session.info.get("review_rework_tasks", set()):
                action = "review"
        derived = table in {"task_brief_revisions", "task_progress_records", "task_review_records", "task_status_logs", "task_events", "outbound_webhook_events", "outbound_webhook_deliveries", "application_snapshots", "task_routing_assessments", "agent_run_events"}
        if derived and not authority.allows(project_id, action):
            action = "execute" if authority.allows(project_id, "execute") else "review"
        if isinstance(obj, Task):
            claim_fields = {"claimed_by", "claim_id", "claim_generation", "claim_expires_at", "version", "updated_at", "execution_mode"}
            prior_claims = inspect(obj).attrs.claimed_by.history.deleted
            if protocol and changed <= claim_fields and ("execution_mode" not in changed or obj.execution_mode == "scheduled") and obj.claimed_by in {None, authority.actor_id} and all(prior in {None, authority.actor_id} for prior in prior_claims):
                action = "execute"
            if changed <= {"progress", "artifact_revision", "accepted_at", "accepted_by_principal_id", "accepted_version", "version", "updated_at"}:
                action = "execute"
            history = inspect(obj).attrs.status.history
            rollup = obj.id in session.info.get("derived_rollups", set()) and obj.is_summary
            if history.has_changes() and obj.status in {"active", "resolved"}:
                action = "review" if obj.id in session.info.get("review_rework_tasks", set()) and obj.status == "active" else "execute"
            if history.has_changes() and obj.status == "closed" and not rollup:
                action = "review"
                if authority.kind == "system" and obj.accepted_at is not None and (not authority.review_override or not authority.reason):
                    raise AuthorityError("accountable_review_required", "System acceptance requires an explicit operator override and reason.")
                if authority.kind == "agent" and authority.actor_role != "verifier":
                    raise AuthorityError("independent_review_required", "Execution cannot accept its own work.")
                if obj.executed_by_principal_id is not None and obj.executed_by_principal_id == authority.principal_id:
                    if not authority.operator or not authority.review_override or not authority.reason:
                        raise AuthorityError("independent_review_required", "Use another reviewer or an explicit accountable operator override.")
            if rollup and not authority.allows(project_id, action):
                action = "execute" if authority.allows(project_id, "execute") else "review"
        if not owned_personal and not authority.allows(project_id, action):
            raise AuthorityError()
        global_tables = {"system_settings", "principals", "identity_subjects", "workspace_memberships", "workspace_authority_state",
                         "project_memberships", "principal_profile_links", "outbound_webhook_targets", "agent_model_bindings", "agent_actors",
                         "team_member_profiles", "team_member_profile_skills", "calendars"}
        if table in global_tables and not authority.operator and not (authority.local and table in {"calendars", "team_member_profiles", "team_member_profile_skills"}):
            raise AuthorityError("operator_required", "Workspace operator permission is required.")
        if isinstance(obj, Task) and inspect(obj).attrs.project_id.history.deleted:
            for old in inspect(obj).attrs.project_id.history.deleted:
                if not authority.allows(old, "edit"):
                    raise AuthorityError()
        if isinstance(obj, Task):
            session.info.setdefault("command_task_projects", {})[obj.id] = obj.project_id
        if id(obj) not in seen:
            seen.add(id(obj))
            fields = [attr.key for attr in inspect(obj).mapper.column_attrs if inspect(obj).attrs[attr.key].history.has_changes()]
            pending.append((obj, table, project_id, action, fields))


@event.listens_for(Session, "after_flush_postexec")
def append_command_audit(session, _flush_context):
    authority = session.info.get("authority")
    if authority is None:
        return
    from app.models.identity import CommandAudit
    for obj, table, project_id, action, fields in session.info.pop("authority_audit_pending", []):
        session.add(CommandAudit(principal_id=authority.principal_id, project_id=project_id,
            action=f"{table}:{action}", source=authority.source, correlation_id=authority.correlation_id,
            reason=authority.reason, details={"entity_id": getattr(obj, "id", None), "changed_fields": fields,
                                            "review_override": authority.review_override}))
