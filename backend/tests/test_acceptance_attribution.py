"""Every acceptance records who accepted it, so the work reads as accepted everywhere."""

import pytest
from sqlalchemy import func, select

from app.authority import Authority
from app.models.identity import IdentitySubject, Principal, PrincipalProfileLink
from app.models.task import Task
from app.models.task_brief import TaskReviewRecord
from app.models.team_member import TeamMemberProfile
from app.schemas.task import TaskCreate
from app.schemas.task_brief import TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.services.delivery_metrics_service import DeliveryMetricsService
from app.services.identity_service import LOCAL_PROFILE_ISSUER
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_service import TaskService
from app.services.work_metrics import aggregate_metrics, task_signals
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client
from tests.test_task_domain import human_context


async def resolved_work(db, authority, project_id, owner_profile_id, title="Reviewed delivery"):
    """A resolved leaf task, executed under the given authority."""
    db.info["authority"] = authority
    task = await TaskService(db).create(None, TaskCreate(title=title, project_id=project_id, owner_profile_id=owner_profile_id))
    task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Do the work"))
    task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Ready for review"))
    await db.commit()
    db.info.pop("authority", None)
    assert task.status == "resolved"
    return task


def accept(task):
    return {"expected_version": task.version, "brief_revision": task.brief_revision, "artifact_revision": task.artifact_revision,
            "verdict": "accept", "reason": "Checked the result"}


async def test_local_person_acceptance_records_the_acceptor_and_reads_accepted(delivery_store):
    factory, scenario, _ = delivery_store
    project_id = scenario.projects[0]
    async with factory() as db:
        owner = TeamMemberProfile(display_name="Local owner", profile_kind="human")
        reviewer = TeamMemberProfile(display_name="Local reviewer", profile_kind="human")
        db.add_all([owner, reviewer])
        await db.commit()
        owner_id, reviewer_id = owner.id, reviewer.id
        executor = Authority(None, "local", local=True, profile_id=owner_id)
        first = await resolved_work(db, executor, project_id, owner_id)
        second = await resolved_work(db, executor, project_id, owner_id, title="Second reviewed delivery")
        legacy_id = scenario.tasks["closed_urgent"]
        legacy = await db.get(Task, legacy_id)
        legacy_before = (legacy.version, legacy.accepted_at, legacy.accepted_by_principal_id, legacy.accepted_version)
        assert legacy.accepted_by_principal_id is None
        links_before = await db.scalar(select(func.count()).select_from(PrincipalProfileLink))
        before = await aggregate_metrics(db, project_id=project_id)

    async with client() as browser:
        chosen = await browser.put("/api/auth/local-profile", json={"profile_id": owner_id})
        assert chosen.status_code == 200, chosen.text
        work = (await browser.get("/api/tasks/my-work")).json()
        assert first.id in {item["id"] for item in work["queues"]["awaiting_review"]}, work

        assert (await browser.put("/api/auth/local-profile", json={"profile_id": reviewer_id})).status_code == 200
        response = await browser.post(f"/api/tasks/{first.id}/review", json=accept(first))
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["status"] == "closed"
        assert body["is_accepted"] is True and body["acceptance_unknown"] is False
        read = (await browser.get(f"/api/tasks/{first.id}")).json()
        assert read["is_accepted"] is True and read["acceptance_unknown"] is False
        response = await browser.post(f"/api/tasks/{second.id}/review", json=accept(second))
        assert response.status_code == 200, response.text
        # The acceptor's own principal never turns the local session into a signed-in one.
        me = (await browser.get("/api/auth/me")).json()
        assert me["authenticated"] is False and me["principal"] is None
        assert me["profile"] == {"id": reviewer_id, "display_name": "Local reviewer", "verified": False}

        assert (await browser.put("/api/auth/local-profile", json={"profile_id": owner_id})).status_code == 200
        work = (await browser.get("/api/tasks/my-work")).json()
        assert work["state"] == "ready"
        assert first.id not in {item["id"] for queue in work["queues"].values() for item in queue}, work
        legacy_read = (await browser.get(f"/api/tasks/{legacy_id}")).json()
        assert legacy_read["is_accepted"] is False and legacy_read["acceptance_unknown"] is True

    async with factory() as db:
        task = await db.get(Task, first.id)
        acceptor = await db.get(Principal, task.accepted_by_principal_id)
        assert acceptor is not None and acceptor.kind == "human" and acceptor.display_name == "Local reviewer"
        assert task.accepted_version == task.version and task.accepted_at is not None
        assert (await db.get(Task, second.id)).accepted_by_principal_id == acceptor.id
        subject = await db.scalar(select(IdentitySubject).where(IdentitySubject.principal_id == acceptor.id))
        assert (subject.issuer, subject.subject) == (LOCAL_PROFILE_ISSUER, str(reviewer_id))
        # The profile stays free to be linked to a signed-in account later.
        assert await db.scalar(select(func.count()).select_from(PrincipalProfileLink)) == links_before
        review = await db.scalar(select(TaskReviewRecord).where(TaskReviewRecord.task_id == first.id))
        assert review.verdict == "accept" and review.principal_id == acceptor.id
        after = await aggregate_metrics(db, project_id=project_id)
        assert after["accepted_tasks"] == before["accepted_tasks"] + 2
        assert after["acceptance_unknown_tasks"] == before["acceptance_unknown_tasks"]
        report = await DeliveryMetricsService(db).report(project_id=project_id)
        assert report.accepted_leaf_tasks == 2 and report.acceptance_events == 2
        # Work closed earlier without an acceptor is neither rewritten nor counted as accepted.
        legacy = await db.get(Task, legacy_id)
        assert (legacy.version, legacy.accepted_at, legacy.accepted_by_principal_id, legacy.accepted_version) == legacy_before


async def test_signed_in_acceptance_records_the_signed_in_person(delivery_store):
    factory, scenario, _ = delivery_store
    project_id = scenario.projects[0]
    async with factory() as db:
        worker, reviewer_id = await human_context(db, project_id)
        task = await resolved_work(db, worker, project_id, worker.profile_id)
        db.info["authority"] = Authority(reviewer_id, "human", workspace_role="member", projects={project_id: "reviewer"})
        task = await TaskBriefService(db).review(task.id, TaskReviewWrite(**accept(task)))
        await db.commit()
        assert task.accepted_by_principal_id == reviewer_id
        signals = task_signals(task)
        assert signals["is_accepted"] is True and signals["acceptance_unknown"] is False
        subjects = await db.scalar(select(func.count()).select_from(IdentitySubject).where(IdentitySubject.issuer == LOCAL_PROFILE_ISSUER))
        assert subjects == 0
        report = await DeliveryMetricsService(db).report(project_id=project_id)
        assert report.accepted_leaf_tasks == 1


@pytest.mark.parametrize("override", [True, False])
async def test_operator_acceptance_records_the_operator_only_with_an_accountable_override(delivery_store, override):
    from app.authority import AuthorityError

    factory, scenario, _ = delivery_store
    project_id = scenario.projects[0]
    async with factory() as db:
        worker, _ = await human_context(db, project_id)
        task = await resolved_work(db, worker, project_id, worker.profile_id)
        operator = Principal(kind="system", display_name="Operator API")
        db.add(operator)
        await db.commit()
        db.info["authority"] = Authority(operator.id, "system", workspace_role="operator", review_override=override,
                                         reason="Owner asked the operator to accept" if override else None)
        if not override:
            task_id, request = task.id, TaskReviewWrite(**accept(task))
            with pytest.raises(AuthorityError, match="explicit operator override"):
                await TaskBriefService(db).review(task_id, request)
            await db.rollback()
            stored = (await db.execute(select(Task.status, Task.accepted_by_principal_id).where(Task.id == task_id))).one()
            assert tuple(stored) == ("resolved", None)
            return
        task = await TaskBriefService(db).review(task.id, TaskReviewWrite(**accept(task)))
        await db.commit()
        assert task.accepted_by_principal_id == operator.id
        signals = task_signals(task)
        assert signals["is_accepted"] is True and signals["acceptance_unknown"] is False
