# PostgreSQL rehearsal and cutover evidence

This DBM-REHEARSE-001/DBM-CUT-002 guide turns the signed operator checklist
into machine-verifiable evidence. The installed `workchord-db-cutover` command
**records and verifies evidence only**. It never connects to PostgreSQL,
SQLite, an application endpoint, or a deployment control plane and never
authorizes a mutation by itself. Operators still execute the frozen
[cutover runbook](sqlite-to-postgresql-cutover.md) under the approved change.

Do not start a rehearsal until the trusted, signed DBM-QUAL-001 report proves
three complete production-shaped runs and the independent DBM-DOC-001
walkthrough is current for the same release. Do not start production until the
separate abort drill and two consecutive full rehearsals have been signed and
the production authorization window is open.

## Evidence and trust boundary

Run every command from the exact installed backend wheel. Preserve the wheel
hash and output of:

```bash
.venv/bin/workchord-db-cutover --help
.venv/bin/workchord-db-cutover verify --help
```

The coordinator accepts Ed25519 signatures only when the caller supplies the
independently provisioned public key with the matching `--*-public-key` flag.
An embedded public key is never its own trust proof. Record every trusted
public-key SHA-256 in the change system before the window. Keep private keys
outside this repository and evidence directory, set their mode to `0600`, and
use `WORKCHORD_CUTOVER_SIGNING_PASSWORD` only when the approved private key is
encrypted.

Use separate approved signer roles for qualification, the independent
documentation walkthrough, rehearsal evidence, production authorization, and
the production change record. The same person or key must not silently satisfy
independent-review boundaries.

Generated documents are checksummed, signed where they become a release gate,
created with mode `0600`, and never overwritten. Move them to the immutable
change/evidence store and verify them again there. The local
`reports/qualification/database/` directory is a workspace, not evidence.

No JSON input may contain a password, token, cookie, API key, private key, DSN,
database URL, connection URL, authorization header, or credential-bearing URL.
Use only the secret-free `host:port/database`, managed resource ID, hash, and
deployment identities already required by the operator checklist.

## 1. Sign the independent documentation walkthrough

Create an unsealed JSON object with kind
`workchord-postgresql-documentation-walkthrough`, schema version `1`, a unique
`walkthrough_id`, UTC `completed_at`, status `passed`, and the exact frozen
release reference. `reviewer` contains a named identity and
`independent: true`. `unresolved_steps` must be empty. `evidence_sha256` is a
nonempty unique list of hashes from the clean-environment walkthrough.

The `checks` object must contain exactly these values, all set to `passed`:

- `clean_install`, `source_preflight`, and `target_bootstrap_and_copy`;
- `rollback_before_first_write` and `forward_recovery_after_first_write`;
- `backup_restore`, `validation_smoke`, and `released_command_help`;
- `stop_condition_tabletop`.

Then sign it:

```bash
.venv/bin/workchord-db-cutover attest-documentation \
  --input '<reviewed>/documentation-walkthrough.json' \
  --release-manifest '<immutable>/frozen-release.json' \
  --signing-key '<signer>/documentation-ed25519-private.pem' \
  --signer '<independent reviewer identity>' \
  --output '<immutable-handoff>/documentation-walkthrough.signed.json'

.venv/bin/workchord-db-cutover verify \
  --report '<immutable-handoff>/documentation-walkthrough.signed.json' \
  --trusted-public-key '<trust-store>/documentation-ed25519-public.pem'
```

Any later release, schema, pool, query/index, topology, migration, recovery, or
runbook change invalidates this document.

## 2. Record the abort drill and full rehearsals

For each attempt, copy the signed
[operator checklist](postgresql-cutover-checklist.md) into the change system
and create an unsealed JSON execution record conforming to the
[cutover execution v1 schema](../../backend/app/database_migration/postgresql-cutover-execution-v1.schema.json).
The Python validator is the semantic authority when JSON Schema cannot express
ordering, timing, or cross-document identity rules.

Every execution binds:

- the frozen release fingerprint, manifest SHA-256, full commit, and at least
  three digest-pinned images;
- the trusted qualification and documentation report SHA-256 values;
- exact secret-free source deployment/SQLite/revision/snapshot/manifest and
  PostgreSQL target/resource/revision identities;
- all six named authorities and C01-C13 gate observations;
- the go/no-go decision, point-of-no-return observation, timing, smoke,
  rollback/recovery, reconciliation, and final evidence index.

Gate owner identities must match the checklist: C01/C12/C13 change commander;
C02/C10/C11 application operator; C03/C08 observer; and C04-C07/C09 database
operator. Completed gates need UTC start/end times and a SHA-256 evidence
reference. `not_started` fields are all null.

The deliberate abort drill uses `environment: rehearsal`,
`mode: abort_drill`, and `sequence_number: 0`. It has a passed prefix, exactly
one `abort` at C02-C12, and a `not_started` suffix. It must prove no PostgreSQL
application write, rollback to sole-writable SQLite in at most 30 minutes,
closed PostgreSQL, critical smoke, and change-commander sign-off.

Successful rehearsals use `mode: full` and sequence numbers `1` then `2`.
Every C01-C13 gate passes, the pre-write `GO` occurs after C12 and before C13,
the first accepted PostgreSQL write is observed inside C13, SQLite remains
frozen read-only, PostgreSQL is sole writable, and critical/steady/burst smoke
passes. Downtime is derived from C02 through C13 and cannot exceed 180 minutes;
the recorded restore RTO cannot exceed 30 minutes. Any nonempty `manual_steps`
or `deviations`, unexplained reconciliation difference, failed attempt, or
runbook edit resets the two-success count.

Seal and finalize each record without overwriting it:

```bash
.venv/bin/workchord-db-cutover seal-execution \
  --input '<reviewed>/execution.json' \
  --output '<immutable-handoff>/execution.sealed.json'

.venv/bin/workchord-db-cutover finalize-rehearsal \
  --execution '<immutable-handoff>/execution.sealed.json' \
  --release-manifest '<immutable>/frozen-release.json' \
  --qualification-report '<immutable>/postgresql-precutover-qualification.json' \
  --qualification-public-key '<trust-store>/qualification-ed25519-public.pem' \
  --documentation-walkthrough '<immutable>/documentation-walkthrough.signed.json' \
  --documentation-public-key '<trust-store>/documentation-ed25519-public.pem' \
  --signing-key '<signer>/rehearsal-ed25519-private.pem' \
  --signer '<rehearsal evidence owner>' \
  --output '<immutable-handoff>/rehearsal-report.signed.json'
```

After the separate abort report and two full reports exist:

```bash
.venv/bin/workchord-db-cutover finalize-rehearsal-series \
  --abort-report '<immutable>/abort-report.signed.json' \
  --rehearsal-report '<immutable>/rehearsal-1.signed.json' \
  --rehearsal-report '<immutable>/rehearsal-2.signed.json' \
  --rehearsal-public-key '<trust-store>/rehearsal-ed25519-public.pem' \
  --signing-key '<signer>/rehearsal-ed25519-private.pem' \
  --signer '<rehearsal evidence owner>' \
  --output '<immutable-handoff>/rehearsal-series.signed.json'
```

The series signature includes the explicit no-omission attestation. It refuses
a missing abort drill, anything other than full sequence `1, 2`, overlapping
attempts, a release/evidence mismatch, or an untrusted rehearsal key.

## 3. Authorize the bounded production change

Production authorization is a separate signed intent, not a command-line
token. Create an unsealed object with kind
`workchord-postgresql-production-cutover-authorization`, schema version `1`,
status `authorized`, unique authorization/change IDs, `created_at`, a
`valid_from`/`expires_at` window of at most seven days, and the exact release,
qualification, documentation, rehearsal-series, source-scope, target, and six
authority identities.

Its `decision` is exact: `approved: true`, `downtime_budget_minutes: 180`,
`rollback_before_first_write: true`, `reverse_sync_available: false`,
`sqlite_retention: read_only`, and an immutable approval evidence SHA-256.
Sign it only after the intended target is independently resolved:

```bash
.venv/bin/workchord-db-cutover authorize-production \
  --intent '<reviewed>/production-intent.json' \
  --release-manifest '<immutable>/frozen-release.json' \
  --qualification-report '<immutable>/postgresql-precutover-qualification.json' \
  --qualification-public-key '<trust-store>/qualification-ed25519-public.pem' \
  --documentation-walkthrough '<immutable>/documentation-walkthrough.signed.json' \
  --documentation-public-key '<trust-store>/documentation-ed25519-public.pem' \
  --rehearsal-series '<immutable>/rehearsal-series.signed.json' \
  --rehearsal-public-key '<trust-store>/rehearsal-ed25519-public.pem' \
  --signing-key '<approver>/authorization-ed25519-private.pem' \
  --signer '<production change approver>' \
  --output '<immutable-handoff>/production-authorization.signed.json'
```

The tool refuses an expired window, identity mismatch, missing dependency, or
self-asserted signer key. Record the signed authorization SHA-256 in the
production execution record before sealing it.

## 4. Finalize production only after the observed first write

Execute the approved cutover runbook. The production execution record uses
`environment: production`, `mode: full`, and the exact authorization SHA-256.
All gates pass. The authorization must predate C01 and cover its start. Source
scope, target, release, and operator identities must equal the authorization.

Do not finalize on configuration deployment alone. C13 records the first
accepted PostgreSQL application write with UTC time, correlation/command ID,
writer identity, observer, and change commander. The outcome must prove zero
unexplained differences, critical smoke, PostgreSQL sole-writable, SQLite
frozen read-only, writes reopened after sign-off, and stabilization started.

```bash
.venv/bin/workchord-db-cutover seal-execution \
  --input '<reviewed>/production-execution.json' \
  --output '<immutable-handoff>/production-execution.sealed.json'

.venv/bin/workchord-db-cutover finalize-production \
  --execution '<immutable-handoff>/production-execution.sealed.json' \
  --release-manifest '<immutable>/frozen-release.json' \
  --qualification-report '<immutable>/postgresql-precutover-qualification.json' \
  --qualification-public-key '<trust-store>/qualification-ed25519-public.pem' \
  --documentation-walkthrough '<immutable>/documentation-walkthrough.signed.json' \
  --documentation-public-key '<trust-store>/documentation-ed25519-public.pem' \
  --rehearsal-series '<immutable>/rehearsal-series.signed.json' \
  --rehearsal-public-key '<trust-store>/rehearsal-ed25519-public.pem' \
  --authorization '<immutable>/production-authorization.signed.json' \
  --authorization-public-key '<trust-store>/authorization-ed25519-public.pem' \
  --signing-key '<recorder>/production-record-ed25519-private.pem' \
  --signer '<production evidence recorder>' \
  --output '<immutable-handoff>/production-cutover.signed.json'

.venv/bin/workchord-db-cutover verify \
  --report '<immutable-handoff>/production-cutover.signed.json' \
  --trusted-public-key '<trust-store>/production-record-ed25519-public.pem'
```

The completed report is the DBM-CUT-002 machine record, not DBM-CLOSE-001.
Continue stabilization, backup/restore, integrity, documentation, and the
30-day availability observation exactly as the cutover and operations
runbooks require. If failure occurs after the recorded first PostgreSQL write,
fence writes and recover forward on PostgreSQL; never reopen SQLite.

Use the signed production record as the mandatory input to the
[post-cutover release and closeout workflow](postgresql-postcutover-release-and-closeout.md).
It is not valid to publish intended versions or close the contract from this
pre-cutover guide alone.
