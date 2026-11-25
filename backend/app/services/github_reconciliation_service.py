"""Reconcile what a task submitted with what GitHub currently shows for its pull requests.

The read model compares the commit each run submitted with the observed head,
checks, merge or unmerged closure, and the review state, and names who acts
next. Catch-up refreshes the task's own pull request links from GitHub for
events a deployment never received. Observing a merge never accepts or closes a
task: acceptance stays with the independent reviewer's verdict.
"""

from typing import Any, Optional

from sqlalchemy import select

from app.authority import require_project
from app.models.agent import AgentRun, AgentTaskAssignment
from app.models.external_link import ExternalLink, ExternalLinkEntityType
from app.models.task import Task
from app.query_limits import MAX_BOUNDED_LIST_ITEMS
from app.services.github_status_service import GitHubStatusService, parse_github_time
from app.services.task_replacement_service import relation_for
from app.utils.github_links import GitHubLinkError, parse_github_url

MAX_CATCH_UP_LINKS = 25


def _sha(url: Optional[str]) -> Optional[str]:
    try:
        parsed = parse_github_url(url) if url else None
    except GitHubLinkError:
        return None
    return parsed.sha if parsed is not None and parsed.github_type == "commit" else None


def _pull_key(url: Optional[str]) -> Optional[str]:
    try:
        parsed = parse_github_url(url) if url else None
    except GitHubLinkError:
        return None
    return parsed.external_key.casefold() if parsed is not None and parsed.github_type == "pull_request" else None


def pull_state(link: ExternalLink) -> str:
    """open, draft, merged, closed_unmerged, or unobserved."""
    if link.status is None:
        return "unobserved"
    return {"closed": "closed_unmerged"}.get(link.status, link.status)


async def observed_head_keeps_acceptance(db, link: ExternalLink, head_sha: Optional[str]) -> bool:
    """Whether recording an observed pull request head may carry the task's acceptance.

    Acceptance covers the submitted commit. A head that differs from it, as the
    reconciliation's ``head_differs_from_submission`` reports, is code no reviewer
    accepted. Without a submission for the link, a head that moved from the one
    recorded before is treated the same way. An observation that names no head
    cannot show which code it covers, so it does not keep acceptance.
    """
    if not head_sha:
        return False
    service = GitHubReconciliationService(db)
    links = await service._pull_links(link.entity_id)
    runs = (await db.scalars(select(AgentRun).where(AgentRun.task_id == link.entity_id).order_by(AgentRun.id)
                             .limit(MAX_BOUNDED_LIST_ITEMS))).all()
    submissions = service._submissions(link, runs, [], len(links) == 1)
    if submissions:
        return submissions[-1]["commit_sha"] == head_sha
    recorded = (link.metadata_json or {}).get("head_sha")
    return not recorded or recorded == head_sha


class GitHubReconciliationService:
    """Read and catch up the GitHub reconciliation of one task."""

    def __init__(self, db):
        self.db = db

    async def _task(self, task_id: int, action: str) -> Task:
        # The scoped read hides a task outside the caller's teams; refuse before any provider call.
        task = await self.db.scalar(select(Task).where(Task.id == task_id))
        if task is None:
            raise LookupError("Task not found or inaccessible")
        require_project(self.db, task.project_id, action)
        return task

    async def _pull_links(self, task_id: int) -> list[ExternalLink]:
        links = (await self.db.scalars(select(ExternalLink).where(
            ExternalLink.entity_type == ExternalLinkEntityType.TASK.value, ExternalLink.entity_id == task_id,
            ExternalLink.provider == "github").order_by(ExternalLink.id).limit(MAX_BOUNDED_LIST_ITEMS))).all()
        return [link for link in links if (link.metadata_json or {}).get("github_type") == "pull_request"]

    async def catch_up(self, task_id: int) -> dict[str, Any]:
        """Refresh this task's pull request links from GitHub, then return the reconciliation."""
        task = await self._task(task_id, "edit")
        ids = [link.id for link in (await self._pull_links(task.id))[:MAX_CATCH_UP_LINKS]]
        github = await GitHubStatusService.from_runtime(self.db)
        # Read every link from GitHub first, holding no lock and no reservation,
        # then record them all in one transaction under one task revision.
        fetched = [item for item in [await github.fetch_pull_request(link_id) for link_id in ids] if item is not None]
        if fetched:
            await github.record_fetched_pull_requests(task_id, fetched)
        return await self.view(task_id)

    async def view(self, task_id: int) -> dict[str, Any]:
        task = await self._task(task_id, "read")
        accepted = task.accepted_at is not None and task.accepted_version == task.version
        runs = (await self.db.scalars(select(AgentRun).where(AgentRun.task_id == task.id).order_by(AgentRun.id)
                                      .limit(MAX_BOUNDED_LIST_ITEMS))).all()
        reviews = (await self.db.scalars(select(AgentTaskAssignment).where(
            AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.purpose == "verification")
            .order_by(AgentTaskAssignment.id).limit(MAX_BOUNDED_LIST_ITEMS))).all()
        links = await self._pull_links(task.id)
        relation = await relation_for(self.db, task.id)
        replaced = relation is not None and relation.original_task_id == task.id
        successor = None
        if replaced:
            replacement = await self.db.get(Task, relation.replacement_task_id)
            if replacement is not None:
                successor = {"task_id": replacement.id, "status": replacement.status,
                             "pull_requests": [self._pull(replacement, link, [], [], False, False, None)
                                               for link in await self._pull_links(replacement.id)]}
        pulls = [self._pull(task, link, runs, reviews, accepted, replaced, relation, len(links)) for link in links]
        return {"task_id": task.id, "task_status": task.status, "accepted": accepted,
                "replacement": None if relation is None else {
                    "role": "original" if replaced else "replacement",
                    "original_task_id": relation.original_task_id,
                    "replacement_task_id": relation.replacement_task_id},
                "successor": successor, "pull_requests": pulls}

    def _submissions(self, link, runs, reviews, only_link):
        key = (link.external_key or "").casefold()
        rows = []
        for run in runs:
            sha = _sha(run.commit_url)
            if sha is None:
                continue
            pull = _pull_key(run.pr_url)
            if pull != key and not (pull is None and only_link):
                continue
            rows.append({
                "run_id": run.id, "commit_sha": sha, "commit_url": run.commit_url, "pr_url": run.pr_url,
                "submitted_at": run.ended_at or run.started_at,
                "reviews": [{"assignment_id": review.id, "actor_id": review.actor_id, "state": review.state}
                            for review in reviews
                            if _sha(((review.review_selection or {}).get("candidate") or {}).get("commit_url")) == sha],
            })
        return rows

    def _pull(self, task, link, runs, reviews, accepted, replaced, relation, link_count=1):
        meta = link.metadata_json or {}
        state = pull_state(link)
        submissions = self._submissions(link, runs, reviews, link_count == 1)
        submitted = submissions[-1] if submissions else None
        head = meta.get("head_sha")
        head_differs = bool(submitted and head and head != submitted["commit_sha"])
        checked = bool(head) and meta.get("checks_sha") == head
        checks_state = meta.get("checks_state") if checked else None
        differences = []
        if state == "unobserved":
            differences.append("never_observed")
        if meta.get("status_refresh_error"):
            differences.append("observation_failed")
        if head_differs:
            differences.append("head_differs_from_submission")
        if head and not checked:
            differences.append("checks_not_observed_for_head")
        if state == "merged" and not accepted:
            differences.append("merged_without_acceptance")
        if state == "closed_unmerged":
            differences.append("closed_without_merge")
        if replaced:
            differences.append("task_replaced")
        owner, action = self._next(state, meta, checks_state, submitted, head_differs, accepted, replaced, relation, reviews)
        observed = meta.get("observed_at") or meta.get("status_refreshed_at") or meta.get("webhook_received_at")
        return {
            "link_id": link.id, "url": link.url, "title": link.title, "state": state,
            "submitted_sha": submitted["commit_sha"] if submitted else None,
            "submissions": submissions,
            "observed_head_sha": head,
            "target_branch": meta.get("base_ref"),
            "checks": {"state": checks_state or ("not_observed" if head else None),
                       "total": meta.get("checks_total") if checked else None,
                       "sha": meta.get("checks_sha") if checked else None,
                       "error": meta.get("checks_error") if checked else None},
            "merged": state == "merged", "merge_commit_sha": meta.get("merge_commit_sha"),
            "merged_at": meta.get("merged_at"), "closed_at": meta.get("closed_at"),
            "observed_at": parse_github_time(observed), "observation_source": meta.get("observation_source"),
            "observation_error": meta.get("status_refresh_error"),
            "review": {"accepted": accepted, "state": "accepted" if accepted else (reviews[-1].state if reviews else "not_requested")},
            "differences": differences, "next_owner": owner, "next_action": action,
        }

    @staticmethod
    def _next(state, meta, checks_state, submitted, head_differs, accepted, replaced, relation, reviews):
        if replaced:
            return "pm", f"Continue on replacement task {relation.replacement_task_id}; this task is withdrawn."
        if accepted:
            return "none", "Accepted by the independent reviewer; nothing further."
        if state == "unobserved":
            return "pm", "Run catch-up to read the pull request from GitHub."
        if meta.get("status_refresh_error"):
            return "pm", "GitHub could not be read; retry catch-up or check the GitHub token."
        if state == "closed_unmerged":
            return "pm", "Closed without merging; reopen the pull request or replace the task."
        if head_differs:
            return "pm", "The head differs from the submitted commit; have the worker submit the current head, then request review."
        if state == "draft":
            return "worker", "Mark the pull request ready for review."
        if state != "merged" and meta.get("head_sha") and checks_state is None:
            return "pm", "Checks are not observed for the current head; run catch-up."
        if state != "merged" and checks_state == "failure":
            return "worker", "Fix the failing checks on the current head."
        pending = bool(reviews) and reviews[-1].state in {"queued", "accepted"}
        if state == "merged":
            return "reviewer", "Merged outside WorkChord; the independent verdict on the submitted commit is still required."
        if pending:
            return "reviewer", "Review the submitted commit; the head matches it."
        return "pm", "Assign an independent reviewer for the submitted commit."
