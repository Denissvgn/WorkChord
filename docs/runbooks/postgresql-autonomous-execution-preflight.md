# PostgreSQL autonomous execution preflight

This runbook describes the repository-side foundation for the autonomous
PostgreSQL migration program. It does not authorize production and does not
replace the separate manual publication process.

## Current boundary

The installed backend contains:

- strict `workchord-postgresql-autonomy-charter-v1` and finite
  `bootstrap-action-manifest-v1` contracts;
- detached remote-signature verification through externally resolved public
  trust anchors, with no private signer in the autonomous package; legacy
  manual file-key signing and file/embedded trust are rejected whenever
  `WORKCHORD_EXECUTION_MODE=zero-human-agent-v1`;
- secret-free `agent-team-master-v1` normalization and non-destructive
  reconciliation;
- source evidence, immutable attempt ancestry, action-lease, external-CAS DAG,
  verifier-package, observation-job, and status-amendment primitives;
- a wheel-included PostgreSQL machine-contract bundle whose ignored source-plan
  snapshots must still be matched to charter-pinned immutable objects;
- deterministic unpublished handoff and closeout evaluators with no release
  destination adapter.

The server does not advertise `model-aware-routing-v1`,
`agent-team-master-v1`, `fenced-verifier-runs-v1`,
`durable-observation-jobs-v1`, or
`autonomous-postgresql-closeout-v1` merely because those primitives exist.
Advertisement is permitted only after every backing REST/MCP/runtime,
identity, journal, evidence, provider, recovery, and adversarial qualification
predicate is live.

## Local diagnostic

From an installed backend environment, run:

```bash
workchord-agent-preflight
```

The command reads only installed package resources and a local Git tree identity
when available. It does not read ignored `docs/plans/`, `docs/adr/`, or
`docs/contracts/` as runtime authority. The current diagnostic supplies no
external charter or source evidence, so it emits a conservative
`BLOCKED_EXTERNAL` / `NO-SHIP` report and exits `2`.

The JSON wrapper has both of these fields:

```json
{
  "accepted_as_autonomy_evidence": false,
  "diagnostic_unsigned": true
}
```

Do not seal, rename, or upload this diagnostic as a passing artifact. An
accepted start report must be built from resolved source evidence and signed by
the charter-selected remote KMS identity.

## Required external inputs

Before an accepted autonomous run can begin, all of the following must exist
outside the interactive repository workflow:

1. an externally signed standing charter and exact finite bootstrap-action
   manifest;
2. a readable revocation source and pinned public trust root;
3. isolated workload identities, independence groups, non-exportable KMS keys,
   a WORM evidence store, and an external HA CAS journal;
4. charter-selected Git/CI/OCI, managed PostgreSQL, deployment, observability,
   backup, DNS, sanitizer, and trusted-clock adapters;
5. exact immutable objects for the source plans and normative contracts;
6. the complete advertised core capability set and two independent passing
   adversarial reconstructions.

Missing inputs remain `BLOCKED_EXTERNAL` or `AUTONOMY-NOT-READY`. They never
trigger an interactive approval, a local private-key fallback, or inferred
provider/production authority.

## Separate self-hosted server acceptance

The [self-hosted server acceptance profile](self-hosted-server-acceptance.md)
provides a smaller installation check backed by PostgreSQL, OpenBao Transit,
MinIO object retention, and Valkey CAS containers. It emits its own schema and
never creates `SignedAutonomousEvidence`, `VerifiedPreflightArtifact`, status
evidence, or a production handoff.

Its successful decision is limited to `SELF-HOSTED-SERVER-ACCEPTED`. The
receipt always retains `NO-SHIP`, does not qualify production autonomy, and
does not satisfy G1-G15.

## Publication handoff

The deterministic handoff bundle is immutable and always labels itself
`NOT-PUBLISHED` and `MANUAL-PUBLICATION-REQUIRED`. Candidate capacity wording is
limited to 1,250 opaque browser identities, 250 active browser sessions, and
200 concurrent MCP/agent clients. It never restates that as 1,250 authenticated
people. A 99.9% availability statement remains unavailable until a complete
passing 30-day observation is source-attested.

Only a current, independently signed `READY-FOR-MANUAL-PUBLICATION` decision and
its exact verified handoff may be exposed to the separate manual process. No
agent in this program can publish, announce, overwrite public documents, or
close DBM-DOC-002/G15.
