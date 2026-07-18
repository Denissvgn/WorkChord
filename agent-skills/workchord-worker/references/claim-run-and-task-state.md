# Claim, Run, And Task State

Use this reference for lifecycle mutations. Once work is selected, keep the
procedure low-freedom.

## Keep State Independent

- Assignment answers who was dispatched and in what queue position.
- Claim/fence answers who may write now.
- Run answers which execution attempt produced events and artifacts.
- Task status answers where work is in the business lifecycle.

Never treat one as proof of the others. Refresh the full tuple after every
mutation.

## Use Atomic V1 Actions

### Begin

Supply the server-advertised atomic begin action with:

- assignment ID for the selected execution-purpose assignment;
- queue revision from the work decision;
- one deterministic idempotency key for this begin attempt;
- requested lease within advertised limits;
- trace/correlation data and run metadata that contain no secrets.

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

### Submit

Re-fetch context, then supply atomic submit with:

- assignment, task, current version, claim/fence, and run IDs;
- deterministic submit idempotency key;
- criterion-by-criterion evidence and concise summary;
- artifact links, commit URL, and pull-request URL when applicable;
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
