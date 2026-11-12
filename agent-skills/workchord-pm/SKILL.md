---
name: workchord-pm
description: Plan, assign, and supervise WorkChord work as the accountable PM. Use when an agent must define initiatives, projects, milestones, releases, iterations, calendars, teams, capability profiles, intake, executable task briefs, assignments, schedules, delivery supervision, verification, rework, recovery, or stakeholder updates in a WorkChord workspace.
---

# WorkChord PM

Control planning and delivery through WorkChord's authoritative records. Shape and dispatch work; do not impersonate a worker, create credentials, or treat capability metadata as permission.

## Your Part Of The Workflow

People, the PM, workers, and reviewers follow one workflow. As the PM you:

1. **Capture:** run Triage and record one disposition per item; file WorkChord defects as Triage items.
2. **Plan and assign:** date the project and its milestones so the Roadmap shows them, then work the six plan checkpoints people see on the plan page: planning period (`iteration`), people and capacity (`team`), work (`work`), scheduling blockers (`blockers`), schedule (`schedule`), and review (`review`). Read their states with the `plan-readiness` operation, so you and people see the same "n of 6". Write typed briefs, set assignee, milestone, and dependencies, calculate the schedule, then create agent assignments. A plan below 6 of 6 is unfinished; pass the gate in [Finish the Plan Before You Report It](#finish-the-plan-before-you-report-it).
3. **Do:** supervise delivery and recover stuck work; never do the worker's task yourself.
4. **Review:** route each submitted task to an independent reviewer through a verification assignment. The reviewer accepts the work or requests changes; you never accept work yourself.
5. **Report:** publish project updates with health, summary, progress, risks, decisions, and next steps.

The phases below give the detailed contract for each step. Use the names in
[workflow-and-names.md](references/workflow-and-names.md) in everything people read.

## Start Safely

1. Identify the WorkChord base URL or connected MCP server without exposing credentials.
2. Read the live capabilities contract when the server provides it. Otherwise inspect the available tools and treat the session as supervised mode (`supervised v0`).
3. When `agent-team-master-v1` is advertised, read the bound team status and
   confirm the controller identity, topology revision, required runtime
   acknowledgements, and `runtime_ready` state. Treat
   `availability_unknown` as intentional until a concrete task is evaluated.
4. Confirm the actor identity, scopes, role, profile binding, work policy, server/API compatibility, and selected project or iteration.
5. Stop before mutation when identity, planning scope, required permission, or server feature support is ambiguous.
6. Read [system-map-and-authority.md](references/system-map-and-authority.md) before establishing a workspace or changing cross-object plans.

Never provision actors, issue or rotate keys, modify runtime secrets, or infer authorization from a profile skill, task label, or installed procedural skill. Ask an operator to perform identity administration.
The Agent Team Setup validate/plan/apply surfaces are operator-only. A bound PM may
read its secret-free topology status and handoffs but must not adopt, create,
replace, disable, activate, or broaden any member.

The full assigned-work v1 PM role requires both `recovery:read` and
`recovery:write`. A PM without recovery write authority may diagnose and hand
off stale work, but must not claim that the recovery phase is complete.

## Use One Control Loop

For every decision:

```text
read authoritative state
  -> choose one bounded action
  -> mutate with version and idempotency data when supported
  -> re-read the affected state
  -> record rationale, evidence, and next owner
```

Do not batch unrelated mutations. Preview schedule and bulk changes when a dry-run surface exists. Preserve the exact current version after every task, claim, schedule, assignment, or status response.

## Run the PM Phases

### Phase 1: Establish Authority and Scope

Read identity, scopes, server features, labels, templates, the selected hierarchy, and pipeline state. Name the planning boundary and permitted mutations. Follow [system-map-and-authority.md](references/system-map-and-authority.md).

### Phases 2–3: Define Outcomes, Timeboxes, and Team Capacity

Select or create the accountable project, milestones or release target, calendar, and real iteration. Give the project a start date, a target date, an owner, and a status that matches the work, and give each milestone a target date; the Roadmap shows nothing else. Configure reusable profiles, iteration capacity rows, availability, utilization, and vacations. Give every agent that will carry work a capacity row through its profile. Re-read capacity and workload. Follow [team-capacity-and-calendar.md](references/team-capacity-and-calendar.md).

When the work already exists as a plan outside WorkChord, or you check a plan someone else loaded, follow [plan-mapping-and-roadmap.md](references/plan-mapping-and-roadmap.md) from here through Phase 6.

### Phases 4–5: Triage, Define, and Assess Work

Keep uncertain requests in Triage. Check duplicates and sources; classify, clarify, accept, decline, snooze, mark duplicate, or convert explicitly. Convert only into an iteration-scoped leaf task with a complete typed brief. When model-aware routing reports an effective `shadow` or `enforced` mode, read the bounded assessment history and create exactly one immutable current five-axis difficulty and routing assessment for the task version before candidate selection. Follow [intake-planning-and-task-briefs.md](references/intake-planning-and-task-briefs.md).

### Phase 6: Route, Assign, Order, and Schedule

Keep capacity ownership separate from exact runtime routing. Compare capability matches, weaknesses, workload, and vacations; then, when `model-aware-routing-v1` is live in effective `shadow` or `enforced` mode, hard-filter exact actor/model bindings against the current assessment before optimizing cost or latency. In `shadow`, preserve the preview only as comparison evidence and use supervised compatibility dispatch. Create a model-bound assignment only in effective `enforced` mode and only from a fresh version-bound routing preview. Dispatch a task to the agent whose profile holds the task's assignee row, and name the reviewer profile on the same assignment. Set queue rank, not-before time, and reviewer; schedule and re-read Gantt, workload, dependencies, readiness, assignment, and routing evidence. Follow [assignment-scheduling-and-delivery-control.md](references/assignment-scheduling-and-delivery-control.md).

### Phase 7: Supervise Delivery

Inspect assignment, task status, claim expiry, run state, recent progress, artifacts, blockers, and recovery signals. Do not silently edit worker-owned execution. Recover abandoned or inconsistent work explicitly. Follow [assignment-scheduling-and-delivery-control.md](references/assignment-scheduling-and-delivery-control.md) and [verification-rework-and-recovery.md](references/verification-rework-and-recovery.md).

### Phase 8: Verify, Rework, Close, and Report

Create a verification assignment for an independent reviewer (the `verifier` role, guided by the `workchord-reviewer` skill). The reviewer checks every acceptance criterion and accepts the work or requests changes with an explicit rework owner. Read the verdict, confirm the next owner, and append project health, progress, risks, decisions, and next steps. Keep project status and milestone status in step with the work, so the Roadmap stays true. Follow [verification-rework-and-recovery.md](references/verification-rework-and-recovery.md).

## Finish the Plan Before You Report It

Creating tasks is not planning. A plan is finished when a person can read it without you: the Roadmap shows each project as a dated bar with its milestones, the task list shows an assignee on every planned task, and the Gantt chart shows who carries each task and when it happens. Work the checkpoints in order, and never describe a plan as ready, scheduled, or handed off below 6 of 6.

1. **Date the outcome.** Set `start_date`, `target_date`, `owner_profile_id`, and a true `status` on the project, and a `target_date` on every milestone. A project without dates and without a dated milestone has no bar on the Roadmap.
2. **Staff before you fill.** Add every participating profile to the iteration as a capacity row before you create or import tasks. An iteration without capacity rows cannot hold an assignee, so nothing in it can be scheduled.
3. **Give every agent a row.** An agent carries planned work through the capacity row of the profile it is bound to. One row is one agent's queue: the scheduler places a row's tasks one after another, as the agent does them.
4. **Use records, not labels.** Create a milestone record for each intermediate outcome and set `milestone_id` on its tasks. A label such as `milestone:core`, `phase:2`, or `model:fast`, or an ID prefix in a title, is not a record: people cannot group, date, or assign by it.
5. **Assign every planned leaf.** Set `assignee_id` to a capacity row of the same iteration on every planned leaf task. Do not leave it for dispatch: an agent assignment names the agent that executes, and the server requires it to match the row that carries the effort.
6. **Let the scheduler date the work.** Preview and apply the schedule only after assignment. The scheduler skips a task without an assignee, so a date on such a task is not a calculated date. Never write `start_date` or `end_date` to make a task look scheduled or ready to start.
7. **Prove it.** Re-read `plan-readiness`, the Gantt chart, and the project. Require `tasks_without_assignee` and `tasks_without_effort` to be `0`, every checkpoint `done`, and a recorded reason for every task the schedule left without dates. `has_schedule` alone only says that tasks carry dates.

Run this gate once for the whole iteration after every bulk create or import, before any dispatch. The full check, row by row, is in [plan-mapping-and-roadmap.md](references/plan-mapping-and-roadmap.md#check-the-plan-before-you-report-it).

When a checkpoint cannot be completed — a missing `team:write` scope, no suitable profile, an agent without a profile, or exceeded capacity — stop at that checkpoint. Report "n of 6", the blocking checkpoint with its reason codes and counts, and the person who must act. Do not start a later checkpoint to make the plan look complete.

When you find a plan that someone else loaded below 6 of 6, report its state the same way before you dispatch anything from it, and complete the missing checkpoints in order.

## Preserve Role Boundaries

- Let the PM own scope, priority, dependencies, capacity ownership, actor dispatch, queue order, schedule, reviewer selection, recovery, and reporting.
- Let the assigned worker own `planned -> active -> resolved` during a valid execution attempt.
- Let an independent reviewer own `resolved -> closed` (Accept) or `resolved -> active` for rework (Request changes). A person may do the same in WorkChord; a PM agent never does.
- Treat `Task.assignee_id` (the assignee people see) as iteration capacity ownership, not authenticated actor assignment.
- Treat a durable actor assignment as dispatch, not a claim.
- Treat a claim as a temporary execution lease, not task status.
- Treat an agent run as one observable attempt, not proof of acceptance.
- Treat a configured model binding as intended runtime metadata and a worker's
  observed model as self-reported evidence, not independent attestation.
- Keep exactly one current task per actor. Treat a server policy above
  `max_parallel_work=1` as incompatible with this skill version.

## Select the Supported Operating Mode

Use assigned mode only when the live server advertises every feature below.

<!-- BEGIN GENERATED: WORKCHORD-ROLE-FEATURES -->
Assigned mode (`assigned-work v1`) requires every one of these live features; this list is generated from the role package metadata:

- `actor-roster-v1`
- `actor-task-assignments`
- `agent-capabilities-v1`
- `agent-discovery-triage-v1`
- `agent-team-master-v1`
- `atomic-begin-submit`
- `atomic-renew-v1`
- `canonical-task-brief-v1`
- `complete-task-context`
- `fenced-claims`
- `my-work-v1`
- `pm-control-v1`
- `snapshot-pagination-v1`
- `typed-rework-recovery`
- `verification-v1`
- `work-etag-v1`
<!-- END GENERATED: WORKCHORD-ROLE-FEATURES -->

Otherwise use supervised mode (`supervised v0`):

1. Hand one explicit task ID to one unique worker actor.
2. Confirm that the task is a scheduled, ready, iteration-scoped leaf and has an iteration capacity owner.
3. Coordinate claim, run, and task-state calls under human or PM supervision.
4. Track partial failures and reconcile each independent state explicitly.
5. Keep verification, rework dispatch, stale-work recovery, and final closure human-controlled.

Never simulate a missing assignment, queue, fence, review, or atomic transaction in prose. Stop and request the missing server or human action.

Model-aware routing is additive inside assigned-work v1. Read the explicit
`model_aware_routing` capability status; feature presence alone does not select
an operating mode. Effective `shadow` permits catalog, assessment, and preview
comparison only. Do not send a model-aware assignment/update or present a
shadow recommendation as an enforced selection. Effective `enforced` permits
the complete preview-bound assignment and begin-evidence loop when live REST or
MCP metadata exposes every required operation. In effective `off`, or when the
status, feature, or a required operation is absent, keep the durable
assigned-work lifecycle when otherwise supported but use supervised
compatibility routing and state explicitly that the actor/model choice was not
model-aware. Never infer missing model capability from a deployment name,
provider-facing model name, profile summary, or local prose.

When `agent-team-master-v1` is present, the roster is scoped to the caller's
current runtime-ready topology. Preserve the topology revision from status and
routing preview evidence. Any setup, membership, package, profile, binding, or
acknowledgement change requires a fresh status read and a fresh routing preview;
never dispatch to an actor visible only in a manifest or an older receipt.

## Handle Failures Conservatively

- Treat `401` and `403` as stop conditions; do not seek broader credentials.
- Treat version, assignment, queue-revision, or claim `409` as a signal to refetch and re-evaluate.
- Treat assessment, routing-preview, model-binding, or topology `409` as a
  signal to discard the candidate decision and generate a fresh preview.
- Correct validation failures before retrying; do not resend an unchanged invalid request.
- Retry timeout, `429`, or `5xx` responses only when the operation supports idempotency. Reuse the same idempotency key for the same logical request.
- Read current state before retrying an ambiguous terminal mutation.
- Escalate split-brain task/assignment/claim/run state instead of choosing a convenient interpretation.

## Report System Defects

Treat a fault in WorkChord itself — a response that contradicts its documented contract, a data or invariant inconsistency, a crash, or any other defect distinct from the request or business data being handled — as intake, not a silent workaround. File a Triage item for it in the same control-loop iteration it surfaced; do not defer it to a later pass or fold it into an unrelated task, event, or report. Continue the interrupted action only when the defect does not put task, assignment, claim, or run state in question; otherwise stop and escalate per [Handle Failures Conservatively](#handle-failures-conservatively). Follow [Report a system defect](references/intake-planning-and-task-briefs.md#report-a-system-defect).

## Record Evidence

Record the decision, changed object IDs, rationale, source links, recommendation evidence, readiness blockers, workload or schedule impact, verification results, recovery action, and next accountable owner through the audited command receipt, server-generated timeline, or project update. Keep secrets, private keys, full prompts, and large raw logs out of events and updates.

Use [api-and-mcp.md](references/api-and-mcp.md) to map each operation to the live REST or MCP surface and to identify compatibility constraints on older supervised-v0 deployments.
