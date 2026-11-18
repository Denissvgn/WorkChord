"""Schema-derived compatibility, legacy payloads, and additive client behavior."""

import json
from copy import deepcopy
from pathlib import Path
import runpy

import pytest
from pydantic import ValidationError

from app.config import Settings
from app.schemas.task import TaskStatusChange, TaskUpdate
from app.schemas.agent import AgentActorCreate
from app.schemas.agent_routing import AgentModelMutationReceipt
from app.schemas.triage import TriageConvertToTaskRequest
from app.services.task_service import TaskVersionConflictError


ROOT = Path(__file__).resolve().parents[2]

PAGED_ROUTES = [
    ("/api/projects/page", "ProjectPage", "next_after_id"),
    ("/api/iterations/page", "IterationPage", "next_after_id"),
    ("/api/projects/portfolio-summaries/page", "ProjectPortfolioPage", "next_after_id"),
    ("/api/tasks/{task_id}/timeline/page", "TaskTimelinePage", "next_cursor"),
    ("/api/time-entries", "TimeEntryPage", "next_after_id"),
    ("/api/time-entries/report", "TimeReportPage", "next_after_id"),
]


def test_client_contract_is_current_and_deterministic():
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    first = exporter["serialized_contract"]()
    assert first == exporter["serialized_contract"]()
    assert first == (ROOT / "backend/tests/fixtures/client-contract-v1.json").read_text()


@pytest.mark.parametrize("path,schema_name,cursor_field", PAGED_ROUTES)
def test_paged_readers_export_cursor_and_response_contracts(path, schema_name, cursor_field):
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    contract = exporter["build_contract"]()
    operation = contract["paths"][path]["get"]
    parameters = {p["name"]: p["schema"] for p in operation["parameters"] if p["in"] == "query"}
    expected = {"limit", "cursor"} if cursor_field == "next_cursor" else {"limit", "after_id", "upper_id"}
    assert expected <= parameters.keys()
    assert parameters["limit"]["minimum"] == 1 and parameters["limit"]["maximum"] == 100
    response = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert response["$ref"] == f"#/components/schemas/{schema_name}"
    properties = contract["components"]["schemas"][schema_name]["properties"]
    assert {"items", "has_more", cursor_field} <= properties.keys()
    assert ("limit" if cursor_field == "next_cursor" else "upper_id") in properties


@pytest.mark.parametrize("path,schema_name,cursor_field", PAGED_ROUTES)
def test_missing_paged_reader_fails_contract_export(monkeypatch, path, schema_name, cursor_field):
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    app = exporter["app"]
    schema = deepcopy(app.openapi())
    del schema["paths"][path]
    monkeypatch.setattr(app, "openapi", lambda: schema)
    with pytest.raises(ValueError, match="Client routes no longer registered"):
        exporter["build_contract"]()


MODEL_CATALOG_ROUTES = [
    ("/api/agent/model-catalog", "get", "200", None),
    ("/api/agent/model-catalog", "post", "201", "AgentModelMutationReceipt"),
    ("/api/agent/model-catalog/{catalog_id}", "patch", "200", "AgentModelMutationReceipt"),
    ("/api/agent/model-catalog/{catalog_id}/disable", "post", "200", "AgentModelMutationReceipt"),
]

RECEIPT_FIELDS = {
    "operation": "model_catalog.create",
    "target_type": "model_catalog",
    "target_id": 3,
    "idempotency_key": "catalog-create-1",
    "rationale": "Declare the first model.",
    "correlation_id": "correlation-1",
    "authoritative_revision": 1,
    "result": {"key": "standard-code"},
}


@pytest.mark.parametrize("path,method,success_status,receipt", MODEL_CATALOG_ROUTES)
def test_model_catalog_routes_accept_either_credential_header(path, method, success_status, receipt):
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    operation = exporter["build_contract"]()["paths"][path][method]
    headers = {p["name"]: p for p in operation["parameters"] if p["in"] == "header"}
    # Agents keep sending their own key; the operator may send the admin key instead.
    for name in ("X-Agent-API-Key", "X-Admin-API-Key"):
        assert name in headers and headers[name].get("required", False) is False
    response = operation["responses"][success_status]["content"]["application/json"]["schema"]
    if receipt is None:
        assert response["items"]["$ref"] == "#/components/schemas/AgentModelCatalogResponse"
    else:
        assert response["$ref"] == f"#/components/schemas/{receipt}"


@pytest.mark.parametrize("path,method,status,response_schema", [
    ("/api/agent/model-bindings", "get", "200", "AgentModelBindingResponse"),
    ("/api/agent/model-bindings/{binding_id}", "get", "200", "AgentModelBindingResponse"),
    ("/api/agent/model-bindings", "post", "201", "AgentModelMutationReceipt"),
    ("/api/agent/model-bindings/{binding_id}", "patch", "200", "AgentModelMutationReceipt"),
    ("/api/agent/model-bindings/{binding_id}/disable", "post", "200", "AgentModelMutationReceipt"),
    ("/api/agent/profile-presets", "get", "200", None),
])
def test_binding_and_preset_contracts_accept_either_credential_header(path, method, status, response_schema):
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    operation = exporter["build_contract"]()["paths"][path][method]
    headers = {p["name"]: p for p in operation["parameters"] if p["in"] == "header"}
    for name in ("X-Agent-API-Key", "X-Admin-API-Key"):
        assert name in headers and headers[name].get("required", False) is False
    response = operation["responses"][status]["content"]["application/json"]["schema"]
    if response_schema is None:
        assert response["type"] == "array"
        assert response["items"]["type"] == "object"
    elif path == "/api/agent/model-bindings" and method == "get":
        assert response["items"]["$ref"] == f"#/components/schemas/{response_schema}"
    else:
        assert response["$ref"] == f"#/components/schemas/{response_schema}"


def test_model_receipt_actor_is_an_agent_id_or_null_for_the_operator():
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    receipt = exporter["build_contract"]()["components"]["schemas"]["AgentModelMutationReceipt"]
    assert "actor_id" in receipt["required"]
    assert receipt["properties"]["actor_id"]["anyOf"] == [
        {"type": "integer", "minimum": 1.0}, {"type": "null"},
    ]
    agent_receipt = AgentModelMutationReceipt.model_validate({**RECEIPT_FIELDS, "actor_id": 7})
    assert agent_receipt.model_dump(mode="json")["actor_id"] == 7
    operator_receipt = AgentModelMutationReceipt.model_validate({**RECEIPT_FIELDS, "actor_id": None})
    assert operator_receipt.model_dump(mode="json")["actor_id"] is None
    for invalid in ({**RECEIPT_FIELDS, "actor_id": 0}, RECEIPT_FIELDS):
        with pytest.raises(ValidationError):
            AgentModelMutationReceipt.model_validate(invalid)


@pytest.mark.parametrize("payload", [
    {"title": "Legacy edit"},
    {"title": "Versioned edit", "expected_version": 2},
])
def test_supported_task_update_payloads(payload):
    update = TaskUpdate.model_validate(payload)
    assert update.model_dump(exclude_unset=True) == payload


def test_legacy_triage_target_and_additive_brief_input():
    assert TriageConvertToTaskRequest.model_validate({"iteration_id": 1}).iteration_id == 1
    request = TriageConvertToTaskRequest.model_validate({
        "iteration_id": 1, "acceptance_criteria": ["A reviewer can read the result"],
        "verification": ["Read back the saved result"],
    })
    assert request.acceptance_criteria == ["A reviewer can read the result"]
    with pytest.raises(ValidationError) as failure:
        TriageConvertToTaskRequest.model_validate({"destination": "backlog"})
    assert failure.value.errors()[0]["loc"] == ("iteration_id",)


def test_unknown_actions_and_invalid_versions_do_not_succeed():
    with pytest.raises(ValidationError):
        TaskStatusChange.model_validate({"status": "blocked"})
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({"expected_version": 0})
    assert TaskUpdate.model_validate({"future_field": "ignored"}).model_dump(exclude_unset=True) == {}


def test_conflict_fixture_uses_the_server_machine_code():
    payload = TaskVersionConflictError(1, {"id": 7, "version": 2}).detail()
    assert json.loads(json.dumps(payload)) == {
        "code": "task_version_conflict", "message": "Task version conflict: expected 1, current 2.",
        "expected_version": 1, "current_task": {"id": 7, "version": 2},
    }


def test_public_skill_bundles_require_the_trusted_checksum():
    with pytest.raises(ValidationError, match="Public agent skill bundles require"):
        Settings(_env_file=None, agent_skill_bundles_public=True,
                 agent_skill_bundle_trusted_checksums_sha256="")
    settings = Settings(_env_file=None, agent_skill_bundles_public=True,
                        agent_skill_bundle_trusted_checksums_sha256="a" * 64)
    assert settings.agent_skill_bundles_public is True


def test_actor_provisioning_does_not_require_or_invent_runtime_binding():
    actor = AgentActorCreate(name="independent-worker", display_name="Independent worker")
    assert actor.model_binding is None
    assert actor.work_policy == "assigned_only"
    assert actor.max_parallel_work == 1


@pytest.mark.parametrize('path', ['/api/tasks/delivery-metrics', '/api/tasks/execution-usage'])
def test_analytics_contract_adds_optional_scope_modes(path):
    exporter = runpy.run_path(str(ROOT / 'scripts/generate_client_contract.py'))
    operation = exporter['build_contract']()['paths'][path]['get']
    params = {item['name']: item for item in operation['parameters'] if item['in'] == 'query'}
    assert {'project_id', 'iteration_id', 'lookback_days', 'backlog', 'all_projects'} <= params.keys()
    for name in ('backlog', 'all_projects'):
        assert params[name]['required'] is False
        assert params[name]['schema']['type'] == 'boolean'
        assert params[name]['schema']['default'] is False
    assert params['lookback_days']['schema']['default'] == 30
    if path.endswith('execution-usage'):
        assert {'budget_amount', 'budget_currency'} <= params.keys()


def test_metric_matches_exports_pagination_contract():
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    contract = exporter["build_contract"]()
    operation = contract["paths"]["/api/tasks/metric-matches"]["get"]
    assert {"limit", "after_id"} <= {p["name"] for p in operation["parameters"]}
    assert {"items", "has_more", "next_after_id"} <= contract["components"]["schemas"]["MetricMatchPage"]["properties"].keys()


def test_planning_readiness_contract_includes_calendar_name():
    exporter = runpy.run_path(str(ROOT / "scripts/generate_client_contract.py"))
    contract = exporter["build_contract"]()
    assert "/api/iterations/{iteration_id}/planning-readiness" in contract["paths"]
    summary = contract["components"]["schemas"]["IterationPlanningReadinessSummary"]
    assert "calendar_name" in summary["properties"]
    assert "calendar_name" not in summary.get("required", [])
