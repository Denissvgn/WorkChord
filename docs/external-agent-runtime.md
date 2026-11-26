# Run an external agent

WorkChord coordinates identity, assignments, execution ownership, evidence and
review. An external runtime executes the model and tools. The
`workchord-worker` executable installed with the backend delivers queued
outbound events; the `workchord-worker` **role package** guides an external
execution agent. Provisioning either does not start a model runtime.

## Upgrade to 1.8.0

Server 1.8.0 changes what role packages and clients read, with no
compatibility period. Upgrade the server and every agent runtime together:

1. Install the role packages from the 1.8.0 skill catalog: `workchord-pm`,
   `workchord-worker`, and the new `workchord-reviewer`. The catalog requires
   server 1.8.0 or later.
2. Move every verifier to `workchord-reviewer`, as described in
   [agent-team setup](agent-team-setup.md#move-verifiers-to-the-reviewer-package),
   and acknowledge each runtime's new handoff.
3. Update any client that reads `GET /api/agent/pipeline`: the
   `ready_for_agent` and `definition_ready_unassigned` lists are replaced by
   one `ready_to_assign` list, and every stage list is always present.
4. Expect a worker's claim-fenced `agent.blocker` task event to mark the task
   Blocked. Only the PM or a person removes the block.

## Provision and connect

1. Follow [agent-team setup](agent-team-setup.md) to create the exact actors,
   capability profiles and model bindings. Use the current
   [portable master](../config/examples/agent-team-master.json), validate it,
   inspect its revision-bound plan, and apply only reviewed actions.
2. Deliver the secret-free handoff and the agent key separately through the
   configured external sink. Provider credentials stay in the runtime's secret
   store; a WorkChord model binding contains intended configuration metadata.
3. Obtain the exact role version and checksum from the verified server catalog.
   Install those bytes, or use the tracked
   [Codex role adapter](../adapters/codex/workchord-agent-roles). Missing or
   mismatched checksums stop delivery.
4. Send the exact `agent-team-runtime-ack-v1` fields from the current handoff to
   `POST /api/agent/team-setup/onboarding/acknowledge`, using only its restricted
   `X-Agent-API-Key`. Onboarding credentials cannot call ordinary REST or MCP
   operations until acknowledgement succeeds. Return the handoff's
   `runtime_instance_id` unchanged, and list `runtime-instance-identity-v1` in the
   acknowledged `server_features`; a different identity is refused. See
   [Identify the runtime instance](agent-team-setup.md#identify-the-runtime-instance).
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

## Give an agent its key

A desktop or sandboxed agent usually does not inherit the environment of the
terminal you exported a key in. Give it the key through a source it reads on
its own, never by pasting the key into chat. The role skills look in this order
and use the first one present:

1. The MCP client's own configuration, as a bearer token for `/api/mcp`.
2. `AGENT_API_KEY` (REST) or `MCP_AGENT_API_KEY` (stdio MCP).
3. The file named by `AGENT_API_KEY_FILE` or `MCP_AGENT_API_KEY_FILE`.
4. The default key file `~/.config/workchord/<role-skill>.key` (under
   `$XDG_CONFIG_HOME` when it is set), for example
   `~/.config/workchord/workchord-pm.key`.

The provisioning script can write the one-time key straight to that file:

```bash
python3 scripts/api_keys/create_agent_actor.py --role pm --name desk-pm --key-file
```

It creates the file readable only by you, refuses to overwrite an existing file
or to write inside a Git work tree, and prints the file path instead of the key.
Pass `--key-file PATH` to choose another location. Stdio MCP accepts the same
file through `MCP_AGENT_API_KEY_FILE`; a group- or world-readable key file is
refused.

An agent without a key can read `GET /.well-known/workchord/agent-connect.json`.
It needs no credentials and returns the auth mode, the capabilities and MCP
paths, where keys are read from, and the actor role and scopes for each role
skill. It never contains a key.
A server built before this route may answer `200` with the web app's HTML page;
only a JSON body with `schema_version` `workchord-agent-connect/v1` is the hint.

## Run MCP without a person to approve calls

Every WorkChord MCP tool declares how it behaves, and a client can decide from
that declaration alone:

| Declaration | Tools | Hints |
| --- | --- | --- |
| Read | `get`, `list`, `search`, `preview`, `draft` and recommendation tools | `readOnlyHint: true` |
| Write | Every tool that creates or changes a record | `readOnlyHint: false`, `destructiveHint: false` |
| Removal | `agent_delete_project_milestone`, `workspace_delete_external_link`, `workspace_unlink_request_source` | `destructiveHint: true` |

All tools act only on WorkChord's own records and declare `openWorldHint: false`.
The declaration describes behavior; the actor key's scopes still decide what a
call may do.

Codex asks for approval before any MCP tool it must assume is destructive, and
a tool that declares nothing is assumed destructive. `codex exec` has nobody to
ask, so it refuses the call and reports `user cancelled MCP tool call` or
`MCP tool call requires approval, but approval policy is never`. With the
declarations above, an unattended Codex session runs every read and write tool
and refuses only the three removal tools.

Set the approval mode on the `workchord` server entry when the default does not
fit:

```toml
[mcp_servers.workchord]
url = "http://127.0.0.1:8480/api/mcp"
bearer_token_env_var = "WORKCHORD_AGENT_KEY"

# A PM runtime that must remove milestones or links without a person:
[mcp_servers.workchord.tools.agent_delete_project_milestone]
approval_mode = "approve"
```

- `default_tools_approval_mode = "approve"` runs every tool without asking. Use
  it for an unattended runtime connected to a server that does not declare its
  tools yet; the actor key's scopes remain the limit.
- `default_tools_approval_mode = "writes"` asks before every tool that is not
  read-only, for an interactive session that should confirm each change.

An MCP call that was refused for approval never reached WorkChord and changed
no work state. It is a fault in the runtime's configuration, not in the server
or the actor key.

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

## Keep a claim through a maintenance window

While an operator has a maintenance window open, a new begin, claim or run
start returns HTTP 409 `maintenance_window_admission_closed`. Retry it after
the window's planned end. Live work continues as usual. To keep a live claim
through the restart, read `GET /api/agent/me/maintenance-windows/current`,
acknowledge with `POST /api/agent/me/maintenance-windows/{window_id}/acknowledge`
and your task, claim ID, claim generation and run, then renew with at least
`minimum_lease_seconds`. Retry a request that fails during the outage with the
same idempotency key. A PM records
`POST /api/agent/me/maintenance-windows/{window_id}/notice-receipt`. See the
[maintenance window runbook](runbooks/control-plane-maintenance-window.md).

## Interpret readiness and routing

`configured` identifies server metadata; current acknowledgement identifies an
exact runtime declaration. `runtime_ready` means configuration and current
handoff checks pass. Task eligibility and fenced ownership are additional
checks. `availability_unknown` remains explicit without an independent
availability observation; advisory runtime observations from paired observers
are recorded separately and never change it or any dispatch decision (see
[advisory runtime observations](agent-team-setup.md#record-advisory-runtime-observations)). Model `matched` is consistency with a worker report;
it does not establish independent model attestation.

Routing `off` uses supervised compatibility commands. `shadow` exposes advisory
assessments without enforced autonomous selection. `enforced` requires current
topology readiness, assessment, preview and selected binding evidence. A worker
must use the mode and capabilities advertised by its deployment.

## Declare the harness session

When the runtime gives a worker its own session or conversation identifier, the
worker sends it once when it begins work, as run metadata:
`{"metadata": {"harness": {"kind": "claude-code", "session_id": "..."}}}`. `kind`
is a short lowercase runtime name and `session_id` is the runtime's identifier,
never a file path; malformed or credential-shaped values are refused. `trace_id`
stays the worker's per-attempt run ID, because one session can serve several
assignments. Like usage reports, the harness session is the actor's
declaration: it lets an independent observer match a run to the session that
performed it, and WorkChord stores it without verifying it.

## Link the work to its code

When the server advertises `work-delivery-links-v1`, a worker records where a
task's code went. Begin takes an optional `branch_url`
(`https://github.com/<owner>/<repo>/tree/<branch>`); submit takes `branch_url`,
`commit_urls` (one `.../commit/<full-sha>` URL per commit) and the existing
`pr_url`. WorkChord links each URL to the task as a GitHub external link in the
same command, skips a URL the task already has, and refuses a URL of the wrong
kind or a short commit SHA. The older `commit_url` field still accepts any
reviewable URL; only a GitHub commit URL there becomes a link. Without the
feature, send none of the new fields, because the server refuses unknown fields.

The role skills name the branch `wc-<task-id>-<slug>`, end each commit message
with `WorkChord-Task: WC-<task-id>`, and name `WC-<task-id>` in the pull
request, so a commit or pull request also leads back to its task. A reviewer
checks the links against the reviewed diff before accepting. A PM counts a task
as done only with a commit or pull-request link or a stated reason why none
exists, and links a shipped release to its merge pull request or tag with
`workspace_create_release_github_link`.

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
[reviewer](../agent-skills/workchord-reviewer/SKILL.md) ·
[model routing](runbooks/model-aware-routing.md).
