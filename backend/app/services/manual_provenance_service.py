"""Record who executed resolved work that was delivered outside recorded runs.

The record is an append-only task event bound to the task's current brief and
artifact revisions. Review provenance reads the latest record for exactly those
revisions; a later artifact or brief change makes it stale. Recording never
reopens, resolves or accepts the task and never touches its progress.
"""

import json
from dataclasses import replace

from sqlalchemy import select

from app.authority import AuthorityError, internal_authority
from app.commands import PlanningConflict, atomic_command
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.identity import Principal, PrincipalProfileLink
from app.models.task import Task
from app.utils.github_links import GitHubLinkError, parse_github_url


EVENT_TYPE = "manual_provenance_recorded"
SCHEMA = "manual-provenance-v1"
REST_PATH = "POST /api/tasks/{task_id}/manual-provenance"
MCP_TOOL = "agent_record_manual_provenance"


def remedy(task_id):
    """Where an accountable owner or PM records the missing provenance."""
    return {"rest": REST_PATH.format(task_id=task_id), "agent_rest": f"POST /api/agent/planning/tasks/{task_id}/manual-provenance",
            "mcp": MCP_TOOL}


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


async def recorded_provenance(db, task):
    """The latest provenance record that applies to the task's current revisions, or None."""
    event = await db.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id, TaskEvent.event_type == EVENT_TYPE)
                            .order_by(TaskEvent.id.desc()).limit(1))
    if event is None:
        return None
    try:
        record = json.loads(event.payload or "{}")
    except (TypeError, ValueError):
        return None
    if (not isinstance(record, dict) or record.get("schema") != SCHEMA
            or record.get("artifact_revision") != task.artifact_revision or record.get("brief_revision") != task.brief_revision
            or type(record.get("version")) is not int or record["version"] > task.version
            or not isinstance(record.get("executor"), dict) or not isinstance(record.get("commit_urls"), list)
            or not isinstance(record.get("head_commit_url"), str)):
        return None
    return event, record


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

        The command audit carries the record's own reason, whatever the request headers said.
        """
        hint = await self.db.scalar(select(Task).where(Task.id == task_id))
        if hint is None:
            raise LookupError("Task not found or inaccessible")
        authority = require_provenance_recorder(self.db, hint.project_id)
        self.db.info["authority"] = replace(authority, reason=data.reason[:2000])
        try:
            return await self._record(task_id, data, commit=commit)
        finally:
            self.db.info["authority"] = authority

    @atomic_command
    async def _record(self, task_id, data, *, commit=True):
        await self.tasks._lock_task_scope(task_id)
        task = await self.tasks.get_by_id(task_id)
        if task is None:
            raise LookupError("Task not found or inaccessible")
        require_provenance_recorder(self.db, task.project_id)
        self.tasks.ensure_expected_version(task, data.expected_version)
        if task.is_summary or task.canceled_at is not None or task.status != "resolved":
            raise PlanningConflict("manual_provenance_requires_resolved_work",
                "Record manual provenance on resolved, uncanceled leaf work. The record never reopens or accepts a task.")
        if task.artifact_revision != data.artifact_revision:
            raise ValueError("Artifact revision is stale")
        await self._require_no_recorded_execution(task)
        executor = await self._executor(data.executor)
        record = {"schema": SCHEMA, "brief_revision": task.brief_revision, "artifact_revision": task.artifact_revision,
                  "executor": executor, **_links(data), "reason": data.reason}
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
        if run is not None or execution is not None or task.claimed_by is not None:
            raise PlanningConflict("manual_provenance_execution_recorded",
                "This task has recorded agent execution, which supplies its own provenance. "
                "Reconcile that execution or record a clean replacement instead.")
        from app.services.review_provenance import _manual_history
        if (await _manual_history(self.db, task)).manual_execution is not None:
            raise PlanningConflict("manual_provenance_execution_recorded",
                "An authenticated person already recorded manual execution of this artifact; it supplies the provenance.")

    async def _executor(self, data):
        if data.kind == "human":
            # Identity rows are server-owned; the recorder's read scope does not decide who the executor is.
            with internal_authority(self.db):
                principal = await self.db.scalar(select(Principal).where(Principal.id == data.principal_id))
                if principal is None or principal.kind != "human" or principal.agent_actor_id is not None:
                    raise PlanningConflict("manual_provenance_executor_unknown", "The executor must be a known human principal.")
                profile_id = await self.db.scalar(select(PrincipalProfileLink.profile_id).where(
                    PrincipalProfileLink.principal_id == principal.id))
            return {"kind": "human", "principal_id": principal.id, "profile_ids": [profile_id] if profile_id else []}
        from app.services.review_provenance import actor_provenance
        actor = await self.db.scalar(select(AgentActor).where(AgentActor.id == data.actor_id))
        if actor is None:
            raise PlanningConflict("manual_provenance_executor_unknown", "The executor must be a known agent actor.")
        receipt = await actor_provenance(self.db, actor, binding_id=data.model_binding_id, lock=True)
        missing = [key for key in ("profile_id", "binding_id", "publisher_key") if not receipt[key]]
        if missing:
            raise PlanningConflict("manual_provenance_executor_unattributable",
                f"The agent executor lacks {', '.join(missing)}. Name an enabled model binding whose catalog entry "
                "declares a publisher, on an actor with a profile.")
        return {"kind": "agent", "actor_id": actor.id, "profile_ids": [receipt["profile_id"]], **receipt}
