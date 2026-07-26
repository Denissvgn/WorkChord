# Verification, Rework, and Recovery

Use this reference to evaluate resolved work independently, close accepted tasks, return failed work through an explicit rework handoff, recover stale execution, and publish durable project updates.

## Contents

- [Build an independent verification packet](#build-an-independent-verification-packet)
- [Handle model evidence and escalation](#handle-model-evidence-and-escalation)
- [Record a verdict](#record-a-verdict)
- [Return work for rework](#return-work-for-rework)
- [Recover stale or inconsistent execution](#recover-stale-or-inconsistent-execution)
- [Triage discoveries](#triage-discoveries)
- [Publish project updates](#publish-project-updates)
- [Complete the phase contract](#complete-the-phase-contract)

## Build an Independent Verification Packet

1. Read the current task, version, complete brief, acceptance criteria, verification instructions, dependencies, source links, and timeline.
2. Read the execution assignment, claim/release state, run detail, terminal result, artifact links, commit or PR link, summary, and error.
3. Confirm that no run remains active and no worker still holds a live execution lease.
4. Map each acceptance criterion to submitted evidence.
5. Re-run or independently inspect the required verification when authorized and safe. Record commands, environment, result, and limitations.
6. Review scope and out-of-scope boundaries for silent expansion or missing deliverables.
7. Review unresolved risks, warnings, partial checks, skipped tests, migration/rollback evidence, and required human approvals.
8. Keep the verifier independent from the implementation actor for high-risk work. Require a human or separately scoped verifier when independence cannot be established.

Do not accept a succeeded run, green local check, commit link, or worker summary as sufficient by itself. Verify the task's stated outcome.

Create a verification-purpose assignment only after the task is `resolved`, its
execution run is terminal, and its claim is released. Under
`model-aware-routing-v1`, request a fresh verification-purpose routing preview
against current independent actors and bindings; the verifier named in the
earlier assessment or execution preview was policy evidence, not reserved
capacity. Bind the resulting assignment to the exact verifier, current
task/run/assessment versions, selected binding, and fresh preview digest. Rank
verification work in the verifier's own queue by explicit review rank and task
priority; do not place it in an implementation queue or reserve execution
capacity while the task is still active.

## Handle Model Evidence and Escalation

Read the execution assignment's selected binding and routing snapshot beside
the run's configured alias, binding ID/revision, observed resolved model, and
trust state. Keep the evidence classes distinct:

| Trust state | Meaning | PM response |
| --- | --- | --- |
| `matched` | Worker-reported model is consistent with the configured binding or an allowed alias | Continue only if all other evidence passes; label it self-reported, not attested |
| `mismatch` | Reported model materially differs from the selected binding | Stop verification/closure, preserve evidence, and use typed recovery or operator escalation |
| `unreported` | Required observed model data is absent | Stop model-aware acceptance and request supported runtime evidence or recovery |
| `unverifiable` | The server cannot compare the declaration and report reliably | Require supervised judgment; never call the model independently verified |

A normal PM must not edit or bypass a binding to clear a mismatch. Ask an
operator to reconcile configuration when catalog/binding metadata is wrong, or
use typed recovery/reassignment when the execution attempt is wrong. Keep
credentials, prompts, provider secrets, and raw runtime logs out of routing
evidence.

Escalate model capability only when run, review, or failure evidence is
attributable to reasoning, context, modality, or tool insufficiency. Record the
specific insufficiency and create a fresh assessment/preview before rework or
recovery. Access denial, missing credentials, unavailable dependencies,
rate-limited or down external services, scheduling conflicts, and invalid task
scope are non-model blockers: correct or escalate their actual cause without
buying a higher model tier. Never downgrade an independent/specialist review
requirement during rework.

## Record a Verdict

### Pass

Pass only when every acceptance criterion has evidence and remaining risk is explicitly accepted by the accountable owner.

In assigned-work v1, submit the typed review verdict with the review assignment, current `expected_task_version`, criterion results, evidence links, limitations, required rationale/correlation metadata, and optional rejection handoff. A pass atomically performs the server-owned `resolved -> closed` transition; a rejection atomically reopens the task and creates ordered rework. Re-read task, review/rework assignments, pipeline, milestone/project progress, and timeline from the verdict response.

In supervised v0, append a concise `agent.checkpoint` with verification evidence only when separately authorized, then let the accountable human or PM transition `resolved -> closed` with the current task version and reason. Re-read the response because closure sets actual end data and can roll up parents.

### Reject

Reject when any acceptance criterion fails, evidence is missing, required verification cannot be trusted, or unresolved risk exceeds the task's acceptance boundary.

Record:

- failed criterion and expected versus observed result;
- exact reproduction or check output summary;
- evidence and artifact links;
- severity and impact;
- whether the original scope remains valid;
- minimum required rework;
- proposed owner, rank, and not-before condition;
- verifier identity and task/run versions.

Do not close partially accepted work. Split follow-up work only when the original criterion can be truthfully accepted without it; otherwise reject the current task.

## Return Work for Rework

In assigned-work v1:

1. Submit one typed rejection verdict with the rework actor, rank, evidence,
   reason, and current task/review versions through the advertised verdict
   operation.
2. Require that transaction to transition `resolved -> active`, fulfill the
   verification assignment, and create an ordered execution assignment with
   `queue_class=rework`; there is no separate client-side send-to-rework call in
   stable v1.
3. Set the exact actor, queue rank, reviewer, rejection evidence, and expected
   task/review versions. If a not-before condition is required but the verdict
   schema does not support it, update the newly returned queued assignment with
   its current queue revision as a separate idempotent PM action.
4. Confirm that no old execution claim or run remains current.
5. Re-read the worker queue and require the server to surface the item as rework, not normal planned work.

For model-aware rework, require the rejection transaction or follow-up routing
flow to preserve the prior assessment, assignment, run, routing snapshot, and
failure reason as lineage. Generate a fresh execution preview before selecting
the rework actor/binding. Change the required model envelope only through a new
current assessment backed by evidence; never copy an empty routing snapshot or
silently reuse the prior candidate list.

In supervised v0:

1. Append the rejection evidence before status change.
2. Let the accountable PM or human transition `resolved -> active` with the current task version and reason.
3. Hand the explicit task ID to one unique worker under supervision.
4. Start a new run without repeating the cosmetic `planned -> active` transition.
5. Track the manual rework owner because the current global ready list contains only planned tasks.

Never leave rejected active work without an explicit next owner. Never reset it to `planned` merely to make it appear in the ready list.

## Recover Stale or Inconsistent Execution

Prefer the server's idempotent reconciler and typed recovery actions when available. Otherwise stop automated dispatch and assign a human recovery owner.

Do not declare work abandoned from an agent-local elapsed-time heuristic. Use
the server's recovery result and codes, evaluated against server time, lease
expiry, assignment state, run heartbeat/status, and ownership consistency.
Inactivity alone is evidence for review, not authority to cancel or requeue. If
the server cannot make that determination, stop dispatch and give the full
state tuple to the accountable recovery owner.

| Observed state | Required response |
| --- | --- |
| Planned task with expired claim and no run | Re-read readiness; release or let expiry clear under the supported contract, then explicitly redispatch. |
| Active task with no live claim and no running run | Mark recovery-required; choose resume/reassign/cancel through an audited action. Do not silently edit it to planned. |
| Running run with expired or missing claim | Stop worker writes, preserve trace, terminate or reconcile the run, then create recovery work. |
| Resolved task with a running run | Do not verify or close; reconcile the run and task evidence first. |
| Disabled actor holding work | Stop dispatch, request operator identity action, and recover assignments/claims explicitly. |
| Multiple live claims or running runs for one task/actor | Return attention-required, freeze mutations, and escalate with all IDs and timestamps. |
| Claim owner, assignment actor, and run actor disagree | Treat as split-brain ownership; do not choose one locally. |
| Ambiguous timeout during close, rework, or recovery | Refetch task, assignment, review, claim, run, and idempotency result before retrying. |

For each recovery:

1. Capture server time, last task version, assignment/review versions, claim actor/expiry/fence, run IDs/statuses, and last progress.
2. Stop new work for the affected actor or task.
3. Choose the smallest safe typed recovery action.
4. Reuse the same idempotency key only for an identical retried request.
5. Re-read every execution dimension and pipeline placement.
6. Record the recovery cause, action, response, next owner, and follow-up prevention.

For model-aware recovery, preserve the original assessment, selected binding,
routing snapshot, run model evidence, and recovery cause. Require a fresh
preview for the recovery assignment. A stale or mismatched binding may require
operator correction, but recovery never grants the PM authority to mutate the
catalog or bypass a hard gate.

Stable `agent_requeue_recovery` /
`POST /api/agent/recovery/{task_id}/requeue` is one audited transaction: it
locks and revalidates the task, refuses a healthy ownership tuple, cancels live
stale assignments and running runs, clears the stale claim, preserves their
history, keeps active work active (or explicitly reopens an inconsistent
resolved task), increments the task fence/version, and creates exactly one
ordered `queue_class=recovery` assignment. Verify every returned canceled ID and
the fresh assignment; never emulate these side effects with separate calls.

Always use the typed recovery GET result as the optimistic command token. Echo
the complete `expected_live_assignment_ids`, `expected_running_run_ids`,
`expected_claim_generation`, and `expected_task_version` into requeue. The live
assignment list includes every purpose participating in the reconciliation
decision. If a live verification assignment or any other ownership changes,
the server rejects the command; refetch and decide explicitly instead of
cancelling it indirectly.

Review verdict and recovery writes also require a deterministic idempotency
key, rationale, and correlation ID. Preserve the same three values only for an
exact retry; changing rationale or correlation creates a different audited
request and must not replay the prior command.

Do not fabricate a `blocked` task status. Use a typed blocker or recovery event, governed label when appropriate, and an accountable recovery owner.

## Triage Discoveries

Classify worker discoveries before changing the plan:

| Class | PM response |
| --- | --- |
| Blocking | Record the blocker, link it to the source task/run, and decide immediate recovery, dependency, or clarification. |
| Confidence-reducing | Record the uncertainty or verification gap; decide whether to expand verification, rework, or accept risk. |
| Non-blocking/out of scope | Create linked Triage intake and keep the current task scope unchanged. |

For discovery Triage, preserve the source task, run, project, iteration, artifact, and originating actor through safe metadata or request-source links. Then check duplicates, classify, convert, defer, decline, or clarify through the normal intake flow. For partial overlap, keep a separate linked item or explicitly decompose under a common accepted parent; do not claim a merge occurred unless the live API exposes and records that action.

Do not silently add discovery work to an active worker's scope.

## Publish Project Updates

Append a structured project update after a meaningful delivery, verification, risk, or recovery decision. Use:

- `health`: `unknown`, `on_track`, `at_risk`, or `off_track` with evidence;
- `summary`: concise stakeholder outcome;
- `progress_text`: completed and active outcomes, not activity volume;
- `risks_text`: impact, likelihood, owner, mitigation, and trigger;
- `decisions_text`: decision, rationale, approver, and date;
- `next_steps_text`: next outcome, owner, and expected time.

Read the current project summary and latest update before appending. Never overwrite history. Re-read update freshness and project target risk after writing.

In stable v1, use `POST /api/agent/projects/{project_id}/updates` or
`agent_create_project_update` with `reports:write`, evidence checked,
required rationale and correlation, and a deterministic idempotency key.
REST sends the audit fields in `X-Agent-Rationale` and `X-Correlation-ID`; MCP
uses the named `rationale` and `correlation_id` arguments. Confirm
`created_by_actor_id`, then re-read the update list and project health. If the
live deployment lacks that authorized mutation, return the structured draft to
the human owner and state clearly that no durable update was written.

## Complete the Phase Contract

### Phase 8: Verify, report, and learn

**Preconditions**

- Require a resolved task for normal verification.
- Require a terminal execution run, released claim, submitted artifacts, current versions, and an independent reviewer.

**Required reads**

- Read task/brief, timeline, assignment, claim, run, artifacts, source links,
  project summary, milestone/release state, latest project update, and discovery
  Triage. For model-aware work, also read assessment, routing snapshot, selected
  binding, observed model, trust state, and a fresh verification preview.

**Allowed mutations**

- Submit a typed pass/reject verdict when available, preserving model-routing
  lineage and independent/specialist requirements.
- Transition `resolved -> closed` on pass or `resolved -> active` through explicit rework on reject.
- Create linked Triage, perform audited recovery, and append a project update within granted authority.

**Exit and postcondition checks**

- Re-read task status/version, review and execution assignments, routing
  snapshots/model evidence, pipeline, milestone/project progress, project update
  freshness, and new rework/recovery ownership.
- Leave every rejected or recovered task with one explicit next owner.

**Evidence and stop rules**

- Record criterion-by-criterion results, commands/checks, artifacts, limitations, verdict, status transition, project impact, and next owner.
- Stop when independence is missing, model trust is mismatch, unreported, or
  unverifiable without accepted supervised handling, evidence conflicts, a run
  remains active, current versions are stale, durable rework/recovery is
  unavailable for unattended work, or the project-update write is unauthorized.
