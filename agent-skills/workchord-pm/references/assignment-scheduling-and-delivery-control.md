# Assignment, Scheduling, and Delivery Control

Use this reference to route definition-ready work, create an ordered dispatch, schedule it against capacity, and supervise execution without taking over worker-owned state.

## Contents

- [Route capacity ownership](#route-capacity-ownership)
- [Route exact actor and model bindings](#route-exact-actor-and-model-bindings)
- [Dispatch exact actors](#dispatch-exact-actors)
- [Order assigned work](#order-assigned-work)
- [Schedule and re-read](#schedule-and-re-read)
- [Supervise delivery](#supervise-delivery)
- [Complete phase contracts](#complete-phase-contracts)

## Route Capacity Ownership

1. Read task assignee recommendations after completing the task brief and capability labels.
2. Compare each candidate's score, confidence, matched skills, weakness matches, workload warnings, and rationale.
3. Read the candidate's current profile, iteration capacity, workload, and vacations. Do not rely only on the recommendation summary.
4. Consider review independence, production access limits, domain context, and planned operational load.
5. Choose one iteration `TeamMember` as capacity owner and write its ID to `Task.assignee_id`.
6. Re-read the task, member workload, and readiness after assignment.

Treat recommendations as explainable advice. Do not auto-assign solely by top score, and never infer permissions from a capability profile.

The top team-member/capacity recommendation is never an exact actor or model
selection. It may inform `Task.assignee_id`, but exact dispatch requires the
separate roster, assessment, routing-preview, and assignment contracts below.

## Route Exact Actor and Model Bindings

Use this loop only when the live capability response advertises
`model-aware-routing-v1`, reports effective `shadow` or `enforced` mode, and
the live operation metadata contains the matching assessment and preview
fields. In `shadow`, perform steps 1 through 6 only, retain the preview as
comparison evidence, and use supervised compatibility dispatch without a
model-aware selection claim. Perform model-bound assignment steps 7 and 8 only
in effective `enforced` mode with matching assignment and begin-evidence
fields.

1. Re-read the definition-ready leaf, current task version, capacity owner,
   current typed assessment, bounded immutable assessment history, policy
   version, dependencies, schedule, workload, vacations, exact actor roster,
   and active model bindings.
2. Reject a missing or stale assessment. Require exactly one current immutable
   assessment for this task/policy version; do not reuse an assessment from an
   earlier task version or average away an advanced axis.
3. Request a non-dispatching routing preview for purpose `execution`. It does
   not mutate task or assignment state; `shadow` may append bounded audit
   evidence. Preserve its preview ID, input digest, generation/expiry time,
   assessment ID/version, task version, actor queue revisions, binding
   revisions, ordered eligible candidates, excluded candidates, blocker codes,
   and review policy.
4. Inspect every hard exclusion. Require actor authorization and purpose
   compatibility, matching profile/capacity ownership, skills and weaknesses,
   adequate model/tool/data-policy metadata, availability, workload, vacation,
   queue, schedule, and one-current-task compliance. A profile, model, or cost
   match cannot bypass any hard gate.
5. Rank only eligible candidates. Within the best adequacy and availability
   class, select the lowest-cost adequate binding; then apply the advertised
   queue, schedule, latency, and stable actor-ID tie-breakers. Cost or latency
   never compensates for missing permission, skill, tier, tool, policy,
   independence, or capacity.
6. If no candidate is eligible, create no assignment. Preserve the returned
   blockers and choose a legitimate PM action: clarify, decompose, reschedule,
   defer, change supported planning inputs, or ask an operator to correct
   staffing/binding metadata. Never lower a hard minimum silently or mutate a
   model binding as a normal PM.
7. Create the assignment with the current task/assessment/policy versions,
   selected actor and model-binding ID/revision, routing preview ID and complete
   digest, purpose, queue data, deterministic idempotency key, rationale, and
   correlation ID. Let the server recompute eligibility and generate the
   bounded routing snapshot; do not submit client-authored candidate evidence
   as authoritative truth.
8. Re-read the task, assignment, actor queue, selected binding, and server-owned
   routing snapshot. Confirm that the selected versions and reason codes match
   the decision and that the snapshot contains no credentials, prompts, or raw
   logs.

Discard the preview and start again after expiry or any task, assessment,
dependency, capacity, vacation, actor policy/queue, binding, reviewer, purpose,
or topology-membership change. On stale-candidate or digest conflict, refetch
authoritative inputs, read the assessment history, create a new assessment only
when a new task version requires one, and generate a fresh preview.
Reassignment or any update that changes actor, binding, purpose, or reviewer
also requires a new preview; queue-only reordering may reuse evidence only when
the live policy explicitly permits it.

Low confidence is not a hard-blocker override. Clarify or seek supervised
judgment when confidence is below the live policy threshold. If the effective
mode is `off` or `shadow`, or the model-aware feature or one required live
operation is absent, keep the assigned-work queue only when its base feature
set is complete, use the existing supervised capability/capacity comparison,
and label the actor/model choice as not model-aware. A shadow preview is
comparison evidence, not assignment authority.

## Dispatch Exact Actors

### Assigned-work v1

Use exact actor dispatch only when the server advertises a durable assignment contract and an enabled actor roster. Confirm that the actor is already provisioned, enabled, compatible, appropriately scoped, and bound to the intended profile. For model-aware routing, require effective `enforced` mode and complete the preview loop above before mutation; for `off`, `shadow`, or compatibility routing, state that no enforced model-aware adequacy claim was made.

Create or update an audited assignment with:

- task ID and current task version;
- exact actor ID;
- purpose `execution` or `verification`;
- queue class `normal`, `rework`, or `recovery`;
- lifecycle state, explicit queue rank, and optional not-before time;
- capacity owner/profile and reviewer;
- routing rationale and matched capabilities;
- for model-aware dispatch, assessment/policy versions, selected model-binding
  ID/revision, preview ID/digest, and server-generated routing snapshot;
- rework, recovery, reassignment, or cancellation reason when applicable.

Use the server's assign, reassign, reorder, cancel, rework, and recovery commands exactly as advertised. Stable v1 assignment and recovery writes require an expected assignment/task token, one deterministic idempotency key, a concise rationale, and a correlation ID; REST carries the last three as `Idempotency-Key`, `X-Agent-Rationale`, and `X-Correlation-ID`, while MCP exposes named arguments. Re-read the assignment and actor queue after every command.

Never let assignment bypass definition or start readiness. Never treat assignment as claim ownership.

### Supervised v0

An older or partially upgraded server may expose only an iteration capacity
assignee and global ready list, without durable actor-specific assignment or
actor roster/profile binding. Apply all constraints:

1. Select one ready leaf task under direct PM or human supervision.
2. Choose one already provisioned unique worker outside the task record.
3. Hand the exact task ID and expected outcome to that worker through the trusted orchestration channel.
4. Record the exact task-to-actor handoff in the trusted human/orchestration record available to the supervised deployment. Do not pretend that this record is a durable v1 assignment or include claim or credential data.
5. Do not claim the task on behalf of the worker.
6. Do not call the global ready-list ordering a worker queue.
7. Do not dispatch a second current task to the same actor.

Keep unattended parallel dispatch disabled in supervised v0. Assigned-work v1
adds durable controls but still permits only one current task per actor; higher
concurrency requires a later API and skill version.

## Order Assigned Work

In assigned-work v1, set queue order explicitly. Expect the server to select work by:

1. a compatible resumable current execution;
2. assigned rework;
3. assigned recovery;
4. normal assigned work whose not-before or scheduled start is due;
5. future assigned work as `wait`, never as early-start permission.

Within one queue class, order by explicit queue rank, priority (`1` highest), not-before or scheduled start, task `sort_order`, and task ID as a stable tie-breaker. Require the work response to include its selection reason and complete sort tuple.

Treat pagination cursors as opaque, actor-bound snapshots. Read the first work
page for the authoritative decision, then follow `pagination.next_cursor` only
to inspect the remaining ready and blocked collections. Restart at the first
page on `409 stale_cursor`; never act on a later page as if it changed `next`.
Verifier and recovery reads return `{items, pagination}` and follow the same
rule. REST `/me/work` may return `304` for a matching private weak ETag; retain
the prior body only when the request limit and cursor are identical, and use
the response's fresh `Retry-After` instead of the retained poll timestamp.

Keep verification-purpose assignments out of the implementation-worker queue.
Stable v1 supports only explicit `assigned_only` dispatch with one current
item. Treat managed unassigned-pool acquisition and higher concurrency as
future contracts, even if a newer server later exposes them.

Account for expected review effort in the task estimate and verifier workload
before dispatch. A planned verifier in an assessment or execution preview is
policy evidence, not a capacity reservation. After execution resolves and its
claim/run are terminal, request a fresh `verification` routing preview against
current independent actors and bindings before creating the verification
assignment. If review effort is material enough to require its own dates or
artifacts, plan a linked verification leaf task with its own capacity owner;
otherwise record the review allowance in the selected verifier's operational
load and do not claim that Gantt reserved it automatically.

In supervised v0, order work manually and hand off only the current explicit task. Treat task `sort_order` as tree order, not a reliable cross-project or per-worker queue.

## Schedule and Re-read

1. Read the iteration, calendar, tasks, dependency graph, constraints, capacity, workload, vacations, and current Gantt before scheduling.
2. Capture the affected task versions, dates, owners, effort, and current overload warnings.
3. Call `agent_preview_schedule` or the REST `/api/agent/planning/iterations/{id}/schedule/preview` command with required idempotency, rationale, and correlation metadata. It persists an exact receipt but rolls back hypothetical task dates.
4. Submit both the complete `expected_task_versions` map and the
   `expected_input_digest` from that preview to `agent_apply_schedule` or the
   matching REST apply route. The digest binds iteration/calendar dates,
   capacity, vacations, task scheduling fields, dependency edges, and active
   scheduling rules. Re-preview after any of those inputs change.
5. Inspect every scheduling decision, delayed or overdue result, workload issue, and task outside constraints.
6. Re-read Gantt, task dates and versions, member workload, readiness, project target risk, and dependent dates.
7. Adjust scope, effort, capacity, owner, constraints, dependency, deferral, iteration dates, or queue order explicitly. Re-run only after changing an input or recording why the same inputs need another attempt.

Do not hide schedule failure by deleting dependencies, removing vacations, lowering effort, or changing constraints without evidence. Scheduling can cascade dates; inspect affected tasks before dispatch.

Choose schedule mitigation in this order unless an accountable owner records a
different policy: first correct bad estimates, calendars, constraints, or
dependency data; then split executable scope or move optional work; then add or
reassign genuinely available capacity; then defer a lower-value outcome. Change
an externally relied-on scope/date/release commitment only as a last resort and
only after the commitment owner approves it durably. Never trade away required
acceptance, security verification, vacations, or dependency truth to make dates
appear feasible.

## Supervise Delivery

Use the pipeline states as a control view:

| Pipeline view | PM action |
| --- | --- |
| Needs definition | Return to the task brief, labels, effort, dependencies, schedule, and capacity owner. |
| Ready for agent | Confirm start readiness, exact dispatch mode, reviewer, and handoff evidence. |
| Executing | Inspect assignment, task status, claim expiry, run, latest checkpoint, artifacts, blockers, and lease health. |
| Verification required | Route to an independent verifier; do not send back to the implementation loop without a rejection verdict. |

For executing work:

1. Read the task and merged timeline.
2. Read the durable assignment and current-work state when supported.
3. Read claim actor and expiry, task version, current and recent runs, last run event, artifacts, commit or PR links, and run terminal state.
4. Compare all states. Flag running run without live claim, active task without an owner, resolved task with running run, expired claim with active execution, disabled actor holding work, or multiple current runs.
5. Read the worker's blocker or discovery evidence before modifying the plan.
6. Let healthy work continue. Avoid noisy PM events that obscure worker checkpoints.
7. Page the complete verifier or recovery collection with its opaque cursor before choosing an intervention; restart on snapshot drift.
8. Use explicit cancel, reassign, recovery, or rework actions when supported. Under supervised v0, stop additional dispatch and ask the human recovery owner to reconcile the separate claim, run, and task states.
9. Re-read pipeline and affected task after intervention.

Never edit worker-produced artifacts, finish the worker run, or transition active work merely to make the board look consistent. Treat push notifications as hints and refetch authoritative state before acting.

## Complete Phase Contracts

### Phase 6: Route, assign, order, and schedule

**Preconditions**

- Require a definition-ready leaf task and configured iteration capacity.
- Confirm the operating mode and available dispatch surface.

**Required reads**

- Read task, versions, dependencies, readiness, capacity recommendations,
  profiles, weaknesses, capacity, workload, vacations, actor roster,
  assignments, iteration, calendar, and Gantt. For model-aware routing, also
  read the current assessment, policy, catalog/bindings, exclusions, and fresh
  routing preview.

**Allowed mutations**

- Set the iteration capacity assignee, constraints, and deliberate planning fields.
- Create or change exact actor assignments only through advertised v1 commands;
  require a fresh version-bound preview for model-aware selection and every
  routing-relevant reassignment.
- Schedule the selected iteration and update queue order with optimistic concurrency where supported.

**Exit and postcondition checks**

- Re-read task, capacity owner, actor/binding dispatch, routing snapshot, queue,
  dates, readiness, Gantt, workload, and target risk.
- Confirm each task is start-ready, explicitly waiting, or returned to definition with exact blockers.

**Evidence and stop rules**

- Record the distinction between capacity advice and exact routing, assessment
  and preview versions, candidate exclusions, adequacy/cost choice, confidence,
  capacity impact, actor/binding and reviewer, queue rank, schedule decisions,
  and blockers.
- Stop on stale task/assessment/preview/binding state, no eligible candidate,
  overload without mitigation, missing exact assignment support, incompatible
  actor, unresolved dependency, or unexplained schedule violation.

### Phase 7: Supervise delivery

**Preconditions**

- Require a recorded dispatch and known execution owner.

**Required reads**

- Read pipeline, task/timeline, assignment, claim, run detail, progress, artifacts, blockers, and project/iteration risk.

**Allowed mutations**

- Use the bounded assignment/recovery command whose receipt and server-generated timeline event record the PM decision or escalation.
- Re-plan PM-owned fields only after recording the reason and coordinating with the current owner.
- Use audited cancel, reassign, recovery, or rework commands when supported.

**Exit and postcondition checks**

- Re-read all affected execution dimensions and pipeline placement.
- Leave exactly one accountable next owner and no silently abandoned active work.

**Evidence and stop rules**

- Record observed state tuple, last progress time, recovery or wait decision, affected IDs, and next review trigger.
- Stop on inconsistent ownership, missing fence/recovery support, ambiguous terminal mutation, or a security/access blocker.
