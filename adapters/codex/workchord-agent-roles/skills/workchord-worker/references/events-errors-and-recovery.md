# Events, Errors, And Recovery

Use this reference to report execution without leaking data and to stop safely
when state becomes uncertain.

## Emit Bounded Evidence

Prefer typed lifecycle actions when the server advertises them. Otherwise use
task/run event types consistently, for example:

| Purpose | Suggested event | Minimal payload |
| --- | --- | --- |
| Progress | `agent.progress` | completed, next step, risk, percent or checkpoint |
| Checkpoint | `agent.checkpoint` | durable artifact or verified intermediate state |
| Blocker | `agent.blocker` | blocker, impact, attempted checks, owner/action needed |
| Discovery | typed `agent_report_discovery` | Triage ID, impact, blocking classification |
| Final evidence | typed submit/fail evidence | criteria/results, checks, artifacts, residual risks |

Use server-defined event names when they differ. Keep payloads small and
structured. Include trace/correlation identifiers where supported. Never put
API keys, claim identifiers/fences, private prompts, credentials, personal
data, or raw large logs in an event. Store large evidence durably and link it.

Emit progress at meaningful checkpoints or before lease/recovery risk, not on
every tool call. Never use an event as a substitute for the authoritative task,
assignment, run, or claim transition.

The v1 server allows only `agent.progress`, `agent.checkpoint`, and
`agent.blocker` for agent-authored task events. Every other task-event name is
server-owned; do not imitate it. A JSON event,
metadata, or evidence object is capped at 100 top-level fields and 32,768
serialized UTF-8 bytes; event messages are capped at 4,000 characters, summary
and error text at 8,000 characters, and artifact links at 50. Keep packets well
below those limits and link large logs or artifacts.

Assignment-bound run events use the same three event names. In assigned-work
v1, every new task event needs a header idempotency key and every new run event
needs its payload idempotency key; both also require the current claim ID and
generation. Supervised-v0 events follow the narrower compatibility contract in
[api-and-mcp.md](api-and-mcp.md). Reuse a key only for the byte-equivalent
logical request. The server resolves an exact receipt before checking a
now-terminal fence, but rejects a changed event type, payload, trace data, or
fence request under the same key.

## Classify Discoveries

- **Blocking:** invalidates safe execution or an acceptance criterion. Stop and
  request PM action.
- **Confidence-reducing:** allows bounded progress but weakens certainty. Record
  it and follow the brief's escalation rule.
- **Non-blocking:** belongs outside scope without changing current success.
  Create linked Triage and continue only the current scope.

Do not create replacement tasks or self-assign discovery work.

## Handle Errors Deliberately

| Result | Required behavior |
| --- | --- |
| `401` | Stop; obtain corrected credentials through the secret-management path |
| `403` | Stop; request corrected least-privilege actor policy; do not seek a broader key |
| `404` | Refetch identity/work/context; stop if the authoritative object is gone |
| assignment/claim/version/fence `409` | Refetch full work and context; re-evaluate; never blind-retry |
| pagination `409 stale_cursor` | Discard the opaque cursor and restart the same read from its first page |
| `400`/`422` validation | Correct the request or escalate; never retry unchanged |
| `429` | Honor retry timing; reuse the same key only for an identical idempotent request |
| timeout/`5xx` | Back off; re-read state before retrying; preserve the key for an identical supported operation |

If a terminal write times out and the operation lacks replay-safe idempotency,
do not guess whether it committed. Read current state. If still ambiguous,
stop and ask the PM/operator to reconcile it.

## Stop On Lease Or Fence Loss

When renewal fails, expiry passes, or fencing is rejected:

1. Stop modifying task artifacts when another worker could observe or publish
   them; preserve local diagnostics safely.
2. Make no further task-bound writes with the stale claim.
3. Refetch `/api/agent/me/work`, the assignment-bound context,
   `/api/agent/me/claims`, and `/api/agent/me/runs` (or their exact MCP v1
   equivalents).
4. Report the last confirmed assignment, task version, run state, and expiry
   without disclosing claim/fence secrets.
5. Resume only if the server returns a fresh consistent `resume` tuple.

Never claim a different task as a way to recover from lost ownership.

## Surface Inconsistent State

Return `attention_required` semantics and request recovery when any of these
appear:

- multiple current assignments or runs for an actor limited to one;
- active task without a valid execution assignment and live claim/run;
- running run after claim expiry or actor disablement;
- succeeded run while the task remains active;
- resolved task with a running run;
- accepted assignment whose task/claim belongs to another actor;
- accepted assignment whose bound task version no longer matches the current
  scope/criteria version;
- ambiguous v0 claim, activation, finish, resolve, or release response.

Include object IDs, public versions/statuses, last confirmed operation, error
code, and proposed reconciliation check. Exclude credentials and fencing
secrets.

When lease/fence loss prevents a safe server event, return that structured
attention report through the invoking orchestrator or PM/operator handoff
channel. Do not attempt a task/run mutation merely to persist the report.

The worker never reconciles stale ownership itself. The PM reads
`/api/agent/recovery` and invokes `/api/agent/recovery/{task_id}/requeue`, or
uses `agent_list_recovery_tasks` and `agent_requeue_recovery`. Treat a PM message
or notification only as a hint; resume only after `/me/work` returns a fresh,
consistent assignment tuple.

## End Failure Or Cancellation Safely

For v1, call the typed fail/cancel action once with current assignment,
task/version, claim/fence, run, idempotency, reason, evidence, and recovery
classification. Verify the returned state.

For supervised v0:

1. Append a concise blocker/failure event when the claim is still live.
2. Finish the running run as `failed` or `canceled`.
3. Release the claim.
4. Re-read state and give the PM the exact confirmed/unknown outcomes.

Do not close, resolve, reassign, requeue, or select replacement work after a
failure. The PM/recovery owner decides whether to rework, recover, defer, or
return the issue to Triage.
