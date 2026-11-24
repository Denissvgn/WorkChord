"""Malformed evidence digests get the same refusal on the REST and MCP planning reconciliation routes."""

import json

import httpx
import pytest

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.services.agent_service import hash_api_key
from app.services.identity_service import initialize_control_plane
from app.services.planning_window_reconciliation import INVALID_EVIDENCE_DIGEST_MESSAGE, reconcile_window
from tests.test_review_provenance_transports import databases
from tests.test_team_pm_dispatch import db_session_factory  # noqa: F401

MALFORMED_DIGESTS = {
    "empty": "",
    "short": "a" * 63,
    "long": "a" * 65,
    "uppercase": "A" * 64,
    "non_hex": "g" * 64,
    "non_ascii": "é" + "a" * 63,
    "trailing_newline": "a" * 64 + "\n",
}


@pytest.mark.parametrize("digest", MALFORMED_DIGESTS.values(), ids=MALFORMED_DIGESTS.keys())
@pytest.mark.parametrize("apply", [False, True])
async def test_service_refuses_malformed_digest_before_any_comparison(digest, apply):
    with pytest.raises(ValueError, match="64 lowercase hexadecimal") as raised:
        await reconcile_window(
            None,
            None,
            1,
            apply=apply,
            expected_evidence_digest=digest,
            idempotency_key="malformed-digest",
            rationale="Reject a malformed digest",
            correlation_id="malformed-digest",
        )
    assert str(raised.value) == INVALID_EVIDENCE_DIGEST_MESSAGE


@pytest.fixture
async def admin_key(db_session, db_session_factory, actor_factory, monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    await initialize_control_plane(db_session)
    key = "malformed-digest-admin"
    await actor_factory(role="pm", scopes='["admin"]', api_key_hash=hash_api_key(key))
    await db_session.commit()
    yield key
    get_settings.cache_clear()


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("digest", MALFORMED_DIGESTS.values(), ids=MALFORMED_DIGESTS.keys())
async def test_rest_refuses_malformed_digest_as_validation_error(db_session_factory, admin_key, digest):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http:
        response = await http.post(
            "/api/agent/tasks/1/reconcile-planning-window",
            params={"expected_evidence_digest": digest},
            headers={"X-Agent-API-Key": admin_key},
        )
    assert response.status_code == 422, response.text


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("digest", MALFORMED_DIGESTS.values(), ids=MALFORMED_DIGESTS.keys())
@pytest.mark.parametrize("apply", [False, True])
async def test_mcp_refuses_malformed_digest_with_typed_code(db_session_factory, admin_key, digest, apply):
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    arguments = {"task_id": 1, "apply": apply, "expected_evidence_digest": digest}
    if apply:
        arguments.update(
            idempotency_key="malformed-digest",
            rationale="Reject a malformed digest",
            correlation_id="malformed-digest",
        )
    async with (
        server.session_manager.run(),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001") as client,
    ):
        response = await client.post(
            "/",
            headers={"X-Agent-API-Key": admin_key, "Accept": "application/json, text/event-stream"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "agent_reconcile_planning_window", "arguments": arguments},
            },
        )
    result = response.json()["result"]
    assert result["isError"], result
    text = result["content"][0]["text"]
    error = json.loads(text[text.index("{"):])
    assert error == {"code": "agent_validation_error", "message": INVALID_EVIDENCE_DIGEST_MESSAGE}, error
