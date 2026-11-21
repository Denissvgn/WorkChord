# Model-aware routing operations

Model-aware routing selects an exact actor and provider-neutral model binding
only after the existing task, actor, capability, data-policy, and capacity
checks pass. Model metadata never grants permission and never contains provider
credentials.

## Security and ownership

An operator owns the model catalog, actor bindings, rollout mode, and topology
readiness process. Planner and worker actors retain their existing least-
privilege scopes. Tool and data-policy tags constrain candidate eligibility;
they do not authorize access to a tool, repository, network, or private data.

Do not place API keys, tokens, credential-bearing endpoints, prompts, raw task
content, private logs, or provider event payloads in catalog entries, bindings,
routing events, metric labels, or webhooks. Worker-reported model identifiers
are unverified comparison evidence unless a separate trusted attestation
mechanism supplies stronger evidence.

Historical performance remains advisory. Do not feed it back into selection
policy without a separately approved calibration contract covering sample
size, decay, bias review, and operator approval.

## Rollout modes

`MODEL_AWARE_ROUTING_MODE` is restart-bound and must have the same value on all
application replicas.

| Mode | Behavior |
| --- | --- |
| `off` | Model-aware routing is not advertised. Existing supervised assignment remains available and historical routing evidence stays readable. |
| `shadow` | The server may create bounded previews for operator comparison, but they cannot become enforced claims or be presented as enforced selections. |
| `enforced` | New model-aware assignments may use exact actor and binding selections only when authoritative topology readiness is satisfied and runtime evidence is required. |

The capability handshake reports both configured and effective modes. Treat the
effective mode and its blocker codes as authoritative. A configured
`enforced` value does not override missing or unsatisfied topology readiness.
Topology readiness has no environment, API, or UI override. It must come from a
server-side topology authority. If a deployment does not integrate that
authority, keep the configured mode `off`; configured `shadow` or `enforced`
will remain effective `off`.

## Enablement

1. Keep `MODEL_AWARE_ROUTING_MODE=off` while upgrading the database and
   application.
2. Create secret-free, provider-neutral catalog entries and revisioned actor
   bindings through the protected operator API.
3. Reconcile the operator-owned planner/worker topology, acknowledge its
   runtimes, and verify the live roster. Do not infer readiness from UI state.
4. Upgrade compatible planner, worker, and reviewer role packages.
5. Confirm the deployment's server-side topology authority reports the expected
   topology identity and revision. Stop at `off` when that authority is absent.
6. Set every application replica to `shadow`, restart them, and confirm the
   capability handshake reports `shadow` as the effective mode.
7. Compare shadow previews with supervised decisions. Investigate no-candidate,
   stale-input, model-mismatch, verifier-rejection, rework, and escalation
   evidence without copying private task content into the review record.
8. Set every replica to `enforced` only after topology readiness is satisfied,
   the roster is current, and workers can report binding and resolved-model
   evidence at begin.

Enablement applies only to new assignments. Never rewrite historical snapshots
or reinterpret a shadow preview as an enforced selection.

## Supervised rework in shadow mode

After an independent reviewer requests changes, read the original worker's
assigned-work queue and complete task context. The server can return
`start_assigned` for an existing or newly issued rework assignment when its
stored rejection and submission identify the same team, worker, model binding
and independent reviewer. The worker begins the exact assignment with the
current queue revision and its observed model. Repeating the begin with the
original idempotency key returns the same run and claim generation.

The latest submitter can also have completed a supervised recovery selected
by the team's PM. The recovery receipt and event must confirm that exact
assignment and actor. Earlier retained contributors continue to participate
in the independent publisher check. The recovery records the task version
when it was issued. The fulfilled assignment must match the later task
version in the worker's submission receipt.

The issued assignment and its routing snapshot preserve their original
lineage. The effective worker views show the supervised handback and review
floor. A successful begin records the complete worker binding, independent
reviewer floor, rejected run, verifier receipt and reviewed candidate digest
in the new run's `execution_provenance.supervised_rework`. The original
verdict and submission stay intact. If an older rejection omits the explicit
candidate digest, the verifier's selection in its event and receipt must
identify the same submitted candidate. For the next verification, preview,
dispatch and verdict require the recorded reviewer profile and a publisher
independent of every contributor. A changed binding, different worker,
missing receipt, or request for a model-tier change leaves routing pending.
After a failed or canceled rework, the PM uses the normal recovery path.
The resulting recovery queue waits for a fresh applicable routing selection.
A previously begun rework cannot be reused to start a second fenced run.
Enforced mode continues to require a fresh model-aware selection.

## Extending an iteration with assigned work

A date-only extension reserves the iteration and every open task version.
Existing ownership can continue when the task, assignment, model bindings,
team, capacity owner and project review policy still match. Workers read
their assigned queue and current task version before renewing or submitting.
The recorded planning evidence identifies the snapshot by its ID, SHA-256
and input revision. A worker command verifies current authority and the
applicable historical evidence under its operation’s locks.
Verification uses the originally selected artifact and reviewer. A rework
begin still checks its independent rejection and the original submitter.

For a cutoff applied before `iteration-window-execution-recovery-v1`, a
workspace operator can preview a single task with
`POST /api/agent/tasks/{task_id}/reconcile-planning-window` or
`agent_reconcile_planning_window`. Supply the planning receipt's
`planning_actor_id` and `planning_command_key`. The server checks its own
before-change snapshot, the exact end-date-only command, and each live
owner’s original receipt. Check the returned task version, assignment IDs
and empty `missing` list. Apply with the returned `expected_evidence_digest`,
`apply=true`, and normal idempotency, rationale and correlation metadata.
The command records operator attribution. The original assignment, task
version, run, lease and source records keep their existing values. Missing
or contradictory server evidence leaves the task pending.

If the worker lease has expired, the PM reads the actual recovery tuple and
uses the usual typed requeue with the current task version, claim generation,
live assignment IDs and running run IDs. This also permits an older service
to drain before an upgrade. Confirm the recorded server time is past expiry.
Save the PM command key, its new assignment ID and the worker’s checkpoint.
An expired lease cannot renew or submit.

If starting a queued recovery would discard an available original-worker
attestation, the work decision reports `retained_output_attestation_required`
on that assignment. When it is the only actionable case, the worker sees
`attention_required`. The assignment and complete context include
`routing_snapshot.retained_output_attestation` with the supported tool,
original run and generation, checkpoint, commit, tree and receipt IDs.
Other ready work remains selectable. A direct begin enforces the same check.

Before starting that fresh assignment, the original worker can attest its
retained artifact through `POST /api/agent/me/runs/{run_id}/attest-retained-output`
or `agent_attest_retained_planning_output`. Submit the original assignment
and fence through the authenticated worker transport, the planning and
recovery actors and command keys or the two receipt IDs in the hint, checkpoint ID, observed model, commit URL,
tree, PR URL, native final turn and `confirmed_final_output=true`. The
server requires the checkpoint to have been recorded on the live original
generation and the PM recovery to have occurred after expiry. It records
the worker's current statement separately from the historical interruption.
The subsequent submission and independent review include both actual runs
and the retained commit. If a worker cannot confirm its final output or the
checkpoint is incomplete, the unknown contributor remains visible to review.
The worker retrieves the old private fence from its own saved response to
the indicated begin or renew operation, matching its original assignment,
run and generation. It obtains the native final turn from its own retained
session and checkpoint. If either is unavailable or the worker cannot
confirm the output, it reports that fact to the primary PM. The PM may use
the normal queued-assignment update with `state=cancelled`, the current
actor queue revision, and an explicit reason. That action frees the worker
for other work and preserves the unresolved contributor on the affected task.

## Operational evidence

Routing events and aggregate metrics identify the policy revision, binding
revision, bounded reason codes, selected or excluded identifiers, and the model
comparison result. They exclude credentials, prompts, raw provider payloads,
private logs, and unbounded task text.

Use the authenticated agent capability endpoint to inspect:

- configured and effective rollout modes;
- whether the feature is advertised;
- rollout and topology-readiness blocker codes;
- the authoritative topology identity and revision, when available.

## Rollback

1. Set `MODEL_AWARE_ROUTING_MODE=off` on every application replica and restart
   them.
2. Confirm the capability handshake reports an effective mode of `off` and no
   longer advertises model-aware dispatch.
3. Return new work to supervised assignment. Already-queued model-aware
   assignments become blocked with `model_aware_assignment_inactive`; cancel or
   reconcile them before creating supervised replacements. Do not repeatedly
   retry begin while the feature is inactive.
4. Let already-accepted/running work continue through its existing fenced run,
   or use the normal failure/recovery controls when it cannot continue.
5. Preserve catalog revisions, assessments, previews, assignments, runs, model
   comparison evidence, events, and webhooks for audit.

Rollback is a control-plane change. It does not downgrade the database, delete
routing history, or rewrite prior assignment evidence.
