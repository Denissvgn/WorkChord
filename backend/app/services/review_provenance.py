"""Attribute task execution and bind independent review to its submitted candidate."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
import httpx

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.agent import AgentIdempotencyRecord, AgentModelBinding, AgentModelCatalogEntry, AgentRun
from app.models.external_link import ExternalLink
from app.models.project import Project
from app.models.team_member import TeamMemberProfile
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY, canonical_routing_json_bytes
from app.utils.github_links import GitHubLinkError, parse_github_url


def _conflict(code, message, **details):
    from app.services.agent_routing_service import AgentRoutingConflictError
    raise AgentRoutingConflictError(code, message, **details)


def digest(value):
    return hashlib.sha256(canonical_routing_json_bytes(value)).hexdigest()


async def different_publisher_required(db, project_id):
    if project_id is None:
        return False
    from app.commands import current_command
    query = select(Project.require_different_review_publisher).where(Project.id == project_id)
    if (command := current_command(db)) is not None and command.mode == "apply":
        query = query.with_for_update(read=True)
    return bool(await db.scalar(query))


def historical_profile(assignment):
    """Only an exact server-owned selection can supply a legacy assignment's profile."""
    try:
        snapshot = json.loads(assignment.routing_snapshot or "{}")
    except (TypeError, ValueError):
        return None
    if not isinstance(snapshot, dict):
        return None
    if (snapshot.get("schema_version") == "routing-decision-snapshot-v1"
            and snapshot.get("authority") == ROUTING_DECISION_AUTHORITY):
        value = snapshot.get("profile_id")
        if type(value) is int and value > 0:
            return value
    return None


async def actor_provenance(db, actor, *, observed_model=None, binding_id=None):
    """Capture the authenticated actor's profile and exact operator-declared model at this instant."""
    from app.services.agent_routing_service import AgentRoutingService

    profile = await db.scalar(select(TeamMemberProfile).where(TeamMemberProfile.id == actor.profile_id)
                              .options(selectinload(TeamMemberProfile.skills)).with_for_update(read=True)
                              .execution_options(populate_existing=True))
    query = (select(AgentModelBinding, AgentModelCatalogEntry).join(AgentModelBinding.model_catalog)
             .where(AgentModelBinding.actor_id == actor.id, AgentModelBinding.enabled.is_(True),
                    AgentModelCatalogEntry.enabled.is_(True)).with_for_update(read=True)
             .execution_options(populate_existing=True))
    if binding_id is not None:
        query = query.where(AgentModelBinding.id == binding_id)
    elif observed_model is None:
        query = query.where(AgentModelBinding.is_default.is_(True))
    matches = []
    for binding, catalog in await db.execute(query):
        if observed_model is None or observed_model in {catalog.key, catalog.configured_model_alias}:
            matches.append((binding, catalog))
    receipt = {"actor_id": actor.id, "profile_id": actor.profile_id,
               "profile_revision": AgentRoutingService._profile_revision(profile),
               "binding_id": None, "binding_revision": None, "catalog_id": None, "catalog_revision": None,
               "catalog_key": None, "configured_model_alias": None, "publisher_key": None}
    if len(matches) == 1:
        binding, catalog = matches[0]
        receipt.update(binding_id=binding.id, binding_revision=binding.revision,
                       catalog_id=catalog.id, catalog_revision=catalog.revision, catalog_key=catalog.key,
                       configured_model_alias=catalog.configured_model_alias, publisher_key=catalog.publisher_key)
    return receipt


async def record_terminal_observation(db, actor, run, observed_model, *, submitting):
    """Preserve a second contributing model on an interrupted or switched execution."""
    initial = run.execution_provenance or {}
    expected = {initial.get("catalog_key"), initial.get("configured_model_alias")}
    if submitting and (not observed_model or observed_model not in expected or not initial.get("publisher_key")):
        _conflict("execution_publisher_unverifiable", "Submit with the model observed on this candidate. Report a model change as interrupted work.")
    if observed_model and observed_model in expected and initial.get("publisher_key"):
        publisher = initial["publisher_key"]
    elif observed_model:
        current = await actor_provenance(db, actor, observed_model=observed_model)
        publisher = current["publisher_key"]
    else:
        publisher = None
    run.execution_provenance = {**initial, "terminal_model": {"reported_model": observed_model, "publisher_key": publisher}}


@dataclass
class ReviewHistory:
    contributors: list[dict]
    candidate: dict | None

    def publisher_blockers(self, publisher):
        if not self.contributors or not publisher or any(not row.get("publisher_key") for row in self.contributors):
            return ["verification_publisher_unverifiable"]
        if any(row["publisher_key"] == publisher for row in self.contributors):
            return ["verification_publisher_not_independent"]
        return []


async def review_history(db, task, assignments, *, strict):
    """A failed or recovered run can have produced retained work. Include every actual attempt."""
    executions = {item.id: item for item in assignments if item.purpose == "execution"}
    query = select(AgentRun).where(AgentRun.task_id == task.id).order_by(AgentRun.id).limit(MAX_BOUNDED_LIST_ITEMS + 1)
    runs = (await db.scalars(query)).all()
    if len(runs) > MAX_BOUNDED_LIST_ITEMS:
        raise CollectionLimitExceededError("task execution provenance", MAX_BOUNDED_LIST_ITEMS)
    contributors = []
    represented = set()
    for run in runs:
        assignment = executions.get(run.assignment_id)
        if assignment is None and not (run.commit_url or run.pr_url):
            continue
        if not strict and (assignment is None or assignment.state != "fulfilled"):
            continue
        receipt = run.execution_provenance or {}
        profile_id = receipt.get("profile_id")
        if profile_id is None and assignment is not None and run.actor_id == assignment.actor_id:
            profile_id = historical_profile(assignment)
        contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                             "publisher_key": receipt.get("publisher_key"),
                             "commit_url": run.commit_url if assignment and assignment.state == "fulfilled" else None})
        terminal = receipt.get("terminal_model")
        if strict and (terminal or receipt.get("different_publisher_required") and run.status in {"failed", "canceled"}):
            last_publisher = (terminal or {}).get("publisher_key")
            if last_publisher != receipt.get("publisher_key"):
                contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                                     "publisher_key": last_publisher})
        represented.add(run.assignment_id)
    for assignment in executions.values():
        if assignment.state == "fulfilled" and assignment.id not in represented:
            contributors.append({"run_id": None, "actor_id": assignment.actor_id,
                                 "profile_id": historical_profile(assignment), "publisher_key": None})
    if not strict:
        return ReviewHistory(contributors, None)

    submitted = [run for run in runs if run.status == "succeeded" and run.assignment_id in executions
                 and executions[run.assignment_id].state == "fulfilled" and run.ended_at is not None]
    if not submitted:
        return ReviewHistory(contributors, None)
    latest = max(submitted, key=lambda run: (run.ended_at, run.id))
    receipts = (await db.scalars(select(AgentIdempotencyRecord).where(
        AgentIdempotencyRecord.actor_id == latest.actor_id, AgentIdempotencyRecord.operation == "work.submit",
        AgentIdempotencyRecord.target_type == "assignment", AgentIdempotencyRecord.target_id == latest.assignment_id,
    ).limit(2))).all()
    if len(receipts) != 1:
        return ReviewHistory(contributors, None)
    try:
        response = json.loads(receipts[0].response_payload)["response"]
        if (response["run"]["id"] != latest.id or response["task"]["id"] != task.id
                or response["assignment"]["id"] != latest.assignment_id
                or response["run"]["actor_id"] != latest.actor_id or response["run"]["status"] != "succeeded"
                or response["task"].get("artifact_revision", 0) != task.artifact_revision
                or response["task"].get("brief_revision", 0) != task.brief_revision):
            return ReviewHistory(contributors, None)
        submitted_run = response["run"]
        pr = parse_github_url(submitted_run["pr_url"]) if submitted_run.get("pr_url") else None
        commit = parse_github_url(submitted_run["commit_url"]) if submitted_run.get("commit_url") else None
        submitted_links = set(submitted_run.get("artifact_links") or [])
        submitted_links.update((submitted_run.get("execution_provenance") or {}).get("submitted_commit_urls", ()))
        artifact_commits, artifact_prs = set(), set()
        for url in submitted_links:
            try:
                link = parse_github_url(url)
            except GitHubLinkError:
                continue
            if link.github_type == "commit":
                artifact_commits.add(link.url)
            elif link.github_type == "pull_request":
                artifact_prs.add(link.url)
        if commit is None and len(artifact_commits) == 1:
            commit = parse_github_url(artifact_commits.pop())
        if pr is None:
            if not artifact_prs:
                linked_urls = await db.scalars(select(ExternalLink.url).where(
                    ExternalLink.entity_type == "task", ExternalLink.entity_id == task.id, ExternalLink.provider == "github"))
                for url in linked_urls:
                    try:
                        link = parse_github_url(url)
                    except GitHubLinkError:
                        continue
                    if link.github_type == "pull_request":
                        artifact_prs.add(link.url)
            if len(artifact_prs) > 1:
                return ReviewHistory(contributors, None)
            if artifact_prs:
                pr = parse_github_url(artifact_prs.pop())
        if submitted_links and commit is None:
            return ReviewHistory(contributors, None)
        if ((commit and commit.github_type != "commit") or
                (pr and (pr.github_type != "pull_request" or not commit
                         or pr.repo_full_name.casefold() != commit.repo_full_name.casefold()))):
            return ReviewHistory(contributors, None)
    except (KeyError, TypeError, ValueError, GitHubLinkError):
        return ReviewHistory(contributors, None)
    basis = {"task_id": task.id, "task_version": task.version, "brief_revision": task.brief_revision,
             "artifact_revision": task.artifact_revision, "run_id": latest.id, "submission_sha256": receipts[0].request_hash,
             "commit_url": commit.url if commit else None, "pr_url": pr.url if pr else None}
    return ReviewHistory(contributors, {**basis, "digest": digest(basis)})


async def select_reviewer(db, task, assignments, reviewer, *, binding_id=None, reviewer_profile_id=None):
    if not await different_publisher_required(db, task.project_id):
        return None
    history = await review_history(db, task, assignments, strict=True)
    receipt = await actor_provenance(db, reviewer, binding_id=binding_id)
    if not history.candidate:
        _conflict("verification_candidate_unverifiable", "An exact submitted candidate is required.")
    if not receipt["profile_id"] or any(row["profile_id"] is None for row in history.contributors):
        _conflict("verification_independence_unverifiable", "An implementation or verifier profile lacks historical evidence.")
    if reviewer_profile_id is not None and receipt["profile_id"] != reviewer_profile_id:
        _conflict("reviewer_profile_mismatch", "The selected reviewer must hold the requested profile.")
    if any(row["actor_id"] == reviewer.id for row in history.contributors):
        _conflict("verification_actor_not_independent", "An implementation actor cannot verify this candidate.")
    if any(row["profile_id"] == receipt["profile_id"] for row in history.contributors):
        _conflict("verification_profile_not_independent", "The review profile contributed to this task.")
    blockers = history.publisher_blockers(receipt["publisher_key"])
    if blockers:
        _conflict(blockers[0], "Review requires a known publisher distinct from every contributing publisher.")
    return {"reviewer": receipt, "candidate": history.candidate, "contributors": history.contributors}


async def observe_review_candidate(db, assignment_id, actor_id):
    """Resolve remote PR evidence before taking the task, actor and assignment locks."""
    from app.models.agent import AgentTaskAssignment
    from app.services.github_status_service import GitHubStatusService

    selection = await db.scalar(select(AgentTaskAssignment.review_selection).where(
        AgentTaskAssignment.id == assignment_id, AgentTaskAssignment.actor_id == actor_id,
        AgentTaskAssignment.purpose == "verification", AgentTaskAssignment.state.in_(("queued", "accepted"))))
    if not selection or not selection["candidate"]["commit_url"]:
        return None
    candidate = selection["candidate"]
    commit = parse_github_url(candidate["commit_url"])
    try:
        github = await GitHubStatusService.from_runtime(db)
        attributed = {}
        for row in selection["contributors"]:
            if row.get("commit_url"):
                source = parse_github_url(row["commit_url"])
                if source.github_type == "commit" and source.repo_full_name.casefold() == commit.repo_full_name.casefold():
                    attributed.setdefault(source.sha, set()).add(row["actor_id"])
        if candidate["pr_url"]:
            blocker = await github.verify_review_head(parse_github_url(candidate["pr_url"]), commit.sha, attributed)
        else:
            blocker = await github.verify_review_commit(commit)
    except (httpx.HTTPError, ValueError, KeyError, TypeError, AttributeError):
        blocker = "verification_candidate_unverifiable"
    return candidate["digest"], blocker


async def verify_verdict(db, task, assignments, assignment, actor, data, observed_candidate):
    from app.commands import current_command

    if assignment.actor_id != actor.id or not assignment.review_selection:
        _conflict("verification_independence_unverifiable", "The assigned reviewer must submit its own observed model.")
    stored = assignment.review_selection
    current = await select_reviewer(db, task, assignments, actor, binding_id=stored["reviewer"]["binding_id"],
                                    reviewer_profile_id=assignment.reviewer_profile_id)
    if current != stored or data.reviewed_candidate_digest != current["candidate"]["digest"]:
        _conflict("verification_candidate_stale", "Refresh the review assignment and review its exact candidate.")
    if data.observed_model not in {current["reviewer"]["catalog_key"], current["reviewer"]["configured_model_alias"]}:
        _conflict("verification_publisher_unverifiable", "The authenticated reviewer's observed model must match its selected binding.")
    if current["candidate"]["commit_url"]:
        if not observed_candidate or observed_candidate[0] != current["candidate"]["digest"]:
            _conflict("verification_candidate_stale", "The selected PR candidate changed during review.")
        if observed_candidate[1] is not None:
            _conflict(observed_candidate[1], "The PR head and all contributing authors must be verifiable for this review.")
    command = current_command(db)
    assert command is not None
    command.verified_publishers.add((task.id, task.version, task.brief_revision, task.artifact_revision))
