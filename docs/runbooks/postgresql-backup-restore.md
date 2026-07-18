# PostgreSQL backup, PITR, and restore

This is the DBM-BACKUP-001 recovery contract. A backup is valid only after an
isolated restore, migration-to-head if needed, final reconciliation, and an
application smoke pass.

## Objectives and retention

- Maximum data-loss window (RPO): 5 minutes.
- Maximum service recovery time (RTO): 30 minutes on the recorded reference
  data set.
- WAL/PITR coverage: 35 days unless the approved product/legal retention
  contract requires longer.
- Backup storage is encrypted, access is limited to the backup role and
  recovery operators, and at least one copy is in a separate failure domain.
- Monitor base/logical backup duration and bytes, WAL archive failures and lag,
  archive/storage growth, and measured restore throughput.

Managed PostgreSQL production must enable automated base backups, continuous
WAL archiving/PITR, encryption, retention, deletion policy, and failover through
the provider control plane. The provider change record supplies immutable
version/configuration evidence. The repository's one-shot jobs supplement,
not replace, that service.

## Logical and base backups

Run a portable logical backup through the distinct backup URL:

~~~bash
docker compose --profile backup run --rm logical-backup
~~~

The job refuses unconfirmed encrypted storage, writes with mode 0600, uses
custom format, verifies the archive catalog, records server/client versions,
fsync-safe atomic naming, byte count, and SHA-256, and applies only the explicit
retention window below `/backups/logical`.

For a self-operated rehearsal primary, run:

~~~bash
docker compose --profile backup run --rm base-backup
~~~

The base job streams WAL, requests a fast checkpoint, creates a PostgreSQL
backup manifest with SHA-256 checksums, runs `pg_verifybackup`, and writes a
second file checksum inventory. Development PostgreSQL enables WAL archiving
with `archive_timeout=300s` into a volume mounted outside `PGDATA`; its startup
wrapper fixes that volume to mode 0700 and PostgreSQL ownership before the
official entrypoint drops privileges. Production uses the managed equivalent
and alerts before archive lag exceeds 300 seconds.

## Isolated restore drill

1. Resolve an empty database named
   `workchord_restore_<at-least-eight-lowercase-letters-or-digits>` on an
   isolated host/network. Never use the production database name.
2. Set `RESTORE_TARGET_IDENTIFIER` from the approved change record and set
   `RESTORE_AUTHORIZED_TARGET` independently to the same value.
3. Mount the chosen dump below `/backups/logical`, obtain its recorded SHA-256,
   and run `scripts/database_backup/restore_verify.sh` in the pinned PostgreSQL
   client image.
4. The script refuses a nonempty database and never uses `--clean`; it cannot
   overwrite production by first deleting objects.
5. If the restored Alembic revision is old, run the packaged migration job with
   an external backup reference and then record the exact new head.
6. Run the same invariant/reconciliation catalog used by DBM-DATA-003, followed
   by backend readiness and representative REST/MCP reads in validation-only
   mode.
7. Record source backup identity, requested recovery point, actual last
   transaction, start/end timestamps, restored bytes, WAL replay lag,
   reconciliation checksum, smoke result, and measured RPO/RTO.

For a PITR drill, choose a transaction boundary recorded after the base backup
and before the latest archived WAL. Restore to that exact timestamp/LSN in the
isolated target, prove the boundary row is present and the following boundary
row absent, then run the full validation above.

## Failure and compatibility policy

- Alert on any archive command/error, consecutive missing WAL segment, archive
  lag above five minutes, backup checksum error, backup-window overrun, or
  restore throughput that projects beyond 30 minutes.
- A PostgreSQL major version restores first into a compatible major. Major
  upgrades use logical transfer or `pg_upgrade` rehearsal; never assume a base
  backup is portable across majors.
- A failed drill invalidates the backup set for release evidence until a later
  scheduled drill passes. It never becomes a paper exception.
- Restore drills delete only the explicitly authorized isolated target through
  platform lifecycle tooling after evidence retention is complete.
