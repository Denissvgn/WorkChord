"""Record who executed resolved work that was delivered outside recorded runs.

The record is an append-only task event. Every record counts its executor, and an
agent recorder, as contributors of the task for review independence, also after later
rework. Only the latest record at the task's current brief and artifact revisions
supplies the review candidate. Recording never reopens, resolves or accepts the task
and never touches its progress.
"""

import json
from dataclasses import replace

import httpx
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.authority import AuthorityError, internal_authority
from app.commands import PlanningConflict, atomic_command
from app.models.agent import (
    AgentActor, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent,
)
from app.models.external_link import ExternalLink
from app.models.identity import Principal, PrincipalProfileLink, ProjectMembership
from app.models.task import Task
from app.models.team_member import TeamMemberProfile
from app.utils.github_links import GitHubLinkError, parse_github_url


EVENT_TYPE = "manual_provenance_recorded"
SCHEMA = "manual-provenance-v1"
REST_PATH = "POST /api/tasks/{task_id}/manual-provenance"
MCP_TOOL = "agent_record_manual_provenance"
# Event types that show an agent executed the task through WorkChord, as manual review history reads them.
AGENT_EXECUTION_EVENTS = ("agent.work_began", "agent.work_renewed", "agent.work_submitted",
                          "agent.work_recovery_required", "agent.run_created", "agent.run_finished")
MAX_RECORDS = 50


def remedy(task_id):
    """Where an accountable owner or PM records the missing provenance."""
    return {"rest": REST_PATH.format(task_id=task_id), "agent_rest": f"POST /api/agent/planning/tasks/{task_id}/manual-provenance",
            "mcp": MCP_TOOL}


class ProvenanceConflict(PlanningConflict):
    """A refusal that also names the offending fact, such as a commit and its attribution gap."""

    def __init__(self, code, message, **context):
        super().__init__(code, message)
        self.context = context

    def detail(self):
        return {**super().detail(), **self.context}


def require_provenance_recorder(db, project_id):
    """A signed-in owner, operator or project manager, or the project's PM agent, records provenance.

    The operator API key, a trusted-local browser with no signed-in person and a paired
    observer are not attributable to one accountable recorder, so none of them qualifies.
    """
    authority = db.info.get("authority")
    human = (authority is not None and authority.kind == "human" and authority.principal_id is not None
             and (authority.workspace_role in {"owner", "operator"} or authority.projects.get(project_id) == "manager"))
    pm_agent = (authority is not None and authority.kind == "agent" and authority.actor_role == "pm"
                and authority.actor_id is not None and authority.allows(project_id, "manage"))
    if authority is None or authority.read_only or not (human or pm_agent):
        raise AuthorityError("provenance_recorder_required",
            "Only a signed-in workspace owner or operator, a project manager, or the project's PM agent can record manual provenance.")
    return authority


async def provenance_blockers(db, task):
    """Why a provenance record would be refused for this task now, as action blockers; empty when it may be recorded.

    It checks the same conditions a record is judged by, without raising, so the task page offers the form only
    where it can succeed.
    """
    blockers = []
    try:
        require_provenance_recorder(db, task.project_id)
    except AuthorityError as exc:
        blockers.append({"code": exc.code, "message": str(exc)})
    if task.is_summary or task.canceled_at is not None or task.status != "resolved":
        blockers.append({"code": "manual_provenance_requires_resolved_work",
                         "message": "Record manual provenance on resolved, uncanceled leaf work."})
        return blockers
    try:
        await ManualProvenanceService(db)._require_no_recorded_execution(task)
    except PlanningConflict as exc:
        blockers.append({"code": exc.code, "message": str(exc)})
    return blockers


def _commit(url, field):
    try:
        link = parse_github_url(url)
    except (GitHubLinkError, ValueError) as exc:
        raise ValueError(f"{field} must be an immutable GitHub commit URL") from exc
    if link.github_type != "commit":
        raise ValueError(f"{field} must be an immutable GitHub commit URL")
    return link


def _links(data):
    head = _commit(data.head_commit_url, "head_commit_url")
    commits = [head.url]
    for url in data.commit_urls:
        link = _commit(url, "commit_urls")
        if link.repo_full_name.casefold() != head.repo_full_name.casefold():
            raise ValueError("Every recorded commit must belong to the head commit's repository")
        if link.url not in commits:
            commits.append(link.url)
    pr_url = None
    if data.pr_url is not None:
        try:
            pr = parse_github_url(data.pr_url)
        except (GitHubLinkError, ValueError) as exc:
            raise ValueError("pr_url must be a GitHub pull request URL") from exc
        if pr.github_type != "pull_request":
            raise ValueError("pr_url must be a GitHub pull request URL")
        pr_url = pr.url
    base_url = None
    if data.base_commit_url is not None:
        base = _commit(data.base_commit_url, "base_commit_url")
        if base.repo_full_name.casefold() != head.repo_full_name.casefold():
            raise ValueError("The base commit must belong to the head commit's repository")
        if base.url in commits:
            raise ValueError("The base commit cannot also be a recorded contribution")
        base_url = base.url
    return {"head_commit_url": head.url, "commit_urls": sorted(commits), "pr_url": pr_url, "base_commit_url": base_url}


def submitted_candidate(record):
    """The candidate fields review provenance verifies, as a worker submission would carry them."""
    submitted = {"pr_url": record.get("pr_url"), "commit_url": record["head_commit_url"],
                 "artifact_links": list(record["commit_urls"])}
    if record.get("base_commit_url"):
        submitted["execution_provenance"] = {"submitted_base_commit_url": record["base_commit_url"]}
    return submitted


def _valid(record):
    return (isinstance(record, dict) and record.get("schema") == SCHEMA and type(record.get("version")) is int
            and isinstance(record.get("executor"), dict) and isinstance(record.get("commit_urls"), list)
            and isinstance(record.get("head_commit_url"), str))


async def recorded_provenances(db, task):
    """Every provenance record of the task, oldest first, and the one that applies to its current revisions.

    Contribution does not go stale: each record's executor and agent recorder stay contributors
    after later rework. Only the latest record, while the brief and artifact revisions are
    unchanged, supplies the review candidate. A record that cannot be read is returned as None
    so that review treats its contribution as unknown; more records than the bound fail closed.
    """
    events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == task.id, TaskEvent.event_type == EVENT_TYPE)
                               .order_by(TaskEvent.id).limit(MAX_RECORDS + 1))).all()
    if len(events) > MAX_RECORDS:
        from app.query_limits import CollectionLimitExceededError
        raise CollectionLimitExceededError("manual provenance records", MAX_RECORDS)
    records = []
    for event in events:
        try:
            record = json.loads(event.payload or "{}")
        except (TypeError, ValueError):
            record = None
        records.append((event, record if _valid(record) else None))
    current = None
    if records and records[-1][1] is not None:
        event, record = records[-1]
        if (record.get("artifact_revision") == task.artifact_revision and record.get("brief_revision") == task.brief_revision
                and record["version"] <= task.version):
            current = (event, record)
    return records, current


def response(event, record):
    executor = record["executor"]
    return {"event_id": event.id, "task_id": event.task_id, "task_version": record["version"],
            "brief_revision": record["brief_revision"], "artifact_revision": record["artifact_revision"],
            "executor": {key: executor.get(key) for key in ("kind", "principal_id", "actor_id", "binding_id",
                                                            "catalog_key", "publisher_key")}
                        | {"profile_ids": list(executor.get("profile_ids") or ())},
            "head_commit_url": record["head_commit_url"], "commit_urls": record["commit_urls"],
            "pr_url": record.get("pr_url"), "base_commit_url": record.get("base_commit_url"), "reason": record["reason"],
            "recorded_by_principal_id": record.get("principal_id"), "recorded_by_actor_id": event.actor_id,
            "recorder_publisher_key": (record.get("recorder") or {}).get("publisher_key"),
            "recorded_at": event.created_at}


class ManualProvenanceService:
    def __init__(self, db):
        self.db = db

    @property
    def tasks(self):
        from app.services.task_service import TaskService
        return TaskService(self.db)

    async def record(self, task_id, data, *, commit=True):
        """Record the executor and the delivered candidate of one resolved task.

        The candidate is checked against GitHub before any lock is taken, with the same
        check the verifier's verdict uses. The command audit carries the record's own
        reason, whatever the request headers said.
        """
        hint = await self.db.scalar(select(Task).where(Task.id == task_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        authority = require_provenance_recorder(self.db, hint.project_id)
        if data.executor.kind == "human" and authority.kind != "human":
            # A human executor carries no publisher, so only an accountable person may attest one.
            raise AuthorityError("manual_provenance_human_recorder_required",
                "Only a signed-in workspace owner, operator or project manager can record a human executor.")
        links = _links(data)
        await self._verify_candidate(hint, links)
        self.db.info["authority"] = replace(authority, reason=data.reason[:2000])
        try:
            return await self._record(task_id, data, links, commit=commit)
        finally:
            self.db.info["authority"] = authority

    async def _verify_candidate(self, task, links):
        """Refuse a candidate that the verdict-time check could never pass."""
        from app.services.github_status_service import GitHubStatusService
        from app.services.review_provenance import _submission_candidate
        candidate = await _submission_candidate(self.db, task, submitted_candidate(links), {"manual_provenance_event_id": None})
        if candidate is None:
            raise ValueError("The pull request, head commit and base commit do not form one verifiable candidate; "
                             "link at most one pull request to the task and name its head commit")
        head = parse_github_url(candidate["commit_url"])
        attributed = {parse_github_url(url).sha: {"recorded"} for url in links["commit_urls"]}
        context = {}
        pr = parse_github_url(candidate["pr_url"]) if candidate["pr_url"] else None
        base = None if pr else parse_github_url(candidate["base_commit_url"])
        github = await GitHubStatusService.from_runtime(self.db)
        # Only the GitHub client's fetch and the parsing of GitHub's payloads are inside this block.
        try:
            if pr is not None:
                blocker = await github.verify_review_head(pr, head.sha, attributed, expected_repository=head.repo_full_name,
                                                          failure_context=context)
            else:
                blocker = await github.verify_review_range(base, head, attributed, failure_context=context)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise ProvenanceConflict("manual_provenance_candidate_unverifiable",
                    "GitHub does not show the declared pull request or commits. Check the URL and repository access.",
                    attribution_gap="candidate_unverifiable") from exc
            raise ProvenanceConflict("manual_provenance_candidate_unverifiable",
                "GitHub could not confirm the declared candidate. Check the GitHub connection, then retry.",
                attribution_gap="github_unavailable") from exc
        except (httpx.HTTPError, json.JSONDecodeError) as exc:
            # The GitHub client's own transport and decoding failures are an outage.
            raise ProvenanceConflict("manual_provenance_candidate_unverifiable",
                "GitHub could not confirm the declared candidate. Check the GitHub connection, then retry.",
                attribution_gap="github_unavailable") from exc
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            # A payload GitHub returned that is not the expected shape, as the verdict-time check treats it.
            raise ProvenanceConflict("manual_provenance_candidate_unverifiable",
                "GitHub returned a response that does not describe the declared candidate.",
                attribution_gap="candidate_unverifiable") from exc
        if blocker is None:
            return
        if blocker == "verification_contributors_unverifiable":
            sha, gap = context.get("offending_sha"), context.get("attribution_gap", "commit_attribution")
            explanation = {
                "commit_attribution": "is not one of the recorded commit_urls; list every commit of the candidate",
                "coauthor_trailer": ("carries a Co-authored-by trailer, so its other contributors stay unverifiable; "
                                     "commits with co-author trailers cannot be attested this way"),
            }.get(gap, "has commit metadata that cannot be attributed")
            raise ProvenanceConflict("manual_provenance_candidate_unverifiable", f"Commit {sha} {explanation}.",
                                     offending_sha=sha, attribution_gap=gap)
        gap = "head_mismatch" if blocker == "verification_candidate_stale" else "candidate_unverifiable"
        raise ProvenanceConflict("manual_provenance_candidate_unverifiable",
            "The pull request head or commit range does not match the declared head commit." if gap == "head_mismatch"
            else "GitHub does not show the declared commits as one verifiable candidate.", attribution_gap=gap)

    @atomic_command
    async def _record(self, task_id, data, links, *, commit=True):
        await self.tasks._lock_task_scope(task_id)
        task = await self.tasks.get_by_id(task_id)
        if task is None:
            raise LookupError("Task not found or inaccessible")
        authority = require_provenance_recorder(self.db, task.project_id)
        self.tasks.ensure_expected_version(task, data.expected_version)
        if task.is_summary or task.canceled_at is not None or task.status != "resolved":
            raise PlanningConflict("manual_provenance_requires_resolved_work",
                "Record manual provenance on resolved, uncanceled leaf work. The record never reopens or accepts a task.")
        if task.artifact_revision != data.artifact_revision:
            raise ValueError("Artifact revision is stale")
        existing = await self.db.scalar(select(func.count(TaskEvent.id)).where(
            TaskEvent.task_id == task.id, TaskEvent.event_type == EVENT_TYPE))
        if existing >= MAX_RECORDS:
            # Review reads every record; more than the bound would make the task unreviewable.
            raise PlanningConflict("manual_provenance_record_limit",
                f"This task already has {MAX_RECORDS} provenance records, the most review can read. "
                "Record a clean replacement instead.")
        await self._require_no_recorded_execution(task)
        self._require_consistent_executor(task, data.executor)
        if links["pr_url"] is not None:
            await self._require_task_evidence(task, links["pr_url"])
        executor = await self._executor(data.executor, task)
        record = {"schema": SCHEMA, "brief_revision": task.brief_revision, "artifact_revision": task.artifact_revision,
                  "executor": executor, **links, "reason": data.reason}
        if authority.kind == "agent":
            record["recorder"] = await self._agent_recorder(authority.actor_id)
        from app.services.review_provenance import _submission_candidate
        if await _submission_candidate(self.db, task, submitted_candidate(record), {"manual_provenance_event_id": None}) is None:
            raise ValueError("The pull request, head commit and base commit do not form one verifiable candidate; "
                             "link at most one pull request to the task and name its head commit")
        await self.tasks.reserve_task_version(task, data.expected_version)
        record["version"] = task.version
        event = await self.tasks.record_task_event(task.id, EVENT_TYPE, record)
        await self.db.flush()
        return response(event, json.loads(event.payload))

    async def _require_no_recorded_execution(self, task):
        run = await self.db.scalar(select(AgentRun.id).where(AgentRun.task_id == task.id).limit(1))
        execution = await self.db.scalar(select(AgentTaskAssignment.id).where(
            AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.purpose == "execution",
            AgentTaskAssignment.state.in_(("queued", "accepted", "fulfilled"))).limit(1))
        agent_event = await self.db.scalar(select(TaskEvent.id).where(
            TaskEvent.task_id == task.id, TaskEvent.event_type.in_(AGENT_EXECUTION_EVENTS)).limit(1))
        if run is not None or execution is not None or agent_event is not None or task.claimed_by is not None:
            raise PlanningConflict("manual_provenance_execution_recorded",
                "This task has recorded agent execution, which supplies its own provenance. "
                "Reconcile that execution or record a clean replacement instead.")
        from app.services.review_provenance import _manual_history
        if (await _manual_history(self.db, task)).manual_execution is not None:
            raise PlanningConflict("manual_provenance_execution_recorded",
                "An authenticated person already recorded manual execution of this artifact; it supplies the provenance.")

    @staticmethod
    def _require_consistent_executor(task, executor):
        """A record never contradicts authenticated manual execution of the task.

        Only manual execution makes the stamped principal evidence of who executed the work. In
        scheduled mode any status change stamps its caller, for example a manager resolving the
        task through the status route, so the stamp says nothing about execution.
        """
        if task.execution_mode != "manual":
            return
        if task.executed_by_principal_id is not None:
            if executor.kind != "human" or executor.principal_id != task.executed_by_principal_id:
                raise PlanningConflict("manual_provenance_executor_conflict",
                    f"The task is in manual execution by principal {task.executed_by_principal_id}; "
                    "a provenance record can only name that person.")
        elif executor.kind != "human":
            raise PlanningConflict("manual_provenance_executor_conflict",
                "The task is in manual execution, so a provenance record can only name a human executor.")

    async def _require_task_evidence(self, task, pr_url):
        """The declared pull request must already be the task's own evidence."""
        progress = task.progress if isinstance(task.progress, dict) else {}
        candidates = [url for url in progress.get("artifacts") or () if isinstance(url, str)]
        candidates += list(await self.db.scalars(select(ExternalLink.url).where(
            ExternalLink.entity_type == "task", ExternalLink.entity_id == task.id, ExternalLink.provider == "github")))
        for url in candidates:
            try:
                link = parse_github_url(url)
            except (GitHubLinkError, ValueError):
                continue
            if link.github_type == "pull_request" and link.url == pr_url:
                return
        raise PlanningConflict("manual_provenance_pr_not_task_evidence",
            "The pull request is neither a progress artifact of the task nor a GitHub link on it. "
            "Link the pull request to the task first.")

    async def _agent_recorder(self, actor_id):
        """An agent recorder is accountable like a contributor: its actor, profile and publisher are kept."""
        from app.services.review_provenance import actor_provenance
        # Actor, binding and catalog rows are server-owned; the caller's read scope does not decide them.
        with internal_authority(self.db):
            actor = await self.db.scalar(select(AgentActor).where(AgentActor.id == actor_id))
            receipt = await actor_provenance(self.db, actor, lock=True) if actor is not None else {}
            # The recorder may run under any of its enabled bindings, so each one's publisher counts.
            publishers = list(await self.db.scalars(select(AgentModelCatalogEntry.publisher_key)
                .join(AgentModelBinding, AgentModelBinding.model_catalog_id == AgentModelCatalogEntry.id)
                .where(AgentModelBinding.actor_id == actor_id, AgentModelBinding.enabled.is_(True),
                       AgentModelCatalogEntry.enabled.is_(True)))) if actor is not None else []
        missing = [key for key in ("profile_id", "binding_id", "publisher_key") if not receipt.get(key)]
        if not missing and not all(publishers):
            missing.append("publisher_key of every enabled binding")
        if missing:
            raise PlanningConflict("manual_provenance_recorder_unattributable",
                f"The recording agent lacks {', '.join(missing)}. Its enabled model bindings must declare a publisher, "
                "because a verifier must be independent of the recorder too.")
        return {"kind": "agent", **receipt, "publisher_keys": sorted(set(publishers) | {receipt["publisher_key"]})}

    async def _require_project_actor(self, actor, task):
        """The agent executor must belong to the task's project.

        An agent belongs to a project through its principal's project membership, or through an
        assignment it holds on a task of that project.
        """
        if task.project_id is None:
            return
        member = await self.db.scalar(select(ProjectMembership.principal_id).join(
            Principal, Principal.id == ProjectMembership.principal_id).where(
            Principal.agent_actor_id == actor.id, ProjectMembership.project_id == task.project_id).limit(1))
        assigned = member is not None or await self.db.scalar(select(AgentTaskAssignment.id).join(
            Task, Task.id == AgentTaskAssignment.task_id).where(
            AgentTaskAssignment.actor_id == actor.id, Task.project_id == task.project_id).limit(1)) is not None
        if not assigned:
            raise PlanningConflict("manual_provenance_executor_outside_project",
                "The agent executor is not a member of this task's project and holds no assignment in it.")

    async def _executor(self, data, task):
        if data.kind == "human":
            # Identity rows are server-owned; the recorder's read scope does not decide who the executor is.
            with internal_authority(self.db):
                principal = await self.db.scalar(select(Principal).where(Principal.id == data.principal_id))
                if principal is None or principal.kind != "human" or principal.agent_actor_id is not None:
                    raise PlanningConflict("manual_provenance_executor_unknown", "The executor must be a known human principal.")
                profile_id = await self.db.scalar(select(PrincipalProfileLink.profile_id).where(
                    PrincipalProfileLink.principal_id == principal.id))
            return {"kind": "human", "principal_id": principal.id, "profile_ids": [profile_id] if profile_id else []}
        with internal_authority(self.db):
            actor = await self.db.scalar(select(AgentActor).where(AgentActor.id == data.actor_id))
            if actor is None:
                raise PlanningConflict("manual_provenance_executor_unknown", "The executor must be a known agent actor.")
            # Checked before any binding detail is read, so a recorder cannot read back another project's actor.
            await self._require_project_actor(actor, task)
            receipt = await self._binding_receipt(actor, data.model_binding_id)
        missing = [key for key in ("profile_id", "binding_id", "publisher_key") if not receipt[key]]
        if missing:
            raise PlanningConflict("manual_provenance_executor_unattributable",
                f"The agent executor lacks {', '.join(missing)}. Name a model binding of this actor whose catalog entry "
                "declares a publisher, on an actor with a profile.")
        return {"kind": "agent", "profile_ids": [receipt["profile_id"]], **receipt}

    async def _binding_receipt(self, actor, binding_id):
        """The executor's profile, binding and publisher at the moment of the record.

        Without a binding id the actor's enabled default binding is used. A named binding may
        be disabled, or its catalog entry retired, because the work may predate that; it must
        belong to the actor, and its catalog entry's publisher at this moment is recorded.
        """
        from app.services.review_provenance import actor_provenance
        if binding_id is None:
            return await actor_provenance(self.db, actor, lock=True)
        from app.services.agent_routing_service import AgentRoutingService
        profile = await self.db.scalar(select(TeamMemberProfile).where(TeamMemberProfile.id == actor.profile_id)
                                       .options(selectinload(TeamMemberProfile.skills))
                                       .execution_options(populate_existing=True)
                                       .with_for_update(read=True)) if actor.profile_id is not None else None
        row = (await self.db.execute(select(AgentModelBinding, AgentModelCatalogEntry)
            .join(AgentModelCatalogEntry, AgentModelCatalogEntry.id == AgentModelBinding.model_catalog_id)
            .where(AgentModelBinding.id == binding_id, AgentModelBinding.actor_id == actor.id)
            .with_for_update(read=True))).one_or_none()
        receipt = {"actor_id": actor.id, "profile_id": actor.profile_id,
                   "profile_revision": AgentRoutingService._profile_revision(profile),
                   "binding_id": None, "binding_revision": None, "catalog_id": None, "catalog_revision": None,
                   "catalog_key": None, "configured_model_alias": None, "publisher_key": None}
        if row is not None:
            binding, catalog = row
            receipt.update(binding_id=binding.id, binding_revision=binding.revision, catalog_id=catalog.id,
                           catalog_revision=catalog.revision, catalog_key=catalog.key,
                           configured_model_alias=catalog.configured_model_alias, publisher_key=catalog.publisher_key)
        return receipt
