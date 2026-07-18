"""Agent integration API router."""
import json
import logging
from typing import Annotated, Any, NoReturn, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent_contract import agent_contract_features
from app.config import get_settings
from app.database import get_db
from app.models.agent import AgentActor
from app.models.team_member import TeamMemberProfile
from app.security import ADMIN_API_KEY_HEADER, admin_api_key_is_valid
from app.schemas.agent import (
    AgentActorCreate,
    AgentActorCreatedResponse,
    AgentActorRosterItem,
    AgentActorResponse,
    AgentActorUpdate,
    AgentDiscoveryTriageCreate,
    AgentDiscoveryTriageResponse,
    AgentCapabilitiesResponse,
    AgentReviewVerdict,
    AgentReviewVerdictResponse,
    AgentReviewQueueResponse,
    AgentRecoveryListResponse,
    AgentRecoveryRequeue,
    AgentRecoveryRequeueResponse,
    AgentRunCreate,
    AgentRunEventCreate,
    AgentRunEventResponse,
    AgentRunFinish,
    AgentRunResponse,
    AgentTaskAssignmentCreate,
    AgentTaskAssignmentResponse,
    AgentTaskAssignmentUpdate,
    AgentTaskContextResponse,
    AgentTaskCreate,
    AgentTaskPatch,
    AgentWorkBegin,
    AgentWorkBeginResponse,
    AgentWorkDecisionResponse,
    AgentWorkRenew,
    AgentWorkSubmit,
    AgentWorkTerminal,
    AgentWorkTerminalResponse,
    TaskClaimRequest,
    TaskClaimResponse,
    TaskEventCreate,
    TaskEventResponse,
    AgentPipelineResponse,
    AgentProjectUpdateCreate,
    AgentProjectUpdateResponse,
    AgentRunDetailResponse,
)
from app.schemas.common import MessageResponse
from app.schemas.agent_skill_bundle import SkillBundleCatalogResponse
from app.schemas.task import TaskResponse
from app.utils.time import utc_now
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    AgentService,
    actor_has_scope,
    actor_scopes,
    require_scope,
)
from app.services.agent_work_service import AgentWorkService
from app.services.agent_skill_bundle_service import (
    AgentSkillBundleService,
    SkillBundleArtifactError,
)
from app.routers.agent_skill_bundles import get_agent_skill_bundle_service
from app.services.task_service import TaskVersionConflictError

router = APIRouter()
logger = logging.getLogger(__name__)


def _if_none_match_matches(value: Optional[str], etag: str) -> bool:
    """Apply weak If-None-Match comparison for a GET representation."""
    if not value:
        return False

    def normalize(tag: str) -> str:
        candidate = tag.strip()
        return candidate[2:] if candidate.startswith("W/") else candidate

    expected = normalize(etag)
    return any(
        candidate.strip() == "*" or normalize(candidate) == expected
        for candidate in value.split(",")
    )


async def get_agent_service(db: Annotated[AsyncSession, Depends(get_db)]) -> AgentService:
    """Dependency for agent service."""
    return AgentService(db)


async def get_agent_work_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AgentWorkService:
    """Dependency for durable assignment and worker lifecycle operations."""
    return AgentWorkService(db)


async def get_agent_actor(
    service: Annotated[AgentService, Depends(get_agent_service)],
    api_key: Annotated[Optional[str], Header(alias="X-Agent-API-Key")] = None,
) -> AgentActor:
    """Authenticate an agent API key."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Agent-API-Key header",
        )
    actor = await service.authenticate(api_key)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or disabled agent API key",
        )
    return actor


def _admin_header_actor() -> AgentActor:
    """Build a transient actor for authenticated human control-plane access."""
    return AgentActor(
        id=0,
        name="admin-api-key",
        display_name="Admin API Key",
        api_key_hash="admin",
        scopes=json.dumps(["admin"]),
        enabled=True,
        created_at=utc_now(),
    )


async def get_agent_admin_actor(
    service: Annotated[AgentService, Depends(get_agent_service)],
    agent_api_key: Annotated[Optional[str], Header(alias="X-Agent-API-Key")] = None,
    admin_api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None,
) -> AgentActor:
    """Authenticate a stored admin actor, bootstrap provisioning key, or admin API key."""
    if agent_api_key:
        actor = await service.authenticate(agent_api_key)
        if actor:
            return actor
        bootstrap_actor = service.authenticate_bootstrap_key(agent_api_key)
        if bootstrap_actor:
            return bootstrap_actor
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or disabled agent API key",
        )
    if admin_api_key_is_valid(admin_api_key):
        return _admin_header_actor()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Missing or invalid {ADMIN_API_KEY_HEADER} or X-Agent-API-Key header",
    )


async def require_agent_read_access(
    service: Annotated[AgentService, Depends(get_agent_service)],
    agent_api_key: Annotated[Optional[str], Header(alias="X-Agent-API-Key")] = None,
    admin_api_key: Annotated[Optional[str], Header(alias=ADMIN_API_KEY_HEADER)] = None,
) -> None:
    """Allow pipeline reads from a configured admin key or scoped agent key."""
    if admin_api_key_is_valid(admin_api_key):
        return
    if not agent_api_key:
        if not get_settings().workchord_admin_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Admin API key is not configured.",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing or invalid {ADMIN_API_KEY_HEADER} or X-Agent-API-Key header",
        )
    actor = await service.authenticate(agent_api_key)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or disabled agent API key",
        )
    try:
        require_scope(actor, "planning:read")
    except AgentPermissionError as exc:
        _handle_agent_error(exc)


def _handle_agent_error(exc: Exception, *, structured: bool = False) -> NoReturn:
    """Convert service errors to HTTP errors."""
    if isinstance(exc, AgentPermissionError):
        detail: Any = (
            {"code": "agent_permission_denied", "message": str(exc)}
            if structured
            else str(exc)
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    if isinstance(exc, TaskVersionConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail())
    if isinstance(exc, AgentConflictError):
        detail = (
            {"code": "agent_state_conflict", "message": str(exc)}
            if structured
            else str(exc)
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
    if isinstance(exc, ValueError):
        detail = (
            {"code": "agent_validation_error", "message": str(exc)}
            if structured
            else str(exc)
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    raise exc


def _claim_response(service: AgentService, task) -> TaskClaimResponse:
    claim_expires_at = task.claim_expires_at
    claim_id = task.claim_id
    claim_generation = task.claim_generation
    if claim_expires_at is None or claim_id is None or claim_generation < 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task claim did not receive a complete fence and expiration timestamp",
        )
    return TaskClaimResponse(
        task=service.task_service.task_to_response(task),
        claim_expires_at=claim_expires_at,
        claim_id=claim_id,
        claim_generation=claim_generation,
    )


def _actor_response(actor: AgentActor) -> AgentActorResponse:
    return AgentActorResponse(
        id=actor.id,
        name=actor.name,
        display_name=actor.display_name,
        scopes=actor_scopes(actor),
        enabled=actor.enabled,
        role=actor.role,
        profile_id=actor.profile_id,
        work_policy=actor.work_policy or "assigned_only",
        max_parallel_work=actor.max_parallel_work or 1,
        queue_revision=actor.queue_revision or 1,
        created_at=actor.created_at,
        last_seen_at=actor.last_seen_at,
    )


@router.get("/agent/capabilities", response_model=AgentCapabilitiesResponse)
async def get_agent_capabilities(
    request: Request,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    bundle_service: Annotated[
        AgentSkillBundleService, Depends(get_agent_skill_bundle_service)
    ],
):
    """Return the authenticated actor and supported agent contract features."""
    features = agent_contract_features(include_skill_bundles=False)
    recommended_skills: dict[str, str] = {}
    catalog_version = None
    catalog_url = None
    discovery_url = None
    settings = get_settings()
    if settings.agent_skill_bundles_public or actor_has_scope(actor, "skills:read"):
        try:
            catalog = SkillBundleCatalogResponse.model_validate_json(
                bundle_service.catalog_payload().content
            )
        except SkillBundleArtifactError:
            logger.warning(
                "Agent skill catalog is unavailable; omitting bundle capabilities",
                exc_info=True,
            )
        else:
            features.append("skill-bundles-v1")
            catalog_version = catalog.catalog_version
            catalog_url = f"{settings.api_prefix.rstrip('/')}/agent/skill-bundles"
            discovery_url = "/.well-known/workchord-agent-skills.json"
            for skill in catalog.skills:
                recommended_skills[skill.role] = f"{skill.name}@{skill.version}"
    return AgentCapabilitiesResponse(
        server_version=request.app.version,
        api_contract="workchord-agent/v1",
        actor=service.actor_response(actor),
        scopes=actor_scopes(actor),
        lease_limits={"minimum_seconds": 60, "default_seconds": 3600, "maximum_seconds": 86400},
        features=features,
        recommended_skills=recommended_skills,
        lifecycle_actions=[
            "assign",
            "reorder",
            "begin",
            "renew",
            "submit",
            "fail",
            "verify",
            "rework",
            "recover",
            "report",
            "report_discovery",
        ],
        skill_catalog_version=catalog_version,
        skill_catalog_url=catalog_url,
        skill_discovery_url=discovery_url,
    )


@router.post(
    "/agent/actors",
    response_model=AgentActorCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_actor(
    data: AgentActorCreate,
    response: Response,
    actor: Annotated[AgentActor, Depends(get_agent_admin_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
):
    """Create an agent actor. Requires admin scope."""
    try:
        require_scope(actor, "admin")
        created, api_key = await service.create_actor(data)
    except Exception as exc:
        _handle_agent_error(exc)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    base = _actor_response(created).model_dump()
    return AgentActorCreatedResponse(**base, api_key=api_key)


@router.get("/agent/actors", response_model=list[AgentActorRosterItem])
async def list_agent_actors(
    actor: Annotated[AgentActor, Depends(get_agent_admin_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
):
    """Return the secret-free actor roster for scoped PM planning."""
    try:
        return await service.list_actor_roster(actor)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.patch("/agent/actors/{actor_id}", response_model=AgentActorResponse)
async def update_agent_actor(
    actor_id: int,
    data: AgentActorUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_admin_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
):
    """Update non-secret actor policy and profile metadata. Requires admin scope."""
    try:
        require_scope(actor, "admin")
        target = await service.db.get(AgentActor, actor_id)
        if target is None:
            raise ValueError("Agent actor not found")
        if "profile_id" in data.model_fields_set and data.profile_id is not None:
            profile = await service.db.get(TeamMemberProfile, data.profile_id)
            if profile is None:
                raise ValueError("Team member profile not found")

        queue_policy_fields = {
            "enabled",
            "role",
            "profile_id",
            "work_policy",
            "max_parallel_work",
        }
        queue_policy_changed = False
        for field_name in data.model_fields_set:
            value = getattr(data, field_name)
            stored_value = json.dumps(value) if field_name == "scopes" else value
            if getattr(target, field_name) != stored_value:
                setattr(target, field_name, stored_value)
                queue_policy_changed = queue_policy_changed or field_name in queue_policy_fields
        if queue_policy_changed:
            target.queue_revision += 1
        await service.db.commit()
        await service.db.refresh(target)
        return service.actor_response(target)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post(
    "/agent/assignments",
    response_model=AgentTaskAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_assignment(
    data: AgentTaskAssignmentCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
):
    """Dispatch one task to an exact actor using PM assignment scope."""
    try:
        return await service.create_assignment(
            actor,
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get(
    "/agent/assignments",
    response_model=list[AgentTaskAssignmentResponse],
)
async def list_agent_assignments(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    task_id: Optional[int] = Query(default=None, ge=1),
    actor_id: Optional[int] = Query(default=None, ge=1),
    purpose: Optional[str] = Query(default=None),
    state: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
):
    """List durable assignments within the caller's authorized queue boundary."""
    try:
        return await service.list_assignments(
            actor,
            task_id=task_id,
            actor_id=actor_id,
            purpose=purpose,
            state=state,
            limit=limit,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.patch(
    "/agent/assignments/{assignment_id}",
    response_model=AgentTaskAssignmentResponse,
)
async def update_agent_assignment(
    assignment_id: int,
    data: AgentTaskAssignmentUpdate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
):
    """Reassign, reorder, or cancel queued work using PM assignment scope."""
    try:
        return await service.update_assignment(
            assignment_id,
            actor,
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get("/agent/tasks/ready", response_model=list[TaskResponse])
async def list_ready_tasks(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    iteration_id: Optional[int] = None,
    tags: Annotated[Optional[list[str]], Query()] = None,
    priority_min: Optional[int] = Query(None, ge=1, le=10),
    priority_max: Optional[int] = Query(None, ge=1, le=10),
    assignee_id: Optional[int] = None,
    capabilities: Annotated[Optional[list[str]], Query()] = None,
    limit: int = Query(50, ge=1, le=200),
):
    """Return claimable tasks with satisfied dependencies."""
    try:
        tasks = await service.list_ready_tasks(
            actor,
            iteration_id=iteration_id,
            tags=tags,
            priority_min=priority_min,
            priority_max=priority_max,
            assignee_id=assignee_id,
            capabilities=capabilities,
            limit=limit,
        )
    except Exception as exc:
        _handle_agent_error(exc)
    return [service.task_service.task_to_response(task) for task in tasks]


@router.get("/agent/me/work", response_model=AgentWorkDecisionResponse)
async def get_my_agent_work(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    response: Response,
    limit: int = Query(20, ge=1, le=200),
    cursor: Optional[str] = None,
    if_none_match: Annotated[Optional[str], Header(alias="If-None-Match")] = None,
):
    """Return the server-authoritative resume, begin, wait, or recovery decision."""
    try:
        decision = await service.get_work(actor, limit=limit, cursor=cursor)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)
    etag = service.work_etag(decision, cursor=cursor, limit=limit)
    cache_headers = {"ETag": etag, "Cache-Control": "private, no-cache"}
    if decision.next_poll_after is not None:
        retry_after = max(
            1,
            int(
                (
                    decision.next_poll_after - utc_now()
                ).total_seconds()
            ),
        )
        cache_headers["Retry-After"] = str(retry_after)
    if _if_none_match_matches(if_none_match, etag):
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=cache_headers)
    response.headers.update(cache_headers)
    return decision


@router.get("/agent/me/claims", response_model=list[dict[str, Any]])
async def list_my_agent_claims(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
):
    """Return claims currently owned by the authenticated actor."""
    try:
        return await service.list_my_claims(actor)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get("/agent/me/runs", response_model=list[AgentRunResponse])
async def list_my_agent_runs(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    limit: int = Query(50, ge=1, le=200),
):
    """Return recent runs owned by the authenticated actor."""
    try:
        return await service.list_my_runs(actor, limit=limit)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get(
    "/agent/tasks/{task_id}/context",
    response_model=AgentTaskContextResponse,
)
async def get_agent_task_context(
    task_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    assignment_id: Optional[int] = None,
):
    """Return the complete assigned-task brief, dependencies, and timeline."""
    try:
        return await service.get_task_context(
            actor,
            task_id,
            assignment_id=assignment_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post("/agent/me/work/begin", response_model=AgentWorkBeginResponse)
async def begin_my_agent_work(
    data: AgentWorkBegin,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    """Atomically accept, fence, claim, run, and activate assigned work."""
    try:
        return await service.begin(
            actor,
            data,
            idempotency_key=idempotency_key,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post("/agent/me/work/submit", response_model=AgentWorkTerminalResponse)
async def submit_my_agent_work(
    data: AgentWorkSubmit,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    """Atomically submit evidence, resolve the task, and release assigned work."""
    try:
        return await service.submit(
            actor,
            data,
            idempotency_key=idempotency_key,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post("/agent/me/work/renew", response_model=AgentWorkBeginResponse)
async def renew_my_agent_work(
    data: AgentWorkRenew,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    """Renew the current assignment fence and run heartbeat atomically."""
    try:
        return await service.renew_work(
            actor,
            data,
            idempotency_key=idempotency_key,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post("/agent/me/work/fail", response_model=AgentWorkTerminalResponse)
async def fail_my_agent_work(
    data: AgentWorkTerminal,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    """Atomically finish failed/canceled work and signal PM recovery."""
    try:
        return await service.fail(
            actor,
            data,
            idempotency_key=idempotency_key,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get("/agent/me/reviews", response_model=AgentReviewQueueResponse)
async def get_my_agent_reviews(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    limit: int = Query(50, ge=1, le=200),
    cursor: Optional[str] = None,
):
    """Return verification-purpose assignments for the authenticated actor."""
    try:
        return await service.get_reviews(actor, limit=limit, cursor=cursor)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post(
    "/agent/me/reviews/verdict",
    response_model=AgentReviewVerdictResponse,
)
async def submit_my_agent_review_verdict(
    data: AgentReviewVerdict,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
):
    """Apply an independent pass/reject verdict and optional rework handoff."""
    try:
        return await service.review(
            actor,
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.get("/agent/recovery", response_model=AgentRecoveryListResponse)
async def list_agent_recovery_tasks(
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    limit: int = Query(50, ge=1, le=200),
    cursor: Optional[str] = None,
):
    """Return typed recovery diagnoses and exact optimistic ownership tuples."""
    try:
        return await service.list_recovery_tasks(actor, limit=limit, cursor=cursor)
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post(
    "/agent/recovery/{task_id}/requeue",
    response_model=AgentRecoveryRequeueResponse,
)
async def requeue_agent_recovery_task(
    task_id: int,
    data: AgentRecoveryRequeue,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
):
    """Reconcile stale execution ownership and dispatch ordered recovery work."""
    try:
        return await service.requeue_recovery(
            actor,
            task_id,
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post(
    "/agent/projects/{project_id}/updates",
    response_model=AgentProjectUpdateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_project_update(
    project_id: int,
    data: AgentProjectUpdateCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    rationale: Annotated[str, Header(alias="X-Agent-Rationale")],
    correlation_id: Annotated[str, Header(alias="X-Correlation-ID")],
):
    """Append an evidence-backed project update with agent attribution."""
    try:
        return await service.create_project_update(
            actor,
            project_id,
            data,
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post(
    "/agent/discoveries",
    response_model=AgentDiscoveryTriageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def report_agent_discovery(
    data: AgentDiscoveryTriageCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentWorkService, Depends(get_agent_work_service)],
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
):
    """Report claim-bound out-of-scope work to PM-controlled Triage."""
    try:
        return await service.report_discovery(
            actor,
            data,
            idempotency_key=idempotency_key,
        )
    except Exception as exc:
        _handle_agent_error(exc, structured=True)


@router.post("/agent/tasks/{task_id}/claim", response_model=TaskClaimResponse)
async def claim_task(
    task_id: int,
    data: TaskClaimRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Claim a task lease."""
    try:
        task = await service.claim_task(task_id, actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _claim_response(service, task)


@router.post("/agent/tasks/{task_id}/renew", response_model=TaskClaimResponse)
async def renew_task_claim(
    task_id: int,
    data: TaskClaimRequest,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Renew a task lease."""
    try:
        task = await service.renew_claim(task_id, actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return _claim_response(service, task)


@router.post("/agent/tasks/{task_id}/release", response_model=TaskResponse)
async def release_task_claim(
    task_id: int,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Release a task lease."""
    try:
        task = await service.release_claim(task_id, actor, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return service.task_service.task_to_response(task)


@router.post(
    "/agent/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_task(
    iteration_id: int,
    data: AgentTaskCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Create a task on behalf of an agent."""
    try:
        task = await service.create_task(iteration_id, actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    return task


@router.patch("/agent/tasks/{task_id}", response_model=TaskResponse)
async def patch_agent_task(
    task_id: int,
    data: AgentTaskPatch,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Patch a task with optimistic concurrency."""
    try:
        task = await service.patch_task(task_id, actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("/agent/tasks/{task_id}/events", response_model=TaskEventResponse)
async def append_task_event(
    task_id: int,
    data: TaskEventCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Append a task checkpoint/progress event."""
    try:
        event = await service.append_task_event(task_id, actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskEventResponse(
        id=event.id,
        task_id=event.task_id,
        actor_type=event.actor_type,
        actor_id=event.actor_id,
        event_type=event.event_type,
        payload=service.event_to_payload(event.payload),
        trace_id=event.trace_id,
        span_id=event.span_id,
        correlation_id=event.correlation_id,
        idempotency_key=event.idempotency_key,
        created_at=event.created_at,
    )


@router.post(
    "/agent/runs",
    response_model=AgentRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_agent_run(
    data: AgentRunCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
    idempotency_key: Annotated[Optional[str], Header(alias="Idempotency-Key")] = None,
):
    """Start an agent run trace."""
    try:
        run = await service.start_run(actor, data, idempotency_key)
    except Exception as exc:
        _handle_agent_error(exc)
    return _run_response(service, run)


@router.post("/agent/runs/{run_id}/events", response_model=AgentRunEventResponse)
async def append_agent_run_event(
    run_id: int,
    data: AgentRunEventCreate,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
):
    """Append an event to an agent run."""
    try:
        event = await service.append_run_event(run_id, actor, data)
    except Exception as exc:
        _handle_agent_error(exc)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return AgentRunEventResponse(
        id=event.id,
        run_id=event.run_id,
        event_type=event.event_type,
        message=event.message,
        payload=service.event_to_payload(event.payload),
        trace_id=event.trace_id,
        span_id=event.span_id,
        correlation_id=event.correlation_id,
        idempotency_key=event.idempotency_key,
        created_at=event.created_at,
    )


@router.post("/agent/runs/{run_id}/finish", response_model=AgentRunResponse)
async def finish_agent_run(
    run_id: int,
    data: AgentRunFinish,
    actor: Annotated[AgentActor, Depends(get_agent_actor)],
    service: Annotated[AgentService, Depends(get_agent_service)],
):
    """Finish an agent run trace."""
    try:
        run = await service.finish_run(run_id, actor, data)
    except Exception as exc:
        _handle_agent_error(exc)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return _run_response(service, run)


def _run_response(service: AgentService, run) -> AgentRunResponse:
    return AgentRunResponse(
        id=run.id,
        task_id=run.task_id,
        actor_id=run.actor_id,
        assignment_id=run.assignment_id,
        claim_generation=run.claim_generation,
        status=run.status,
        trace_id=run.trace_id,
        model_binding_id=run.model_binding_id,
        model_binding_revision=run.model_binding_revision,
        configured_model_alias=run.configured_model_alias,
        resolved_model_id=run.resolved_model_id,
        model=run.model,
        tool_name=run.tool_name,
        metadata=service.event_to_payload(run.run_metadata),
        artifact_links=service.list_to_payload(run.artifact_links),
        commit_url=run.commit_url,
        pr_url=run.pr_url,
        summary=run.summary,
        error=run.error,
        started_at=run.started_at,
        ended_at=run.ended_at,
        heartbeat_at=run.heartbeat_at,
    )


def _run_detail_response(service: AgentService, run) -> AgentRunDetailResponse:
    events = [
        AgentRunEventResponse(
            id=evt.id,
            run_id=evt.run_id,
            event_type=evt.event_type,
            message=evt.message,
            payload=service.event_to_payload(evt.payload),
            trace_id=evt.trace_id,
            span_id=evt.span_id,
            correlation_id=evt.correlation_id,
            idempotency_key=evt.idempotency_key,
            created_at=evt.created_at,
        )
        for evt in run.events
    ]
    return AgentRunDetailResponse(
        id=run.id,
        task_id=run.task_id,
        actor_id=run.actor_id,
        assignment_id=run.assignment_id,
        claim_generation=run.claim_generation,
        status=run.status,
        trace_id=run.trace_id,
        model=run.model,
        tool_name=run.tool_name,
        metadata=service.event_to_payload(run.run_metadata),
        artifact_links=service.list_to_payload(run.artifact_links),
        commit_url=run.commit_url,
        pr_url=run.pr_url,
        summary=run.summary,
        error=run.error,
        started_at=run.started_at,
        ended_at=run.ended_at,
        heartbeat_at=run.heartbeat_at,
        events=events,
    )


@router.get("/agent/pipeline", response_model=AgentPipelineResponse)
async def get_agent_pipeline(
    service: Annotated[AgentService, Depends(get_agent_service)],
    _: Annotated[None, Depends(require_agent_read_access)],
):
    """Retrieve all current tasks grouped by their agent pipeline columns."""
    cols = await service.get_pipeline()
    return AgentPipelineResponse(
        needs_definition=cols["needs_definition"],
        ready_for_agent=cols["ready_for_agent"],
        definition_ready_unassigned=cols.get("definition_ready_unassigned", []),
        assigned_waiting=cols.get("assigned_waiting", []),
        start_ready=cols.get("start_ready", []),
        executing=cols["executing"],
        verification_required=cols["verification_required"],
        recovery_required=cols.get("recovery_required", []),
    )


@router.get("/agent/runs/{run_id}", response_model=AgentRunDetailResponse)
async def get_agent_run_detail(
    run_id: int,
    service: Annotated[AgentService, Depends(get_agent_service)],
    _: Annotated[None, Depends(require_agent_read_access)],
):
    """Get the full details of an agent run including chronological trace events."""
    run = await service.get_run(run_id)
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent run not found")
    return _run_detail_response(service, run)
