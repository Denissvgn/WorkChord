"""An owner may accept one resolved task while the different-publisher policy stays on."""

import json

import pytest
from sqlalchemy import select, update

from app.authority import Authority, AuthorityError
from app.commands import command_transaction
from app.models.agent import TaskEvent
from app.models.identity import CommandAudit, ProjectMembership, WorkspaceMembership
from app.models.project import Project
from app.models.task import Task
from app.models.task_brief import TaskReviewRecord
from app.schemas.task_brief import BriefCriterion, OwnerAcceptanceWrite, TaskBrief
from app.services.task_brief_service import TaskBriefService
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_managed_authority import client, managed_store  # noqa: F401


REASON = "The owner verified the merged change by hand"


async def policy_scope(managed_store, role="owner"):
    """Turn the policy on for the first project and add a second resolved task there."""
    factory, scenario, _, principal_ids = managed_store
    project_id = scenario.projects[0]
    async with factory() as db:
        await db.execute(update(Project).where(Project.id == project_id).values(require_different_review_publisher=True))
        db.add(WorkspaceMembership(principal_id=principal_ids[0], role=role))
        db.add(ProjectMembership(principal_id=principal_ids[1], project_id=project_id, role="manager"))
        other = Task(title="Other resolved work", status="resolved", project_id=project_id,
                     iteration_id=scenario.iterations[0], effort_days=1, effort_hours=8)
        unpoliced = Task(title="Harbor resolved work", status="resolved", project_id=scenario.projects[1],
                         iteration_id=scenario.iterations[1], effort_days=1, effort_hours=8)
        db.add_all([other, unpoliced])
        await db.commit()
        return scenario.tasks["resolved"], other.id, unpoliced.id


def owner_client(managed_store, index=0, **headers):
    _, _, tokens, _ = managed_store
    return client(tokens[index], **{"X-CSRF-Token": f"csrf-{index}", "Origin": "https://test", **headers})


async def acceptance_body(factory, task_id, reason=REASON):
    async with factory() as db:
        task = await db.get(Task, task_id)
        return {"expected_version": task.version, "brief_revision": task.brief_revision,
                "artifact_revision": task.artifact_revision, "reason": reason}


@pytest.mark.parametrize("role", ["owner", "operator"])
async def test_owner_override_accepts_one_task_and_keeps_the_policy_for_the_rest(managed_store, role):
    factory, scenario, _, principal_ids = managed_store
    task_id, other_id, _ = await policy_scope(managed_store, role)
    body = await acceptance_body(factory, task_id)
    async with owner_client(managed_store, **{"X-Correlation-ID": "owner-override"}) as owner:
        ordinary = await owner.post(f"/api/tasks/{task_id}/review", json={**body, "verdict": "accept"})
        assert ordinary.status_code == 403, ordinary.text
        assert ordinary.json()["detail"]["code"] == "verified_publisher_review_required"

        accepted = await owner.post(f"/api/tasks/{task_id}/owner-acceptance", json=body)
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["status"] == "closed" and accepted.json()["is_accepted"] is True

        reviews = (await owner.get(f"/api/tasks/{task_id}/reviews")).json()
        assert [(item["verdict"], item["kind"], item["principal_id"], item["reason"]) for item in reviews] == [
            ("accept", "owner_override", principal_ids[0], REASON)]
        current = (await owner.get(f"/api/tasks/{task_id}/reviews/current")).json()
        assert current["review"]["kind"] == "owner_override"

        # The project policy is unchanged, so other work still needs a verified publisher.
        other_body = await acceptance_body(factory, other_id)
        for path, payload in ((f"/api/tasks/{other_id}/review", {**other_body, "verdict": "accept"}),
                              (f"/api/tasks/{other_id}/status", {"status": "closed", "expected_version": other_body["expected_version"]})):
            refused = await owner.put(path, json=payload) if path.endswith("/status") else await owner.post(path, json=payload)
            assert refused.status_code == 403, refused.text
            assert refused.json()["detail"]["code"] == "verified_publisher_review_required"

        metrics = (await owner.get("/api/tasks/delivery-metrics", params={"project_id": scenario.projects[0]})).json()
        assert metrics["acceptance_events"] == 1 and metrics["owner_override_acceptance_events"] == 1

    async with factory() as db:
        assert await db.scalar(select(Project.require_different_review_publisher).where(Project.id == scenario.projects[0])) is True
        task = await db.get(Task, task_id)
        assert (task.status, task.accepted_by_principal_id, task.accepted_version) == ("closed", principal_ids[0], task.version)
        assert (await db.get(Task, other_id)).status == "resolved"
        audits = (await db.scalars(select(CommandAudit).where(CommandAudit.correlation_id == "owner-override"))).all()
        assert any(row.action == "tasks:review" and row.details["entity_id"] == task_id for row in audits)
        for row in audits:
            assert row.principal_id == principal_ids[0] and row.reason == REASON
            assert row.details["owner_acceptance_override_task_ids"] == [task_id]
        event = await db.scalar(select(TaskEvent).where(TaskEvent.task_id == task_id, TaskEvent.event_type == "owner_acceptance_override"))
        payload = json.loads(event.payload)
        assert payload["reason"] == REASON and payload["principal_id"] == principal_ids[0]


async def test_override_refuses_non_owners_missing_reasons_and_unpoliced_projects(managed_store):
    factory, _, _, _ = managed_store
    task_id, _, unpoliced_id = await policy_scope(managed_store)
    body = await acceptance_body(factory, task_id)
    path = f"/api/tasks/{task_id}/owner-acceptance"

    async with owner_client(managed_store, index=1) as manager:
        refused = await manager.post(path, json=body)
        assert refused.status_code == 403, refused.text
        assert refused.json()["detail"]["code"] == "owner_acceptance_required"
    async with client(**{"X-Admin-API-Key": "managed-operator-fixture", "X-Review-Override": "true",
                         "X-Command-Reason": REASON}) as operator_key:
        refused = await operator_key.post(path, json=body)
        assert refused.status_code == 403, refused.text
        assert refused.json()["detail"]["code"] == "owner_acceptance_required"
    async with owner_client(managed_store) as owner:
        for payload in ({**body, "reason": "   "}, {key: value for key, value in body.items() if key != "reason"}):
            missing = await owner.post(path, json=payload)
            assert missing.status_code == 422, missing.text
        stale = await owner.post(path, json={**body, "artifact_revision": body["artifact_revision"] + 1})
        assert stale.status_code == 422, stale.text
        unpoliced = await owner.post(f"/api/tasks/{unpoliced_id}/owner-acceptance", json=await acceptance_body(factory, unpoliced_id))
        assert unpoliced.status_code == 409, unpoliced.text
        assert unpoliced.json()["detail"]["code"] == "owner_override_not_required"

    async with factory() as db:
        for refused_id in (task_id, unpoliced_id):
            assert (await db.get(Task, refused_id)).status == "resolved"
        assert await db.scalar(select(TaskReviewRecord.id).where(TaskReviewRecord.original_task_id.in_([task_id, unpoliced_id]))) is None


async def test_review_override_header_waives_only_self_review_on_an_owner_override(managed_store):
    factory, scenario, _, principal_ids = managed_store
    await policy_scope(managed_store)
    brief = TaskBrief(goal="Ship the change", acceptance_criteria=[BriefCriterion(id="works", text="The change works")])
    async with factory() as db:
        task = Task(title="Owner-executed work", status="resolved", project_id=scenario.projects[0],
                    iteration_id=scenario.iterations[0], effort_days=1, effort_hours=8,
                    brief=brief.model_dump(mode="json"), brief_revision=1, executed_by_principal_id=principal_ids[0])
        db.add(task)
        await db.commit()
        task_id = task.id
    path = f"/api/tasks/{task_id}/owner-acceptance"
    body = await acceptance_body(factory, task_id)
    async with owner_client(managed_store) as owner:
        self_review = await owner.post(path, json=body)
        assert self_review.status_code == 403, self_review.text
        assert self_review.json()["detail"]["code"] == "independent_review_required"
        # The header sets aside self-review independence, never the criterion evidence.
        unevidenced = await owner.post(path, json=body, headers={"X-Review-Override": "true"})
        assert unevidenced.status_code == 422, unevidenced.text
        assert "evidence" in unevidenced.text
    async with factory() as db:
        assert (await db.get(Task, task_id)).status == "resolved"
        await db.execute(update(Task).where(Task.id == task_id).values(progress={
            "criteria": [{"criterion_id": "works", "criterion_revision": 1, "state": "completed", "evidence": "Checked by hand"}],
            "artifacts": [], "brief_revision": 1, "artifact_revision": 0}))
        await db.commit()
    async with owner_client(managed_store) as owner:
        accepted = await owner.post(path, json=await acceptance_body(factory, task_id), headers={"X-Review-Override": "true"})
        assert accepted.status_code == 200, accepted.text
        assert accepted.json()["status"] == "closed"


async def test_trusted_local_browser_without_a_signed_in_person_cannot_override(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["resolved"]
    async with factory() as db:
        await db.execute(update(Project).where(Project.id == scenario.projects[0]).values(require_different_review_publisher=True))
        await db.commit()
    async with client() as browser:
        refused = await browser.post(f"/api/tasks/{task_id}/owner-acceptance", json=await acceptance_body(factory, task_id))
        assert refused.status_code == 403, refused.text
        assert refused.json()["detail"]["code"] == "owner_acceptance_required"
    async with factory() as db:
        assert (await db.get(Task, task_id)).status == "resolved"


@pytest.mark.parametrize("authority", [
    Authority(None, "local", local=True),
    Authority(1, "system", workspace_role="operator", review_override=True, reason=REASON),
    Authority(None, "agent", actor_id=1, actor_role="verifier", local=True, scopes=frozenset({"admin"})),
    Authority(1, "human", workspace_role="owner", read_only=True),
    Authority(1, "human", workspace_role="member", projects={1: "manager"}),
], ids=["trusted-local", "operator-key", "agent", "observer", "project-manager"])
async def test_only_a_signed_in_owner_or_operator_may_override(delivery_store, authority):  # noqa: F811
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["resolved"]
    async with factory() as db:
        await db.execute(update(Project).where(Project.id == scenario.projects[0]).values(require_different_review_publisher=True))
        await db.commit()
        body = await acceptance_body(factory, task_id)
        db.info["authority"] = authority
        with pytest.raises(AuthorityError) as refused:
            await TaskBriefService(db).owner_accept(task_id, OwnerAcceptanceWrite(**body))
        assert refused.value.code == "owner_acceptance_required"
        owner = Authority(1, "human", workspace_role="owner")
        db.info["authority"] = owner
        with pytest.raises(AuthorityError) as blank:
            await TaskBriefService(db).owner_accept(task_id, OwnerAcceptanceWrite.model_construct(**{**body, "reason": "  ", "evidence": ""}))
        assert blank.value.code == "override_reason_required"
        assert db.info["authority"] is owner


async def test_override_grant_covers_only_its_task_revision_and_acceptance(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    project_id = scenario.projects[0]
    async with factory() as db:
        await db.execute(update(Project).where(Project.id == project_id).values(require_different_review_publisher=True))
        other = Task(title="Other resolved work", status="resolved", project_id=project_id,
                     iteration_id=scenario.iterations[0], effort_days=1, effort_hours=8)
        db.add(other)
        await db.commit()
        service = TaskBriefService(db)
        async with command_transaction(db, mode="preview") as command:
            task = await TaskService(db).get_by_id(scenario.tasks["resolved"])
            granted = (task.id, task.version, task.brief_revision, task.artifact_revision)
            command.owner_acceptance_overrides.add(granted)
            await service.require_review(task, accepting=True)
            for target, accepting in ((task, False), (await TaskService(db).get_by_id(other.id), True)):
                with pytest.raises(AuthorityError) as refused:
                    await service.require_review(target, accepting=accepting)
                assert refused.value.code == "verified_publisher_review_required"
            command.owner_acceptance_overrides = {(task.id, task.version + 1, task.brief_revision, task.artifact_revision)}
            with pytest.raises(AuthorityError) as stale:
                await service.require_review(task, accepting=True)
            assert stale.value.code == "verified_publisher_review_required"


async def test_the_refusal_and_the_task_actions_name_the_owner_acceptance_next_step(managed_store):
    factory, _, _, _ = managed_store
    task_id, _, _ = await policy_scope(managed_store)
    body = await acceptance_body(factory, task_id)
    async with owner_client(managed_store) as owner:
        refused = await owner.post(f"/api/tasks/{task_id}/review", json={**body, "verdict": "accept"})
        step = refused.json()["detail"]["next_step"]
        assert (step["kind"], step["ui_action"]) == ("accept_as_owner", "accept_as_owner")
        assert step["commands"]["rest"] == "POST /api/tasks/{task_id}/owner-acceptance"

        actions = (await owner.get(f"/api/tasks/{task_id}/actions")).json()["actions"]
        blocker = next(item for item in actions if item["action"] == "accept_review")["blockers"][0]
        assert blocker["code"] == "verified_publisher_review_required"
        assert blocker["next_step"]["commands"]["rest"] == f"POST /api/tasks/{task_id}/owner-acceptance"
