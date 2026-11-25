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
3. pulls digest-pinned OpenBao, Versity S3 Gateway, AWS CLI, and Valkey images;
4. builds backend and frontend artifacts with the clean Git revision and
   deterministic artifact digests baked into fixed image files;
5. creates separate PostgreSQL migrator, runtime, and backup identities;
6. starts PostgreSQL, migrations, repair, backend, worker, and frontend;
7. configures an OpenBao Transit Ed25519 key and a short-lived restricted token;
8. starts the Versity S3 Gateway evidence store on a persistent volume, creates
   a bucket with object lock, versioning, and default `COMPLIANCE` retention,
   and grants a separate acceptance identity only the object actions a bucket
   policy names;
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

## Evidence store

The signed evidence lives in the `workchord-server-acceptance` bucket of a
single-node [Versity S3 Gateway](https://github.com/versity/versitygw)
(`evidence-store`), which serves the S3 API over a POSIX directory on the
`workchord_autonomy_evidence` volume. Two one-shot jobs configure it on every
run, and both are safe to repeat:

- `evidence-store-accounts` creates or updates the acceptance identity with
  the gateway's plain `user` role, which cannot create, list, configure, or
  delete buckets;
- `evidence-store-bootstrap` creates the bucket with object lock (which also
  enables versioning), sets the default `COMPLIANCE` retention, applies
  `deploy/autonomy/evidence-store-acceptance-policy.json` with the acceptance
  identity as its only principal, and checks that versioning, retention, and
  the refusal of anonymous requests are in place.

The default retention is one day. Set `AUTONOMY_EVIDENCE_RETENTION_DAYS` to a
larger whole number of days to keep evidence longer; a receipt never outlives
its locked evidence. While retained, an evidence version cannot be deleted or
have its retention shortened through the S3 API, even with the root identity.

The evidence-store credentials are not bound to stored data: the gateway takes
its root identity at startup and the accounts job re-applies the acceptance
identity. They are therefore not among the durable values the launcher
protects.

Earlier releases used MinIO, whose images are no longer published, and named
these settings `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`,
`AUTONOMY_MINIO_ACCESS_KEY`, `AUTONOMY_MINIO_SECRET_KEY`, and
`AUTONOMY_MINIO_RETENTION`. The launcher drops those names and generates
`EVIDENCE_STORE_ROOT_ACCESS_KEY`, `EVIDENCE_STORE_ROOT_SECRET_KEY`,
`AUTONOMY_EVIDENCE_ACCESS_KEY`, and `AUTONOMY_EVIDENCE_SECRET_KEY` when it
rewrites `server.env`. To migrate a `server.env` before running Docker Compose
by hand, for example for the commands below:

```bash
python3 scripts/server/seed_adoption_env.py \
  --migrate-env .runtime/autonomy/server.env
```

It replaces the MinIO entries in place, keeps every other line, never prints a
value, and leaves a file that needs no migration unchanged. A former
`AUTONOMY_MINIO_RETENTION` value is not carried over; set
`AUTONOMY_EVIDENCE_RETENTION_DAYS` instead. Evidence stored by MinIO stays in
the old `workchord_autonomy_minio` volume, which the new store does not read.
Remove that volume once its retention has expired and no receipt depends on it.

## Adopting a running instance

To move an already running Compose project and its database into this layout,
follow [Adopting a running instance](self-hosted-adoption.md). It uses two
optional inputs of this script: `WORKCHORD_CREDENTIAL_SINK_HOST_DIR` mounts a
private host directory as the backend's credential sink (through
`docker-compose.credential-sink.yml`), and `WORKCHORD_MIGRATION_BACKUP_REFERENCE`
names the verified recovery point that an existing database needs before its
migration. After a run, `scripts/server/write_deployment_record.py` writes a
record that names every service's image.

## Retained public artifacts

The deployment acceptance workflow retains public artifacts for 14 days,
including on failure. Its validated staging directory contains the latest
receipt, up to eight prior receipts, their associated Ed25519 public pins,
an exact candidate and SHA-256 checksum index, and a sanitized status summary.
Environment files, credentials, private keys, session state and runtime logs
are excluded. Invalid or oversized receipt files are rejected. A missing
required receipt or failed run remains failure evidence.

After downloading and unpacking the artifact, use the matching installed
backend to verify its membership, checksums, signatures and current latest
receipt build identity:

```bash
workchord-server-acceptance \
  --verify-exported-artifacts /path/to/downloaded-public-artifacts \
  --trusted-signer-public-key-file /path/to/independently-preserved-public-pin.b64
```

Preserve the trust pin independently through a trusted signer bootstrap or
owner-controlled channel. A key bundled beside a receipt establishes its
association, not its authority; the verifier refuses a trust input inside the
downloaded directory. Prior receipts are archival signature evidence, while
the latest receipt must remain valid and match the verifier's baked build.
The unsigned archive index provides byte integrity rather than a separate
attestation of the hosted job. Public artifact verification retains the same
non-production acceptance boundary.

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
- the evidence store keeps the signed candidate under default `COMPLIANCE`
  retention, reads back the exact bytes, refuses deletion of that exact
  retained version, and still returns the same bytes afterward;
- Valkey has append-only persistence enabled, confirms a local AOF fsync, and
  rejects a `SET NX` from an independent connection while preserving the first
  value.

The administrative OpenBao, evidence-store, and Valkey ports are attached only
to an internal Docker network. OpenBao and evidence-store root credentials are
present in their service daemons and one-shot bootstrap containers, but are
withheld from the acceptance container. The acceptance container receives only restricted
credentials. Generated credentials are not committed.

The worker is started from the same revision-bound backend image, but this
receipt does not claim a delivery heartbeat or a completed outbound delivery.
Its acceptance scope is exactly the predicates listed above.

## Boundary and promotion

OpenBao runs in its automatically initialized, in-memory dev mode, while the
evidence store and Valkey are single-node containers; all three remain on the same Docker
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
