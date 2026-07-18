"""Focused model and schema coverage for MAR-DATA-001 and MAR-DATA-002."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app import models  # noqa: F401 - register every mapped table
from app.database import Base
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    ImmutableRoutingAssessmentError,
    TaskRoutingAssessment,
)
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task
from app.schemas.agent import AgentRunResponse, AgentTaskAssignmentResponse
from app.schemas.agent_routing import (
    AgentModelBindingCreate,
    AgentModelBindingResponse,
    AgentModelCatalogCreate,
    AgentModelCatalogResponse,
    TaskRoutingAssessmentCreate,
    TaskRoutingAssessmentResponse,
)


def _catalog_values(*, key: str = "balanced-code", **overrides):
    values = {
        "key": key,
        "provider": "configured-provider",
        "configured_model_alias": key,
        "reasoning_tier": 2,
        "context_tier": "medium",
        "modality_tags": ["text"],
        "cost_tier": "medium",
        "latency_tier": "balanced",
        "enabled": True,
        "revision": 1,
    }
    values.update(overrides)
    return values


def _assessment_payload(*, task_id: int, task_version: int = 1, **overrides):
    values = {
        "task_id": task_id,
        "task_version": task_version,
        "band": "advanced",
        "axes": {
            "reasoning": 3,
            "ambiguity": 2,
            "context_breadth": 2,
            "risk": 3,
            "verification_burden": 3,
        },
        "required_skill_levels": {
            "backend-python": 4,
            "data-integrity-review": 3,
        },
        "required_model": {
            "minimum_reasoning_tier": 3,
            "minimum_context_tier": "medium",
            "modality_tags": ["text"],
            "tool_tags": ["shell", "code-edit"],
            "data_policy_tags": ["workspace-source"],
        },
        "review_mode": "specialist-independent",
        "confidence": 0.86,
        "reason_codes": ["migration", "data-integrity"],
        "rationale": "Cross-module migration with rollback requirements.",
        "assessor": "pm-controller",
    }
    values.update(overrides)
    return values


@pytest.fixture
def routing_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'workchord_test_routing_data.db'}")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        yield session
        session.rollback()
    Base.metadata.drop_all(engine)
    engine.dispose()


def _persist_task_graph(db_session: Session):
    calendar = Calendar(name="Routing calendar", year=2026)
    db_session.add(calendar)
    db_session.flush()
    iteration = Iteration(
        name="Routing iteration",
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 31),
        calendar_id=calendar.id,
    )
    actor = AgentActor(
        name="routing-worker",
        display_name="Routing Worker",
        api_key_hash="routing-worker-key-hash",
    )
    db_session.add_all([iteration, actor])
    db_session.flush()
    task = Task(title="Route this task", iteration_id=iteration.id)
    db_session.add(task)
    db_session.flush()
    return task, actor


@pytest.mark.contract
def test_catalog_and_binding_schemas_are_secret_free_and_deterministic() -> None:
    catalog = AgentModelCatalogCreate.model_validate(
        _catalog_values(key=" Balanced-Code ", modality_tags=["Vision", "text"])
    )
    assert catalog.key == "balanced-code"
    assert catalog.modality_tags == ["text", "vision"]

    binding = AgentModelBindingCreate(
        actor_id=1,
        model_catalog_id=1,
        is_default=True,
        tool_tags=["shell", "code-edit"],
        data_policy_tags=["workspace-source"],
    )
    assert binding.tool_tags == ["code-edit", "shell"]

    with pytest.raises(ValidationError, match="extra_forbidden"):
        AgentModelCatalogCreate.model_validate(
            {**_catalog_values(), "api_key": "must-never-be-stored"}
        )
    with pytest.raises(ValidationError, match="modality_tags entries must be unique"):
        AgentModelCatalogCreate.model_validate(
            _catalog_values(modality_tags=["text", "TEXT"])
        )
    with pytest.raises(ValidationError, match="less than or equal to 3"):
        AgentModelCatalogCreate.model_validate(_catalog_values(reasoning_tier=4))
    with pytest.raises(ValidationError, match="default model binding must be enabled"):
        AgentModelBindingCreate(
            actor_id=1,
            model_catalog_id=1,
            is_default=True,
            enabled=False,
        )


@pytest.mark.contract
def test_assessment_schema_rejects_unsafe_band_and_unbounded_values() -> None:
    normalized = TaskRoutingAssessmentCreate.model_validate(
        _assessment_payload(task_id=1)
    )
    assert normalized.required_model.tool_tags == ["code-edit", "shell"]
    assert normalized.reason_codes == ["data-integrity", "migration"]

    with pytest.raises(ValidationError, match="routine requires every governed axis"):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(task_id=1, band="routine")
        )
    with pytest.raises(ValidationError, match="independent review mode"):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(task_id=1, review_mode="standard")
        )
    with pytest.raises(ValidationError):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(task_id=1, confidence=float("nan"))
        )


@pytest.mark.contract
def test_legacy_assignment_and_run_responses_remain_readable() -> None:
    timestamp = datetime(2026, 7, 18, tzinfo=UTC)
    assignment = AgentTaskAssignmentResponse(
        id=1,
        task_id=2,
        actor_id=3,
        purpose="execution",
        queue_class="normal",
        state="fulfilled",
        queue_rank=1000,
        task_version=4,
        routing_snapshot={},
        created_at=timestamp,
        updated_at=timestamp,
    )
    run = AgentRunResponse(
        id=5,
        task_id=2,
        actor_id=3,
        status="succeeded",
        model="legacy-worker-report",
        metadata={},
        artifact_links=[],
        started_at=timestamp,
    )

    assert assignment.model_binding_id is None
    assert assignment.model_binding_revision is None
    assert assignment.routing_snapshot == {}
    assert run.model == "legacy-worker-report"
    assert run.model_binding_id is None
    assert run.resolved_model_id is None


@pytest.mark.sqlite
def test_multiple_bindings_allow_only_one_enabled_default(routing_session) -> None:
    db_session = routing_session
    _task, actor = _persist_task_graph(db_session)
    balanced = AgentModelCatalogEntry(**_catalog_values())
    advanced = AgentModelCatalogEntry(
        **_catalog_values(
            key="advanced-code",
            configured_model_alias="advanced-code",
            reasoning_tier=3,
            cost_tier="high",
            latency_tier="slow",
        )
    )
    db_session.add_all([balanced, advanced])
    db_session.flush()
    default_binding = AgentModelBinding(
        actor=actor,
        model_catalog=balanced,
        is_default=True,
        enabled=True,
    )
    alternate_binding = AgentModelBinding(
        actor=actor,
        model_catalog=advanced,
        is_default=False,
        enabled=True,
    )
    db_session.add_all([default_binding, alternate_binding])
    db_session.flush()
    assert default_binding.selectable is True
    assert alternate_binding.selectable is True

    alternate_binding.is_default = True
    with pytest.raises(IntegrityError):
        db_session.flush()


@pytest.mark.sqlite
@pytest.mark.parametrize(
    "overrides",
    [
        {"key": "invalid-tier", "reasoning_tier": 4},
        {"key": "Not-Canonical"},
    ],
)
def test_catalog_database_constraints_fail_closed(
    routing_session,
    overrides,
) -> None:
    db_session = routing_session
    invalid = AgentModelCatalogEntry(**_catalog_values(**overrides))
    db_session.add(invalid)
    with pytest.raises(IntegrityError):
        db_session.flush()


@pytest.mark.sqlite
def test_duplicate_catalog_keys_fail_at_database_boundary(routing_session) -> None:
    db_session = routing_session
    db_session.add_all(
        [
            AgentModelCatalogEntry(**_catalog_values()),
            AgentModelCatalogEntry(**_catalog_values()),
        ]
    )
    with pytest.raises(IntegrityError):
        db_session.flush()


@pytest.mark.sqlite
def test_referenced_binding_cannot_be_deleted_and_can_be_disabled(routing_session) -> None:
    db_session = routing_session
    task, actor = _persist_task_graph(db_session)
    catalog = AgentModelCatalogEntry(**_catalog_values())
    db_session.add(catalog)
    db_session.flush()
    binding = AgentModelBinding(
        actor_id=actor.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        revision=3,
    )
    db_session.add(binding)
    db_session.flush()
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=actor.id,
        task_version=task.version,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_snapshot='{"model_binding_revision":3}',
    )
    db_session.add(assignment)
    db_session.flush()
    run = AgentRun(
        task_id=task.id,
        actor_id=actor.id,
        assignment_id=assignment.id,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        configured_model_alias=catalog.configured_model_alias,
        resolved_model_id="provider/model-actual",
        model="provider/model-actual",
    )
    db_session.add(run)
    db_session.commit()
    binding_id = binding.id
    assignment_id = assignment.id
    run_id = run.id

    db_session.delete(binding)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()

    stored = db_session.scalar(
        select(AgentModelBinding)
        .options(selectinload(AgentModelBinding.model_catalog))
        .where(AgentModelBinding.id == binding_id)
    )
    assert stored is not None
    stored.is_default = False
    stored.enabled = False
    db_session.commit()
    assert stored.selectable is False
    stored_assignment = db_session.get(AgentTaskAssignment, assignment_id)
    stored_run = db_session.get(AgentRun, run_id)
    assert stored_assignment is not None
    assert stored_run is not None
    assert stored_assignment.model_binding_revision == 3
    assert stored_run.configured_model_alias == "balanced-code"
    assert stored_run.resolved_model_id == "provider/model-actual"


@pytest.mark.sqlite
def test_assessment_round_trip_staleness_and_immutability(routing_session) -> None:
    db_session = routing_session
    task, actor = _persist_task_graph(db_session)
    payload = TaskRoutingAssessmentCreate.model_validate(
        _assessment_payload(
            task_id=task.id,
            task_version=task.version,
            assessor_actor_id=actor.id,
        )
    )
    assessment = TaskRoutingAssessment(**payload.model_values())
    db_session.add(assessment)
    db_session.commit()

    current = TaskRoutingAssessmentResponse.from_record(
        assessment,
        current_task_version=task.version,
    )
    stale = TaskRoutingAssessmentResponse.from_record(
        assessment,
        current_task_version=task.version + 1,
    )
    assert current.is_current is True
    assert stale.is_current is False
    assert assessment.is_current_for(task.version) is True
    assert current.required_skill_levels["backend-python"] == 4

    assessment.rationale = "Mutated evidence"
    with pytest.raises(ImmutableRoutingAssessmentError):
        db_session.flush()


@pytest.mark.sqlite
def test_binding_schema_round_trip_exposes_selection_state(routing_session) -> None:
    db_session = routing_session
    _task, actor = _persist_task_graph(db_session)
    catalog = AgentModelCatalogEntry(**_catalog_values())
    binding = AgentModelBinding(
        actor=actor,
        model_catalog=catalog,
        is_default=True,
        enabled=True,
        tool_tags=["code-edit"],
    )
    db_session.add(binding)
    db_session.commit()

    response = AgentModelBindingResponse.model_validate(binding)
    catalog_response = AgentModelCatalogResponse.model_validate(catalog)
    assert response.model_catalog_key == "balanced-code"
    assert response.selectable is True
    assert catalog_response.key == "balanced-code"
