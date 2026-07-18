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

`DATABASE_PROCESS_ROLE=web` permits at most 20 pooled connections per process
(15 steady plus 5 overflow by default). `delivery_worker` permits at most 10
(8 plus 2 in the approved deployment contract). One-shot migration and
inspection paths always use `NullPool` and do not consume a persistent pool
allocation.

## Historical migration compatibility rule

Revision identifiers and domain meaning are immutable. Before PostgreSQL is an
official production backend, a historical revision may receive a narrowly
scoped compatibility repair only when all of the following are true:

1. the old statement is accepted by SQLite but cannot execute on PostgreSQL, or
   depends on object-creation ordering that PostgreSQL correctly rejects;
2. the repair preserves the revision ID, final logical schema, existing SQLite
   upgrades, and application data meaning;
3. fresh SQLite, legacy SQLite, fresh PostgreSQL, and staged legacy PostgreSQL
   paths are covered by the dual-dialect migration suite;
4. type, nullability, sequence, or data normalization beyond syntax/order is
   performed in a new head revision with an explicit downgrade policy.

The current permitted repairs are the portable Boolean default in revision
`20260507_0001` and deferring two `user_sessions` foreign keys until revision
`20260510_0023` creates their target table. Revision `20260718_0031` owns the
reviewable UTC timestamp, legacy-nullability, and PostgreSQL sequence alignment.

After PostgreSQL production support is declared, historical revisions are
fully frozen; later corrections must use a new revision.

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
