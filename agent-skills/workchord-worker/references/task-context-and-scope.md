# Task Context And Scope

Use this reference before beginning, after any conflict, and before terminal
submission.

## Validate The Complete Context

Re-fetch the selected task and timeline. Compare them with the work decision.
Require:

- exact execution assignment, actor, purpose, queue class, and assignment state;
- task ID, current version, `planned` or valid rework/recovery `active` status,
  iteration, project, milestone, capacity owner, priority, and schedule;
- parent chain and confirmation that the task is an executable leaf;
- every dependency ID, state, and satisfaction rule;
- readiness result with stable blocker/warning codes;
- current claim owner, claim expiry/fence summary, and run summary;
- reviewer/verifier, expected evidence, source links, and relevant timeline
  decisions.

Stop when the task and decision disagree. Never repair the disagreement by
editing planning fields.

## Require An Executable Brief

Require these sections or equivalent typed fields:

| Section | Worker question |
| --- | --- |
| Goal | What observable outcome must exist, and why? |
| Context and sources | Which files, records, decisions, and evidence apply? |
| Scope | What changes or investigation belong here? |
| Out of scope | Which adjacent work must be reported instead? |
| Constraints and risks | Which compatibility, security, migration, rollout, timing, or access limits apply? |
| Expected deliverables | Which files, records, artifacts, or decisions must exist? |
| Acceptance criteria | Which independently checkable statements define success? |
| Verification | Which commands, checks, reviewer steps, and evidence are required? |
| Dependencies and inputs | Which predecessor states or external inputs are required? |
| Handoff and escalation | Who reviews, and what requires PM/human input? |

Do not begin if an omission can change implementation scope, safety, or the
meaning of success. Emit or return exact missing-context reasons and request PM
clarification. Description length, labels, and capability matches alone do not
make a task executable.

## Respect Readiness

Require `start_ready` for normal autonomous work. Confirm that:

- the definition remains complete;
- scheduled dates exist and `not_before` is due according to server time;
- hard dependencies satisfy the advertised policy;
- the task is not deferred;
- this actor has the queued execution assignment;
- no foreign live claim/run exists.

For assigned rework or recovery, require an `active` task with rejection or
recovery evidence, no current execution owner, and a fresh exact assignment.
Do not force it through the normal planned-ready list.

## Preserve PM-Owned Fields

Do not change any of these as an execution worker:

- goal, scope, exclusions, acceptance criteria, priority, effort, or labels;
- project, milestone, iteration, parent, dependency graph, or capacity owner;
- actor assignment, queue class/rank, schedule, constraints, reviewer, or
  deferral state.

Use only worker lifecycle operations, bounded task/run events, evidence and
artifact attachment, and the allowed worker status transitions. Do not
transition `resolved -> closed`.

If execution proves the plan invalid, stop or continue only the unquestionably
safe in-scope portion. Record a blocker or discovery; let the PM re-plan.

## Handle Discoveries Without Scope Creep

For a real out-of-scope issue:

1. Check the current task and any Triage items already returned in authorized
   context for an obvious duplicate. If the connected MCP surface permits the
   normal `workspace_list_triage_items` read, a narrow title/source search is
   allowed; absence of a broad search surface does not authorize a browser
   session or speculative endpoint.
2. Create a Triage item only when worker policy permits it and the actor has
   `triage:write`. Prefer `POST /api/agent/discoveries` or
   `agent_report_discovery`, which validates the accepted assignment, current
   task version, running run, and live claim/fence in one attributable action.
3. Include a concise problem statement, evidence, impact, proposed urgency,
   current task ID, assignment ID, and run/trace correlation in structured
   metadata. Include no secrets or raw large logs.
4. Use a deterministic idempotency key for the logical discovery and preserve
   the returned Triage ID; link the discovery to the current task/source when
   the server supports it.
5. Emit a small discovery event containing the Triage ID.
6. Continue only if the discovery is non-blocking and the current acceptance
   criteria remain valid; otherwise report a blocker and stop safely.

Do not convert the discovery to a task, assign it, reorder it, or absorb it into
the current work. Those are PM decisions.

## Prepare Final Evidence

Before success, map every acceptance criterion to:

- the resulting artifact or observable behavior;
- the exact verification command/check and result;
- any remaining limitation or risk;
- durable commit, pull request, report, screenshot, or log link where relevant.

Keep evidence concise and reproducible. Store large outputs in the designated
artifact system and link them. Re-fetch context after verification; do not
submit against a stale task, assignment, claim, or run.
