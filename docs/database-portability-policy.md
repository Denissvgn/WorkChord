# Database portability policy

WorkChord supports two explicit SQLAlchemy runtime URLs during the PostgreSQL
migration window:

- `sqlite+aiosqlite://...` for development, tests, and the supported legacy
  source database;
- `postgresql+psycopg://...` for PostgreSQL through Psycopg 3 in both async
  application and synchronous migration/inspection paths.

No other SQLite or PostgreSQL driver is part of the support contract. Database
credentials and connection-policy values must not be logged; use the redacted
database summary exposed by `app.database` for diagnostics.

The production fallback allowed value is always false. PostgreSQL production
support is declared only by the signed post-cutover publication for the actual
release boundary. At that boundary SQLite production support is removed;
SQLite remains available only for direct development, tests, and the frozen
read-only migration source. Repository support code or a synthetic evidence
chain is not proof that a particular deployment completed cutover.

`DATABASE_PROCESS_ROLE=web` permits at most 20 pooled connections per process
(15 steady plus 5 overflow by default). `delivery_worker` permits at most 10
(8 plus 2 in the approved deployment contract). One-shot migration and
inspection paths always use `NullPool` and do not consume a persistent pool
allocation.

## Initial schema and future migrations

New databases are created by the single frozen initial revision
`20260928_0001`. It includes the complete application schema, constraints,
indexes, UTC timestamp types, and task recovery fences. Schema creation does
not seed application data. Future schema changes use new Alembic revisions.

Databases created by earlier unreleased builds are outside this revision chain.
Keep a backup if their development data is needed, then point `DATABASE_URL`
at a new empty database and run schema initialization followed by explicit
repairs. Never stamp the initial revision onto an old or unversioned schema.
The upgrade command refuses those databases without modifying them. It does
not delete or automatically reset an existing database.

The initial revision has no destructive downgrade. Recovery uses a complete
backup and its matching application image; disposable development databases
may be recreated explicitly.

## Operational command boundary

Application startup only asserts that the configured schema is Alembic-current.
It does not run DDL.

- `python -m app.cli.upgrade --check` performs read-only inspection from any
  process role.
- The `migration` role runs `python -m app.cli.upgrade --schema-only` to
  bootstrap an empty target, or `python -m app.cli.upgrade --no-repairs` to
  upgrade a recognized database. It never creates application-owned rows.
- After schema work succeeds, the separate `repair` role runs
  `python -m app.cli.upgrade --repairs-only` to serialize post-copy seed and
  compatibility repairs on an already current schema.
- The migration command rejects a combined migration-and-repair invocation;
  set `DATABASE_POOL_SIZE=1` and `DATABASE_MAX_OVERFLOW=0` for both one-shot
  roles, as shown in the Compose topology.

PostgreSQL schema upgrades and repairs take a session advisory lock. A
non-empty PostgreSQL upgrade also requires
`--external-backup-reference <operator-reference>`; `--skip-backup` only skips
the automatic SQLite file backup and cannot bypass the PostgreSQL backup/PITR
gate.
