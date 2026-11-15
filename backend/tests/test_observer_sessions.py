"""Paired observer sessions read like their principal, change nothing, and renew within a cap."""

import base64
from datetime import timedelta
import hashlib

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import func, select

from app.config import Settings, get_settings
from app.models.user_session import UserSession
from app.services.identity_service import digest
from app.utils.time import as_utc, utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store


VERIFIER = "o" * 64
CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b"=").decode()
OBSERVER_CAP = timedelta(days=30)
PERSON_CAP = timedelta(days=7)


@pytest_asyncio.fixture
async def local_store(delivery_store, monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    try:
        yield delivery_store
    finally:
        get_settings.cache_clear()


def bearer(token):
    return client(**{"Authorization": "Bearer " + token})


async def start(access="observe", label="Desk reader"):
    async with client() as device:
        return await device.post("/api/auth/native-connections/start",
                                 json={"code_challenge": CHALLENGE, "access": access, "client_label": label})


async def exchange(connection):
    async with client() as device:
        return await device.post("/api/auth/native-connections/exchange",
                                 json={"request_id": connection["request_id"], "code_verifier": VERIFIER})


async def approve_with(browser, connection, label="Desk reader"):
    details = await browser.get(f"/api/auth/native-connections/{connection['request_id']}")
    assert details.status_code == 200, details.text
    assert details.json()["access"] == "observe"
    assert details.json()["client_label"] == label
    approved = await browser.post(f"/api/auth/native-connections/{connection['request_id']}/approve",
                                  json={"verification_code": connection["verification_code"]})
    assert approved.status_code == 200, approved.text


async def pair_managed(token, csrf, label="Desk reader"):
    started = await start(label=label)
    assert started.status_code == 201, started.text
    connection = started.json()
    assert connection["access"] == "observe"
    async with client(token, **{"X-CSRF-Token": csrf, "Origin": "https://test"}) as browser:
        await approve_with(browser, connection, label)
    grant = await exchange(connection)
    assert grant.status_code == 200, grant.text
    return grant.json()


async def session_row(factory, token):
    async with factory() as db:
        return await db.scalar(select(UserSession).where(UserSession.session_token_hash == digest(token)))


async def move_sign_in(factory, token, *, ago):
    async with factory() as db:
        row = await db.scalar(select(UserSession).where(UserSession.session_token_hash == digest(token)))
        row.authenticated_at = utc_now() - ago
        await db.commit()


async def session_count(factory):
    async with factory() as db:
        return await db.scalar(select(func.count()).select_from(UserSession))


def assert_read_only(response):
    assert response.status_code == 403, response.text
    assert response.json()["detail"]["code"] == "read_only_credential"


async def test_managed_observer_reads_as_its_person_and_changes_nothing(managed_store):
    factory, scenario, tokens, people = managed_store
    grant = await pair_managed(tokens[0], "csrf-0")
    assert grant["access"] == "observe"
    issued = await session_row(factory, grant["access_token"])
    assert issued.principal_id == people[0] and issued.client_label == "Desk reader" and issued.csrf_token is None
    assert as_utc(issued.expires_at) <= utc_now() + timedelta(hours=24, seconds=5)
    task = scenario.tasks["planned"]
    async with bearer(grant["access_token"]) as observer:
        me = (await observer.get("/api/auth/me")).json()
        assert me["principal"]["id"] == people[0]
        assert me["access"] == "observe"
        assert me["observer"]["client_label"] == "Desk reader"
        assert me["csrf_token"] is None
        projects = await observer.get("/api/projects")
        assert [p["id"] for p in projects.json()] == [scenario.projects[0]]
        assert (await observer.get(f"/api/tasks/{task}")).status_code == 200
        assert (await observer.get(f"/api/tasks/{scenario.tasks['other_project']}")).status_code in {403, 404}
        before = await session_count(factory)
        assert (await observer.get("/api/session/whoami")).status_code == 200
        assert await session_count(factory) == before
        listed = (await observer.get("/api/auth/sessions")).json()
        assert [(row["current"], row["access"]) for row in listed] == [(True, "observe")]
        browser_session = await session_row(factory, tokens[0])
        for method, path, body in [
            ("PUT", f"/api/tasks/{task}", {"title": "Changed by an observer"}),
            ("POST", "/api/projects", {"name": "Observer project"}),
            ("PUT", f"/api/tasks/{task}/subscription", {"subscribed": True}),
            ("POST", "/api/saved-views", {"name": "Mine", "view_type": "tasks"}),
            ("POST", "/api/session/rotate", None),
            ("DELETE", f"/api/auth/sessions/{browser_session.public_id}", None),
        ]:
            assert_read_only(await observer.request(method, path, json=body))
        assert (await observer.post("/api/auth/logout")).status_code == 200
        assert (await observer.get("/api/projects")).status_code == 401
    async with client(tokens[0]) as browser:
        assert (await browser.get(f"/api/tasks/{task}")).json()["title"] != "Changed by an observer"


async def test_observer_cannot_approve_pairings_or_travel_with_another_credential(managed_store):
    _, _, tokens, _ = managed_store
    grant = await pair_managed(tokens[0], "csrf-0")
    other = (await start(label="Second reader")).json()
    async with bearer(grant["access_token"]) as observer:
        details = await observer.get(f"/api/auth/native-connections/{other['request_id']}")
        assert details.status_code == 403
    async with client(tokens[0], **{"Authorization": "Bearer " + grant["access_token"]}) as mixed:
        response = await mixed.get("/api/projects")
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "conflicting_credentials"


async def test_observer_renewal_rotates_never_upgrades_and_stops_at_the_cap(managed_store):
    factory, _, tokens, _ = managed_store
    grant = await pair_managed(tokens[0], "csrf-0")
    first = await session_row(factory, grant["access_token"])
    async with bearer(grant["access_token"]) as observer:
        renewed = await observer.post("/api/auth/native-token")
        assert renewed.status_code == 200, renewed.text
    renewal = renewed.json()
    assert renewal["access"] == "observe"
    successor = await session_row(factory, renewal["access_token"])
    assert successor.access == "observe" and successor.client_label == "Desk reader"
    assert as_utc(successor.authenticated_at) == as_utc(first.authenticated_at)
    assert as_utc(successor.expires_at) <= as_utc(first.authenticated_at) + OBSERVER_CAP
    async with bearer(grant["access_token"]) as replay:
        assert (await replay.get("/api/projects")).status_code == 401
    async with bearer(renewal["access_token"]) as observer:
        assert (await observer.get("/api/auth/me")).json()["access"] == "observe"
        assert_read_only(await observer.post("/api/projects", json={"name": "Still read-only"}))

    await move_sign_in(factory, renewal["access_token"], ago=OBSERVER_CAP - timedelta(hours=1))
    async with bearer(renewal["access_token"]) as observer:
        near_cap = await observer.post("/api/auth/native-token")
        assert near_cap.status_code == 200, near_cap.text
    clamped = await session_row(factory, near_cap.json()["access_token"])
    assert as_utc(clamped.expires_at) <= as_utc(clamped.authenticated_at) + OBSERVER_CAP
    assert as_utc(clamped.expires_at) <= utc_now() + timedelta(hours=1, seconds=5)

    await move_sign_in(factory, near_cap.json()["access_token"], ago=OBSERVER_CAP + timedelta(seconds=1))
    async with bearer(near_cap.json()["access_token"]) as observer:
        refused = await observer.post("/api/auth/native-token")
        assert refused.status_code == 401
        assert refused.json()["detail"]["code"] == "session_renewal_limit"


async def test_person_renewal_keeps_the_sign_in_time_and_rotates_bearers(managed_store):
    factory, _, tokens, _ = managed_store
    cookie = await session_row(factory, tokens[0])
    async with client(tokens[0], **{"X-CSRF-Token": "csrf-0", "Origin": "https://test"}) as browser:
        native = await browser.post("/api/auth/native-token")
        assert native.status_code == 200, native.text
        assert native.json()["access"] == "full"
        # The documented browser-to-device exchange leaves the browser signed in.
        assert (await browser.get("/api/projects")).status_code == 200
    first = native.json()["access_token"]
    assert as_utc((await session_row(factory, first)).authenticated_at) == as_utc(cookie.authenticated_at)
    async with bearer(first) as device:
        renewed = await device.post("/api/auth/native-token")
        assert renewed.status_code == 200, renewed.text
    second = renewed.json()["access_token"]
    async with bearer(first) as replay:
        assert (await replay.get("/api/projects")).status_code == 401
    successor = await session_row(factory, second)
    assert successor.access == "full"
    assert as_utc(successor.authenticated_at) == as_utc(cookie.authenticated_at)
    assert as_utc(successor.expires_at) <= as_utc(cookie.authenticated_at) + PERSON_CAP

    await move_sign_in(factory, second, ago=PERSON_CAP + timedelta(seconds=1))
    async with bearer(second) as device:
        refused = await device.post("/api/auth/native-token")
        assert refused.status_code == 401
        assert refused.json()["detail"]["code"] == "session_renewal_limit"


async def test_signed_in_cookie_rotation_shares_the_renewal_cap(managed_store):
    factory, _, tokens, _ = managed_store
    headers = {"X-CSRF-Token": "csrf-0", "Origin": "https://test"}
    await move_sign_in(factory, tokens[0], ago=PERSON_CAP - timedelta(minutes=30))
    async with client(tokens[0], **headers) as browser:
        rotated = await browser.post("/api/session/rotate")
        assert rotated.status_code == 200, rotated.text
        fresh = rotated.cookies.get("workchord_session")
    row = await session_row(factory, fresh)
    assert as_utc(row.expires_at) <= as_utc(row.authenticated_at) + PERSON_CAP
    assert as_utc(row.expires_at) <= utc_now() + timedelta(minutes=30, seconds=5)
    await move_sign_in(factory, fresh, ago=PERSON_CAP + timedelta(seconds=1))
    csrf = (await session_row(factory, fresh)).csrf_token
    async with client(fresh, **{"X-CSRF-Token": csrf, "Origin": "https://test"}) as browser:
        refused = await browser.post("/api/session/rotate")
        assert refused.status_code == 401
        assert refused.json()["detail"]["code"] == "session_renewal_limit"


async def test_trusted_local_pairs_observers_from_its_browser_and_can_revoke_them(local_store):
    factory, scenario, _ = local_store
    full = await start(access="full")
    assert full.status_code == 409
    assert full.json()["detail"]["code"] == "native_auth_unavailable"
    started = await start(label="Local reader")
    assert started.status_code == 201, started.text
    connection = started.json()
    async with client() as browser:
        assert (await browser.get("/api/session/whoami")).status_code == 200
        await approve_with(browser, connection, "Local reader")
        grant = await exchange(connection)
        assert grant.status_code == 200, grant.text
        token = grant.json()["access_token"]
        issued = await session_row(factory, token)
        assert issued.principal_id is None and issued.access == "observe"
        async with bearer(token) as observer:
            me = (await observer.get("/api/auth/me")).json()
            assert me["principal"] is None and me["access"] == "observe"
            assert me["observer"]["client_label"] == "Local reader"
            projects = await observer.get("/api/projects")
            assert sorted(p["id"] for p in projects.json()) == sorted(scenario.projects)
            before = await session_count(factory)
            assert (await observer.get("/api/session/whoami")).status_code == 200
            assert await session_count(factory) == before
            assert_read_only(await observer.put(f"/api/tasks/{scenario.tasks['planned']}", json={"title": "Changed"}))
            assert_read_only(await observer.post("/api/projects", json={"name": "Observer project"}))
        listed = (await browser.get("/api/auth/sessions")).json()
        assert [(row["public_id"], row["client_label"]) for row in listed] == [(issued.public_id, "Local reader")]
        revoked = await browser.delete(f"/api/auth/sessions/{issued.public_id}")
        assert revoked.status_code == 200, revoked.text
    async with bearer(token) as observer:
        assert (await observer.get("/api/projects")).status_code == 401


async def test_a_local_observer_stops_working_when_the_workspace_becomes_managed(local_store, monkeypatch):
    _, _, _ = local_store
    connection = (await start()).json()
    async with client() as browser:
        await browser.get("/api/session/whoami")
        await approve_with(browser, connection)
    token = (await exchange(connection)).json()["access_token"]
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    async with bearer(token) as observer:
        assert (await observer.get("/api/projects")).status_code == 401


def test_renewal_caps_cannot_be_shorter_than_one_session():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, auth_session_max_age_seconds=3600, auth_session_absolute_max_age_seconds=60)
    with pytest.raises(ValidationError):
        Settings(_env_file=None, auth_observer_session_max_age_seconds=3600, auth_observer_absolute_max_age_seconds=60)
    with pytest.raises(ValidationError):
        Settings(_env_file=None, auth_observer_session_max_age_seconds=0)
