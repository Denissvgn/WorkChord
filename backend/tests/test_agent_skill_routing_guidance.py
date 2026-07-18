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
from app.routers import agent as agent_router
from scripts import build_agent_skills


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPOSITORY_ROOT / "agent-skills"


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
def test_server_does_not_advertise_incomplete_model_aware_feature() -> None:
    features = agent_contract_features(include_skill_bundles=True)

    assert agent_router.agent_contract_features is agent_contract_features
    assert mcp_agent_tools.agent_contract_features is agent_contract_features
    assert build_agent_skills.MODEL_AWARE_ROUTING_FEATURE == MODEL_AWARE_ROUTING_FEATURE
    assert MODEL_AWARE_ROUTING_FEATURE not in features
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

    assert build_agent_skills.CATALOG_VERSION == "1.4.0"
    assert build_agent_skills.ROLE_METADATA["workchord-pm"]["version"] == "1.4.0"
    assert build_agent_skills.ROLE_METADATA["workchord-worker"]["version"] == "1.3.0"
    assert ("workchord-pm", "1.3.0") in releases
    assert ("workchord-worker", "1.2.0") in releases
    assert "1.3.0" in catalogs
    assert ("workchord-pm", "1.4.0") in releases
    assert ("workchord-worker", "1.3.0") in releases
    assert "1.4.0" in catalogs
