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
4. Upgrade compatible planner and worker role packages.
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
