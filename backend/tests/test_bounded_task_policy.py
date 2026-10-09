"""Nested UI detail observes inherited policy without loading an execution graph."""

import pytest
from sqlalchemy import func, select

from app.authority import Authority, AuthorityError
from app.models.identity import CommandAudit
from app.models.task import Task
from app.services.task_detail_service import TaskDetailService
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import managed_store


async def test_nested_detail_returns_current_flags_without_graph_hydration(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        nested = await db.get(Task, scenario.tasks['nested'])
        parent = await db.get(Task, nested.parent_id)
        parent.is_deferred = True
        parent.is_optional = True
        await db.commit()
    async with factory() as db:
        count = await db.scalar(select(func.count()).select_from(CommandAudit))
        detail = await TaskDetailService(db).detail(scenario.tasks['nested'])
        assert detail.task.effective_is_deferred and detail.task.effective_is_optional
        assert not detail.execution_context_complete
        task = await db.get(Task, scenario.tasks['nested'])
        assert 'children' not in task.__dict__ and 'parent' not in task.__dict__
        assert await db.scalar(select(func.count()).select_from(CommandAudit)) == count


async def test_deep_policy_is_complete_while_displayed_ancestry_remains_bounded(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        parent_id = None
        for depth in range(25):
            node = Task(title=f'Nested work {depth}', project_id=scenario.projects[0], parent_id=parent_id, is_deferred=depth == 0)
            db.add(node)
            await db.flush()
            parent_id = node.id
        await db.commit()
        leaf_id = parent_id
    async with factory() as db:
        detail = await TaskDetailService(db).detail(leaf_id, limit=10)
        assert detail.task.effective_is_deferred
        assert len(detail.ancestors) == 20 and not detail.ancestors_complete
        assert not detail.execution_context_complete


async def test_hidden_parent_policy_cannot_disclose_private_scope(managed_store):
    factory, scenario, _, principals = managed_store
    async with factory() as db:
        hidden = Task(title='Private parent', project_id=scenario.projects[1], is_deferred=True)
        db.add(hidden)
        await db.flush()
        visible = Task(title='Legacy visible child', project_id=scenario.projects[0], parent_id=hidden.id)
        db.add(visible)
        await db.commit()
        leaf_id = visible.id
    async with factory() as db:
        db.info['authority'] = Authority(principals[0], 'human', projects={scenario.projects[0]: 'editor'})
        with pytest.raises(AuthorityError):
            await TaskDetailService(db).detail(leaf_id)


async def test_project_tree_serialization_preserves_loaded_parent_policy(delivery_store):
    from app.services.project_service import ProjectService
    from app.services.task_service import TaskService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        nested = await db.get(Task, scenario.tasks['nested'])
        parent = await db.get(Task, nested.parent_id)
        parent.is_deferred = True
        await db.commit()
    async with factory() as db:
        roots = await ProjectService(db).get_tasks(scenario.projects[0])
        responses = [TaskService(db).task_to_response(task) for task in roots]
        nested = next(child for root in responses for child in root.children if child.id == scenario.tasks['nested'])
        assert nested.effective_is_deferred
