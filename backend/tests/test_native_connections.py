"""Browser-approved native sessions preserve proof, identity and revocation."""

import base64
import asyncio
from datetime import timedelta
import hashlib

import pytest
from sqlalchemy import select

from app.models.user_session import UserSession
from app.services.identity_service import digest
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store


VERIFIER = "v" * 64
CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b"=").decode()


async def start_connection():
    async with client() as native:
        response = await native.post("/api/auth/native-connections/start", json={"code_challenge": CHALLENGE})
        assert response.status_code == 201, response.text
        assert response.headers["cache-control"] == "no-store"
        return response.json()


async def approve(connection, token, csrf="csrf-0"):
    async with client(token) as browser:
        return await browser.post(f"/api/auth/native-connections/{connection['request_id']}/approve",
            headers={"X-CSRF-Token": csrf, "Origin": "https://test"},
            json={"verification_code": connection["verification_code"]})


async def exchange(connection, verifier=VERIFIER):
    async with client() as native:
        return await native.post("/api/auth/native-connections/exchange",
            json={"request_id": connection["request_id"], "code_verifier": verifier})


async def test_native_handoff_requires_browser_consent_and_exact_proof(managed_store):
    _, _, tokens, people = managed_store
    connection = await start_connection()
    assert connection["verification_path"].startswith("/mobile/connect?")
    assert (await exchange(connection)).json() == {"status": "pending"}
    denied = await approve(connection, None)
    assert denied.status_code == 401
    denied = await approve(connection, tokens[0], "incorrect")
    assert denied.status_code == 403
    wrong_proof = await exchange(connection, "x" * 64)
    assert wrong_proof.status_code == 404
    approved = await approve(connection, tokens[0])
    assert approved.status_code == 200, approved.text
    grant = await exchange(connection)
    assert grant.status_code == 200, grant.text
    assert grant.json()["token_type"] == "Bearer"
    assert grant.headers["cache-control"] == "no-store"
    async with client(**{"Authorization": "Bearer " + grant.json()["access_token"]}) as native:
        for _ in range(2):
            identity = (await native.get("/api/auth/me")).json()
            assert identity["principal"]["id"] == people[0]
        assert (await native.post("/api/auth/logout")).status_code == 200
        assert (await native.get("/api/projects")).status_code == 401
    assert (await exchange(connection)).status_code == 410


async def test_native_approval_cannot_be_switched_to_another_account(managed_store):
    _, _, tokens, _ = managed_store
    connection = await start_connection()
    assert (await approve(connection, tokens[0])).status_code == 200
    assert (await approve(connection, tokens[0])).status_code == 200
    assert (await approve(connection, tokens[1], "csrf-1")).status_code == 409


async def test_native_handoff_rechecks_approving_session_revocation(managed_store):
    factory, _, tokens, _ = managed_store
    connection = await start_connection()
    assert (await approve(connection, tokens[0])).status_code == 200
    async with factory() as db:
        session = await db.scalar(select(UserSession).where(UserSession.session_token_hash == digest(tokens[0])))
        session.revoked_at = utc_now()
        await db.commit()
    assert (await exchange(connection)).status_code == 401


async def test_native_expiration_and_input_bounds(managed_store):
    from app.models.native_connection import NativeConnection
    factory, _, tokens, _ = managed_store
    connection = await start_connection()
    async with factory() as db:
        row = await db.get(NativeConnection, digest(connection["request_id"]))
        row.expires_at = utc_now() - timedelta(seconds=1)
        await db.commit()
    assert (await approve(connection, tokens[0])).status_code == 410
    assert (await exchange(connection)).status_code == 410
    async with client() as native:
        response = await native.post("/api/auth/native-connections/start", json={"code_challenge": "bad"})
        assert response.status_code == 422


async def test_native_connection_details_require_a_human_session(managed_store):
    _, scenario, tokens, _ = managed_store
    connection = await start_connection()
    path = f"/api/auth/native-connections/{connection['request_id']}"
    async with client() as anonymous:
        assert (await anonymous.get(path)).status_code == 401
    async with client(**{"X-Agent-API-Key": scenario.actor_keys[0]}) as actor:
        assert (await actor.get(path)).status_code == 403
    async with client(tokens[0]) as browser:
        result = await browser.get(path)
        assert result.status_code == 200
        assert result.json()["verification_code"] == connection["verification_code"]
        assert "code_challenge" not in result.text


async def test_concurrent_native_exchange_issues_one_session(managed_store):
    _, _, tokens, _ = managed_store
    connection = await start_connection()
    assert (await approve(connection, tokens[0])).status_code == 200
    results = await asyncio.gather(exchange(connection), exchange(connection))
    assert sorted(response.status_code for response in results) == [200, 410]
    assert sum("access_token" in response.json() for response in results) == 1
