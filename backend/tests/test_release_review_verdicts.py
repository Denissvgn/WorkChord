"""A release counts the current independent decisions on its linked work."""

import json
import secrets

import httpx
import pytest

from app.main import app
from app.models.agent import AgentTaskAssignment, TaskEvent
from app.models.project import Project
from app.models.release import Release
from app.models.team_member import TeamMemberProfile
from app.services.agent_service import hash_api_key
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY
from app.services.identity_service import IdentityService
from app.services.task_context_revision_service import reserve_task_context_revision
from tests.test_review_provenance_transports import databases
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_release_counts_independent_verdict(
    db_session, db_session_factory, task_factory, actor_factory, profile_factory, monkeypatch, transport,
):
    db = db_session
    reviewer_key = secrets.token_urlsafe()
    reviewer = await actor_factory(role="verifier", profile=await profile_factory(),
                                   api_key_hash=hash_api_key(reviewer_key),
                                   scopes=json.dumps(["verification:read", "verification:write"]))
    other_key = secrets.token_urlsafe()
    await actor_factory(role="verifier", api_key_hash=hash_api_key(other_key), scopes=json.dumps(["admin"]))
    worker = await actor_factory()
    principal = (await IdentityService(db).actor_context(reviewer)).principal_id
    project = Project(name="Reviewed deliveries")
    coordinator = TeamMemberProfile(display_name="Release coordinator", profile_kind="human")
    db.add_all([project, coordinator])
    await db.flush()
    accepted, rejected, manual, self_review, shared_profile = [
        await task_factory(project_id=project.id, title=title, status="resolved")
        for title in ("Reviewed change", "Incorrect result", "Closed directly", "Reviewer contribution",
                      "Change made under reviewer's profile")
    ]
    self_review.executed_by_principal_id = principal
    release = Release(name="Candidate", project_id=project.id, tasks=[accepted, rejected, manual])
    db.add(release)
    assignments = [AgentTaskAssignment(task_id=task.id, actor_id=reviewer.id, purpose="verification",
                                       state="queued", task_version=task.version)
                   for task in (accepted, rejected, self_review, shared_profile)]
    db.add_all(assignments)
    db.add(AgentTaskAssignment(task_id=shared_profile.id, actor_id=worker.id, purpose="execution",
                               state="fulfilled", task_version=shared_profile.version, routing_snapshot=json.dumps({
                                   "schema_version": "routing-decision-snapshot-v1",
                                   "authority": ROUTING_DECISION_AUTHORITY, "profile_id": reviewer.profile_id,
                               })))
    await db.commit()

    async def submit(task, assignment, decision, *, key=reviewer_key, version=None, error=None):
        payload = dict(assignment_id=assignment.id, expected_task_version=task.version if version is None else version, verdict=decision,
                       evidence={"inspection": "Compared the submitted result to the criterion"})
        if decision == "reject":
            payload.update(reason="Result differs from expected", rework_actor_id=worker.id)
        return await through(transport, db_session_factory, monkeypatch, "agent_submit_review_verdict",
                             "/api/agent/me/reviews/verdict", key, payload,
                             receipt=f"decision-{assignment.id}", error=error)

    await submit(accepted, assignments[0], "pass", key=other_key, error="Review belongs to another actor")
    await submit(accepted, assignments[0], "pass", version=accepted.version + 1, error="task_version_conflict")
    for decision in ("pass", "reject"):
        await submit(self_review, assignments[2], decision, error="independent_review_required")
        await submit(shared_profile, assignments[3], decision, error="verification_profile_not_independent")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost") as browser:
        profile = await browser.put("/api/auth/local-profile", json={"profile_id": coordinator.id})
        assert profile.is_success, profile.text
        closed = await browser.put(f"/api/tasks/{manual.id}/status",
                                   json={"status": "closed", "expected_version": manual.version})
        assert closed.is_success, closed.text
        for task, assignment, decision in ((accepted, assignments[0], "pass"), (rejected, assignments[1], "reject")):
            receipt = await submit(task, assignment, decision)
            assert await submit(task, assignment, decision) == receipt
            assert receipt["review_assignment"]["state"] == "fulfilled"
            assert receipt["review_assignment"]["actor_id"] == reviewer.id
            assert receipt["task"]["is_accepted"] == (decision == "pass")
            if decision == "reject":
                assert receipt["rework_assignment"]["actor_id"] == worker.id
            current = (await browser.get(f"/api/tasks/{task.id}/reviews/current")).json()
            row = current["review"]
            assert current["task_version"] == row["task_version"] == receipt["task"]["version"]
            assert row["reviewed_task_version"] == task.version
            assert (row["brief_revision"], row["artifact_revision"]) == (task.brief_revision, task.artifact_revision)
            assert row["principal_id"] == principal and row["kind"] == "review"
            assert row["verdict"] == ("accept" if decision == "pass" else "reject")
            assert json.loads(row["evidence"]) == {"inspection": "Compared the submitted result to the criterion"}
            timeline = (await browser.get(f"/api/tasks/{task.id}/timeline")).json()
            event, = [item for item in timeline["items"] if item["title"] == "agent.verification_verdict"]
            evidence = event["payload"]
            assert event["actor_id"] == reviewer.id and evidence["assignment_id"] == assignment.id
            assert evidence["reviewed_task_version"] == task.version and evidence["verdict"] == decision

        for task in (manual, self_review, shared_profile):
            assert (await browser.get(f"/api/tasks/{task.id}/reviews/current")).json()["review"] is None
        manual_state = (await browser.get(f"/api/tasks/{manual.id}")).json()
        assert manual_state["status"] == "closed" and manual_state["acceptance_unknown"] and not manual_state["is_accepted"]
        counts = (await browser.get(f"/api/releases/{release.id}")).json()
        assert (counts["total_tasks"], counts["implemented_tasks"], counts["accepted_tasks"],
                counts["acceptance_unknown_tasks"]) == (3, 2, 1, 1)
        for metric, task in (("accepted", accepted), ("acceptance_unknown", manual)):
            matches = (await browser.get("/api/tasks/metric-matches",
                                         params={"release_id": release.id, "metric": metric})).json()
            assert [item["id"] for item in matches["items"]] == [task.id]

        for preserved in (True, False):
            async with db_session_factory() as edit:
                await reserve_task_context_revision(edit, accepted.id, context_kind="external_link",
                                                    action="observed" if preserved else "changed",
                                                    preserve_acceptance=preserved)
                await edit.commit()
            counts = (await browser.get(f"/api/releases/{release.id}")).json()
            current = (await browser.get(f"/api/tasks/{accepted.id}/reviews/current")).json()
            assert counts["accepted_tasks"] == int(preserved)
            assert (current["review"] is not None) == preserved


async def test_older_acceptance_needs_an_assigned_verdict_receipt(db_session, task_factory, actor_factory):
    from app.models.agent import AgentIdempotencyRecord
    from app.models.identity import Principal
    from app.models.task_brief import TaskReviewRecord
    from app.services.release_service import ReleaseService
    from app.utils.time import utc_now

    db = db_session
    actor = await actor_factory(role="verifier")
    principal = Principal(kind="agent", display_name="Verifier", agent_actor_id=actor.id)
    project = Project(name="Existing work")
    db.add_all([project, principal])
    await db.flush()
    task = await task_factory(project_id=project.id, status="closed", version=2, accepted_version=2,
                              accepted_at=utc_now(), accepted_by_principal_id=principal.id)
    release = Release(name="Delivery", project_id=project.id, tasks=[task])
    assignment = AgentTaskAssignment(task_id=task.id, purpose="verification", actor_id=actor.id,
                                     state="fulfilled", task_version=task.version)
    review = TaskReviewRecord(task_id=task.id, original_task_id=task.id, task_version=task.version,
                              brief_revision=task.brief_revision, artifact_revision=task.artifact_revision,
                              principal_id=principal.id, verdict="accept", reason="Checked delivery", evidence="")
    db.add_all([release, assignment, review])
    await db.commit()
    assert (await ReleaseService(db).get_by_id(release.id)).accepted_tasks == 0
    db.add(AgentIdempotencyRecord(actor_id=actor.id, target_type="assignment", target_id=assignment.id,
                                  operation="verification.verdict", idempotency_key="held-verdict", request_hash="a" * 64))
    await db.commit()
    assert (await ReleaseService(db).get_by_id(release.id)).accepted_tasks == 0
    decision = {"assignment_id": assignment.id, "verdict": "pass", "task_version": task.version}
    for key, mismatch in (("changes-requested", {"verdict": "reject"}),
                          ("previous-version", {"task_version": task.version - 1}),
                          ("other-assignment", {"assignment_id": assignment.id + 1})):
        db.add_all([
            AgentIdempotencyRecord(actor_id=actor.id, target_type="assignment", target_id=assignment.id,
                                   operation="verification.verdict", idempotency_key=key, request_hash="a" * 64),
            TaskEvent(task_id=task.id, actor_type="agent", actor_id=actor.id,
                      event_type="agent.verification_verdict", idempotency_key=key,
                      payload=json.dumps({**decision, **mismatch})),
        ])
    await db.commit()
    assert (await ReleaseService(db).get_by_id(release.id)).accepted_tasks == 0
    db.add(TaskEvent(task_id=task.id, actor_type="agent", actor_id=actor.id,
                     event_type="agent.verification_verdict", idempotency_key="held-verdict",
                     payload=json.dumps(decision)))
    await db.commit()
    assert (await ReleaseService(db).get_by_id(release.id)).accepted_tasks == 1
    assert review.reviewed_task_version is None
