"""OIDC, native bearer, revocation, ownership and real MCP transport contracts."""

import base64
from datetime import timedelta
import hashlib
import json
from types import SimpleNamespace
from urllib.parse import parse_qs, urlencode, urlsplit

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from sqlalchemy import func, select

from app.config import get_settings
from app.main import app
from app.models.identity import Principal, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.saved_view import SavedView
from app.models.task import Task
from app.models.user_session import UserSession
from app.services import identity_service
from app.services.identity_service import digest, safe_return_path
from app.services.snapshot_service import SnapshotService
from app.utils.time import utc_now
from tests.test_managed_authority import managed_store, client
from tests.test_delivery_scenarios import delivery_store


async def test_oidc_code_flow_rotates_and_revokes_real_sessions(managed_store, monkeypatch):
    factory, _, _, _ = managed_store
    monkeypatch.setenv("OIDC_ISSUER_URL", "https://issuer.example")
    monkeypatch.setenv("OIDC_CLIENT_ID", "workchord-client")
    monkeypatch.setenv("OIDC_CLIENT_SECRET", "provider-fixture-secret")
    monkeypatch.setenv("OIDC_REDIRECT_URI", "https://test/api/auth/callback")
    get_settings.cache_clear()
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    jwk["kid"] = "fixture-key"
    authorization = {}
    real_client = httpx.AsyncClient

    async def provider(request):
        if request.url.path.endswith("openid-configuration"):
            return httpx.Response(200, json={"issuer": "https://issuer.example", "authorization_endpoint": "https://issuer.example/authorize",
                "token_endpoint": "https://issuer.example/token", "jwks_uri": "https://issuer.example/keys"})
        if request.url.path == "/keys":
            return httpx.Response(200, json={"keys": [jwk]})
        assert request.url.path == "/token"
        body = parse_qs(request.content.decode())
        challenge = base64.urlsafe_b64encode(hashlib.sha256(body["code_verifier"][0].encode()).digest()).rstrip(b"=").decode()
        assert challenge == authorization["code_challenge"][0]
        assert body["redirect_uri"] == ["https://test/api/auth/callback"]
        assert body["client_secret"] == ["provider-fixture-secret"]
        claims = {"iss": "https://issuer.example", "sub": "new-verified-subject", "aud": "workchord-client", "name": "Verified person",
                  "iat": int(utc_now().timestamp()), "exp": int((utc_now() + timedelta(minutes=5)).timestamp()), "nonce": authorization["nonce"][0]}
        return httpx.Response(200, json={"id_token": jwt.encode(claims, key, algorithm="RS256", headers={"kid": "fixture-key"})})

    monkeypatch.setattr(identity_service, "httpx", SimpleNamespace(AsyncClient=lambda **kwargs: real_client(transport=httpx.MockTransport(provider), **kwargs)))
    async with client() as browser:
        login = await browser.get("/api/auth/login", params={"return_to": "/tasks?task=1"})
        assert login.status_code == 303, login.text
        authorization.update(parse_qs(urlsplit(login.headers["location"]).query))
        assert authorization["code_challenge_method"] == ["S256"]
        callback = await browser.get("/api/auth/callback", params={"code": "fixture-grant", "state": authorization["state"][0]})
        assert callback.status_code == 303, callback.text
        assert callback.headers["location"] == "/tasks?task=1"
        me = (await browser.get("/api/auth/me")).json()
        assert me["authenticated"] is True
        assert me["workspace_role"] is None
        assert me["projects"] == {}
        raw = browser.cookies.get("workchord_session")
        async with factory() as db:
            stored = await db.scalar(select(UserSession).where(UserSession.session_token_hash == digest(raw)))
            assert stored.principal_id == me["principal"]["id"]
            assert stored.session_token_hash != raw
        replay = await browser.get("/api/auth/callback", params={"code": "fixture-grant", "state": authorization["state"][0]})
        assert replay.status_code == 401
        rotation = await browser.post("/api/session/rotate", headers={"X-CSRF-Token": me["csrf_token"], "Origin": "https://test"})
        assert rotation.status_code == 200, rotation.text
        async with client(**{"Authorization": "Bearer " + raw}) as old:
            assert (await old.get("/api/projects")).status_code == 401
        fresh = (await browser.get("/api/auth/me")).json()
        assert fresh["principal"]["id"] == me["principal"]["id"]
        assert fresh["csrf_token"] != me["csrf_token"]
        native = await browser.post("/api/auth/native-token", headers={"X-CSRF-Token": fresh["csrf_token"], "Origin": "https://test"})
        assert native.status_code == 200
        async with client(**{"Authorization": "Bearer " + native.json()["access_token"]}) as bearer:
            assert (await bearer.get("/api/auth/me")).json()["principal"] == fresh["principal"]
        assert (await browser.post("/api/auth/logout", headers={"X-CSRF-Token": fresh["csrf_token"]})).status_code == 200


async def test_shared_iteration_snapshots_cannot_reveal_another_project(managed_store):
    factory, scenario, tokens, people = managed_store
    async with factory() as db:
        original = await db.get(Iteration, scenario.iterations[0])
        shared = Iteration(name="Shared legacy container", calendar_id=original.calendar_id, start_date=original.start_date, end_date=original.end_date)
        db.add(shared)
        await db.flush()
        db.add_all([Task(title="Visible snapshot work", iteration_id=shared.id, project_id=scenario.projects[0]),
                    Task(title="Private snapshot work", iteration_id=shared.id, project_id=scenario.projects[1]),
                    WorkspaceMembership(principal_id=people[0], role="member")])
        await db.commit()
        filename = await SnapshotService(db).create_snapshot(shared.id, "saved")
        shared_id = shared.id
    async with client(tokens[0]) as member:
        listing = await member.get(f"/api/iterations/{shared_id}/snapshots")
        assert listing.status_code == 200, listing.text
        assert listing.json() == []
        read = await member.get(f"/api/iterations/{shared_id}/snapshots/{filename}")
        assert read.status_code == 404
        assert "Private snapshot work" not in read.text


async def test_retention_preserves_references_and_revoked_sessions_stay_revoked(managed_store):
    factory, _, tokens, people = managed_store
    async with factory() as db:
        old = UserSession(principal_id=people[0], session_token_hash=digest("o" * 43), csrf_token="old",
            ip_address="192.0.2.20", user_agent="retired-device", expires_at=utc_now() - timedelta(days=40),
            last_seen_at=utc_now() - timedelta(days=41))
        db.add(old)
        await db.flush()
        db.add(SavedView(name="Retained ownership", scope="personal", view_type="tasks", created_by_session_id=old.id, owner_principal_id=people[0]))
        await db.commit()
        old_id = old.id
    async with client(**{"X-Admin-API-Key": "managed-operator-fixture"}) as operator:
        cleanup = await operator.post("/api/auth/sessions/cleanup")
        assert cleanup.status_code == 200, cleanup.text
        assert cleanup.json()["anonymized"] == 1
        disabled = await operator.put(f"/api/auth/principals/{people[0]}", json={"enabled": False, "reason": "Revoke a compromised account session"})
        assert disabled.status_code == 200
        enabled = await operator.put(f"/api/auth/principals/{people[0]}", json={"enabled": True, "reason": "Restore access after verified recovery"})
        assert enabled.status_code == 200
    async with factory() as db:
        old = await db.get(UserSession, old_id)
        assert old.ip_address == "redacted" and old.user_agent is None and old.session_token_hash is None
        assert await db.scalar(select(func.count()).select_from(SavedView).where(SavedView.created_by_session_id == old_id)) == 1
    async with client(tokens[0]) as old_browser:
        assert (await old_browser.get("/api/projects")).status_code == 401


async def test_mcp_http_uses_the_same_principal_and_project_boundary(managed_store):
    factory, scenario, tokens, _ = managed_store
    from app import mcp_server
    fresh = mcp_server.create_mcp_server()
    transport_app = mcp_server.MCPAgentKeyMiddleware(fresh.streamable_http_app())
    mcp_server.set_mcp_session_factory(factory)
    try:
        async with fresh.session_manager.run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=transport_app), base_url="https://testserver",
                headers={"X-Agent-API-Key": scenario.actor_keys[0], "Accept": "application/json, text/event-stream"}) as worker:
                init = await worker.post("/", json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                    "protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "authority-fixture", "version": "1"}}})
                assert init.status_code == 200, init.text
                own = await worker.post("/", json={"jsonrpc": "2.0", "id": 2, "method": "resources/read", "params": {"uri": f"workchord://tasks/{scenario.tasks['planned']}"}})
                assert own.status_code == 200, own.text
                assert "Planned" in own.text
                private = await worker.post("/", json={"jsonrpc": "2.0", "id": 3, "method": "resources/read", "params": {"uri": f"workchord://tasks/{scenario.tasks['other_project']}"}})
                assert "Harbor" not in private.text
                denied = await worker.post("/", json={"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
                    "name": "agent_patch_task", "arguments": {"task_id": scenario.tasks["planned"], "payload": {"title": "Forbidden edit"}}}})
                assert denied.json()["result"]["isError"] is True
                mixed = await worker.post("/", headers={"Cookie": "workchord_session=" + tokens[0]}, json={"jsonrpc": "2.0", "id": 5, "method": "tools/list"})
                assert mixed.status_code == 401
    finally:
        mcp_server.reset_mcp_session_factory()


@pytest.mark.parametrize("value", ["//foreign.example", "/%2f%2fforeign.example", "/%255cforeign.example", "/%0aLocation:foreign", "https://foreign.example"])
def test_return_paths_stay_within_the_application(value):
    assert safe_return_path(value) == "/"
