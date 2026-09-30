"""Small UI reads, independent of the complete authoritative execution graph."""

from sqlalchemy import or_, select
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
        return select(Task.id, Task.title, Task.version, Task.status, Task.project_id, Task.iteration_id, Task.parent_id, Task.owner_profile_id)

    async def page(self, query, *, limit=50, after_id=0):
        if not 1 <= limit <= 100 or after_id < 0:
            raise ValueError("Use a limit from 1 to 100 and a nonnegative cursor")
        rows = (await self.db.execute(query.where(Task.id > after_id).order_by(Task.id).limit(limit + 1))).all()
        more = len(rows) > limit
        items = [TaskReference.model_validate(row) for row in rows[:limit]]
        return TaskReferencePage(items=items, has_more=more, next_after_id=items[-1].id if more else None, limit=limit)

    async def lookup(self, *, project_id=None, iteration_id=None, query=None, backlog_only=False, limit=50, after_id=0):
        statement = self.references()
        if project_id is not None:
            require_project(self.db, project_id)
            statement = statement.where(Task.project_id == project_id)
        if iteration_id is not None:
            statement = statement.where(Task.iteration_id == iteration_id)
        if backlog_only:
            statement = statement.where(Task.iteration_id.is_(None))
        if query:
            if len(query) > 200:
                raise ValueError("Search text must contain at most 200 characters")
            statement = statement.where(or_(Task.title.contains(query, autoescape=True), Task.description.contains(query, autoescape=True)))
        return await self.page(statement, limit=limit, after_id=after_id)

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
