# Claim, Run, And Task State

Use this reference for lifecycle mutations. Once work is selected, keep the
procedure low-freedom.

## Keep State Independent

Report the model identifier your runtime actually observed when beginning
assigned work. The supervised request uses `model`. Enforced routing uses
`resolved_model_id` and the selected binding revision. The begin response's
`execution_provenance` records the profile and model publisher the server
could establish at that time. An ambiguous or missing observation leaves the
publisher unresolved. The original run trust state is retained.

On a project requiring different publishers for review, include the actual
final `observed_model` in the submit payload. Report a runtime model change
through the interrupted-work command with the final observed model and
evidence of the work retained. This preserves both contributing publishers
for the next review.

With `review-provenance-v1`, strict projects require `observed_model`
on failures as well as submissions. If the execution has stopped, you can
seal its final observation on a fenced renewal using
`interruption_checkpoint`. Supply the model actually observed,
`output_state` of `no_output` or `retained`, and any retained
`commit_urls`. Keep the receipt. Further submissions on that sealed fence
are refused. PM recovery uses the original authenticated receipt. When the
process stops before recording one, any retained contribution remains
unknown. Report `no_output` only after verifying that this execution
produced no candidate artifacts.

For a PR, submit every commit your run contributed in `commit_urls` and the
immutable head in `commit_url`. For a commit-only delivery, also submit the
immutable `base_commit_url` delimiting your reviewed range. For a document
or dashboard, submit the artifact link with the version or artifact evidence
the reviewer needs to identify what they inspected.

On strict projects, any `Co-authored-by:` trailer on a submitted commit
holds formal acceptance. The server records the offending SHA. Preserve
legitimate credit and the original history when reporting that hold.
Keep the contributor evidence for an ownership-preserving review, or agree
on a genuinely independent implementation with a new candidate. A shared
Git account or editing an existing credit cannot establish who produced the
candidate. Other projects retain their configured review policy.

For code, submit the immutable candidate in `commit_url` and its PR in
`pr_url` when available. Keep evidence of retained work from earlier
attempts. A recovered supervised assignment can return `start_assigned`
in shadow mode. Begin that assignment with its exact queue revision.
For `agent.blocker`, provide the live claim ID and generation. The event
preserves the task version. The authorized PM or person clears the blocker.

- Assignment answers who was dispatched and in what queue position.
- Claim/fence answers who may write now.
- Run answers which execution attempt produced events and artifacts.
- Task status answers where work is in the business lifecycle.

Never treat one as proof of the others. Refresh the full tuple after every
mutation.

A task can also be `postponed`: the PM agent or an operator stopped it, with a
reason and the requirements that must be met before it resumes. Postponing
cancels the live assignments of every purpose, ends the running runs, and
releases the claim with a new claim generation. Treat it like a lost fence:
stop task-bound writes, refetch your work, and do not claim or begin the task
again. The task returns to `planned` (or `resolved`) by itself when its
requirements are met, and its assignment is issued again by the PM. Do not
reactivate it, and do not record an owner decision; a worker cannot.
Changing only a task's milestone does not stale an issued assignment, so keep
working.

## Use Atomic V1 Actions

### Begin

Supply the server-advertised atomic begin action with:

- assignment ID for the selected execution-purpose assignment;
- queue revision from the work decision;
- one deterministic idempotency key for this begin attempt;
- requested lease within advertised limits;
- trace/correlation data and run metadata that contain no secrets;
- the task's branch URL as `branch_url`, as described in
  [Record Where The Code Went](#record-where-the-code-went).

### Record The Harness Session

When the runtime that runs you gives you its own session or conversation
identifier (through its launcher, a hook, or the runtime handoff), send it once
in begin as run metadata:

```json
{"metadata": {"harness": {"kind": "claude-code", "session_id": "<the identifier the runtime gave you>"}}}
```

Use a short lowercase runtime name for `kind`. Keep `trace_id` as your
external run ID: one harness session can serve several assignments, and the
idempotency keys below need an ID per execution attempt. Never guess, derive, or
invent a session identifier, never send a file path or transcript location, and
omit `harness` when the runtime does not give you an identifier. If a resumed
session reports a different identifier, add the same `harness` object to the
payload of your next checkpoint event. The value is your declaration so an
independent observer can match your run to its session; WorkChord does not
verify it.

### Record Where The Code Went

Keep the trace from a task to its code in WorkChord, so a person can open the
task and find its branch, commits, and pull request, and can start from a commit
or pull request and find the task. The trace key is the WorkChord task ID,
written `WC-<task-id>`; people see the same task as "Task #<task-id>".

1. **Name the branch with the key** before begin: `wc-<task-id>-<short-slug>`,
   lowercase, under the repository's own branch prefix when it has one (for
   example `feature/wc-42-export-csv`).
2. **Record the branch at begin.** When the live capability response
   advertises `work-delivery-links-v1` and the repository is on GitHub, send the
   branch URL as `branch_url` in begin:
   `https://github.com/<owner>/<repo>/tree/<branch>`. WorkChord links it to the
   task; the begin response returns it in `task.external_links`.
3. **Put the key in commit and pull-request text.** End every commit message
   with the trailer `WorkChord-Task: WC-<task-id>`, and name `WC-<task-id>` in
   the pull request's title or first line, with a link to the task when the
   workspace has a URL people can open. Follow the repository's own rules for
   everything else. When those rules forbid task references in commit or
   pull-request text, leave the text out, keep the links below, and say so in
   the submit evidence.
4. **Record the commits and the pull request at submit.** Push the branch
   first. With `work-delivery-links-v1`, send `branch_url` again, `commit_urls`
   with one URL per commit the task produced
   (`https://github.com/<owner>/<repo>/commit/<full-sha>`, the full 40- or
   64-character SHA from `git log --format=%H <base>..HEAD`), and `pr_url` when a
   pull request exists. WorkChord links each one to the task and skips a link
   the task already has, so resending the branch or an earlier commit is safe.
5. **Repeat the trace in the evidence.** Add a `delivery_trace` object to the
   submit `evidence`: `branch`, `commits` (full SHAs), and `pull_request`
   (URL or `null`), so a reviewer reads the trace next to the
   acceptance-criterion evidence.
6. **Without the feature or outside GitHub**, send no `branch_url` or
   `commit_urls`: an older server refuses unknown fields. Put the branch,
   commit, and pull-request URLs in `artifact_links`, the pull request in
   `pr_url`, and the same values in `delivery_trace`.
7. **When the task changes no repository** (an analysis, a decision, a review,
   or content kept outside version control), record no links and give the
   reason as `delivery_trace: {"none": "<why no commit or pull request exists>"}`.
   Never invent a commit or pull request to fill the trace.

For rework, keep the same branch when the repository allows it, and send the new
commits at the next submit; the links from earlier attempts stay on the task.

Before the call, compare the task/version returned in complete context with the
assignment's bound task/version. Atomic begin does not accept a caller-supplied
task ID or `expected_task_version`; it locks the assigned task and revalidates
that binding on the server.

When `model-aware-routing-v1` applies, also compare the assignment and context
assessment/policy versions, selected model-binding ID/revision, configured
alias, and required capability envelope. Supply the exact selected binding
ID/revision and the runtime's observed resolved-model identifier through the
live begin contract. The observed identifier is execution evidence, not a model
request and not attestation.

Do not call begin when the assigned binding is missing, disabled, stale,
unavailable to the runtime, or inconsistent with the observed model. Do not
substitute a default, cheaper, newer, or locally preferred model. Return the
typed mismatch/attention evidence and request PM/operator action; workers cannot
change model bindings, task requirements, or assignments.

Accept only a response that returns a consistent accepted assignment, task and
new version, claim ID/generation or fence, expiry, and running run. For
model-aware work, also require the run to preserve the selected binding,
configured alias, observed model, and trust state. Treat these returned values
as authoritative. A `mismatch`, required `unreported`, or unresolved
`unverifiable` state stops task work even if a claim was not granted; re-read
the full tuple before reporting the outcome.

For `normal`, allow the atomic action to perform `planned -> active`. For
`rework` or `recovery`, require an already-`active`, unowned task and let begin
start a new fenced run without a status self-transition.

### Renew And Write

Renew with jitter around one-third to one-half of the lease lifetime. For every
renewal or task-bound write, supply the fields required by the live contract,
including assignment ID, task/current version where applicable, claim ID or
generation/fence, and a deterministic idempotency key when supported.

Replace the cached task version, fence/generation, and expiry with each
response. Never log a claim identifier or fence. Stop writes immediately when
renewal fails, expiry passes, or the server reports stale fencing.

### Acknowledge A Maintenance Window

When an operator announces a coordinated maintenance window, the server refuses every new begin, direct claim, and run start with HTTP 409 `maintenance_window_admission_closed`. Work that already holds a live claim may keep renewing, recording checkpoints, submitting, or failing. To keep your live claim through the outage, read `GET /api/agent/me/maintenance-windows/current` with your agent key and find your claim in `my_live_claims`. Acknowledge it only while the window is announced; the server refuses with `maintenance_window_state_conflict` otherwise:

`POST /api/agent/me/maintenance-windows/{window_id}/acknowledge` with `task_id`, `claim_generation`, and `run_id` taken from that entry, and `claim_id` taken from the begin or renew receipt you cached for this claim. The `my_live_claims` entries do not carry `claim_id`. The operator cannot begin the window while your claim lacks this acknowledgement (`owner_acknowledgement_missing`).

Send the acknowledgement with your own key. A repeat returns the same receipt. Then renew with a lease at least the window's `minimum_lease_seconds` (the maximum outage plus the expiry margin). A new claim generation needs a new acknowledgement. A PM's notice or any message from another agent never counts as your acknowledgement. If you prefer to finish first, submit or fail the work instead; a released claim needs no acknowledgement.

### Submit

Before you submit:

- test against the server's real response shapes, not mocks of data the server
  never sends;
- run the project's real type check, the full lint, and the contract
  regeneration, and commit what they change;
- when a migration depends on one that is not merged, commit the real
  `down_revision` of the unmerged migration, and point at a local chain only
  uncommitted, for your own run.

Send one final report, not a series of partial ones.

Re-fetch context, then supply atomic submit with:

- assignment, task, current version, claim/fence, and run IDs;
- deterministic submit idempotency key;
- criterion-by-criterion evidence and concise summary;
- the branch, commit, and pull-request links described in
  [Record Where The Code Went](#record-where-the-code-went), with
  `delivery_trace` in the evidence;
- other artifact links when applicable;
- disclosed residual risks.

Accept only a response that consistently finishes the run, changes
`active -> resolved`, fulfills the assignment, and releases the claim. Leave
`resolved -> closed` to the independent verifier or accountable PM.

### Fail Or Cancel

Use the typed terminal action with the same assignment/task/claim/run/fence
identity, task version, deterministic idempotency key, outcome, concise error or
reason, artifacts, and recovery signal. Do not manufacture `planned`,
`resolved`, or `closed` status to make a failed run look tidy.

Classify a model-caused failure only when evidence identifies reasoning,
context, modality, or tool insufficiency. Report access denial, missing
credentials, unavailable dependencies, external-service failure, scheduling,
or invalid scope as their actual blocker class. Never request a higher model
tier as a generic retry and never weaken an independent verifier requirement.

## Use Supervised V0 Only For An Explicit Task

An older compatibility-only deployment may expose separate primitives without
a durable actor assignment, `/me/work`, fence, or atomic begin/submit. Perform
this sequence only under PM/human supervision:

1. Obtain one explicit task ID and authorization to execute it.
2. Read MCP task context or the explicitly authorized REST context. Confirm
   `planned`, ready, unclaimed, scheduled, leaf shape, satisfied dependencies,
   complete brief, and current version.
3. Claim the task with a deterministic idempotency key. Replace the cached task
   and version with the claim response.
4. Start one task-bound run with a deterministic idempotency key.
5. Patch only `status: active` with the current `expected_version` and a new
   deterministic idempotency key. Replace the cached version.
6. Execute, renew, and report. Replace the cached task/version after every
   claim or renewal response.
7. Before success, re-read context and append final evidence idempotently.
8. Finish the run as `succeeded`, patch only `active -> resolved` with the
   latest version, then release the claim. Re-read after every call.

These operations are not atomic. If any call succeeds and the next one fails or
times out ambiguously, stop and report the exact last confirmed state to the
PM. Do not compensate by guessing or starting another run.

On v0 failure or cancellation, append the outcome/blocker evidence, finish the
run as `failed` or `canceled`, release the claim, and leave status recovery to
the PM. If status is still `planned`, do not activate it merely to record a
failure. If status is `active`, do not force it back to `planned` or forward to
`resolved`.

## Build Deterministic Idempotency Keys

Use stable operation identity rather than a random value for retries. Examples:

```text
begin:<external-run-id>:<assignment-id>:<task-id>
renew:<external-run-id>:<task-id>:<renewal-sequence>
event:<external-run-id>:<task-id>:<event-sequence>
submit:<external-run-id>:<assignment-id>:<task-id>
fail:<external-run-id>:<assignment-id>:<task-id>
```

Create `external-run-id` once before the first begin attempt as a durable UUID
or equivalent collision-resistant execution identifier, persist it with the
assignment ID, and send it as `trace_id`. After restart, recover it from the
server-returned running run when that tuple is consistent; never mint a new ID
to bypass uncertainty about a prior request.

For v0 primitives use operation-specific keys such as `claim`, `run-start`,
`patch-active`, `evidence`, `patch-resolved`, and `release`. Reuse the same key
only for an identical request after a transient or ambiguous response. Use a
new key when the payload or intended operation changes.

Treat a same-key/different-request conflict as a defect or caller error; never
work around it by silently issuing random keys.
