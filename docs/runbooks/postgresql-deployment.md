# PostgreSQL deployment topology

The default `docker-compose.yml` is the DBM-DEPLOY-001 integration topology. It
uses the immutable PostgreSQL 18.4 image from the capacity contract, the
`PG_UNICODE_FAST` built-in locale, UTC, `workchord, pg_catalog`, a durable
major-version-aware volume, a two-second health probe, a one-shot schema job,
a separate repair job, web, and a dedicated delivery worker. No application
service mounts a SQLite data volume.

~~~bash
docker compose up --build
docker compose -f docker-compose.yml -f docker-compose.rehearsal.yml up --build
~~~

The rehearsal override runs two web and two worker replicas. Each process uses
its container hostname as the replica ID when `MAINTENANCE_REPLICA_ID=auto`.
Use `scripts/database_migration/reset_local_postgresql.sh` only with
`WORKCHORD_ALLOW_LOCAL_DATABASE_RESET=YES`; the script fixes the project/file
scope and refuses production.

Production uses an independently operated or managed PostgreSQL writer
endpoint; it is not a sidecar or shared application filesystem. The production
manifest requires distinct migrator/runtime/backup URLs, verified TLS, two web
and two worker replicas, the approved 40-web/20-worker connection budget, and
no SQLite volume. Nginx resolves all backend task addresses through Docker DNS,
keeps a shared passive-health upstream zone, retries only eligible upstream
failures, and enforces gateway-wide connection/request bounds rather than a
process-local counter.

The database or service manifest records PostgreSQL exact build, UTF-8,
provider/locale/collation version, UTC database/roles, schema/search path,
storage class/IOPS, max connections, allocated connection budget, TLS policy,
backup/PITR configuration, writer DNS name, failover DNS TTL, and monitoring
endpoints. Removing one web replica must reroute within 30 seconds.

During database failover, SQLAlchemy pre-ping rejects stale pooled connections;
the retry boundary handles documented connection SQLSTATEs only. DNS must
publish the new writer within the measured TTL. Web and workers remain unready
until `SELECT 1`, exact Alembic head, queue state, and migration gate all pass.
Do not bypass readiness or increase pools to mask a failover.
