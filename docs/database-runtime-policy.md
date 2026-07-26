# Database runtime, concurrency, and maintenance policy

This document is the executable Wave 2 policy for the supported migration
window: SQLite remains a development/legacy source dialect and PostgreSQL is
the target runtime. Tests under `backend/tests/database/` bind the policy to
both dialects and to a real PostgreSQL server when `POSTGRES_ADMIN_URL` is set.

## Global lock order

Any transaction that needs more than one mutable row class acquires locks in
this order and never discovers an earlier key by first locking a later row:

1. aggregate root: `Project`, then `Iteration`;
2. `Task`, ordered by primary key;
3. `AgentActor`, ordered by primary key;
4. `AgentTaskAssignment`, ordered by primary key;
5. `AgentRun`, ordered by primary key;
6. command/idempotency/event rows created by the transaction.

Independent aggregates (`TeamMemberProfile` preset creation, `TriageItem`, and
`OutboundWebhookDelivery`) lock only their own row class. If a future command
must combine one of them with the main task lifecycle, it must add that class to
this order and add a deadlock/race test before merging. Multi-row sets always
use ascending primary-key order. Queue selection is
`next_retry_at NULLS FIRST, created_at NULLS LAST, id`.

Current `FOR UPDATE` inventory:

| Area | Locked rows | Enforcement |
| --- | --- | --- |
| Task dependency/tree mutation | `Iteration -> Task` | `TaskService` locks the iteration aggregate before the task row |
| Task context revision | `Task` | `task_context_revision_service.lock_task_context` |
| Atomic assignment/work lifecycle | `Task -> AgentActor -> AgentTaskAssignment -> AgentRun` | ordered helpers in `AgentWorkService` |
| Legacy claim/event/run lifecycle | `Task` or `AgentRun` | focused transitions in `AgentService`; live uniqueness indexes are the final fence |
| Planning preview/apply | `Iteration -> Calendar[FOR SHARE] -> Task[id...] -> TaskDependency[id...] -> TeamMember[id...] -> Vacation[id...]` | `AgentPlanningService`; all exclusive locks are scoped to one iteration aggregate |
| Profile preset creation | `TeamMemberProfile` | seed-key uniqueness plus locked re-read |
| Triage reservation | `TriageItem` | `TriageService.get_by_id(for_update=True)` |
| Delivery queue | due `OutboundWebhookDelivery[id...]` | PostgreSQL `FOR UPDATE SKIP LOCKED`; SQLite compare-and-set lease update |
| Project update append | `Project` | `AgentWorkService.create_project_update` |

SQLite ignores `SELECT FOR UPDATE`. Its compatibility path may use a no-op
write only inside an explicit `dialect.name == "sqlite"` branch to reserve the
single writer. PostgreSQL paths never classify or retry SQLite "database is
locked" messages.

The iteration row is the schedule aggregate root. Its `FOR UPDATE` lock fences
new task and team-member foreign keys for that iteration; existing task,
dependency, member, and vacation rows are then locked in deterministic order.
The calendar uses `FOR SHARE`, so a calendar edit waits but schedules for two
different iterations using the same calendar do not block one another. Apply
also re-hashes every input after scheduling, normalizing only the three
scheduler-owned output fields back to their pre-apply values, before task
versions and audit events are committed. PostgreSQL schedule code contains no
table-level lock.

## Retry boundary

`app.database_runtime.run_database_retry` recognizes SQLSTATE `40001`
(serialization), `40P01` (deadlock), PostgreSQL connection class `08`, and the
documented shutdown/connection-slot states. The default budget is three
attempts, full jitter bounded to 250 ms per delay, and a one-second total
deadline.

Replay is allowed only for a complete compare-and-set transaction or a command
protected by a durable idempotency/command record. The callable includes its
commit. An operation that performed untracked HTTP, SMTP, GitHub, or other
external I/O is not retryable. Exhaustion becomes a typed conflict or database
unavailable error; unknown DBAPI/programming errors propagate unchanged.

The delivery lease claim is the first integrated safe retry boundary. If its
commit succeeds but acknowledgement is lost, replay observes the lease as no
longer due and lets it expire; it cannot send twice.

## Ordering and comparison contract

- Every limited/paginated/queue query ends in a unique primary-key tie-breaker.
- Nullable queue times are `NULLS FIRST`; nullable target dates and event times
  use an explicit `NULLS LAST` where undated work follows dated work.
- ASCII search input is case-insensitive on both dialects.
- Non-ASCII search input is NFKC-normalized by the application and then matched
  with exact case/code points. WorkChord does not claim SQLite `LOWER` and a
  PostgreSQL locale provide equivalent Unicode case folding.
- JSON object key order is never used as equality, ordering, cursor, or digest
  evidence. Digests canonicalize in application code.
- Qualification records PostgreSQL encoding/collation/version and UTC database
  and role timezone from the database-creation contract.

## Cardinality boundaries

The ordinary iteration tree and project tree endpoints refuse more than 2,500
tasks with typed `collection_limit_exceeded` HTTP 413 responses. Ordinary
bounded lists cap at the capacity contract's 500-item response profile. The
global iteration list keeps its legacy response for small workspaces, refuses
implicit overflow, and offers stable `(start_date, id)` keyset pages; the
frontend explicitly walks those pages. Team/profile, agent-pipeline, project,
history, and overdue-work collections also fail with the same typed limit
instead of truncating silently. Synchronous iteration export is separately
capped at 5,000 tasks. Project and iteration summary statistics use SQL
aggregates rather than loading task graphs. The production seed's 10,000-task
hot project therefore uses the summary path; a complete project graph requires
a later asynchronous/bounded export workflow.

## Process roles

- `migration`: one-shot Alembic/schema and serialized repair command; pool
  capacity at most two and operational paths use `NullPool`.
- `repair`: explicit post-copy repair mode; pool capacity at most two.
- `web`: schema assertion and HTTP/MCP serving only; no DDL, seeds, repairs, or
  embedded delivery loop. Pool capacity at most twenty.
- `delivery_worker`: durable delivery claiming/sending only; pool capacity at
  most ten. Provider waits occur after the read transaction is released.

Compose starts migration to successful completion before web and worker roles.
Production web configuration fails validation if the embedded-worker flag is
enabled. Worker shutdown stops new polls, finishes its current bounded job, and
leaves any process-loss claim recoverable by lease expiry.

## Liveness, readiness, and metrics

- `/health/live` (and backward-compatible `/health`) proves only process HTTP
  liveness.
- `/health/ready` uses a strict deadline to check connectivity, `SELECT 1`, the
  exact packaged Alembic head, queue/drain state, and safe PostgreSQL statistics.
- `/metrics` exports low-cardinality Prometheus text for HTTP/query latency,
  active transactions, checked-out connections, pool timeouts,
  retry/deadlock classes, slow queries, process RSS, queue depth/age/leases,
  worker throughput, database size, temporary I/O, dead tuples, and analyze
  lag.

SQL text, parameters, request bodies, credentials, and database URLs with
secrets are never metric labels or log fields. Request/command correlation IDs
are bounded safe identifiers. Deployment collectors remain responsible for
gateway/client attempts, DNS/TLS failures, database CPU, storage latency/IOPS,
WAL/archive and replication lag, bloat estimates, and backup duration. Those
external series join the application scrape in the qualification artifact;
absence of one is a failed qualification input, not a zero value.

The production gateway emits one JSON record to stdout for every accepted HTTP
attempt, using a generated request/correlation ID, method, URI path without the
query string, gateway/upstream status, timings, and response bytes. Its exact
`/health` route reaches backend liveness through production TLS and routing.
The deployment monitor must call that public URL every 30 seconds and record
DNS, connect, TLS, timeout, and HTTP outcomes, including failures that cannot
reach Nginx. Alert and qualification thresholds come directly from
the installed contract bundle member
`backend/app/autonomy/contracts/postgresql/postgresql-capacity-contract-v1.json`;
collectors must retain the raw gateway/synthetic denominator needed by its
availability SLI.

PostgreSQL deployments enable slow-query logging and `pg_stat_statements` only
through the approved database topology/role grants. The application continues
to work when the runtime role cannot install extensions.

## Maintenance and validation modes

`MAINTENANCE_MODE` is restart-bound deployment configuration with exactly
`off`, `read-only-maintenance`, and `validation-only` states. Its revision,
replica identity, complete allowlist, and SHA-256 configuration fingerprint are
reported by liveness/readiness so an operator can compare every replica.

In either fenced state:

- every unsafe REST method is rejected with typed HTTP 503 and `Retry-After`;
- every write-only/execute-only MCP scope is rejected before opening a DB
  transaction;
- browser session creation/touch/expiry cleanup and agent last-seen touches are
  suppressed;
- web startup cannot seed or repair;
- the dedicated worker exits drained and cannot claim a lease.

Read-only maintenance permits safe REST reads. Validation-only permits only the
exact paths/prefixes in `MAINTENANCE_VALIDATION_ALLOWLIST`, plus protocol-level
MCP access whose tool calls are scope-classified read-only. The default REST
allowlist is `/health`, `/health/live`, `/health/ready`, and `/metrics`.

Readiness reports a writer-drained signal only when the mode is fenced, local
active mutations and worker jobs are zero, and the durable queue has no active
leases. Snapshot approval additionally requires every replica to report the
same configuration fingerprint and requires the deployment controller to stop
all SQLite-owning processes; one replica's in-memory observation is never
sufficient.
