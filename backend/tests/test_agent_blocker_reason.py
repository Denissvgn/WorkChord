"""An agent-reported blocker becomes the task's human-readable Blocked reason."""

from __future__ import annotations

import pytest

from app.services.agent_service import (
    MAX_BLOCKER_REASON_CHARS,
    blocker_reason_from_payload,
)


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"blocker": "  Database credentials are missing  "}, "Database credentials are missing"),
        ({"summary": "Waiting for API access", "impact": "high"}, "Waiting for API access"),
        ({"blocker": "", "reason": "Upstream service is down"}, "Upstream service is down"),
        ({"message": "Cannot reach the staging host"}, "Cannot reach the staging host"),
    ],
)
def test_reason_uses_the_first_meaningful_text_field(payload, expected) -> None:
    assert blocker_reason_from_payload(payload) == expected


@pytest.mark.parametrize("payload", [{}, {"blocker": 3}, {"impact": "high"}, None, ["blocker"]])
def test_reason_falls_back_to_a_neutral_sentence(payload) -> None:
    assert blocker_reason_from_payload(payload) == "Blocker reported by the assigned agent."


def test_reason_is_bounded() -> None:
    reason = blocker_reason_from_payload({"blocker": "x" * (MAX_BLOCKER_REASON_CHARS + 50)})
    assert len(reason) == MAX_BLOCKER_REASON_CHARS
