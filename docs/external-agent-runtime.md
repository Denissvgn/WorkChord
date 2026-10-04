# Run an external agent

WorkChord coordinates identity, assignments, execution ownership, evidence and
review. An external runtime executes the model and tools. The
`workchord-worker` executable installed with the backend delivers queued
outbound events; the `workchord-worker` **role package** guides an external
execution agent. Provisioning either does not start a model runtime.

## Provision and connect

1. Follow [agent-team setup](agent-team-setup.md) to create the exact actors,
   capability profiles and model bindings. Use the current
   [portable master](../config/examples/agent-team-master.json), validate it,
   inspect its revision-bound plan, and apply only reviewed actions.
2. Deliver the secret-free handoff and actor credential separately through the
   configured external sink. Provider credentials stay in the runtime's secret
   store; a WorkChord model binding contains intended configuration metadata.
3. Obtain the exact role version and checksum from the verified server catalog.
   Install those bytes, or use the tracked
   [Codex role adapter](../adapters/codex/workchord-agent-roles). Missing or
   mismatched checksums stop delivery.
4. Send the exact `agent-team-runtime-ack-v1` fields from the current handoff to
   `POST /api/agent/team-setup/onboarding/acknowledge`, using only its restricted
   `X-Agent-API-Key`. Onboarding credentials cannot call ordinary REST or MCP
   operations until acknowledgement succeeds.
5. Retain the acknowledgement digest. When revisions change, obtain the current
   handoff and explicitly refresh with `expected_previous_acknowledgement_digest`.
   A stale handoff or changed body does not authorize blind replacement.
6. Start the external runtime with its own provider/tool configuration. Verify
   actual provider access and availability separately from handoff checks.

After onboarding, REST uses `X-Agent-API-Key`. The web instance exposes
authenticated streamable MCP at `/api/mcp` (or the configured API prefix).
Local stdio MCP uses `MCP_AGENT_API_KEY` from the runtime secret store:

```bash
.venv/bin/workchord-mcp --transport stdio
```

Stdio MCP requires the backend's configured database environment. Remote
runtimes normally connect to the web instance's MCP endpoint or REST API.
Keep credentials and transient claim/fence receipts out of task text, prompts,
shared logs and artifacts.

## Read the authoritative work decision

Read `/api/agent/capabilities` or `agent_get_capabilities`. Confirm identity,
scopes, current features, lease bounds and `max_parallel_work=1`. Read
`/api/agent/me/work` or `agent_get_my_work`:

| State | Runtime action |
| --- | --- |
| `start_assigned` | Use the exact server-selected assignment and queue revision |
| `resume` | Reconcile and resume the returned current run and live fence |
| `wait` / `no_work` | Honor server timing; select no substitute work |
| `attention_required` | Stop task-bound writes and request explicit recovery |

Fetch assignment-bound complete context before beginning and before submitting.
Use `task.brief` when present, including ordered criterion IDs/revisions and
verification instructions. Legacy Markdown is a fallback only when canonical
brief data is absent. Changed scope, criteria, assignment, topology or model
binding requires fresh context and an appropriate PM decision.

## Begin, renew and submit

Use the generated [REST/MCP operation reference](../agent-skills/workchord-worker/references/api-and-mcp.md).
Begin atomically through `/api/agent/me/work/begin` or `agent_begin_my_work`.
In enforced routing, supply the selected binding ID/revision and the observed
resolved model. Preserve the returned assignment, task version, run, claim ID,
claim generation and expiry in runtime-private state.

Renew before expiry with the exact current tuple and a deterministic
idempotency key. Submit through the typed submit command with current task
version, run and fence, bounded artifacts and criterion-level progress:
`criterion_id`, `criterion_revision`, `state: completed`, and evidence for each
current criterion. A successful execution resolves implementation work;
acceptance requires an eligible independent verifier or accountable human
reviewer with the current task, brief and artifact revisions.

For a rejection, retain artifacts and the recorded criterion failures. The PM
makes the fresh rework/routing decision. In supervised routing, provisional
lineage remains blocked until an explicit supervised exact reassignment.
The worker resumes only from a fresh authoritative work decision.

## Handle interruptions and conflicts

Preserve the logical request and idempotency key after an ambiguous response.
Replay only identical supported content, then read current work and context.
Stop on expired/lost fences, stale versions or unauthorized scope; never
blindly resubmit against a newer version or select another task to recover.
Typed fail/cancel and PM recovery retain historical attempts and require
current ownership/revision inputs. A provider outage or missing credential is
an external blocker, not evidence that a higher model tier is needed.

## Interpret readiness and routing

`configured` identifies server metadata; current acknowledgement identifies an
exact runtime declaration. `runtime_ready` means configuration and current
handoff checks pass. Task eligibility and fenced ownership are additional
checks. `availability_unknown` remains explicit without an independent
availability observation. Model `matched` is consistency with a worker report;
it does not establish independent model attestation.

Routing `off` uses supervised compatibility commands. `shadow` exposes advisory
assessments without enforced autonomous selection. `enforced` requires current
topology readiness, assessment, preview and selected binding evidence. A worker
must use the mode and capabilities advertised by its deployment.

## Record usage and evaluate outcomes

Follow [execution usage](execution-usage.md): report attempt totals with an
explicit source, provenance, interval, coverage and deterministic report ID.
Unknown counters remain unknown. Corrections require the current report digest
and preserve prior reports and price snapshots. Simulations have separate
totals, currencies remain separate, and reports remain unreconciled declarations.

Use [delivery analytics](delivery-analytics.md) to relate coverage to accepted
outcomes, review delay, rework and recovery. Explicit manual effort is separate
from elapsed duration. Independently reconcile actual provider receipts and
criterion-level acceptance before claiming delivery economics. Missing runtime,
reviewer or baseline observations remain unavailable.

Role references: [planner](../agent-skills/workchord-pm/SKILL.md) ·
[execution worker](../agent-skills/workchord-worker/SKILL.md) ·
[model routing](runbooks/model-aware-routing.md).
