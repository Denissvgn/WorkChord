# PostgreSQL security and credential boundaries

This is the DBM-SEC-001 role, TLS, network, and rotation contract. WorkChord
does not claim row-level security or tenant isolation. RLS remains out of scope
until a tenant model defines its policy and tests.

## Roles

Provision these identities in the platform secret manager, never in source or
database settings rows:

| Role | Login | Authority |
| --- | --- | --- |
| `workchord_owner` | No | Owns the application schema and objects; no CREATEROLE or superuser |
| `workchord_migrator` | Yes | Can `SET ROLE workchord_owner`; used only by migration/repair jobs |
| `workchord_runtime` | Yes | DML plus sequence use in `workchord`; cannot create/alter schema or roles |
| `workchord_readonly` | Yes | Operator SELECT only |
| `workchord_backup` | Yes | Logical-backup SELECT and sequence visibility; self-operated base backup additionally requires platform-granted REPLICATION |

Create login roles with platform-generated passwords or certificate identities.
Do not pass passwords as `psql -v` variables. As a database administrator,
apply grants after schema migration:

~~~bash
psql "$DATABASE_ADMIN_URL" -X \
  -v ON_ERROR_STOP=1 \
  -v owner_role=workchord_owner \
  -v migrator_role=workchord_migrator \
  -v runtime_role=workchord_runtime \
  -v readonly_role=workchord_readonly \
  -v backup_role=workchord_backup \
  -f deploy/postgresql/apply-security.sql
~~~

The script revokes untrusted `public` creation, pins per-role timezone and
search path, grants current objects, configures owner default privileges for
future migrations, grants runtime read access to Alembic and migration-gate
state, and explicitly removes owner membership from runtime.

Managed-service base backup/PITR authority stays in the provider control plane.
For a self-operated primary, a database administrator separately grants
`REPLICATION` to the backup login and restricts its HBA/network path; the
schema grant script deliberately cannot smuggle cluster-level authority into a
normal application grant change.

Production Compose maps `DATABASE_MIGRATION_URL` only into migration/repair,
`DATABASE_RUNTIME_URL` only into web/workers, and `DATABASE_BACKUP_URL` only
into the backup job. Web and workers reject `DATABASE_SESSION_ROLE`; only
migration/repair may assume the NOLOGIN owner.

## TLS and network

- Production uses `sslmode=verify-full` and an absolute read-only CA path.
- Client certificate and key are configured together or neither is accepted.
- The PostgreSQL endpoint accepts only web, worker, migration, backup,
  monitoring, and approved operator network paths.
- The public gateway cannot reach an administrative database endpoint. The
  application network is internal; only explicitly egress-enabled services can
  reach a managed PostgreSQL boundary.
- Database URLs, query parameters, SQL parameters, and credentials are never
  emitted in logs, manifests, or metric labels.

## Rotation

1. Create a new runtime secret version and login credential without revoking
   the old one.
2. Apply the same role membership, database defaults, and network policy.
3. Restart one web replica and one worker with the new `DATABASE_RUNTIME_URL`.
4. Pass readiness and read/write smoke; verify the old and new identities have
   identical grants and neither can create schema objects or roles.
5. Roll the remaining replicas. Confirm pool connections using the old login
   drain to zero.
6. Revoke the old credential, terminate only its remaining sessions, and record
   the bounded disruption.
7. Repeat separately for migrator, read-only, and backup identities. Never
   expose migrator credentials to a web container during a rotation.

Emergency revocation skips the overlap but keeps the application fenced until
readiness and integrity checks pass with a replacement identity. Run the grant
denial, TLS verification, secret scan, and rotation rehearsal before release.
