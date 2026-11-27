"""The legal next step for every verification and review refusal, kept in one place.

A refusal names what went wrong; its ``next_step`` names what a person or agent may do
about it. Every REST envelope, MCP tool error and task action blocker takes its next step
from this catalogue, so the three never drift apart. A code with no entry here gets no
``next_step`` key, and a test fails when a refusal code in the source has no entry.

A code has one default step. A code that is raised for different causes also has named
variants, and the raise site that knows its cause picks the variant, so a step is never
offered where it would be refused. Each ``kind`` names exactly one sentence: the task page
translates the sentence by its kind.
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
AUTHORITY_DEPLOYMENT_OPERATOR = "deployment_operator"
AUTHORITY_ANY = "any_signed_in_member"

# The task page offers these two as forms; every other next step is text and a command.
UI_ACTION_RECORD_PROVENANCE = "record_provenance"
UI_ACTION_ACCEPT_AS_OWNER = "accept_as_owner"

_PROVENANCE_COMMANDS = {
    "rest": "POST /api/tasks/{task_id}/manual-provenance",
    "agent_rest": "POST /api/agent/planning/tasks/{task_id}/manual-provenance",
    "mcp": "agent_record_manual_provenance",
}
_OWNER_ACCEPT_COMMANDS = {"rest": "POST /api/tasks/{task_id}/owner-acceptance"}
_ASSIGN_VERIFIER_COMMANDS = {"rest": "POST /api/agent/assignments", "mcp": "agent_create_assignment"}
_REVIEW_QUEUE_COMMANDS = {"rest": "GET /api/agent/me/reviews", "mcp": "agent_get_my_reviews"}
_TEAM_STATUS_COMMANDS = {"rest": "GET /api/agent/team-setup/status", "mcp": "agent_get_team_setup_status"}


def _step(kind: str, authority: str, message: str, commands: dict[str, str] | None = None, ui_action: str | None = None):
    return {"kind": kind, "authority": authority, "message": message, "commands": commands or {}, "ui_action": ui_action}


_ACCEPT_AS_OWNER_POLICY = (
    "A workspace owner or operator can accept it as owner with a reason; the project policy stays on.")
_RECORD_PROVENANCE = _step(
    "record_provenance", AUTHORITY_PROVENANCE_RECORDER,
    "Record who executed the work and its exact commits with Record provenance. This task has no recorded runs, so a signed-in"
    " workspace owner, operator or project manager, or the project's PM agent, can record it; anyone else should ask one of them.",
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
    # Verification: publisher, candidate, independence.
    "verification_publisher_unverifiable": _step(
        "refresh_verifier_binding", AUTHORITY_VERIFIER,
        "Refresh the review assignment after any change to the reviewer's binding or profile, then submit the verdict again"
        " with the reviewer's own observed model, which must match its selected binding.", _REVIEW_QUEUE_COMMANDS),
    "verification_candidate_unverifiable": _step(
        "resubmit_artifact", AUTHORITY_ANY,
        "Link exactly one pull request to the task, or have the executor resubmit the artifact with a pull request or a"
        " GitHub compare URL, then ask for the review again."),
    "verification_independence_unverifiable": _step(
        "submit_own_verdict", AUTHORITY_VERIFIER,
        "The verdict must come from the assigned reviewer itself, submitted with its own observed model. If you are not the"
        " assigned reviewer, ask the project manager to assign you.", _REVIEW_QUEUE_COMMANDS),
    "verification_contributors_unverifiable": _step(
        "fix_candidate_commits", AUTHORITY_ANY,
        "Every commit of the candidate must be attributed to this task's executor and carry no Co-authored-by trailer. Have the"
        " executor resubmit the artifact with a pull request that holds only such commits, or retry once GitHub is reachable."),
    "verification_candidate_stale": _step(
        "refresh_review_assignment", AUTHORITY_VERIFIER,
        "Refresh the review assignment so it names the task's current candidate, then review that exact candidate.",
        _REVIEW_QUEUE_COMMANDS),
    "verification_evidence_unavailable": _step(
        "acknowledge_review_evidence", AUTHORITY_VERIFIER,
        "Read the review's current evidence packet and submit the verdict acknowledging that exact packet; scoped evidence"
        " also needs a verifier that did not contribute to the work.", _REVIEW_QUEUE_COMMANDS),
    "verification_actor_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_profile_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_publisher_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "verification_specialist_skill_missing": _step(
        "assign_skilled_verifier", AUTHORITY_TEAM_MANAGER,
        "Assign a verifier whose profile holds the required specialist skill and that did not contribute to this work, then"
        " have it review the task.", _ASSIGN_VERIFIER_COMMANDS),
    "execution_publisher_unverifiable": _step(
        "submit_observed_model", AUTHORITY_EXECUTOR,
        "Submit the terminal command again with the model the agent observed. If the model binding changed during the run,"
        " report the interruption and the retained work instead.", {"mcp": "agent_submit_my_work"}),
    "reviewer_profile_mismatch": _step(
        "assign_matching_reviewer", AUTHORITY_TEAM_MANAGER,
        "Assign a reviewer that holds the requested profile; submitted rework names the independent reviewer profile it"
        " requires.", _ASSIGN_VERIFIER_COMMANDS),
    "reviewer_profile_missing": _step(
        "give_reviewer_profile", AUTHORITY_TEAM_MANAGER,
        "The reviewer has no profile. Give the reviewer actor a profile with the verification assignment mode, then assign it"
        " again.", _ASSIGN_VERIFIER_COMMANDS),
    "reviewer_profile_ambiguous": _step(
        "choose_reviewer_profile", AUTHORITY_TEAM_MANAGER,
        "More than one reviewer profile fits. Name the reviewer profile in the assignment.", _ASSIGN_VERIFIER_COMMANDS),
    "reviewer_profile_not_independent": _ASSIGN_INDEPENDENT_VERIFIER,
    "replacement_contribution_unattributed": _step(
        "attribute_carried_run", AUTHORITY_TEAM_MANAGER,
        "A run this replacement carries has no recorded profile or publisher, so the replacement stays held and even an owner"
        " cannot accept it. Attribute the carried run, or replace the task with a clean one."),
    # Review authority.
    "verified_publisher_review_required": _step(
        "accept_as_owner", AUTHORITY_OWNER_OPERATOR,
        "Assign an agent verifier to review this work; for work with no recorded runs, record provenance first so a verifier can"
        " be shown to be independent. A signed-in workspace owner or operator can instead accept it as owner with a reason,"
        " which needs no provenance; the project policy stays on.", _OWNER_ACCEPT_COMMANDS, UI_ACTION_ACCEPT_AS_OWNER),
    "accountable_review_required": _step(
        "repeat_with_override", AUTHORITY_OPERATOR,
        "Repeat the request with the X-Review-Override: true header and a written reason in X-Command-Reason, or have a person"
        " review the work instead.", {"rest": "POST /api/tasks/{task_id}/review"}),
    "independent_review_required": _step(
        "use_another_reviewer", AUTHORITY_REVIEWER,
        "Ask a reviewer who did not execute or submit this work to review it; an agent reviewer must hold the verifier role."
        " An accountable operator may instead use the review override with a written reason."),
    "owner_acceptance_required": _step(
        "sign_in_as_owner", AUTHORITY_OWNER_OPERATOR,
        "Only a signed-in workspace owner or operator can accept as owner. Ask one of them to accept the task, or to assign an"
        " agent verifier."),
    "override_reason_required": _step(
        "add_override_reason", AUTHORITY_OWNER_OPERATOR,
        "Add a written reason for the owner acceptance and send it again.", _OWNER_ACCEPT_COMMANDS),
    "owner_override_not_required": _step(
        "use_ordinary_review", AUTHORITY_REVIEWER,
        "This project does not require a different review publisher, so accept the task with an ordinary review instead.",
        {"rest": "POST /api/tasks/{task_id}/review"}),
    # Team readiness and routing.
    "agent_team_actor_outside_topology": _step(
        "choose_team_actor", AUTHORITY_TEAM_MANAGER,
        "Choose an actor that is a runtime-ready member of the caller's current team. Read the team setup status: its"
        " non_ready_actors say which members are not ready and its readiness_rule says why, and the project's PM can add or"
        " ready the actor you need.", _TEAM_STATUS_COMMANDS),
    "verifier_outside_topology": _step(
        "choose_team_verifier", AUTHORITY_TEAM_MANAGER,
        "Choose a verifier that is a runtime-ready member of the caller's current team, or have the project's PM add the"
        " verifier to the team. Read the team setup status for the members and what keeps each from being ready.",
        _TEAM_STATUS_COMMANDS),
    "verifier_not_runtime_ready": _READY_TEAM_ACTOR,
    "caller_not_runtime_ready": _step(
        "ready_caller_actor", AUTHORITY_TEAM_MANAGER,
        "The calling actor is not runtime-ready in its team. Read the team setup status: its non_ready_actors and"
        " readiness_rule say what is missing for the caller; the project's PM can make it ready, then repeat the request.",
        _TEAM_STATUS_COMMANDS),
    "caller_not_bound_to_topology": _step(
        "bind_caller_to_topology", AUTHORITY_OPERATOR,
        "The calling actor is not a member of any live team. A workspace operator can add it to the team in team setup; then"
        " repeat the request.", _TEAM_STATUS_COMMANDS),
    "model_aware_routing_preview_unavailable": _step(
        "ready_routing_topology", AUTHORITY_TEAM_MANAGER,
        "Model-aware routing is waiting for its team. Read the team setup status, ready the actors this refusal lists in"
        " topology_readiness, then repeat the preview.", _TEAM_STATUS_COMMANDS),
    # Manual provenance records.
    "manual_provenance_candidate_unverifiable": _step(
        "correct_provenance_candidate", AUTHORITY_PROVENANCE_RECORDER,
        "Correct the head commit, commit list, pull request or base commit named in this refusal so they are immutable GitHub"
        " URLs of one candidate, then record provenance again.", _PROVENANCE_COMMANDS, UI_ACTION_RECORD_PROVENANCE),
    "manual_provenance_execution_recorded": _step(
        "reconcile_recorded_execution", AUTHORITY_TEAM_MANAGER,
        "The task already has recorded execution, which supplies its own provenance, so a record is refused. Reconcile that"
        " execution, or replace the task with a clean one."),
    "manual_provenance_requires_resolved_work": _step(
        "resolve_before_provenance", AUTHORITY_ANY,
        "Record provenance only on resolved, uncanceled leaf work. Resolve the task first, then record it."),
    "manual_provenance_pr_not_task_evidence": _step(
        "link_pull_request_first", AUTHORITY_PROVENANCE_RECORDER,
        "Link the pull request to the task, as a GitHub link or a progress artifact, first; then record provenance again.",
        _PROVENANCE_COMMANDS, UI_ACTION_RECORD_PROVENANCE),
    "manual_provenance_executor_unknown": _step(
        "name_known_executor", AUTHORITY_PROVENANCE_RECORDER,
        "Name an executor that exists: a known person, or a known agent actor.", _PROVENANCE_COMMANDS,
        UI_ACTION_RECORD_PROVENANCE),
    "manual_provenance_executor_outside_project": _step(
        "name_project_executor", AUTHORITY_PROVENANCE_RECORDER,
        "Name an agent executor that is a member of the task's project or holds an assignment in it.", _PROVENANCE_COMMANDS,
        UI_ACTION_RECORD_PROVENANCE),
    "manual_provenance_executor_conflict": _step(
        "name_manual_executor", AUTHORITY_PROVENANCE_RECORDER,
        "The task is in manual execution, so a record can only name the person who executed it.", _PROVENANCE_COMMANDS,
        UI_ACTION_RECORD_PROVENANCE),
    "manual_provenance_human_recorder_required": _step(
        "record_as_signed_in_person", AUTHORITY_PROVENANCE_RECORDER,
        "A human executor can be recorded only by a signed-in workspace owner, operator or project manager, not by an agent.",
        {"rest": "POST /api/tasks/{task_id}/manual-provenance"}),
    "manual_provenance_record_limit": _step(
        "replace_overrecorded_task", AUTHORITY_TEAM_MANAGER,
        "The task already has the most provenance records review can read. Replace it with a clean task."),
    "manual_provenance_recorder_unattributable": _step(
        "fix_recorder_agent", AUTHORITY_TEAM_MANAGER,
        "The recording agent lacks a profile, binding or model publisher. Give its enabled model bindings a publisher, or have"
        " a person record the provenance."),
    "manual_provenance_executor_unattributable": _step(
        "fix_executor_agent", AUTHORITY_PROVENANCE_RECORDER,
        "The agent executor lacks a profile, binding or model publisher. Name a model binding of that actor whose catalog entry"
        " declares a publisher, on an actor with a profile.", _PROVENANCE_COMMANDS, UI_ACTION_RECORD_PROVENANCE),
    "provenance_recorder_required": _step(
        "ask_provenance_recorder", AUTHORITY_ANY,
        "Only a signed-in workspace owner, operator or project manager, or the project's PM agent, can record provenance. Ask"
        " one of them."),
    "observation_actor_unverifiable": _step(
        "name_actor_through_run", AUTHORITY_ANY,
        "Name an actor through a run or an assignment of a task you can read, then record the observation again."),
}

# Steps a raise site picks when it knows the cause, by name. ``record_provenance`` is chosen only where the refusal already
# names the manual provenance remedy, because a record is refused for work with recorded runs or execution.
VARIANTS: dict[str, dict[str, Any]] = {
    "record_provenance": _RECORD_PROVENANCE,
    "resubmit_artifact": NEXT_STEPS["verification_candidate_unverifiable"],
    "carried_run_unattributed": NEXT_STEPS["replacement_contribution_unattributed"],
    "give_verifier_publisher": _step(
        "give_verifier_publisher", AUTHORITY_TEAM_MANAGER,
        "The verifier's model binding declares no publisher, so independence cannot be shown. Give an enabled binding of the"
        " verifier a catalog entry with a publisher, then assign it again.", _ASSIGN_VERIFIER_COMMANDS),
    "runs_submit_candidate": _step(
        "runs_submit_candidate", AUTHORITY_EXECUTOR,
        "The task's recorded agent runs must supply a submitted repository candidate. Have the executing agent resubmit its"
        " work with its pull request or commits; a provenance record cannot replace a run.", {"mcp": "agent_submit_my_work"}),
    "retry_candidate_check": _step(
        "retry_candidate_check", AUTHORITY_VERIFIER,
        "The candidate could not be verified on GitHub. Retry the verdict once GitHub is reachable; if it keeps failing, have"
        " the executor resubmit the artifact with the exact pull request or compare URL.", _REVIEW_QUEUE_COMMANDS),
    "unrecorded_publisher": _step(
        "unrecorded_publisher", AUTHORITY_OWNER_OPERATOR,
        "No contributing run or execution records a model publisher, so independence cannot be shown. " + _ACCEPT_AS_OWNER_POLICY
        + " Otherwise redo the work so a run records its observed model.", _OWNER_ACCEPT_COMMANDS, UI_ACTION_ACCEPT_AS_OWNER),
    "profile_evidence_missing": _step(
        "profile_evidence_missing", AUTHORITY_OWNER_OPERATOR,
        "A contributing run or the reviewer has no recorded profile, which a provenance record cannot add. Give the verifier a"
        " profile and assign it again; for runs that never recorded a profile, " + _ACCEPT_AS_OWNER_POLICY[0].lower()
        + _ACCEPT_AS_OWNER_POLICY[1:], _OWNER_ACCEPT_COMMANDS),
    "enable_routing_mode": _step(
        "enable_routing_mode", AUTHORITY_DEPLOYMENT_OPERATOR,
        "Model-aware routing is switched off for this deployment. The deployment operator sets MODEL_AWARE_ROUTING_MODE to"
        " shadow or enforced and restarts the backend; previews work in either mode."),
}

# Strings that look like refusal codes in the source but are not refusals.
NOT_REFUSAL_CODES = frozenset({
    "verification_code", "verification_path", "verification_burden", "verification_burden_axis", "verification_required",
    "candidate_unverifiable", "manual_provenance_event_id", "manual_provenance_record", "manual_provenance_recorded",
    "owner_acceptance_override", "owner_acceptance_override_task_ids", "owner_override_accepted", "reviewer_profile_id",
    "reviewer_profile_ids",
})


def _fill(step: dict[str, Any], task_id: int | None) -> dict[str, Any]:
    step = deepcopy(step)
    if task_id is not None:
        step["commands"] = {key: value.replace("{task_id}", str(task_id)) for key, value in step["commands"].items()}
    return step


def next_step_for(code: str | None, *, task_id: int | None = None, variant: str | None = None) -> dict[str, Any] | None:
    """The machine-readable next step for a refusal code, or None when the code has none.

    ``variant`` names the step the raise site chose for its cause; an unknown name is a
    programming error. ``{task_id}`` in a command is filled in when the task is known and
    left as a path template otherwise.
    """
    if variant is not None:
        return _fill(VARIANTS[variant], task_id)
    entry = NEXT_STEPS.get(code or "")
    return None if entry is None else _fill(entry, task_id)


def with_next_step(detail: dict[str, Any], *, task_id: int | None = None) -> dict[str, Any]:
    """Add the code's next step to a refusal envelope that does not carry one yet."""
    if "next_step" in detail:
        return detail
    step = next_step_for(detail.get("code"), task_id=task_id)
    return detail if step is None else {**detail, "next_step": step}
