# System Map and Authority

Use this reference to choose the correct WorkChord object, establish authority, and keep planning, assignment, execution, and verification separate.

## Contents

- [Map decisions to objects](#map-decisions-to-objects)
- [Keep execution dimensions separate](#keep-execution-dimensions-separate)
- [Establish authority and scope](#establish-authority-and-scope)
- [Select an operating mode](#select-an-operating-mode)
- [Enforce role ownership](#enforce-role-ownership)
- [Stop and escalate](#stop-and-escalate)

## Map Decisions to Objects

| Object | Put here | Keep out |
| --- | --- | --- |
| Initiative | A strategic grouping shared by several projects | Executable steps or worker queue order |
| Project | One accountable outcome, owner, health state, dates, updates, milestones, and releases | A single implementation action |
| Milestone | An intermediate outcome or checkpoint inside one project | Iteration capacity or claim lifetime |
| Release | A project-scoped shipping or rollout record | General planning timeboxes |
| Iteration | A dated execution and capacity boundary linked to a calendar and optionally a project | Unaccepted or unclear intake |
| Triage item | An uncertain request, source, duplicate candidate, classification, and disposition | Work a worker may immediately execute |
| Task tree | Accepted scope, decomposition, dependencies, ownership, and schedule | Strategy or unrecorded discoveries |
| Team member profile | Reusable capability, interest, and weakness evidence | Permission, credentials, or leases |
| Iteration team member | Capacity ownership, availability, utilization, workload, and vacations for one iteration | Exact authenticated process identity |
| Agent actor | An authenticated automation identity and enforced scopes | Capacity accounting or proof of task acceptance |
| Agent-team topology | Operator-reconciled logical membership, package handoff, and runtime readiness | Task-specific capacity or current availability |
| Agent task assignment | Exact actor dispatch, purpose, rank, and not-before time when the server supports it | Capacity or exclusive execution |
| Claim | Temporary exclusive execution lease | Durable dispatch or task lifecycle |
| Agent run | One traceable execution attempt and its evidence | Acceptance or closure |

Keep uncertainty in Triage. Promote it only after selecting a real iteration and creating an executable task payload. Keep parent tasks as roll-up structure; dispatch only leaf tasks.

## Keep Execution Dimensions Separate

Track all five dimensions independently:

1. Set capacity ownership through the iteration `TeamMember` referenced by `Task.assignee_id`.
2. Set exact process dispatch through a durable actor assignment only when the live server supports it.
3. Track the business lifecycle through `planned`, `active`, `resolved`, and `closed`.
4. Track temporary execution exclusivity through the claim and its expiry or fence.
5. Track each attempt through an agent run, progress events, terminal result, and artifacts.

Never infer one dimension from another. In particular, do not interpret a matching profile, `agent` label, ready result, capacity assignee, active task, or running trace as an exact actor assignment.

## Establish Authority and Scope

Treat this as PM phase 1.

### Preconditions

- Obtain a configured WorkChord connection and an already provisioned PM actor or authorized human session.
- Obtain the intended workspace, initiative, project, or iteration from the request or existing records.
- Keep all credentials in the runtime secret store; never echo or persist them.

### Required reads

1. Read live capabilities if available; otherwise enumerate the connected tools and record supervised-v0 mode.
2. Read actor identity, enabled state, role, profile binding, scopes, work policy, and concurrency limit when exposed.
3. When the server advertises `agent-team-master-v1`, read
   `agent_get_team_setup_status` or `GET /api/agent/team-setup/status` and
   confirm this PM is the current controller of a runtime-ready topology.
4. Read projects, iterations, governed labels, reusable templates, and the agent pipeline.
5. Read the selected project summary, iteration summary, relevant task tree, Triage queue, and current updates.
6. Check server/API compatibility against the installed skill manifest when one is present.

### Allowed mutations

- Select an existing planning boundary without mutation.
- Create or update planning objects only after confirming the exact required surface and scope.
- Ask an operator to provision or bind an actor when identity administration is required.
- Read the bound secret-free agent-team status; do not call operator-only setup
  validation, planning, apply, adoption, replacement, or activation surfaces.

Do not create actors, reveal keys, rotate secrets, edit runtime configuration, or broaden scopes as a normal PM action.

Treat an externally relied-on target date, release boundary, scope promise, or
reported health commitment as a stakeholder commitment. Before changing one,
identify the accountable business owner named on the project or decision record
and obtain that owner's explicit approval. Represent approval durably in the
task timeline or project update with approver identity, decision, date,
correlation/source link, and affected object IDs; a chat acknowledgement without
an attributable record is not sufficient. If no accountable owner or approved
recording surface exists, leave the commitment unchanged and report a proposal.

### Exit and postcondition checks

- Name the selected project and iteration, or state that the request remains in Triage.
- Name every mutation class the actor can perform and every required action that remains human/operator-only.
- Re-read the chosen objects before entering the next phase.

### Evidence to record

- Record server/API contract, operating mode, actor ID, relevant scopes, planning boundary IDs, missing features, and escalation owner.
- Record no credential value.

## Select an Operating Mode

### Assigned-work v1

Select assigned-work v1 only after the server explicitly advertises all features used by the flow, including actor/profile identity, durable actor assignments, authoritative current/next work, snapshot-bound pagination, work ETags, complete context, atomic and fenced begin/submit, independent review, and typed recovery.

Use the server's actor roster and assignment state as authority. Never recreate queue selection locally.

### Supervised v0

Select supervised v0 when any required feature is absent. Apply all of these constraints:

- Dispatch one explicit task ID to one unique actor.
- Allow one current task per actor.
- Keep a human or accountable PM in the claim/run/status reconciliation loop.
- Use existing pipeline, task, timeline, run, and claim reads; do not pretend they form an atomic state.
- Keep final verification and stale-work recovery human-controlled.
- Record any partial failure between separate mutations and re-read before continuing.

Do not call a global ready-list result an actor assignment. Do not direct unattended parallel workers from supervised v0.

## Enforce Role Ownership

| Decision or transition | Owner |
| --- | --- |
| Scope, priority, dependencies, labels, capacity assignee, schedule, queue, reviewer | PM or planner |
| Actor/key provisioning and scope grants | Operator or administrator |
| Claim, run, progress, `planned -> active`, `active -> resolved` | Assigned worker |
| Acceptance verdict, `resolved -> closed`, or rejection `resolved -> active` | Independent verifier or accountable PM |
| Recovery of abandoned or inconsistent execution | PM/recovery owner, using an audited server action when available |
| Automatic parent roll-up | Server |

Avoid changing worker-owned active state merely to improve board appearance. Record a blocker or recovery decision instead.

Distinguish product security work from platform identity administration. Actor
scopes, credentials, keys, runtime secrets, and identity bindings remain
operator/admin-owned. A task that changes the product's authorization behavior
may be planned only with an accountable security owner, explicit permitted test
environment and rollback expectations, threat/risk evidence in the brief, and a
human or separately scoped independent verifier. Never put credentials in the
brief or let a capability profile substitute for security approval.
Record the security owner's approval before dispatch in an attributable task
event or project update with owner identity, decision, date, affected boundary,
test/rollback conditions, source/correlation link, and reviewer identity. If the
organization's authoritative security owner cannot be identified or the
approval cannot be recorded durably, keep the task out of executable queues.

## Stop and Escalate

Stop before mutation when any of these conditions holds:

- The actor, planning boundary, or required permission is unknown.
- The request needs actor creation, key handling, or a broader scope.
- Two projects or iterations could own the same task and the requester has not chosen.
- The server does not expose a required durable assignment, verification, or recovery operation.
- The task, assignment, claim, run, and status disagree about the current owner.
- A `401`, `403`, compatibility failure, or ambiguous terminal write occurs.

Report the conflicting IDs and states, the last confirmed version, the missing operation, and the lowest-risk next owner. Do not improvise around the authority boundary.
