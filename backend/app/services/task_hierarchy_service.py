"""Read-only ownership of bounded task graph hydration and integrity checks."""
from sqlalchemy import select
from sqlalchemy.orm import attributes, selectinload
from app.models.task import Task, TaskDependency
from app.models.team_member import TeamMember
from app.models.request_source import RequestSourceLink
from app.query_limits import CollectionLimitExceededError, MAX_ITERATION_TREE_TASKS

class TaskTreeIntegrityError(ValueError):
    """Raised when persisted task parent links cannot form a valid iteration tree."""


class TaskHierarchyService:
    def __init__(self, db, load_owner_names):
        self.db = db
        self.load_owner_names = load_owner_names

    def _task_graph_query(self, iteration_id: int | None, project_id: int | None = None):
        """Build the bounded relationship query used before in-memory tree assembly."""
        return (
            select(Task)
            .where(Task.iteration_id == iteration_id, *([Task.project_id == project_id] if iteration_id is None else []))
            .execution_options(populate_existing=True)
            .options(
                selectinload(Task.owner_profile),
                selectinload(Task.project),
                selectinload(Task.milestone),
                selectinload(Task.assignee).selectinload(TeamMember.vacations),
                selectinload(Task.claimed_agent),
                selectinload(Task.external_links),
                selectinload(Task.request_source_links).selectinload(
                    RequestSourceLink.request_source
                ),
            )
            .order_by(Task.sort_order, Task.id)
        )

    async def _load_iteration_tree(
        self,
        iteration_id: int,
        *,
        max_tasks: int = MAX_ITERATION_TREE_TASKS,
        project_id: int | None = None,
    ) -> tuple[list[Task], dict[int, Task]]:
        """Load and defensively assemble a contract-bounded iteration."""
        identities = select(Task.id).where(Task.iteration_id == iteration_id,
            *([Task.project_id == project_id] if iteration_id is None else [])).limit(max_tasks + 1)
        if len((await self.db.scalars(identities)).all()) > max_tasks:
            raise CollectionLimitExceededError("iteration task tree", max_tasks)
        result = await self.db.execute(
            self._task_graph_query(iteration_id, project_id).limit(max_tasks + 1)
        )
        tasks = list(result.scalars().all())
        if len(tasks) > max_tasks:
            raise CollectionLimitExceededError("iteration task tree", max_tasks)
        await self.load_owner_names(tasks)
        tasks_by_id = {task.id: task for task in tasks}

        # Relationship access from synchronous scheduling/snapshot serializers
        # must never initiate async I/O.  Rebuild this collection explicitly
        # from one bounded query so concurrent flushes cannot leave a task with
        # an expired or partially populated dependency relationship.
        dependencies_by_task: dict[int, list[TaskDependency]] = {
            task.id: [] for task in tasks
        }
        if tasks_by_id:
            dependency_result = await self.db.execute(
                select(TaskDependency)
                .where(TaskDependency.task_id.in_(tasks_by_id))
                .options(selectinload(TaskDependency.depends_on))
                .order_by(TaskDependency.task_id, TaskDependency.id)
            )
            for dependency in dependency_result.scalars():
                dependencies_by_task[dependency.task_id].append(dependency)
        for task in tasks:
            attributes.set_committed_value(
                task,
                "dependencies",
                dependencies_by_task[task.id],
            )

        visit_state: dict[int, int] = {}

        def visit(task: Task) -> None:
            state = visit_state.get(task.id, 0)
            if state == 1:
                raise TaskTreeIntegrityError(
                    f"Task tree cycle detected in iteration {iteration_id} at task {task.id}."
                )
            if state == 2:
                return
            visit_state[task.id] = 1
            if task.parent_id is not None:
                parent = tasks_by_id.get(task.parent_id)
                if parent is None:
                    raise TaskTreeIntegrityError(
                        f"Task {task.id} references missing or cross-iteration parent {task.parent_id}."
                    )
                visit(parent)
            visit_state[task.id] = 2

        for task in tasks:
            visit(task)

        roots: list[Task] = []
        children_by_parent: dict[int, list[Task]] = {task.id: [] for task in tasks}
        for task in tasks:
            if task.parent_id is None:
                roots.append(task)
                attributes.set_committed_value(task, "parent", None)
                continue
            parent = tasks_by_id[task.parent_id]
            children_by_parent[parent.id].append(task)
            attributes.set_committed_value(task, "parent", parent)

        for task in tasks:
            children = sorted(
                children_by_parent[task.id],
                key=lambda child: (child.sort_order, child.id),
            )
            attributes.set_committed_value(task, "children", children)
        roots.sort(key=lambda root: (root.sort_order, root.id))
        return roots, tasks_by_id
