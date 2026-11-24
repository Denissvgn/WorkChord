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
            accepted = await self._accepted(kind, target)
            entry = {"id": edge.id, "kind": kind, "target_id": target.id,
                "title": target.title if kind == "task" else target.name,
                "target_branch": edge.target_branch, "merge": None, "hold": None}
            if edge.target_branch is None:
                entry.update(ready=accepted, reason=None if accepted else "prerequisite_acceptance_required")
            else:
                merge = await self._merge_evidence(target, edge.target_branch)
                ready = accepted and merge["verified"]
                entry.update(ready=ready, merge=merge)
                if not ready:
                    entry["reason"] = "prerequisite_acceptance_required" if not accepted else "prerequisite_merge_not_observed"
                    entry["hold"] = self._hold(target, edge.target_branch, accepted, merge, entry["reason"])
                else:
                    entry["reason"] = None
            result.append(entry)
        return result

    async def holds(self, task_id):
        """Prerequisites that keep a task from starting, each with its reason and next owner."""
        return [item for item in await self.projection(task_id) if not item["ready"]]

    async def _merge_evidence(self, target, branch):
        """Read stored pull request observations only; this never calls GitHub."""
        from app.services.github_reconciliation_service import GitHubReconciliationService, pull_state
        pulls = []
        for link in await GitHubReconciliationService(self.db)._pull_links(target.id):
            meta = link.metadata_json or {}
            pulls.append({"link_id": link.id, "url": link.url, "state": pull_state(link), "target_branch": meta.get("base_ref"),
                "merge_commit_sha": meta.get("merge_commit_sha"), "observed_at": meta.get("observed_at") or meta.get("status_refreshed_at")})
        verified = [pull for pull in pulls if pull["state"] == "merged" and pull["target_branch"] == branch and pull["merge_commit_sha"]]
        if verified:
            state = "merged_on_target"
        elif not pulls or all(pull["state"] == "unobserved" for pull in pulls):
            state = "not_observed"
        elif any(pull["state"] in {"open", "draft"} for pull in pulls):
            state = "open_pull_request"
        elif any(pull["state"] == "merged" for pull in pulls):
            state = "merged_on_other_branch"
        else:
            state = "closed_unmerged"
        return {"state": state, "verified": bool(verified), "target_branch": branch, "pull_requests": pulls}

    @staticmethod
    def _hold(target, branch, accepted, merge, reason):
        """Name who acts next for a prerequisite that needs accepted code on a branch."""
        label = f"task {target.id}"
        state = merge["state"]
        if not accepted:
            owner = "reviewer" if target.status == "resolved" else "worker"
            if state == "merged_on_target":
                action = f"Code for {label} is merged on {branch}; the independent reviewer must still accept it."
            elif owner == "reviewer":
                action = f"Review and accept {label}; its code must also be merged on {branch}."
            else:
                action = f"Finish and submit {label}; it must then be accepted and merged on {branch}."
            case = "open_pull_request" if state == "open_pull_request" else "not_accepted"
        else:
            owner, case = "pm", state
            action = {
                "open_pull_request": f"Have the accepted pull request for {label} merged into {branch}, then run GitHub catch-up for it.",
                "merged_on_other_branch": f"The pull request for {label} merged into a branch other than {branch}; merge it into {branch} or change the prerequisite branch.",
                "closed_unmerged": f"The pull request for {label} closed without merging; reopen it or record a replacement task.",
            }.get(state, f"No merge into {branch} is observed for {label}; link its pull request if missing, then run GitHub catch-up.")
        return {"case": case, "reason": reason, "next_owner": owner, "next_action": action}

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
        from app.models.task_replacement import TaskReplacement
        with internal_authority(self.db):
            replaced = set((await self.db.scalars(select(TaskReplacement.original_task_id).where(
                TaskReplacement.original_task_id.in_([leaf.id for leaf in leaves])))).all())
        # A replaced original's deliverable is counted once, through its replacement.
        leaves = [leaf for leaf in leaves if leaf.id not in replaced]
        return bool(leaves) and all([await self._accepted("task", leaf) for leaf in leaves])

    async def ready(self, task_id):
        return all(item["ready"] for item in await self.projection(task_id))

    @atomic_command
    async def add(self, task_id, kind, target_id, expected_version, target_branch=None):
        from app.services.task_service import TaskService
        from app.services.task_brief_service import clear_execution_evidence
        if kind not in {"task", "milestone"}:
            raise ValueError("Use a task or milestone prerequisite")
        if kind == "task" and task_id == target_id:
            raise PlanningConflict("delivery_dependency_cycle", "A task cannot depend on itself.")
        target_branch = self._branch(target_branch, kind)
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
        if target_branch is not None and target.is_summary:
            raise ValueError("A target branch applies to a leaf task prerequisite")
        if existing and existing.target_branch == target_branch:
            return await self.projection(task_id)
        await service.reserve_task_version(task, expected_version)
        await service._require_unclaimed_structure([task.id])
        if existing:
            existing.target_branch = target_branch
        else:
            self.db.add(DeliveryDependency(task_id=task_id, target_branch=target_branch, **{column.key: target_id}))
        self.db.info.setdefault("delivery_changed_nodes", set()).add(("task", task.id))
        clear_execution_evidence(task)
        await self.db.flush()
        await self.validate_cycles()
        return await self.projection(task_id)

    @staticmethod
    def _branch(value, kind):
        if value is None:
            return None
        if kind != "task":
            raise ValueError("A target branch applies only to a task prerequisite")
        branch = value.strip().removeprefix("refs/heads/")
        if not branch or len(branch) > 255 or any(char.isspace() for char in branch):
            raise ValueError("Use a branch name without spaces")
        return branch

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
            if task_ids:
                from app.models.task_replacement import TaskReplacement
                linked = await self.db.scalar(select(TaskReplacement.id).where(
                    TaskReplacement.original_task_id.in_(task_ids) | TaskReplacement.replacement_task_id.in_(task_ids)).limit(1))
                if linked is not None:
                    raise PlanningConflict("task_replacement_referenced", "A replacement disposition retains this work for audit.")

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
