"""Framework-neutral MCP tool handlers for agent task access.

These functions intentionally delegate to domain services so REST and MCP use
the same audited command and read-model paths.
"""
import asyncio
import hashlib
import json
import os
import secrets
import tomllib
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
from typing import Any, Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent_contract import agent_contract_features
from app.config import get_settings
from app.models.agent import AgentActor, AgentIdempotencyRecord
from app.schemas.agent import (
    AgentCapabilitiesResponse,
    AgentDiscoveryTriageCreate,
    AgentProjectUpdateCreate,
    AgentRecoveryRequeue,
    AgentReviewVerdict,
    AgentRunDetailResponse,
    AgentRunCreate,
    AgentRunEventResponse,
    AgentRunEventCreate,
    AgentRunFinish,
    AgentTaskAssignmentCreate,
    AgentTaskAssignmentUpdate,
    AgentTaskCreate,
    AgentTaskPatch,
    AgentWorkBegin,
    AgentWorkRenew,
    AgentWorkSubmit,
    AgentWorkTerminal,
    TaskClaimRequest,
    TaskEventCreate,
)
from app.schemas.agent_planning import (
    AgentPlanningCommandContext,
    AgentScheduleCommand,
)
from app.schemas.agent_routing import (
    AgentModelBindingCreate,
    AgentModelBindingDisable,
    AgentModelBindingUpdate,
    AgentModelCatalogCreate,
    AgentModelCatalogDisable,
    AgentModelCatalogUpdate,
)
from app.schemas.agent_skill_bundle import (
    SkillBundleCatalogResponse,
    SkillBundleManifestResponse,
)
from app.schemas.iteration import IterationCreate, IterationSummary, IterationUpdate
from app.schemas.label import LabelGroupResponse, LabelResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneResponse,
    ProjectMilestoneUpdate,
    ProjectResponse,
    ProjectUpdate,
    ProjectUpdateEntryResponse,
)
from app.schemas.release import ReleaseResponse
from app.schemas.request_source import (
    RequestSourceLinkCreateRequest,
    RequestSourceLinkWithSourceResponse,
    RequestSourceResponse,
)
from app.schemas.saved_view import SavedViewType
from app.schemas.system_settings import SystemSettingsResponse
from app.schemas.template import TemplateType, WorkTemplateResponse
from app.schemas.team import (
    MemberCapacity,
    MemberWorkload,
    TeamMemberProfileResponse,
    TeamMemberProfileCreate,
    TeamMemberProfileUpdate,
    TeamMemberCreate,
    TeamMemberResponse,
    TeamMemberUpdate,
    VacationCreate,
    VacationResponse,
    VacationUpdate,
)
from app.schemas.triage import (
    TriageActionRequest,
    TriageClassificationSuggestionResponse,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageItemCreate,
    TriageItemResponse,
    TriageItemStatus,
    TriageItemUpdate,
    TriageSnoozeRequest,
    TriageTaskDraftRequest,
)
from app.services.agent_profile_catalog_service import AgentProfileCatalogService
from app.services.agent_model_catalog_service import AgentModelCatalogService
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_service import (
    AgentConflictError,
    AgentService,
    actor_has_scope,
    actor_scopes,
    validate_idempotency_key,
)
from app.services.agent_skill_bundle_service import (
    AgentSkillBundleService,
    SkillBundleArtifactError,
    SkillBundleNotFoundError,
)
from app.services.agent_work_service import AgentWorkService
from app.services.assignee_recommendation_service import AssigneeRecommendationService
from app.services.external_link_service import ExternalLinkService
from app.services.iteration_service import IterationService
from app.services.label_service import LabelService
from app.services.project_service import ProjectService
from app.services.release_service import ReleaseService
from app.services.request_source_service import (
    RequestSourceConflictError,
    RequestSourceService,
)
from app.services.saved_view_service import SavedViewService
from app.services.system_settings_service import RuntimeSettingsService
from app.services.task_context_revision_service import (
    TaskContextVersionConflictError,
    lock_task_context,
)
from app.services.task_service import TaskService
from app.services.template_service import TemplateService
from app.services.team_service import TeamService
from app.services.triage_service import TriageConflictError, TriageService


AGENT_SKILLS_DIR_ENV = "WORKCHORD_AGENT_SKILLS_DIR"
AGENT_SKILL_ARTIFACTS_DIR_ENV = "WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR"
REQUEST_SOURCE_WRITE_MAX_ATTEMPTS = 6
def _dump(value: Any) -> Any:
    """Convert Pydantic, SQLAlchemy-ish, and nested values to JSON-safe data."""
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list | tuple):
        return [_dump(item) for item in value]
    if isinstance(value, dict):
        return {key: _dump(item) for key, item in value.items()}
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _response(schema: type[BaseModel], value: Any) -> dict[str, Any]:
    """Validate an ORM/service result into a JSON-safe schema response."""
    return schema.model_validate(value).model_dump(mode="json")


def _responses(schema: type[BaseModel], values: Sequence[Any]) -> list[dict[str, Any]]:
    """Validate a sequence of ORM/service results into JSON-safe responses."""
    return [_response(schema, value) for value in values]


def _triage_command_request_hash(payload: dict[str, Any]) -> str:
    """Return a stable fingerprint for a validated MCP triage command."""
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _triage_command_context(
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> AgentPlanningCommandContext:
    """Validate complete audit metadata for one durable triage command."""
    key = validate_idempotency_key(idempotency_key, required=True)
    assert key is not None
    return AgentPlanningCommandContext(
        idempotency_key=key,
        rationale=rationale,
        correlation_id=correlation_id,
    )


def _triage_audited_request(
    command: AgentPlanningCommandContext,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Bind one triage payload fingerprint to its decision context."""
    return {
        "command": {
            "rationale": command.rationale,
            "correlation_id": command.correlation_id,
        },
        "payload": payload,
    }


async def _triage_command_replay(
    db: AsyncSession,
    *,
    actor_id: int,
    operation: str,
    target_type: str,
    target_id: int,
    idempotency_key: str,
    request_payload: dict[str, Any],
) -> dict[str, Any] | None:
    """Return an exact durable receipt or reject non-identical key reuse."""
    result = await db.execute(
        select(AgentIdempotencyRecord).where(
            AgentIdempotencyRecord.actor_id == actor_id,
            AgentIdempotencyRecord.operation == operation,
            AgentIdempotencyRecord.target_type == target_type,
            AgentIdempotencyRecord.target_id == target_id,
            AgentIdempotencyRecord.idempotency_key == idempotency_key,
        )
    )
    record = result.scalar_one_or_none()
    if record is None:
        return None
    request_hash = _triage_command_request_hash(request_payload)
    if not secrets.compare_digest(record.request_hash, request_hash):
        raise AgentConflictError("idempotency_mismatch")
    try:
        receipt = json.loads(record.response_payload)
        response = receipt["response"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise AgentConflictError("Idempotent triage command receipt is invalid") from exc
    if not isinstance(response, dict):
        raise AgentConflictError("Idempotent triage command receipt is invalid")
    return response


def _stage_triage_command_receipt(
    db: AsyncSession,
    *,
    actor_id: int,
    operation: str,
    target_type: str,
    target_id: int,
    idempotency_key: str,
    request_payload: dict[str, Any],
    response: dict[str, Any],
    command: AgentPlanningCommandContext | None = None,
) -> None:
    """Stage an actor-attributed exact response in the mutation transaction."""
    receipt: dict[str, Any] = {"response": response}
    if command is not None:
        receipt["audit"] = {
            "actor_id": actor_id,
            "operation": operation,
            "target_type": target_type,
            "target_id": target_id,
            "idempotency_key": idempotency_key,
            "rationale": command.rationale,
            "correlation_id": command.correlation_id,
        }
    db.add(
        AgentIdempotencyRecord(
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            idempotency_key=idempotency_key,
            request_hash=_triage_command_request_hash(request_payload),
            response_payload=json.dumps(
                receipt,
                sort_keys=True,
            ),
        )
    )


async def _stage_triage_command_audit_event(
    db: AsyncSession,
    *,
    actor: AgentActor,
    operation: str,
    triage_item_id: int,
    command: AgentPlanningCommandContext,
) -> None:
    """Append one actor-attributed triage decision to the shared audit ledger."""
    await TaskService(db).record_task_event(
        None,
        "agent_triage_command",
        {
            "operation": operation,
            "triage_item_id": triage_item_id,
            "rationale": command.rationale,
        },
        actor_type="agent",
        actor_id=actor.id,
        correlation_id=command.correlation_id,
        idempotency_key=command.idempotency_key,
    )


async def _stage_context_command_audit_event(
    db: AsyncSession,
    *,
    actor: AgentActor,
    operation: str,
    target_type: str,
    target_id: int,
    command: AgentPlanningCommandContext,
    task_id: int | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    """Append one actor-attributed PM context decision in the mutation transaction."""
    await TaskService(db).record_task_event(
        task_id,
        f"agent_{operation.replace('.', '_')}",
        {
            "operation": operation,
            "target_type": target_type,
            "target_id": target_id,
            "rationale": command.rationale,
            "details": details or {},
        },
        actor_type="agent",
        actor_id=actor.id,
        correlation_id=command.correlation_id,
        idempotency_key=command.idempotency_key,
    )


async def _commit_triage_command(
    db: AsyncSession,
    *,
    actor_id: int,
    operation: str,
    target_type: str,
    target_id: int,
    idempotency_key: str,
    request_payload: dict[str, Any],
    response: dict[str, Any],
) -> dict[str, Any]:
    """Commit mutation and receipt together, recovering a concurrent exact replay."""
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        replay = await _triage_command_replay(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            idempotency_key=idempotency_key,
            request_payload=request_payload,
        )
        if replay is None:
            raise
        return replay
    return response


async def _mutate_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    *,
    operation: str,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
    data: BaseModel,
    service_method: str,
) -> dict[str, Any] | None:
    """Lock, mutate, and store one exact actor-attributed triage receipt."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    request_payload = _triage_audited_request(
        command,
        {
            "triage_item_id": triage_item_id,
            "payload": data.model_dump(mode="json", exclude_unset=True),
        },
    )
    replay = await _triage_command_replay(
        db,
        actor_id=actor.id,
        operation=operation,
        target_type="triage_item",
        target_id=triage_item_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay

    service = TriageService(db)
    try:
        item = await service.get_by_id(triage_item_id, for_update=True)
        if item is None:
            await db.rollback()
            return None
        replay = await _triage_command_replay(
            db,
            actor_id=actor.id,
            operation=operation,
            target_type="triage_item",
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
        )
        if replay is not None:
            await db.rollback()
            return replay
        mutate = getattr(service, service_method)
        item = await mutate(triage_item_id, data, commit=False)
        if item is None:  # pragma: no cover - protected by locked read
            await db.rollback()
            return None
        response = _response(TriageItemResponse, item)
        await _stage_triage_command_audit_event(
            db,
            actor=actor,
            operation=operation,
            triage_item_id=triage_item_id,
            command=command,
        )
        _stage_triage_command_receipt(
            db,
            actor_id=actor.id,
            operation=operation,
            target_type="triage_item",
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
            command=command,
        )
        return await _commit_triage_command(
            db,
            actor_id=actor.id,
            operation=operation,
            target_type="triage_item",
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
        )
    except Exception:
        await db.rollback()
        raise


def _iteration_project_payload(iteration: Any) -> dict[str, Any] | None:
    """Return compact project scope metadata for an iteration payload."""
    if iteration.project is None:
        return None
    return {
        "id": iteration.project.id,
        "name": iteration.project.name,
        "status": iteration.project.status,
        "health": iteration.project.health,
    }


def _server_version() -> str:
    """Return the installed backend package version without importing the ASGI app."""
    try:
        return package_version("workchord-backend")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        try:
            with pyproject.open("rb") as stream:
                return str(tomllib.load(stream)["project"]["version"])
        except (OSError, KeyError, TypeError, tomllib.TOMLDecodeError):
            return "unknown"


def _agent_skill_bundle_service() -> AgentSkillBundleService:
    """Return the same validated deployed-release service used by REST."""
    configured = os.getenv(AGENT_SKILL_ARTIFACTS_DIR_ENV) or os.getenv(
        AGENT_SKILLS_DIR_ENV
    )
    return AgentSkillBundleService(Path(configured).expanduser() if configured else None)


def _skill_resource_error(exc: Exception) -> LookupError:
    """Hide deployment paths while preserving a stable MCP not-found boundary."""
    if isinstance(exc, SkillBundleNotFoundError):
        return LookupError("Agent skill version or file was not found")
    return LookupError("Validated agent skill artifacts are unavailable")


async def get_agent_skill_catalog() -> dict[str, Any]:
    """MCP resource handler: return the validated deployed skill catalog."""
    try:
        payload = _agent_skill_bundle_service().catalog_payload()
        return SkillBundleCatalogResponse.model_validate_json(payload.content).model_dump(
            mode="json"
        )
    except (SkillBundleArtifactError, SkillBundleNotFoundError, ValueError) as exc:
        raise _skill_resource_error(exc) from exc


async def get_agent_skill_manifest(
    skill_name: str,
    skill_version: str,
) -> dict[str, Any]:
    """MCP resource handler: return one validated exact-version manifest."""
    try:
        payload = _agent_skill_bundle_service().manifest_payload(
            skill_name, skill_version
        )
        return SkillBundleManifestResponse.model_validate_json(
            payload.content
        ).model_dump(mode="json")
    except (SkillBundleArtifactError, SkillBundleNotFoundError, ValueError) as exc:
        raise _skill_resource_error(exc) from exc


async def get_agent_skill_file(
    skill_name: str,
    skill_version: str,
    requested_path: str,
) -> str:
    """Return one UTF-8 allow-listed file from the validated release archive."""
    try:
        content = _agent_skill_bundle_service().file_payload(
            skill_name, skill_version, requested_path
        ).content
    except (SkillBundleArtifactError, SkillBundleNotFoundError, ValueError) as exc:
        raise _skill_resource_error(exc) from exc
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LookupError("Agent skill file is not UTF-8") from exc


async def get_agent_skill_entrypoint(
    skill_name: str,
    skill_version: str,
) -> str:
    """MCP resource handler: return the validated exact-version SKILL.md."""
    return await get_agent_skill_file(skill_name, skill_version, "SKILL.md")


async def get_agent_skill_reference(
    skill_name: str,
    skill_version: str,
    reference_name: str,
) -> str:
    """Return one direct Markdown reference from a validated role archive."""
    if (
        not reference_name.endswith(".md")
        or "/" in reference_name
        or "\\" in reference_name
        or reference_name in {".", ".."}
    ):
        raise LookupError("Agent skill reference was not found")
    return await get_agent_skill_file(
        skill_name, skill_version, f"references/{reference_name}"
    )


async def list_iterations(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: list iterations."""
    iterations = await IterationService(db).get_all()
    return [
        {
            "id": iteration.id,
            "name": iteration.name,
            "project_id": iteration.project_id,
            "project": _iteration_project_payload(iteration),
            "start_date": iteration.start_date.isoformat(),
            "end_date": iteration.end_date.isoformat(),
        }
        for iteration in iterations
    ]


async def get_iteration(db: AsyncSession, iteration_id: int) -> dict[str, Any] | None:
    """MCP handler: get one iteration."""
    iteration = await IterationService(db).get_by_id(iteration_id)
    if not iteration:
        return None
    return {
        "id": iteration.id,
        "name": iteration.name,
        "calendar_id": iteration.calendar_id,
        "project_id": iteration.project_id,
        "project": _iteration_project_payload(iteration),
        "start_date": iteration.start_date.isoformat(),
        "end_date": iteration.end_date.isoformat(),
        "manager_email": iteration.manager_email,
    }


async def get_iteration_summary(
    db: AsyncSession,
    iteration_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return the vacation-aware iteration summary."""
    summary = await IterationService(db).get_summary(iteration_id)
    return _response(IterationSummary, summary) if summary else None


async def get_iteration_gantt(
    db: AsyncSession,
    iteration_id: int,
) -> dict[str, Any]:
    """MCP handler: return the existing read-only Gantt projection."""
    # Gantt assembly currently lives in the REST adapter rather than a service.
    # Call that implementation so MCP cannot drift by rebuilding schedule math.
    from app.routers.gantt import get_gantt_data

    if await IterationService(db).get_by_id(iteration_id) is None:
        raise LookupError("Iteration not found")
    return _dump(await get_gantt_data(iteration_id, db))


async def list_team_member_profiles(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: list reusable profiles with their advisory skills."""
    profiles = await TeamService(db).list_profiles()
    return _responses(TeamMemberProfileResponse, profiles)


async def get_team_member_profile(
    db: AsyncSession,
    profile_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return one reusable profile with its skills."""
    profile = await TeamService(db).get_profile(profile_id)
    return _response(TeamMemberProfileResponse, profile) if profile else None


async def list_iteration_team(
    db: AsyncSession,
    iteration_id: int,
) -> list[dict[str, Any]]:
    """MCP handler: list iteration capacity owners, profiles, and vacations."""
    members = await TeamService(db).get_by_iteration(iteration_id)
    return _responses(TeamMemberResponse, members)


async def get_team_member_capacity(
    db: AsyncSession,
    member_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return vacation-aware capacity for one iteration member."""
    capacity = await TeamService(db).calculate_capacity(member_id)
    return _response(MemberCapacity, capacity) if capacity else None


async def get_team_member_workload(
    db: AsyncSession,
    member_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return allocated and free capacity for one member."""
    workload = await TeamService(db).get_workload(member_id)
    return _response(MemberWorkload, workload) if workload else None


async def list_team_member_vacations(
    db: AsyncSession,
    member_id: int,
) -> list[dict[str, Any]] | None:
    """MCP handler: return vacation periods for one iteration member."""
    member = await TeamService(db).get_by_id(member_id)
    if member is None:
        return None
    return _responses(VacationResponse, member.vacations)


async def get_profile_skill_catalog(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: return code-owned advisory capability definitions."""
    return AgentProfileCatalogService(db).catalog()


async def get_agent_profile_presets(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: return reusable agent profile presets."""
    return AgentProfileCatalogService(db).presets()


async def get_agent_routes(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: return the explainable, non-authorizing route index."""
    return AgentProfileCatalogService(db).routes()


async def apply_agent_profile_preset(
    db: AsyncSession,
    actor: AgentActor,
    preset_key: str,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: apply a preset with an exact actor-attributed receipt."""
    command = AgentPlanningCommandContext(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    receipt = await AgentPlanningService(db).apply_profile_preset(
        preset_key,
        actor,
        command=command,
    )
    return receipt.result


def _planning_command_context(
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> AgentPlanningCommandContext:
    """Build the common validated MCP PM-command audit context."""
    return AgentPlanningCommandContext(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )


async def create_planning_project(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one project through the audited PM adapter."""
    receipt = await AgentPlanningService(db).create_project(
        actor,
        ProjectCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_project(
    db: AsyncSession,
    actor: AgentActor,
    project_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one project through the audited PM adapter."""
    receipt = await AgentPlanningService(db).update_project(
        project_id,
        actor,
        ProjectUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_milestone(
    db: AsyncSession,
    actor: AgentActor,
    project_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one audited project milestone."""
    receipt = await AgentPlanningService(db).create_milestone(
        project_id,
        actor,
        ProjectMilestoneCreateRequest.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_milestone(
    db: AsyncSession,
    actor: AgentActor,
    project_id: int,
    milestone_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one audited project-scoped milestone."""
    receipt = await AgentPlanningService(db).update_milestone(
        project_id,
        milestone_id,
        actor,
        ProjectMilestoneUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def delete_planning_milestone(
    db: AsyncSession,
    actor: AgentActor,
    project_id: int,
    milestone_id: int,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: delete one audited project-scoped milestone."""
    receipt = await AgentPlanningService(db).delete_milestone(
        project_id,
        milestone_id,
        actor,
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_task(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one task through the audited decomposition adapter."""
    receipt = await AgentPlanningService(db).create_task(
        iteration_id,
        actor,
        AgentTaskCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def patch_planning_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: patch one task through the audited decomposition adapter."""
    receipt = await AgentPlanningService(db).patch_task(
        task_id,
        actor,
        AgentTaskPatch.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_iteration(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one iteration through the audited PM adapter."""
    receipt = await AgentPlanningService(db).create_iteration(
        actor,
        IterationCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_iteration(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one iteration through the audited PM adapter."""
    receipt = await AgentPlanningService(db).update_iteration(
        iteration_id,
        actor,
        IterationUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_profile(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one reusable team profile."""
    receipt = await AgentPlanningService(db).create_profile(
        actor,
        TeamMemberProfileCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_profile(
    db: AsyncSession,
    actor: AgentActor,
    profile_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one reusable team profile."""
    receipt = await AgentPlanningService(db).update_profile(
        profile_id,
        actor,
        TeamMemberProfileUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_team_member(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: add one capacity owner to an iteration."""
    receipt = await AgentPlanningService(db).create_team_member(
        iteration_id,
        actor,
        TeamMemberCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_team_member(
    db: AsyncSession,
    actor: AgentActor,
    member_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one iteration capacity owner."""
    receipt = await AgentPlanningService(db).update_team_member(
        member_id,
        actor,
        TeamMemberUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_planning_vacation(
    db: AsyncSession,
    actor: AgentActor,
    member_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: add one validated vacation period."""
    receipt = await AgentPlanningService(db).create_vacation(
        member_id,
        actor,
        VacationCreate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_planning_vacation(
    db: AsyncSession,
    actor: AgentActor,
    vacation_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one validated vacation period."""
    receipt = await AgentPlanningService(db).update_vacation(
        vacation_id,
        actor,
        VacationUpdate.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def preview_planning_schedule(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: preview schedule changes in a rolled-back savepoint."""
    receipt = await AgentPlanningService(db).preview_schedule(
        iteration_id,
        actor,
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def apply_planning_schedule(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: apply a schedule using exact task-version tokens."""
    receipt = await AgentPlanningService(db).apply_schedule(
        iteration_id,
        actor,
        AgentScheduleCommand.model_validate(payload),
        command=_planning_command_context(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def search_tasks(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: Optional[int] = None,
    query: Optional[str] = None,
) -> list[dict[str, Any]]:
    """MCP handler: search tasks by title/description."""
    service = AgentService(db)
    tasks = await service.list_ready_tasks(actor, iteration_id=iteration_id, limit=200)
    query_lower = query.lower() if query else None
    if query_lower:
        tasks = [
            task for task in tasks
            if query_lower in task.title.lower()
            or (task.description and query_lower in task.description.lower())
        ]
    return [
        service.task_service.task_to_response(task).model_dump(mode="json")
        for task in tasks
    ]


async def get_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
) -> dict[str, Any] | None:
    """MCP handler: get task details."""
    service = AgentService(db)
    task = await service.task_service.get_by_id(task_id)
    return service.task_service.task_to_response(task).model_dump(mode="json") if task else None


async def get_task_context(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return task plus timeline context."""
    service = AgentService(db)
    task = await service.task_service.get_by_id(task_id)
    if not task:
        return None
    timeline = await service.get_task_timeline(task_id)
    return {
        "task": service.task_service.task_to_response(task).model_dump(mode="json"),
        "timeline": timeline,
    }


async def get_agent_capabilities(
    db: AsyncSession,
    actor: AgentActor,
) -> dict[str, Any]:
    """MCP handler: return the authenticated v1 compatibility handshake."""
    recommended: dict[str, str] = {}
    catalog_version: str | None = None
    features = agent_contract_features(include_skill_bundles=False)
    catalog_url: str | None = None
    discovery_url: str | None = None
    settings = get_settings()
    if settings.agent_skill_bundles_public or actor_has_scope(actor, "skills:read"):
        try:
            catalog = SkillBundleCatalogResponse.model_validate(
                await get_agent_skill_catalog()
            )
            catalog_version = catalog.catalog_version
            for entry in catalog.skills:
                recommended[entry.role] = f"{entry.name}@{entry.version}"
            features.append("skill-bundles-v1")
            catalog_url = f"{settings.api_prefix.rstrip('/')}/agent/skill-bundles"
            discovery_url = "/.well-known/workchord-agent-skills.json"
        except LookupError:
            # The authenticated runtime contract remains useful when optional
            # release artifacts were not copied into this deployment.
            recommended = {}
    service = AgentWorkService(db)
    response = AgentCapabilitiesResponse(
        server_version=_server_version(),
        api_contract="workchord-agent/v1",
        actor=service.actor_response(actor),
        scopes=actor_scopes(actor),
        lease_limits={
            "minimum_seconds": 60,
            "default_seconds": 3600,
            "maximum_seconds": 86400,
        },
        features=features,
        recommended_skills=recommended,
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
    return response.model_dump(mode="json")


async def list_agent_actor_roster(
    db: AsyncSession,
    actor: AgentActor,
    *,
    include_disabled: bool = False,
) -> list[dict[str, Any]]:
    """MCP handler: return secret-free enabled actor dispatch metadata."""
    return _dump(
        await AgentWorkService(db).list_actor_roster(
            actor,
            include_disabled=include_disabled,
        )
    )


async def list_agent_model_catalog(
    db: AsyncSession,
    actor: AgentActor,
    *,
    include_disabled: bool = False,
) -> list[dict[str, Any]]:
    """MCP handler: list provider-neutral secret-free model declarations."""

    return _dump(
        await AgentModelCatalogService(db).list_catalog(
            actor,
            include_disabled=include_disabled,
        )
    )


async def get_agent_model_catalog_entry(
    db: AsyncSession,
    actor: AgentActor,
    catalog_key: str,
) -> dict[str, Any]:
    """MCP handler: read one stable model catalog entry."""

    return _dump(
        await AgentModelCatalogService(db).get_catalog(
            actor,
            catalog_key.strip().lower(),
        )
    )


async def list_agent_model_bindings(
    db: AsyncSession,
    actor: AgentActor,
    *,
    actor_id: int | None = None,
    include_disabled: bool = False,
) -> list[dict[str, Any]]:
    """MCP handler: list secret-free actor model bindings."""

    return _dump(
        await AgentModelCatalogService(db).list_bindings(
            actor,
            actor_id=actor_id,
            include_disabled=include_disabled,
        )
    )


async def get_agent_model_binding(
    db: AsyncSession,
    actor: AgentActor,
    binding_id: int,
) -> dict[str, Any]:
    """MCP handler: read one current or historical model binding."""

    return _dump(
        await AgentModelCatalogService(db).get_binding(actor, binding_id)
    )


def _model_command(
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> AgentPlanningCommandContext:
    return AgentPlanningCommandContext(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )


async def create_agent_model_catalog_entry(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: create one operator-owned model declaration."""

    receipt = await AgentModelCatalogService(db).create_catalog(
        actor,
        AgentModelCatalogCreate.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_agent_model_catalog_entry(
    db: AsyncSession,
    actor: AgentActor,
    catalog_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one model declaration behind its revision."""

    receipt = await AgentModelCatalogService(db).update_catalog(
        catalog_id,
        actor,
        AgentModelCatalogUpdate.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def disable_agent_model_catalog_entry(
    db: AsyncSession,
    actor: AgentActor,
    catalog_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: soft-disable one model declaration."""

    receipt = await AgentModelCatalogService(db).disable_catalog(
        catalog_id,
        actor,
        AgentModelCatalogDisable.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_agent_model_binding(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: bind an actor to one catalog entry."""

    receipt = await AgentModelCatalogService(db).create_binding(
        actor,
        AgentModelBindingCreate.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def update_agent_model_binding(
    db: AsyncSession,
    actor: AgentActor,
    binding_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: update one actor binding behind its revision."""

    receipt = await AgentModelCatalogService(db).update_binding(
        binding_id,
        actor,
        AgentModelBindingUpdate.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def disable_agent_model_binding(
    db: AsyncSession,
    actor: AgentActor,
    binding_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: soft-disable one actor binding."""

    receipt = await AgentModelCatalogService(db).disable_binding(
        binding_id,
        actor,
        AgentModelBindingDisable.model_validate(payload),
        command=_model_command(
            idempotency_key=idempotency_key,
            rationale=rationale,
            correlation_id=correlation_id,
        ),
    )
    return receipt.model_dump(mode="json")


async def create_agent_assignment(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: Optional[str] = None,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: dispatch one task to an exact actor."""
    service = AgentWorkService(db)
    assignment = await service.create_assignment(
        actor,
        AgentTaskAssignmentCreate(**payload),
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    return assignment.model_dump(mode="json")


async def list_agent_assignments(
    db: AsyncSession,
    actor: AgentActor,
    *,
    task_id: Optional[int] = None,
    actor_id: Optional[int] = None,
    purpose: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    """MCP handler: list durable assignments within the authorized queue boundary."""
    assignments = await AgentWorkService(db).list_assignments(
        actor,
        task_id=task_id,
        actor_id=actor_id,
        purpose=purpose,
        state=state,
        limit=limit,
    )
    return [assignment.model_dump(mode="json") for assignment in assignments]


async def update_agent_assignment(
    db: AsyncSession,
    actor: AgentActor,
    assignment_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: Optional[str] = None,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: reassign, reorder, defer, or cancel queued work."""
    service = AgentWorkService(db)
    assignment = await service.update_assignment(
        assignment_id,
        actor,
        AgentTaskAssignmentUpdate(**payload),
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    return assignment.model_dump(mode="json")


async def get_my_work(
    db: AsyncSession,
    actor: AgentActor,
    *,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> dict[str, Any]:
    """MCP handler: return the authoritative current/next work decision."""
    decision = await AgentWorkService(db).get_work(actor, limit=limit, cursor=cursor)
    return decision.model_dump(mode="json")


async def list_my_claims(
    db: AsyncSession,
    actor: AgentActor,
) -> list[dict[str, Any]]:
    """MCP handler: list claims currently owned by this actor."""
    return _dump(await AgentWorkService(db).list_my_claims(actor))


async def list_my_runs(
    db: AsyncSession,
    actor: AgentActor,
    *,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """MCP handler: list recent runs owned by this actor."""
    return _dump(await AgentWorkService(db).list_my_runs(actor, limit=limit))


async def get_complete_task_context(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    *,
    assignment_id: Optional[int] = None,
) -> dict[str, Any]:
    """MCP handler: return assignment-bound brief, dependencies, and timeline."""
    context = await AgentWorkService(db).get_task_context(
        actor,
        task_id,
        assignment_id=assignment_id,
    )
    return context.model_dump(mode="json")


async def begin_my_work(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """MCP handler: atomically accept, claim, run, and activate assigned work."""
    result = await AgentWorkService(db).begin(
        actor,
        AgentWorkBegin(**payload),
        idempotency_key=idempotency_key,
    )
    return result.model_dump(mode="json")


async def renew_my_work(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """MCP handler: renew the current assignment fence and run heartbeat."""
    result = await AgentWorkService(db).renew_work(
        actor,
        AgentWorkRenew(**payload),
        idempotency_key=idempotency_key,
    )
    return result.model_dump(mode="json")


async def report_discovery(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """MCP handler: report claim-bound out-of-scope work to Triage."""
    result = await AgentWorkService(db).report_discovery(
        actor,
        AgentDiscoveryTriageCreate(**payload),
        idempotency_key=idempotency_key,
    )
    return result.model_dump(mode="json")


async def submit_my_work(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """MCP handler: atomically submit, resolve, fulfill, and release work."""
    result = await AgentWorkService(db).submit(
        actor,
        AgentWorkSubmit(**payload),
        idempotency_key=idempotency_key,
    )
    return result.model_dump(mode="json")


async def fail_my_work(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
) -> dict[str, Any]:
    """MCP handler: atomically fail/cancel work and signal recovery."""
    result = await AgentWorkService(db).fail(
        actor,
        AgentWorkTerminal(**payload),
        idempotency_key=idempotency_key,
    )
    return result.model_dump(mode="json")


async def get_my_reviews(
    db: AsyncSession,
    actor: AgentActor,
    *,
    limit: int = 50,
    cursor: Optional[str] = None,
) -> dict[str, Any]:
    """MCP handler: return this actor's verification-purpose assignments."""
    result = await AgentWorkService(db).get_reviews(
        actor,
        limit=limit,
        cursor=cursor,
    )
    return result.model_dump(mode="json")


async def submit_review_verdict(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: record an independent pass/reject verdict."""
    result = await AgentWorkService(db).review(
        actor,
        AgentReviewVerdict(**payload),
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    return result.model_dump(mode="json")


async def list_agent_recovery_tasks(
    db: AsyncSession,
    actor: AgentActor,
    *,
    limit: int = 50,
    cursor: Optional[str] = None,
) -> dict[str, Any]:
    """MCP handler: list active tasks with no valid live execution owner."""
    service = AgentWorkService(db)
    result = await service.list_recovery_tasks(
        actor,
        limit=limit,
        cursor=cursor,
    )
    return result.model_dump(mode="json")


async def requeue_agent_recovery(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: reconcile stale ownership and dispatch recovery work."""
    result = await AgentWorkService(db).requeue_recovery(
        actor,
        task_id,
        AgentRecoveryRequeue(**payload),
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    return result.model_dump(mode="json")


async def get_agent_pipeline(
    db: AsyncSession,
    actor: AgentActor,
) -> dict[str, list[dict[str, Any]]]:
    """MCP handler: return the full PM supervision pipeline."""
    pipeline = await AgentService(db).get_pipeline()
    return {
        key: [task.model_dump(mode="json") for task in tasks]
        for key, tasks in pipeline.items()
    }


async def get_agent_run_detail(
    db: AsyncSession,
    actor: AgentActor,
    run_id: int,
) -> dict[str, Any] | None:
    """MCP handler: return one run and its chronological events."""
    service = AgentService(db)
    run = await service.get_run(run_id)
    if run is None:
        return None
    base = AgentWorkService.run_response(run).model_dump()
    events = [
        AgentRunEventResponse(
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
        for event in run.events
    ]
    return AgentRunDetailResponse(**base, events=events).model_dump(mode="json")


async def get_task_timeline(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
) -> list[dict[str, Any]] | None:
    """MCP handler: return only the merged task timeline."""
    context = await get_task_context(db, actor, task_id)
    return context["timeline"] if context else None


async def list_ready_tasks(
    db: AsyncSession,
    actor: AgentActor,
    **filters: Any,
) -> list[dict[str, Any]]:
    """MCP handler: list ready tasks."""
    service = AgentService(db)
    tasks = await service.list_ready_tasks(actor, **filters)
    return [
        service.task_service.task_to_response(task).model_dump(mode="json")
        for task in tasks
    ]


async def claim_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    lease_seconds: int = 3600,
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: claim a task."""
    service = AgentService(db)
    task = await service.claim_task(
        task_id,
        actor,
        TaskClaimRequest(lease_seconds=lease_seconds),
        idempotency_key=idempotency_key,
    )
    return service.task_service.task_to_response(task).model_dump(mode="json") if task else None


async def renew_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    lease_seconds: int = 3600,
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: renew a task claim."""
    service = AgentService(db)
    task = await service.renew_claim(
        task_id,
        actor,
        TaskClaimRequest(lease_seconds=lease_seconds),
        idempotency_key=idempotency_key,
    )
    return service.task_service.task_to_response(task).model_dump(mode="json") if task else None


async def release_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: release a task."""
    service = AgentService(db)
    task = await service.release_claim(task_id, actor, idempotency_key=idempotency_key)
    return service.task_service.task_to_response(task).model_dump(mode="json") if task else None


async def create_task(
    db: AsyncSession,
    actor: AgentActor,
    iteration_id: int,
    payload: dict[str, Any],
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: create a task."""
    service = AgentService(db)
    task = await service.create_task(
        iteration_id,
        actor,
        AgentTaskCreate(**payload),
        idempotency_key=idempotency_key,
    )
    return task.model_dump(mode="json")


async def update_task(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    payload: dict[str, Any],
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: update a task."""
    service = AgentService(db)
    task = await service.patch_task(
        task_id,
        actor,
        AgentTaskPatch(**payload),
        idempotency_key=idempotency_key,
    )
    return task.model_dump(mode="json") if task else None


async def append_task_event(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    payload: dict[str, Any],
    idempotency_key: Optional[str] = None,
) -> dict[str, Any] | None:
    """MCP handler: append a task event."""
    service = AgentService(db)
    event = await service.append_task_event(
        task_id,
        actor,
        TaskEventCreate(**payload),
        idempotency_key=idempotency_key,
    )
    if not event:
        return None
    return {
        "id": event.id,
        "task_id": event.task_id,
        "event_type": event.event_type,
        "payload": service.event_to_payload(event.payload),
        "created_at": event.created_at.isoformat(),
    }


async def start_agent_run(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    idempotency_key: Optional[str] = None,
) -> dict[str, Any]:
    """MCP handler: start an agent run."""
    service = AgentService(db)
    run = await service.start_run(actor, AgentRunCreate(**payload), idempotency_key)
    return service._run_payload(run)


async def append_run_event(
    db: AsyncSession,
    actor: AgentActor,
    run_id: int,
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    """MCP handler: append an event to an agent run."""
    service = AgentService(db)
    event = await service.append_run_event(run_id, actor, AgentRunEventCreate(**payload))
    if not event:
        return None
    return {
        "id": event.id,
        "run_id": event.run_id,
        "event_type": event.event_type,
        "message": event.message,
        "payload": service.event_to_payload(event.payload),
        "trace_id": event.trace_id,
        "span_id": event.span_id,
        "correlation_id": event.correlation_id,
        "idempotency_key": event.idempotency_key,
        "created_at": event.created_at.isoformat(),
    }


async def finish_agent_run(
    db: AsyncSession,
    actor: AgentActor,
    run_id: int,
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    """MCP handler: finish an agent run."""
    service = AgentService(db)
    run = await service.finish_run(run_id, actor, AgentRunFinish(**payload))
    return service._run_payload(run) if run else None


async def list_projects(db: AsyncSession) -> list[dict[str, Any]]:
    """MCP handler: list projects."""
    projects = await ProjectService(db).list_projects()
    return _responses(ProjectResponse, projects)


async def get_project(db: AsyncSession, project_id: int) -> dict[str, Any] | None:
    """MCP handler: get one project."""
    project = await ProjectService(db).get_by_id(project_id)
    return _response(ProjectResponse, project) if project else None


async def get_project_summary(db: AsyncSession, project_id: int) -> dict[str, Any] | None:
    """MCP handler: get project progress summary."""
    summary = await ProjectService(db).get_summary(project_id)
    return summary.model_dump(mode="json") if summary else None


async def list_project_milestones(
    db: AsyncSession, project_id: int
) -> list[dict[str, Any]] | None:
    """MCP handler: list one project's roadmap milestones."""
    milestones = await ProjectService(db).list_milestones(project_id)
    return (
        _responses(ProjectMilestoneResponse, milestones)
        if milestones is not None
        else None
    )


async def get_project_milestone(
    db: AsyncSession, project_id: int, milestone_id: int
) -> dict[str, Any] | None:
    """MCP handler: read one project-scoped milestone."""
    milestone = await ProjectService(db).get_milestone_for_project(
        project_id, milestone_id
    )
    return _response(ProjectMilestoneResponse, milestone) if milestone else None


async def list_project_updates(
    db: AsyncSession,
    project_id: int,
) -> list[dict[str, Any]] | None:
    """MCP handler: list append-only project status updates."""
    updates = await ProjectService(db).list_project_updates(project_id)
    return _responses(ProjectUpdateEntryResponse, updates) if updates is not None else None


async def create_agent_project_update(
    db: AsyncSession,
    actor: AgentActor,
    project_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: append an attributed, evidence-backed project update."""
    response = await AgentWorkService(db).create_project_update(
        actor,
        project_id,
        AgentProjectUpdateCreate(**payload),
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    return response.model_dump(mode="json")


async def list_project_tasks(db: AsyncSession, project_id: int) -> list[dict[str, Any]] | None:
    """MCP handler: list tasks linked to a project."""
    tasks = await ProjectService(db).get_tasks(project_id)
    if tasks is None:
        return None
    task_service = TaskService(db)
    return [task_service.task_to_response(task).model_dump(mode="json") for task in tasks]


async def list_triage_items(
    db: AsyncSession,
    active: Optional[bool] = True,
    statuses: Optional[list[str]] = None,
    q: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """MCP handler: list triage items."""
    normalized_statuses = [TriageItemStatus(status) for status in statuses] if statuses else None
    items = await TriageService(db).list_items(
        active=active,
        statuses=normalized_statuses,
        q=q,
        source=source,
        limit=limit,
        offset=offset,
    )
    return _responses(TriageItemResponse, items)


async def get_triage_item(db: AsyncSession, triage_item_id: int) -> dict[str, Any] | None:
    """MCP handler: get a triage item."""
    item = await TriageService(db).get_by_id(triage_item_id)
    return _response(TriageItemResponse, item) if item else None


async def create_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: idempotently create a PM-controlled triage item."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    actor_id = actor.id
    data = TriageItemCreate(**payload)
    request_payload = _triage_audited_request(
        command,
        {"triage_item": data.model_dump(mode="json")},
    )
    operation = "triage.create"
    target_type = "triage_collection"
    target_id = 0
    replay = await _triage_command_replay(
        db,
        actor_id=actor_id,
        operation=operation,
        target_type=target_type,
        target_id=target_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay

    try:
        item = await TriageService(db).create(data, commit=False)
        response = _response(TriageItemResponse, item)
        await _stage_triage_command_audit_event(
            db,
            actor=actor,
            operation=operation,
            triage_item_id=item.id,
            command=command,
        )
        _stage_triage_command_receipt(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
            command=command,
        )
        return await _commit_triage_command(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=target_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
        )
    except Exception:
        await db.rollback()
        raise


async def classify_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """MCP handler: idempotently persist one advisory classification receipt."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    actor_id = actor.id
    request_payload = _triage_audited_request(
        command,
        {"triage_item_id": triage_item_id},
    )
    operation = "triage.classify"
    target_type = "triage_item"
    replay = await _triage_command_replay(
        db,
        actor_id=actor_id,
        operation=operation,
        target_type=target_type,
        target_id=triage_item_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay

    try:
        suggestion = await TriageService(db).classify_item(
            triage_item_id,
            commit=False,
        )
        if suggestion is None:
            await db.rollback()
            return None
        response = _response(TriageClassificationSuggestionResponse, suggestion)
        await _stage_triage_command_audit_event(
            db,
            actor=actor,
            operation=operation,
            triage_item_id=triage_item_id,
            command=command,
        )
        _stage_triage_command_receipt(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
            command=command,
        )
        return await _commit_triage_command(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
        )
    except Exception:
        await db.rollback()
        raise


async def draft_triage_task(
    db: AsyncSession,
    triage_item_id: int,
    payload: Optional[dict[str, Any]] = None,
) -> dict[str, Any] | None:
    """MCP handler: draft transient task details for triage conversion."""
    draft = await TriageService(db).draft_task(
        triage_item_id,
        TriageTaskDraftRequest(**(payload or {})),
    )
    return draft.model_dump(mode="json") if draft else None


async def update_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """Idempotently update editable triage metadata."""
    return await _mutate_triage_item(
        db,
        actor,
        triage_item_id,
        operation="triage.update",
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
        data=TriageItemUpdate(**payload),
        service_method="update",
    )


async def accept_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """Idempotently accept one triage item."""
    return await _mutate_triage_item(
        db,
        actor,
        triage_item_id,
        operation="triage.accept",
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
        data=TriageActionRequest(**payload),
        service_method="accept",
    )


async def decline_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """Idempotently decline one triage item."""
    return await _mutate_triage_item(
        db,
        actor,
        triage_item_id,
        operation="triage.decline",
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
        data=TriageActionRequest(**payload),
        service_method="decline",
    )


async def snooze_triage_item(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """Idempotently snooze one triage item until a future timestamp."""
    return await _mutate_triage_item(
        db,
        actor,
        triage_item_id,
        operation="triage.snooze",
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
        data=TriageSnoozeRequest(**payload),
        service_method="snooze",
    )


async def mark_triage_item_duplicate(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """Idempotently mark one item as a duplicate of an item or task."""
    return await _mutate_triage_item(
        db,
        actor,
        triage_item_id,
        operation="triage.mark_duplicate",
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
        data=TriageDuplicateRequest(**payload),
        service_method="mark_duplicate",
    )


async def convert_triage_to_task(
    db: AsyncSession,
    actor: AgentActor,
    triage_item_id: int,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """MCP handler: idempotently convert one locked triage item to one task."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    actor_id = actor.id
    data = TriageConvertToTaskRequest(**payload)
    request_payload = _triage_audited_request(
        command,
        {
            "triage_item_id": triage_item_id,
            "conversion": data.model_dump(mode="json"),
        },
    )
    operation = "triage.convert_to_task"
    target_type = "triage_item"
    replay = await _triage_command_replay(
        db,
        actor_id=actor_id,
        operation=operation,
        target_type=target_type,
        target_id=triage_item_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay

    service = TriageService(db)
    try:
        # Serialize conversion on the source item, then recheck the receipt in
        # case an identical concurrent request committed while this call waited.
        item = await service.get_by_id(triage_item_id, for_update=True)
        if item is None:
            await db.rollback()
            return None
        replay = await _triage_command_replay(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
        )
        if replay is not None:
            await db.rollback()
            return replay

        result = await service.convert_to_task(
            triage_item_id,
            data,
            commit=False,
        )
        if result is None:  # pragma: no cover - protected by the locked read
            await db.rollback()
            return None
        item, task = result
        response = TriageConvertToTaskResponse(
            triage_item=TriageItemResponse.model_validate(item),
            task=TaskService(db).task_to_response(task),
        ).model_dump(mode="json")
        await _stage_triage_command_audit_event(
            db,
            actor=actor,
            operation=operation,
            triage_item_id=triage_item_id,
            command=command,
        )
        _stage_triage_command_receipt(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
            command=command,
        )
        return await _commit_triage_command(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
            response=response,
        )
    except TriageConflictError:
        await db.rollback()
        replay = await _triage_command_replay(
            db,
            actor_id=actor_id,
            operation=operation,
            target_type=target_type,
            target_id=triage_item_id,
            idempotency_key=key,
            request_payload=request_payload,
        )
        if replay is not None:
            return replay
        raise
    except Exception:
        await db.rollback()
        raise


async def list_releases_for_project(db: AsyncSession, project_id: int) -> list[dict[str, Any]] | None:
    """MCP handler: list releases for a project."""
    releases = await ReleaseService(db).list_for_project(project_id)
    return _responses(ReleaseResponse, releases) if releases is not None else None


async def get_release(db: AsyncSession, release_id: int) -> dict[str, Any] | None:
    """MCP handler: get a release."""
    release = await ReleaseService(db).get_by_id(release_id)
    return _response(ReleaseResponse, release) if release else None


async def list_label_groups(db: AsyncSession, include_inactive: bool = False) -> list[dict[str, Any]]:
    """MCP handler: list label groups."""
    groups = await LabelService(db).list_groups(include_inactive=include_inactive)
    return _responses(LabelGroupResponse, groups)


async def list_labels(
    db: AsyncSession,
    group_id: Optional[int] = None,
    group_key: Optional[str] = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    """MCP handler: list labels."""
    service = LabelService(db)
    if group_id is not None and group_key is None:
        group = await service.get_group_by_id(group_id)
        if group is None:
            return []
        group_key = group.key
    labels = await service.list_labels(group_key=group_key, include_inactive=include_inactive)
    return _responses(LabelResponse, labels)


async def list_templates(
    db: AsyncSession,
    template_type: Optional[str] = None,
    include_inactive: bool = False,
) -> list[dict[str, Any]]:
    """MCP handler: list work templates."""
    normalized_type = TemplateType(template_type) if template_type else None
    templates = await TemplateService(db).list_templates(
        template_type=normalized_type,
        include_inactive=include_inactive,
    )
    return _responses(WorkTemplateResponse, templates)


async def list_saved_views(
    db: AsyncSession,
    view_type: Optional[str] = None,
) -> list[dict[str, Any]]:
    """MCP handler: list shared/system saved views visible without a user session."""
    service = SavedViewService(db)
    if view_type:
        views = await service.list_visible(SavedViewType(view_type), session_id=None)
    else:
        views = []
        for candidate_type in SavedViewType:
            views.extend(await service.list_visible(candidate_type, session_id=None))
    return [view.model_dump(mode="json") for view in views]


async def list_external_links(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
) -> list[dict[str, Any]]:
    """MCP handler: list external links for a supported entity."""
    service = ExternalLinkService(db)
    links = (
        await service.list_task_links(entity_id)
        if entity_type == "task"
        else await service.list_for_entity(entity_type, entity_id)
    )
    if links is None:
        return []
    return [service.link_to_response(link).model_dump(mode="json") for link in links]


async def create_task_github_link(
    db: AsyncSession,
    actor: AgentActor,
    task_id: int,
    url: str,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any] | None:
    """MCP handler: idempotently link a GitHub URL to a task."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    request_payload = _triage_audited_request(
        command,
        {"task_id": task_id, "url": url},
    )
    replay = await _triage_command_replay(
        db,
        actor_id=actor.id,
        operation="external_link.github.create",
        target_type="task",
        target_id=task_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay
    if not await lock_task_context(db, task_id):
        return None
    # The context lock may have waited for an exact concurrent command. Resolve
    # its durable receipt before evaluating provider-level duplicate state.
    replay = await _triage_command_replay(
        db,
        actor_id=actor.id,
        operation="external_link.github.create",
        target_type="task",
        target_id=task_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay
    service = ExternalLinkService(db)
    link = await service.create_task_github_link(task_id, url, commit=False)
    if link is None:
        return None
    response = service.link_to_response(link).model_dump(mode="json")
    await _stage_context_command_audit_event(
        db,
        actor=actor,
        operation="external_link.github.create",
        target_type="task",
        target_id=task_id,
        command=command,
        task_id=task_id,
        details={"external_link_id": link.id, "url": link.url},
    )
    _stage_triage_command_receipt(
        db,
        actor_id=actor.id,
        operation="external_link.github.create",
        target_type="task",
        target_id=task_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
        command=command,
    )
    return await _commit_triage_command(
        db,
        actor_id=actor.id,
        operation="external_link.github.create",
        target_type="task",
        target_id=task_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
    )


async def delete_external_link(
    db: AsyncSession,
    actor: AgentActor,
    link_id: int,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: idempotently delete an external link."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    request_payload = _triage_audited_request(command, {"link_id": link_id})
    replay = await _triage_command_replay(
        db,
        actor_id=actor.id,
        operation="external_link.delete",
        target_type="external_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay
    service = ExternalLinkService(db)
    link = await service.get_by_id(link_id)
    task_id = link.entity_id if link is not None and link.entity_type == "task" else None
    deleted = await service.delete_link(link_id, commit=False)
    response = {"deleted": deleted}
    await _stage_context_command_audit_event(
        db,
        actor=actor,
        operation="external_link.delete",
        target_type="external_link",
        target_id=link_id,
        command=command,
        task_id=task_id,
        details={
            "entity_type": link.entity_type if link is not None else None,
            "entity_id": link.entity_id if link is not None else None,
        },
    )
    _stage_triage_command_receipt(
        db,
        actor_id=actor.id,
        operation="external_link.delete",
        target_type="external_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
        command=command,
    )
    return await _commit_triage_command(
        db,
        actor_id=actor.id,
        operation="external_link.delete",
        target_type="external_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
    )


async def search_request_sources(
    db: AsyncSession,
    q: Optional[str] = None,
    source_type: Optional[str] = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """MCP handler: search request sources."""
    sources = await RequestSourceService(db).search_sources(
        q=q,
        source_type=source_type,
        limit=limit,
    )
    return _responses(RequestSourceResponse, sources)


async def list_request_source_links(
    db: AsyncSession,
    target_type: str,
    target_id: int,
) -> list[dict[str, Any]]:
    """MCP handler: list request-source links for a target."""
    links = await RequestSourceService(db).list_links_for_target(target_type, target_id)
    return _responses(RequestSourceLinkWithSourceResponse, links)


async def create_request_source_link(
    db: AsyncSession,
    actor: AgentActor,
    payload: dict[str, Any],
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: idempotently create an attributed request-source link."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    request = RequestSourceLinkCreateRequest(**payload)
    request_payload = _triage_audited_request(
        command,
        request.model_dump(mode="json"),
    )
    target_type = str(request.target_type.value)
    actor_id = actor.id
    for attempt in range(REQUEST_SOURCE_WRITE_MAX_ATTEMPTS):
        replay = await _triage_command_replay(
            db,
            actor_id=actor_id,
            operation="request_source.link.create",
            target_type=target_type,
            target_id=request.target_id,
            idempotency_key=key,
            request_payload=request_payload,
        )
        if replay is not None:
            return replay

        try:
            current_actor = await db.get(AgentActor, actor_id)
            if current_actor is None:
                raise AgentConflictError("Agent actor is unavailable")
            service = RequestSourceService(db)
            link = await service.create_link(request, commit=False)
            loaded = await service.get_link(link.id)
            if loaded is None:
                raise AgentConflictError("Created request-source link is unavailable")
            response = _response(RequestSourceLinkWithSourceResponse, loaded)
            await _stage_context_command_audit_event(
                db,
                actor=current_actor,
                operation="request_source.link.create",
                target_type=target_type,
                target_id=request.target_id,
                command=command,
                task_id=request.target_id if target_type == "task" else None,
                details={
                    "request_source_id": link.request_source_id,
                    "request_source_link_id": link.id,
                },
            )
            _stage_triage_command_receipt(
                db,
                actor_id=actor_id,
                operation="request_source.link.create",
                target_type=target_type,
                target_id=request.target_id,
                idempotency_key=key,
                request_payload=request_payload,
                response=response,
                command=command,
            )
            return await _commit_triage_command(
                db,
                actor_id=actor_id,
                operation="request_source.link.create",
                target_type=target_type,
                target_id=request.target_id,
                idempotency_key=key,
                request_payload=request_payload,
                response=response,
            )
        except RequestSourceConflictError:
            await db.rollback()
            replay = await _triage_command_replay(
                db,
                actor_id=actor_id,
                operation="request_source.link.create",
                target_type=target_type,
                target_id=request.target_id,
                idempotency_key=key,
                request_payload=request_payload,
            )
            if replay is not None:
                return replay
            raise
        except TaskContextVersionConflictError:
            await db.rollback()
            replay = await _triage_command_replay(
                db,
                actor_id=actor_id,
                operation="request_source.link.create",
                target_type=target_type,
                target_id=request.target_id,
                idempotency_key=key,
                request_payload=request_payload,
            )
            if replay is not None:
                return replay
            if attempt + 1 >= REQUEST_SOURCE_WRITE_MAX_ATTEMPTS:
                raise
            await asyncio.sleep(min(0.01 * (2**attempt), 0.2))
        except OperationalError as exc:
            await db.rollback()
            message = str(exc).lower()
            sqlite_write_race = any(
                marker in message
                for marker in (
                    "database is locked",
                    "database table is locked",
                    "database schema is locked",
                )
            )
            if not sqlite_write_race or attempt + 1 >= REQUEST_SOURCE_WRITE_MAX_ATTEMPTS:
                raise
            await asyncio.sleep(min(0.01 * (2**attempt), 0.2))

    raise AgentConflictError("Request-source link command could not be serialized")


async def unlink_request_source(
    db: AsyncSession,
    actor: AgentActor,
    link_id: int,
    *,
    idempotency_key: str,
    rationale: str,
    correlation_id: str,
) -> dict[str, Any]:
    """MCP handler: idempotently unlink a request source."""
    command = _triage_command_context(
        idempotency_key=idempotency_key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    key = command.idempotency_key
    request_payload = _triage_audited_request(command, {"link_id": link_id})
    replay = await _triage_command_replay(
        db,
        actor_id=actor.id,
        operation="request_source.link.delete",
        target_type="request_source_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
    )
    if replay is not None:
        return replay
    service = RequestSourceService(db)
    link = await service.get_link(link_id)
    task_id = link.task_id if link is not None else None
    deleted = await service.unlink(link_id, commit=False)
    response = {"deleted": deleted}
    await _stage_context_command_audit_event(
        db,
        actor=actor,
        operation="request_source.link.delete",
        target_type="request_source_link",
        target_id=link_id,
        command=command,
        task_id=task_id,
        details={
            "request_source_id": link.request_source_id if link is not None else None,
            "target_type": (
                "task"
                if link is not None and link.task_id is not None
                else "project"
                if link is not None and link.project_id is not None
                else "triage_item"
                if link is not None and link.triage_item_id is not None
                else None
            ),
        },
    )
    _stage_triage_command_receipt(
        db,
        actor_id=actor.id,
        operation="request_source.link.delete",
        target_type="request_source_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
        command=command,
    )
    return await _commit_triage_command(
        db,
        actor_id=actor.id,
        operation="request_source.link.delete",
        target_type="request_source_link",
        target_id=link_id,
        idempotency_key=key,
        request_payload=request_payload,
        response=response,
    )


async def recommend_assignees_for_task(db: AsyncSession, task_id: int) -> list[dict[str, Any]] | None:
    """MCP handler: recommend assignees for a task."""
    recommendations = await AssigneeRecommendationService(db).recommend_for_task(task_id)
    return _dump(recommendations) if recommendations is not None else None


async def recommend_assignees_for_triage(
    db: AsyncSession,
    triage_item_id: int,
    iteration_id: Optional[int] = None,
) -> list[dict[str, Any]] | None:
    """MCP handler: recommend assignees for triage intake."""
    recommendations = await AssigneeRecommendationService(db).recommend_for_triage(
        triage_item_id,
        iteration_id=iteration_id,
    )
    return _dump(recommendations) if recommendations is not None else None


async def system_runtime_config_status(db: AsyncSession) -> dict[str, Any]:
    """MCP handler: return redacted runtime config status."""
    response = await RuntimeSettingsService(db).system_response()
    return SystemSettingsResponse.model_validate(response).model_dump(mode="json")
