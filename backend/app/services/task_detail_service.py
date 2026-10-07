"""Small UI reads, independent of the complete authoritative execution graph."""

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import selectinload, raiseload

from app.authority import require_project
from app.models.task import Task, TaskDependency
from app.schemas.task_detail import TaskDetailResponse, TaskReference, TaskReferencePage
from app.schemas.task import TaskAgentReadiness


class TaskDetailService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def references():
        from app.models.project import Project
        from app.models.iteration import Iteration
        return select(Task.id, Task.title, Task.version, Task.status, Task.project_id, Task.iteration_id,
            Task.parent_id, Task.owner_profile_id, Project.name.label("project_name"), Iteration.name.label("iteration_name"),
            Task.blocked_reason, Task.canceled_at,
            and_(Task.status == "closed", Task.accepted_at.is_not(None), Task.accepted_by_principal_id.is_not(None), Task.accepted_version.is_not(None),
                 Task.accepted_version == Task.version, Task.canceled_at.is_(None)).label("acceptance_current")
            ).outerjoin(Project, Project.id == Task.project_id).outerjoin(Iteration, Iteration.id == Task.iteration_id)

    async def page(self, query, *, limit=50, after_id=0):
        if not 1 <= limit <= 100 or after_id < 0:
            raise ValueError("Use a limit from 1 to 100 and a nonnegative cursor")
        rows = (await self.db.execute(query.where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).all()
        more = len(rows) > limit
        items = [TaskReference.model_validate(row) for row in rows[:limit]]
        return TaskReferencePage(items=items, has_more=more, next_after_id=items[-1].id if more else None, limit=limit)

    async def lookup(self, *, project_id=None, iteration_id=None, query=None, backlog_only=False, limit=50, after_id=0, status=None, parent_id=None, roots_only=False):
        statement = self.references()
        if project_id is not None:
            require_project(self.db, project_id)
            statement = statement.where(Task.project_id == project_id)
        if iteration_id is not None:
            statement = statement.where(Task.iteration_id == iteration_id)
        if backlog_only:
            statement = statement.where(Task.iteration_id.is_(None))
        if status is not None:
            if status not in {"planned", "active", "resolved", "closed"}:
                raise ValueError("Select a supported task status")
            statement = statement.where(Task.status == status)
        if roots_only and parent_id is not None:
            raise ValueError("Select roots or a parent, not both")
        if roots_only:
            statement = statement.where(Task.parent_id.is_(None))
        if parent_id is not None:
            parent = await self.db.get(Task, parent_id)
            if parent is None:
                raise LookupError("Parent task not found or inaccessible")
            require_project(self.db, parent.project_id)
            if project_id is not None and parent.project_id != project_id or iteration_id is not None and parent.iteration_id != iteration_id:
                raise ValueError("Parent must belong to the selected scope")
            statement = statement.where(Task.parent_id == parent_id)
        if query:
            if len(query) > 200:
                raise ValueError("Search text must contain at most 200 characters")
            from app.sql_semantics import portable_contains
            text = query.strip()
            identifier = text.removeprefix("#")
            predicate = portable_contains(Task.title, text)
            if identifier.isascii() and identifier.isdigit() and len(identifier) <= 18:
                predicate = or_(predicate, Task.id == int(identifier))
            statement = statement.where(predicate)
        return await self.page(statement, limit=limit, after_id=after_id)

    async def my_work(self, *, limit=50, after_id=0, project_id=None, iteration_id=None, backlog_only=False):
        """Bounded human ownership queues, independent of exact-agent assignment decisions."""
        from app.services.task_domain_service import TaskDomainService
        authority = self.db.info.get("authority")
        queues = {key: [] for key in ("active", "queued", "blocked", "awaiting_review")}
        if authority is None or authority.kind != "human" or authority.profile_id is None:
            return {"state": "profile_unlinked", "queues": queues, "has_more": False, "next_after_id": None}
        if not authority.operator and not authority.local and not authority.projects and not authority.workspace_role:
            return {"state": "membership_required", "queues": queues, "has_more": False, "next_after_id": None}
        statement = self.references().where(Task.owner_profile_id == authority.profile_id,
            or_(Task.status != "closed", Task.accepted_at.is_(None), Task.accepted_by_principal_id.is_(None), Task.accepted_version.is_(None), Task.accepted_version != Task.version),
            Task.canceled_at.is_(None), Task.is_summary.is_(False))
        if backlog_only and iteration_id is not None:
            raise ValueError("Select backlog or an iteration, not both")
        if project_id is not None:
            from app.authority import require_project
            require_project(self.db, project_id)
            statement = statement.where(Task.project_id == project_id)
        if iteration_id is not None:
            statement = statement.where(Task.iteration_id == iteration_id)
        if backlog_only:
            statement = statement.where(Task.iteration_id.is_(None))
        page = await self.page(statement, limit=limit, after_id=after_id)
        for item in page.items:
            actions = await TaskDomainService(self.db).allowed_actions(item.id)
            blocked = item.status == "closed" or bool(item.blocked_reason) or any(
                blocker.code in {"dependencies_incomplete", "dependency_incomplete"}
                for action in actions.actions if action.action == "start_manual" for blocker in action.blockers)
            from app.services.delivery_dependency_service import DeliveryDependencyService
            blocked = blocked or not await DeliveryDependencyService(self.db).ready(item.id)
            category = "blocked" if blocked else "awaiting_review" if item.status == "resolved" else "active" if item.status == "active" else "queued"
            queues[category].append({**item.model_dump(mode="json"), "actions": actions.model_dump(mode="json")["actions"]})
        return {"state": "ready", "queues": queues, "has_more": page.has_more, "next_after_id": page.next_after_id}

    async def detail(self, task_id, *, limit=50, children_after_id=0, dependencies_after_id=0):
        from app.services.task_service import TaskService
        task = await self.db.scalar(select(Task).where(Task.id == task_id).options(raiseload("*"),
            selectinload(Task.project), selectinload(Task.iteration), selectinload(Task.assignee), selectinload(Task.owner_profile), selectinload(Task.milestone), selectinload(Task.claimed_agent)))
        if task is None:
            return None
        require_project(self.db, task.project_id)
        await TaskService(self.db).load_owner_names([task])
        response = TaskService(self.db).task_to_response(task)
        # A detail projection is never eligible as input to dispatch or scheduling.
        response.children = []
        response.dependencies = []
        response.agent_readiness = TaskAgentReadiness(blocker_codes=["execution_context_required"], blockers=["Load the complete execution context to evaluate agent readiness."])
        children = await self.page(self.references().where(Task.parent_id == task.id), limit=limit, after_id=children_after_id)
        dependencies = await self.page(self.references().join(TaskDependency, TaskDependency.depends_on_id == Task.id).where(TaskDependency.task_id == task.id), limit=limit, after_id=dependencies_after_id)
        ancestors, seen, parent_id = [], {task.id}, task.parent_id
        for _ in range(20):
            if parent_id is None:
                break
            if parent_id in seen:
                raise ValueError("Task ancestry contains a cycle")
            seen.add(parent_id)
            row = (await self.db.execute(self.references().where(Task.id == parent_id))).first()
            if row is None:
                break
            ancestors.append(TaskReference.model_validate(row))
            parent_id = row.parent_id
        response.is_composite = response.is_composite or bool(children.items)
        return TaskDetailResponse(task=response, ancestors=list(reversed(ancestors)), ancestors_complete=parent_id is None, children=children, dependencies=dependencies)
