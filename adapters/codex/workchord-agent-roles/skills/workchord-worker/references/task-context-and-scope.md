# Task Context And Scope

Use this reference before beginning, after any conflict, and before terminal
submission.

## Validate The Complete Context

Re-fetch the selected task and timeline. Compare them with the work decision.
Require:

- exact execution assignment, actor, purpose, queue class, and assignment state;
- task ID, current version, `planned` or valid rework/recovery `active` status,
  iteration, project, milestone, assignee, priority, and schedule;
- parent chain and confirmation that the task is an executable leaf;
- every dependency ID, state, and satisfaction rule;
- readiness result with stable blocker/warning codes;
- current claim owner, claim expiry/fence summary, and run summary;
- reviewer/verifier, expected evidence, source links, and relevant timeline
  decisions.

Stop when the task and decision disagree. Never repair the disagreement by
editing planning fields.

## Require An Executable Brief

Use `context.task.brief` whenever it exists (`brief_source: canonical`). Its
`goal`, `context`, `scope`, `exclusions`, `artifact_expectations`, `verification`,
and ordered `acceptance_criteria` are authoritative. `task_brief` is a legacy
Markdown projection; it can disagree with the canonical brief. Use it only
when the typed brief is absent. Never derive criterion identities from text,
checkboxes, list positions, or the legacy description.

Retain each criterion's exact `id`, `revision`, `text`, and `verification`,
along with `task.version`, `brief_revision`, and `artifact_revision`. Treat
`task.progress` as current execution evidence only when its revision bindings
match the current brief and artifact. Historical progress is evidence of an
earlier attempt, not proof that the current criteria are complete.

Require these sections or equivalent typed fields:

| Section (typed field) | Worker question |
| --- | --- |
| Goal (`goal`) | What observable outcome must exist, and why? |
| Context (`context`) | Which files, records, decisions, and evidence apply? |
| Scope (`scope`) | What changes or investigation belong here? |
| Out of scope (`exclusions`) | Which adjacent work must be reported instead? |
| Constraints and risks (headed paragraph in `context`) | Which compatibility, security, migration, rollout, timing, or access limits apply? |
| Expected artifacts (`artifact_expectations`) | Which files, records, artifacts, or decisions must exist? |
| Acceptance criteria (`acceptance_criteria`) | Which independently checkable statements define success, and how is each checked? |
| Verification approach (`verification`) | Which commands, checks, reviewer steps, and evidence are required? |
| Dependencies and inputs (dependency links and `context`) | Which predecessor states or external inputs are required? |
| Handoff and escalation (headed paragraph in `context`) | Who reviews, and what requires PM/human input? |

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
Do not force it through the normal planned-ready list. Read the latest review's
`criteria` packet, whether an agent reviewer or a person wrote it: each entry
names a criterion `id` and `revision`, a `result` of `pass`, `fail`, or
`not_checked`, and a `note`. Fix every `fail`, and check `not_checked` criteria
again before you submit.

When the work decision is `wait`, read its blocker codes before you report:

| Blocker code | Means | Your action |
| --- | --- | --- |
| `schedule_missing` | The task has no calculated dates, usually because it has no assignee or no effort. | Start nothing. Report the code and the task to the PM. |
| `scheduled_start_future` | The calculated start date is later than today. | Start nothing. Wait; report it only when you have no other work and the PM should know you are free. |
| `not_before_future` | The assignment's not-before time has not arrived. | Wait until that time. |
| A dependency code | A predecessor is not finished. | Wait; never start the predecessor yourself. |

Never ask for dates to be written by hand and never write them. The PM clears
these codes by changing a scheduling input and calculating the schedule again.

## Report Plan Gaps Without Repairing Them

A task that reaches you should already be fully planned. Read these values from
the complete context and compare them with your own profile binding from the
capability response:

| Read | A complete plan shows | Gap to report |
| --- | --- | --- |
| `task.assignee` | The capacity row of your own profile | No assignee, or a row of another profile |
| `assignment.team_member_id` | The same row as the task's assignee | A different row, or none |
| `task.start_date`, `task.end_date` | Calculated dates | Missing dates on work the server let you begin, such as rework |
| `assignment.reviewer_profile_id` | A profile other than yours | None, or your own profile |
| `task.milestone` | The milestone the task belongs to, when its project has milestones | None while sibling tasks have one |

The work decision stays authoritative. A gap in this table is not a reason to
refuse `start_assigned` or `resume`, and it is never yours to repair.

1. Begin or resume as the decision says.
2. Report every gap once, in your first `agent.checkpoint` task event of the
   run. Add a `plan_gaps` list to its payload, one short sentence per gap, for
   example "Task has no assignee; I am working on it as agent 12."
3. Do not repeat the report on later events, and do not mark the task Blocked
   for a plan gap.
4. Name the same gaps in your submit summary when they still hold, so the
   reviewer and the PM see them beside the evidence.

Report as a blocker, not as a plan gap, anything that changes scope, safety, or
the meaning of success.

## Preserve PM-Owned Fields

Do not change any of these as an execution worker:

- goal, scope, exclusions, acceptance criteria, priority, effort, or labels;
- project, milestone, iteration, parent, dependency graph, or assignee;
- agent assignment, queue class/rank, schedule, constraints, reviewer, or
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

For canonical success, include `criterion_progress` in the typed submit body:
one entry per current criterion with `criterion_id`, `criterion_revision`,
`state: completed`, and non-empty `evidence`. Include durable artifact URLs in
`artifact_links`. Send the current `expected_task_version` and the exact
assignment/run/claim-generation tuple. Submit records implementation evidence;
independent review records acceptance. A stale criterion revision or changed
scope requires recovery and a fresh assignment, not relabeling old evidence.
