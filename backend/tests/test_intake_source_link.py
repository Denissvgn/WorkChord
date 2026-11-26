"""Source links on intakes and tasks follow one policy."""
import json

import httpx
import pytest

from app import mcp_agent_tools
from app.main import app
from app.mcp_server import _structured_tool_error
from app.models.agent import AgentActor
from app.models.triage import TriageItem
from app.services.identity_service import IdentityService
from app.utils.source_link_policy import (
    SOURCE_LINK_ERROR_CODE,
    SourceLinkRefused,
    evaluate_source_link,
    normalize_source_link,
)
from tests.test_delivery_scenarios import delivery_store  # noqa: F401  (shared fixture)

LOOPBACK = "http://127.0.0.1:8480/tasks?project=6&iteration=9"
PRIVATE = "http://192.168.1.20/board/7"


@pytest.mark.parametrize(
    ("raw", "action", "value"),
    [
        (None, "none", None),
        ("  ", "none", None),
        ("https://example.com/issues/1", "kept", "https://example.com/issues/1"),
        ("/tasks?project=6", "kept", "/tasks?project=6"),
        (LOOPBACK, "rewritten", "/tasks?project=6&iteration=9"),
        ("http://localhost:3000", "rewritten", "/"),
        ("http://[::1]:8480/triage#top", "rewritten", "/triage#top"),
        (PRIVATE, "dropped", None),
        ("http://169.254.169.254/latest", "dropped", None),
        ("//evil.example/x", "dropped", None),
        ("ftp://example.com/file", "dropped", None),
        ("http://user:pw@127.0.0.1/x", "dropped", None),
    ],
)
def test_policy_decisions(raw, action, value):
    decision = evaluate_source_link(raw)
    assert (decision.action, decision.value) == (action, value)


def test_configured_public_address_is_the_same_instance(monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "public_base_url", "https://work.example.org")
    assert normalize_source_link("https://work.example.org/tasks/4") == "/tasks/4"
    assert evaluate_source_link("https://other.example.org/tasks/4").action == "kept"


def test_normalize_names_the_field_and_next_step():
    with pytest.raises(SourceLinkRefused) as caught:
        normalize_source_link(PRIVATE)
    detail = caught.value.detail()
    assert detail["code"] == SOURCE_LINK_ERROR_CODE and detail["field"] == "source_url"
    assert detail["next_step"]


async def _legacy_intake(factory, scenario, link):
    """An intake stored before the policy, holding a link that is now refused."""
    async with factory() as db:
        item = TriageItem(title="Legacy", source="docs", source_url=link, project_hint_id=scenario.projects[0], labels=[], metadata_json={})
        db.add(item)
        await db.commit()
        return item.id


async def test_rest_create_and_edit_refuse_with_named_error(delivery_store):  # noqa: F811
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        refused = await client.post("/api/triage", json={"title": "Bad link", "source_url": PRIVATE})
        assert refused.status_code == 400, refused.text
        detail = refused.json()["detail"]
        assert detail["code"] == SOURCE_LINK_ERROR_CODE and detail["field"] == "source_url" and detail["next_step"]

        created = await client.post("/api/triage", json={"title": "Same instance", "source_url": LOOPBACK})
        assert created.status_code == 201, created.text
        assert created.json()["source_url"] == "/tasks?project=6&iteration=9"

        edit = await client.put(f"/api/triage/{created.json()['id']}", json={"source_url": PRIVATE})
        assert edit.status_code == 400 and edit.json()["detail"]["code"] == SOURCE_LINK_ERROR_CODE
        cleared = await client.put(f"/api/triage/{created.json()['id']}", json={"source_url": None})
        assert cleared.status_code == 200 and cleared.json()["source_url"] is None


async def test_mcp_create_refuses_with_named_error(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        db.info["authority"] = await IdentityService(db).actor_context(actor)
        with pytest.raises(SourceLinkRefused) as caught:
            await mcp_agent_tools.create_triage_item(
                db, actor, {"title": "Bad link", "source_url": PRIVATE},
                idempotency_key="source-link-1", rationale="Check the named error", correlation_id="source-link-corr",
            )
    payload = json.loads(_structured_tool_error(caught.value))
    assert payload["code"] == SOURCE_LINK_ERROR_CODE and payload["field"] == "source_url" and payload["next_step"]


async def test_loopback_link_converts_to_task_as_relative_path(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    item_id = await _legacy_intake(factory, scenario, LOOPBACK)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        read = await client.get(f"/api/triage/{item_id}")
        assert read.status_code == 200 and read.json()["source_url"] == LOOPBACK
        converted = await client.post(f"/api/triage/{item_id}/convert-to-task", json={"iteration_id": scenario.iterations[0], "project_id": scenario.projects[0]})
        assert converted.status_code == 200, converted.text
        body = converted.json()
        assert body["task"]["source_url"] == "/tasks?project=6&iteration=9"
        assert body["source_link"]["action"] == "rewritten" and "relative path" in body["source_link"]["message"]
        assert body["triage_item"]["source_url"] == LOOPBACK


async def test_private_link_is_dropped_on_conversion_to_task(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    item_id = await _legacy_intake(factory, scenario, PRIVATE)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        converted = await client.post(f"/api/triage/{item_id}/convert-to-task", json={"iteration_id": scenario.iterations[0], "project_id": scenario.projects[0], "scope": ["Check the board"]})
        assert converted.status_code == 200, converted.text
        body = converted.json()
        assert body["task"]["source_url"] is None
        assert body["source_link"]["action"] == "dropped" and body["source_link"]["original"] == PRIVATE
        assert PRIVATE not in (body["task"]["description"] or "")


@pytest.mark.parametrize(("link", "action"), [(LOOPBACK, "rewritten"), (PRIVATE, "dropped")])
async def test_link_policy_applies_to_backlog_conversion(delivery_store, link, action):  # noqa: F811
    factory, scenario, _ = delivery_store
    item_id = await _legacy_intake(factory, scenario, link)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        converted = await client.post(f"/api/triage/{item_id}/convert-to-backlog", json={"project_id": scenario.projects[0]})
        assert converted.status_code == 200, converted.text
        body = converted.json()
        assert body["task"]["iteration_id"] is None and body["source_link"]["action"] == action
        assert body["task"]["source_url"] == ("/tasks?project=6&iteration=9" if action == "rewritten" else None)


async def test_legacy_intake_stays_editable_and_a_public_link_is_unchanged(delivery_store):  # noqa: F811
    factory, scenario, _ = delivery_store
    legacy_id = await _legacy_intake(factory, scenario, PRIVATE)
    public_id = await _legacy_intake(factory, scenario, "https://example.com/issues/1")
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        edited = await client.put(f"/api/triage/{legacy_id}", json={"title": "Renamed", "source_url": PRIVATE})
        assert edited.status_code == 200, edited.text
        converted = await client.post(f"/api/triage/{public_id}/convert-to-backlog", json={"project_id": scenario.projects[0]})
        assert converted.status_code == 200
        assert converted.json()["task"]["source_url"] == "https://example.com/issues/1" and converted.json()["source_link"] is None


UNSAFE_REWRITES = ["http://localhost//evil.com/x", "http://localhost/\\evil.com", "http://localhost/a b"]


@pytest.mark.parametrize("raw", UNSAFE_REWRITES)
def test_same_instance_link_with_unsafe_path_is_dropped(raw):
    decision = evaluate_source_link(raw)
    assert decision.action == "dropped" and decision.value is None and decision.reason
    with pytest.raises(SourceLinkRefused):
        normalize_source_link(raw)


@pytest.mark.parametrize("raw", [LOOPBACK, "http://localhost:3000", "/tasks?project=6", "https://example.com/a", "http://[::1]/triage#top"])
def test_policy_is_idempotent(raw):
    once = evaluate_source_link(raw).value
    assert evaluate_source_link(once).value == once


@pytest.mark.parametrize("link", UNSAFE_REWRITES)
@pytest.mark.parametrize("route", ["convert-to-task", "convert-to-backlog"])
async def test_legacy_unsafe_value_converts_instead_of_failing(delivery_store, link, route):  # noqa: F811
    factory, scenario, _ = delivery_store
    item_id = await _legacy_intake(factory, scenario, link)
    body = {"project_id": scenario.projects[0]}
    if route == "convert-to-task":
        body["iteration_id"] = scenario.iterations[0]
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        converted = await client.post(f"/api/triage/{item_id}/{route}", json=body)
        assert converted.status_code == 200, converted.text
        assert converted.json()["task"]["source_url"] is None
        assert converted.json()["source_link"]["action"] == "dropped"
