# PostgreSQL operator and developer guide

This is the pre-cutover entrypoint for DBM-DOC-001. It describes the supported
database boundary and routes every dangerous operation to its focused runbook.
It is documentation, not production-change authorization.

## Supported boundary and capacity wording

PostgreSQL 18 on its current approved minor is the integration and production
system of record. The only supported SQLAlchemy URLs are
`postgresql+psycopg://` for PostgreSQL and `sqlite+aiosqlite://` for direct
local development, tests, and the frozen legacy migration source. Production
sets `DATABASE_POSTGRESQL_REQUIRED=true`; there is no hidden SQLite fallback.

The pre-cutover capacity report can certify exactly **1,250 opaque browser
identities, 250 active browser sessions, and 200 concurrent MCP/agent
clients**. It cannot certify 1,250 authenticated people. Authentication, RBAC,
tenancy, and a people-based claim require a separate security contract.
Monthly 99.9% availability is a post-release 30-day observation objective, not
a conclusion from laboratory load runs.

## Runbook map

Use these documents in order. A later gate never makes an earlier failed gate
optional.

| Need | Contract |
| --- | --- |
| Driver, pool, migration, and dialect policy | [database portability policy](../database-portability-policy.md) |
| Locks, retries, process roles, probes, metrics, and write fences | [database runtime policy](../database-runtime-policy.md) |
| Development, rehearsal, and production topology | [deployment topology](postgresql-deployment.md) |
| Roles, grants, TLS, networks, and credential rotation | [security](postgresql-security.md) |
| SQLite snapshot, preflight, load, repair, and reconciliation | [data migration](sqlite-to-postgresql-migration.md) |
| Backup, PITR, restore, RPO, and RTO | [backup and restore](postgresql-backup-restore.md) |
| Capacity, soak, fault, and signed report evidence | [qualification](postgresql-qualification.md) |
| Timed change, rollback, and point of no return | [cutover](sqlite-to-postgresql-cutover.md) and [operator checklist](postgresql-cutover-checklist.md) |
| Signed abort drill, rehearsal series, authorization, and production record | [rehearsal/cutover evidence](postgresql-rehearsal-cutover-evidence.md) |
| Post-cutover release, stabilization, retirement, and independent SHIP/NO-SHIP | [post-cutover release and closeout](postgresql-postcutover-release-and-closeout.md) |
| Symptoms and stop-safe recovery | [troubleshooting](postgresql-troubleshooting.md) |

## Secret and release inputs

Install from a clean checkout of the exact release commit. Build the backend,
frontend/gateway, and PostgreSQL artifacts once, then record immutable image
digests. Tags alone are not release identities. Create the root virtual
environment exactly as shown in `README.md`; every source-tree command below
is run from the repository root and uses `.venv/bin`.

Keep these secret categories independent:

- migrator URL: login allowed to `SET ROLE workchord_owner`, available only to
  the one-shot migration and repair jobs;
- runtime URL: DML and sequence access only, shared by web and delivery-worker
  replicas through the secret manager;
- read-only URL: operator inspection only;
- backup URL or provider identity: logical backup and approved recovery use;
- administrative/provider identity: role creation, database lifecycle,
  failover, and PITR only; never mapped into an application container;
- application encryption, admin, bootstrap-agent, integration, and signing
  keys: separate from every database credential.

Never place a URL, password, private certificate key, browser/session token,
agent key, or qualification signing key in a rendered manifest, command log,
report, or repository file. Percent-encode reserved credential characters.

## Database, role, and connection contract

Create the database as UTF-8 using the built-in `PG_UNICODE_FAST` locale, UTC,
schema `workchord`, and search path `workchord, pg_catalog`. Record the exact
server build, locale provider/version, storage class/size/IOPS, maximum
connections, writer endpoint, failover DNS TTL, archive/PITR settings, and TLS
policy. Apply `deploy/postgresql/apply-security.sql` as documented in the
security runbook after the schema exists.

| Process role | Normal replicas | Per-process steady + overflow | Maximum total | Database authority |
| --- | ---: | ---: | ---: | --- |
| `web` | 2 | 15 + 5 | 40 | runtime DML only |
| `delivery_worker` | 2 | 8 + 2 | 20 | runtime DML only |
| `migration` | 1 one-shot | `NullPool` / configured 1 + 0 | 2 hard ceiling | schema migration through owner role |
| `repair` | 1 one-shot | `NullPool` / configured 1 + 0 | 2 hard ceiling | post-copy repair through owner role |

Reserve provider, monitoring, backup, migration, and failover headroom outside
the 60 application connections. Do not increase a pool to hide checkout
timeouts or failover latency; a material pool change invalidates the current
qualification attempt.

Production uses `DATABASE_SSL_MODE=verify-full` and an absolute, read-only CA
path. Configure both client certificate and key or neither. The runtime process
must not receive `DATABASE_SESSION_ROLE`; startup rejects that privilege leak.

## Clean local PostgreSQL install

The local Compose stack is the clean-install reference, not a production
template. It creates PostgreSQL, runs a one-shot migration and repair, starts
one web process and one dedicated delivery worker, and never mounts SQLite into
an application service.

~~~bash
cp .env.example .env
.venv/bin/python scripts/api_keys/generate_workchord_keys.py
docker compose config --quiet
docker compose up --build --detach
docker compose ps
curl --fail --silent --show-error http://localhost/health/live
curl --fail --silent --show-error http://localhost/health/ready
~~~

Copy generated secret values into `.env` before saving runtime credentials.
The readiness response must report the current Alembic head, healthy database,
an open migration gate, and one internally consistent maintenance fingerprint.
`docker compose logs migration repair backend delivery-worker` must contain no
URL or secret value.

The named volumes contain the PostgreSQL cluster, WAL archive, and backup
workspace. A live volume/file copy is not a backup. Use the backup jobs and an
isolated restore drill. The reset helper is only for a disposable local stack:

~~~bash
WORKCHORD_ALLOW_LOCAL_DATABASE_RESET=YES \
  scripts/database_migration/reset_local_postgresql.sh
~~~

It refuses production. Never use it as a cutover reset mechanism.

For direct local Python development only, the default SQLite URL remains
available. Run schema inspection or upgrade from the repository root:

~~~bash
./scripts/upgrade_database.sh --check
./scripts/upgrade_database.sh
(cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8001)
~~~

An online SQLite migration snapshot must still use `workchord-db-migrate
preflight`; never copy a live `.db` file.

## Clean production or rehearsal install

Before rendering Compose, the platform owner must provide the exact database,
schema, roles, TLS mounts, image digests, DNS names, storage and connection
budgets, monitoring destinations, and managed backup/PITR evidence. Rehearsal
uses an isolated database and the same two-web/two-worker shape. Production
must not reuse any local password or sidecar database.

Set every required `docker-compose.prod.yml` input through the deployment
secret/configuration system, then validate without starting a service:

~~~bash
docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml config --images
~~~

Confirm that the rendered output contains three distinct database URL secret
references and no secret values, SQLite URL, SQLite volume, floating image tag,
or administrative database identity. The production database must already
exist with the approved locale and roles. For an empty clean install, the
migration job reaches the packaged Alembic head and the repair job installs
versioned application seeds. For a nonempty upgrade, set the immutable
`DATABASE_EXTERNAL_BACKUP_REFERENCE` first.

~~~bash
docker compose -f docker-compose.prod.yml up migration
docker compose -f docker-compose.prod.yml up repair
docker compose -f docker-compose.prod.yml up --detach backend delivery-worker frontend proxy
docker compose -f docker-compose.prod.yml ps --all
~~~

The two attached one-shot commands must each exit 0. Keep their stopped
containers until the dependent services are healthy so Compose can enforce the
`service_completed_successfully` boundary; do not replace them with an
untracked shell migration.

Probe every web replica directly and through the public TLS gateway. Only then
may the load balancer route it. Confirm two unique replica IDs and a shared
configuration fingerprint. Confirm one worker can be removed and replaced
without duplicate delivery or an unbounded queue.

## Schema-only bootstrap, upgrade, and post-copy repair

Application startup performs read-only schema assertion; it never runs DDL or
seed repair. Use the packaged commands with the process role and pool fence:

~~~bash
DATABASE_PROCESS_ROLE=migration \
DATABASE_POOL_SIZE=1 \
DATABASE_MAX_OVERFLOW=0 \
DATABASE_SESSION_ROLE=workchord_owner \
  .venv/bin/python -m app.cli.upgrade --schema-only

DATABASE_PROCESS_ROLE=repair \
DATABASE_POOL_SIZE=1 \
DATABASE_MAX_OVERFLOW=0 \
DATABASE_SESSION_ROLE=workchord_owner \
  .venv/bin/python -m app.cli.upgrade --repairs-only

.venv/bin/python -m app.cli.upgrade --check
~~~

`--schema-only` is for an empty migration target. A nonempty PostgreSQL upgrade
uses `--no-repairs --external-backup-reference <approved-reference>` and is
followed by the separate repair command. `--skip-backup` can skip only the
automatic SQLite backup; it never bypasses PostgreSQL backup/PITR approval.
One-shot jobs exit nonzero on an unknown schema, multiple Alembic heads, failed
backup boundary, wrong role, or failed repair. Do not start web/worker services
after such an exit.

## Web, worker, readiness, and observability

Web replicas serve HTTP/MCP only. `workchord-worker` is the dedicated durable
delivery consumer; `OUTBOUND_DELIVERY_WORKER_ENABLED=true` is valid only with
`DATABASE_PROCESS_ROLE=delivery_worker`. Provider waits occur outside the
read transaction. On graceful shutdown the worker stops new claims and leaves
a process-loss claim recoverable through lease expiry.

- `/health/live` proves only that the process can answer HTTP.
- `/health/ready` proves bounded database connectivity, exact schema head,
  migration gate, queue/drain state, and database-statistics access.
- `/metrics` exposes low-cardinality application and database-pool evidence.
- the external monitor must call the public gateway every 30 seconds and keep
  DNS, connect, TLS, timeout, HTTP, and failed-attempt outcomes.

Never bypass readiness. A missing provider/gateway/WAL/storage metric is a
failed qualification input, not a zero. SQL text, parameters, request bodies,
URLs, credentials, and unbounded IDs must not become labels or log fields.

## Maintenance and validation modes

`MAINTENANCE_MODE` is restart-bound and accepts exactly `off`,
`read-only-maintenance`, or `validation-only`. Deploy one explicit
`MAINTENANCE_REVISION` to every web and worker replica and restart them; this is
not a mutable runtime toggle.

Both fenced modes reject unsafe REST and write-capable MCP operations before a
database transaction, suppress session/agent metadata touches, and prevent the
worker from claiming a lease. `validation-only` additionally limits REST to
the exact configured health/metrics allowlist. Before snapshot approval,
record `/health/ready` from every replica and require:

- the intended fenced mode and one shared configuration fingerprint;
- unique replica IDs and the complete expected replica set;
- zero active mutations, transactions, worker jobs, and active leases;
- `writer_drain.drained=true` on every replica;
- a controller-owned zero-connection result after every SQLite-owning process,
  scheduler, old release, shell, and job is stopped.

Seal that evidence using the migration runbook. One replica's in-memory zero
is never sufficient. A fingerprint mismatch, missing replica, active lease, or
source/WAL change is a mandatory stop.

## Backup, failover, rollback, and qualification

PostgreSQL release evidence requires managed or self-operated base backup,
continuous WAL/PITR, a portable logical backup, and an isolated restore that
passes reconciliation and validation-only application smoke. The approved
limits are RPO at most five minutes and RTO at most 30 minutes on the reference
data set. Follow the backup runbook; never restore with `--clean` into a
nonempty target.

Writer failover evidence begins at induced writer loss and includes unready
detection, promotion, endpoint convergence, stale-pool rejection, reconnect,
production-path readiness, and every client-observed failed attempt. Fence
writes if the writer identity is uncertain. After the first accepted
PostgreSQL application write there is no SQLite rollback or reverse
synchronization; recover forward through failover, PITR, or isolated validated
restore.

The load tools and signed-report assembler are necessary but are not a pass.
DBM-QUAL-001 requires three unique, consecutive, non-overlapping, complete
attempts against the same frozen release. Each includes all seven required load
phases, the eight-hour soak, fault and recovery drills, final CI evidence, and
independent review. A failed or stopped attempt increments the attempt number
and breaks the consecutive sequence. Follow the qualification runbook and keep
all generated artifacts out of Git.

## Pre-rehearsal documentation walkthrough

Run this walkthrough from a clean checkout using only released artifacts and
these documents. Record the commit and image digests, operator name, start/end
times, command exits, and evidence SHA-256 values.

1. Render the local and production/rehearsal Compose files without an
   undocumented variable or SQLite production fallback.
2. Start a fresh local PostgreSQL project and pass migration, repair, web,
   worker, liveness, and readiness checks.
3. Run every database/migration/load command's `--help` from the documented
   root virtual environment; confirm the flags and paths still exist.
4. Tabletop source fencing, snapshot preflight, target bootstrap/load,
   reconciliation, pre-write rollback, point of no return, forward recovery,
   restore, and every mandatory stop condition using the cutover checklist.
5. Run `scripts/ci/check_postgresql_documentation.py` and the final CI matrix.
6. Have an operator who did not author the change repeat the walkthrough and
   sign the review. Any later schema, query, index, pool, timeout, topology,
   retention, migration, or recovery change invalidates the walkthrough.

Encode and sign the independent result with `workchord-db-cutover
attest-documentation` as specified in the
[rehearsal/cutover evidence guide](postgresql-rehearsal-cutover-evidence.md).
The embedded key is not trusted unless it matches the independently supplied
public key.

Do not mark DBM-DOC-001 complete until this independent walkthrough passes
after the final DBM-RES-001 tuning change.
