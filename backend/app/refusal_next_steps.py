"""The legal next step for every verification and review refusal, kept in one place.

A refusal names what went wrong; its ``next_step`` names what a person or agent may do
about it. Every REST envelope, MCP tool error and task action blocker takes its next step
from this catalogue, so the three never drift apart. A code with no entry here gets no
``next_step`` key, and a test fails when a verification refusal code in the source has no
entry.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

# Who may use the next step. A person without the authority is told whom to ask.
AUTHORITY_OWNER_OPERATOR = "workspace_owner_or_operator"
AUTHORITY_PROVENANCE_RECORDER = "owner_operator_project_manager_or_pm_agent"
AUTHORITY_REVIEWER = "reviewer_without_contribution"
AUTHORITY_VERIFIER = "assigned_agent_verifier"
AUTHORITY_EXECUTOR = "executing_agent"
AUTHORITY_TEAM_MANAGER = "project_manager_or_pm_agent"
AUTHORITY_OPERATOR = "workspace_operator"
AUTHORITY_ANY = "any_signed_in_member"

# The task page offers these two as forms; every other next step is text and a command.
UI_ACTION_RECORD_PROVENANCE = "record_provenance"
UI_ACTION_ACCEPT_AS_OWNER = "accept_as_owner"

_PROVENANCE_COMMANDS = {
    "rest": "POST /api/tasks/{task_id}/manual-provenance",
    "agent_rest": "POST /api/agent/planning/tasks/{task_id}/manual-provenance",
    "mcp": "agent_record_manual_provenance",
}
_ASSIGN_VERIFIER_COMMANDS = {"rest": "POST /api/agent/assignments", "mcp": "agent_create_assignment"}
_REVIEW_QUEUE_COMMANDS = {"rest": "GET /api/agent/me/reviews", "mcp": "agent_get_my_reviews"}
_TEAM_STATUS_COMMANDS = {"rest": "GET /api/agent/team-setup/status", "mcp": "agent_get_team_setup_status"}


def _step(kind: str, authority: str, message: str, commands: dict[str, str] | None = None, ui_action: str | None = None):
    return {"kind": kind, "authority": authority, "message": message, "commands": commands or {}, "ui_action": ui_action}


_RECORD_PROVENANCE = _step(
    "record_provenance", AUTHORITY_PROVENANCE_RECORDER,
    "Record who executed the work and its exact commits with Record provenance. A signed-in workspace owner, operator or"
    " project manager, or the project's PM agent, can record it; anyone else should ask one of them.",
    _PROVENANCE_COMMANDS, UI_ACTION_RECORD_PROVENANCE)
_ASSIGN_INDEPENDENT_VERIFIER = _step(
    "assign_independent_verifier", AUTHORITY_TEAM_MANAGER,
    "Assign a verifier that did not contribute to this work, whose profile and model publisher differ from every contributor,"
    " then have it review the task.", _ASSIGN_VERIFIER_COMMANDS)
_READY_TEAM_ACTOR = _step(
    "ready_team_actor", AUTHORITY_TEAM_MANAGER,
    "Read the team setup status: its non_ready_actors say which actors are not runtime-ready and its readiness_rule says why."
    " Ready those actors, then repeat the request.", _TEAM_STATUS_COMMANDS)

NEXT_STEPS: dict[str, dict[str, Any]] = {
    "verification_publisher_unverifiable": _step(
        "refresh_verifier_binding", AUTHORITY_VERIFIER,
        "Refresh the review assignment after any change to the reviewer's binding or profile, then submit the verdict again"
        " with the reviewer's own observed model, which must match its selected binding.", _REVIEW_QUEUE_COMMANDS),
    "verification_candidate_unverifiable": _RECORD_PROVENANCE | {"message": (
        "Link exactly one pull request to the task, or record who executed the work and its exact commits with Record"
        " provenance. A signed-in workspace owner, operator or project manager, or the project's PM agent, can record it;"
        " anyone else should ask one of them.")},
    "verification_independence_unverifiable": _RECORD_PROVENANCE | {"message": (
        "Record who executed the work and its exact commits with Record provenance so independence can be proven; an assigned"
        " reviewer instead submits its verdict with its own observed model. A signed-in workspace owner, operator or project"
        " manager, or the project's PM agent, can record provenance; anyone else should ask one of them.")},
    "verified_publisher_review_required": _step(
        "accept_as_owner", AUTHORITY_OWNER_OPERATOR,
        "Assign an agent verifier to review this work, or, as a signed-in workspace owner or operator, accept it as owner"
        " with a reason; the project policy stays on. If the executor is not recorded, use Record provenance first.",
        {"rest": "POST /api/tasks/{task_id}/owner-acceptance"}, UI_ACTION_ACCEPT_AS_OWNER),
    "accountable_review_required": _step(
        "accountable_operator_review", AUTHORITY_OPERATOR,
        "Have a signed-in workspace operator accept it with the review override and a written reason, or have a person review"
        " the work instead.", {"rest": "POST /api/tasks/{task_id}/review"}),
    "independent_review_required": _step(
        "use_another_reviewer", AUTHORITY_REVIEWER,
        "Ask a reviewer who did not execute or submit this work to review it; an agent reviewer must hold the verifier role."
        " An accountable operator may instead use the review override with a written reason."),
    "agent_team_actor_outside_topology": _step(
        "choose_team_actor", AUTHORITY_TEAM_MANAGER,
        "Choose an actor that is a runtime-ready member of the caller's current team. Read the team setup status: its"
        " non_ready_actors say which members are not ready and its readiness_rule says why, and the project's PM can add or"
        " ready the actor you need.", _TEAM_STATUS_COMMANDS),
    "verifier_outside_topology": _step(
        "choose_team_actor", AUTHORITY_TEAM_MANAGER,
        "Choose a verifier that is a runtime-ready member of the caller's current team, or have the project's PM add the"
        " verifier to the team. Read the team setup status for the members and what keeps each from being ready.",
        _TEAM_STATUS_COMMANDS),
    "verifier_not_runtime_ready": _READY_TEAM_ACTOR,
    "caller_not_runtime_ready": _READY_TEAM_ACTOR | {"authority": AUTHORITY_ANY, "message": (
        "The calling actor is not runtime-ready in its team. Read the team setup status: its non_ready_actors and"
        " readiness_rule say what is missing for the caller; the project's PM can make it ready, then repeat the request.")},
    "caller_not_bound_to_topology": _step(
        "bind_caller_to_topology", AUTHORITY_TEAM_MANAGER,
        "The calling actor is not a member of any live team. Have a workspace operator or the project's PM add it to the team"
        " in team setup, then repeat the request.", _TEAM_STATUS_COMMANDS),
    "model_aware_routing_preview_unavailable": _step(
        "enable_routing_preview", AUTHORITY_OPERATOR,
        "Read this refusal's blocker_codes and topology_readiness: ready the team actors it names, or have a workspace operator"
        " set MODEL_AWARE_ROUTING_MODE to shadow or enforced. Previews work in either mode.", _TEAM_STATUS_COMMANDS),
    "verification_candidate_stale": _step(
        "refresh_review_assignment", AUTHORITY_VERIFIER,
        "Refresh the review assignment so it names the task's current candidate, then review that exact candidate.",
        _REVIEW_QUEUE_COMMANDS),
    "verification_evidence_unavailable": _step(
        "acknowledge_review_evidence", AUTHORITY_VERIFIER,
        "Read the review's current evidence packet and submit the verdict acknowledging that exact packet; scoped evidence"
        " also needs a verifier that did not contribute to the work.", _REVIEW_QUEUE_COMMANDS),
    "verification_contributors_unverifiable": _RECORD_PROVENANCE,
    "verification_actor_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_profile_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_publisher_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_specialist_skill_missing": _ASSIGN_INDEPENDENT_VERIFIER | {"message": (
        "Assign a verifier whose profile holds the required specialist skill and that did not contribute to this work, then"
        " have it review the task.")},
    "execution_publisher_unverifiable": _step(
        "submit_observed_model", AUTHORITY_EXECUTOR,
        "Submit the terminal command again with the model the agent observed. If the model binding changed during the run,"
        " report the interruption and the retained work instead.", {"mcp": "agent_submit_my_work"}),
    "manual_provenance_candidate_unverifiable": _RECORD_PROVENANCE | {"message": (
        "Correct the head commit, commit list, pull request or base commit named in this refusal so they are immutable GitHub"
        " URLs of one candidate, then record provenance again.")},
    "observation_actor_unverifiable": _step(
        "name_actor_through_run", AUTHORITY_ANY,
        "Name an actor through a run or an assignment of a task you can read, then record the observation again."),
}

# Strings that look like refusal codes in the source but are not refusals.
NOT_REFUSAL_CODES = frozenset({
    "verification_code", "verification_path", "verification_burden", "verification_burden_axis", "verification_required",
    "candidate_unverifiable",
})


def next_step_for(code: str | None, *, task_id: int | None = None) -> dict[str, Any] | None:
    """The machine-readable next step for a refusal code, or None when the code has none.

    ``{task_id}`` in a command is filled in when the task is known and left as a path
    template otherwise.
    """
    entry = NEXT_STEPS.get(code or "")
    if entry is None:
        return None
    step = deepcopy(entry)
    if task_id is not None:
        step["commands"] = {key: value.replace("{task_id}", str(task_id)) for key, value in step["commands"].items()}
    return step


def with_next_step(detail: dict[str, Any], *, task_id: int | None = None) -> dict[str, Any]:
    """Add the code's next step to a refusal envelope that does not carry one yet."""
    if "next_step" in detail:
        return detail
    step = next_step_for(detail.get("code"), task_id=task_id)
    return detail if step is None else {**detail, "next_step": step}
