"""Operator-attested review material. The receipt never grants access to a host or runs a command."""

import json
from datetime import datetime, timedelta

from pydantic import TypeAdapter
from sqlalchemy import select

from app.authority import AuthorityError, internal_authority, require_operator
from app.commands import command_transaction, current_command
from app.config import get_settings
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentTaskAssignment,
    TaskEvent,
    TaskRoutingAssessment,
)
from app.models.identity import Principal, PrincipalProfileLink, WorkspaceAuthorityState, WorkspaceMembership
from app.query_limits import MAX_BOUNDED_LIST_ITEMS, CollectionLimitExceededError
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.review_evidence import ReviewEvidenceCommand, ReviewEvidenceIssue
from app.services.agent_service import actor_has_scope, is_admin_key_principal
from app.services.review_provenance import actor_provenance, digest
from app.utils.time import as_utc, utc_now

ISSUED = "review.evidence_issued"
REVOKED = "review.evidence_revoked"


def _conflict(message, **details):
    from app.services.agent_routing_service import AgentRoutingConflictError

    raise AgentRoutingConflictError("verification_evidence_unavailable", message, **details)


async def _event(db, task_id, evidence_id):
    event = await db.scalar(
        select(TaskEvent).where(
            TaskEvent.id == evidence_id,
            TaskEvent.task_id == task_id,
            TaskEvent.event_type == ISSUED,
            TaskEvent.actor_type == "operator",
        )
    )
    if event is None:
        _conflict("No operator evidence for this task and identifier.")
    return event


async def _revocation_id(db, task_id, evidence_id):
    return await db.scalar(
        select(TaskEvent.id)
        .where(
            TaskEvent.task_id == task_id,
            TaskEvent.event_type == REVOKED,
            TaskEvent.actor_type == "operator",
            TaskEvent.span_id == str(evidence_id),
        )
        .limit(1)
    )


def history_digest(contributors, manual_execution):
    return digest({"contributors": contributors, "manual_execution": manual_execution})


async def _issuer_identity(db, principal_id, actor_id, reviewer, contributors, manual):
    """Read the issuing principal's current authority and attributable identities inside the server."""
    if not principal_id:
        _conflict("A durable operator identity is required for review evidence.")
    command = current_command(db)

    async def load(filter_, *columns):
        query = select(*columns).where(filter_)
        if command and command.mode == "apply":
            query = query.with_for_update(read=True)
        return (await db.execute(query)).one_or_none()

    # Reviewers may not enumerate workspace memberships. Only this boolean authority
    # check and the already authenticated issuer's identity are consumed outside the scope.
    with db.no_autoflush, internal_authority(db):
        principal = await load(
            Principal.id == principal_id, Principal.kind, Principal.enabled, Principal.agent_actor_id
        )
        if not principal or not principal.enabled or principal.agent_actor_id != actor_id:
            _conflict("The recorded issuing principal is no longer available.")
        link = await load(PrincipalProfileLink.principal_id == principal_id, PrincipalProfileLink.profile_id)
        profiles = {link.profile_id} if link else set()
        if actor_id is None:
            state = await load(WorkspaceAuthorityState.id == 1, WorkspaceAuthorityState.operator_principal_id)
            if principal.kind != "system" or not state or state.operator_principal_id != principal_id:
                _conflict("The recorded principal is no longer the workspace operator.")
        else:
            actor = await load(
                AgentActor.id == actor_id, AgentActor.enabled, AgentActor.lifecycle_state,
                AgentActor.scopes, AgentActor.profile_id,
            )
            membership = await load(WorkspaceMembership.principal_id == principal_id, WorkspaceMembership.role)
            operator = get_settings().workchord_auth_mode == "trusted_local" or (
                membership is not None and membership.role in {"owner", "operator"}
            )
            if not (
                principal.kind == "agent" and actor and actor.enabled and actor.lifecycle_state == "active"
                and actor_has_scope(actor, "admin") and operator
            ):
                _conflict("The recorded issuer no longer has operator authority.")
            if actor.profile_id is not None:
                profiles.add(actor.profile_id)
        participants = [reviewer, *contributors]
        participant_ids = {p["actor_id"] for p in participants if p.get("actor_id") is not None}
        participant_profiles = {p["profile_id"] for p in participants if p.get("profile_id") is not None}
        # A linked personal identity and its actor profile can differ. Both identify
        # the same participant for independence, including after a profile relink.
        if participant_ids:
            current_profiles = await db.scalars(
                select(AgentActor.profile_id).where(
                    AgentActor.id.in_(participant_ids), AgentActor.profile_id.is_not(None)
                )
            )
            participant_profiles.update(current_profiles)
            aliases = await db.scalars(select(PrincipalProfileLink.profile_id).join(
                Principal, Principal.id == PrincipalProfileLink.principal_id
            ).where(Principal.agent_actor_id.in_(participant_ids)))
            participant_profiles.update(aliases)
        if manual:
            participant_profiles.update(manual["profile_ids"])
        if (
            actor_id in participant_ids or profiles & participant_profiles
            or manual and principal_id == manual["principal_id"]
        ):
            _conflict("The issuer must be independent from the candidate's contributors and assigned reviewer.")
    return {"principal_id": principal_id, "actor_id": actor_id, "profile_ids": sorted(profiles)}


def assignment_observation(task, assignments, assignment_id, scope, candidate):
    """Validate the existing review owner before fresh-dispatch capacity is evaluated."""
    if assignment_id is None:
        return {}
    owner = next((assignment for assignment in assignments if assignment.id == assignment_id), None)
    selected = owner.review_selection if owner else None
    if not (
        owner
        and owner.task_id == task.id
        and owner.purpose == "verification"
        and owner.state in ("queued", "accepted")
        and owner.task_version == task.version
        and owner.actor_id == scope["reviewer"]["actor_id"]
        and selected
        and selected.get("reviewer") == scope["reviewer"]
        and selected.get("candidate") == candidate
        and selected.get("review_evidence") == scope
    ):
        _conflict("The given assignment no longer holds this exact independent review and evidence.")
    return {"assignment_id": owner.id, "assignment_state": owner.state}


async def resolve(db, task, evidence_id, history, *, reviewer=None):
    """Recheck expiry, revocation and immutable source/binding identity at each consuming boundary."""
    event = await _event(db, task.id, evidence_id)
    try:
        payload = json.loads(event.payload)["response"]
        record = payload["evidence"]
        expires = datetime.fromisoformat(record["expires_at"])
        valid_payload = payload["action"] == "issue" and digest(record) == payload["evidence_digest"]
    except (KeyError, TypeError, ValueError):
        _conflict("The recorded operator evidence is invalid.")
    candidate = history.candidate
    revoked = await _revocation_id(db, task.id, evidence_id)
    now = utc_now()
    if (
        revoked is not None
        or not valid_payload
        or task.status != "resolved"
        or not as_utc(event.created_at) <= now < as_utc(expires)
        or record["task_id"] != task.id
        or record["project_id"] != task.project_id
        or record["task_version"] != task.version
        or record["brief_revision"] != task.brief_revision
        or record["artifact_revision"] != task.artifact_revision
        or record["execution_history_digest"]
        != history_digest(history.contributors, history.manual_execution)
        or not candidate
        or candidate.get("digest") != record["candidate_digest"]
        or candidate.get("commit_url") != record["commit_url"]
    ):
        _conflict("Review evidence is expired, revoked, or belongs to another candidate.")
    bound = record["reviewer"]
    issuer = record["issuer"]
    identity = await _issuer_identity(db, issuer["principal_id"], event.actor_id, bound,
                                      history.contributors, history.manual_execution)
    if any(issuer.get(key) != value for key, value in identity.items()):
        _conflict("The recorded issuer identity has changed.")
    if reviewer is None:
        actor = await db.get(AgentActor, bound["actor_id"])
        if actor is None or not actor.enabled or actor.role != "verifier":
            _conflict("The verifier for this evidence is no longer available.")
        reviewer = await actor_provenance(db, actor, binding_id=bound["binding_id"])
    if reviewer != bound:
        _conflict("The current verifier identity or selected model binding differs from the receipt.")
    await _check_model(db, task, bound, record["assessment_id"], record["method"], record["tests"])
    return {"id": event.id, "digest": payload["evidence_digest"], **record}


def requirements_for(assessment, scope, actor_id, binding_id):
    """Use an exact review packet in place of host-shell only for its named verification binding."""
    if scope is None or (
        scope["reviewer"]["actor_id"],
        scope["reviewer"]["binding_id"],
    ) != (actor_id, binding_id):
        return assessment
    if not (scope.get("method") == "source_and_tests" and scope.get("tests")
            or scope.get("method") == "source_only" and assessment.get("allow_source_only_review") is True):
        return assessment
    return {
        **assessment,
        "tool_tags": [tag for tag in assessment.get("tool_tags", []) if tag != "host-shell"],
    }


async def _check_model(db, task, reviewer, expected_assessment, method, tests):
    from app.services.agent_routing_policy import (
        ROUTING_POLICY_VERSION,
        evaluate_model_envelope,
    )

    assessment = await db.scalar(
        select(TaskRoutingAssessment).where(
            TaskRoutingAssessment.task_id == task.id,
            TaskRoutingAssessment.task_version == task.version,
            TaskRoutingAssessment.policy_version == ROUTING_POLICY_VERSION,
        )
    )
    if assessment is None or assessment.id != expected_assessment:
        _conflict("An exact, current task routing assessment is required for scoped review.")
    binding = await db.get(AgentModelBinding, reviewer["binding_id"])
    catalog = await db.get(AgentModelCatalogEntry, reviewer["catalog_id"])
    if not binding or not catalog or "host-shell" not in assessment.required_model.get("tool_tags", []):
        _conflict("The assessment does not describe a host-shell review requirement.")
    if method == "source_only" and assessment.required_model.get("allow_source_only_review") is not True:
        _conflict("The current assessment must explicitly allow source-only review.")
    permitted = requirements_for(
        assessment.required_model,
        {"reviewer": reviewer, "method": method, "tests": tests},
        reviewer["actor_id"],
        binding.id,
    )
    eligibility = evaluate_model_envelope(
        permitted,
        binding_present=True,
        binding_enabled=binding.enabled,
        binding_revision_current=binding.revision == reviewer["binding_revision"],
        catalog_present=True,
        catalog_enabled=catalog.enabled,
        actual_reasoning_tier=catalog.reasoning_tier,
        actual_context_tier=catalog.context_tier,
        actual_modality_tags=catalog.modality_tags or (),
        actual_tool_tags=binding.tool_tags or (),
        actual_data_policy_tags=binding.data_policy_tags or (),
        actual_effort=catalog.effort,
        actual_qualification_keys=catalog.qualification_keys or (),
    )
    if eligibility.hard_blocker_codes:
        _conflict(
            "This reviewer still lacks other model or data-policy requirements.",
            hard_blocker_codes=list(eligibility.hard_blocker_codes),
        )
    return assessment.id


async def check_supervised_selection(db, task, principal, selection, reviewer_profile_id):
    """Supervised dispatch must also produce a positive live route for an evidence-backed verifier."""
    from app.schemas.agent_routing import AgentRoutingPreviewCreate
    from app.services.agent_routing_service import AgentRoutingService

    scope = selection["review_evidence"]
    routing = AgentRoutingService(db)
    await routing._require_preview_rollout(principal)
    data = AgentRoutingPreviewCreate(
        purpose="verification",
        assessment_id=scope["assessment_id"],
        expected_task_version=task.version,
        reviewer_profile_id=reviewer_profile_id,
        review_evidence_id=scope["id"],
        # Keep the named reviewer's row, and so its blockers, in the bounded result.
        focus_actor_id=scope["reviewer"]["actor_id"],
        focus_model_binding_id=scope["reviewer"]["binding_id"],
    )
    preview = await routing._build_preview(
        task=task, data=data, generated_at=utc_now(), requesting_actor_id=principal.id
    )
    if preview.hard_blocker_codes or not any(
        (
            candidate.actor_id,
            candidate.model_binding_id,
            candidate.model_binding_revision,
        )
        == (
            scope["reviewer"]["actor_id"],
            scope["reviewer"]["binding_id"],
            scope["reviewer"]["binding_revision"],
        )
        for candidate in preview.eligible_candidates
    ):
        _conflict(
            "The evidence-backed reviewer must pass the current verification routing policy.",
            hard_blocker_codes=preview.hard_blocker_codes,
            exclusion_codes=sorted(
                {
                    code
                    for item in preview.exclusions
                    if item.actor_id == scope["reviewer"]["actor_id"]
                    and item.model_binding_id == scope["reviewer"]["binding_id"]
                    for code in item.hard_blocker_codes
                }
            ),
        )


async def record_review_evidence(db, actor, task_id, payload, *, idempotency_key, rationale, correlation_id):
    from app.services.agent_routing_service import AgentRoutingService
    from app.services.review_provenance import select_reviewer

    require_operator(db)
    authority = db.info["authority"]
    if authority.read_only or not (
        is_admin_key_principal(actor)
        and authority.kind == "system"
        or actor.id > 0
        and authority.actor_id == actor.id
        and actor_has_scope(actor, "admin")
    ):
        raise AuthorityError(
            "operator_required",
            "The authenticated workspace operator must attest review evidence.",
        )
    data = TypeAdapter(ReviewEvidenceCommand).validate_python(payload)
    cmd = AgentPlanningCommandContext(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    issuer_id = actor.id if actor.id > 0 else None
    request_hash = digest({"payload": data.model_dump(mode="json"), "rationale": cmd.rationale})
    event_type = ISSUED if isinstance(data, ReviewEvidenceIssue) else REVOKED
    async with command_transaction(db, commit=True):
        service = AgentRoutingService(db)
        task = await service._lock_task(task_id)
        if task is None:
            raise LookupError("Task not found.")
        prior = await db.scalar(
            select(TaskEvent).where(
                TaskEvent.task_id == task_id,
                TaskEvent.event_type == event_type,
                TaskEvent.actor_type == "operator",
                TaskEvent.actor_id == issuer_id,
                TaskEvent.idempotency_key == cmd.idempotency_key,
            )
        )
        if prior:
            prior_payload = json.loads(prior.payload)
            if prior_payload["request_sha256"] != request_hash or prior_payload.get("principal_id") != authority.principal_id:
                _conflict("The idempotency key was already used for different evidence.")
            return {"event_id": prior.id, **prior_payload["response"]}
        if isinstance(data, ReviewEvidenceIssue):
            now = utc_now()
            if task.status != "resolved":
                _conflict("Issue review evidence only for a resolved candidate awaiting review.")
            if not now < data.expires_at <= now + timedelta(days=1):
                _conflict("The evidence validity must end within the next 24 hours.")
            if (
                data.expected_task_version,
                data.expected_brief_revision,
                data.expected_artifact_revision,
            ) != (task.version, task.brief_revision, task.artifact_revision):
                _conflict("Review the current task, brief and artifact revisions before attesting evidence.")
            verifier = await db.get(AgentActor, data.reviewer_actor_id)
            if verifier is None or not verifier.enabled or verifier.role != "verifier":
                _conflict("An enabled verifier is required.")
            assignments = list(
                await db.scalars(
                    select(AgentTaskAssignment)
                    .where(AgentTaskAssignment.task_id == task.id)
                    .order_by(AgentTaskAssignment.id)
                    .limit(MAX_BOUNDED_LIST_ITEMS + 1)
                )
            )
            if len(assignments) > MAX_BOUNDED_LIST_ITEMS:
                raise CollectionLimitExceededError("task review evidence assignments", MAX_BOUNDED_LIST_ITEMS)
            selection = await select_reviewer(db, task, assignments, verifier, binding_id=data.binding_id)
            if not selection or selection["acceptance_blockers"] or not selection["candidate"]:
                _conflict("An independent, exact submitted candidate is required.")
            reviewer = selection["reviewer"]
            candidate = selection["candidate"]
            commit = candidate.get("commit_url")
            if (
                reviewer["binding_revision"] != data.expected_binding_revision
                or not commit
                or commit.rsplit("/", 1)[-1] != data.commit_sha
            ):
                _conflict("The reviewer's binding or candidate commit changed.")
            identity = await _issuer_identity(db, authority.principal_id, issuer_id, reviewer,
                                              selection["contributors"], selection.get("manual_execution"))
            assessment_id = await _check_model(db, task, reviewer, data.expected_assessment_id, data.method, data.tests)
            evidence = {
                "task_id": task.id,
                "project_id": task.project_id,
                "task_version": task.version,
                "brief_revision": task.brief_revision,
                "artifact_revision": task.artifact_revision,
                "candidate_digest": candidate["digest"],
                "execution_history_digest": history_digest(
                    selection["contributors"], selection.get("manual_execution")
                ),
                "commit_url": commit,
                "reviewer": reviewer,
                "assessment_id": assessment_id,
                "method": data.method,
                "packet_sha256": data.packet_sha256,
                "issuer": {
                    **identity,
                    "transport": authority.source,
                },
                "tests": [x.model_dump() for x in data.tests],
                "expires_at": as_utc(data.expires_at).isoformat(),
            }
            result = {
                "action": "issue",
                "evidence_digest": digest(evidence),
                "evidence": evidence,
            }
            span = None
        else:
            await _event(db, task.id, data.evidence_id)
            if await _revocation_id(db, task.id, data.evidence_id) is not None:
                _conflict("This review evidence has already been revoked.")
            result = {"action": "revoke", "evidence_id": data.evidence_id}
            span = str(data.evidence_id)
        record = TaskEvent(
            task_id=task.id,
            actor_type="operator",
            actor_id=issuer_id,
            event_type=event_type,
            span_id=span,
            idempotency_key=cmd.idempotency_key,
            correlation_id=cmd.correlation_id,
            payload=json.dumps(
                {
                    "principal_id": authority.principal_id,
                    "request_sha256": request_hash,
                    "rationale": cmd.rationale,
                    "response": result,
                }
            ),
        )
        db.add(record)
        await db.flush()
        return {"event_id": record.id, **result}
