# Self-hosted server acceptance

This profile deploys revision-bound WorkChord artifacts from a clean checkout
with container-backed service analogues and emits a machine-readable acceptance
receipt. It is intended for a self-hosted server that needs a reproducible
installation path without separately provisioned PostgreSQL, signing,
immutable-object, or CAS services.

The profile is deliberately separate from PostgreSQL production qualification.
A passing receipt says `SELF-HOSTED-SERVER-ACCEPTED`; it always also says:

- `accepted_as_production_evidence: false`;
- `accepted_as_zero_human_evidence: false`;
- `production_autonomy_qualified: false`;
- `production_gates_satisfied: false`;
- `production_program_decision: NO-SHIP`.

It cannot be submitted to the G1-G15 status evaluator, production preflight,
cutover, handoff, or closeout commands.

## One-command deployment

Run from a clean Git checkout:

```bash
./scripts/server/accept_self_hosted.sh
```

The command:

1. generates server-local credentials under ignored `.runtime/autonomy/`;
2. renders the base and server Compose files;
3. pulls digest-pinned OpenBao, MinIO, MinIO Client, and Valkey images;
4. builds backend and frontend artifacts with the clean Git revision and
   deterministic artifact digests baked into fixed image files;
5. creates separate PostgreSQL migrator, runtime, and backup identities;
6. starts PostgreSQL, migrations, repair, backend, worker, and frontend;
7. configures an OpenBao Transit Ed25519 key and a short-lived restricted token;
8. creates a MinIO bucket with versioning, default `COMPLIANCE` retention, and
   a bucket-scoped acceptance identity;
9. mounts persistent application, database, evidence, and CAS volumes;
10. enables Valkey append-only persistence;
11. runs `workchord-server-acceptance` and verifies the serialized receipt
    offline against a separate public-key pin written by the signer bootstrap.

The application remains running on `http://127.0.0.1:8080` by default. Put a
TLS reverse proxy on the host in front of that loopback listener for remote
access. Override `WORKCHORD_HTTP_PORT` or `POSTGRES_HOST_PORT` in
`.runtime/autonomy/server.env` before a later run if the host needs different
bindings. A non-loopback plaintext bind is rejected unless
`WORKCHORD_ALLOW_INSECURE_HTTP=true` is set explicitly; that override is only
appropriate on an already protected network. Session cookies are secure by
default and the gateway preserves the reverse proxy's HTTPS scheme. Set
`WORKCHORD_SESSION_COOKIE_SECURE=false` only for loopback-only HTTP access.

Before exposing the loopback listener through a TLS reverse proxy, set exact
MCP transport allowlists in `.runtime/autonomy/server.env`. For example:

```dotenv
MCP_ALLOWED_HOSTS='["workchord.example.com"]'
MCP_ALLOWED_ORIGINS='["https://workchord.example.com"]'
```

Keep `MCP_DNS_REBINDING_PROTECTION=true`. A non-loopback bind is refused while
either MCP allowlist still has its loopback-only default.

The secret-free receipt is written to:

```text
.runtime/autonomy/reports/latest.json
```

Its required signer trust input is written separately to:

```text
.runtime/autonomy/reports/trusted-signer-public-key.b64
```

To verify the latest receipt again without contacting OpenBao:

```bash
docker compose \
  --project-name workchord-server \
  --env-file .runtime/autonomy/server.env \
  -f docker-compose.yml \
  -f docker-compose.server.yml \
  --profile autonomy \
  run --rm --no-deps autonomy-acceptance \
    workchord-server-acceptance \
    --verify-receipt /var/lib/workchord/acceptance/latest.json
```

The command refuses a dirty checkout. The Git revision and content digest are
baked into fixed files in both artifacts and returned by their runtime identity
endpoints. Revisions are cross-checked, the backend digest is compared with the
acceptance container's baked package digest, and both artifact digests enter
the signatures. This binds the predicates to revision-bound artifacts; it is
not an OCI registry digest or a supply-chain attestation.

The signed receipt validity horizon is at most 24 hours and never outlives its
locked evidence. Offline verification is an acceptance result only when the
receipt is still valid and matches the verifier container's baked backend and
frontend identities; an expired receipt is not a current server acceptance.

On a rerun, the prior `latest.json` and its matching signer pin are archived as
a `previous-*` pair before any new work starts. A new `latest.json` is published
atomically only after the pending receipt passes offline verification. Preserve
`.runtime/autonomy/server.env`: if it is missing or has lost any durable secret
while the database volume remains, the launcher refuses to invent replacements
and explains the recovery boundary.

## What is proved

Acceptance performs live checks against the deployed services:

- the backend uses the restricted `workchord_runtime` PostgreSQL login,
  readiness reaches PostgreSQL, the schema is at packaged Alembic head, and no
  migration gate remains open;
- backend, acceptance, and gateway build identities match the source revision,
  the backend package content digest matches the acceptance image, the gateway
  digest matches the frontend artifact independently built into that image,
  the gateway reaches backend liveness, and the wheel-packaged PostgreSQL
  machine contract matches the signed manifest digest;
- OpenBao Transit uses a non-exportable Ed25519 key, signs the candidate and
  final receipt, verifies both through the remote API, and requires the
  bootstrap-produced public-key pin for offline verification;
- MinIO stores the signed candidate under default `COMPLIANCE` retention, reads
  back the exact bytes, attempts deletion of that exact retained version, and
  still returns the same bytes afterward;
- Valkey has append-only persistence enabled, confirms a local AOF fsync, and
  rejects a `SET NX` from an independent connection while preserving the first
  value.

The administrative OpenBao, MinIO, and Valkey ports are attached only to an
internal Docker network. OpenBao and MinIO root credentials are present in
their service daemons and one-shot bootstrap containers, but are withheld from
the acceptance container. The acceptance container receives only restricted
credentials. Generated credentials are not committed.

The worker is started from the same revision-bound backend image, but this
receipt does not claim a delivery heartbeat or a completed outbound delivery.
Its acceptance scope is exactly the predicates listed above.

## Boundary and promotion

OpenBao runs in its automatically initialized, in-memory dev mode, while MinIO
and Valkey are single-node containers; all three remain on the same Docker
host. Existing receipts remain verifiable after an OpenBao restart when their
embedded key matches the separately preserved bootstrap pin. The old signer
cannot issue new receipts. These are useful analogues for signing,
object-retention, and CAS mechanics. They are not managed KMS, independently
operated compliance WORM storage, or an HA journal.

The profile does not establish production IAM, TLS, backup/PITR, provider,
resilience, capacity, independent-review, cutover, stabilization, publication,
or retention-horizon evidence. Use the separate
[PostgreSQL operations guide](postgresql-operations.md) and production evidence
chain for those decisions.

To inspect the running topology:

```bash
docker compose \
  --project-name workchord-server \
  --env-file .runtime/autonomy/server.env \
  -f docker-compose.yml \
  -f docker-compose.server.yml \
  --profile autonomy ps --all
```

To stop containers while preserving database, evidence, and CAS volumes:

```bash
docker compose \
  --project-name workchord-server \
  --env-file .runtime/autonomy/server.env \
  -f docker-compose.yml \
  -f docker-compose.server.yml \
  --profile autonomy down
```
