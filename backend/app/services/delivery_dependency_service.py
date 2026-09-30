"""Authorized delivery readiness, global cycles and downstream evidence invalidation."""

from collections import defaultdict, deque

from sqlalchemy import or_, select

from app.authority import AuthorityError, internal_authority, require_project
from app.commands import PlanningConflict, atomic_command, lock_planning
from app.models.delivery_dependency import DeliveryDependency
from app.models.project import ProjectMilestone
from app.models.task import Task, TaskDependency


class DeliveryDependencyService:
    def __init__(self, db):
        self.db = db

    async def graph(self):
        """Only identifiers enter the internal graph; no hidden work is serialized."""
        graph = defaultdict(set)
        with internal_authority(self.db):
            for task_id, parent, milestone in (await self.db.execute(select(Task.id, Task.parent_id, Task.milestone_id))).all():
                graph[("task", task_id)]
                if parent:
                    graph[("task", parent)].add(("task", task_id))
                if milestone:
                    graph[("milestone", milestone)].add(("task", task_id))
            for source, target in (await self.db.execute(select(TaskDependency.task_id, TaskDependency.depends_on_id))).all():
                graph[("task", source)].add(("task", target))
            for source, task, milestone in (await self.db.execute(select(DeliveryDependency.task_id,
                DeliveryDependency.prerequisite_task_id, DeliveryDependency.prerequisite_milestone_id))).all():
                graph[("task", source)].add(("task", task) if task else ("milestone", milestone))
        return graph

    async def validate_cycles(self):
        graph = await self.graph()
        remaining = {node: len(targets) for node, targets in graph.items()}
        reverse = defaultdict(set)
        for node, targets in graph.items():
            for target in targets:
                reverse[target].add(node)
                remaining.setdefault(target, 0)
        queue = deque(node for node, count in remaining.items() if count == 0)
        while queue:
            node = queue.popleft()
            for parent in reverse[node]:
                remaining[parent] -= 1
                if remaining[parent] == 0:
                    queue.append(parent)
            remaining.pop(node)
        if remaining:
            raise PlanningConflict("delivery_dependency_cycle", "This change would create a delivery dependency cycle.")

    async def projection(self, task_id):
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise ValueError("Task not found or inaccessible")
        require_project(self.db, task.project_id)
        edges = (await self.db.scalars(select(DeliveryDependency).where(DeliveryDependency.task_id == task_id)
            .order_by(DeliveryDependency.id))).all()
        authority = self.db.info.get("authority")
        result = []
        for edge in edges:
            kind = "task" if edge.prerequisite_task_id else "milestone"
            model = Task if kind == "task" else ProjectMilestone
            target_id = edge.prerequisite_task_id or edge.prerequisite_milestone_id
            target = await self.db.scalar(select(model).where(model.id == target_id))
            visible = target is not None and (authority is None or authority.allows(target.project_id, "read"))
            if not visible:
                result.append({"id": edge.id, "kind": kind, "ready": False, "reason": "prerequisite_unavailable"})
                continue
            ready = await self._accepted(kind, target)
            result.append({"id": edge.id, "kind": kind, "target_id": target.id,
                "title": target.title if kind == "task" else target.name,
                "ready": ready, "reason": None if ready else "prerequisite_acceptance_required"})
        return result

    async def _accepted(self, kind, target):
        if kind == "task" and not target.is_summary:
            return target.status == "closed" and target.canceled_at is None and target.accepted_at is not None and target.accepted_by_principal_id is not None and target.accepted_version == target.version
        if kind == "milestone" and target.status != "completed":
            return False
        if kind == "task" and target.canceled_at:
            return False
        if kind == "task":
            from app.services.task_service import TaskService
            ids = await TaskService(self.db)._task_subtree_ids(target.id)
            query = select(Task).where(Task.id.in_(ids), Task.is_summary.is_(False))
        else:
            query = select(Task).where(Task.milestone_id == target.id, Task.is_summary.is_(False))
        leaves = (await self.db.scalars(query)).all()
        return bool(leaves) and all([await self._accepted("task", leaf) for leaf in leaves])

    async def ready(self, task_id):
        return all(item["ready"] for item in await self.projection(task_id))

    @atomic_command
    async def add(self, task_id, kind, target_id, expected_version):
        from app.services.task_service import TaskService
        from app.services.task_brief_service import clear_execution_evidence
        if kind not in {"task", "milestone"}:
            raise ValueError("Use a task or milestone prerequisite")
        if kind == "task" and task_id == target_id:
            raise PlanningConflict("delivery_dependency_cycle", "A task cannot depend on itself.")
        await lock_planning(self.db)
        service = TaskService(self.db)
        task = await service.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found or inaccessible")
        require_project(self.db, task.project_id, "edit")
        model = Task if kind == "task" else ProjectMilestone
        target = await self.db.scalar(select(model).where(model.id == target_id))
        if target is None:
            raise ValueError("Prerequisite not found or inaccessible")
        require_project(self.db, target.project_id, "read")
        column = DeliveryDependency.prerequisite_task_id if kind == "task" else DeliveryDependency.prerequisite_milestone_id
        existing = await self.db.scalar(select(DeliveryDependency).where(DeliveryDependency.task_id == task_id, column == target_id))
        service.ensure_expected_version(task, expected_version)
        if existing:
            return await self.projection(task_id)
        await service.reserve_task_version(task, expected_version)
        await service._require_unclaimed_structure([task.id])
        self.db.add(DeliveryDependency(task_id=task_id, **{column.key: target_id}))
        self.db.info.setdefault("delivery_changed_nodes", set()).add(("task", task.id))
        clear_execution_evidence(task)
        await self.db.flush()
        await self.validate_cycles()
        return await self.projection(task_id)

    @atomic_command
    async def remove(self, task_id, edge_id, expected_version):
        from app.services.task_service import TaskService
        from app.services.task_brief_service import clear_execution_evidence
        await lock_planning(self.db)
        service = TaskService(self.db)
        task = await service.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found or inaccessible")
        require_project(self.db, task.project_id, "edit")
        service.ensure_expected_version(task, expected_version)
        edge = await self.db.scalar(select(DeliveryDependency).where(DeliveryDependency.id == edge_id, DeliveryDependency.task_id == task_id))
        if edge:
            await service.reserve_task_version(task, expected_version)
            await service._require_unclaimed_structure([task.id])
            await self.db.delete(edge)
            self.db.info.setdefault("delivery_changed_nodes", set()).add(("task", task.id))
            clear_execution_evidence(task)
            await self.db.flush()
        return await self.projection(task_id)

    async def require_unreferenced(self, task_ids=(), milestone_id=None):
        with internal_authority(self.db):
            query = select(DeliveryDependency.id)
            if milestone_id is not None:
                query = query.where(DeliveryDependency.prerequisite_milestone_id == milestone_id)
            else:
                query = query.where(DeliveryDependency.prerequisite_task_id.in_(task_ids), DeliveryDependency.task_id.notin_(task_ids))
            if await self.db.scalar(query.limit(1)) is not None:
                raise PlanningConflict("delivery_dependency_referenced", "Remove incoming delivery dependencies before deleting or moving this work.")

    async def reconcile(self):
        nodes = self.db.info.pop("delivery_changed_nodes", set())
        changed_graph = self.db.info.pop("delivery_graph_changed", False)
        changed_scope = self.db.info.pop("delivery_scope_changed", set())
        if changed_scope:
            with internal_authority(self.db):
                linked = await self.db.scalar(select(DeliveryDependency.id).where(or_(
                    DeliveryDependency.task_id.in_(changed_scope), DeliveryDependency.prerequisite_task_id.in_(changed_scope))).limit(1))
            if linked:
                raise PlanningConflict("delivery_dependency_referenced", "Unlink delivery dependencies before changing project scope.")
        with internal_authority(self.db):
            if await self.db.scalar(select(DeliveryDependency.id).limit(1)) is None:
                return
        if changed_graph:
            await self.validate_cycles()
        if not nodes:
            return
        from app.services.task_service import TaskService
        from app.services.task_brief_service import clear_execution_evidence
        graph = await self.graph()
        reverse = defaultdict(set)
        for source, targets in graph.items():
            for target in targets:
                reverse[target].add(source)
        visited = set(nodes)
        queue = deque(nodes)
        affected = set()
        while queue:
            for source in reverse[queue.popleft()]:
                if source not in visited:
                    visited.add(source)
                    queue.append(source)
                    if source[0] == "task":
                        affected.add(source[1])
        self.db.info["delivery_reconciling"] = True
        try:
            with internal_authority(self.db):
                for task in (await self.db.scalars(select(Task).where(Task.id.in_(affected)).order_by(Task.id))).all():
                    await TaskService(self.db).reserve_task_version(task, task.version)
                    clear_execution_evidence(task)
                await self.db.flush()
        finally:
            self.db.info.pop("delivery_reconciling", None)
