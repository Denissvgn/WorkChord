"""A task's submitted commit is reconciled with its linked pull request as GitHub shows it now."""

from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy import select

from app.authority import Authority, AuthorityError
from app.config import get_settings
from app.models.agent import AgentRun, AgentTaskAssignment, TaskEvent
from app.models.external_link import ExternalLink
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task_replacement import TaskReplacement
from app.services.external_link_service import ExternalLinkService
from app.services.github_reconciliation_service import GitHubReconciliationService
from app.services.github_status_service import GitHubStatusService
from app.services.github_webhook_service import GitHubWebhookService

REPO = "https://github.com/example/project"
SHA_A = "a" * 40
SHA_B = "b" * 40
MERGE = "c" * 40
PR_URL = f"{REPO}/pull/39"


class FakeGitHub:
    """A mutable pull request behind a mock transport; records every request."""

    def __init__(self):
        self.pull = self.payload(SHA_A, "2026-07-01T10:00:00Z")
        self.runs = [{"status": "completed", "conclusion": "success"}]
        self.requests = []

    @staticmethod
    def payload(head, updated, *, number=39, state="open", merged_at=None, draft=False):
        merged = merged_at is not None
        return {
            "number": number, "title": "Add export", "state": state, "draft": draft, "merged": merged,
            "merged_at": merged_at, "closed_at": merged_at, "updated_at": updated,
            "merge_commit_sha": MERGE, "head": {"sha": head, "ref": "feature"}, "base": {"ref": "main"},
        }

    def transport(self):
        def respond(request):
            self.requests.append(request.url.path)
            if request.url.path.endswith("/check-runs"):
                return httpx.Response(200, json={"total_count": len(self.runs), "check_runs": self.runs})
            return httpx.Response(200, json=self.pull)

        return httpx.MockTransport(respond)


@pytest.fixture
def github(monkeypatch):
    fake = FakeGitHub()

    async def from_runtime(cls, session, transport=None):
        return GitHubStatusService(session, transport=fake.transport())

    monkeypatch.setattr(GitHubStatusService, "from_runtime", classmethod(from_runtime))
    yield fake
    get_settings.cache_clear()


async def _project(db):
    project = Project(name="Kernel")
    db.add(project)
    await db.flush()
    return project


async def _delivery(db, task_factory, actor_factory, project, *, submitted=SHA_A, pr_url=PR_URL, number=39):
    """A task whose run submitted a commit for a pull request linked to it."""
    task = await task_factory(project_id=project.id)
    (await db.get(Iteration, task.iteration_id)).project_id = project.id
    link = await ExternalLinkService(db).create_task_github_link(task.id, f"{REPO}/pull/{number}", commit=False)
    actor = await actor_factory()
    db.add(AgentRun(task_id=task.id, actor_id=actor.id, status="succeeded",
                    commit_url=f"{REPO}/commit/{submitted}", pr_url=pr_url))
    await db.commit()  # a refresh releases its read transaction, as a request does
    return task, link


def _as(db, project, role="manager"):
    db.info["authority"] = Authority(None, "human", projects={project.id: role})


async def _events(db, task_id, event_type):
    return (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == task_id,
                                                     TaskEvent.event_type == event_type))).all()


async def test_a_never_observed_link_shows_its_submission_and_asks_for_catch_up(db_session, task_factory, actor_factory):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    _as(db_session, project)
    view = await GitHubReconciliationService(db_session).view(task.id)
    pull = view["pull_requests"][0]
    assert (pull["state"], pull["submitted_sha"], pull["observed_head_sha"]) == ("unobserved", SHA_A, None)
    assert pull["differences"] == ["never_observed"]
    assert (pull["next_owner"], pull["observed_at"]) == ("pm", None)


async def test_catch_up_shows_an_advanced_head_with_checks_on_that_head(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    github.pull = github.payload(SHA_B, "2026-07-01T11:00:00Z")
    _as(db_session, project)
    view = await GitHubReconciliationService(db_session).catch_up(task.id)
    pull = view["pull_requests"][0]
    assert (pull["state"], pull["submitted_sha"], pull["observed_head_sha"]) == ("open", SHA_A, SHA_B)
    assert pull["target_branch"] == "main"
    assert pull["checks"] == {"state": "success", "total": 1, "sha": SHA_B, "error": None}
    assert "head_differs_from_submission" in pull["differences"]
    assert (pull["next_owner"], pull["observation_source"]) == ("pm", "refresh")
    assert pull["observed_at"] is not None
    assert pull["merged"] is False and view["accepted"] is False


async def test_failing_and_pending_checks_name_the_worker_or_reviewer(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    _as(db_session, project)
    github.runs = [{"status": "completed", "conclusion": "failure"}, {"status": "in_progress", "conclusion": None}]
    pull = (await GitHubReconciliationService(db_session).catch_up(task.id))["pull_requests"][0]
    assert (pull["checks"]["state"], pull["next_owner"]) == ("pending", "pm")
    github.runs = [{"status": "completed", "conclusion": "timed_out"}]
    pull = (await GitHubReconciliationService(db_session).catch_up(task.id))["pull_requests"][0]
    assert (pull["checks"]["state"], pull["next_owner"]) == ("failure", "worker")


async def test_an_external_merge_is_recorded_once_and_never_accepts_the_task(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    github.pull = github.payload(SHA_A, "2026-07-01T12:00:00Z", state="closed", merged_at="2026-07-01T12:00:00Z")
    _as(db_session, project)
    service = GitHubReconciliationService(db_session)
    for _ in range(2):
        view = await service.catch_up(task.id)
    pull = view["pull_requests"][0]
    assert (pull["state"], pull["merge_commit_sha"], pull["merged"]) == ("merged", MERGE, True)
    assert pull["differences"] == ["merged_without_acceptance"]
    assert (pull["next_owner"], view["accepted"], pull["review"]) == ("reviewer", False, {"accepted": False, "state": "not_requested"})
    merged = await _events(db_session, task.id, "github_pr_merged")
    assert len(merged) == 1
    await db_session.refresh(task)
    assert task.accepted_at is None and task.status == "planned"


async def test_an_unmerged_closure_is_a_pm_decision(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    github.pull = github.payload(SHA_A, "2026-07-01T12:00:00Z", state="closed")
    github.pull["closed_at"] = "2026-07-01T12:00:00Z"
    _as(db_session, project)
    pull = (await GitHubReconciliationService(db_session).catch_up(task.id))["pull_requests"][0]
    assert (pull["state"], pull["merged"], pull["merge_commit_sha"]) == ("closed_unmerged", False, None)
    assert (pull["closed_at"], pull["next_owner"]) == ("2026-07-01T12:00:00Z", "pm")
    assert pull["differences"] == ["closed_without_merge"]
    assert len(await _events(db_session, task.id, "github_pr_closed")) == 1


def _webhook(db, secret="s"):
    settings = get_settings().model_copy(update={"github_webhook_secret": secret})
    return GitHubWebhookService(db, settings_override=settings)


def _delivery_payload(action, pull):
    return {"action": action, "pull_request": pull, "repository": {"full_name": "example/project"},
            "sender": {"login": "octo"}}


async def test_duplicate_and_out_of_order_deliveries_leave_the_newest_state(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    _as(db_session, project)
    hook = _webhook(db_session)
    newer = github.payload(SHA_B, "2026-07-01T11:00:00Z")
    older = github.payload(SHA_A, "2026-07-01T10:30:00Z")
    first = await hook.process("pull_request", "d-2", _delivery_payload("synchronize", newer))
    assert first.matched and first.ignored_reason is None
    late = await hook.process("pull_request", "d-1", _delivery_payload("synchronize", older))
    assert late.ignored_reason == "stale_delivery" and late.automation_results == []
    repeat = await hook.process("pull_request", "d-2", _delivery_payload("synchronize", newer))
    assert repeat.matched
    await db_session.refresh(link)
    assert link.metadata_json["head_sha"] == SHA_B and link.metadata_json["observation_source"] == "webhook"
    assert len(await _events(db_session, task.id, "github_pr_synchronize")) == 2  # d-2 once, d-1 once

    merged = github.payload(SHA_B, "2026-07-01T12:00:00Z", state="closed", merged_at="2026-07-01T12:00:00Z")
    await hook.process("pull_request", "d-3", _delivery_payload("closed", merged))
    reopened_late = await hook.process("pull_request", "d-4", _delivery_payload("synchronize", github.payload(SHA_B, "2026-07-01T11:30:00Z")))
    assert reopened_late.ignored_reason == "stale_delivery"
    await db_session.refresh(link)
    assert (link.status, link.metadata_json["merge_commit_sha"]) == ("merged", MERGE)


async def test_catch_up_recovers_a_merge_whose_event_was_missed_and_keeps_older_review_on_its_commit(
    db_session, task_factory, actor_factory, github
):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    reviewer = await actor_factory(role="verifier")
    db_session.add(AgentTaskAssignment(
        task_id=task.id, actor_id=reviewer.id, purpose="verification", state="fulfilled", task_version=task.version,
        routing_snapshot="{}", review_selection={"candidate": {"commit_url": f"{REPO}/commit/{SHA_A}"}}))
    actor = await actor_factory()
    db_session.add(AgentRun(task_id=task.id, actor_id=actor.id, status="succeeded",
                            commit_url=f"{REPO}/commit/{SHA_B}", pr_url=PR_URL))
    await db_session.flush()
    _as(db_session, project)
    hook = _webhook(db_session)
    await hook.process("pull_request", "d-1", _delivery_payload("opened", github.payload(SHA_A, "2026-07-01T10:00:00Z")))
    # The synchronize and merge deliveries never arrive.
    github.pull = github.payload(SHA_B, "2026-07-01T12:00:00Z", state="closed", merged_at="2026-07-01T12:00:00Z")
    view = await GitHubReconciliationService(db_session).catch_up(task.id)
    pull = view["pull_requests"][0]
    assert (pull["state"], pull["submitted_sha"], pull["observed_head_sha"]) == ("merged", SHA_B, SHA_B)
    assert "head_differs_from_submission" not in pull["differences"]
    by_sha = {row["commit_sha"]: row["reviews"] for row in pull["submissions"]}
    assert [r["state"] for r in by_sha[SHA_A]] == ["fulfilled"] and by_sha[SHA_B] == []
    assert len(await _events(db_session, task.id, "github_pr_merged")) == 1


async def test_catch_up_never_reads_a_link_outside_the_callers_teams(db_session, task_factory, actor_factory, github):
    mine, theirs = await _project(db_session), await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, theirs)
    own_task, own_link = await _delivery(db_session, task_factory, actor_factory, mine, number=40,
                                         pr_url=f"{REPO}/pull/40")
    _as(db_session, mine)
    service = GitHubReconciliationService(db_session)
    with pytest.raises(LookupError):
        await service.catch_up(task.id)
    with pytest.raises(LookupError):
        await service.view(task.id)
    assert github.requests == []
    await service.catch_up(own_task.id)
    assert github.requests and all("/pulls/40" in path or "/commits/" in path for path in github.requests)
    await db_session.refresh(link)
    assert link.status is None


async def test_a_viewer_reads_the_reconciliation_but_cannot_trigger_catch_up(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project)
    _as(db_session, project, "viewer")
    assert (await GitHubReconciliationService(db_session).view(task.id))["pull_requests"]
    with pytest.raises(AuthorityError):
        await GitHubReconciliationService(db_session).catch_up(task.id)
    assert github.requests == []


async def test_a_replaced_task_points_at_its_successor_and_its_own_pull_request(db_session, task_factory, actor_factory, github):
    project = await _project(db_session)
    original = (await _delivery(db_session, task_factory, actor_factory, project))[0].id
    replacement = (await _delivery(db_session, task_factory, actor_factory, project, submitted=SHA_B,
                                   pr_url=f"{REPO}/pull/58", number=58))[0].id
    db_session.add(TaskReplacement(project_id=project.id, original_task_id=original, replacement_task_id=replacement,
                                   reason="Unattributed work", owner_decision="Replace", base_commit_url=f"{REPO}/commit/{'0' * 40}"))
    await db_session.commit()
    github.pull = github.payload(SHA_B, "2026-07-01T12:00:00Z", number=58)
    _as(db_session, project)
    await GitHubReconciliationService(db_session).catch_up(replacement)
    view = await GitHubReconciliationService(db_session).view(original)
    assert view["replacement"] == {"role": "original", "original_task_id": original, "replacement_task_id": replacement}
    assert view["pull_requests"][0]["next_owner"] == "pm"
    assert "task_replaced" in view["pull_requests"][0]["differences"]
    assert str(replacement) in view["pull_requests"][0]["next_action"]
    successor = view["successor"]["pull_requests"][0]
    assert (successor["url"], successor["observed_head_sha"]) == (f"{REPO}/pull/58", SHA_B)
    own = await GitHubReconciliationService(db_session).view(replacement)
    assert own["replacement"]["role"] == "replacement" and own["successor"] is None
    assert own["pull_requests"][0]["submitted_sha"] == SHA_B


@pytest.mark.parametrize("old_checks, old_owner", [("failure", "worker"), ("success", "pm")])
async def test_checks_read_for_an_older_head_are_not_reported_for_the_new_head(
    db_session, task_factory, actor_factory, github, old_checks, old_owner
):
    project = await _project(db_session)
    task, link = await _delivery(db_session, task_factory, actor_factory, project, submitted=SHA_B)
    task_id, link_id = task.id, link.id
    _as(db_session, project)
    github.runs = [{"status": "completed", "conclusion": old_checks}]
    github.pull = github.payload(SHA_A, "2026-07-01T10:00:00Z")
    service = GitHubReconciliationService(db_session)
    before = (await service.catch_up(task_id))["pull_requests"][0]
    assert (before["checks"]["state"], before["checks"]["sha"]) == (old_checks, SHA_A)
    assert before["next_owner"] == "pm" and "head_differs_from_submission" in before["differences"]

    await _webhook(db_session).process("pull_request", "d-9", _delivery_payload(
        "synchronize", github.payload(SHA_B, "2026-07-01T11:00:00Z")))
    after = (await service.view(task_id))["pull_requests"][0]
    assert after["observed_head_sha"] == SHA_B
    assert (after["checks"]["state"], after["checks"]["sha"]) == ("not_observed", None)
    assert "checks_not_observed_for_head" in after["differences"]
    assert (after["next_owner"], "catch-up" in after["next_action"]) == ("pm", True)

    github.pull = github.payload(SHA_B, "2026-07-01T11:30:00Z")
    github.runs = [{"status": "completed", "conclusion": "success"}]
    restored = (await service.catch_up(task_id))["pull_requests"][0]
    assert (restored["checks"]["state"], restored["checks"]["sha"]) == ("success", SHA_B)
    assert "checks_not_observed_for_head" not in restored["differences"]
    assert restored["next_owner"] == "pm" and "reviewer" in restored["next_action"]
