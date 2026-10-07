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
from app.schemas.triage import TriageConvertToTaskRequest
from app.services.task_service import TaskVersionConflictError


ROOT = Path(__file__).resolve().parents[2]

PAGED_ROUTES = [
    ("/api/projects/page", "ProjectPage", "next_after_id"),
    ("/api/iterations/page", "IterationPage", "next_after_id"),
    ("/api/projects/portfolio-summaries/page", "ProjectPortfolioPage", "next_after_id"),
    ("/api/tasks/{task_id}/timeline/page", "TaskTimelinePage", "next_cursor"),
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
