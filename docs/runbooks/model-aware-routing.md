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

## Candidate-bound review evidence

On a project requiring an independent publisher, an authenticated workspace operator may deliver an immutable review packet to a specific verifier. The issuer must be independent of the candidate’s contributors and verifier, including their linked profiles. Named offline test results can satisfy the assessment’s `host-shell` requirement for verification. Source alone qualifies only when the PM explicitly sets `required_model.allow_source_only_review=true` in the assessment for this task version. A worker still needs its own execution tools. This mechanism executes no commands and changes no model binding.

1. Capture the reviewed Git commit and the SHA-256 of the exact packet. For `source_and_tests`, include each named offline test and the SHA-256 of its result. For `source_only`, omit the test list. Distribute the packet through the team's approved channel.
2. Use `POST /api/agent/tasks/{task_id}/review-evidence` or MCP `agent_attest_review_evidence` with `action=issue`, `expected_assessment_id`, the expected task, brief and artifact revisions, `commit_sha`, `reviewer_actor_id`, `binding_id`, `expected_binding_revision`, `method`, `packet_sha256` and an offset-aware `expires_at` within the next 24 hours. Each test entry has `name` and `result_sha256`. Supply the normal idempotency key, rationale and correlation ID.
3. Use the returned `event_id` as `review_evidence_id` on the verification preview and assignment. In supervised mode, provide the exact `review_binding_id`. In enforced mode, select the same binding using the current signed preview. Other model, data-policy, capacity and independence requirements still apply.
4. The reviewer checks the received packet and passes its digest as `reviewed_packet_sha256` with the normal observed model and reviewed candidate digest. The server rechecks the operator receipt, candidate, expiry and verifier identity when it records the verdict.

Before merging an externally hosted pull request, the PM can use the same verification preview with both `review_evidence_id` and `review_assignment_id`. Compare `review_evidence.assignment_id`, `assignment_state`, actor, binding, candidate and packet digests with the current assignment. A valid existing owner can hold a current receipt even when the fresh-dispatch candidate list is empty. An expired, revoked or mismatched receipt yields `verification_evidence_unavailable`. Check the external head independently and pin the merge to that SHA. The preview applies to its read instant.

An operator can revoke an issued receipt through the same command with `action=revoke` and `evidence_id`. Changing the candidate, task revisions or reviewer binding requires fresh evidence. A revoked, expired or retired issuer cannot support either verdict. The PM can reorder or cancel the queued assignment and select a fresh receipt. An assessment is immutable and unique for its task version and policy. If an existing assessment requires tests, supply the named results or use a genuine versioned planning change and fresh assessment before offering source alone. A completed verdict and its audit record remain historical. A later rework submission requires a new candidate-bound decision. Clients can discover this protocol through `scoped-review-evidence-v1`.

## Reassigning receipt-backed verification

A review receipt is bound to one verifier actor, one model binding and its
revision, one candidate commit, one packet digest and one expiry. The server
rechecks those facts when the receipt is consumed, so a receipt cannot be used
by a different verifier or binding. Changing only `reviewer_profile_id` keeps
the receipt, and the server refuses that change with `reviewer_profile_mismatch`.

On a supervised update (`AgentTaskAssignmentUpdate`), changing `actor_id` or
`review_binding_id` to another verifier or binding without a fresh
`review_evidence_id` is refused with `verification_evidence_unavailable`. The
model-aware update (`ModelAwareAgentTaskAssignmentUpdate`) does not apply that
guard. It rebuilds the signed preview without the receipt, so only a verifier
that is natively capable can be selected. It also overwrites the row's earlier
`review_selection`. The operator's receipt event survives, but the assignment
no longer shows the earlier evidence. Do not use the model-aware update for
this change. Use cancel-and-recreate, which keeps the old assignment's
`review_selection` intact.

When the new verifier already has every required tool natively, without a
scoped receipt, the supported route is to cancel the old assignment and create
a fresh verification assignment with no receipt:

1. Re-read the old assignment and the reviewer's queue. Confirm that it is still
   `queued` and note its `expected_queue_revision`.
2. Cancel it with `PATCH /api/agent/assignments/{assignment_id}` (MCP
   `agent_update_assignment`) using `state` `cancelled`, the current
   `expected_queue_revision`, and a `reason`. The cancellation skips the review
   evidence checks, so it does not need a receipt.
3. Run the verification preview for the new verifier with
   `POST /api/agent/tasks/{task_id}/routing-preview` (MCP
   `agent_preview_task_routing`) using `purpose` `verification`, the current
   `assessment_id`, the current `expected_task_version`, and the optional
   `reviewer_profile_id`. Omit `review_evidence_id` and `review_assignment_id`.
   In supervised mode the server does not rerun this preview when the assignment
   is created without a receipt. The PM must read the result and act on it
   before step 4. The new verifier must appear as an eligible candidate for the
   exact binding, with no `model_tool_missing` or other exclusion for it. Its
   own tool tags must satisfy the assessment's required tool tags. For a scoped
   review, the receipt is what relaxes the `host-shell` requirement, so a
   verifier that needs a receipt to meet it is not eligible for this route.
4. Create the fresh assignment with `POST /api/agent/assignments` (MCP
   `agent_create_assignment`) using `purpose` `verification`, the new `actor_id`,
   the current `expected_task_version`, and, in supervised mode, the exact
   `review_binding_id` and `reviewer_profile_id`. Do not set
   `review_evidence_id`. In enforced mode, use the model-aware create body with
   the `assessment_id`, `model_binding_id`, `model_binding_revision`, and the
   signed `routing_preview_id` and `routing_preview_digest` from the preview in
   step 3. The server verifies that preview on the enforced-mode create. Supply
   the normal `Idempotency-Key`, `X-Agent-Rationale` and `X-Correlation-ID`
   headers, or the MCP `idempotency_key`, `rationale` and `correlation_id`
   arguments.
5. Re-read the new assignment. Its `review_selection` should carry the new
   reviewer and candidate, and no `review_evidence` key.

Checks enforced by the server on every verification create, supervised or
enforced, when the project requires an independent publisher:

- the verifier's publisher differs from every contributing publisher, and the
  candidate history is known;
- the verifier is not an implementation actor, its profile did not contribute to
  the task, and any manual-execution profile rule still holds;
- a requested `reviewer_profile_id` matches the verifier's profile.

Checks that the server enforces only on the enforced-mode create, using the
signed preview: the routing policy, binding revision, model envelope, capacity
and schedule. In supervised mode these are a manual check in step 3, and the
PM must act on the preview result.

Verdict-time checks apply later to the new assignment: the observed model must
match the new binding, and a `pass` verdict requires the reviewed candidate
digest to match the current candidate. A reject or other non-pass verdict does
not need that digest.

Nothing from the earlier assignment is erased. The cancelled row, its
`review_selection` and the receipt's operator event remain in the task history,
and cancelling does not revoke the receipt. Use `action=revoke` only when the
packet itself must be withdrawn. A receipt never moves to the new verifier, so
it cannot be used in the fresh assignment. Any completed verdict and its audit
record stay historical. If the candidate, task revisions or binding change
later, issue a fresh receipt before any scoped review.

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

## Preferring a free or local model

A catalog entry has a `local_first` setting, off by default, which an operator
sets when creating or updating the entry through the API or the model catalog
form in Settings. Existing entries upgrade with it off and rank exactly as
before, so the cost tier keeps its meaning for hosted models.

Routing applies the setting only after every hard gate has passed. Among
candidates of equal adequacy, a local-first entry ranks ahead of the others
even when a hosted entry has a lower cost tier; the remaining order is then
cost, queue depth, schedule delay, latency, actor, and binding. It never lifts
a candidate over a capability, schedule or data-policy blocker, and it never
outranks a candidate with better adequacy. The routing preview marks the
candidate as local-first and states in its rationale that the preference
applied. Changing the setting revises the catalog entry, so live assignments
that depend on it follow the usual reconciliation.

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
After a failed or canceled rework, the PM uses the normal recovery path,
described in the next section. A rework that began as a supervised handback
does not count as earlier model-aware routing for that recovery.
A previously begun rework cannot be reused to start a second fenced run.
Enforced mode continues to require a fresh model-aware selection.

## Recovery requeue by mode

A typed recovery requeue always records the pending model lineage, including
the earlier review floor. Whether its new assignment can begin depends on the
effective mode for the recovery actor. A configured `shadow` or `enforced`
mode counts as `off` while the actor has no ready team topology:

| Effective mode | Result |
| --- | --- |
| `off` | The recovery is supervised and the actor can begin it at once. |
| `shadow` | The recovery is supervised when the team's primary PM issues it, no earlier assignment carries model-aware routing (a rework that began as a supervised handback does not count), and at most one reviewer profile is recorded and it is not the recovery actor's. Otherwise the requeue is refused and nothing changes. |
| `enforced` | The recovery waits with `routing_selection_pending` until a model-aware assignment update completes a fresh selection. |

A supervised recovery takes the single recorded reviewer profile when there is
exactly one and it is not the recovery actor's. If enforcement becomes active
before the actor begins, the recovery waits for a fresh selection.

A refused requeue returns `recovery_supervision_unavailable` with a
`condition`:

- `primary_pm_required`: only the team's primary PM can issue it.
- `model_aware_history`: earlier assignments, listed in
  `model_aware_assignment_ids`, need a fresh model-aware selection. Recover
  the task once routing is enforced, or use the supervised path below.
- `reviewer_profile_ambiguous`: earlier assignments name several reviewer
  profiles, listed in `reviewer_profile_ids`. Use the supervised path below
  and name the reviewer profile.
- `reviewer_profile_not_independent`: the recovery actor's profile is the
  recorded reviewer profile. Choose another recovery actor.

For `model_aware_history` and `reviewer_profile_ambiguous` in shadow mode, the
PM can instead make the decision explicitly. Cancel any queued stale execution
assignment with an assignment update. Then create a supervised assignment with
`purpose` `execution` and `queue_class` `recovery`, the chosen actor and an
explicit `reviewer_profile_id` through assignment create, which shadow mode
permits. Supervised assignment create does not carry the model-aware lineage,
so record the reason for the choice in its rationale.

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

While the extension's window is open, the worker can keep reporting on its
original run. Progress and checkpoint events leave the window in force. The
next renewal or submission moves the assignment to the current task version,
and the window is then no longer needed. A failure with retained output ends
the run and the window, and the task enters the PM's recovery list. A worker
blocker changes the task state the window recorded. The task shows as
blocked; the worker can no longer renew, submit or fail that run, and the PM
resolves the blocker and recovers the work.

A runtime may re-acknowledge during a window only to adopt
`iteration-window-execution-recovery-v1`. Existing work continues when that
feature is the only difference from the acknowledgement in force when the
window opened. Any other acknowledgement change, topology revision, model
binding, membership or review policy change ends the window's authority.
Renew, submit and fail then report that the fence `no longer matches current
ownership`. The task appears in the PM's recovery list, and the PM uses the
typed recovery path below.

Downgrading the database below schema revision `20261121_0019`, or restoring
a backup taken before it, removes every stored window. Assignments that relied
on a window no longer match their task version, so their workers cannot renew,
submit or fail. Let that work finish before rolling back where possible.
Otherwise the PM recovers each affected task with the typed requeue once its
lease expires. On SQLite, this downgrade needs SQLite 3.35 or later.

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

## Diagnosing a named actor in a bounded preview

A preview returns at most 25 eligible candidates and 50 exclusions within a
32,768-byte packet, and reports the rest in `eligible_candidates_omitted` and
`exclusions_omitted`. When a team has more rows than that, a named worker or
reviewer can be among the omitted rows. Add `focus_actor_id`, and optionally
`focus_model_binding_id`, to the same execution or verification preview
request on `POST /api/agent/tasks/{task_id}/routing-preview` or MCP
`agent_preview_task_routing`. The response then keeps that actor's rows (one
binding's row, or all of the actor's rows) in their ranked or sorted place,
with the same hard blocker codes, and trims other rows first. The omission
counts still cover every row left out, and the preview digest covers the
response as returned.

A focus changes no eligibility. A team-bound caller sees only its own team's
actors, so a focus on any other actor is ignored and the response equals the
unfocused one. A preview focused on the actor being selected, alone or with
the selected binding, can be used for that assignment; the server recomputes
it at selection time.

## Packet size and the preview digest

The 32,768-byte limit applies to the canonical serialized preview response
after the server fills in model defaults and the digest fields. It is not a
limit on the raw HTTP body or on MCP framing: JSON-RPC envelopes, MCP text
wrapping, and HTTP headers are outside it. A client that measures bytes should
measure the response body it receives, and should not expect that number to
equal the canonical size.

The server computes `preview_digest` over a projection of the response that
uses UTC `+00:00` timestamps and omits the model defaults of the top-level
response fields; nested candidate and exclusion rows keep their defaults. The
body a client receives uses the schema's own datetime format and includes all
defaults, so the digest cannot be recomputed from the body. Clients must send
back the `preview_digest` and `preview_id` exactly as the server returned them
when creating or updating an assignment. Only the server can re-derive the
digest, and it does so when it recomputes the preview at selection time.

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
