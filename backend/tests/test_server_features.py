"""The public feature list names only features this server has."""

from app.main import app
from app.routers.identity import NativeConnectionStart
from app.schemas.external_link import ExternalLinkProvider
from app.server_features import SERVER_FEATURES
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client, managed_store
from tests.test_observer_sessions import local_store


def routes():
    return {(method.upper(), path) for path, operations in app.openapi()["paths"].items() for method in operations}


EVIDENCE = {
    "observer-sessions-v1": lambda: "access" in NativeConnectionStart.model_fields,
    "person-assignment-reads-v1": lambda: ("GET", "/api/agent/assignments") in routes(),
    "team-topology-read-v1": lambda: ("GET", "/api/agent/team-setup/topology") in routes(),
    "agdash-external-links-v1": lambda: ExternalLinkProvider("agdash") is ExternalLinkProvider.AGDASH,
    "harness-session-metadata-v1": lambda: __import__("app.models.agent", fromlist=["AgentRun"]).AgentRun.harness_session_id,
    "runtime-observations-v1": lambda: {("GET", "/api/agent/observations"), ("POST", "/api/agent/observations")} <= routes(),
    "person-run-reads-v1": lambda: ("GET", "/api/agent/runs") in routes(),
    "delivery-prerequisite-retarget-v1": lambda: ("PATCH", "/api/tasks/{task_id}/delivery-dependencies/{edge_id}") in routes(),
}


def test_every_listed_feature_is_present_and_named_once():
    assert len(SERVER_FEATURES) == len(set(SERVER_FEATURES))
    assert set(SERVER_FEATURES) == set(EVIDENCE)
    for name in SERVER_FEATURES:
        assert EVIDENCE[name](), name


async def anonymous_features():
    async with client() as anonymous:
        response = await anonymous.get("/api/auth/me")
    assert response.status_code == 200, response.text
    return response.json()["features"]


async def test_a_managed_server_lists_features_without_a_credential(managed_store):
    assert await anonymous_features() == list(SERVER_FEATURES)


async def test_a_trusted_local_server_lists_features_without_a_credential(local_store):
    assert await anonymous_features() == list(SERVER_FEATURES)
