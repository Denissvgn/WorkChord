"""Authoritative assessment, preview, and selection validation for agent routing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import hashlib
import hmac
import json
import math
import secrets
from typing import Any, Sequence

from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentModelBinding,
    AgentRun,
    AgentTaskAssignment,
    TaskRoutingAssessment,
)
from app.models.iteration import Iteration
from app.models.task import Task, TaskStatus
from app.models.team_member import TeamMember, TeamMemberProfile
from app.query_limits import CollectionLimitExceededError
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentRoutingCandidate,
    AgentRoutingExclusion,
    AgentRoutingPreviewCreate,
    AgentRoutingPreviewResponse,
    RoutingDecisionSnapshot,
    TaskRoutingAssessmentCommand,
    TaskRoutingAssessmentCreate,
    TaskRoutingAssessmentListResponse,
    TaskRoutingAssessmentMutationReceipt,
    TaskRoutingAssessmentResponse,
    TaskRoutingAssessmentState,
)
from app.services.agent_routing_policy import (
    MAX_ROUTING_CANDIDATES,
    MAX_ROUTING_EXCLUSIONS,
    MAX_ROUTING_PACKET_BYTES,
    MIN_ROUTING_ASSESSMENT_CONFIDENCE,
    MODEL_FAILURE_CATEGORIES,
    REVIEW_MODE_ORDER,
    ROUTING_DECISION_AUTHORITY,
    ROUTING_DECISION_LINEAGE_FIELDS,
    ROUTING_LINEAGE_AUTHORITY,
    ROUTING_POLICY_VERSION,
    ROUTING_PREVIEW_TTL_SECONDS,
    RoutingBlockerCode,
    RoutingProfileEvidence,
    canonical_routing_json_bytes,
    evaluate_actor_authorization,
    evaluate_assignment_compatibility,
    evaluate_model_envelope,
    evaluate_required_skills,
    normalize_model_failure_category,
    routing_candidate_rank_key,
    review_mode_meets,
    validate_routing_packet_size,
)
from app.services.agent_routing_observability import (
    RoutingOperationalEvent,
    record_routing_operational_event,
    routing_exclusion_projection,
)
from app.services.agent_routing_rollout import (
    AgentRoutingRolloutError,
    AgentRoutingRolloutMode,
    AgentRoutingRolloutService,
    AgentRoutingTopologyReadinessStatus,
)
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    actor_has_scope,
    actor_scopes,
    validate_idempotency_key,
)
from app.services.calendar_service import CalendarService
from app.services.task_service import TaskService, TaskVersionConflictError
from app.utils.time import as_utc, utc_now


_REQUIRED_BRIEF_SECTIONS = (
    "goal",
    "context and sources",
    "scope",
    "out of scope",
    "acceptance criteria",
    "verification",
)
_LIVE_ASSIGNMENT_STATES = ("queued", "accepted")
_ROUTING_READ_SCOPES = (
    "planning:read",
    "planning:write",
    "assignments:read",
    "assignments:write",
)
_PREVIEW_CLOCK_SKEW_SECONDS = 5
_MAX_ROUTING_INPUT_ROWS = 500


class AgentRoutingConflictError(AgentConflictError):
    """Stable routing conflict shared by REST, MCP, and assignment commands."""

    def __init__(self, code: str, message: str, **context: Any):
        self.code = code
        self.message = message
        self.context = context
        super().__init__(message)

    def detail(self) -> dict[str, Any]:
        """Return the client-safe structured conflict envelope."""

        return {
            "code": self.code,
            "message": self.message,
            **self.context,
        }


@dataclass(frozen=True)
class RoutingSelectionValidation:
    """Authoritative result consumed inside the assignment transaction."""

    assessment: TaskRoutingAssessment
    binding: AgentModelBinding
    preview: AgentRoutingPreviewResponse
    snapshot: RoutingDecisionSnapshot


def _request_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_routing_json_bytes(payload)).hexdigest()


def _json_value(value: Any, fallback: Any) -> Any:
    if value is None:
        return fallback
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return fallback


def _brief_sections(description: str | None) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in (description or "").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {
        key: "\n".join(lines).strip()
        for key, lines in sections.items()
        if "\n".join(lines).strip()
    }


def _assessment_payload(record: TaskRoutingAssessment) -> dict[str, Any]:
    return TaskRoutingAssessmentResponse.from_record(
        record,
        current_task_version=record.task_version,
    ).model_dump(mode="json", exclude={"is_current", "policy_conformant"})


def _json_projection(value: Any) -> Any:
    """Convert nested schema/time values to the canonical JSON-native boundary."""

    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, datetime):
        return as_utc(value).isoformat()
    if isinstance(value, tuple):
        return [_json_projection(item) for item in value]
    if isinstance(value, list):
        return [_json_projection(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): _json_projection(item)
            for key, item in value.items()
        }
    return value


class AgentRoutingService:
    """Create immutable assessments and deterministic exact-actor previews."""

    def __init__(
        self,
        db: AsyncSession,
        *,
        rollout_service: AgentRoutingRolloutService | None = None,
    ):
        self.db = db
        self.task_service = TaskService(db)
        self.rollout_service = rollout_service

    async def _require_preview_rollout(self, actor: AgentActor):
        """Translate fail-closed rollout state into the routing error envelope."""

        rollout_service = self.rollout_service
        if rollout_service is None:
            if self.db is None:
                rollout_service = AgentRoutingRolloutService()
            else:
                from app.services.agent_team_setup_service import (
                    AgentTeamSetupService,
                )

                readiness = await AgentTeamSetupService(
                    self.db
                ).routing_readiness(actor)
                rollout_service = (
                    AgentRoutingRolloutService()
                    if readiness.status
                    == AgentRoutingTopologyReadinessStatus.UNAVAILABLE
                    else AgentRoutingRolloutService(
                        topology_readiness=readiness
                    )
                )
        try:
            return rollout_service.require_preview()
        except AgentRoutingRolloutError as exc:
            status = exc.status
            raise AgentRoutingConflictError(
                exc.code,
                "Model-aware routing is unavailable in the effective rollout mode",
                configured_mode=status.configured_mode.value,
                effective_mode=status.effective_mode.value,
                blocker_codes=list(status.blocker_codes),
                topology_readiness=status.topology_readiness.as_dict(),
            ) from exc

    @staticmethod
    def _require_read(actor: AgentActor) -> None:
        if not any(actor_has_scope(actor, scope) for scope in _ROUTING_READ_SCOPES):
            raise AgentPermissionError(
                "Missing required scope; expected routing or planning read authority"
            )

    @staticmethod
    def _require_assessment_write(actor: AgentActor) -> None:
        if not actor_has_scope(actor, "planning:write"):
            raise AgentPermissionError("Missing required scope: planning:write")
        if actor.id <= 0:
            raise AgentPermissionError(
                "Routing assessments require a stored assessor actor identity"
            )

    async def _task_version(self, task_id: int) -> int:
        result = await self.db.execute(
            select(Task.version).where(Task.id == task_id)
        )
        task_version = result.scalar_one_or_none()
        if task_version is None:
            raise LookupError("Task not found")
        return int(task_version)

    async def _lock_task(self, task_id: int) -> Task | None:
        if self.db.get_bind().dialect.name == "sqlite":
            await self.db.execute(
                text("UPDATE tasks SET id = id WHERE id = :task_id"),
                {"task_id": task_id},
            )
        result = await self.db.execute(
            select(Task.id).where(Task.id == task_id).with_for_update()
        )
        if result.scalar_one_or_none() is None:
            return None
        return await self.task_service.get_by_id(task_id)

    async def lock_selection_inputs(self, task_id: int) -> None:
        """Fence every mutable routing input for an assignment transaction.

        SQLite's task no-op write reserves the database writer before routing
        evidence is read. PostgreSQL uses one deterministic table-lock request
        to cover both existing rows and phantoms such as a newly provisioned
        actor, vacation, binding, or competing live assignment.
        """

        dialect = self.db.get_bind().dialect.name
        if dialect == "sqlite":
            await self.db.execute(
                text("UPDATE tasks SET id = id WHERE id = :task_id"),
                {"task_id": task_id},
            )
            return
        if dialect == "postgresql":
            await self.db.execute(
                text(
                    "LOCK TABLE "
                    "calendars, iterations, team_member_profiles, "
                    "team_member_profile_skills, team_members, vacations, "
                    "tasks, task_dependencies, agent_actors, "
                    "agent_model_catalog_entries, agent_model_bindings, "
                    "agent_team_topologies, agent_team_topology_members, "
                    "task_routing_assessments, agent_task_assignments, "
                    "agent_runs "
                    "IN SHARE ROW EXCLUSIVE MODE"
                )
            )
            return
        # Best-effort row fencing for development dialects other than the two
        # supported deployment databases.
        await self.db.execute(
            select(Task.id)
            .where(Task.id == task_id)
            .with_for_update()
        )

    async def _assessment_rows(
        self,
        task_id: int,
        *,
        limit: int = 100,
    ) -> list[TaskRoutingAssessment]:
        result = await self.db.execute(
            select(TaskRoutingAssessment)
            .where(TaskRoutingAssessment.task_id == task_id)
            .order_by(
                TaskRoutingAssessment.created_at.desc(),
                TaskRoutingAssessment.id.desc(),
            )
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_assessment_state(
        self,
        task_id: int,
        actor: AgentActor,
    ) -> TaskRoutingAssessmentState:
        """Return no/current/stale state without conflating old evidence with routeability."""

        self._require_read(actor)
        task_version = await self._task_version(task_id)
        rows = await self._assessment_rows(task_id, limit=1)
        latest = (
            TaskRoutingAssessmentResponse.from_record(
                rows[0],
                current_task_version=task_version,
            )
            if rows
            else None
        )
        current_record = (
            await self.db.execute(
                select(TaskRoutingAssessment).where(
                    TaskRoutingAssessment.task_id == task_id,
                    TaskRoutingAssessment.task_version == task_version,
                    TaskRoutingAssessment.policy_version
                    == ROUTING_POLICY_VERSION,
                )
            )
        ).scalar_one_or_none()
        current = (
            TaskRoutingAssessmentResponse.from_record(
                current_record,
                current_task_version=task_version,
            )
            if current_record is not None
            else None
        )
        if current is not None and current.is_current:
            state = "current"
            assessment = current
        elif current is not None or latest is not None:
            state = "stale"
            assessment = current or latest
        else:
            state = "none"
            assessment = None
        return TaskRoutingAssessmentState(
            task_id=task_id,
            current_task_version=task_version,
            state=state,
            assessment=assessment,
        )

    async def list_assessments(
        self,
        task_id: int,
        actor: AgentActor,
        *,
        limit: int = 100,
    ) -> TaskRoutingAssessmentListResponse:
        """Return a bounded newest-first append-only assessment history."""

        self._require_read(actor)
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        task_version = await self._task_version(task_id)
        rows = await self._assessment_rows(task_id, limit=limit)
        total_count = int(
            (
                await self.db.execute(
                    select(func.count(TaskRoutingAssessment.id)).where(
                        TaskRoutingAssessment.task_id == task_id
                    )
                )
            ).scalar_one()
        )
        assessments = [
            TaskRoutingAssessmentResponse.from_record(
                row,
                current_task_version=task_version,
            )
            for row in rows
        ]
        while assessments:
            projected = {
                "task_id": task_id,
                "current_task_version": task_version,
                "assessments": assessments,
                "total_count": total_count,
                "omitted_count": total_count - len(assessments),
            }
            if (
                len(
                    canonical_routing_json_bytes(
                        _json_projection(projected)
                    )
                )
                <= MAX_ROUTING_PACKET_BYTES
            ):
                break
            assessments.pop()
        return TaskRoutingAssessmentListResponse(
            task_id=task_id,
            current_task_version=task_version,
            assessments=assessments,
            total_count=total_count,
            omitted_count=max(total_count - len(assessments), 0),
        )

    async def _assessment_replay(
        self,
        *,
        actor_id: int,
        task_id: int,
        idempotency_key: str,
        request_payload: dict[str, Any],
    ) -> TaskRoutingAssessmentMutationReceipt | None:
        result = await self.db.execute(
            select(AgentIdempotencyRecord).where(
                AgentIdempotencyRecord.actor_id == actor_id,
                AgentIdempotencyRecord.operation == "routing.assessment.create",
                AgentIdempotencyRecord.target_type == "task",
                AgentIdempotencyRecord.target_id == task_id,
                AgentIdempotencyRecord.idempotency_key == idempotency_key,
            )
        )
        record = result.scalar_one_or_none()
        if record is None:
            return None
        if not secrets.compare_digest(
            record.request_hash,
            _request_hash(request_payload),
        ):
            raise AgentRoutingConflictError(
                "routing_assessment_idempotency_conflict",
                "Idempotency key was already used with a different assessment request",
            )
        try:
            stored = json.loads(record.response_payload)
            return TaskRoutingAssessmentMutationReceipt.model_validate(
                stored["response"]
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise AgentRoutingConflictError(
                "routing_assessment_receipt_invalid",
                "Stored routing assessment receipt is invalid",
            ) from exc

    async def create_assessment(
        self,
        task_id: int,
        actor: AgentActor,
        data: TaskRoutingAssessmentCommand,
        command: AgentPlanningCommandContext,
    ) -> TaskRoutingAssessmentMutationReceipt:
        """Append one server-attributed assessment for the current task version."""

        self._require_assessment_write(actor)
        idempotency_key = validate_idempotency_key(
            command.idempotency_key,
            required=True,
        )
        assert idempotency_key is not None
        request_payload = {
            "command": {
                "rationale": command.rationale,
                "correlation_id": command.correlation_id,
            },
            "payload": data.model_dump(mode="json"),
        }
        replay = await self._assessment_replay(
            actor_id=actor.id,
            task_id=task_id,
            idempotency_key=idempotency_key,
            request_payload=request_payload,
        )
        if replay is not None:
            return replay

        try:
            task = await self._lock_task(task_id)
            if task is None:
                raise LookupError("Task not found")
            replay = await self._assessment_replay(
                actor_id=actor.id,
                task_id=task_id,
                idempotency_key=idempotency_key,
                request_payload=request_payload,
            )
            if replay is not None:
                await self.db.rollback()
                return replay
            await self._require_preview_rollout(actor)
            if task.version != data.expected_task_version:
                raise TaskVersionConflictError(
                    data.expected_task_version,
                    self.task_service._metadata_from_task(task),
                )
            if data.confidence < MIN_ROUTING_ASSESSMENT_CONFIDENCE:
                raise ValueError(
                    "confidence must be at least "
                    f"{MIN_ROUTING_ASSESSMENT_CONFIDENCE:.2f}"
                )
            pending_result = await self.db.execute(
                select(AgentTaskAssignment.routing_snapshot).where(
                    AgentTaskAssignment.task_id == task.id,
                    AgentTaskAssignment.purpose == "execution",
                    AgentTaskAssignment.queue_class.in_(("rework", "recovery")),
                    AgentTaskAssignment.state == "queued",
                )
            )
            review_floors: list[str] = []
            for raw_snapshot in pending_result.scalars():
                snapshot = _json_value(raw_snapshot, {})
                if (
                    snapshot.get("schema_version")
                    != "routing-lineage-snapshot-v1"
                    or snapshot.get("authority")
                    != ROUTING_LINEAGE_AUTHORITY
                    or snapshot.get("selection_pending") is not True
                ):
                    continue
                review_floor = snapshot.get("review_floor")
                if isinstance(review_floor, dict):
                    review_floors.append(
                        str(review_floor.get("review_mode") or "none")
                    )
            required_review_floor = max(
                review_floors or ["none"],
                key=lambda value: REVIEW_MODE_ORDER.get(value, -1),
            )
            if not review_mode_meets(
                str(data.review_mode),
                required_review_floor,
            ):
                raise AgentRoutingConflictError(
                    "routing_review_floor_not_met",
                    "Rework or recovery must preserve the prior review floor",
                    required_review_mode=required_review_floor,
                    supplied_review_mode=str(data.review_mode),
                    task_id=task.id,
                )
            existing_result = await self.db.execute(
                select(TaskRoutingAssessment).where(
                    TaskRoutingAssessment.task_id == task.id,
                    TaskRoutingAssessment.task_version == task.version,
                    TaskRoutingAssessment.policy_version
                    == ROUTING_POLICY_VERSION,
                )
            )
            existing = existing_result.scalar_one_or_none()
            if existing is not None:
                raise AgentRoutingConflictError(
                    "routing_assessment_version_already_exists",
                    "The current task version already has an immutable routing assessment",
                    assessment_id=existing.id,
                    task_id=task.id,
                    task_version=task.version,
                    policy_version=ROUTING_POLICY_VERSION,
                )

            create = TaskRoutingAssessmentCreate(
                task_id=task.id,
                task_version=task.version,
                policy_version=ROUTING_POLICY_VERSION,
                band=data.band,
                axes=data.axes,
                required_skill_levels=data.required_skill_levels,
                required_model=data.required_model,
                review_mode=data.review_mode,
                confidence=data.confidence,
                reason_codes=data.reason_codes,
                rationale=data.rationale,
                assessor=actor.name,
                assessor_actor_id=actor.id,
            )
            assessment = TaskRoutingAssessment(**create.model_values())
            self.db.add(assessment)
            await self.db.flush()
            response = TaskRoutingAssessmentResponse.from_record(
                assessment,
                current_task_version=task.version,
            )
            event = await self.task_service.record_task_event(
                task.id,
                "agent.routing_assessment_created",
                {
                    "assessment_id": assessment.id,
                    "task_version": task.version,
                    "policy_version": ROUTING_POLICY_VERSION,
                    "band": assessment.band,
                    "review_mode": assessment.review_mode,
                    "confidence": assessment.confidence,
                },
                actor_type="agent",
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=idempotency_key,
            )
            await self.db.flush()
            operational_event_id = await record_routing_operational_event(
                self.db,
                event=RoutingOperationalEvent.ASSESSMENT_CREATED,
                task_id=task.id,
                actor_id=actor.id,
                correlation_id=command.correlation_id,
                idempotency_key=idempotency_key,
                values={
                    "assessment_id": assessment.id,
                    "assessment_task_version": assessment.task_version,
                    "task_version": task.version,
                    "policy_version": assessment.policy_version,
                    "band": assessment.band,
                    "review_mode": assessment.review_mode,
                    "reason_codes": list(assessment.reason_codes),
                },
            )
            receipt = TaskRoutingAssessmentMutationReceipt(
                operation="routing.assessment.create",
                actor_id=actor.id,
                target_type="task_routing_assessment",
                target_id=assessment.id,
                task_id=task.id,
                idempotency_key=idempotency_key,
                rationale=command.rationale,
                correlation_id=command.correlation_id,
                authoritative_task_version=task.version,
                assessment=response,
                audit_event_ids=[event.id, operational_event_id],
            )
            self.db.add(
                AgentIdempotencyRecord(
                    actor_id=actor.id,
                    operation="routing.assessment.create",
                    target_type="task",
                    target_id=task.id,
                    idempotency_key=idempotency_key,
                    request_hash=_request_hash(request_payload),
                    response_payload=json.dumps(
                        {"response": receipt.model_dump(mode="json")},
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                )
            )
            await self.db.commit()
            return receipt
        except IntegrityError as exc:
            await self.db.rollback()
            replay = await self._assessment_replay(
                actor_id=actor.id,
                task_id=task_id,
                idempotency_key=idempotency_key,
                request_payload=request_payload,
            )
            if replay is not None:
                return replay
            raise AgentRoutingConflictError(
                "routing_assessment_concurrent_conflict",
                "A concurrent command created assessment evidence for this task version",
                task_id=task_id,
                expected_task_version=data.expected_task_version,
            ) from exc
        except Exception:
            await self.db.rollback()
            raise

    @staticmethod
    def _profile_evidence(
        profile: TeamMemberProfile | None,
    ) -> RoutingProfileEvidence | None:
        if profile is None:
            return None
        return RoutingProfileEvidence(
            profile_id=profile.id,
            profile_kind=profile.profile_kind,
            automation_enabled=profile.automation_enabled,
            assignment_modes=frozenset(profile.assignment_modes or []),
            skill_levels={
                skill.skill_key: skill.level
                for skill in profile.skills
            },
            weakness_keys=frozenset(
                skill.skill_key
                for skill in profile.skills
                if skill.is_weakness
            ),
        )

    @staticmethod
    def _profile_revision(profile: TeamMemberProfile | None) -> str | None:
        if profile is None:
            return None
        evidence = {
            "profile_id": profile.id,
            "updated_at": profile.updated_at.isoformat(),
            "automation_enabled": profile.automation_enabled,
            "profile_kind": profile.profile_kind,
            "assignment_modes": sorted(profile.assignment_modes or []),
            "skills": [
                {
                    "id": skill.id,
                    "key": skill.skill_key,
                    "level": skill.level,
                    "interest": skill.interest,
                    "weakness": skill.is_weakness,
                    "updated_at": skill.updated_at.isoformat(),
                }
                for skill in sorted(
                    profile.skills,
                    key=lambda item: (item.skill_key, item.id),
                )
            ],
        }
        digest = hashlib.sha256(canonical_routing_json_bytes(evidence)).hexdigest()[:24]
        return f"p{profile.id}-{digest}"

    @staticmethod
    def _task_global_blockers(
        task: Task,
        *,
        purpose: str,
        task_assignments: Sequence[AgentTaskAssignment],
        running_runs: Sequence[AgentRun],
    ) -> list[str]:
        blockers: list[str] = []
        if task.is_deferred:
            blockers.append(RoutingBlockerCode.TASK_DEFERRED.value)
        if task.children:
            blockers.append(RoutingBlockerCode.TASK_COMPOSITE.value)

        if purpose == "execution":
            pending_reselection = any(
                assignment.purpose == "execution"
                and assignment.queue_class in {"rework", "recovery"}
                and assignment.state == "queued"
                and bool(
                    _json_value(
                        assignment.routing_snapshot,
                        {},
                    ).get("selection_pending")
                )
                for assignment in task_assignments
            )
            if task.status != TaskStatus.PLANNED.value and not (
                task.status == TaskStatus.ACTIVE.value and pending_reselection
            ):
                blockers.append(
                    RoutingBlockerCode.TASK_STATUS_INCOMPATIBLE.value
                )
            brief = _brief_sections(task.description)
            tags = set(_json_value(task.tags, []))
            definition_incomplete = any(
                not brief.get(section) for section in _REQUIRED_BRIEF_SECTIONS
            )
            open_questions = brief.get("open questions", "").strip().lower()
            if (
                open_questions
                and open_questions not in {"none", "- none", "n/a", "- n/a"}
            ):
                definition_incomplete = True
            if (
                "agent" not in tags
                or not any(tag.startswith("cap:") for tag in tags)
                or task.effort_days <= 0
                or not 1 <= task.priority <= 10
            ):
                definition_incomplete = True
            if definition_incomplete:
                blockers.append(
                    RoutingBlockerCode.TASK_DEFINITION_NOT_READY.value
                )
            if any(
                edge.depends_on.status
                not in {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}
                for edge in task.dependencies
            ):
                blockers.append(
                    RoutingBlockerCode.TASK_DEPENDENCY_UNRESOLVED.value
                )
        elif purpose == "verification":
            if task.status != TaskStatus.RESOLVED.value:
                blockers.append(
                    RoutingBlockerCode.TASK_STATUS_INCOMPATIBLE.value
                )
            if (
                task.claimed_by is not None
                or running_runs
                or any(
                    assignment.purpose == "execution"
                    and assignment.state in _LIVE_ASSIGNMENT_STATES
                    for assignment in task_assignments
                )
            ):
                blockers.append(
                    RoutingBlockerCode.CURRENT_WORK_CONFLICT.value
                )
        else:
            raise ValueError("purpose must be execution or verification")

        if task.start_date is None or task.end_date is None:
            blockers.append(RoutingBlockerCode.SCHEDULE_MISSING.value)
        elif task.end_date < task.start_date:
            blockers.append(RoutingBlockerCode.SCHEDULE_CONFLICT.value)
        return sorted(set(blockers))

    @staticmethod
    def _preview_signing_key() -> bytes:
        settings = get_settings()
        root_material = (
            settings.settings_encryption_key
            or settings.agent_bootstrap_api_key
        )
        if not root_material:
            if settings.deployment_environment == "production":
                raise AgentRoutingConflictError(
                    "routing_preview_signing_unavailable",
                    "Routing previews require deployment signing material",
                )
            root_material = f"non-production:{settings.database_url}"
        return hmac.new(
            root_material.encode("utf-8"),
            b"workchord-routing-preview-v1",
            hashlib.sha256,
        ).digest()

    @classmethod
    def _preview_id(
        cls,
        *,
        generated_at: datetime,
        task_id: int,
        assessment_id: int,
        purpose: str,
        reviewer_profile_id: int | None,
        input_digest: str,
        requesting_actor_id: int,
    ) -> str:
        issued_epoch = int(as_utc(generated_at).timestamp())
        message = ".".join(
            (
                str(issued_epoch),
                str(requesting_actor_id),
                str(task_id),
                str(assessment_id),
                purpose,
                str(reviewer_profile_id or 0),
                input_digest,
            )
        )
        signature = hmac.new(
            cls._preview_signing_key(),
            message.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return f"rp1.{issued_epoch}.{requesting_actor_id}.{signature}"

    @staticmethod
    def _parse_preview_id(preview_id: str) -> tuple[datetime, int]:
        parts = preview_id.split(".")
        if (
            len(parts) != 4
            or parts[0] != "rp1"
            or not parts[1].isdigit()
            or not parts[2].isdigit()
            or len(parts[3]) != 64
        ):
            raise AgentRoutingConflictError(
                "routing_preview_invalid",
                "Routing preview ID is malformed",
            )
        try:
            issued_at = datetime.fromtimestamp(int(parts[1]), tz=UTC)
        except (OverflowError, OSError, ValueError) as exc:
            raise AgentRoutingConflictError(
                "routing_preview_invalid",
                "Routing preview issue time is invalid",
            ) from exc
        requesting_actor_id = int(parts[2])
        if requesting_actor_id <= 0:
            raise AgentRoutingConflictError(
                "routing_preview_invalid",
                "Routing preview requester identity is invalid",
            )
        return issued_at, requesting_actor_id

    async def _preview_context(
        self,
        task: Task,
    ) -> tuple[
        Iteration,
        list[TeamMember],
        list[AgentActor],
        list[AgentTaskAssignment],
        list[AgentRun],
        dict[int, tuple[int, int]],
        dict[int, int],
    ]:
        iteration_result = await self.db.execute(
            select(Iteration)
            .options(
                selectinload(Iteration.calendar),
                selectinload(Iteration.team_members)
                .selectinload(TeamMember.vacations),
                selectinload(Iteration.team_members)
                .selectinload(TeamMember.profile)
                .selectinload(TeamMemberProfile.skills),
            )
            .where(Iteration.id == task.iteration_id)
        )
        iteration = iteration_result.scalar_one_or_none()
        if iteration is None:
            raise AgentRoutingConflictError(
                "routing_iteration_missing",
                "Task iteration is missing",
                task_id=task.id,
            )
        members = list(iteration.team_members)
        if len(members) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing team members",
                _MAX_ROUTING_INPUT_ROWS,
            )

        actor_result = await self.db.execute(
            select(AgentActor)
            .options(
                selectinload(AgentActor.profile).selectinload(
                    TeamMemberProfile.skills
                ),
                selectinload(AgentActor.model_bindings).selectinload(
                    AgentModelBinding.model_catalog
                ),
            )
            .order_by(AgentActor.id)
            .limit(_MAX_ROUTING_INPUT_ROWS + 1)
        )
        actors = list(actor_result.scalars().all())
        if len(actors) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing actors",
                _MAX_ROUTING_INPUT_ROWS,
            )

        assignment_result = await self.db.execute(
            select(AgentTaskAssignment)
            .options(
                selectinload(AgentTaskAssignment.actor).selectinload(
                    AgentActor.profile
                )
            )
            .where(AgentTaskAssignment.task_id == task.id)
            .order_by(AgentTaskAssignment.id)
            .limit(_MAX_ROUTING_INPUT_ROWS + 1)
        )
        task_assignments = list(assignment_result.scalars().all())
        if len(task_assignments) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing task assignments",
                _MAX_ROUTING_INPUT_ROWS,
            )
        run_result = await self.db.execute(
            select(AgentRun)
            .where(
                AgentRun.task_id == task.id,
                AgentRun.status == "running",
            )
            .order_by(AgentRun.id)
            .limit(_MAX_ROUTING_INPUT_ROWS + 1)
        )
        running_task_runs = list(run_result.scalars().all())
        if len(running_task_runs) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing task runs",
                _MAX_ROUTING_INPUT_ROWS,
            )

        actor_ids = [actor.id for actor in actors]
        assignment_counts: dict[int, tuple[int, int]] = {}
        running_counts: dict[int, int] = {}
        if actor_ids:
            count_rows = (
                await self.db.execute(
                    select(
                        AgentTaskAssignment.actor_id,
                        AgentTaskAssignment.state,
                        func.count(AgentTaskAssignment.id),
                    )
                    .where(
                        AgentTaskAssignment.actor_id.in_(actor_ids),
                        AgentTaskAssignment.state.in_(_LIVE_ASSIGNMENT_STATES),
                    )
                    .group_by(
                        AgentTaskAssignment.actor_id,
                        AgentTaskAssignment.state,
                    )
                )
            ).all()
            mutable_counts: dict[int, list[int]] = {
                actor_id: [0, 0] for actor_id in actor_ids
            }
            for actor_id, state, count in count_rows:
                mutable_counts[int(actor_id)][0 if state == "queued" else 1] = int(
                    count
                )
            assignment_counts = {
                actor_id: (counts[0], counts[1])
                for actor_id, counts in mutable_counts.items()
            }
            running_counts = {
                int(actor_id): int(count)
                for actor_id, count in (
                    await self.db.execute(
                        select(AgentRun.actor_id, func.count(AgentRun.id))
                        .where(
                            AgentRun.actor_id.in_(actor_ids),
                            AgentRun.status == "running",
                        )
                        .group_by(AgentRun.actor_id)
                    )
                ).all()
            }
        return (
            iteration,
            members,
            actors,
            task_assignments,
            running_task_runs,
            assignment_counts,
            running_counts,
        )

    async def _capacity_inputs(
        self,
        *,
        task: Task,
        iteration: Iteration,
        members: Sequence[TeamMember],
    ) -> dict[int, dict[str, Any]]:
        allocated_rows = (
            await self.db.execute(
                select(
                    Task.assignee_id,
                    func.coalesce(func.sum(Task.effort_days), 0.0),
                )
                .where(
                    Task.iteration_id == iteration.id,
                    Task.assignee_id.is_not(None),
                    Task.is_deferred.is_(False),
                    Task.id != task.id,
                )
                .group_by(Task.assignee_id)
            )
        ).all()
        allocated_by_member = {
            int(member_id): float(effort)
            for member_id, effort in allocated_rows
        }
        calendar_service = CalendarService(self.db)
        capacity: dict[int, dict[str, Any]] = {}
        for member in members:
            working_days = calendar_service.calculate_working_days(
                iteration.calendar,
                iteration.start_date,
                iteration.end_date,
            ).working_days
            vacation_days = 0
            for vacation in member.vacations:
                overlap_start = max(vacation.start_date, iteration.start_date)
                overlap_end = min(vacation.end_date, iteration.end_date)
                if overlap_start <= overlap_end:
                    vacation_days += calendar_service.calculate_working_days(
                        iteration.calendar,
                        overlap_start,
                        overlap_end,
                    ).working_days
            available_days = (
                (working_days - vacation_days)
                * (member.availability_percent / 100)
                * (1 - member.operational_utilization / 100)
            )
            committed = allocated_by_member.get(member.id, 0.0)
            required = max(float(task.effort_days), 0.0)
            ratio = (
                (committed + required) / available_days
                if available_days > 0
                else math.inf
            )
            vacation_conflict = bool(
                task.start_date is not None
                and task.end_date is not None
                and any(
                    vacation.start_date <= task.end_date
                    and vacation.end_date >= task.start_date
                    for vacation in member.vacations
                )
            )
            capacity[member.id] = {
                "available_capacity_days": round(available_days, 2),
                "committed_effort_days": round(committed, 2),
                "workload_ratio": (
                    round(ratio, 4) if math.isfinite(ratio) else None
                ),
                "vacation_conflict": vacation_conflict,
                "vacations": [
                    {
                        "id": vacation.id,
                        "start_date": vacation.start_date.isoformat(),
                        "end_date": vacation.end_date.isoformat(),
                    }
                    for vacation in sorted(
                        member.vacations,
                        key=lambda item: (item.start_date, item.end_date, item.id),
                    )
                ],
            }
        return capacity

    @staticmethod
    def _member_for_candidate(
        *,
        task: Task,
        purpose: str,
        profile_id: int | None,
        members: Sequence[TeamMember],
    ) -> TeamMember | None:
        if purpose == "execution":
            return next(
                (member for member in members if member.id == task.assignee_id),
                None,
            )
        if profile_id is None:
            return None
        return next(
            (member for member in members if member.profile_id == profile_id),
            None,
        )

    @staticmethod
    def _routing_input_evidence(
        *,
        task: Task,
        assessment: TaskRoutingAssessment,
        purpose: str,
        reviewer_profile_id: int | None,
        iteration: Iteration,
        members: Sequence[TeamMember],
        actors: Sequence[AgentActor],
        task_assignments: Sequence[AgentTaskAssignment],
        running_task_runs: Sequence[AgentRun],
        assignment_counts: dict[int, tuple[int, int]],
        running_counts: dict[int, int],
        capacity: dict[int, dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "policy_version": ROUTING_POLICY_VERSION,
            "purpose": purpose,
            "reviewer_profile_id": reviewer_profile_id,
            "task": {
                "id": task.id,
                "version": task.version,
                "status": task.status,
                "title_digest": hashlib.sha256(
                    task.title.encode("utf-8")
                ).hexdigest(),
                "description_digest": hashlib.sha256(
                    (task.description or "").encode("utf-8")
                ).hexdigest(),
                "tags": sorted(_json_value(task.tags, [])),
                "priority": task.priority,
                "effort_days": task.effort_days,
                "is_deferred": task.is_deferred,
                "assignee_id": task.assignee_id,
                "start_date": (
                    task.start_date.isoformat() if task.start_date else None
                ),
                "end_date": task.end_date.isoformat() if task.end_date else None,
                "child_ids": sorted(child.id for child in task.children),
                "dependencies": [
                    {
                        "task_id": edge.depends_on_id,
                        "version": edge.depends_on.version,
                        "status": edge.depends_on.status,
                    }
                    for edge in sorted(
                        task.dependencies,
                        key=lambda item: (item.depends_on_id, item.id),
                    )
                ],
                "claim": {
                    "actor_id": task.claimed_by,
                    "generation": task.claim_generation,
                    "expires_at": (
                        task.claim_expires_at.isoformat()
                        if task.claim_expires_at
                        else None
                    ),
                },
            },
            "assessment": _assessment_payload(assessment),
            "iteration": {
                "id": iteration.id,
                "start_date": iteration.start_date.isoformat(),
                "end_date": iteration.end_date.isoformat(),
                "calendar": {
                    "id": iteration.calendar.id,
                    "year": iteration.calendar.year,
                    "holidays": sorted(iteration.calendar.holidays or []),
                    "weekend_days": sorted(iteration.calendar.weekend_days or []),
                    "short_days": sorted(iteration.calendar.short_days or []),
                },
            },
            "capacity": [
                {
                    "member_id": member.id,
                    "profile_id": member.profile_id,
                    "iteration_id": member.iteration_id,
                    "availability_percent": member.availability_percent,
                    "professionalism_coefficient": member.professionalism_coefficient,
                    "operational_utilization": member.operational_utilization,
                    **capacity[member.id],
                }
                for member in sorted(members, key=lambda item: item.id)
            ],
            "actors": [
                {
                    "id": actor.id,
                    "enabled": actor.enabled,
                    "role": actor.role,
                    "scopes": sorted(actor_scopes(actor)),
                    "profile_id": actor.profile_id,
                    "work_policy": actor.work_policy,
                    "max_parallel_work": actor.max_parallel_work,
                    "queue_revision": actor.queue_revision,
                    "profile_revision": AgentRoutingService._profile_revision(
                        actor.profile
                    ),
                    "profile": (
                        {
                            "kind": actor.profile.profile_kind,
                            "automation_enabled": actor.profile.automation_enabled,
                            "assignment_modes": sorted(
                                actor.profile.assignment_modes or []
                            ),
                            "skills": [
                                {
                                    "key": skill.skill_key,
                                    "level": skill.level,
                                    "weakness": skill.is_weakness,
                                    "updated_at": skill.updated_at.isoformat(),
                                }
                                for skill in sorted(
                                    actor.profile.skills,
                                    key=lambda item: (item.skill_key, item.id),
                                )
                            ],
                        }
                        if actor.profile is not None
                        else None
                    ),
                    "bindings": [
                        {
                            "id": binding.id,
                            "revision": binding.revision,
                            "enabled": binding.enabled,
                            "default": binding.is_default,
                            "tool_tags": sorted(binding.tool_tags or []),
                            "data_policy_tags": sorted(
                                binding.data_policy_tags or []
                            ),
                            "catalog": (
                                {
                                    "id": binding.model_catalog.id,
                                    "key": binding.model_catalog.key,
                                    "revision": binding.model_catalog.revision,
                                    "enabled": binding.model_catalog.enabled,
                                    "configured_model_alias": (
                                        binding.model_catalog.configured_model_alias
                                    ),
                                    "reasoning_tier": (
                                        binding.model_catalog.reasoning_tier
                                    ),
                                    "context_tier": binding.model_catalog.context_tier,
                                    "modality_tags": sorted(
                                        binding.model_catalog.modality_tags or []
                                    ),
                                    "cost_tier": binding.model_catalog.cost_tier,
                                    "latency_tier": binding.model_catalog.latency_tier,
                                }
                                if binding.model_catalog is not None
                                else None
                            ),
                        }
                        for binding in sorted(
                            actor.model_bindings,
                            key=lambda item: item.id,
                        )
                    ],
                    "queued_assignments": assignment_counts.get(
                        actor.id, (0, 0)
                    )[0],
                    "accepted_assignments": assignment_counts.get(
                        actor.id, (0, 0)
                    )[1],
                    "running_runs": running_counts.get(actor.id, 0),
                }
                for actor in actors
            ],
            "task_assignments": [
                {
                    "id": assignment.id,
                    "actor_id": assignment.actor_id,
                    "actor_profile_id": (
                        assignment.actor.profile_id
                        if assignment.actor is not None
                        else None
                    ),
                    "purpose": assignment.purpose,
                    "queue_class": assignment.queue_class,
                    "state": assignment.state,
                    "task_version": assignment.task_version,
                    "reviewer_profile_id": assignment.reviewer_profile_id,
                    "binding_id": assignment.model_binding_id,
                    "binding_revision": assignment.model_binding_revision,
                    "routing_profile_id": _json_value(
                        assignment.routing_snapshot,
                        {},
                    ).get("profile_id"),
                    "routing_snapshot_digest": hashlib.sha256(
                        canonical_routing_json_bytes(
                            _json_value(
                                assignment.routing_snapshot,
                                {},
                            )
                        )
                    ).hexdigest(),
                }
                for assignment in task_assignments
            ],
            "running_task_runs": [
                {
                    "id": run.id,
                    "actor_id": run.actor_id,
                    "assignment_id": run.assignment_id,
                    "binding_id": run.model_binding_id,
                    "binding_revision": run.model_binding_revision,
                }
                for run in running_task_runs
            ],
        }

    async def _build_preview(
        self,
        *,
        task: Task,
        data: AgentRoutingPreviewCreate,
        generated_at: datetime,
        requesting_actor_id: int,
    ) -> AgentRoutingPreviewResponse:
        from app.services.agent_team_setup_service import AgentTeamSetupService

        topology_boundary = await AgentTeamSetupService(
            self.db
        ).membership_boundary(requesting_actor_id)
        if len(task.children) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing task children",
                _MAX_ROUTING_INPUT_ROWS,
            )
        if len(task.dependencies) > _MAX_ROUTING_INPUT_ROWS:
            raise CollectionLimitExceededError(
                "routing task dependencies",
                _MAX_ROUTING_INPUT_ROWS,
            )
        assessment_result = await self.db.execute(
            select(TaskRoutingAssessment).where(
                TaskRoutingAssessment.id == data.assessment_id,
                TaskRoutingAssessment.task_id == task.id,
            )
        )
        assessment = assessment_result.scalar_one_or_none()
        if assessment is None:
            raise AgentRoutingConflictError(
                "routing_assessment_missing",
                "The requested task routing assessment does not exist",
                task_id=task.id,
                assessment_id=data.assessment_id,
            )
        if task.version != data.expected_task_version:
            raise TaskVersionConflictError(
                data.expected_task_version,
                self.task_service._metadata_from_task(task),
            )
        assessment_response = TaskRoutingAssessmentResponse.from_record(
            assessment,
            current_task_version=task.version,
        )
        if not assessment_response.is_current:
            raise AgentRoutingConflictError(
                "routing_assessment_stale",
                "The routing assessment is not current for the task",
                task_id=task.id,
                current_task_version=task.version,
                assessment_id=assessment.id,
                assessment_task_version=assessment.task_version,
                policy_version=assessment.policy_version,
            )
        if assessment.confidence < MIN_ROUTING_ASSESSMENT_CONFIDENCE:
            raise AgentRoutingConflictError(
                "routing_assessment_low_confidence",
                "The routing assessment does not meet the confidence floor",
                assessment_id=assessment.id,
                confidence=assessment.confidence,
                minimum_confidence=MIN_ROUTING_ASSESSMENT_CONFIDENCE,
            )

        (
            iteration,
            members,
            actors,
            task_assignments,
            running_task_runs,
            assignment_counts,
            running_counts,
        ) = await self._preview_context(task)
        capacity = await self._capacity_inputs(
            task=task,
            iteration=iteration,
            members=members,
        )
        input_evidence = self._routing_input_evidence(
            task=task,
            assessment=assessment,
            purpose=data.purpose,
            reviewer_profile_id=data.reviewer_profile_id,
            iteration=iteration,
            members=members,
            actors=actors,
            task_assignments=task_assignments,
            running_task_runs=running_task_runs,
            assignment_counts=assignment_counts,
            running_counts=running_counts,
            capacity=capacity,
        )
        input_evidence["topology"] = (
            {
                "key": topology_boundary.topology_key,
                "revision": topology_boundary.topology_revision,
                "runtime_ready_actor_ids": sorted(
                    topology_boundary.runtime_ready_actor_ids
                ),
            }
            if topology_boundary is not None
            else None
        )
        input_digest = hashlib.sha256(
            canonical_routing_json_bytes(input_evidence)
        ).hexdigest()
        global_blockers = self._task_global_blockers(
            task,
            purpose=data.purpose,
            task_assignments=task_assignments,
            running_runs=running_task_runs,
        )
        if (
            task.start_date is not None
            and task.end_date is not None
            and (
                task.start_date < iteration.start_date
                or task.end_date > iteration.end_date
            )
        ):
            global_blockers.append(
                RoutingBlockerCode.SCHEDULE_CONFLICT.value
            )
            global_blockers = sorted(set(global_blockers))

        execution_assignments = [
            assignment
            for assignment in task_assignments
            if assignment.purpose == "execution"
            and assignment.state == "fulfilled"
        ]
        execution_actor_ids = [
            assignment.actor_id for assignment in execution_assignments
        ]
        execution_profile_ids: list[int | None] = []
        for assignment in execution_assignments:
            historical_snapshot = _json_value(
                assignment.routing_snapshot,
                {},
            )
            historical_profile_id = (
                historical_snapshot.get("profile_id")
                if (
                    historical_snapshot.get("schema_version")
                    == "routing-decision-snapshot-v1"
                    and historical_snapshot.get("authority")
                    == ROUTING_DECISION_AUTHORITY
                )
                else None
            )
            execution_profile_ids.append(
                historical_profile_id
                if isinstance(historical_profile_id, int)
                and historical_profile_id > 0
                else None
            )
        eligible_rows: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        exclusion_rows: list[dict[str, Any]] = []
        examined_pairs = 0

        for actor in actors:
            profile = self._profile_evidence(actor.profile)
            profile_revision = self._profile_revision(actor.profile)
            queued, accepted = assignment_counts.get(actor.id, (0, 0))
            running = running_counts.get(actor.id, 0)
            member = self._member_for_candidate(
                task=task,
                purpose=data.purpose,
                profile_id=actor.profile_id,
                members=members,
            )
            member_capacity = capacity.get(member.id) if member else None
            reviewer_profile_id = (
                data.reviewer_profile_id
                if data.reviewer_profile_id is not None
                else (
                    actor.profile_id
                    if data.purpose == "verification"
                    else None
                )
            )
            authority = evaluate_actor_authorization(
                intent=data.purpose,
                enabled=actor.enabled,
                role=actor.role,
                scopes=actor_scopes(actor),
            )
            compatibility = evaluate_assignment_compatibility(
                intent=data.purpose,
                actor_id=actor.id,
                actor_profile=profile,
                capacity_owner_id=member.id if member else None,
                capacity_owner_profile_id=(
                    member.profile_id if member else None
                ),
                reviewer_profile_id=reviewer_profile_id,
                execution_actor_ids=execution_actor_ids,
                execution_profile_ids=execution_profile_ids,
                review_mode=assessment.review_mode,
                required_specialist_skill_levels=assessment.required_skill_levels,
            )
            skill = evaluate_required_skills(
                required_skill_levels=assessment.required_skill_levels,
                actual_skill_levels=(
                    profile.skill_levels if profile is not None else {}
                ),
                weakness_keys=(
                    profile.weakness_keys if profile is not None else ()
                ),
            )
            actor_blockers = [
                *global_blockers,
                *authority.hard_blocker_codes,
                *compatibility.hard_blocker_codes,
                *skill.hard_blocker_codes,
            ]
            if (
                topology_boundary is not None
                and actor.id
                not in topology_boundary.runtime_ready_actor_ids
            ):
                actor_blockers.append(
                    RoutingBlockerCode.ACTOR_TOPOLOGY_INCOMPATIBLE.value
                )
            if (
                actor.work_policy != "assigned_only"
                or actor.max_parallel_work != 1
            ):
                actor_blockers.append(
                    RoutingBlockerCode.ACTOR_POLICY_INCOMPATIBLE.value
                )
            if member_capacity is None:
                actor_blockers.append(
                    RoutingBlockerCode.CAPACITY_OWNER_MISSING.value
                )
            else:
                if member_capacity["available_capacity_days"] <= 0:
                    actor_blockers.append(
                        RoutingBlockerCode.CAPACITY_UNAVAILABLE.value
                    )
                workload_ratio = member_capacity["workload_ratio"]
                if workload_ratio is None or workload_ratio > 1.05:
                    actor_blockers.append(
                        RoutingBlockerCode.WORKLOAD_LIMIT_EXCEEDED.value
                    )
                if member_capacity["vacation_conflict"]:
                    actor_blockers.append(
                        RoutingBlockerCode.VACATION_CONFLICT.value
                    )
            if accepted or running:
                actor_blockers.append(
                    RoutingBlockerCode.CURRENT_WORK_CONFLICT.value
                )

            bindings = sorted(actor.model_bindings, key=lambda item: item.id)
            if not bindings:
                exclusion_rows.append(
                    {
                        "actor_id": actor.id,
                        "actor_revision": actor.queue_revision,
                        "actor_queue_revision": actor.queue_revision,
                        "profile_id": actor.profile_id,
                        "profile_revision": profile_revision,
                        "capacity_owner_id": member.id if member else None,
                        "capacity_owner_profile_id": (
                            member.profile_id if member else None
                        ),
                        "eligible": False,
                        "hard_blocker_codes": sorted(
                            set(
                                (
                                    *actor_blockers,
                                    RoutingBlockerCode.MODEL_BINDING_MISSING.value,
                                )
                            )
                        ),
                        "matched_skill_levels": dict(
                            skill.matched_skill_levels
                        ),
                        "missing_skill_keys": list(skill.missing_skill_keys),
                        "insufficient_skill_keys": list(
                            skill.insufficient_skill_keys
                        ),
                        "blocking_weakness_keys": list(
                            skill.blocking_weakness_keys
                        ),
                        "available_capacity_days": (
                            member_capacity["available_capacity_days"]
                            if member_capacity
                            else None
                        ),
                        "committed_effort_days": (
                            member_capacity["committed_effort_days"]
                            if member_capacity
                            else None
                        ),
                        "workload_ratio": (
                            member_capacity["workload_ratio"]
                            if member_capacity
                            else None
                        ),
                        "vacation_conflict": (
                            member_capacity["vacation_conflict"]
                            if member_capacity
                            else None
                        ),
                        "queued_assignments": queued,
                        "accepted_assignments": accepted,
                        "running_runs": running,
                        "schedule_delay_days": (
                            max(
                                (task.start_date - generated_at.date()).days,
                                0,
                            )
                            if task.start_date
                            else None
                        ),
                        "schedule_eligible": not any(
                            blocker
                            in {
                                RoutingBlockerCode.SCHEDULE_MISSING.value,
                                RoutingBlockerCode.SCHEDULE_CONFLICT.value,
                            }
                            for blocker in global_blockers
                        ),
                        "rationale": (
                            "Excluded because the actor has no model binding."
                        ),
                    }
                )
                continue

            for binding in bindings:
                examined_pairs += 1
                if examined_pairs > _MAX_ROUTING_INPUT_ROWS:
                    raise CollectionLimitExceededError(
                        "routing actor-model pairs",
                        _MAX_ROUTING_INPUT_ROWS,
                    )
                catalog = binding.model_catalog
                model = evaluate_model_envelope(
                    assessment.required_model,
                    binding_present=True,
                    binding_enabled=binding.enabled,
                    binding_revision_current=True,
                    catalog_present=catalog is not None,
                    catalog_enabled=(
                        catalog.enabled if catalog is not None else False
                    ),
                    actual_reasoning_tier=(
                        catalog.reasoning_tier if catalog is not None else None
                    ),
                    actual_context_tier=(
                        catalog.context_tier if catalog is not None else None
                    ),
                    actual_modality_tags=(
                        catalog.modality_tags if catalog is not None else ()
                    ),
                    actual_tool_tags=binding.tool_tags or (),
                    actual_data_policy_tags=binding.data_policy_tags or (),
                )
                blockers = sorted(
                    set((*actor_blockers, *model.hard_blocker_codes))
                )
                schedule_delay_days = (
                    float(
                        max(
                            (task.start_date - generated_at.date()).days,
                            0,
                        )
                    )
                    if task.start_date
                    else 0.0
                )
                common = {
                    "actor_id": actor.id,
                    "actor_revision": actor.queue_revision,
                    "actor_queue_revision": actor.queue_revision,
                    "profile_id": actor.profile_id,
                    "profile_revision": profile_revision,
                    "capacity_owner_id": member.id if member else None,
                    "capacity_owner_profile_id": (
                        member.profile_id if member else None
                    ),
                    "model_binding_id": binding.id,
                    "model_binding_revision": binding.revision,
                    "model_catalog_id": catalog.id if catalog else None,
                    "model_catalog_key": catalog.key if catalog else None,
                    "model_catalog_revision": (
                        catalog.revision if catalog else None
                    ),
                    "configured_model_alias": (
                        catalog.configured_model_alias if catalog else None
                    ),
                    "matched_skill_levels": dict(
                        skill.matched_skill_levels
                    ),
                    "missing_skill_keys": list(skill.missing_skill_keys),
                    "blocking_weakness_keys": list(
                        skill.blocking_weakness_keys
                    ),
                    "reasoning_tier": (
                        catalog.reasoning_tier if catalog else None
                    ),
                    "context_tier": catalog.context_tier if catalog else None,
                    "cost_tier": catalog.cost_tier if catalog else None,
                    "latency_tier": catalog.latency_tier if catalog else None,
                    "available_capacity_days": (
                        member_capacity["available_capacity_days"]
                        if member_capacity
                        else None
                    ),
                    "committed_effort_days": (
                        member_capacity["committed_effort_days"]
                        if member_capacity
                        else None
                    ),
                    "workload_ratio": (
                        member_capacity["workload_ratio"]
                        if member_capacity
                        else None
                    ),
                    "vacation_conflict": (
                        member_capacity["vacation_conflict"]
                        if member_capacity
                        else None
                    ),
                    "queued_assignments": queued,
                    "accepted_assignments": accepted,
                    "running_runs": running,
                    "schedule_delay_days": schedule_delay_days,
                    "schedule_eligible": not any(
                        blocker
                        in {
                            RoutingBlockerCode.SCHEDULE_MISSING.value,
                            RoutingBlockerCode.SCHEDULE_CONFLICT.value,
                        }
                        for blocker in blockers
                    ),
                }
                if not blockers:
                    assert catalog is not None
                    assert model.adequacy_class is not None
                    assert member_capacity is not None
                    rank_key = routing_candidate_rank_key(
                        adequacy_class=model.adequacy_class,
                        cost_tier=catalog.cost_tier,
                        queue_depth=queued,
                        schedule_delay_days=schedule_delay_days,
                        latency_tier=catalog.latency_tier,
                        actor_id=actor.id,
                        binding_id=binding.id,
                    )
                    eligible_rows.append(
                        (
                            rank_key,
                            {
                                **common,
                                "modality_tags": sorted(
                                    catalog.modality_tags or []
                                ),
                                "tool_tags": sorted(binding.tool_tags or []),
                                "data_policy_tags": sorted(
                                    binding.data_policy_tags or []
                                ),
                                "eligible": True,
                                "hard_blocker_codes": [],
                                "adequacy_class": model.adequacy_class,
                                "rank": 1,
                                "confidence": assessment.confidence,
                                "rationale": (
                                    "Meets all hard routing gates; ordered by "
                                    "adequacy, cost, queue, schedule, latency, "
                                    "actor, and binding."
                                ),
                            },
                        )
                    )
                else:
                    exclusion_rows.append(
                        {
                            **common,
                            "eligible": False,
                            "hard_blocker_codes": blockers,
                            "insufficient_skill_keys": list(
                                skill.insufficient_skill_keys
                            ),
                            "missing_modality_tags": list(
                                model.missing_modality_tags
                            ),
                            "missing_tool_tags": list(
                                model.missing_tool_tags
                            ),
                            "missing_data_policy_tags": list(
                                model.missing_data_policy_tags
                            ),
                            "rationale": (
                                "Excluded by one or more deterministic hard "
                                "routing gates."
                            ),
                        }
                    )

        eligible_rows.sort(key=lambda item: item[0])
        ranked_candidates: list[AgentRoutingCandidate] = []
        for rank, (_, values) in enumerate(eligible_rows, start=1):
            values["rank"] = rank
            ranked_candidates.append(AgentRoutingCandidate.model_validate(values))
        exclusions = [
            AgentRoutingExclusion.model_validate(values)
            for values in sorted(
                exclusion_rows,
                key=lambda item: (
                    item["actor_id"],
                    item.get("model_binding_id") or 0,
                    tuple(item["hard_blocker_codes"]),
                ),
            )
        ]
        bounded_candidates = ranked_candidates[:MAX_ROUTING_CANDIDATES]
        bounded_exclusions = exclusions[:MAX_ROUTING_EXCLUSIONS]
        generated_at = as_utc(generated_at).replace(microsecond=0)
        expires_at = generated_at + timedelta(
            seconds=ROUTING_PREVIEW_TTL_SECONDS
        )
        preview_id = self._preview_id(
            generated_at=generated_at,
            task_id=task.id,
            assessment_id=assessment.id,
            purpose=data.purpose,
            reviewer_profile_id=data.reviewer_profile_id,
            input_digest=input_digest,
            requesting_actor_id=requesting_actor_id,
        )
        hard_blocker_codes = (
            []
            if bounded_candidates
            else sorted(
                set(
                    (
                        *global_blockers,
                        RoutingBlockerCode.NO_ELIGIBLE_CANDIDATE.value,
                    )
                )
            )
        )
        response_values = {
            "preview_id": preview_id,
            "input_digest": input_digest,
            "task_id": task.id,
            "topology_key": (
                topology_boundary.topology_key
                if topology_boundary is not None
                else None
            ),
            "topology_revision": (
                topology_boundary.topology_revision
                if topology_boundary is not None
                else None
            ),
            "purpose": data.purpose,
            "assessment_id": assessment.id,
            "assessment_task_version": assessment.task_version,
            "current_task_version": task.version,
            "policy_version": ROUTING_POLICY_VERSION,
            "review_mode": assessment.review_mode,
            "reviewer_profile_id": data.reviewer_profile_id,
            "generated_at": generated_at,
            "expires_at": expires_at,
            "recommended_candidate": (
                bounded_candidates[0] if bounded_candidates else None
            ),
            "eligible_candidates": bounded_candidates,
            "exclusions": bounded_exclusions,
            "eligible_candidates_omitted": max(
                len(ranked_candidates) - len(bounded_candidates),
                0,
            ),
            "exclusions_omitted": max(
                len(exclusions) - len(bounded_exclusions),
                0,
            ),
            "hard_blocker_codes": hard_blocker_codes,
        }
        # Cardinality limits alone are insufficient because evidence strings
        # vary in size. Trim the deterministic tail until the full packet,
        # including its digest field, stays within the durable boundary.
        packet_budget = MAX_ROUTING_PACKET_BYTES - 128
        while (
            len(
                canonical_routing_json_bytes(
                    _json_projection(response_values)
                )
            )
            > packet_budget
        ):
            if response_values["exclusions"]:
                response_values["exclusions"].pop()
                response_values["exclusions_omitted"] += 1
                continue
            if len(response_values["eligible_candidates"]) > 1:
                response_values["eligible_candidates"].pop()
                response_values["eligible_candidates_omitted"] += 1
                continue
            raise AgentRoutingConflictError(
                "routing_preview_packet_too_large",
                "Routing preview evidence cannot fit the bounded response packet",
                task_id=task.id,
            )
        preview_digest = hashlib.sha256(
            canonical_routing_json_bytes(_json_projection(response_values))
        ).hexdigest()
        preview = AgentRoutingPreviewResponse(
            preview_digest=preview_digest,
            **response_values,
        )
        validate_routing_packet_size(
            preview,
            label="Routing preview",
        )
        return preview

    async def preview_task_routing(
        self,
        task_id: int,
        actor: AgentActor,
        data: AgentRoutingPreviewCreate,
        *,
        now: datetime | None = None,
    ) -> AgentRoutingPreviewResponse:
        """Return a deterministic preview and stage bounded shadow/audit evidence."""

        rollout = await self._require_preview_rollout(actor)
        self._require_read(actor)
        if actor.id <= 0:
            raise AgentPermissionError(
                "Routing previews require a stored actor identity"
            )
        task = await self.task_service.get_by_id(task_id)
        if task is None:
            raise LookupError("Task not found")
        preview = await self._build_preview(
            task=task,
            data=data,
            generated_at=now or utc_now(),
            requesting_actor_id=actor.id,
        )
        operational_values = {
            "task_version": preview.current_task_version,
            "policy_version": ROUTING_POLICY_VERSION,
            "rollout_mode": rollout.effective_mode.value,
            "assessment_id": preview.assessment_id,
            "assessment_task_version": preview.assessment_task_version,
            "purpose": preview.purpose,
            "routing_preview_id": preview.preview_id,
            "routing_preview_digest": preview.preview_digest,
            "input_digest": preview.input_digest,
            "recommended_actor_id": (
                preview.recommended_candidate.actor_id
                if preview.recommended_candidate is not None
                else None
            ),
            "recommended_model_binding_id": (
                preview.recommended_candidate.model_binding_id
                if preview.recommended_candidate is not None
                else None
            ),
            "recommended_model_binding_revision": (
                preview.recommended_candidate.model_binding_revision
                if preview.recommended_candidate is not None
                else None
            ),
            "recommended_model_catalog_id": (
                preview.recommended_candidate.model_catalog_id
                if preview.recommended_candidate is not None
                else None
            ),
            "recommended_model_catalog_revision": (
                preview.recommended_candidate.model_catalog_revision
                if preview.recommended_candidate is not None
                else None
            ),
            "hard_blocker_codes": list(preview.hard_blocker_codes),
            **routing_exclusion_projection(preview.exclusions),
        }
        recorded = False
        if rollout.effective_mode == AgentRoutingRolloutMode.SHADOW:
            await record_routing_operational_event(
                self.db,
                event=RoutingOperationalEvent.PREVIEW_RECORDED,
                task_id=task.id,
                actor_id=actor.id,
                values=operational_values,
            )
            recorded = True
        if preview.recommended_candidate is None:
            await record_routing_operational_event(
                self.db,
                event=RoutingOperationalEvent.NO_ELIGIBLE_CANDIDATE,
                task_id=task.id,
                actor_id=actor.id,
                values={
                    key: value
                    for key, value in operational_values.items()
                    if key
                    not in {
                        "recommended_actor_id",
                        "recommended_model_binding_id",
                        "recommended_model_binding_revision",
                        "recommended_model_catalog_id",
                        "recommended_model_catalog_revision",
                    }
                },
            )
            recorded = True
        if recorded:
            await self.db.commit()
        return preview

    @staticmethod
    def _completed_prior_lineage(
        existing_assignment: AgentTaskAssignment | None,
        *,
        selected_reasoning_tier: int,
        selected_context_tier: str,
    ) -> dict[str, Any] | None:
        """Compact pending lineage and record the governed tier comparison."""

        if existing_assignment is None:
            return None
        stored = _json_value(existing_assignment.routing_snapshot, {})
        if (
            stored.get("schema_version") != "routing-lineage-snapshot-v1"
            or stored.get("selection_pending") is not True
        ):
            return None
        stored_lineage = json.loads(
            canonical_routing_json_bytes(stored).decode("utf-8")
        )
        source_authority_verified = (
            stored_lineage.get("authority") == ROUTING_LINEAGE_AUTHORITY
        )
        if not source_authority_verified:
            raise AgentRoutingConflictError(
                "routing_lineage_authority_unverified",
                "Legacy routing lineage cannot authorize model-aware selection",
                assignment_id=existing_assignment.id,
            )
        prior_decisions = stored_lineage.get("prior_decisions")
        if not isinstance(prior_decisions, list):
            prior_decisions = []
        compact_decisions: list[dict[str, Any]] = []
        prior_tiers: list[tuple[int, str]] = []
        for raw_decision in prior_decisions[:4]:
            if not isinstance(raw_decision, dict):
                continue
            decision = {
                field: raw_decision[field]
                for field in ROUTING_DECISION_LINEAGE_FIELDS
                if field in raw_decision
            }
            eligible_summaries = decision.pop(
                "eligible_candidate_summaries",
                [],
            )
            exclusion_summaries = decision.pop(
                "exclusion_summaries",
                [],
            )
            stored_eligible_omitted = decision.get(
                "eligible_candidates_omitted"
            )
            if (
                not isinstance(stored_eligible_omitted, int)
                or isinstance(stored_eligible_omitted, bool)
                or stored_eligible_omitted < 0
            ):
                stored_eligible_omitted = 0
            decision["eligible_candidates_omitted"] = (
                stored_eligible_omitted
            ) + (
                len(eligible_summaries)
                if isinstance(eligible_summaries, list)
                else 0
            )
            stored_exclusions_omitted = decision.get(
                "exclusions_omitted"
            )
            if (
                not isinstance(stored_exclusions_omitted, int)
                or isinstance(stored_exclusions_omitted, bool)
                or stored_exclusions_omitted < 0
            ):
                stored_exclusions_omitted = 0
            decision["exclusions_omitted"] = (
                stored_exclusions_omitted
            ) + (
                len(exclusion_summaries)
                if isinstance(exclusion_summaries, list)
                else 0
            )
            reasoning_tier = decision.get("selected_reasoning_tier")
            context_tier = decision.get("selected_context_tier")
            if (
                isinstance(reasoning_tier, int)
                and reasoning_tier in {1, 2, 3}
                and context_tier in {"small", "medium", "large"}
            ):
                prior_tiers.append((reasoning_tier, str(context_tier)))
            trust_lineage = decision.get("trust_lineage")
            if isinstance(trust_lineage, dict):
                decision["trust_lineage"] = {
                    field: trust_lineage[field]
                    for field in (
                        "assessment_assessor",
                        "assessment_assessor_actor_id",
                        "preview_requested_by_actor_id",
                        "assignment_created_by_actor_id",
                        "execution_actor_id",
                        "observed_model_reported_by_actor_id",
                    )
                    if field in trust_lineage
                }
            else:
                decision.pop("trust_lineage", None)
            compact_decisions.append(decision)

        stored_source_ids = stored_lineage.get("source_assignment_ids")
        source_assignment_ids = sorted(
            {
                value
                for value in (
                    stored_source_ids
                    if isinstance(stored_source_ids, list)
                    else []
                )
                if isinstance(value, int)
                and not isinstance(value, bool)
                and value > 0
            }
        )[:20]
        stored_review_floor = stored_lineage.get("review_floor")
        if not isinstance(stored_review_floor, dict):
            stored_review_floor = {}
        review_mode = str(
            stored_review_floor.get("review_mode") or "none"
        )
        if review_mode not in REVIEW_MODE_ORDER:
            review_mode = "none"
        stored_reviewer_ids = stored_review_floor.get(
            "reviewer_profile_ids"
        )
        reviewer_profile_ids = sorted(
            {
                value
                for value in (
                    stored_reviewer_ids
                    if isinstance(stored_reviewer_ids, list)
                    else []
                )
                if isinstance(value, int)
                and not isinstance(value, bool)
                and value > 0
            }
        )[:20]
        lineage = {
            "schema_version": "routing-lineage-snapshot-v1",
            "authority": ROUTING_LINEAGE_AUTHORITY,
            "source_authority": "verified",
            "policy_version": ROUTING_POLICY_VERSION,
            "selection_pending": True,
            "task_id": existing_assignment.task_id,
            "task_version": existing_assignment.task_version,
            "purpose": "execution",
            "queue_class": (
                existing_assignment.queue_class
                if existing_assignment.queue_class in {"rework", "recovery"}
                else "rework"
            ),
            "provisional_actor_id": existing_assignment.actor_id,
            "source_assignment_ids": source_assignment_ids,
            "prior_decisions": compact_decisions,
            "review_floor": {
                "review_mode": review_mode,
                "reviewer_profile_ids": reviewer_profile_ids,
                "independence_must_be_revalidated": (
                    REVIEW_MODE_ORDER[review_mode]
                    >= REVIEW_MODE_ORDER["independent"]
                ),
            },
        }

        context_order = {"small": 1, "medium": 2, "large": 3}
        comparison_available = bool(prior_tiers)
        previous_reasoning_tier = (
            max(value[0] for value in prior_tiers)
            if comparison_available
            else None
        )
        previous_context_tier = (
            max(prior_tiers, key=lambda value: context_order[value[1]])[1]
            if comparison_available
            else None
        )
        tier_increased = bool(
            comparison_available
            and (
                selected_reasoning_tier > int(previous_reasoning_tier)
                or context_order[selected_context_tier]
                > context_order[str(previous_context_tier)]
            )
        )
        cause = stored_lineage.get("cause")
        if not isinstance(cause, dict):
            cause = {}
        failure_category = normalize_model_failure_category(
            cause.get("category")
        )
        lineage["cause"] = {
            "category": failure_category,
            "reason": "Prior routing handback required fresh selection.",
        }
        escalation_eligible = (
            failure_category in MODEL_FAILURE_CATEGORIES
        )
        if tier_increased and not escalation_eligible:
            raise AgentRoutingConflictError(
                "routing_model_escalation_not_allowed",
                "A non-model failure cannot increase the selected model tier",
                assignment_id=existing_assignment.id,
                previous_reasoning_tier=previous_reasoning_tier,
                previous_context_tier=previous_context_tier,
                selected_reasoning_tier=selected_reasoning_tier,
                selected_context_tier=selected_context_tier,
            )
        lineage["model_tier_change"] = {
            "eligible": escalation_eligible,
            "comparison_available": comparison_available,
            "previous_reasoning_tier": previous_reasoning_tier,
            "previous_context_tier": previous_context_tier,
            "selected_reasoning_tier": selected_reasoning_tier,
            "selected_context_tier": selected_context_tier,
            "applied": tier_increased,
            "reason": (
                "governed_model_failure_escalation"
                if tier_increased
                else (
                    "selected_tier_not_increased"
                    if comparison_available
                    else "prior_tier_unavailable"
                )
            ),
        }
        lineage["selection_result"] = {
            "completed_by_snapshot": True,
            "assignment_id": existing_assignment.id,
        }
        validate_routing_packet_size(
            lineage,
            label="Completed prior routing lineage",
        )
        return lineage

    async def validate_assignment_selection(
        self,
        *,
        task: Task,
        selected_actor: AgentActor,
        data: Any,
        existing_assignment: AgentTaskAssignment | None = None,
        task_assignments: Sequence[AgentTaskAssignment] | None = None,
        assignment_created_by_actor: AgentActor | None = None,
        now: datetime | None = None,
        selection_inputs_locked: bool = False,
    ) -> RoutingSelectionValidation:
        """Recompute and freeze one preview selection inside an assignment transaction."""

        del task_assignments  # The preview reloads one coherent authoritative view.
        if not selection_inputs_locked:
            await self.lock_selection_inputs(task.id)
        current_time = as_utc(now or utc_now())
        issued_at, preview_request_actor_id = self._parse_preview_id(
            data.routing_preview_id
        )
        if issued_at > current_time + timedelta(
            seconds=_PREVIEW_CLOCK_SKEW_SECONDS
        ):
            raise AgentRoutingConflictError(
                "routing_preview_invalid",
                "Routing preview issue time is in the future",
                preview_id=data.routing_preview_id,
            )
        expires_at = issued_at + timedelta(
            seconds=ROUTING_PREVIEW_TTL_SECONDS
        )
        if current_time >= expires_at:
            raise AgentRoutingConflictError(
                "routing_preview_expired",
                "Routing preview has expired",
                preview_id=data.routing_preview_id,
                generated_at=issued_at.isoformat(),
                expires_at=expires_at.isoformat(),
                server_time=current_time.isoformat(),
            )

        purpose = (
            existing_assignment.purpose
            if existing_assignment is not None
            else data.purpose
        )
        reviewer_profile_id: int | None
        if existing_assignment is not None and (
            "reviewer_profile_id" not in data.model_fields_set
        ):
            reviewer_profile_id = existing_assignment.reviewer_profile_id
        else:
            reviewer_profile_id = data.reviewer_profile_id
        expected_task_version = getattr(
            data,
            "expected_task_version",
            task.version,
        )
        preview_request = AgentRoutingPreviewCreate(
            purpose=purpose,
            assessment_id=data.assessment_id,
            expected_task_version=expected_task_version,
            reviewer_profile_id=reviewer_profile_id,
        )
        recomputed = await self._build_preview(
            task=task,
            data=preview_request,
            generated_at=issued_at,
            requesting_actor_id=preview_request_actor_id,
        )
        if not secrets.compare_digest(
            recomputed.preview_id,
            data.routing_preview_id,
        ):
            raise AgentRoutingConflictError(
                "routing_preview_stale",
                "Routing preview inputs changed and require regeneration",
                supplied_preview_id=data.routing_preview_id,
                current_preview_id=recomputed.preview_id,
                current_input_digest=recomputed.input_digest,
            )
        if not secrets.compare_digest(
            recomputed.preview_digest,
            data.routing_preview_digest,
        ):
            raise AgentRoutingConflictError(
                "routing_preview_digest_mismatch",
                "Routing preview digest does not match current authoritative evidence",
                preview_id=data.routing_preview_id,
                supplied_preview_digest=data.routing_preview_digest,
                current_preview_digest=recomputed.preview_digest,
            )

        selected = next(
            (
                candidate
                for candidate in recomputed.eligible_candidates
                if candidate.actor_id == selected_actor.id
                and candidate.model_binding_id == data.model_binding_id
            ),
            None,
        )
        if selected is None:
            selected_exclusion = next(
                (
                    exclusion
                    for exclusion in recomputed.exclusions
                    if exclusion.actor_id == selected_actor.id
                    and exclusion.model_binding_id
                    in {None, data.model_binding_id}
                ),
                None,
            )
            raise AgentRoutingConflictError(
                "routing_selection_ineligible",
                "Selected actor and model binding are not eligible",
                actor_id=selected_actor.id,
                model_binding_id=data.model_binding_id,
                hard_blocker_codes=(
                    [
                        blocker.value
                        if hasattr(blocker, "value")
                        else str(blocker)
                        for blocker in selected_exclusion.hard_blocker_codes
                    ]
                    if selected_exclusion is not None
                    else [
                        RoutingBlockerCode.NO_ELIGIBLE_CANDIDATE.value
                    ]
                ),
            )
        if selected.model_binding_revision != data.model_binding_revision:
            raise AgentRoutingConflictError(
                "routing_model_binding_revision_stale",
                "Selected model binding revision is stale",
                model_binding_id=data.model_binding_id,
                supplied_revision=data.model_binding_revision,
                current_revision=selected.model_binding_revision,
            )

        binding_result = await self.db.execute(
            select(AgentModelBinding)
            .options(selectinload(AgentModelBinding.model_catalog))
            .where(AgentModelBinding.id == data.model_binding_id)
            .with_for_update()
        )
        binding = binding_result.scalar_one_or_none()
        if (
            binding is None
            or binding.actor_id != selected_actor.id
            or not binding.selectable
            or binding.revision != data.model_binding_revision
        ):
            raise AgentRoutingConflictError(
                "routing_model_binding_stale",
                "Selected model binding changed before assignment",
                actor_id=selected_actor.id,
                model_binding_id=data.model_binding_id,
                supplied_revision=data.model_binding_revision,
                current_revision=(binding.revision if binding else None),
            )

        assessment = await self.db.get(
            TaskRoutingAssessment,
            recomputed.assessment_id,
        )
        if assessment is None:
            raise AgentRoutingConflictError(
                "routing_assessment_missing",
                "Selected routing assessment disappeared before assignment",
                assessment_id=recomputed.assessment_id,
            )
        assignment_creator_id = (
            assignment_created_by_actor.id
            if assignment_created_by_actor is not None
            else preview_request_actor_id
        )
        if assignment_creator_id <= 0:
            raise AgentPermissionError(
                "Model-aware assignments require a stored PM actor identity"
            )
        effective_reviewer_profile_id = (
            reviewer_profile_id
            if reviewer_profile_id is not None
            else (
                selected.profile_id
                if purpose == "verification"
                else None
            )
        )
        prior_lineage = self._completed_prior_lineage(
            existing_assignment,
            selected_reasoning_tier=selected.reasoning_tier,
            selected_context_tier=selected.context_tier,
        )
        snapshot = RoutingDecisionSnapshot(
            task_id=task.id,
            topology_key=recomputed.topology_key,
            topology_revision=recomputed.topology_revision,
            task_version=task.version,
            assessment_id=assessment.id,
            assessment_task_version=assessment.task_version,
            assessment_band=assessment.band,
            assessment_confidence=assessment.confidence,
            assessment_reason_codes=tuple(assessment.reason_codes),
            purpose=purpose,
            actor_id=selected.actor_id,
            actor_revision=selected.actor_revision,
            actor_queue_revision=selected.actor_queue_revision,
            profile_id=selected.profile_id,
            profile_revision=selected.profile_revision,
            capacity_owner_id=selected.capacity_owner_id,
            capacity_owner_profile_id=selected.capacity_owner_profile_id,
            model_binding_id=selected.model_binding_id,
            model_binding_revision=selected.model_binding_revision,
            model_catalog_id=selected.model_catalog_id,
            model_catalog_key=selected.model_catalog_key,
            model_catalog_revision=selected.model_catalog_revision,
            configured_model_alias=selected.configured_model_alias,
            selected_reasoning_tier=selected.reasoning_tier,
            selected_context_tier=selected.context_tier,
            resolved_model=None,
            review_mode=assessment.review_mode,
            reviewer_profile_id=effective_reviewer_profile_id,
            routing_preview_id=recomputed.preview_id,
            routing_preview_digest=recomputed.preview_digest,
            input_digest=recomputed.input_digest,
            preview_generated_at=recomputed.generated_at,
            preview_expires_at=recomputed.expires_at,
            selected_rank=selected.rank,
            adequacy_class=selected.adequacy_class,
            selection_reason_codes=(
                "hard-gates-passed",
                "deterministic-rank",
            ),
            eligible_candidate_summaries=[
                {
                    "actor_id": candidate.actor_id,
                    "profile_id": candidate.profile_id,
                    "model_binding_id": candidate.model_binding_id,
                    "model_binding_revision": candidate.model_binding_revision,
                    "model_catalog_key": candidate.model_catalog_key,
                    "rank": candidate.rank,
                    "adequacy_class": candidate.adequacy_class,
                    "cost_tier": candidate.cost_tier,
                    "latency_tier": candidate.latency_tier,
                }
                for candidate in recomputed.eligible_candidates
            ],
            exclusion_summaries=[
                {
                    "actor_id": exclusion.actor_id,
                    "model_binding_id": exclusion.model_binding_id,
                    "hard_blocker_codes": exclusion.hard_blocker_codes,
                }
                for exclusion in recomputed.exclusions
            ],
            eligible_candidates_omitted=(
                recomputed.eligible_candidates_omitted
            ),
            exclusions_omitted=recomputed.exclusions_omitted,
            rationale=selected.rationale,
            confidence=selected.confidence,
            trust_lineage={
                "assessment_assessor": assessment.assessor,
                "assessment_assessor_actor_id": assessment.assessor_actor_id,
                "preview_requested_by_actor_id": preview_request_actor_id,
                "assignment_created_by_actor_id": assignment_creator_id,
                "execution_actor_id": selected.actor_id,
                "observed_model_reported_by_actor_id": None,
            },
            prior_lineage=prior_lineage,
        )
        validate_routing_packet_size(
            snapshot,
            label="Routing decision snapshot",
        )
        return RoutingSelectionValidation(
            assessment=assessment,
            binding=binding,
            preview=recomputed,
            snapshot=snapshot,
        )
