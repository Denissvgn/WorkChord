---
name: workchord-pm
description: Operate WorkChord as an accountable PM controller. Use when an agent must define initiatives, projects, milestones, releases, iterations, calendars, teams, capability profiles, intake, executable task briefs, assignments, schedules, delivery supervision, verification, rework, recovery, or stakeholder updates in a WorkChord workspace.
---

# WorkChord PM

Control planning and delivery through WorkChord's authoritative records. Shape and dispatch work; do not impersonate a worker, create credentials, or treat capability metadata as permission.

## Start Safely

1. Identify the WorkChord base URL or connected MCP server without exposing credentials.
2. Read the live capabilities contract when the server provides it. Otherwise inspect the available tools and treat the session as supervised v0.
3. When `agent-team-master-v1` is advertised, read the bound team status and
   confirm the controller identity, topology revision, required runtime
   acknowledgements, and `runtime_ready` state. Treat
   `availability_unknown` as intentional until a concrete task is evaluated.
4. Confirm the actor identity, scopes, role, profile binding, work policy, server/API compatibility, and selected project or iteration.
5. Stop before mutation when identity, planning scope, required permission, or server feature support is ambiguous.
6. Read [system-map-and-authority.md](references/system-map-and-authority.md) before establishing a workspace or changing cross-object plans.

Never provision actors, issue or rotate keys, modify runtime secrets, or infer authorization from a profile skill, task label, or installed procedural skill. Ask an operator to perform identity administration.
The Setup Master validate/plan/apply surfaces are operator-only. A bound PM may
read its secret-free topology status and handoffs but must not adopt, create,
replace, disable, activate, or broaden any member.

The full assigned-work v1 PM controller requires both `recovery:read` and
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

## Run the PM Cycle

The six controller steps below map to the detailed eight-phase contracts as
follows: step 1 → phase 1; step 2 → phases 2-3; step 3 → phases 4-5; step 4 →
phase 6; step 5 → phase 7; step 6 → phase 8.

### 1. Establish Authority and Scope

Read identity, scopes, server features, labels, templates, the selected hierarchy, and pipeline state. Name the planning boundary and permitted mutations. Follow [system-map-and-authority.md](references/system-map-and-authority.md).

### 2. Define Outcomes, Timeboxes, and Team Capacity

Select or create the accountable project, milestones or release target, calendar, and real iteration. Configure reusable profiles, iteration capacity rows, availability, utilization, and vacations. Re-read capacity and workload. Follow [team-capacity-and-calendar.md](references/team-capacity-and-calendar.md).

### 3. Triage, Define, and Assess Work

Keep uncertain requests in Triage. Check duplicates and sources; classify, clarify, accept, decline, snooze, mark duplicate, or convert explicitly. Convert only into an iteration-scoped leaf task with a complete brief. When model-aware routing reports an effective `shadow` or `enforced` mode, read the bounded assessment history and create exactly one immutable current five-axis difficulty and routing assessment for the task version before candidate selection. Follow [intake-planning-and-task-briefs.md](references/intake-planning-and-task-briefs.md).

### 4. Route, Assign, Order, and Schedule

Keep capacity ownership separate from exact runtime routing. Compare capability matches, weaknesses, workload, and vacations; then, when `model-aware-routing-v1` is live in effective `shadow` or `enforced` mode, hard-filter exact actor/model bindings against the current assessment before optimizing cost or latency. In `shadow`, preserve the preview only as comparison evidence and use supervised compatibility dispatch. Create a model-bound assignment only in effective `enforced` mode and only from a fresh version-bound routing preview. Set queue rank, not-before time, and reviewer; schedule and re-read Gantt, workload, dependencies, readiness, assignment, and routing evidence. Follow [assignment-scheduling-and-delivery-control.md](references/assignment-scheduling-and-delivery-control.md).

### 5. Supervise Delivery

Inspect assignment, task status, claim expiry, run state, recent progress, artifacts, blockers, and recovery signals. Do not silently edit worker-owned execution. Recover abandoned or inconsistent work explicitly. Follow [assignment-scheduling-and-delivery-control.md](references/assignment-scheduling-and-delivery-control.md) and [verification-rework-and-recovery.md](references/verification-rework-and-recovery.md).

### 6. Verify, Rework, Close, and Report

Compare submitted evidence with every acceptance criterion. Let an independent verifier or accountable PM close accepted work. Reject failed work to an explicitly owned rework queue. Append project health, progress, risks, decisions, and next steps. Follow [verification-rework-and-recovery.md](references/verification-rework-and-recovery.md).

## Preserve Role Boundaries

- Let the PM own scope, priority, dependencies, capacity ownership, actor dispatch, queue order, schedule, reviewer selection, recovery, and reporting.
- Let the assigned worker own `planned -> active -> resolved` during a valid execution attempt.
- Let an independent verifier or accountable PM own `resolved -> closed` or `resolved -> active` for rework.
- Treat `Task.assignee_id` as iteration capacity ownership, not authenticated actor assignment.
- Treat a durable actor assignment as dispatch, not a claim.
- Treat a claim as a temporary execution lease, not task status.
- Treat an agent run as one observable attempt, not proof of acceptance.
- Treat a configured model binding as intended runtime metadata and a worker's
  observed model as self-reported evidence, not independent attestation.
- Keep exactly one current task per actor. Treat a server policy above
  `max_parallel_work=1` as incompatible with this skill version.

## Select the Supported Operating Mode

Use assigned-work v1 only when the live server advertises
`agent-capabilities-v1`, `actor-roster-v1`, `actor-task-assignments`,
`agent-team-master-v1`,
`my-work-v1`, `snapshot-pagination-v1`, `work-etag-v1`,
`complete-task-context`, `atomic-begin-submit`, `atomic-renew-v1`,
`fenced-claims`, `verification-v1`,
`typed-rework-recovery`, `agent-discovery-triage-v1`, and `pm-control-v1`.

Otherwise use supervised v0:

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
