"""Contract coverage for MAR-SKILL-001, MAR-SKILL-002, and MAR-PKG-001."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app import mcp_agent_tools
from app.agent_contract import (
    MODEL_AWARE_ROUTING_FEATURE,
    agent_contract_features,
)
from app.main import app as main_app
from app.mcp_server import mcp
from app.routers import agent as agent_router
from app.schemas.agent import (
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentTaskAssignmentUpdate,
    ModelAwareAgentWorkBegin,
)
from app.schemas.agent_routing import (
    AgentRoutingPreviewCreate,
    TaskRoutingAssessmentCommand,
)
from scripts import build_agent_skills


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPOSITORY_ROOT / "agent-skills"
MODEL_AWARE_BODY_MODELS = {
    model.__name__: model
    for model in (
        TaskRoutingAssessmentCommand,
        AgentRoutingPreviewCreate,
        ModelAwareAgentTaskAssignmentCreate,
        ModelAwareAgentTaskAssignmentUpdate,
        ModelAwareAgentWorkBegin,
    )
}


def _read(relative: str) -> str:
    return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")


def _normalized(relative: str) -> str:
    return re.sub(r"\s+", " ", _read(relative))


def _operation(operation_id: str) -> dict:
    matches = [
        operation
        for operation in build_agent_skills.ASSIGNED_WORK_V1_CONTRACT["operations"]
        if operation["id"] == operation_id
    ]
    assert len(matches) == 1
    return matches[0]


def _derived_band(axes: tuple[int, int, int, int, int]) -> str:
    if all(value == 1 for value in axes):
        return "routine"
    if any(value == 3 for value in axes):
        return "advanced"
    return "standard"


def _schema_refs(value: object) -> set[str]:
    if isinstance(value, dict):
        refs: set[str] = set()
        reference = value.get("$ref")
        if isinstance(reference, str):
            refs.add(reference.removeprefix("#/components/schemas/"))
        for item in value.values():
            refs.update(_schema_refs(item))
        return refs
    if isinstance(value, list):
        refs = set()
        for item in value:
            refs.update(_schema_refs(item))
        return refs
    return set()


@pytest.mark.contract
@pytest.mark.parametrize(
    ("label", "axes", "expected"),
    [
        ("Known one-file text correction", (1, 1, 1, 1, 1), "routine"),
        ("Normal multi-module feature", (2, 2, 2, 2, 2), "standard"),
        ("Novel cross-repository migration", (3, 2, 3, 3, 3), "advanced"),
        ("Small authentication permission change", (1, 1, 1, 3, 3), "advanced"),
        ("Large repetitive rename", (1, 1, 1, 1, 1), "routine"),
    ],
)
def test_pm_skill_covers_governed_difficulty_scenarios(
    label: str,
    axes: tuple[int, int, int, int, int],
    expected: str,
) -> None:
    guidance = _normalized(
        "agent-skills/workchord-pm/references/"
        "intake-planning-and-task-briefs.md"
    )

    assert _derived_band(axes) == expected
    assert label in guidance
    assert f"`{expected}`" in guidance
    assert "Difficulty is not priority, effort, elapsed time, or business value" in guidance
    assert "supervised compatibility routing" in guidance
    assert "A second assessment for the same task/policy version is a conflict" in guidance
    assert "bounded immutable history" in guidance


@pytest.mark.contract
def test_pm_skill_hard_gates_selection_before_cost() -> None:
    guidance = _normalized(
        "agent-skills/workchord-pm/references/"
        "assignment-scheduling-and-delivery-control.md"
    )

    assert "top team-member/capacity recommendation is never an exact actor" in guidance
    assert "Rank only eligible candidates" in guidance
    assert "Cost or latency never compensates" in guidance
    assert "If no candidate is eligible, create no assignment" in guidance
    assert "generate a fresh preview" in guidance
    assert "planned verifier" in guidance
    assert "not a capacity reservation" in guidance


@pytest.mark.contract
def test_pm_skill_distinguishes_model_and_external_blockers() -> None:
    guidance = _normalized(
        "agent-skills/workchord-pm/references/"
        "verification-rework-and-recovery.md"
    )

    for trust_state in ("matched", "mismatch", "unreported", "unverifiable"):
        assert f"`{trust_state}`" in guidance
    assert "not attested" in guidance
    assert "Access denial" in guidance
    assert "non-model blockers" in guidance
    assert "Never downgrade an independent/specialist review requirement" in guidance
    assert "Resolution advances the task version" in guidance
    assert "one current assessment required by the reopened task version" in guidance


@pytest.mark.contract
def test_worker_skill_obeys_selected_binding_without_expanding_authority() -> None:
    skill = _normalized("agent-skills/workchord-worker/SKILL.md")
    lifecycle = _normalized(
        "agent-skills/workchord-worker/references/claim-run-and-task-state.md"
    )

    assert "send the exact assigned binding ID/revision" in skill
    assert "Never substitute another binding" in skill
    assert "do not request or perform a model-tier change yourself" in skill
    assert "workers cannot change model bindings" in lifecycle
    assert "Do not substitute a default, cheaper, newer, or locally preferred model" in lifecycle
    assert "execution evidence, not a model request and not attestation" in lifecycle


@pytest.mark.contract
def test_model_aware_operation_contract_is_feature_gated() -> None:
    operation_ids = {
        "model-catalog",
        "routing-assessment-current",
        "routing-assessment-history",
        "routing-assessment-create",
        "routing-preview",
        "model-aware-assignment-create",
        "model-aware-assignment-update",
        "model-aware-begin",
    }
    operations = [_operation(operation_id) for operation_id in operation_ids]

    assert all(
        operation["required_feature"] == MODEL_AWARE_ROUTING_FEATURE
        for operation in operations
    )
    assert _operation("routing-preview")["rest"]["method"] == "POST"
    assert _operation("routing-preview")["summary"].endswith("without mutation.")
    history = _operation("routing-assessment-history")
    assert history["rest"]["query_parameters"] == [
        {"name": "limit", "required": False}
    ]
    assert history["mcp"]["tool"] == "agent_list_task_routing_assessments"
    assert _operation("model-catalog")["rest"]["query_parameters"] == [
        {"name": "include_disabled", "required": False}
    ]
    assert _operation("actor-roster")["rest"]["query_parameters"] == [
        {"name": "include_disabled", "required": False}
    ]

    assignment_fields = {
        field["name"]: field["required"]
        for field in _operation("model-aware-assignment-create")["rest"]["body"][
            "fields"
        ]
    }
    for field in (
        "assessment_id",
        "model_binding_id",
        "model_binding_revision",
        "routing_preview_id",
        "routing_preview_digest",
    ):
        assert assignment_fields[field]
    assert "routing_snapshot" not in assignment_fields

    begin_fields = {
        field["name"]: field["required"]
        for field in _operation("model-aware-begin")["rest"]["body"]["fields"]
    }
    assert begin_fields["model_binding_id"]
    assert begin_fields["model_binding_revision"]
    assert begin_fields["resolved_model_id"]


@pytest.mark.contract
@pytest.mark.asyncio
async def test_model_aware_package_contract_matches_live_rest_and_mcp() -> None:
    openapi_paths = main_app.openapi()["paths"]
    live_tools = {tool.name: tool for tool in await mcp.list_tools()}
    operations = [
        operation
        for operation in build_agent_skills.ASSIGNED_WORK_V1_CONTRACT["operations"]
        if operation["id"] == "actor-roster"
        or operation.get("required_feature") == MODEL_AWARE_ROUTING_FEATURE
    ]

    for operation in operations:
        rest = operation["rest"]
        live_rest = openapi_paths[rest["path"]][rest["method"].lower()]
        live_parameters = {
            (parameter["in"], parameter["name"]): parameter
            for parameter in live_rest.get("parameters", [])
        }
        for location, key in (
            ("path", "path_parameters"),
            ("query", "query_parameters"),
            ("header", "header_parameters"),
        ):
            for parameter in rest[key]:
                live_parameter = live_parameters[(location, parameter["name"])]
                assert live_parameter["required"] is parameter["required"]

        body = rest["body"]
        if body is not None:
            body_model = MODEL_AWARE_BODY_MODELS[body["model"]]
            declared_fields = {
                field["name"]: field["required"] for field in body["fields"]
            }
            assert declared_fields == {
                name: field.is_required()
                for name, field in body_model.model_fields.items()
            }
            live_body_schema = live_rest["requestBody"]["content"][
                "application/json"
            ]["schema"]
            assert body["model"] in _schema_refs(live_body_schema)

        mcp_contract = operation["mcp"]
        live_tool_schema = live_tools[mcp_contract["tool"]].inputSchema
        declared_tool_parameters = {
            parameter["name"]: parameter["required"]
            for parameter in mcp_contract["parameters"]
        }
        assert set(live_tool_schema["properties"]) == set(declared_tool_parameters)
        live_required = set(live_tool_schema.get("required", []))
        assert declared_tool_parameters == {
            name: name in live_required for name in declared_tool_parameters
        }


@pytest.mark.contract
def test_server_advertises_complete_model_aware_feature() -> None:
    features = agent_contract_features(include_skill_bundles=True)

    assert agent_router.agent_contract_features is agent_contract_features
    assert mcp_agent_tools.agent_contract_features is agent_contract_features
    assert build_agent_skills.MODEL_AWARE_ROUTING_FEATURE == MODEL_AWARE_ROUTING_FEATURE
    assert MODEL_AWARE_ROUTING_FEATURE in features
    assert "skill-bundles-v1" in features
    assert len(features) == len(set(features))


@pytest.mark.contract
def test_wave4_versions_are_new_frozen_identities() -> None:
    baseline = json.loads(
        (SKILLS_ROOT / build_agent_skills.RELEASE_BASELINE_FILENAME).read_text(
            encoding="utf-8"
        )
    )
    releases = {
        (release["name"], release["version"]) for release in baseline["releases"]
    }
    catalogs = {catalog["version"] for catalog in baseline["catalogs"]}

    assert build_agent_skills.CATALOG_VERSION == "1.5.0"
    assert build_agent_skills.ROLE_METADATA["workchord-pm"]["version"] == "1.5.0"
    assert build_agent_skills.ROLE_METADATA["workchord-worker"]["version"] == "1.4.0"
    assert ("workchord-pm", "1.3.0") in releases
    assert ("workchord-worker", "1.2.0") in releases
    assert "1.3.0" in catalogs
    assert ("workchord-pm", "1.4.0") in releases
    assert ("workchord-worker", "1.3.0") in releases
    assert "1.4.0" in catalogs
    assert ("workchord-pm", "1.5.0") in releases
    assert ("workchord-worker", "1.4.0") in releases
    assert "1.5.0" in catalogs
