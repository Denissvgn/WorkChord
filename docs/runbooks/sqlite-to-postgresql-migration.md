# SQLite-to-PostgreSQL data migration

This runbook covers DBM-DATA-001 through DBM-DATA-003. It does not authorize a
production change. Production operators execute these commands only through
the cutover runbook and preserve every checksummed JSON artifact.

## Safety model

- `workchord-db-migrate preflight` opens the source read-only and creates the
  artifact with SQLite's backup API. A bare online file copy is unsupported.
- Writer-drain evidence must be less than 15 minutes old, include every
  replica, use one maintenance revision/fingerprint, report zero active
  writers and leases, and confirm that the controller stopped all SQLite
  owners.
- The source and its WAL identities are checked before and after backup. The
  snapshot is fsynced, reopened read-only, and fully inspected.
- The PostgreSQL loader accepts only the exact packaged Alembic head and an
  empty target whose secret-free identity exactly matches
  `--authorize-target`.
- The target-owned `database_migration_gates` row makes readiness fail from the
  first committed load checkpoint until final reconciliation passes.
- A table is one restart unit. Rows are read and inserted in bounded chunks,
  but the table and its checkpoint commit together. Nullable cyclic references
  are restored only after all parent tables exist.
- The source is never repaired automatically. An anomaly stops the run before
  PostgreSQL mutation.

## Prepare checksummed evidence

Copy `scripts/database_migration/writer-drain-evidence.example.json`, replace
its placeholder readiness fields with the exact payload from every replica,
and set `captured_at` immediately before sealing it:

~~~bash
cd backend
.venv/bin/workchord-db-migrate seal-document \
  --input ../reports/migration/writer-drain.raw.json \
  --output ../reports/migration/writer-drain.json
~~~

Never put a database URL, password, certificate key, API token, setting
plaintext, source path, or row value in evidence JSON.

## Snapshot and source preflight

Resolve `SOURCE_DB`, `SNAPSHOT_DB`, and `EVIDENCE_DIR` to absolute paths owned
by the migration operator. The snapshot and manifest paths must not already
exist.

~~~bash
cd backend
.venv/bin/workchord-db-migrate preflight \
  --source "$SOURCE_DB" \
  --snapshot "$SNAPSHOT_DB" \
  --writer-drain-evidence "$EVIDENCE_DIR/writer-drain.json" \
  --manifest "$EVIDENCE_DIR/source-manifest.json"
~~~

Preflight checks the exact table and column inventory, Alembic revision,
`PRAGMA integrity_check`, `PRAGMA foreign_key_check`, explicit FK orphan
queries, primary/unique keys, Boolean ranges, UTC timestamps, dates, native and
text JSON, encrypted-setting shape, target-owned table emptiness, counts, and
canonical SHA-256 digests. It also records estimated bytes, duration, and the
minimum free-space budget.

Stop if the command exits 2. Repair only a copy under an independently reviewed
and versioned rule; then repeat maintenance/drain, snapshot, and preflight from
the beginning.

## Bootstrap and authorize the target

Use the dedicated migrator login. `DATABASE_SESSION_ROLE` is the NOLOGIN owner
role granted only to the migrator. Production requires verified TLS.

~~~bash
cd backend
DATABASE_PROCESS_ROLE=migration \
DATABASE_POOL_SIZE=1 \
DATABASE_MAX_OVERFLOW=0 \
DATABASE_SESSION_ROLE=workchord_owner \
.venv/bin/python -m app.cli.upgrade --schema-only

TARGET_ID=$(.venv/bin/workchord-db-migrate target-identity)
printf 'Resolved target: %s\n' "$TARGET_ID"
~~~

An independent operator compares `TARGET_ID` with the approved change record.
Do not paste a URL; the identifier is `host:port/database` and contains no
credentials.

Copy and fill the target-capacity and loader-method examples. Capacity evidence
must cover data, indexes, temporary space, WAL, and archive space. Loader
method evidence records the production-shaped `COPY FROM STDIN` versus bounded
insert benchmark and the approved outage/WAL/restart tradeoff. Seal both with
`seal-document`. Production loading refuses to run without them.

## Load

~~~bash
cd backend
.venv/bin/workchord-db-migrate load \
  --snapshot "$SNAPSHOT_DB" \
  --manifest "$EVIDENCE_DIR/source-manifest.json" \
  --report "$EVIDENCE_DIR/load-report.json" \
  --authorize-target "$TARGET_ID" \
  --capacity-evidence "$EVIDENCE_DIR/target-capacity.json" \
  --loader-method-evidence "$EVIDENCE_DIR/loader-method.json" \
  --chunk-size 1000
~~~

The loader preserves primary keys, converts declared Boolean/date/time/JSON
types, stages nullable references, repairs all owned sequences, runs `ANALYZE`,
and keeps credentials out of output. A process failure leaves the gate failed;
rerunning the same command verifies completed-table row counts and resumes at
the next table. A different manifest or target identity is refused.

## Raw reconciliation, repairs, and final reconciliation

~~~bash
cd backend
.venv/bin/workchord-db-migrate reconcile \
  --phase raw \
  --snapshot "$SNAPSHOT_DB" \
  --manifest "$EVIDENCE_DIR/source-manifest.json" \
  --report "$EVIDENCE_DIR/reconcile-raw.json" \
  --authorize-target "$TARGET_ID"

DATABASE_PROCESS_ROLE=repair \
DATABASE_POOL_SIZE=1 \
DATABASE_MAX_OVERFLOW=0 \
DATABASE_SESSION_ROLE=workchord_owner \
.venv/bin/workchord-db-migrate repairs \
  --manifest "$EVIDENCE_DIR/source-manifest.json" \
  --report "$EVIDENCE_DIR/post-copy-repairs.json" \
  --authorize-target "$TARGET_ID"

.venv/bin/workchord-db-migrate reconcile \
  --phase final \
  --snapshot "$SNAPSHOT_DB" \
  --manifest "$EVIDENCE_DIR/source-manifest.json" \
  --raw-report "$EVIDENCE_DIR/reconcile-raw.json" \
  --repair-report "$EVIDENCE_DIR/post-copy-repairs.json" \
  --report "$EVIDENCE_DIR/reconcile-final.json" \
  --authorize-target "$TARGET_ID"
~~~

Raw reconciliation requires identical counts and canonical digests for every
transfer table, valid constraints, collision-safe sequences, current planner
statistics, matching domain reads, and successful decryption of every secret
setting with `SETTINGS_ENCRYPTION_KEY`. Repairs are restricted to the versioned
seed/settings table catalog; the report contains only primary-key and row
hashes. Final reconciliation accepts exactly those recorded transformations
and zero unexplained differences. Only then does the gate become `reconciled`.

Store the snapshot read-only and store all JSON reports by their SHA-256 in the
change record. Do not reopen writes merely because the final command passed;
the cutover commander owns that decision.
