# Agent-team setup

WorkChord can reconcile a portable, secret-free agent-team master into one
controller, one or more workers, and optional independent verifiers. The
master declares stable logical actor keys, role scope presets, capability
profiles, provider-neutral model bindings, immutable role-package checksums,
runtime references, and external credential references.

The server remains authoritative for actor IDs, scopes, profile and binding
revisions, lifecycle state, topology revision, and runtime readiness. A
manifest is desired state, not proof that a runtime is connected or available
for a particular task.

## Prerequisites

1. Configure `WORKCHORD_ADMIN_API_KEY`.
2. Create an operator-owned credential sink directory, set its permissions to
   `0700`, and configure `AGENT_TEAM_CREDENTIAL_SINK_DIR`.
3. Set `AGENT_TEAM_CREDENTIAL_SINK_REF` to the non-secret reference prefix used
   by every member in the master.
4. Create and enable the provider-neutral model catalog entries referenced by
   the master. Provider credentials do not belong in the catalog or master.
5. Use immutable package identities from the server's agent skill catalog.

Start from
[`config/examples/agent-team-master.json`](../config/examples/agent-team-master.json).
Replace deployment-specific URLs, runtime references, and model catalog keys.
The JSON Schema is generated at
`docs/contracts/agent-team-master-v1.schema.json`.

## Validate and plan

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

## Apply selected actions

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

## Start and acknowledge runtimes

Each configured member's status includes a secret-free handoff with:

- topology and logical actor keys;
- the resolved server-owned actor ID and role;
- server URL and required features;
- immutable package version and checksum;
- profile and binding revisions;
- supported assignment modes and startup instructions;
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

## Interpret status

`GET /api/agent/team-setup/status` and the MCP
`agent_get_team_setup_status` tool share the same backend-derived projection.
Operators may select a topology; a PM can read only its bound topology.

- `configured` means desired server objects exist.
- `onboarding` means at least one required runtime has not acknowledged its
  exact handoff.
- `runtime_ready` means the controller and required workers are current, with
  an independent verifier ready when the policy requires one.
- `blocked` includes stable blocker codes and an operator next action.
- `connection_state` describes observed freshness.
- `availability_unknown` is intentional. Availability is evaluated only for a
  concrete task, queue, capacity, and model-binding context.

Routing previews and every exact-actor assignment, reassignment, verification,
rework, and recovery command enforce the caller's current topology revision
and runtime-ready membership. A topology change invalidates stale routing
evidence.

## Drift, adoption, rotation, and rollback

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

Export a redacted setup report from the status projection. The result contains
logical keys, server-owned IDs, revisions, readiness evidence, queue counts,
blockers, and external reference names, but no credential values:

```bash
.venv/bin/python scripts/api_keys/setup_agent_team.py \
  status --topology-key default-agent-team \
  > /secure/operator/agent-team-status.json
```

To stop dispatch without erasing history, approve the proposed disable actions
or set the deployment routing mode to `off`. Correct the master or external
runtime, request a fresh plan against the latest topology revision, and apply
only the recovery actions. Never edit topology tables or actor lifecycle state
directly.

## Credential and evidence handling

Do not place API keys, provider credentials, credential values, prompts,
environment dumps, private endpoints containing credentials, or raw logs in a
master, plan, handoff, status payload, screenshot, task, or commit. Protect the
credential sink directory and its backup policy independently from WorkChord.
Setup receipts and events contain only bounded identifiers, revisions,
digests, blocker codes, and non-secret references.
