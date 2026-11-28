# Agent team setup

An agent team has a PM (the controller), one or more workers, and optional
reviewers. Each member runs in its own runtime and has its own key. There are
two ways to set one up:

- **Connect an agent** (the default path) adds one member at a time from
  **Team → Connect**. You answer five questions and the server creates the member.
- **Advanced: apply a team manifest** reconciles a whole team from a portable,
  secret-free master file. It is the path for reviewing every change, adopting
  existing members, rotating credentials, and rolling back.

The server remains authoritative for actor IDs, scopes, profile and binding
revisions, lifecycle state, topology revision, and handoff checks. A
configured member is desired state, not proof that a runtime is connected or
available for a particular task.

## Connect an agent

Open **Team**, then the **Connect** tab. The **Members** tab lists the people and
agents already on the team, and the **Models** tab holds the model catalog.

Connecting an agent needs unlocked editing. Choose **Unlock editing** from the
account menu, or at the top of Settings, and enter the admin key the operator
gave you. See [identity and recovery](identity-and-recovery.md#account-menu-and-unlock-editing).
The operator must also have configured the server's credential folder.

Then answer five questions:

1. **Role.** What the agent will do. **PM** plans the work, assigns it, and keeps
   the team moving. A team has one PM. **Worker** does the tasks assigned to it
   and reports the evidence. **Reviewer** checks finished work against its
   acceptance criteria. The manifest calls this role `verifier`.
2. **Runtime.** Where the agent runs: **Pi with a local model**, or **Other**.
3. **Model.** An enabled catalog entry. A catalog entry describes a model; it
   does not install it. If no entry is enabled, add one in the Models tab first.
   For Pi, choose the entry that matches the local model configured in Pi.
4. **Review.** Choose **Review change**. The server validates and plans the
   change. Connecting applies only the new member. Existing members stay unchanged.
5. **Connect.** Choose **Connect agent**. The server creates the member and
   writes its key to the credential folder. This page never receives the key.

After the connection is created, the page shows the credential folder reference,
the skill package to install, and a configuration snippet for the runtime:

- Install the role package from the server skill catalog. The page shows its
  name, version, and SHA-256 digest.
- On the runtime host, set `WORKCHORD_CREDENTIAL_DIR` to the private folder
  behind the reference shown. For a runtime on another machine, move the key
  file over a secure channel. The snippet needs `jq` and keeps the key inside the
  runtime environment.
- Start the runtime with the snippet. It acknowledges onboarding with its own key.

The page then shows **Waiting for the runtime acknowledgement…**, and **Connected**
once the runtime has acknowledged. Use **Check connection** to look again.
A member is not routed work until its runtime acknowledges.

If the connection fails, the page explains why:

- **The server could not confirm the key was written.** The server created the
  member but disabled it. Retrying does not change that. Open **Advanced**, start
  from the current manifest, run the dry run, and confirm the credential
  replacement it offers for this member.
- **The connection was interrupted.** Retry the same request. It returns the
  original receipt and does not create a second agent.
- **The credential folder is not available.** Ask the operator to configure it,
  then review again.

## Advanced: apply a team manifest

Use the manifest path when you need to see and approve each change before it
applies. Open **Team → Connect** and choose **Advanced: apply a team manifest**
at the bottom of the page. The same server rules apply on this path, and it
can change more than one member at once.

### Prerequisites

1. Configure `WORKCHORD_ADMIN_API_KEY`.
2. Create an operator-owned credential sink directory, set its permissions to
   `0700`, and configure `AGENT_TEAM_CREDENTIAL_SINK_DIR`.
3. Set `AGENT_TEAM_CREDENTIAL_SINK_REF` to the non-secret reference prefix used
   by every member in the master.
4. Create and enable the provider-neutral model catalog entries referenced by
   the master. Provider credentials do not belong in the catalog or master.
5. Use immutable package identities from the server's agent skill catalog.
   Each role has its own package: `workchord-pm` for the controller,
   `workchord-worker` for workers, and `workchord-reviewer` for reviewers.

Start from
[`config/examples/agent-team-master.json`](../config/examples/agent-team-master.json).
Replace deployment-specific URLs, runtime references, and model catalog keys.
The JSON Schema is generated at
`docs/contracts/agent-team-master-v1.schema.json`.

### Start from the current team or a template

The manifest editor offers two starting points without copying files:

- **Start from the current team** loads the applied master. If no team is
  applied yet, use a template.
- **Start from a template** loads one filled from this server's own catalogs,
  with the latest role package and its digest for each role and the first
  enabled model catalog entry.

`GET /api/agent/team-setup/starting-points` returns both (`current` is null
before any team is applied). Problems are listed with the manifest line they
refer to, and safe plan actions (no authority change, no confirmation) can be
applied together; the rationale is always typed by the operator.

### Validate and plan

Validation checks canonical shape, secret exclusions, role and package
compatibility, model/profile references, server features, and the configured
credential sink:

```bash
.venv/bin/python scripts/api_keys/setup_agent_team.py \
  validate config/examples/agent-team-master.json
```

Read status to obtain the current topology revision, then request a plan bound
to that exact revision:

```bash
.venv/bin/python scripts/api_keys/setup_agent_team.py status

.venv/bin/python scripts/api_keys/setup_agent_team.py \
  plan config/examples/agent-team-master.json \
  --expected-revision 0
```

Save the plan response. Its action IDs and digest are stable for the same
desired and current state. Inspect every action. Adoption, replacement,
disablement, and other authority-changing actions require deliberate review;
the service never converts absence from a manifest into a hard delete.

### Apply selected actions

Apply only exact reviewed action IDs. There is intentionally no bulk
"apply everything" operation:

```bash
.venv/bin/python scripts/api_keys/setup_agent_team.py \
  apply config/examples/agent-team-master.json \
  --plan /secure/operator/agent-team-plan.json \
  --approve create-primary-pm \
  --approve create-backend-worker \
  --idempotency-key agent-team-approved-20260728
```

Use `--confirm ACTION_ID` as well as `--approve ACTION_ID` for an action whose
plan says confirmation is required. Keep the same idempotency key when
resuming an interrupted request. Reusing it with different inputs fails
closed.

The service creates new actors disabled and in onboarding state, writes their
one-time API keys only to the configured sink, and stores a non-secret
delivery receipt. It then configures profiles, model bindings, and handoff
metadata. If delivery is uncertain, the actor stays disabled and the response
identifies the explicit recovery or replacement action; WorkChord never
redisplays the credential.

### Start and acknowledge runtimes

Each configured member's status includes a secret-free handoff with:

- topology and logical actor keys;
- the resolved server-owned actor ID and role;
- server URL and required features;
- immutable package version and checksum;
- profile and binding revisions;
- supported assignment modes and startup instructions;
- the `runtime_instance_id` the server issued for this member's runtime;
- the external credential reference.

The operator delivers the handoff and retrieves the corresponding credential
from the external sink through its own secure process. The runtime checks the
package checksum, starts with the restricted onboarding identity, and posts
the exact handoff acknowledgement to:

`POST /api/agent/team-setup/onboarding/acknowledge`

Only that acknowledgement is accepted during onboarding. Normal
authentication, roster, assignment, and work operations reject the identity
until the acknowledgement matches the current topology revision, actor,
package, profile, model bindings, features, and assignment modes. Successful
acknowledgement activates the actor. Repeated failed acknowledgements are
rate-limited.

### Identify the runtime instance

The handoff carries a `runtime_instance_id`, and the acknowledgement returns it
in a field of the same name. The server records it with the acknowledgement,
so a runtime that did not receive this handoff cannot acknowledge in the
member's place without the difference being recorded. An acknowledgement that
names another identity is refused with `agent_team_ack_runtime_instance_mismatch`
and is not stored.

The server draws the identity at random, and draws a new one each time a
credential delivery succeeds: when a member is created, when a replacement actor
is delivered its credential, and when a credential is recovered. It is stored with
the member and does not depend on the delivery receipt, which a sink may derive
from fixed inputs. A member that existed before the upgrade is issued its own
random identity by the migration, so every handoff names one; an acknowledgement
that predates it carries none and stays valid. The runtime acknowledges again with
a new identity. The identity is an opaque label, not a secret and not a proof: a
runtime that holds a copy of the handoff can return it. It tells apart the
handoffs the server issued, and it makes a change visible.

A refused acknowledgement is recorded in its own short transaction, so the
record survives the failed request. It is audited like the acknowledgement itself
and counts against the attempt limit. A member whose issued identity is missing
(which the migration and member creation prevent) has no handoff, and its status
names the blocker `runtime_instance_not_issued`; the rest of the team's status is
still returned.

The server feature `runtime-instance-identity-v1` states how a runtime that does
not send the field is handled:

- A runtime that lists the feature in its acknowledged `server_features` must send
  the identity. Without it the acknowledgement is refused with
  `agent_team_ack_runtime_instance_missing`.
- A manifest may list the feature in `required_server_features`. A runtime must
  then list it, and so must send the identity.
- Otherwise an acknowledgement without the field is accepted exactly as before.
  Its digest does not change, and the identity reads as unknown. That covers every
  acknowledgement recorded before the upgrade, which stays valid.

Member status adds `runtime_identity` for each member:

- `state` follows the stored acknowledgement alone. It is `unknown` (no
  acknowledgement, or one without an identity), `current` (the acknowledgement
  returned the identity the handoff now carries), `changed` (the same, after
  another identity, or none, held the seat; or the runtime stopped sending one) or
  `stale` (the acknowledgement returned an earlier identity than the handoff now
  carries).
- `expected_instance_id` is the identity the handoff now carries;
  `acknowledged_instance_id` is the one in the stored acknowledgement.
- `previous_instance_id` and `changed_at` say which identity was replaced and
  when.
- `refused_instance_id` and `refused_at` are set while a refusal is recorded: a
  runtime returned another identity and was turned away. A refusal is not a state.
  It is shown beside the state the acknowledgement gives, and an acknowledgement
  that carries the issued identity, including a repeat of the stored one, clears it.

An acknowledgement that carries an identity other than the one the handoff now
carries is stale, so a runtime that was replaced stays out of dispatch until the
new runtime acknowledges. The Connect page and the team setup member cards show
the same state, and the setup report does not list identities.

### Declare tool capabilities

A member may list the tools it expects each model binding to offer in the
optional `declared_tool_tags` object, keyed by model binding key (for example
`{"implementation-default": ["host-shell"]}`). Reconciliation creates bindings
with no tool tags whatever the manifest declares, so a declaration is a
reviewable intent, not a capability. Routing reads only the tags on the binding
itself and keeps reporting `model_tool_missing` for work that needs a declared
but unverified tool.

Member status lists `declared_tool_tags`, the `unverified_tool_tags` that the
binding does not carry yet, and a `tool_capability_next_action`; the handoff's
startup instructions name the same tools, and the team `next_action` points at
them. To verify a capability, the operator adds the tag to the binding with a
binding edit once it has been confirmed on the runtime. The edit moves the
binding revision, so the runtime acknowledges the new revision before the
member is ready again. Adding a declaration to a live team is a member-contract
change, so the runtime acknowledges it again, and the later binding edit needs
another acknowledgement. The declaration is not an acknowledgement and never
adds a tag by itself.

### Interpret status

`GET /api/agent/team-setup/status` and the MCP
`agent_get_team_setup_status` tool share the same backend-derived projection.
Operators may select a topology; a PM can read only its bound topology.

- `configured` means desired server objects exist.
- `onboarding` means at least one required runtime has not acknowledged its
  exact handoff.
- `runtime_ready` means configuration and current revision-bound handoff checks
  pass for required members. It does not establish provider availability or
  independent model attestation.
- `blocked` includes stable blocker codes and an operator next action.
- `connection_state` describes observed freshness.
- `availability_unknown` is intentional without independent runtime/provider
  observations. Concrete task eligibility uses queue, capacity and binding
  checks and remains separate from availability. Advisory runtime
  observations (see below) do not change it.

### Record advisory runtime observations

An independent observer, such as a dashboard paired as a read-only observer,
records what it saw of a runtime session with POST `/api/agent/observations`:
the kind (`session_active`, `session_idle`, `session_ended` or
`model_observed` with the observed model), the harness kind and session ID, the
time it observed it, an idempotency key, and optionally the task, run or actor
it concerns. Only a paired observer or an operator may record one. A task or run
must be readable by the observer, and an observer names an actor only through a
run or assignment of such a task. Repeating a key with the same content returns
the first observation; different content is refused. Each observer may record
`AGENT_OBSERVATION_HOURLY_LIMIT` observations per hour (600 by default).

Observations are advisory. Recording one writes only its own row: no actor,
`last_seen_at`, queue revision, assignment, run, task event, topology member or
webhook changes, and no routing, readiness, assignment or work decision reads
them. Status and report keep `availability_unknown`. People, observers and
operators read them with GET `/api/agent/observations`, limited to the tasks
they can see; agent keys cannot read them, so agents cannot steer on them.
Operators remove observations older than `AGENT_OBSERVATION_RETENTION_DAYS` (30
by default) in bounded batches with POST `/api/agent/observations/cleanup`.

Routing previews and every exact-actor assignment, reassignment, verification,
rework, and recovery command enforce the caller's current topology revision
and runtime-ready membership. A topology change invalidates stale routing
evidence.

### Which actors are runtime-ready, and what a refusal tells you

An actor is runtime-ready when it matches its declared role, scopes, profile
and model bindings, its runtime handoff is issued, its current runtime
acknowledgement (package, profile and model-binding revisions, runtime instance
identity) is recorded, its credential is delivered, it is enabled and active,
and it polled its queue within the topology's
`maximum_runtime_staleness_seconds`. Polling is what keeps an actor present: an
actor that stops polling becomes stale and is no longer ready. `blocker_codes`
name what is missing.

Execution dispatch, rework and recovery depend on the team as it is today: the
actor that receives the work must be runtime-ready, and enforced model-aware
dispatch of execution work needs the whole topology ready.

Verification is judged by the selected verifier. While the whole team is not
ready, a model-aware verification assignment or preview, and the verifier's
verdict, are allowed when

- the verifier is a runtime-ready member of the caller's team;
- the caller is bound to that team and holds every readiness condition except a
  recent poll (a caller that is acting right now need not have polled lately,
  but a disabled, drifted, unacknowledged or not-yet-ready (for example
  onboarding) caller is refused); or the caller
  is bound to no team and has authority over the task's project, in which case
  the verifier's own team is used.

A verifier that is not present, or is outside the caller's team, is still
refused. In `trusted_local` mode with no authority set (the single-user local
mode) a caller bound to no team is treated as having authority over every
project. A verification preview that names no `focus_actor_id` lists every
candidate and keeps the whole-team requirement.

Two refusals say who is missing instead of leaving the cause to be guessed.
`agent_team_actor_outside_topology` (an exact actor that is not a runtime-ready
member) and `model_aware_routing_preview_unavailable` (routing unavailable
because the team is not ready), and for a verification assignment also the
enforced-dispatch refusal, carry:

- `readiness_rule`: the rule above, with the staleness limit in seconds;
- `maximum_runtime_staleness_seconds`;
- `non_ready_actors`: one row per declared actor that is not runtime-ready,
  with `actor_id`, `actor_key`, `role`, `connection_state`, `blocker_codes`,
  `last_seen_at` (its last queue poll), `last_ready_at` and
  `blocks_this_request`.

Only a team the caller belongs to is described, or, for a caller bound to no
team, the verifier's team when the caller has authority over the task's
project. A preview checks the caller's scopes, identity and the task before it
says anything about a team.

`last_ready_at` is the last poll while the actor was otherwise ready. It is set
only when a recent poll is the only thing missing (`runtime_stale`), where it
equals `last_seen_at`; otherwise it is `null` and `blocker_codes` say why.
`blocks_this_request` is true for the actors whose absence caused that
refusal: the exact actor for an assignment, the verifier (and a caller that is
not ready) for a verification preview or assignment, and every non-ready actor
otherwise.

### Read the team and its runtime references

`GET /api/agent/team-setup/topology` and the MCP `agent_get_team_topology` tool
return who is on the team: each member's actor key and ID, name, role, profile,
lifecycle, whether it is runtime-ready, its model binding keys, and its
`runtime_ref`, so a reader can tell which runtime runs which actor. They never
return a `credential_ref`, a handoff or an acknowledgement payload. Agent keys
read on the status rule: an operator any topology, a PM only its bound one.
Without an agent key, people with a workspace role, a trusted-local browser, a
paired observer of such a person, and operators may read it; a project role
alone does not admit a person, because the team is workspace-wide. Pass
`topology_key` to choose a topology; otherwise the first one is returned.

### Drift, adoption, rotation, and rollback

- Safe mutable drift produces an update action.
- An unmanaged actor with the declared stable name produces an explicit
  adoption action; WorkChord does not silently take ownership.
- Immutable identity or uncertain credential state produces a replacement
  action requiring confirmation.
- Identity replacement uses a new stable `actor_name`, `runtime_ref`, and
  `credential_ref`. The previous actor is disabled and retained with its
  assignments, runs, and audit evidence.
- Credential recovery keeps the actor identity but changes only
  `credential_ref` to a new sink reference. This avoids overwriting a
  potentially delivered one-time key whose outcome is uncertain.
- Members omitted from desired state produce disable proposals. Historical
  actors, receipts, assignments, and runs remain intact.
- Package, profile, binding, credential-delivery, acknowledgement, and
  connection drift remain separate status evidence.

#### Move reviewers to the reviewer package

Reviewer members (the `verifier` role) must use the `workchord-reviewer`
package; validation rejects a reviewer that still declares `workchord-pm`. To
upgrade an existing team:

1. Upgrade the server so its skill catalog lists `workchord-reviewer`.
2. In the master, set each reviewer's `skill_package` to the
   `workchord-reviewer` name, version, and archive checksum from that catalog.
3. Validate and plan, review the action proposed for each reviewer, then
   apply it.
4. Install the reviewer package in each reviewer runtime and acknowledge the
   new handoff. Reviewers stay out of dispatch until they acknowledge it.

Until step 3 is applied, a team stored before the upgrade stays readable.
Status reports `stored_contract_outdated` on the topology, on the master step,
and on each member whose stored contract no longer meets the role rules. Those
members get no handoff, cannot acknowledge
(`agent_team_ack_contract_outdated`), and stay out of dispatch; the other
members are unaffected. The plan replaces each outdated contract with an
ordinary update action that keeps the actor, its credential, and its bindings.
After a partial apply, a member whose update was not yet approved keeps its
outdated contract and is still reported this way. A member whose credential
delivery is pending or uncertain is brought up to date by its credential
recovery: on an outdated contract, recovery accepts the new `credential_ref`
together with the role-governed fields (`scope_preset`, `assignment_modes`,
`skill_package`) of the current master, and nothing else.

Export the bounded aggregate setup report through
`GET /api/agent/team-setup/report` or the operator CLI. It contains the topology
revision and digest, lifecycle and current-work counts, reconciliation receipt
counts, blocker codes, and an explicit `availability_unknown` dispatch context.
It contains no member handoffs, runtime endpoints, external references, or
credential values; runtime references are read through the topology read above:

```bash
.venv/bin/python scripts/api_keys/setup_agent_team.py \
  report --topology-key default-agent-team \
  > /secure/operator/agent-team-setup-report.json
```

The report conforms to `agent-team-setup-report-v1`; its generated JSON Schema
is `docs/contracts/agent-team-setup-report-v1.schema.json`. Use `status` when an
authorized operator needs the per-member reconciliation and runtime-handoff
view. Neither projection claims task-contextual availability.

To stop dispatch without erasing history, approve the proposed disable actions
or set the deployment routing mode to `off`. Correct the master or external
runtime, request a fresh plan against the latest topology revision, and apply
only the recovery actions. Never edit topology tables or actor lifecycle state
directly.

### Credential and evidence handling

Do not place API keys, provider credentials, credential values, prompts,
environment dumps, private endpoints containing credentials, or raw logs in a
master, plan, handoff, status payload, screenshot, task, or commit. Protect the
credential sink directory and its backup policy independently from WorkChord.
Setup receipts and events contain only bounded identifiers, revisions,
digests, blocker codes, and non-secret references.

For external model startup, exact assigned execution, fenced recovery, review
and usage evidence, follow the [external runtime guide](external-agent-runtime.md).
