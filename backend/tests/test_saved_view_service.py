"""Saved-view task filter normalization and matching behavior."""

from math import nan
from types import SimpleNamespace
from typing import Any, cast

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession
from app.schemas.saved_view import SavedViewCreateRequest, SavedViewType
from app.services.saved_view_service import SavedViewService


def service_without_database() -> SavedViewService:
    return SavedViewService(cast(AsyncSession, None))


def task_response(
    *,
    assignee: Any = None,
    effort_days: Any = 1,
    is_deferred: bool = False,
    is_composite: bool = False,
    children: list[Any] | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        assignee=assignee,
        effort_days=effort_days,
        is_deferred=is_deferred,
        is_composite=is_composite,
        children=children or [],
        project_id=None,
        priority=5,
        status="planned",
        dependencies=[],
        is_overdue=False,
        agent_readiness=SimpleNamespace(is_ready=True),
        start_date=None,
        end_date=None,
        tags=[],
    )


@pytest.mark.parametrize(
    "planning_issue",
    [None, "unassigned", "missing-effort", "any"],
)
def test_task_planning_issue_filter_normalizes_supported_values(
    planning_issue: str | None,
) -> None:
    filters, is_valid, invalid_reason = service_without_database().normalize_filters(
        SavedViewType.TASKS,
        {"planningIssue": planning_issue},
    )

    assert is_valid is True
    assert invalid_reason is None
    assert filters["planningIssue"] == planning_issue


@pytest.mark.parametrize(
    "planning_issue",
    ["", "missing_effort", "UNASSIGNED", True, ["unassigned"]],
)
def test_task_planning_issue_filter_rejects_unknown_values(
    planning_issue: Any,
) -> None:
    filters, is_valid, invalid_reason = service_without_database().normalize_filters(
        SavedViewType.TASKS,
        {"planningIssue": planning_issue},
    )

    assert filters == {}
    assert is_valid is False
    assert invalid_reason is not None
    assert "planningIssue" in invalid_reason


@pytest.mark.asyncio
async def test_task_planning_issue_filter_persists_in_saved_view(
    db_session: AsyncSession,
) -> None:
    owner = UserSession(
        public_id="planningview",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )
    db_session.add(owner)
    await db_session.flush()

    service = SavedViewService(db_session)
    created = await service.create_for_session(
        SavedViewCreateRequest(
            name="Planning blockers",
            view_type=SavedViewType.TASKS,
            filters_json={"planningIssue": "any"},
        ),
        owner.id,
    )

    stored = await service.get_by_id(created.id)
    visible = await service.get_visible_by_id(created.id, owner.id)

    assert stored is not None
    assert stored.filters_json["planningIssue"] == "any"
    assert visible is not None
    assert visible.filters_json["planningIssue"] == "any"


def test_task_planning_issue_matching_uses_planning_leaf_semantics() -> None:
    service = service_without_database()
    assigned = SimpleNamespace(id=7)

    unassigned = task_response(assignee=None, effort_days=2)
    missing_effort = task_response(assignee=assigned, effort_days=0)
    both = task_response(assignee=None, effort_days=nan)
    ready = task_response(assignee=assigned, effort_days=2)

    assert service._task_matches_planning_issue(unassigned, "unassigned") is True
    assert service._task_matches_planning_issue(unassigned, "missing-effort") is False
    assert service._task_matches_planning_issue(missing_effort, "unassigned") is False
    assert service._task_matches_planning_issue(missing_effort, "missing-effort") is True
    assert service._task_matches_planning_issue(both, "any") is True
    assert service._task_matches_planning_issue(ready, "any") is False

    assert service._task_matches_planning_issue(
        task_response(assignee=None, effort_days=0, is_deferred=True),
        "any",
    ) is False
    assert service._task_matches_planning_issue(
        task_response(assignee=None, effort_days=0, is_composite=True),
        "any",
    ) is False
    assert service._task_matches_planning_issue(
        task_response(
            assignee=None,
            effort_days=0,
            children=[task_response(assignee=None, effort_days=1)],
        ),
        "any",
    ) is False


def test_task_planning_issue_filter_preserves_matching_child_context() -> None:
    service = service_without_database()
    matching_child = task_response(assignee=None, effort_days=2)
    parent = task_response(
        assignee=None,
        effort_days=0,
        is_composite=True,
        children=[matching_child],
    )
    filters, is_valid, _ = service.normalize_filters(
        SavedViewType.TASKS,
        {"planningIssue": "unassigned"},
    )

    assert is_valid is True
    assert service._task_matches_filters(parent, filters, {}) is False
    assert service._task_filter_includes_row(parent, filters, {}) is True
