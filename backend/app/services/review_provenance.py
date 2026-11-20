"""Attribute task execution and bind independent review to its submitted candidate."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
import httpx

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.agent import AgentIdempotencyRecord, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentRunEvent, TaskEvent
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
    query = select(Project.require_different_review_publisher).where(Project.id == project_id,
                                                                    Project.require_different_review_publisher.is_(True))
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


async def actor_provenance(db, actor, *, observed_model=None, binding_id=None, lock=False):
    """Capture the authenticated actor's profile and exact operator-declared model at this instant."""
    from app.services.agent_routing_service import AgentRoutingService

    profile_query = select(TeamMemberProfile).where(TeamMemberProfile.id == actor.profile_id).options(
        selectinload(TeamMemberProfile.skills)).execution_options(populate_existing=True)
    query = (select(AgentModelBinding, AgentModelCatalogEntry).join(AgentModelBinding.model_catalog)
             .where(AgentModelBinding.actor_id == actor.id, AgentModelBinding.enabled.is_(True),
                    AgentModelCatalogEntry.enabled.is_(True))
             .execution_options(populate_existing=True))
    if lock:
        profile_query = profile_query.with_for_update(read=True)
        query = query.with_for_update(read=True)
    profile = await db.scalar(profile_query) if actor.profile_id is not None else None
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


_OUTPUT_KEYS = {"artifact", "artifacts", "artifact_links", "commit", "commit_url", "commit_urls", "commit_sha",
                "retained_commits", "head_sha", "pr_url", "pull_request"}


def _has_output(value):
    if isinstance(value, dict):
        return any((key in _OUTPUT_KEYS and bool(child)) or _has_output(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_has_output(child) for child in value)
    return False


async def no_output_corroborated(db, run, reported_evidence=None):
    """A sealed worker statement cannot discard artifacts already recorded on the same run."""
    if (run.commit_url or run.pr_url or json.loads(run.artifact_links or "[]") or _has_output(reported_evidence)
            or (run.execution_provenance or {}).get("submitted_commit_urls")):
        return False
    run_events = select(AgentRunEvent.payload).where(AgentRunEvent.run_id == run.id)
    task_events = select(TaskEvent.payload).where(TaskEvent.task_id == run.task_id, TaskEvent.actor_id == run.actor_id,
        TaskEvent.event_type.in_(("agent.progress", "agent.checkpoint", "agent.blocker")), TaskEvent.created_at >= run.started_at)
    if run.ended_at is not None:
        task_events = task_events.where(TaskEvent.created_at <= run.ended_at)
    for query in (run_events, task_events):
        rows = (await db.scalars(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
        if len(rows) > MAX_BOUNDED_LIST_ITEMS:
            return False
        for payload in rows:
            try:
                if _has_output(json.loads(payload or "{}")):
                    return False
            except (TypeError, ValueError):
                return False
    return True


async def record_terminal_observation(db, actor, run, observed_model, *, submitting, output_state=None,
                                      commit_urls=(), evidence=None, checkpoint=False):
    """Preserve a second contributing model on an interrupted or switched execution."""
    initial = run.execution_provenance or {}
    expected = {initial.get("catalog_key"), initial.get("configured_model_alias")}
    if not observed_model:
        _conflict("execution_publisher_unverifiable", "Provide the observed model on this terminal command.",
                  missing=[{"run_id": run.id, "facts": ["observed_model"]}])
    if output_state == "no_output" and (commit_urls or not await no_output_corroborated(db, run, evidence)):
        _conflict("execution_output_conflict", "Recorded artifacts contradict a no-output declaration.")
    current = await actor_provenance(db, actor, observed_model=observed_model,
                                    binding_id=initial.get("binding_id") if submitting else None, lock=True)
    publisher = current["publisher_key"]
    identity_fields = ("profile_id", "binding_id", "binding_revision", "catalog_id", "catalog_revision", "publisher_key")
    if submitting and (observed_model not in expected or not publisher
                       or any(current[key] != initial.get(key) for key in identity_fields)):
        _conflict("execution_publisher_unverifiable", "The model binding changed during execution. Report the interruption and retained work.")
    field = "interruption_checkpoint" if checkpoint else "terminal_model"
    observation = {"reported_model": observed_model, "publisher_key": publisher,
                   "source": "sealed_worker_checkpoint" if checkpoint else "authenticated_terminal",
                   "output_state": output_state or ("retained" if submitting or commit_urls else "unknown"),
                   "commit_urls": list(commit_urls), "run_id": run.id, "actor_id": actor.id,
                   "assignment_id": run.assignment_id, "claim_generation": run.claim_generation}
    sealed = initial.get("interruption_checkpoint")
    if sealed and (submitting or any(sealed.get(key) != observation[key] for key in
                                    ("reported_model", "output_state", "commit_urls", "publisher_key"))):
        _conflict("execution_output_conflict", "The worker already sealed its final output for this fence.")
    run.execution_provenance = {**initial, field: observation}


async def recover_terminal_observation(db, run):
    """Resolve only the server-bound receipt for a worker's final sealed checkpoint on this exact fence."""
    stored = run.execution_provenance or {}
    seal = stored.get("interruption_checkpoint")
    query = select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.actor_id == run.actor_id,
        AgentIdempotencyRecord.operation == "work.renew", AgentIdempotencyRecord.target_type == "assignment",
        AgentIdempotencyRecord.target_id == run.assignment_id, AgentIdempotencyRecord.created_at >= run.started_at)
    if run.ended_at is not None:
        query = query.where(AgentIdempotencyRecord.created_at <= run.ended_at)
    if seal is not None:
        if not isinstance(seal, dict) or not isinstance(seal.get("renew_key"), str):
            return None, {}
        query = query.where(AgentIdempotencyRecord.idempotency_key == seal["renew_key"])
    receipts = (await db.scalars(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
    if len(receipts) > MAX_BOUNDED_LIST_ITEMS:
        return None, {}
    matched = []
    identity = (run.id, run.actor_id, run.assignment_id, run.claim_generation)
    for receipt in receipts:
        try:
            packet = json.loads(receipt.response_payload)["response_without_claim_id"]
            captured = (packet["run"].get("execution_provenance") or {}).get("interruption_checkpoint")
            if not captured or captured.get("renew_key") != receipt.idempotency_key:
                continue
            if ((seal is not None and captured != seal) or captured.get("source") != "sealed_worker_checkpoint"
                    or tuple(captured.get(k) for k in ("run_id", "actor_id", "assignment_id", "claim_generation")) != identity
                    or tuple(packet["run"].get(k) for k in ("id", "actor_id", "assignment_id", "claim_generation")) != identity
                    or packet["task"]["id"] != run.task_id or packet["assignment"]["purpose"] != "execution"
                    or packet["assignment"]["id"] != run.assignment_id or packet["assignment"]["actor_id"] != run.actor_id
                    or captured.get("output_state") not in {"no_output", "retained"}):
                return None, {}
            matched.append((captured, receipt.id))
        except (AttributeError, KeyError, TypeError, ValueError):
            return None, {}
    if len(matched) != 1:
        return None, {}
    captured, receipt_id = matched[0]
    if captured["output_state"] == "no_output" and not await no_output_corroborated(db, run):
        return None, {}
    return captured, {"renew": receipt_id}


async def mark_server_interruption(db, run):
    provenance = run.execution_provenance or {}
    terminal, sources = await recover_terminal_observation(db, run)
    run.execution_provenance = {**provenance, "terminal_model": terminal or {
        "source": "server_interruption", "reported_model": None, "publisher_key": None, "output_state": "unknown"},
        "interruption_source_receipts": sources}


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
        verification_run = any(item.id == run.assignment_id and item.actor_id == run.actor_id and
                               item.purpose == "verification" for item in assignments)
        if verification_run:
            continue
        if strict and assignment is None:
            contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": None,
                                 "publisher_key": None, "missing": ["execution_assignment", "profile_id", "publisher_key"]})
            continue
        if not strict and (assignment is None or assignment.state != "fulfilled"):
            continue
        receipt = run.execution_provenance or {}
        terminal = receipt.get("terminal_model") or {}
        interrupted = run.status in {"failed", "canceled", "cancelled"}
        if (strict and interrupted and terminal.get("source") in {"authenticated_terminal", "sealed_worker_checkpoint"}
                and terminal.get("output_state") == "no_output" and await no_output_corroborated(db, run)):
            represented.add(run.assignment_id)
            continue
        profile_id = receipt.get("profile_id")
        if profile_id is None and assignment is not None and run.actor_id == assignment.actor_id:
            profile_id = historical_profile(assignment)
        commits = set(receipt.get("submitted_commit_urls") or ())
        commits.update(terminal.get("commit_urls") or ())
        if run.commit_url:
            commits.add(run.commit_url)
        contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                             "publisher_key": receipt.get("publisher_key"),
                             "commit_urls": sorted(commits)})
        if strict and (terminal or interrupted):
            last_publisher = (terminal or {}).get("publisher_key")
            if last_publisher != receipt.get("publisher_key") or not last_publisher:
                contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                                     "publisher_key": last_publisher,
                                     "missing": [] if last_publisher else ["terminal_model"]})
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
        base_url = (submitted_run.get("execution_provenance") or {}).get("submitted_base_commit_url")
        base = parse_github_url(base_url) if base_url else None
        submitted_links = set(submitted_run.get("artifact_links") or [])
        submitted_links.update((submitted_run.get("execution_provenance") or {}).get("submitted_commit_urls", ()))
        artifact_commits, artifact_prs = set(), set()
        repository_artifact = False
        for url in submitted_links:
            try:
                link = parse_github_url(url)
            except GitHubLinkError:
                continue
            repository_artifact |= link.github_type in {"commit", "pull_request", "branch", "tag"}
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
        if repository_artifact and commit is None:
            return ReviewHistory(contributors, None)
        if ((commit and commit.github_type != "commit") or (pr and (pr.github_type != "pull_request" or not commit))
                or (base and (not commit or base.github_type != "commit" or base.repo_full_name.casefold() != commit.repo_full_name.casefold()))
                or (commit and not pr and not base)):
            return ReviewHistory(contributors, None)
    except (KeyError, TypeError, ValueError, GitHubLinkError):
        return ReviewHistory(contributors, None)
    basis = {"task_id": task.id, "task_version": task.version, "brief_revision": task.brief_revision,
             "artifact_revision": task.artifact_revision, "run_id": latest.id, "submission_sha256": receipts[0].request_hash,
             "commit_url": commit.url if commit else None, "pr_url": pr.url if pr else None,
             "base_commit_url": base.url if base else None}
    return ReviewHistory(contributors, {**basis, "digest": digest(basis)})


async def select_reviewer(db, task, assignments, reviewer, *, binding_id=None, reviewer_profile_id=None):
    if not await different_publisher_required(db, task.project_id):
        return None
    history = await review_history(db, task, assignments, strict=True)
    receipt = await actor_provenance(db, reviewer, binding_id=binding_id, lock=True)
    if not receipt["profile_id"] or any(row["profile_id"] is None for row in history.contributors):
        _conflict("verification_independence_unverifiable", "An implementation or verifier profile lacks historical evidence.",
                 missing=[{"run_id": r["run_id"], "facts": r.get("missing", ["profile_id"])} for r in history.contributors if r["profile_id"] is None])
    if reviewer_profile_id is not None and receipt["profile_id"] != reviewer_profile_id:
        _conflict("reviewer_profile_mismatch", "The selected reviewer must hold the requested profile.")
    if any(row["actor_id"] == reviewer.id for row in history.contributors):
        _conflict("verification_actor_not_independent", "An implementation actor cannot verify this candidate.")
    if any(row["profile_id"] == receipt["profile_id"] for row in history.contributors):
        _conflict("verification_profile_not_independent", "The review profile contributed to this task.")
    blockers = history.publisher_blockers(receipt["publisher_key"])
    if blockers:
        _conflict(blockers[0], "Review requires a known publisher distinct from every contributing publisher.",
                 missing=[{"run_id": r["run_id"], "facts": r.get("missing", ["publisher_key"])}
                          for r in history.contributors if not r.get("publisher_key")])
    return {"reviewer": receipt, "candidate": history.candidate, "contributors": history.contributors,
            "acceptance_blockers": [] if history.candidate else ["verification_candidate_unverifiable"]}


async def observe_review_candidate(db, assignment_id, actor_id):
    """Resolve remote PR evidence before taking the task, actor and assignment locks."""
    from app.models.agent import AgentTaskAssignment
    from app.services.github_status_service import GitHubStatusService

    selection = await db.scalar(select(AgentTaskAssignment.review_selection).where(
        AgentTaskAssignment.id == assignment_id, AgentTaskAssignment.actor_id == actor_id,
        AgentTaskAssignment.purpose == "verification", AgentTaskAssignment.state.in_(("queued", "accepted"))))
    if not selection or not selection.get("candidate") or not selection["candidate"]["commit_url"]:
        return None
    candidate = selection["candidate"]
    commit = parse_github_url(candidate["commit_url"])
    try:
        github = await GitHubStatusService.from_runtime(db)
        attributed = {}
        for row in selection["contributors"]:
            urls = row.get("commit_urls", ())
            for url in urls:
                source = parse_github_url(url)
                if source.github_type == "commit" and source.repo_full_name.casefold() == commit.repo_full_name.casefold():
                    attributed.setdefault(source.sha, set()).add(row["actor_id"])
        if candidate["pr_url"]:
            blocker = await github.verify_review_head(parse_github_url(candidate["pr_url"]), commit.sha, attributed,
                                                      expected_repository=commit.repo_full_name)
        else:
            blocker = await github.verify_review_range(parse_github_url(candidate["base_commit_url"]), commit, attributed)
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
    if current["reviewer"] != stored["reviewer"]:
        _conflict("verification_publisher_unverifiable", "Refresh the assignment after a change to the reviewer's binding or profile.")
    if data.verdict == "pass" and not current["candidate"]:
        _conflict("verification_candidate_unverifiable", "An exact submitted candidate is required for acceptance.")
    if data.verdict == "pass" and (current != stored or data.reviewed_candidate_digest != current["candidate"]["digest"]):
        _conflict("verification_candidate_stale", "Refresh the review assignment and review its exact candidate.")
    if data.observed_model not in {current["reviewer"]["catalog_key"], current["reviewer"]["configured_model_alias"]}:
        _conflict("verification_publisher_unverifiable", "The authenticated reviewer's observed model must match its selected binding.")
    if data.verdict == "pass" and current["candidate"]["commit_url"]:
        if not observed_candidate or observed_candidate[0] != current["candidate"]["digest"]:
            _conflict("verification_candidate_stale", "The selected PR candidate changed during review.")
        if observed_candidate[1] is not None:
            _conflict(observed_candidate[1], "The PR head and all contributing authors must be verifiable for this review.")
    command = current_command(db)
    assert command is not None
    command.verified_publishers.add((task.id, task.version, task.brief_revision, task.artifact_revision))
