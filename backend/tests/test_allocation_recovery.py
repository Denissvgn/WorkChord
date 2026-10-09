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


async def test_deleted_allocation_restore_preserves_replacement_global_owner(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original_profile = TeamMemberProfile(display_name="Original captured person", profile_kind="human")
        replacement_profile = TeamMemberProfile(display_name="Unrelated replacement person", profile_kind="human")
        db.add_all([original_profile, replacement_profile])
        await db.commit()
        original_profile_id, replacement_profile_id = original_profile.id, replacement_profile.id
        original = await TeamService(db).create(scenario.iterations[0], TeamMemberCreate(
            name="Captured allocation", position="Engineer", profile_id=original_profile_id))
        original_id = original.id
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "allocation_identity")
        assert await TeamService(db).delete(original_id)
        replacement = await TeamService(db).create(scenario.iterations[0], TeamMemberCreate(
            name="Replacement allocation", position="Engineer", profile_id=replacement_profile_id))
        replacement_id = replacement.id
        assert replacement_id > original_id
        project = await db.get(Project, scenario.projects[0])
        project.owner_id = replacement_id
        await db.commit()
        before = (replacement.name, replacement.profile_id, replacement.iteration_id, project.owner_id)
        await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        replacement = await db.get(TeamMember, replacement_id)
        project = await db.get(Project, scenario.projects[0])
        assert replacement is not None
        after = (replacement.name, replacement.profile_id, project.owner_id)
        assert after == (before[0], replacement_profile_id, replacement_id), {
            "captured_id": original_id, "replacement_id": replacement_id,
            "before": before, "after": after, "source_snapshot": saved,
        }


@pytest.mark.parametrize("same_profile", [False, True])
async def test_reused_lifetime_rejects_atomically_even_for_same_person(delivery_store, same_profile):
    from uuid import uuid4
    factory, scenario, _ = delivery_store
    async with factory() as db:
        member = await db.get(TeamMember, scenario.capacity_rows[0])
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "lifetime_guard")
        member.allocation_token = str(uuid4())
        if not same_profile:member.profile_id = None
        await db.commit()
        before = (member.allocation_token, member.profile_id)
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        with pytest.raises(PlanningConflict, match="lifetime"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        member = await db.get(TeamMember, scenario.capacity_rows[0])
        assert (member.allocation_token, member.profile_id) == before
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_profile_edit_retains_recoverable_allocation_lifetime(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        member = await db.get(TeamMember, scenario.capacity_rows[0])
        original = (member.allocation_token, member.profile_id)
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "profile_edit")
        member.profile_id = None
        await db.commit()
        await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        member = await db.get(TeamMember, scenario.capacity_rows[0])
        assert (member.allocation_token, member.profile_id) == original


async def test_missing_snapshot_lifetime_is_preserved_but_restore_is_held(delivery_store):
    import hashlib
    factory, scenario, _ = delivery_store
    async with factory() as db:
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "legacy_identity")
        row = await db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.filename == saved))
        payload = dict(row.payload)
        payload["team_members"] = [{key: value for key, value in member.items() if key != "allocation_token"} for member in payload["team_members"]]
        row.payload = payload
        row.checksum = hashlib.sha256(SnapshotService._encode(payload)).hexdigest()
        await db.commit()
        before = (row.payload, row.checksum)
        with pytest.raises(PlanningConflict, match="provenance"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        row = await db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.filename == saved))
        assert (row.payload, row.checksum) == before


@pytest.mark.parametrize("reference", ["member_profile", "task_owner"])
async def test_snapshot_refuses_reused_profile_lifetime(delivery_store, reference):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        original = TeamMemberProfile(display_name="Captured person", profile_kind="human")
        db.add(original)
        await db.commit()
        original_id = original.id
        if reference == "member_profile":
            member = await TeamService(db).create(scenario.iterations[0], TeamMemberCreate(
                name="Captured person", position="Engineer", profile_id=original_id))
            record_id = member.id
        else:
            task = await db.get(Task, scenario.tasks["planned"])
            task.owner_profile_id = original_id
            await db.commit()
            record_id = task.id
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "profile_identity")
        if reference == "task_owner":
            task.owner_profile_id = None
            await db.commit()
        assert await TeamService(db).delete_profile(original_id)
    async with factory() as db:
        replacement = TeamMemberProfile(display_name="Unrelated replacement person", profile_kind="human")
        db.add(replacement)
        await db.commit()
        replacement_id = replacement.id
        assert replacement_id > original_id
        record = await db.get(TeamMember if reference == "member_profile" else Task, record_id)
        field = "profile_id" if reference == "member_profile" else "owner_profile_id"
        before = getattr(record, field)
        assert before is None
        try:
            await SnapshotService(db).restore(scenario.iterations[0], saved)
        except PlanningConflict:
            pass
    async with factory() as db:
        record = await db.get(TeamMember if reference == "member_profile" else Task, record_id)
        after = getattr(record, field)
        assert after == before, {
            "reference": reference, "captured_profile_id": original_id,
            "replacement_profile_id": replacement_id, "before": before,
            "after": after, "snapshot": saved,
        }
        assert (await db.get(TeamMemberProfile, replacement_id)).display_name == "Unrelated replacement person"


async def test_replaced_profile_token_rejects_before_recovery_state_changes(delivery_store):
    from uuid import uuid4
    factory, scenario, _ = delivery_store
    async with factory() as db:
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "profile_lifetime_guard")
        profile = await db.get(TeamMemberProfile, scenario.profile)
        profile.profile_token = str(uuid4())
        await db.commit()
        token = profile.profile_token
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        with pytest.raises(PlanningConflict, match="person lifetime"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        assert (await db.get(TeamMemberProfile, scenario.profile)).profile_token == token
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_backlog_restore_preflights_person_lifetime_before_recovery_writes(delivery_store):
    from uuid import uuid4
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        profile = TeamMemberProfile(display_name="Backlog owner", profile_kind="human")
        db.add(profile)
        await db.flush()
        task = Task(title="Backlog deliverable", project_id=scenario.projects[0], owner_profile_id=profile.id)
        db.add(task)
        await db.commit()
        saved = await BacklogSnapshotService(db).capture(scenario.projects[0])
        profile.profile_token = str(uuid4())
        await db.commit()
        before = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
        versions = dict((await db.execute(select(Task.id, Task.version).where(Task.project_id == scenario.projects[0], Task.iteration_id.is_(None)))).all())
        with pytest.raises(PlanningConflict, match="person lifetime"):
            await BacklogSnapshotService(db).restore(scenario.projects[0], saved, versions, reason="Recover captured work")
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == before


async def test_missing_person_lifetime_map_preserves_snapshot_and_rejects_restore(delivery_store):
    import hashlib
    factory, scenario, _ = delivery_store
    async with factory() as db:
        saved = await SnapshotService(db).create_snapshot(scenario.iterations[0], "legacy_person_provenance")
        row = await db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.filename == saved))
        payload = dict(row.payload)
        payload.pop("profile_lifetimes")
        row.payload = payload
        row.checksum = hashlib.sha256(SnapshotService._encode(payload)).hexdigest()
        await db.commit()
        before = (row.payload, row.checksum)
        with pytest.raises(PlanningConflict, match="person lifetime provenance"):
            await SnapshotService(db).restore(scenario.iterations[0], saved)
    async with factory() as db:
        row = await db.scalar(select(ApplicationSnapshot).where(ApplicationSnapshot.filename == saved))
        assert (row.payload, row.checksum) == before


async def test_scoped_manager_can_restore_another_eligible_person_without_profile_access(managed_store):
    from app.authority import Authority
    from app.models.identity import PrincipalProfileLink, ProjectMembership
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    factory, scenario, _, principals = managed_store
    async with factory() as db:
        owner = TeamMemberProfile(display_name="Eligible project owner", profile_kind="human")
        db.add(owner)
        await db.flush()
        owner_id = owner.id
        db.add(PrincipalProfileLink(principal_id=principals[1], profile_id=owner_id, linked_by_principal_id=principals[0]))
        db.add(ProjectMembership(principal_id=principals[1], project_id=scenario.projects[0], role="editor"))
        manager_role = await db.scalar(select(ProjectMembership).where(ProjectMembership.principal_id == principals[0], ProjectMembership.project_id == scenario.projects[0]))
        manager_role.role = "manager"
        task = Task(title="Scoped backlog work", project_id=scenario.projects[0], owner_profile_id=owner_id)
        db.add(task)
        await db.commit()
        task_id = task.id
    async with factory() as db:
        db.info["authority"] = Authority(principals[0], "human", projects={scenario.projects[0]: "manager"})
        assert await db.scalar(select(TeamMemberProfile.id).where(TeamMemberProfile.id == owner_id)) is None
        saved = await BacklogSnapshotService(db).capture(scenario.projects[0])
        versions = dict((await db.execute(select(Task.id, Task.version).where(Task.project_id == scenario.projects[0], Task.iteration_id.is_(None)))).all())
        await BacklogSnapshotService(db).restore(scenario.projects[0], saved, versions, reason="Recover authorized backlog")
    async with factory() as db:
        assert (await db.get(Task, task_id)).owner_profile_id == owner_id
