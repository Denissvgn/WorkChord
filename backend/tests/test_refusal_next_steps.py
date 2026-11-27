"""Every verification and review refusal names the legal next step, over REST, MCP and the task page."""

import json
import re
from pathlib import Path

import pytest

from app import refusal_next_steps as catalogue
from app.authority import AuthorityError
from app.commands import PlanningConflict
from app.main import app
from app.mcp_server import _structured_tool_error, mcp
from app.refusal_next_steps import NEXT_STEPS, NOT_REFUSAL_CODES, next_step_for
from app.services.agent_routing_rollout import AgentRoutingRolloutService
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_team_setup_service import AgentTeamSetupConflictError

APP_DIR = Path(__file__).resolve().parents[1] / "app"
# A quoted string that is shaped like a verification or review refusal code.
CODE_SHAPE = re.compile(
    r"""["']((?:verification_[a-z_]+)|(?:[a-z_]+_review_required)|(?:[a-z_]+_unverifiable)|(?:[a-z_]*outside_topology)"""
    r"""|(?:caller_not_[a-z_]+)|(?:verifier_(?:not|outside)_[a-z_]+)|(?:model_aware_routing_preview_unavailable))["']""")
REQUIRED = {
    "verification_publisher_unverifiable", "verification_candidate_unverifiable", "verification_independence_unverifiable",
    "verified_publisher_review_required", "accountable_review_required", "independent_review_required",
    "agent_team_actor_outside_topology", "model_aware_routing_preview_unavailable",
    "verifier_outside_topology", "caller_not_runtime_ready",
}


def source_refusal_codes():
    found = set()
    for path in APP_DIR.rglob("*.py"):
        if "migrations" in path.parts or path.name == "refusal_next_steps.py":
            continue
        found.update(CODE_SHAPE.findall(path.read_text(encoding="utf-8")))
    return found - NOT_REFUSAL_CODES


def test_every_verification_refusal_code_in_the_source_has_a_next_step():
    codes = source_refusal_codes()
    assert REQUIRED <= codes, "the scan no longer finds the refusals this guard exists for"
    missing = sorted(codes - set(NEXT_STEPS))
    assert not missing, f"These refusal codes have no next step in app/refusal_next_steps.py: {missing}"


def test_the_catalogue_names_no_code_the_source_no_longer_raises():
    stale = sorted(set(NEXT_STEPS) - source_refusal_codes())
    assert not stale, f"Remove next steps for codes nothing raises: {stale}"


def route_templates():
    return {f"{method.upper()} {path}" for path, item in app.openapi()["paths"].items() for method in item}


async def mcp_tool_names():
    return {tool.name for tool in await mcp.list_tools()}


async def test_every_next_step_is_a_sentence_with_commands_that_exist():
    routes, tools = route_templates(), await mcp_tool_names()
    for code, step in NEXT_STEPS.items():
        assert set(step) == {"kind", "authority", "message", "commands", "ui_action"}, code
        assert step["kind"] and step["authority"], code
        assert step["message"].endswith(".") and len(step["message"].split()) >= 8, code
        assert step["ui_action"] in {None, catalogue.UI_ACTION_RECORD_PROVENANCE, catalogue.UI_ACTION_ACCEPT_AS_OWNER}, code
        for channel, command in step["commands"].items():
            if channel == "mcp":
                assert command in tools, (code, command)
            else:
                verb, _, path = command.partition(" ")
                assert f"{verb} {path.split(' ')[0]}" in routes, (code, command)


def test_the_task_id_fills_the_command_templates_without_changing_the_catalogue():
    step = next_step_for("verification_candidate_unverifiable", task_id=42)
    assert step["commands"]["rest"] == "POST /api/tasks/42/manual-provenance"
    assert NEXT_STEPS["verification_candidate_unverifiable"]["commands"]["rest"].endswith("{task_id}/manual-provenance")
    assert next_step_for("not_a_refusal") is None


@pytest.mark.parametrize("code", sorted(NEXT_STEPS))
def test_each_envelope_carries_the_same_next_step_over_rest_and_mcp(code):
    expected = next_step_for(code)
    for error in (AuthorityError(code, "Refused."), PlanningConflict(code, "Refused."),
                  AgentRoutingConflictError(code, "Refused.", target_actor_id=3),
                  AgentTeamSetupConflictError(code, "Refused.", target_actor_id=3)):
        assert error.detail()["next_step"] == expected
        # The MCP tool error is the same envelope the REST handler returns.
        assert json.loads(_structured_tool_error(error)) == error.detail()


def test_a_code_without_an_entry_and_an_explicit_next_step_are_left_alone():
    assert "next_step" not in AuthorityError("permission_denied").detail()
    own = {"kind": "custom"}
    assert AgentRoutingConflictError("verification_candidate_unverifiable", "Refused.", next_step=own).detail()["next_step"] == own


def test_the_rollout_refusal_keeps_its_readiness_detail_and_gains_the_next_step():
    status = AgentRoutingRolloutService().status()
    error = AgentRoutingConflictError("model_aware_routing_preview_unavailable", "Unavailable.",
                                      effective_mode=status.effective_mode.value, blocker_codes=list(status.blocker_codes))
    detail = error.detail()
    assert detail["effective_mode"] == "off" and detail["next_step"]["kind"] == "enable_routing_preview"
