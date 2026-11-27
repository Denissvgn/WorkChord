# Verification, Rework, and Recovery

Use this reference to route resolved work to an independent reviewer, follow its verdict and rework handoff, recover stale execution, and publish durable project updates. The reviewer's own checks live in the `workchord-reviewer` skill; a PM agent never records Accept or Request changes.

## Contents

- [Route work to review](#route-work-to-review)
- [Handle model evidence and escalation](#handle-model-evidence-and-escalation)
- [Read the verdict](#read-the-verdict)
- [Close work with its delivery trace](#close-work-with-its-delivery-trace)
- [Return work for rework](#return-work-for-rework)
- [Reconcile the pull request and replace unattributable work](#reconcile-the-pull-request-and-replace-unattributable-work)
- [Supersede work another task already delivered](#supersede-work-another-task-already-delivered)
- [Record who executed work delivered outside recorded runs](#record-who-executed-work-delivered-outside-recorded-runs)
- [Follow a verification refusal's next step](#follow-a-verification-refusals-next-step)
- [Recover stale or inconsistent execution](#recover-stale-or-inconsistent-execution)
- [Triage discoveries](#triage-discoveries)
- [Publish project updates](#publish-project-updates)
- [Complete the phase contract](#complete-the-phase-contract)

## Route Work to Review

When the server advertises `scoped-review-evidence-v1`, a workspace operator can attest a source packet for the exact submitted commit, reviewer and model binding. For checked Git and test evidence, the operator also records each named offline test and its result digest. Keep `host-shell` in the worker requirements. For a source-only review, explicitly set `required_model.allow_source_only_review=true` in the immutable assessment. Give its ID to the independent operator as `expected_assessment_id`. Obtain the current routing assessment and the operator's receipt, then pass its `event_id` as `review_evidence_id` on the verification preview and assignment. Use the same explicit `review_binding_id` in supervised mode or the same preview-selected binding in enforced mode. A positive preview is required. Follow the ordinary capacity, model and publisher checks. If the packet expires or ownership changes, request a fresh receipt.

For an existing review, include `review_assignment_id` with `review_evidence_id` on the preview immediately before a SHA-pinned merge. Match the returned `review_evidence.assignment_id`, `assignment_state`, candidate and packet digests against the held review. This readback validates the existing owner before ranking capacity for new dispatches.

To move verification to a different verifier who already has every required tool natively, without a scoped receipt, do not use the model-aware assignment update. That update rebuilds the preview without any receipt and overwrites the row's earlier `review_selection`. Cancel the old assignment and create a fresh verification assignment instead; the prior evidence and the receipt event are kept:

1. Re-read the old assignment and the reviewer's queue. Confirm it is still `queued` and note its `expected_queue_revision`.
2. Cancel it with `PATCH /api/agent/assignments/{assignment_id}` (MCP `agent_update_assignment`) using `state` `cancelled`, the current `expected_queue_revision`, and a `reason`. Cancellation does not need a receipt.
3. Run a verification routing preview for the new verifier with `POST /api/agent/tasks/{task_id}/routing-preview` (MCP `agent_preview_task_routing`), `purpose` `verification`, the current `assessment_id`, the current `expected_task_version`, and the new `reviewer_profile_id`. Omit `review_evidence_id` and `review_assignment_id`. The new verifier must be an eligible candidate for the exact binding with no `model_tool_missing` or other exclusion.
4. Create the fresh assignment with `POST /api/agent/assignments` (MCP `agent_create_assignment`) using `purpose` `verification`, the new `actor_id`, the current `expected_task_version`, and the exact `review_binding_id` and `reviewer_profile_id` in supervised mode. Do not set `review_evidence_id`. In enforced mode, use the model-aware create body with the signed preview from step 3.
5. Re-read the new assignment and confirm its `review_selection` names the new verifier and the submitted candidate.

If the new verifier needs a scoped receipt to meet a tool requirement, it is not eligible for this route; request the receipt first.

1. Confirm the task is Implemented (`resolved`), no run remains active, and no worker still holds a live execution lease.
2. Choose a reviewer actor with the `verifier` role who did not do or report this work. Require a person or a separately scoped reviewer when independence cannot be established; the server refuses a non-independent verdict with `independent_review_required`.
3. Confirm the typed brief, criterion progress, artifacts, and delivery trace are current enough to review: the task carries its branch, commit, and pull-request links, or the submission states in `delivery_trace.none` why no repository changed. When `task.brief` exists, evidence from an older `brief_revision` or `artifact_revision` cannot support acceptance; return incomplete submissions to the worker through recovery instead of routing them to review.
4. Name the rework owner in the assignment reason when it should differ from the worker who submitted; otherwise the reviewer hands rework back to that worker.

Create a verification-purpose assignment only after the task is `resolved`, its
execution run is terminal, and its claim is released. Under
`model-aware-routing-v1`, request a fresh verification-purpose routing preview
against current independent actors and bindings. Resolution advances the task
version, so first read the current assessment and bounded history; create
exactly one assessment for the resolved task version when none is current,
preserving or strengthening the prior review floor and capability envelope
unless new authoritative evidence justifies another change. The verifier named
in the earlier assessment or execution preview was policy evidence, not
reserved capacity. Bind the resulting assignment to the exact verifier,
current task/run/assessment versions, selected binding, and fresh preview
digest. Rank verification work in the verifier's own queue by explicit review
rank and task priority; do not place it in an implementation queue or reserve
execution capacity while the task is still active.

## Handle Model Evidence and Escalation

When a project requires a different model publisher for review, dispatch a
verification actor whose profile and publisher allow it to review every
contributing implementation attempt. The server compares historical run
receipts, including interrupted or reworked executions. A supervised
verification assignment can select a specific eligible binding with
`review_binding_id`. The returned `review_selection` identifies the selected
reviewer, submitted candidate and contributors. Use the current task version
and the worker's own submission evidence.

When the server advertises `review-provenance-v1`, an eligible independent
reviewer can return a defective or unavailable candidate for rework.
`review_selection.acceptance_blockers` lists problems with accepting that
candidate. Both formal verdicts require an independently attributable
reviewer. Only a topology's primary controller acting as PM can use
`return_for_evidence: true` on released, resolved strict-project work. It
requires a previous fulfilled execution assignment with a successful,
claim-fenced run from the same team, the current ownership tuple and a
reason. This administrative action records zero verdicts. Cancel or finish
any outstanding verification assignment separately.

An owner performing manual work signs in, starts the task with
`start_manual`, writes current progress with at least one artifact link,
and submits with `resolve_manual` under the same human identity. Before
assigning a reviewer, check the manual execution and artifact receipt. The
server allows this route only when it can establish the human executor and
finds no agent execution assignments, runs or conflicting execution evidence.
The independent assigned agent still supplies its own observed model and a
known publisher. The human owner and workspace operator cannot give a formal
verdict on the strict project. When a resolved task cannot get a verified
agent verifier, do not ask anyone to switch `require_different_review_publisher`
off to close it: ask a signed-in workspace owner or operator to accept it as
owner (`POST /api/tasks/{task_id}/owner-acceptance` with a reason; in the web
interface, Work and review > Accept as owner). It is recorded as an owner
override in Review history, not as an independent review, and the policy stays
on. A person's ordinary Accept is refused with `verified_publisher_review_required`,
a `trusted_local` browser with no signed-in person cannot use the owner
acceptance, and an agent never does. An unverified owner name, a planned assignment
or an empty run list is insufficient. The administrative return command
requires a previous agent submission and cannot reopen human-only work.
Refresh existing verification previews after an upgrade.

Give the operator the affected task and run IDs and the named missing facts.
The operator can preview with
`POST /api/agent/model-catalog/execution-provenance/{run_id}/reconcile`
or `agent_reconcile_run_provenance(run_id)`. A retained acknowledgement can
be supplied for comparison with the original server digest. An apply request
uses `apply=true` and `expected_evidence_digest` from that preview. REST
also requires the `Idempotency-Key`, `X-Agent-Rationale` and
`X-Correlation-ID` headers. The MCP operator supplies `idempotency_key`,
`rationale` and `correlation_id`. Retain the returned source receipts and
operator event ID. A missing terminal model requires an authenticated final
checkpoint from the same execution fence. Older records with missing model
publisher evidence remain unresolved. Reconciliation preserves the run's
original model trust state.

For interrupted work, take the exact version, claim generation, live assignment
IDs and running run IDs from the recovery queue. The primary controller can
requeue an eligible worker on its own team. Outside enforced routing the
requeue issues a supervised recovery that can immediately offer
`start_assigned`. In shadow mode it may instead be refused with
`recovery_supervision_unavailable`; its `condition` says why
(`primary_pm_required`, `model_aware_history`, `reviewer_profile_ambiguous`,
`reviewer_profile_not_independent`) and nothing changed. Resolve that condition
or recover once routing is enforced. Under enforced routing, complete the
governed selection on the existing assignment when it reports
`routing_selection_pending`. Preserve any independent verification ownership.

Use `agent_get_execution_usage_summary` or `/api/tasks/execution-usage` for an
authorized project/iteration and stated observation window. Compare reports
with accepted task identities, rejection/reopen events and review/recovery
coverage. Unreported attempts and unknown costs remain visible; a succeeded
run is not an accepted outcome. Simulated reports have separate totals.
Worker-reported provider costs and immutable price-based estimates stay
separate, with no implicit currency conversion or live repricing. Optional
budgets are advisory comparisons for covered reports and do not authorize or
block execution. Independently reconcile actual provider receipts before
claiming measured delivery economics or pilot acceptance.

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

## Read the Verdict

The reviewer records Accept (`pass`) or Request changes (`reject`) through the typed verdict operation. Accept atomically performs the server-owned `resolved -> closed` transition. Request changes atomically reopens the task and creates ordered rework for the named worker. After either verdict, re-read the task, review and rework assignments, pipeline, milestone/project progress, and timeline.

In supervised v0, let the accountable person transition `resolved -> closed` with the current task version and reason after reviewing the evidence. Re-read the response because closure sets actual end data and can roll up parents.

Do not close partially accepted work. Split follow-up work only when the original criterion can be truthfully accepted without it; otherwise the reviewer requests changes on the current task.

## Close Work With Its Delivery Trace

Every finished task leads to the code it produced. Before you report a task as
Accepted, close it in supervised v0, or count it toward a milestone, release, or
project update, read the task's external links
(`workspace_list_external_links` with `entity_type` `task`) and require one of:

- at least one GitHub `commit` or `pull_request` link, or, on a server without
  `work-delivery-links-v1` or outside GitHub, the same URLs in the run's
  artifact links; or
- a stated reason in the submission's `delivery_trace.none` why no commit or
  pull request exists, such as a docs-only change kept outside version control,
  an analysis, or a recorded no-change decision.

When neither is present, the task is not finished. For work still to be
reviewed or in rework, ask the reviewer to request changes or the worker to
record the trace at the next submit. For work already Accepted, find the
commit or pull request in the repository by its `WC-<task-id>` key (the
`WorkChord-Task: WC-<task-id>` commit trailer or the `wc-<task-id>` branch name)
and link it with `workspace_create_task_github_link`; when you cannot find it,
report the gap in the project update instead of inventing a link. Add a link
yourself only while no execution run is active on the task: a link changes the
task version, and the worker's submit then fails as a scope change.

When a release ships, link the release to the code it shipped: its merge pull
request or its release tag
(`https://github.com/<owner>/<repo>/releases/tag/<tag>`), through
`workspace_create_release_github_link`. Re-read it with
`workspace_list_external_links` (`entity_type` `release`) and name the link in
the release's project update. A release without either link is not reported as
shipped.

## Return Work for Rework

In assigned-work v1:

1. The reviewer's Request changes verdict names the rework actor, rank,
   evidence, reason, and current task/review versions.
2. That transaction transitions `resolved -> active`, fulfills the
   verification assignment, and creates an ordered execution assignment with
   `queue_class=rework`; there is no separate client-side send-to-rework call in
   stable v1.
3. Check the returned actor, queue rank, and rejection evidence. To change the
   owner or rank, or to add a not-before condition the verdict schema does not
   carry, update the queued rework assignment with its current queue revision
   as a separate idempotent PM action.
4. Confirm that no old execution claim or run remains current.
5. Re-read the worker queue and require the server to surface the item as rework, not normal planned work.

For model-aware rework, require the rejection transaction or follow-up routing
flow to preserve the prior assessment, assignment, run, routing snapshot, and
failure reason as lineage. Read the immutable assessment history and create the
one current assessment required by the reopened task version before generating
a fresh execution preview and selecting the rework actor/binding. Preserve the
prior review floor. Change the required model envelope only through that new
current assessment backed by evidence; never copy an empty routing snapshot or
silently reuse the prior candidate list.

In supervised v0:

1. Append the rejection evidence before status change.
2. Let the accountable PM or human transition `resolved -> active` with the current task version and reason.
3. Hand the explicit task ID to one unique worker under supervision.
4. Start a new run without repeating the cosmetic `planned -> active` transition.
5. Track the manual rework owner because the current global ready list contains only planned tasks.

Never leave rejected active work without an explicit next owner. Never reset it to `planned` merely to make it appear in the ready list.

## Reconcile the Pull Request and Replace Unattributable Work

### Read the GitHub reconciliation

`GET /api/tasks/{task_id}/github-reconciliation` compares what each run submitted with what GitHub last showed for the task's linked pull requests. It is a read-through view of stored observations. Each pull request entry carries `state` (`open`, `draft`, `merged`, `closed_unmerged`, `unobserved`), the submitted and observed head SHA, `target_branch`, `checks`, `merged`, `merge_commit_sha`, `observed_at`, `review`, `differences`, `next_owner` and `next_action`. Differences include `never_observed`, `observation_failed`, `head_differs_from_submission`, `checks_not_observed_for_head`, `merged_without_acceptance`, `closed_without_merge` and `task_replaced`. `next_owner` is `pm`, `worker`, `reviewer` or `none`.

The PM agent reads this view with `agent_get_github_reconciliation` and runs `agent_run_github_catch_up` (`POST /api/tasks/{task_id}/github-reconciliation/catch-up`), which reads the task's own pull requests from GitHub for events a deployment never received, then returns the same view. A person can run the same from the task page (**Run catch-up**, with edit access). Use it when an entry is `unobserved` or its checks are not observed for the current head. One catch-up reads every linked pull request first and records all links in one version bump; a provider error is cached per link and the call still succeeds. Acceptance is kept across an observed merge when the observed head equals the latest submitted commit; a head pushed after acceptance, or a missing head, makes it stale.

A merge never accepts or closes a task. A pull request merged outside WorkChord keeps its task unaccepted (`merged_without_acceptance`), and the independent verdict on the submitted commit is still required. If the head differs from the submitted commit, have the worker submit the current head before review.

### Replace unattributable work

When a task's runs lack the model attribution the review policy needs, the task can never be accepted. The project's PM actor, a project manager or a workspace operator records a clean replacement: create the replacement as an ordinary planned task in the same project (and milestone), then send `agent_record_task_replacement` (`POST /api/agent/planning/tasks/{original_id}/replacement`, or `POST /api/tasks/{original_id}/replacement` for a person) with `replacement_task_id`, `expected_original_version`, `expected_replacement_version`, `reason`, `owner_decision`, `base_commit_url` and `carried_run_ids`. `agent_get_task_replacement` (`GET /api/agent/planning/tasks/{task_id}/replacement`) reads the disposition for either task.

The original must be unaccepted leaf work with no live execution. The command keeps the original with its attempts, withdraws it from delivery counts, and moves schedule and delivery dependents and open release membership to the replacement. Only the replacement can be accepted, and it is reviewed on its own runs plus every carried run. Carrying a run with no attribution keeps the replacement held (`replacement_contribution_unattributed`). Never reopen or review the original.

## Supersede Work Another Task Already Delivered

When another task already delivered the work and is closed or accepted, do not reopen and close the original. Record `POST /api/tasks/{original_id}/supersession` with `{successor_task_id, expected_original_version, expected_successor_version, reason}`; only a project owner or manager, an operator or the project's PM agent decides, and there is no MCP tool for it. The original is withdrawn with its history, a postponed original's postponement is closed, and its dependents, delivery prerequisites, open reactivation requirements and release membership move to the successor, so the deliverable counts once. The successor cannot then be canceled. Task responses show the outcome as `displayed_state: superseded` with `successor_task_id`. Use a replacement (above) instead when the original's work is being redone.

## Record Who Executed Work Delivered Outside Recorded Runs

When resolved work was delivered outside recorded runs, the verifier cannot be selected until its executor is on record. Call `agent_record_manual_provenance` (`POST /api/agent/planning/tasks/{task_id}/manual-provenance`, `planning:write`, planning command headers) with `{expected_version, artifact_revision, executor: {kind: agent, actor_id, model_binding_id?}, head_commit_url, commit_urls, pr_url | base_commit_url, reason}`. Link the pull request to the task first, and list every commit of the pull request in `commit_urls`. You count as a contributor of the work, so the verifier must use a different publisher from yours. A human executor can only be recorded by a signed-in person; ask the owner. The task stays resolved and its version advances, so create the verification assignment again with the new task version. Never cancel and recreate assignments in a loop.

## Follow a Verification Refusal's Next Step

A verification refusal carries `next_step` (`kind`, `authority`, `message`, `commands`, `ui_action`). Follow it instead of retrying.

| Refusal | What to do |
| --- | --- |
| `verification_publisher_unverifiable` | At assignment time with no recorded runs: an owner, operator, project manager or the PM agent records manual provenance. With no recorded model publisher on a run: an owner or operator accepts as owner, or the work is redone. At verdict time: refresh the review assignment; the verifier submits with its own observed model, which must match the selected binding. |
| `verification_candidate_unverifiable` | `manual_provenance` in `missing`: the work was resolved outside recorded runs; ask the owner who executed it and which pull request and commits carry it, record manual provenance, then create the verification assignment again. `current_human_artifact` only: ask the executor to link exactly one pull request to the task or resubmit the artifact with a pull request or compare URL. `submitted_candidate` only: the task's runs have no exact submitted candidate; route it to rework or a clean replacement. At verdict time: retry when GitHub is reachable. |
| `verification_independence_unverifiable` | The assigned reviewer submits its own verdict with its own observed model. A replacement history that is too long or cyclic, or a run with no recorded profile, is for an owner decision or a replacement, not a provenance record. |
| `verification_contributors_unverifiable` | Every candidate commit must be attributed to the executor and carry no Co-authored-by trailer; resubmit with a pull request that holds only such commits, or retry when GitHub is reachable. |
| `verified_publisher_review_required` | Assign an agent verifier (record provenance first for work with no recorded runs), or ask a signed-in owner or operator to accept as owner with a reason. |
| `accountable_review_required` | Repeat with `X-Review-Override: true` and a written reason in `X-Command-Reason`, or have a person review. |
| `independent_review_required` | Another reviewer, one who did not execute or submit the work, reviews it; an agent reviewer needs the verifier role. |
| `manual_provenance_candidate_unverifiable` | Read `attribution_gap`. For `commit_attribution`, add `offending_sha` to `commit_urls`. For `coauthor_trailer`, the work cannot be attested; tell the owner. For `head_mismatch`, use the pull request's current head. |
| `manual_provenance_pr_not_task_evidence` | Link the pull request to the task first. |
| `manual_provenance_execution_recorded`, `manual_provenance_executor_conflict` | The task's runs or executing person already supply provenance; use execution reconciliation or a clean replacement. |
| `manual_provenance_human_recorder_required` | Ask a signed-in owner or project manager. |
| `manual_provenance_recorder_unattributable`, `manual_provenance_executor_unattributable` | The binding needs a catalog entry with a publisher; ask the operator. |
| `verification_actor_not_independent`, `verification_profile_not_independent`, `verification_publisher_not_independent`, `verification_specialist_skill_missing`, `reviewer_profile_*` | Assign a verifier that did not contribute and whose profile, publisher and skills fit. |

### Team presence

`agent_team_actor_outside_topology`, `verifier_outside_topology`, `verifier_not_runtime_ready`, `caller_not_runtime_ready`, `caller_not_bound_to_topology` and `model_aware_routing_preview_unavailable` are readiness refusals. Read `non_ready_actors`, `readiness_rule` and `topology_readiness` in the refusal, and `agent_get_team_setup_status`. Have each listed actor with `blocks_this_request: true` fix what its `blocker_codes` name (acknowledge its current handoff, restore its binding) and poll its queue, because an actor is present only within `maximum_runtime_staleness_seconds` of its last poll; then retry. For a verification assignment only the verifier, and a caller that is itself not ready, need to be ready. When model-aware routing is switched off for the deployment, the operator must set `MODEL_AWARE_ROUTING_MODE` to `shadow` or `enforced` and restart.

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
| Active task with no live claim and no running run | Mark recovery-required; choose resume or reassign through an audited action, or postpone it when it must stop but may resume (`agent_postpone_task`); cancel only work that will never be done. Do not silently edit it to planned. |
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
routing snapshot, run model evidence, and recovery cause. Read the immutable
assessment history, create the one current assessment required by the recovered
task version while preserving the prior review floor, and require a fresh
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

Recovery and assignment writes also require a deterministic idempotency
key, rationale, and correlation ID. Preserve the same three values only for an
exact retry; changing rationale or correlation creates a different audited
request and must not replay the prior command.

A worker's claim-fenced `agent.blocker` task event marks the task Blocked, with its reason and the worker's name in Activity; people see it in My Work → Blocked and the project's blocked count. Decide the response (clarify, fix the dependency, recover, or reassign), then remove the block with Remove block once the cause is resolved. When your deployment offers no agent operation for Remove block, ask a person to do it. Never mark work blocked with a label.

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

Keep the records Projects, Roadmap view reads in step with the update:

- Set project `status` to `active` when its first task starts, and to `completed` when its outcome is Accepted. A project that still reads `planned` while tasks are Active or Implemented misleads everyone who opens Projects, Roadmap view.
- Set a milestone to `active` when its first task starts and to `completed` when its last task is Accepted.
- Leave `health` at `unknown` only until the first update.
- Change a committed project or milestone target date only with the owner's recorded approval. Report a calculated end that passes the target as a risk instead.

In stable v1, use `POST /api/agent/projects/{project_id}/updates` or
`agent_create_project_update` with `reports:write`, evidence checked,
required rationale and correlation, and a deterministic idempotency key.
REST sends the audit fields in `X-Agent-Rationale` and `X-Correlation-ID`; MCP
uses the named `rationale` and `correlation_id` arguments. Confirm
`created_by_actor_id`, then re-read the update list and project health. If the
live deployment lacks that authorized mutation, return the structured draft to
the human owner and state clearly that no durable update was written.

## Complete the Phase Contract

### Phase 8: Route review, report, and learn

**Preconditions**

- Require a resolved task for normal verification.
- Require a terminal execution run, released claim, submitted artifacts, a delivery trace (commit or pull-request links, or a stated reason why none exists), current versions, and an independent reviewer.

**Required reads**

- Read task/brief, timeline, assignment, claim, run, artifacts, source links,
  project summary, milestone/release state, latest project update, and discovery
  Triage. For model-aware work, also read assessment, routing snapshot, selected
  binding, observed model, trust state, and a fresh verification preview.

**Allowed mutations**

- Create the verification assignment for an independent reviewer, preserving
  model-routing lineage and independent/specialist requirements.
- Adjust the owner, rank, or not-before time of the rework assignment the
  reviewer's verdict created.
- Create linked Triage, perform audited recovery, and append a project update within granted authority.

**Exit and postcondition checks**

- Re-read task status/version, review and execution assignments, routing
  snapshots/model evidence, pipeline, milestone/project progress, project update
  freshness, and new rework/recovery ownership.
- Leave every rejected or recovered task with one explicit next owner.
- Leave every Accepted task with a commit or pull-request link or a stated
  reason why none exists, and every shipped release with its merge pull-request
  or tag link.

**Evidence and stop rules**

- Record the reviewer, verdict, status transition, project impact, and next owner.
- Stop when independence is missing, model trust is mismatch, unreported, or
  unverifiable without accepted supervised handling, evidence conflicts, a run
  remains active, current versions are stale, durable rework/recovery is
  unavailable for unattended work, or the project-update write is unauthorized.
