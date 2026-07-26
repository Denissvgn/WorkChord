# SQLite-to-PostgreSQL cutover, rollback, and stop conditions

This DBM-CUT-001 runbook is a production mutation checklist, not production
authorization. Execute it first in a timed tabletop and then in the required
rehearsals. Preserve every command result and checksummed artifact. Copy
`postgresql-cutover-checklist.md` into the approved evidence system and use it
as the signed timer, authority, gate, go/no-go, and point-of-no-return record.
Encode that reviewed record with the installed `workchord-db-cutover` workflow
in `postgresql-rehearsal-cutover-evidence.md`; the command records evidence and
never performs or authorizes a database or deployment mutation.

## Named authority and immutable inputs

Before T-7 days, record named people for change commander, database operator,
application operator, observer/evidence recorder, product owner, and incident
commander. Only the change commander calls go/no-go. Only the product owner may
accept the downtime budget. The database operator independently confirms every
resolved target before a destructive platform operation.

Freeze these secret-free identifiers in the change record:

- source SQLite file identity and deployment/release;
- application image digest and migration CLI version;
- source manifest/snapshot SHA-256;
- PostgreSQL `host:port/database`, managed resource ID, exact version, locale,
  storage, and current recovery point;
- maintenance revision and expected replica set;
- gateway/upstream release and DNS names;
- evidence directory/change ID.

Required green inputs are CI, schema/dialect/concurrency/maintenance suites,
capacity qualification, security grant/TLS/rotation rehearsal, a valid
backup/PITR restore drill, loader benchmark/capacity evidence, two successful
migration rehearsals after a separate abort drill, and operator walkthrough.

## Time budget

| Gate | Target | Hard stop |
| --- | ---: | ---: |
| Fence, drain, snapshot | 20 min | 35 min |
| Target bootstrap and load | 45 min | 75 min cumulative |
| Raw reconcile, repairs, final reconcile | 30 min | 120 min cumulative |
| Switch, validation smoke, go/no-go | 20 min | 150 min cumulative |
| Contingency before forced abort | 30 min | 180 min total |

The observer starts and records each timer. Crossing a hard stop is an abort,
not an invitation to improvise.

## Cutover checklist

1. **T-60 minutes — announce and freeze change.** Confirm incident channel,
   status communication, operator access, image/report checksums, target IDs,
   latest valid PostgreSQL recovery point, and 180-minute hard-stop alarm.
2. **Fence every writer.** Restart all web replicas with
   `MAINTENANCE_MODE=validation-only`, one explicit
   `MAINTENANCE_REVISION`, and `MAINTENANCE_REPLICA_ID=auto`. Stop all workers,
   schedulers, migration jobs, shell sessions, and old releases that own the
   SQLite file.
3. **Prove drain.** Fetch `/health/ready` from every replica. Require one
   fingerprint, unique replica IDs, zero active mutations/transactions/worker
   jobs/leases, and `writer_drain.drained=true`. The controller independently
   proves zero source connections. Seal writer-drain evidence.
4. **Snapshot and preflight.** Run the exact preflight command in
   `sqlite-to-postgresql-migration.md`. Fsync the snapshot and evidence
   filesystem. Independently compare the snapshot and manifest checksums with
   the change record.
5. **Confirm recovery.** Record the frozen SQLite snapshot as the pre-write
   rollback source. Confirm the PostgreSQL target's latest base backup/PITR
   point and backup-system health. Stop if either backup boundary is invalid.
6. **Resolve and bootstrap target.** Two operators compare the migration CLI's
   `target-identity` with the managed resource ID/change record. The loader does
   not reset a nonempty target. If rehearsal policy calls for target deletion,
   perform it only in platform tooling after both operators resolve the exact
   nonproduction target; then recreate and run schema-only bootstrap.
7. **Load.** Seal target-capacity and loader-method evidence, then run the
   catalogued loader. Preserve its report. A partial failure remains closed and
   may resume only with the same source manifest and target gate.
8. **Raw reconciliation.** Run raw reconciliation. Require every table count
   and digest, FK/constraint, sequence, secret, domain read, and statistics gate
   to pass. Do not run repairs before this report passes.
9. **Repairs and second reconciliation.** Run the dedicated repair role, record
   its exact hash-only mutations, and run final reconciliation. Require zero
   unexplained differences and gate status `reconciled`.
10. **Switch configuration while still fenced.** Deploy two web and two worker
    replicas with the approved `DATABASE_RUNTIME_URL`, verified TLS, runtime
    role, pool budgets, and the same validation-only revision. Keep the SQLite
    snapshot inaccessible to application writers.
11. **Validation smoke.** Require readiness on every web replica; exercise
    public DNS/TLS/gateway health, representative REST and MCP reads, preserved
    browser sessions, agent key lookup, assignments/runs, task/dependency
    trees, queue state, and a rollback-only transaction/sequence probe. Remove
    one web replica and prove bounded reroute. Confirm database/log/metric
    secret scans and SLO/error/connection limits.
12. **Go/no-go before writes.** The observer reads every stop condition and
    evidence checksum. Database and application operators sign their gates.
    The change commander records `GO` or calls rollback.
13. **Reopen writes — point of no return.** Deploy `MAINTENANCE_MODE=off`, start
    workers, and require all replica fingerprints/readiness to agree. The first
    accepted PostgreSQL application write is the point of no return. Record its
    timestamp/correlation ID and begin stabilization monitoring.

All source snapshot, target bootstrap, load, reconciliation, and repair
commands are executed from the repository root exactly as published in
`sqlite-to-postgresql-migration.md`. Deployment, backup, restore, maintenance,
and troubleshooting prerequisites are indexed in `postgresql-operations.md`.
Run each command's `--help` from the frozen released artifact during the
pre-cutover walkthrough; a flag/path difference is a stop condition, not an
operator improvisation.

## Mandatory stop conditions

Stop immediately for SQLite integrity/FK/orphan failure; unknown table/column
or Alembic revision; source/WAL change; missing replica or fingerprint drift;
nonzero writer/transaction/lease; unauthorized or nonempty target; target
version/locale/timezone/search-path/TLS/grant mismatch; insufficient
data/index/temp/WAL/archive capacity; load/checkpoint/sequence failure;
unexplained count/digest/reference/invariant/repair difference; failed secret
decryption; stale planner statistics; failed readiness/session/agent/queue/API
smoke; gateway/database SLO failure; invalid backup/archive lag; operator or
timer uncertainty; or any unreviewed command deviation.

## Rollback before writes reopen

1. Keep maintenance fencing active and workers stopped. Announce abort and
   preserve the failed target/gate/report evidence.
2. Resolve the frozen snapshot checksum again and reopen it read-only for
   `integrity_check`, revision, and manifest comparison.
3. Restore the approved SQLite configuration/release with
   `DATABASE_POSTGRESQL_REQUIRED=false` only for this authorized rollback.
   Point it at a new operator-owned copy made through SQLite backup/restore,
   never the evidence artifact itself.
4. Start one fenced SQLite web replica, pass readiness and representative read
   smoke, then expand replicas only according to the pre-migration SQLite
   topology. SQLite must not be used by multiple write-capable replicas.
5. Lift the fence only after change-commander sign-off. Demonstrate service
   restoration within the 30-minute rollback budget and retain PostgreSQL
   closed for investigation.

## Recovery after writes reopen

There is no reverse synchronization. Never switch back to SQLite after the
first PostgreSQL write. Fence writes, declare an incident, and recover forward
on PostgreSQL through failover, PITR, or an isolated validated restore. Preserve
the frozen SQLite snapshot only as historical evidence.

Stabilization monitors readiness, errors, latency, connections, locks,
deadlocks, queue depth/age, WAL/archive/replication lag, storage/I/O,
autovacuum/analyze, bloat, backup duration, and integrity. Monthly 99.9%
availability is claimable only after the full 30-day client/gateway SLI window.
Publish the actual release boundary and run the independent closure audit with
the [post-cutover workflow](postgresql-postcutover-release-and-closeout.md);
the production cutover record alone is not a SHIP decision.
