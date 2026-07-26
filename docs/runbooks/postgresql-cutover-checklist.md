# PostgreSQL cutover operator checklist

Copy this checklist into the approved change/evidence system for each tabletop,
abort drill, rehearsal, and production change. The copy is the signed record;
this repository template is not evidence or authorization. Execute the full
[cutover runbook](sqlite-to-postgresql-cutover.md) and keep all times in UTC.
After review, encode C01-C13 with the
[signed evidence workflow](postgresql-rehearsal-cutover-evidence.md). The
machine record supplements this checklist; it does not replace named authority
or authorize production.

## Immutable change record

| Field | Resolved value or evidence SHA-256 | Independently confirmed by |
| --- | --- | --- |
| Change ID and environment |  |  |
| Release commit and backend/frontend/gateway image digests |  |  |
| Source deployment, absolute SQLite identity, and source revision |  |  |
| Frozen snapshot and source-manifest SHA-256 |  |  |
| PostgreSQL `host:port/database` and managed resource ID |  |  |
| PostgreSQL build, locale/collation, UTC, schema/search path |  |  |
| Storage, connection, TLS, DNS/failover, monitoring contract |  |  |
| Latest valid backup/PITR recovery point and restore-drill report |  |  |
| Maintenance revision, fingerprint, and expected replicas |  |  |
| Qualification report and two rehearsal report SHA-256 values |  |  |
| Evidence directory/change-system identity |  |  |

## Named authority

| Authority | Name/ID | Signed at |
| --- | --- | --- |
| Change commander; sole go/no-go caller |  |  |
| Product owner; downtime-budget acceptance |  |  |
| Database operator; destructive-target confirmation |  |  |
| Application operator |  |  |
| Observer/evidence recorder; timer owner |  |  |
| Incident commander |  |  |

## Timed gate record

Record `PASS`, `ABORT`, or `NOT STARTED`; never use a partial/waived state.
Every evidence reference is immutable and checksummed.

| Gate | Owner | Target / cumulative hard stop | Start | End | Status | Evidence SHA-256 / signed decision |
| --- | --- | ---: | --- | --- | --- | --- |
| C01 announce, freeze identities, confirm authority | Change commander | T-60 / 0 min |  |  |  |  |
| C02 deploy `validation-only` to every replica; stop workers/SQLite owners | Application operator | 10 / 10 min |  |  |  |  |
| C03 prove complete replica agreement and zero writer/transaction/job/lease/connection drain | Observer | 10 / 20 min |  |  |  |  |
| C04 backup-API snapshot, fsync, manifest, read-only source preflight | Database operator | 15 / 35 min |  |  |  |  |
| C05 confirm frozen SQLite and PostgreSQL PITR recovery boundaries | Database operator | included / 35 min |  |  |  |  |
| C06 independently resolve and schema-bootstrap the empty PostgreSQL target | Database operator | 15 / 50 min |  |  |  |  |
| C07 catalogued load with sealed capacity/loader evidence | Database operator | 25 / 75 min |  |  |  |  |
| C08 raw reconciliation | Observer | 15 / 90 min |  |  |  |  |
| C09 post-copy repair, final reconciliation, sequence/statistics checks | Database operator | 30 / 120 min |  |  |  |  |
| C10 switch all services to approved PostgreSQL URLs while fenced | Application operator | 10 / 130 min |  |  |  |  |
| C11 direct/public readiness, REST/MCP/session/agent/queue/replica-loss smoke | Application operator | 20 / 150 min |  |  |  |  |
| C12 read every stop condition and record pre-write go/no-go | Change commander | 5 / 155 min |  |  |  |  |
| C13 reopen writes and start workers | Change commander | 25 / 180 min |  |  |  |  |

Crossing any hard stop records `ABORT`. Preserve partial target and report
evidence; do not improvise or silently extend the window.

## Mandatory pre-write decision

- [ ] Every DBM-CUT-001 stop condition was read aloud and evaluated.
- [ ] CI, three-run qualification, security, restore, migration rehearsals,
      loader capacity, and documentation walkthrough are current for this
      exact release.
- [ ] Database and application operators signed their gates.
- [ ] Source and target identities and both recovery boundaries are unchanged.
- [ ] Total elapsed time is below 180 minutes.

Decision: `GO` / `ABORT`

Change commander and UTC timestamp:

## Point of no return

The point of no return is the **first accepted PostgreSQL application write**,
not configuration deployment or a read-only smoke request.

| Field | Value |
| --- | --- |
| Maintenance-off revision/fingerprint |  |
| First write UTC timestamp |  |
| First write correlation/command ID |  |
| PostgreSQL writer identity |  |
| Observer and change-commander signatures |  |

Before this record exists, follow the cutover runbook's SQLite rollback. After
it exists, there is no reverse synchronization and no SQLite rollback; fence
writes and recover forward on PostgreSQL.

## Abort or stabilization record

| Field | Value |
| --- | --- |
| Abort/incident called at gate and UTC time |  |
| Mandatory stop condition |  |
| Last known valid recovery boundary |  |
| PostgreSQL application write accepted: yes/no |  |
| Recovery path and authorization |  |
| Service restored/steady at UTC time |  |
| Final evidence index SHA-256 |  |
| Incident/change commander sign-off |  |

Stabilization records public availability/error/latency, database connections,
locks/deadlocks, queue age/drain, WAL/archive/replication, storage/I/O,
autovacuum/analyze, bloat, backups, and integrity. It does not claim monthly
99.9% availability before the complete 30-day observation window.
