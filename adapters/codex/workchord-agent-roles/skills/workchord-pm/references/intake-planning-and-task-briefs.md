# Intake, Planning, and Task Briefs

Use this reference to move uncertain requests through Triage and turn accepted outcomes into independently executable leaf tasks.

## Contents

- [Run Triage](#run-triage)
- [Report a system defect](#report-a-system-defect)
- [Choose a disposition](#choose-a-disposition)
- [Decompose accepted work](#decompose-accepted-work)
- [Write the complete task brief](#write-the-complete-task-brief)
- [Check definition and start readiness](#check-definition-and-start-readiness)
- [Complete phase contracts](#complete-phase-contracts)

## Run Triage

1. Create or read the Triage item with title, description, source, source URL, external key, project or iteration hints, priority hint, labels, and safe metadata.
2. Read request-source links and duplicate suggestions before creating a second record.
3. Treat duplicate and classification suggestions as advisory. Inspect evidence, score, confidence, rationale, unmatched labels, and proposed project or assignee.
4. Request a transient task draft only after reading the source. Verify every grounded fact, warning, open question, risk, and ungrounded suggestion.
5. Ask for clarification when a decision-changing fact is missing. Update the item with the question and available context; keep it `new` or snooze it until a defined follow-up time.
6. Record one explicit disposition.

Do not invent a `clarify` status. Use an update plus `new`, or use `snoozed` with a follow-up time and reason.

Do not use a universal duplicate-score threshold. Scores are advisory and may
change with the classifier. Mark a duplicate only after the PM confirms that
the candidate owns the same requested outcome and that preserving the source
link will not lose distinct acceptance, ownership, or timing information. For
partial overlap, keep separate items and link the shared source/context, or
decompose them under an explicit common parent after acceptance. Never silently
merge distinct outcomes or discard the non-overlapping portion.

## Report a System Defect

Create this Triage item the moment the PM observes WorkChord itself
faulting during an otherwise normal read or mutation: a response that
contradicts its documented or advertised contract, a data or invariant
inconsistency across re-reads, a crash, or a defect in a tool/endpoint
separate from the caller's own input or a known supervised-v0 gap. This is
distinct from [Triage Discoveries](verification-rework-and-recovery.md#triage-discoveries),
which routes a worker's business-domain findings; a self-observed system
defect follows the same intake mechanics below.

1. Label it `bug` plus the `agent` source label so it is distinguishable
   from a business intake request in the same queue.
2. Title it with the faulting operation. Describe the exact endpoint or
   tool, the request sent, the expected versus observed response or state,
   and minimal reproduction steps.
3. Preserve any trace ID, correlation ID, run ID, or timestamp already in
   hand. Never fetch or paste credentials, private keys, or full raw logs to
   document it.
4. Set a source value that marks agent self-detection (for example
   `agent-observed-defect`) and a priority hint from actual user or data
   impact, not investigative convenience.
5. Link the source task, assignment, or run the defect surfaced in when one
   exists; do not block that unrelated object's own disposition on this new
   item.
6. Route it through the normal disposition flow in
   [Choose a Disposition](#choose-a-disposition); a defect report earns no
   special-cased lifecycle.

## Choose a Disposition

| Disposition | Apply when | Required evidence |
| --- | --- | --- |
| Accept | The problem is understood and should enter planning, but task conversion is not yet ready or is intentionally separate | Outcome, owner, priority rationale, remaining planning step |
| Convert | A real iteration and complete executable task payload are known | Selected iteration/project, task brief, effort, dependencies, labels, capacity owner |
| Decline | The request should not be pursued | Reason and accountable decision owner |
| Snooze | A known date or input should trigger reconsideration | `snoozed_until`, reason, expected input |
| Mark duplicate | An existing Triage item or task owns the outcome | Exactly one duplicate target and optional source-link action |
| Clarify | A missing fact changes scope, value, acceptance, access, or routing | Question, requester/owner, next review time; preserve `new` or snooze |

Before conversion:

- Confirm the target iteration exists and is plannable.
- Match the task project to a project-scoped iteration.
- Set `project_id` explicitly, including explicit null, when converting into an unscoped iteration and a hint would otherwise be ambiguous.
- Use an `assignee_id` from the selected iteration only.
- Use dependencies from the same iteration.
- Preserve the intake source, external key, source URL, and request-source links.
- Treat a second conversion conflict as success only after refetching and confirming the existing converted task is the intended one.

## Decompose Accepted Work

1. Keep a parent task only for roll-up when several deliverables share one accepted outcome.
2. Create leaf tasks that one worker can complete and one verifier can evaluate.
3. Separate work when ownership, capability, dependency, risk, artifact, or verification method differs.
4. Add dependencies only for real predecessor constraints. Confirm the dependency graph has no self-edge, duplicate edge, cycle, or cross-iteration edge before mutation.
5. Set priority from `1` to `10`, where `1` is highest. Do not use priority as a hidden queue rank.
6. Set positive effort and distinguish effort from elapsed schedule time.
7. Set project and milestone consistently; never attach a milestone from another project.

8. Add the governed `agent` source label plus at least one active capability label, such as `cap:code`, `cap:test`, `cap:docs`, or `cap:research`, for agent-dispatched work.
9. Mark optional or deferred work explicitly and record the reconsideration trigger for deferral.
10. Leave schedule dates to the scheduling flow; use minimum start and maximum end constraints only when they are real.

For stable PM automation, create and revise these tasks with
`agent_create_planning_task` and `agent_patch_planning_task`, or their matching
agent-planning REST routes. Supply the required idempotency key, rationale, and
correlation ID. The older `agent_create_task` and `agent_patch_task` names are
supervised-v0 compatibility primitives, not the audited decomposition contract.

## Write the Complete Task Brief

Put this structure in the task description until the live server exposes equivalent typed fields. Preserve concrete source links and verification commands.

```markdown
## Goal
State the observable outcome and why it matters.

## Context and sources
Link the request, relevant files or records, prior decisions, and known evidence.

## Scope
List the changes or investigation that belong to this task.

## Out of scope
Name adjacent work the worker must report instead of absorbing.

## Constraints and risks
Record compatibility, security, migration, rollout, timing, and access limits.

## Expected deliverables
Name the files, records, artifacts, or decisions that must exist.

## Acceptance criteria
Use independently checkable statements.

## Verification
Give commands, checks, reviewer expectations, and required evidence.

## Dependencies and inputs
Name predecessor tasks, external inputs, and the state that satisfies each one.

## Handoff and escalation
Name the reviewer and conditions requiring PM or human input.
```

Reject vague phrases such as “make it work,” “update as needed,” or “test everything.” Name paths, behavioral boundaries, compatible versions, expected outputs, and the minimum sufficient evidence whenever they are knowable.

Never place credentials, private keys, secret values, or inaccessible personal context in the brief.

## Check Definition and Start Readiness

### Definition-ready

Require all of these before routing or scheduling:

- Use a leaf task in a real iteration.
- Complete every task-brief section or explicitly state “none” with rationale.
- Link the correct project and optional milestone.
- Set positive effort and priority.
- Set a valid same-iteration dependency graph.
- Add `agent` plus at least one active governed capability label for agent work.
- Set an iteration capacity owner or record the exact recommendation decision still required.
- Resolve all open questions that could change scope.
- Set constraints that make the work schedulable.
- Name expected artifacts, verification evidence, reviewer, and escalation conditions.

Treat the current server's description-length and keyword readiness check as a minimum signal, not proof of this contract.

### Start-ready

Require definition readiness to remain true, then require:

- scheduled start and end dates;
- completed hard dependencies;
- no deferral;
- no conflicting live claim or run;
- `planned` status for normal work;
- an exact due execution assignment in assigned-work v1, or one explicit PM-to-worker task handoff in supervised v0;
- rejection or recovery evidence plus an explicit owner for active rework/recovery.

Re-read `agent_readiness.criteria`, blockers, warnings, task version, schedule, dependencies, claim, and assignment immediately before dispatch.

## Complete Phase Contracts

### Phase 4: Triage intake

**Preconditions**

- Preserve the originating request and requester-visible evidence.
- Avoid assuming that a Triage hint is an accepted planning decision.

**Required reads**

- Read the item, request-source links, duplicate suggestions, classifications, governed labels, candidate projects/iterations, and any prior converted task.

**Allowed mutations**

- Update intake metadata; accept, decline, snooze, mark duplicate, classify, draft, or convert through explicit lifecycle actions.
- Link sources without copying secret content.

**Exit and postcondition checks**

- Re-read the item and confirm exactly one recorded disposition.
- After conversion, re-read both the `converted` item and its planned task with preserved source context.

**Evidence and stop rules**

- Record disposition reason, source, duplicate decision, confidence limits, chosen hierarchy, and next owner.
- Stop when source evidence is unavailable, duplicate ownership is unresolved, or conversion lacks a real iteration and executable brief.

### Phase 5: Define executable work

**Preconditions**

- Confirm accepted outcome, project boundary, iteration, and available team context.

**Required reads**

- Read templates, labels, existing task tree, dependencies, project/milestone, iteration team, source links, and relevant prior decisions.

**Allowed mutations**

- Create or update task hierarchy, description, effort, priority, capacity assignee, project, milestone, dependencies, labels, flags, and constraints.
- Use optimistic task versions where supported.

**Exit and postcondition checks**

- Re-read each leaf task and its readiness criteria.
- Confirm the brief, links, dependency graph, capacity ownership, and definition-ready result.

**Evidence and stop rules**

- Record decomposition rationale, dependency reasons, estimate basis, required capability, verifier, and exact blockers.
- Stop on a cycle, cross-iteration dependency, ambiguous scope, missing acceptance evidence, or stale task version.
