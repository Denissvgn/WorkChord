# PostgreSQL troubleshooting and stop-safe recovery

Use this guide only after the deployment identity, environment, database
target, maintenance revision, and current change record are resolved. It does
not override the mandatory stop conditions in the migration, qualification, or
cutover runbooks.

## Safe first capture

Capture secret-free evidence before restarting or changing configuration:

~~~bash
docker compose ps
curl --fail --silent --show-error http://localhost/health/live
curl --fail --silent --show-error http://localhost/health/ready
docker compose logs --since 15m migration repair backend delivery-worker
~~~

For production, add `-f docker-compose.prod.yml` and use the approved public
and direct replica probe URLs. Record the rendered configuration checksum,
image digests, replica IDs, maintenance fingerprint, Alembic head, migration
gate, writer endpoint, current database/server identity, and correlation IDs.
Do not record a database URL, query parameter, SQL parameter, request body,
password, token, cookie, private key, or secret setting value.

## Symptom guide

| Symptom | Inspect | Safe response |
| --- | --- | --- |
| Startup says PostgreSQL is required | Redacted driver/dialect summary and `DEPLOYMENT_ENVIRONMENT` | Supply the approved `postgresql+psycopg://` secret. Never disable `DATABASE_POSTGRESQL_REQUIRED` in production. |
| URL/driver validation fails | Scheme, percent-encoding, host/database presence, process role | Use only `postgresql+psycopg://` or the explicit local/test `sqlite+aiosqlite://` path. Do not log the URL. |
| TLS verification fails | CA mount, absolute path, hostname/SAN, certificate validity, client cert/key pairing | Keep the replica unready. Repair trust or DNS; never fall back from `verify-full` or disable verification in production. |
| `/health/live` passes but `/health/ready` fails | Readiness reason, DB reachability, Alembic head, migration gate, queue/drain, statistics grant | Keep traffic out. Fix the named gate; do not route on liveness or suppress readiness. |
| Migration reports empty/unknown/multiple heads | Exact target identity and `app.cli.upgrade --check` output | Stop. Resolve the release/schema mismatch. Never stamp a revision or run ad-hoc DDL to force green. |
| Runtime role gets permission denied | Current login, grants, owner/default privileges, schema/search path | Reapply the reviewed security contract as an administrator. Never give the runtime login owner, `CREATEDB`, `CREATEROLE`, or superuser. |
| Runtime process rejects `DATABASE_SESSION_ROLE` | Rendered web/worker environment | Remove the owner role from runtime containers. Only migration/repair may assume it. |
| Pool timeout or connection saturation | Checked-out/overflow/timeouts, provider sessions, web/worker replica count, reserved headroom | Find held sessions or demand. Do not increase pools during an attempt; treat a pool change as tuning and rerun qualification. |
| Deadlock/serialization error | SQLSTATE, bounded retry metrics, involved aggregate/correlation IDs | Let only an approved idempotent transaction retry. Unknown errors propagate; do not add broad retries around external I/O. |
| Maintenance replicas disagree | Mode, revision, fingerprint, unique replica IDs, expected replica count | Keep the fence closed and redeploy every replica. Never accept a partial rollout as writer-drain evidence. |
| Writer drain is false | Active mutations/transactions/jobs/leases and controller SQLite connections | Stop remaining workers, schedulers, shells, jobs, and old releases. Wait for/resolve leases; do not snapshot until every signal is zero. |
| Source preflight says the SQLite source or WAL changed | Source owners, source/WAL identities, evidence age | Abort. Re-fence, create a new backup-API snapshot and manifest, and restart preflight. Never copy the live file. |
| Loader refuses target or says nonempty | Secret-free target identity, authorization record, migration-gate/checkpoints | Stop. Do not reset through the loader. Two operators must resolve an explicitly disposable target before platform deletion. |
| Loader exits `migration_loader_busy` | Active migration job/process and the latest target-owned migration gate | Do not wait, take over, or start another loader. If inspection confirms that no owner remains, explicitly rerun the same manifested load with identical target authorization, evidence, and chunk size; do not rewrite the gate. |
| Load or reconciliation differs | Table report, counts/digests, constraints, sequences, secret checks, statistics, repair hashes | Keep PostgreSQL closed. Preserve evidence and investigate. Do not waive or manually edit a difference. |
| Worker queue age/backlog grows | Worker readiness, active leases, provider latency, batch/poll settings, pool occupancy | Replace a failed worker and observe bounded drain. Do not start an embedded worker in web or duplicate-send a leased item. |
| `pg_stat_statements` is unavailable | preload configuration, extension installation, monitoring role grants | The application may run, but qualification lacks required query evidence. Fix the platform configuration and restart the attempt. |
| WAL archive/backup check fails | Archiver counters since the recorded reset, lag, storage, checksum/catalog, encryption attestation | Stop release/cutover. Repair archive or storage and complete a new isolated restore drill. Missing WAL is never a paper exception. |
| Writer failover does not converge | Unready/promotion/DNS/pool reconnect timeline and every failed client attempt | Fence writes and declare an incident. Recover forward on PostgreSQL; never switch back to SQLite after PostgreSQL writes reopen. |
| Storage horizon is below 12 months or 70% arrives early | Eight-hour growth/WAL/bloat/I/O/backup evidence and lifecycle policy | Stop. Implement and test the selected expansion/archive/partition/purge intervention, then restart all three attempts. |

## Mode-specific recovery boundaries

In `validation-only`, only the explicit health/metrics allowlist and read-only
MCP validation calls are available. In `read-only-maintenance`, ordinary safe
reads are allowed but all writes and metadata touches remain fenced. Changing
mode requires a restart of every replica with a new revision; never patch one
process in place.

Before the first accepted PostgreSQL application write, rollback uses a new
operator-owned copy of the checksummed frozen SQLite snapshot and the exact
pre-migration release. After that write, there is no reverse synchronization:
fence the system and recover forward through PostgreSQL failover, PITR, or an
isolated validated restore.

## Escalation packet

Give the incident/change commander only secret-free evidence:

- change ID, environment, release commit and image digests;
- start/end time and current gate/timer;
- source manifest/snapshot hashes or PostgreSQL resource and recovery-point
  identities, as applicable;
- replica readiness payloads, maintenance fingerprint, queue/drain summary;
- error class/SQLSTATE, bounded correlation IDs, SLO/connection/WAL/storage
  observations, and artifact checksums;
- last known valid backup/PITR/restore evidence and whether PostgreSQL has
  accepted any application write.

If the target, writer, source, evidence integrity, timer, or authority is
uncertain, stop. Do not improvise a destructive command.
