"""Complete permission-safe observations for shared planning input mutations."""

from sqlalchemy import select

from app.authority import AuthorityError, internal_authority, require_operator, require_project
from app.commands import PlanningConflict
from app.config import get_settings


async def affected_iteration_ids(db, kind, values):
    """Resolve one complete scope for both read observations and atomic writes."""
    from app.models.calendar import Calendar
    from app.models.capacity import ProfileAvailability
    from app.models.iteration import Iteration
    from app.models.project import Project
    from app.models.task import Task
    from app.models.team_member import TeamMember, TeamMemberProfile, Vacation

    resource = {"calendar": Calendar, "project": Project, "iteration": Iteration,
                "profile": TeamMemberProfile, "member": TeamMember, "vacation": Vacation}
    field = {"calendar": "calendar_id", "project": "project_id", "iteration": "iteration_id",
             "profile": "profile_id", "member": "member_id", "vacation": "vacation_id"}.get(kind)
    identifier = values.get(field) if field else None
    entity = None
    if identifier is not None:
        entity = await db.get(resource[kind], identifier, populate_existing=True)
        if entity is None:
            raise LookupError("Planning input not found or inaccessible")
    authority = db.info.get("authority")
    trusted = authority is None and get_settings().workchord_auth_mode == "trusted_local" or authority is not None and authority.local
    if kind in {"calendar", "profile"} and not trusted:
        require_operator(db)
    if kind == "project":
        require_project(db, identifier, "edit")
    with internal_authority(db):
        if kind == "calendar":
            direct = select(Iteration.id).where(Iteration.calendar_id == identifier)
            shared = select(TeamMember.iteration_id).join(ProfileAvailability, ProfileAvailability.profile_id == TeamMember.profile_id).where(
                ProfileAvailability.calendar_id == identifier, TeamMember.iteration_id.is_not(None))
            query = direct.union(shared)
        elif kind == "project":
            query = select(Iteration.id).where(Iteration.project_id == identifier).union(
                select(Task.iteration_id).where(Task.project_id == identifier, Task.iteration_id.is_not(None)))
        elif kind == "profile":
            query = select(TeamMember.iteration_id).where(TeamMember.profile_id == identifier, TeamMember.iteration_id.is_not(None)).distinct()
        else:
            iteration_id = values.get("iteration_id")
            if kind == "iteration":
                iteration_id = identifier
            elif entity is not None and kind == "member":
                iteration_id = entity.iteration_id
            elif entity is not None and kind == "vacation":
                iteration_id = await db.scalar(select(TeamMember.iteration_id).where(TeamMember.id == entity.team_member_id))
            query = select(Iteration.id).where(Iteration.id == iteration_id)
        ids = sorted(set((await db.scalars(query.limit(501))).all()))
        if len(ids) > 500:
            raise PlanningConflict("planning_scope_oversized", "This planning input affects more than the supported revision context limit.")
        if authority is not None and not authority.operator and not authority.local:
            scopes = set((await db.scalars(select(Iteration.project_id).where(Iteration.id.in_(ids)))).all())
            scopes.update((await db.scalars(select(Task.project_id).where(Task.iteration_id.in_(ids)).distinct())).all())
            if any(not authority.allows(scope, "read") for scope in scopes):
                raise AuthorityError("incomplete_authorized_graph", "This context requires access to all scheduling inputs.")
            if kind in {"iteration", "member", "vacation"} and any(not authority.allows(scope, "edit") for scope in scopes):
                raise AuthorityError()
    return ids


async def observe_planning_input(db, kind, resource_id, *, creating_member=False):
    """Read data and revisions together; reject drift without advancing any state."""
    import json
    from app.models.calendar import Calendar
    from app.models.iteration import Iteration
    from app.models.project import Project
    from app.models.team_member import TeamMember, TeamMemberProfile, Vacation

    field = {"calendar": "calendar_id", "project": "project_id", "iteration": "iteration_id",
             "profile": "profile_id", "member": "member_id", "vacation": "vacation_id"}[kind]
    values = {"iteration_id": resource_id} if creating_member else {field: resource_id}
    model = Iteration if creating_member else {"calendar": Calendar, "project": Project,
        "iteration": Iteration, "profile": TeamMemberProfile, "member": TeamMember, "vacation": Vacation}[kind]

    async def revisions():
        ids = await affected_iteration_ids(db, kind, values)
        with internal_authority(db):
            return dict((await db.execute(select(Iteration.id, Iteration.revision).where(Iteration.id.in_(ids)).order_by(Iteration.id))).all())

    before = await revisions()
    columns = list(model.__table__.columns)
    row = (await db.execute(select(*columns).where(model.id == resource_id))).mappings().first()
    if row is None:
        raise LookupError("Planning input not found or inaccessible")
    after = await revisions()
    if before != after:
        raise PlanningConflict("planning_context_changed", "Planning input changed during this initial read. Reload before opening a draft.")
    if len(json.dumps(before, separators=(",", ":")).encode()) > 16384:
        raise PlanningConflict("planning_scope_oversized", "The complete revision context exceeds the supported header limit.")
    return {"kind": kind, "resource_id": resource_id, "resource": dict(row),
            "expected_revisions": before, "complete": True}
