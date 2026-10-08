"""Allocation membership recovery preserves durable references and rolls back failures."""

import httpx
import pytest
from sqlalchemy import func, select, text

from app.commands import PlanningConflict
from app.main import app
from app.models.agent import AgentTaskAssignment
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from app.schemas.team import TeamMemberCreate
from app.services.snapshot_service import SnapshotService
from app.services.team_service import TeamService
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import managed_store


async def capture_then_add(factory, scenario):
    async with factory() as db:
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "saved_membership")
        profile = TeamMemberProfile(display_name="Later owner", profile_kind="human")
        db.add(profile)
        await db.commit()
        member = await TeamService(db).create(scenario.iterations[0], TeamMemberCreate(
            name="Later allocation", position="Engineer", profile_id=profile.id))
        return saved, member.id, profile.id


async def test_extra_allocation_detaches_but_global_owner_and_profile_identity_survive(delivery_store):
    factory, scenario, _ = delivery_store
    saved, member_id, profile_id = await capture_then_add(factory, scenario)
    async with factory() as db:
        project = await db.get(Project, scenario.projects[0])
        project.owner_id = member_id
        await db.commit()
        await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        member = await db.get(TeamMember, member_id)
        assert member.iteration_id is None and member.profile_id == profile_id
        assert (await db.get(Project, scenario.projects[0])).owner_id == member_id
        assert await db.get(TeamMemberProfile, profile_id) is not None


@pytest.mark.parametrize("reference", ["external_task", "queued_assignment"])
async def test_incompatible_allocation_reference_rejects_before_recovery_changes(delivery_store, reference):
    factory, scenario, _ = delivery_store
    saved, member_id, _ = await capture_then_add(factory, scenario)
    async with factory() as db:
        if reference == "external_task":
            (await db.get(Task, scenario.tasks["other_project"])).assignee_id = member_id
        else:
            db.add(AgentTaskAssignment(task_id=scenario.tasks["planned"], actor_id=scenario.actors[0],
                team_member_id=member_id, purpose="execution", state="queued", task_version=1))
        await db.commit()
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        with pytest.raises(PlanningConflict, match="references"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        assert (await db.get(TeamMember, member_id)).iteration_id == scenario.iterations[0]
        assert (await db.get(Iteration, scenario.iterations[0])).revision == revision
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_failure_after_detach_restores_membership_and_retains_recovery_history(delivery_store, monkeypatch):
    from app.services.task_brief_service import TaskBriefService

    factory, scenario, _ = delivery_store
    saved, member_id, _ = await capture_then_add(factory, scenario)
    async with factory() as db:
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        async def fail(*_args, **_kwargs):
            raise RuntimeError("Injected restored brief failure")
        monkeypatch.setattr(TaskBriefService, "restore_brief", fail)
        with pytest.raises(RuntimeError, match="restored brief"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        assert (await db.get(TeamMember, member_id)).iteration_id == scenario.iterations[0]
        assert (await db.get(Iteration, scenario.iterations[0])).revision == revision
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_unknown_physical_allocation_reference_fails_closed(delivery_store):
    factory, scenario, _ = delivery_store
    saved, member_id, _ = await capture_then_add(factory, scenario)
    async with factory() as db:
        await db.execute(text("CREATE TABLE extension_allocation_link (id INTEGER PRIMARY KEY, allocation_id INTEGER REFERENCES team_members(id))"))
        await db.commit()
        try:
            with pytest.raises(PlanningConflict, match="reference ownership"):
                await SnapshotService(db).restore(scenario.iterations[0], saved)
            assert (await db.get(TeamMember, member_id)).iteration_id == scenario.iterations[0]
        finally:
            await db.execute(text("DROP TABLE extension_allocation_link"))
            await db.commit()


async def test_saved_allocation_external_reference_is_preflighted_too(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "saved_reference")
        (await db.get(Task, scenario.tasks["other_project"])).assignee_id = scenario.capacity_rows[0]
        await db.commit()
        with pytest.raises(PlanningConflict, match="references"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        assert (await db.get(Task, scenario.tasks["other_project"])).assignee_id == scenario.capacity_rows[0]


async def test_operator_rest_restore_reconciles_exact_allocation_membership(managed_store):
    factory, scenario, _, _ = managed_store
    # Setup is an owned store operation; the restore itself uses the real operator boundary.
    from app.authority import Authority
    async with factory() as db:
        from app.models.identity import WorkspaceAuthorityState
        system = await db.get(WorkspaceAuthorityState, 1)
        db.info["authority"] = Authority(system.operator_principal_id, "system", workspace_role="operator")
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "operator_membership")
        profile = TeamMemberProfile(display_name="Later person", profile_kind="human")
        db.add(profile)
        await db.commit()
        member = await TeamService(db).create(scenario.iterations[0], TeamMemberCreate(
            name="Later allocation", position="Engineer", profile_id=profile.id))
        member_id = member.id
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://test") as operator:
        result = await operator.post(f"/api/iterations/{scenario.iterations[0]}/snapshots/{saved}/restore",
            headers={"X-Admin-API-Key": "managed-operator-fixture"}, json={"confirm": True, "expected_revision": revision})
        assert result.status_code == 200, result.text
    async with factory() as db:
        ids = set((await db.scalars(select(TeamMember.id).where(TeamMember.iteration_id == scenario.iterations[0]))).all())
        assert ids == {scenario.capacity_rows[0]}
        assert (await db.get(TeamMember, member_id)).iteration_id is None
