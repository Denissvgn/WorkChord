"""Real principal, transport, scoped-read and command-denial contracts."""

from datetime import timedelta
import json

import httpx
import jwt
import pytest
import pytest_asyncio
from cryptography.hazmat.primitives.asymmetric import rsa
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError

from app.config import get_settings
from app.main import app
from app.models.identity import Principal, IdentitySubject, ProjectMembership, WorkspaceMembership, WorkspaceAuthorityState
from app.models.recovery import ApplicationSnapshot
from app.models.saved_view import SavedView
from app.models.task import Task
from app.models.user_session import UserSession
from app.services.identity_service import digest, validate_id_token
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


@pytest_asyncio.fixture
async def managed_store(delivery_store, monkeypatch):
    factory, scenario, snapshots = delivery_store
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("CORS_ORIGINS", '["https://test"]')
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "managed-operator-fixture")
    get_settings.cache_clear()
    tokens = ["a" * 43, "b" * 43]
    async with factory() as db:
        humans = [Principal(kind="human", display_name="Same display name") for _ in range(2)]
        system = Principal(kind="system", display_name="Operator API")
        db.add_all([*humans, system])
        await db.flush()
        db.add(WorkspaceAuthorityState(id=1, operator_principal_id=system.id))
        for i, human in enumerate(humans):
            db.add(IdentitySubject(principal_id=human.id, issuer="https://issuer.example", subject=f"subject-{i}"))
            db.add(ProjectMembership(principal_id=human.id, project_id=scenario.projects[i], role="editor"))
            db.add(UserSession(principal_id=human.id, session_token_hash=digest(tokens[i]), csrf_token=f"csrf-{i}",
                ip_address="192.0.2.1", user_agent="same-browser", authenticated_at=utc_now(), expires_at=utc_now() + timedelta(hours=1)))
        worker = Principal(kind="agent", display_name="Worker", agent_actor_id=scenario.actors[0])
        db.add(worker)
        await db.flush()
        db.add(ProjectMembership(principal_id=worker.id, project_id=scenario.projects[0], role="executor"))
        await db.commit()
        principal_ids = [p.id for p in humans]
    try:
        yield factory, scenario, tokens, principal_ids
    finally:
        get_settings.cache_clear()


def client(token=None, **headers):
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="https://test",
        cookies={"workchord_session": token} if token else {}, headers=headers)


async def test_managed_mode_rejects_missing_forged_and_conflicting_identity(managed_store):
    _, scenario, tokens, _ = managed_store
    async with client() as anonymous:
        assert (await anonymous.get("/api/projects")).status_code == 401
    async with client("forged") as forged:
        assert (await forged.get("/api/projects")).status_code == 401
    async with client(tokens[0], **{"X-Agent-API-Key": scenario.actor_keys[0]}) as mixed:
        response = await mixed.get("/api/projects")
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "conflicting_credentials"


async def test_project_reads_hide_unrelated_ids_counts_and_people(managed_store):
    _, scenario, tokens, _ = managed_store
    async with client(tokens[0]) as first:
        projects = await first.get("/api/projects")
        assert projects.status_code == 200, projects.text
        assert [p["id"] for p in projects.json()] == [scenario.projects[0]]
        for path in [f"/api/projects/{scenario.projects[1]}", f"/api/tasks/{scenario.tasks['other_project']}",
                     f"/api/iterations/{scenario.iterations[1]}/snapshots"]:
            result = await first.get(path)
            assert result.status_code in {403, 404}, (path, result.text)
            assert "Harbor" not in result.text
        own = await first.get(f"/api/iterations/{scenario.iterations[0]}/tasks")
        assert own.status_code == 200, own.text
        assert "Harbor" not in own.text
        me = await first.get("/api/auth/me")
        assert me.json()["workspace_role"] is None
        assert me.json()["authenticated"] is True


async def test_cookie_mutations_require_request_integrity(managed_store):
    _, scenario, tokens, _ = managed_store
    path = f"/api/tasks/{scenario.tasks['planned']}"
    async with client(tokens[0]) as first:
        denied = await first.put(path, json={"title": "Missing integrity"})
        assert denied.status_code == 403
        allowed = await first.put(path, json={"title": "Authorized edit", "expected_version": 1},
            headers={"X-CSRF-Token": "csrf-0", "Origin": "https://test"})
        assert allowed.status_code == 200, allowed.text
        assert (await first.get(path)).json()["title"] == "Authorized edit"
        cross_site = await first.put(path, json={"title": "Wrong origin"},
            headers={"X-CSRF-Token": "csrf-0", "Origin": "https://foreign.example"})
        assert cross_site.status_code == 403


async def test_execution_actor_cannot_accept_via_ordinary_status_route(managed_store):
    factory, scenario, _, _ = managed_store
    async with factory() as db:
        before_snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as worker:
        response = await worker.put(f"/api/tasks/{scenario.tasks['resolved']}/status", json={"status": "closed", "expected_version": 1})
        assert response.status_code == 403, response.text
        assert response.json()["detail"]["code"] == "independent_review_required"
    async with factory() as db:
        assert (await db.get(Task, scenario.tasks["resolved"])).status == "resolved"
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == before_snapshots


async def test_viewer_cannot_reorder_via_bulk_sql(managed_store):
    factory, scenario, tokens, ids = managed_store
    async with factory() as db:
        membership = await db.get(ProjectMembership, (ids[0], scenario.projects[0]))
        membership.role = "viewer"
        await db.commit()
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0"}) as viewer:
        response = await viewer.post("/api/tasks/reorder", json={"task_ids": [scenario.tasks["active"], scenario.tasks["planned"]], "iteration_id": scenario.iterations[0]})
        assert response.status_code == 403, response.text


async def test_guest_transfer_requires_token_and_preserves_original_attribution(managed_store):
    factory, _, tokens, ids = managed_store
    proof = "g" * 43
    async with factory() as db:
        guest = UserSession(session_token_hash=digest(proof), ip_address="192.0.2.9", expires_at=utc_now() + timedelta(days=1))
        db.add(guest)
        await db.flush()
        view = SavedView(name="Guest view", scope="personal", view_type="tasks", created_by_session_id=guest.id)
        db.add(view)
        await db.commit()
        guest_id, view_id = guest.id, view.id
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0"}) as human:
        denied = await human.post("/api/auth/transfer-guest", json={"guest_session_id": guest_id})
        assert denied.status_code == 403
        transferred = await human.post("/api/auth/transfer-guest", json={"guest_token": proof})
        assert transferred.status_code == 200, transferred.text
        again = await human.post("/api/auth/transfer-guest", json={"guest_token": proof})
        assert again.status_code == 200
        assert again.json()["already_transferred"] is True
    async with factory() as db:
        view = await db.get(SavedView, view_id)
        assert view.owner_principal_id == ids[0]
        assert view.created_by_session_id == guest_id
        assert (await db.get(UserSession, guest_id)).principal_id is None
    async with client(tokens[1], **{"X-CSRF-Token": "csrf-1"}) as other:
        assert (await other.post("/api/auth/transfer-guest", json={"guest_token": proof})).status_code == 403


async def test_logout_revokes_bearer_and_cookie_access(managed_store):
    _, _, tokens, _ = managed_store
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0"}) as human:
        assert (await human.post("/api/auth/logout")).status_code == 200
    async with client(**{"Authorization": "Bearer " + tokens[0]}) as replay:
        assert (await replay.get("/api/projects")).status_code == 401


async def test_issuer_subject_unique_without_name_or_ip_identity(managed_store):
    factory, _, _, ids = managed_store
    assert ids[0] != ids[1]
    async with factory() as db:
        db.add(IdentitySubject(principal_id=ids[1], issuer="https://issuer.example", subject="subject-0"))
        with pytest.raises(IntegrityError):
            await db.flush()
        await db.rollback()


def test_oidc_signature_nonce_issuer_audience_and_expiry(monkeypatch):
    monkeypatch.setenv("OIDC_ISSUER_URL", "https://issuer.example")
    monkeypatch.setenv("OIDC_CLIENT_ID", "workchord-client")
    get_settings.cache_clear()
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    jwk["kid"] = "trusted"
    claims = {"iss": "https://issuer.example", "sub": "verified-subject", "aud": "workchord-client",
              "iat": int(utc_now().timestamp()), "exp": int((utc_now() + timedelta(minutes=5)).timestamp()), "nonce": "bound-nonce"}
    token = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "trusted"})
    assert validate_id_token(token, {"keys": [jwk]}, "bound-nonce")["sub"] == "verified-subject"
    from app.authority import AuthorityError
    for override in [{"iss": "https://wrong.example"}, {"aud": "wrong-client"}, {"nonce": "wrong-nonce"}, {"exp": 1}]:
        invalid = jwt.encode({**claims, **override}, key, algorithm="RS256", headers={"kid": "trusted"})
        with pytest.raises(AuthorityError):
            validate_id_token(invalid, {"keys": [jwk]}, "bound-nonce")
    forged = jwt.encode(claims, "attacker-supplied-secret-with-32-characters", algorithm="HS256", headers={"kid": "trusted"})
    with pytest.raises(AuthorityError):
        validate_id_token(forged, {"keys": [jwk]}, "bound-nonce")
    get_settings.cache_clear()


async def test_viewer_denials_cover_alternate_commands_and_private_reads(managed_store):
    factory, scenario, tokens, ids = managed_store
    async with factory() as db:
        (await db.get(ProjectMembership, (ids[0], scenario.projects[0]))).role = "viewer"
        await db.commit()
        before = [(task.id, task.version, task.title, task.status) for task in (await db.scalars(select(Task).order_by(Task.id))).all()]
        snapshots = await db.scalar(select(func.count()).select_from(ApplicationSnapshot))
    task_id, iteration_id = scenario.tasks["planned"], scenario.iterations[0]
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0"}) as viewer:
        for method, path, body in [
            ("PUT", f"/api/tasks/{task_id}", {"title": "Denied"}),
            ("DELETE", f"/api/tasks/{task_id}", None),
            ("POST", f"/api/tasks/{task_id}/ai/suggest", {"intent": "improve_description"}),
            ("POST", f"/api/iterations/{iteration_id}/tasks/merge", {"task_ids": [task_id, scenario.tasks["active"]], "parent_title": "Denied"}),
            ("POST", f"/api/iterations/{iteration_id}/tasks/batch-update", {"tasks": [{"task_id": task_id, "update": {"title": "Denied"}}]}),
            ("POST", f"/api/iterations/{iteration_id}/schedule", {}),
        ]:
            result = await viewer.request(method, path, json=body)
            assert result.status_code == 403, (method, path, result.status_code, result.text)
        for path in [f"/api/tasks/{scenario.tasks['other_project']}/timeline", f"/api/tasks/{scenario.tasks['other_project']}/status-history",
                     f"/api/iterations/{scenario.iterations[1]}/gantt", f"/api/projects/{scenario.projects[1]}/summary"]:
            result = await viewer.get(path)
            assert result.status_code in {403, 404}, (path, result.text)
            assert "Harbor" not in result.text
    async with factory() as db:
        assert [(task.id, task.version, task.title, task.status) for task in (await db.scalars(select(Task).order_by(Task.id))).all()] == before
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == snapshots


async def test_editor_relationship_change_uses_the_shared_version_boundary(managed_store):
    factory, scenario, tokens, _ = managed_store
    task_id = scenario.tasks["planned"]
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0"}) as editor:
        result = await editor.post(f"/api/tasks/{task_id}/external-links", json={"provider": "custom", "url": "https://example.com/artifact"})
        assert result.status_code == 201, result.text
        task = (await editor.get(f"/api/tasks/{task_id}")).json()
        assert task["version"] == 2
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(ApplicationSnapshot)) == 1


async def test_worker_bulk_sql_cannot_bypass_review_authority(managed_store):
    from app.authority import Authority, AuthorityError
    from app.commands import command_transaction
    factory, scenario, _, _ = managed_store
    async with factory() as db:
        principal = await db.scalar(select(Principal).where(Principal.agent_actor_id == scenario.actors[0]))
        db.info['authority'] = Authority(principal.id, 'agent', projects={scenario.projects[0]: 'editor'},
            actor_id=scenario.actors[0], actor_role='worker', scopes=frozenset({'tasks:write'}))
        with pytest.raises(AuthorityError, match='Execution cannot accept'):
            async with command_transaction(db):
                await db.execute(update(Task).where(Task.id == scenario.tasks['resolved']).values(status='closed'))
    async with factory() as db:
        assert (await db.get(Task, scenario.tasks['resolved'])).status == 'resolved'
