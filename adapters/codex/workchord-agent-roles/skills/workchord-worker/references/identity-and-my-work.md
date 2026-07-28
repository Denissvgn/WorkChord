# Identity And My Work

Use this reference to establish authority, choose autonomous v1 or supervised
v0, and interpret the server-owned work decision.

## Separate The Runtime Identities

Keep these concepts independent:

| Concept | Meaning | Never infer it from |
| --- | --- | --- |
| Capacity owner | Iteration team member carrying planned effort | Actor identity or claim |
| Actor profile | Advisory capability and routing information | Permission or exact assignment |
| Task assignment | Durable dispatch to one exact actor and queue position | Capacity ownership or claim |
| Selected model binding | Operator-declared intended runtime and capability envelope | Credentials, permission, or observed execution |
| Claim/fence | Temporary exclusive execution authority | Assignment or task status |
| Observed model evidence | Worker-reported resolved runtime recorded on a run | Independent or cryptographic attestation |
| Run and task status | Execution attempt and business lifecycle | Each other |

Treat profile capability matches as advisory. Enforce permissions through actor
scopes and enforce execution ownership through the assignment plus live claim
and fence.

## Read Identity Safely

Obtain configuration from the runtime secret/configuration store:

- `WORKCHORD_BASE_URL` and an optional API-prefix setting;
- `AGENT_API_KEY` for REST;
- `MCP_AGENT_API_KEY` for MCP.

Never ask a user to paste a key into task context and never echo it. Confirm that
all calls use the same real, enabled `AgentActor`; never use the bootstrap key
for normal work or MCP.

Read the authenticated capability response when the deployment offers it.
Confirm:

- server and API contract versions;
- actor ID, role, optional profile, enabled state, and scopes;
- work policy and `max_parallel_work`;
- lease limits and supported lifecycle actions;
- stable feature keys and recommended worker-skill compatibility.
- when model-aware routing is advertised, the assignment/context fields that
  carry assessment policy, selected binding/revision, configured alias, and
  required observed-model evidence.

An actor profile does not grant permission. A broad scope does not authorize a
worker to perform PM planning or independent verification.

Stable assigned-work v1 currently requires `work_policy=assigned_only` and
`max_parallel_work=1`. Stop as incompatible if the live actor reports another
value; managed-pool selection and multiple current items are not part of this
role version.

## Gate The Mode

Use autonomous v1 only when all required features are advertised:

| Feature | Guarantee required by this skill |
| --- | --- |
| `agent-capabilities-v1` | Authenticated actor, scope, policy, action, feature, and compatibility handshake |
| `actor-task-assignments` | Exact, durable execution dispatch to this actor |
| `my-work-v1` | Server-owned current/next decision and queue revision |
| `snapshot-pagination-v1` | Ready, blocked, review, and recovery pages use opaque snapshot-bound cursors |
| `work-etag-v1` | REST work polling supports a private weak ETag and bodyless `304` |
| `complete-task-context` | Assignment, brief, dependencies, readiness, timeline, and evidence contract |
| `atomic-begin-submit` | Transactional lifecycle boundaries for start and success |
| `atomic-renew-v1` | Lease extension and run heartbeat update remain one fenced operation |
| `fenced-claims` | Stale writers cannot mutate after lease loss |
| `typed-rework-recovery` | Rework, failure, cancellation, and recovery remain discoverable |
| `agent-discovery-triage-v1` | Out-of-scope findings become claim-bound, attributable Triage records |

Do not infer support from an endpoint returning `404`, a similar tool name, or
skill prose. If any feature is absent, switch to supervised v0 or stop.

Treat `model-aware-routing-v1` separately from the base v1 gate. Feature
presence permits model-aware execution only when
`model_aware_routing.effective_mode` is `enforced`. Then require the exact
selected binding and begin-evidence fields from the live operation metadata.
In effective `off` or `shadow`, continue the base assigned-work lifecycle for
legacy assignments when all base features remain available, but do not begin a
queued model-aware assignment or infer a model choice from the assignment
reason, profile, provider-facing name, or local configuration. If the feature
is advertised but mode status or the binding/evidence contract is incomplete,
stop as incompatible rather than downgrading silently.

Supervised v0 requires all of the following:

- one explicit task ID supplied by a PM or human;
- explicit confirmation that this actor may execute it;
- a complete brief and satisfied readiness checks;
- one-task-at-a-time supervision;
- acceptance that claim, run, and status calls can partially succeed.

Do not use `agent_list_ready_tasks` or `/api/agent/tasks/ready` to select work in
v0. The ready list is a compatibility/readiness surface, not proof of dispatch.

## Interpret `/me/work`

Fetch `GET /api/agent/me/work?limit={n}` or call `agent_get_my_work(limit=n)`.
Preserve the returned server time, selection-policy version, queue revision,
pagination snapshot revision and cursor, assignment IDs, task versions,
claim/run summary, selection reason, blocker codes, and next-poll time.

| State | Required action |
| --- | --- |
| `resume` | Validate and resume only `current`; never accept another task |
| `start_assigned` | Validate and atomically begin only `next` |
| `wait` | Start nothing; wait until the reported safe poll time or a refetch hint |
| `no_work` | Record or return idle state and end the acquisition cycle |
| `attention_required` | Start nothing; preserve recovery codes and escalate |

Treat rework and recovery as explicit assignments, not as normal ready tasks.
Exclude verification-purpose assignments from this implementation-worker loop.
For a model-aware decision, require `current` or `next` plus complete context to
agree on the selected binding ID/revision and routing lineage; local runtime
availability does not authorize substitution.
If multiple current items, an orphan active task, a lost lease, a conflicting
run, or an unknown state appears, stop with `attention_required` semantics even
if another queue item looks runnable.

The first response without a cursor owns the action decision. `next` remains
the global authoritative first assignment on later pages; never select work
from page position. When queue inspection is needed, follow only the opaque
`pagination.next_cursor` while `pagination.has_more` is true. The work response
pages `queue` and `blocked_assigned` independently and reports each collection's
returned/has-more state. Do not edit, decode, persist across actors, or reuse a
cursor after a `409 stale_cursor`; restart from the first page.

For REST polling, send the last weak `ETag` as `If-None-Match` with the same
limit and cursor. A bodyless `304` means the ownership-equivalent decision is
unchanged; keep the prior body, but schedule the next poll from the fresh
`Retry-After` header rather than the retained body's now-stale
`next_poll_after`. Any notification, changed parameters, or non-`304` response
requires using the newly returned decision and ETag.

## Restart Correctly

On process restart:

1. Discard local assumptions about current or next work.
2. Re-authenticate and re-read capabilities.
3. Fetch `/api/agent/me/work`, `/api/agent/me/claims`, and
   `/api/agent/me/runs`, or `agent_get_my_work`, `agent_list_my_claims`, and
   `agent_list_my_runs` through MCP.
4. Resume only a complete server-confirmed assignment/claim/fence/run tuple.
5. Request PM recovery for every mismatch; the PM uses
   `GET /api/agent/recovery` plus
   `POST /api/agent/recovery/{task_id}/requeue`, or
   `agent_list_recovery_tasks` plus `agent_requeue_recovery`. Never invoke the
   PM command or claim a replacement task yourself.

Polling is the portable acquisition baseline. Use the server cursor, ETag, and
bounded backoff as described above. Treat webhooks and MCP notifications only
as hints to fetch a fresh first-page decision.
