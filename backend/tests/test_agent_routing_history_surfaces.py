"""Contract and parity coverage for routing-assessment history surfaces."""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from app import mcp_agent_tools
from app.config import get_settings
from app.mcp_server import ROUTING_READ_SCOPE_REQUIREMENT, mcp
from app.routers import agent_planning
from app.schemas.agent_routing import (
    TaskRoutingAssessmentListResponse,
    TaskRoutingAssessmentResponse,
)
from app.services.agent_routing_service import _ROUTING_READ_SCOPES


def _history() -> TaskRoutingAssessmentListResponse:
    assessment = TaskRoutingAssessmentResponse(
        id=7,
        task_id=3,
        task_version=2,
        policy_version="model-aware-routing-v1",
        band="routine",
        axes={
            "reasoning": 1,
            "ambiguity": 1,
            "context_breadth": 1,
            "risk": 1,
            "verification_burden": 1,
        },
        required_skill_levels={},
        required_model={
            "minimum_reasoning_tier": 1,
            "minimum_context_tier": "small",
            "modality_tags": ["text"],
            "tool_tags": [],
            "data_policy_tags": [],
        },
        review_mode="none",
        confidence=0.9,
        reason_codes=[],
        rationale="Assessment for the current task version.",
        assessor="routing-pm",
        assessor_actor_id=11,
        created_at=datetime(2026, 7, 27, 12, tzinfo=UTC),
        policy_conformant=True,
        is_current=True,
    )
    return TaskRoutingAssessmentListResponse(
        task_id=3,
        current_task_version=2,
        assessments=[assessment],
        total_count=2,
        omitted_count=1,
    )


@pytest.mark.contract
@pytest.mark.asyncio
async def test_routing_assessment_history_rest_and_mcp_are_bounded_and_equal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    history = _history()
    calls: list[tuple[int, int, int]] = []

    class FakeRoutingService:
        async def list_assessments(
            self,
            task_id: int,
            actor: Any,
            *,
            limit: int,
        ) -> TaskRoutingAssessmentListResponse:
            calls.append((task_id, actor.id, limit))
            return history

    service = FakeRoutingService()
    actor = SimpleNamespace(id=11)
    monkeypatch.setattr(
        mcp_agent_tools,
        "AgentRoutingService",
        lambda _db: service,
    )
    rest = await agent_planning.list_task_routing_assessments(
        3,
        actor,
        service,
        limit=1,
    )
    mcp_result = await mcp_agent_tools.list_task_routing_assessments(
        object(),
        actor,
        3,
        limit=1,
    )

    assert rest.model_dump(mode="json") == mcp_result
    assert rest.current_task_version == 2
    assert [item.task_version for item in rest.assessments] == [2]
    assert rest.total_count == 2
    assert rest.omitted_count == 1
    assert calls == [(3, 11, 1), (3, 11, 1)]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_routing_assessment_history_route_and_tool_are_registered() -> None:
    api_prefix = get_settings().api_prefix
    routes = {
        (f"{api_prefix}{route.path}", method)
        for route in agent_planning.router.routes
        for method in (getattr(route, "methods", None) or ())
    }
    tool_names = {tool.name for tool in await mcp.list_tools()}

    assert (
        "/api/agent/planning/tasks/{task_id}/routing-assessments",
        "GET",
    ) in routes
    assert "agent_list_task_routing_assessments" in tool_names
    assert ROUTING_READ_SCOPE_REQUIREMENT == _ROUTING_READ_SCOPES
