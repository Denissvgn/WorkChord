---
name: workchord-worker
description: Execute one WorkChord backlog assignment safely from acquisition through handoff. Use when an implementation, analysis, documentation, test, design, or operations agent must discover or resume its assigned work, validate task context, claim and trace execution, report progress or blockers, submit evidence, resolve work for independent verification, or recover from lifecycle conflicts.
---

# WorkChord Worker

Operate as an execution worker. Let WorkChord decide what work is current;
do not plan, assign, rank, reorder, or verify the backlog yourself.

## Establish The Operating Mode

1. Read [identity-and-my-work.md](references/identity-and-my-work.md).
2. Read actor identity, scopes, server/API contract, work policy, concurrency
   limit, and feature keys from the live capability response when available.
3. Use autonomous v1 only when the server advertises all of:
   `agent-capabilities-v1`, `actor-task-assignments`, `my-work-v1`,
   `snapshot-pagination-v1`,
   `work-etag-v1`, `complete-task-context`, `atomic-begin-submit`,
   `atomic-renew-v1`, `fenced-claims`,
   `typed-rework-recovery`, and `agent-discovery-triage-v1`.
4. Otherwise use supervised v0 only with one task ID explicitly handed off by
   a PM or human. Never select a task from the global ready list in v0.
5. Stop on an incompatible contract, disabled identity, missing execution
   scope, ambiguous actor, or any concurrency policy other than
   `max_parallel_work=1`.

Keep credentials in the client secret store. Never put a key, claim identifier,
fence value, full prompt, or other secret in task prose, events, logs, or
artifacts.

## Execute One Work Decision

1. Fetch the authoritative current/next work decision.
2. Obey its state exactly:

   - `resume`: resume only the returned current assignment and run.
   - `start_assigned`: begin only the returned next assignment.
   - `wait`: do not begin early; poll at or after the server-provided time.
   - `no_work`: report idle state and stop this cycle.
   - `attention_required`: perform no new work; report the recovery codes and
     request PM/operator action.

3. Do not infer priority from the global ready list, notifications, labels,
   profile matches, task IDs, or local state. Treat notifications as refetch
   hints only.
4. Keep exactly one current task at most. Multiple current items or a policy
   above `max_parallel_work=1` are incompatible with this skill version.

## Validate Before Mutation

Read [task-context-and-scope.md](references/task-context-and-scope.md), then
re-fetch the selected task's complete context and timeline. Confirm the exact
assignment, task and version, queue revision, dependency states, readiness,
structured brief, reviewer, expected evidence, and current claim/run summary.

Stop and escalate before beginning when scope, acceptance criteria,
verification, dependencies, authority, or assignment identity is missing or
contradictory. Never repair PM-owned scope, priority, dates, dependencies,
capacity owner, actor assignment, queue rank, or reviewer yourself.

## Begin Or Resume

Read [claim-run-and-task-state.md](references/claim-run-and-task-state.md).

- Prefer the server's atomic begin action. Supply its assignment ID, queue
  revision, lease request, safe run metadata, and one deterministic idempotency
  key. Compare the context task version with the assignment-bound version
  before calling; the server revalidates that binding inside begin.
- Replace cached assignment, task version, claim/fence, expiry, and run values
  with every authoritative response.
- For normal work, accept only the server-owned `planned -> active` transition.
- For explicit rework or recovery, accept an already-`active` task and begin a
  new fenced run; do not perform a cosmetic status transition.
- In supervised v0, follow the documented claim/start/activate sequence and
  stop for PM reconciliation after any partial or ambiguous result.

## Work Inside The Lease

- Execute only the accepted scope.
- Renew with jitter around one-third to one-half of the lease lifetime. Stop all
  task-bound writes immediately after lease or fence loss.
- Emit bounded progress/checkpoint events and durable artifact links. Keep raw
  logs and sensitive data elsewhere.
- Use the claim-bound discovery action to create linked Triage for genuine
  out-of-scope work. Do not absorb it into the current assignment.
- Report a blocker through the supported typed action or event. Do not invent a
  `blocked` task status and do not silently choose replacement work.

Use [events-errors-and-recovery.md](references/events-errors-and-recovery.md)
for event contents, retry rules, failures, cancellations, and inconsistent
state.

## Submit Or Stop

1. Re-fetch the work decision and complete context.
2. Confirm that the assignment, task version, live claim/fence, and running run
   still match.
3. Prefer atomic submit to record final evidence, finish the run, transition
   `active -> resolved`, fulfill the assignment, and release the claim.
4. On failure or cancellation, use the typed terminal action so the run,
   release, and PM recovery signal remain consistent.
5. In supervised v0, use the documented multi-call sequence and surface every
   partial result for reconciliation.
6. Never transition `resolved -> closed`, verify your own high-risk work,
   self-assign, reassign, reorder, or silently continue onto another task.

## Choose The Transport

Read [api-and-mcp.md](references/api-and-mcp.md) before making calls. Prefer MCP
when the client already exposes the WorkChord tools; otherwise use REST.
Do not mix transports during one mutation unless recovery requires an
authoritative read and preserves the same actor identity.

Apply this control rule throughout:

```text
read authoritative state
  -> perform one bounded mutation
  -> accept returned versions and fences
  -> re-read affected state
  -> record evidence or escalation
```
