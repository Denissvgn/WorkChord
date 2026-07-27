"""Compatibility coverage for persisted and projected run-model trust evidence."""

from __future__ import annotations

from datetime import UTC, datetime
import json
from typing import Any

import pytest

from app.models.agent import AgentActor, AgentRun
from app.routers.agent import _run_detail_response, _run_response
from app.schemas.agent import AgentRunCreate
from app.services.agent_service import AgentService


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("reported_model", "expected_trust_state"),
    [
        (None, "unreported"),
        ("   ", "unreported"),
        ("legacy-runtime-alias", "unverifiable"),
    ],
)
async def test_legacy_run_start_classifies_reported_model_evidence(
    monkeypatch: pytest.MonkeyPatch,
    reported_model: str | None,
    expected_trust_state: str,
) -> None:
    class RecordingSession:
        added: AgentRun | None = None

        def add(self, value: AgentRun) -> None:
            self.added = value

        async def flush(self) -> None:
            assert self.added is not None
            self.added.id = 1

        async def commit(self) -> None:
            return None

        async def refresh(self, _value: Any) -> None:
            return None

    async def suppress_webhook(*_args, **_kwargs) -> None:
        return None

    monkeypatch.setattr(
        "app.services.agent_service.emit_outbound_webhook_event",
        suppress_webhook,
    )
    actor = AgentActor(
        id=7,
        name="legacy-runner",
        display_name="Legacy Runner",
        api_key_hash="legacy-runner-key-hash",
        scopes=json.dumps(["runs:write"]),
    )
    session = RecordingSession()

    run = await AgentService(session).start_run(  # type: ignore[arg-type]
        actor,
        AgentRunCreate(model=reported_model),
    )

    assert session.added is run
    assert run.model_trust_state == expected_trust_state
    assert run.model_match_basis is None


@pytest.mark.contract
def test_rest_run_projections_preserve_binding_and_model_trust_evidence() -> None:
    timestamp = datetime(2026, 7, 27, 12, tzinfo=UTC)
    run = AgentRun(
        id=17,
        task_id=23,
        actor_id=29,
        assignment_id=31,
        claim_generation=3,
        status="succeeded",
        trace_id="trace-model-trust",
        model_binding_id=37,
        model_binding_revision=5,
        configured_model_alias="runtime-model-alias",
        resolved_model_id="catalog-model-key",
        model_trust_state="matched",
        model_match_basis="catalog_key",
        model="catalog-model-key",
        run_metadata="{}",
        artifact_links="[]",
        started_at=timestamp,
        ended_at=timestamp,
        heartbeat_at=timestamp,
    )
    service = AgentService(None)  # type: ignore[arg-type]

    response = _run_response(service, run)
    detail = _run_detail_response(service, run)

    for projection in (response, detail):
        assert projection.model_binding_id == 37
        assert projection.model_binding_revision == 5
        assert projection.configured_model_alias == "runtime-model-alias"
        assert projection.resolved_model_id == "catalog-model-key"
        assert projection.model_trust_state == "matched"
        assert projection.model_match_basis == "catalog_key"
