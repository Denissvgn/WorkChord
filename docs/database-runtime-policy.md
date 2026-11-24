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
| Planning preview/apply | `PlanningState -> Iteration -> Calendar[id...] [FOR SHARE] -> Task[id...] -> TaskDependency[id...] -> TeamMember[id...] -> Vacation[id...]` | The planning revision serializes shared capacity inputs. The PM command scopes its work rows to the authorized iteration. |
| Dated capacity adjustment | `PlanningState -> Iteration[id...] -> TeamMember -> TeamMemberCapacityAdjustment[active...] -> Task[id...] -> AgentTaskAssignment[id...]` | The planning revision serializes it with schedules and dispatch. The row's tasks on reduced dates are locked, without a version change, before their live assignments are read to refuse a reduction under issued work. |
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
Selected annual calendars use `FOR SHARE` in ID order. An editor waits for a
forecast using that calendar. The preview digest includes the observed iteration
revision and the explicit iteration and member calendar rules. Apply
also re-hashes every input after scheduling, accounting for its own iteration
reservation and restoring scheduler-owned output fields to their pre-apply values before task
versions and audit events are committed. PostgreSQL schedule code contains no
table-level lock.

A dispatch and a calendar edit serialize through the planning revision row.
PostgreSQL dispatch takes it before the routing table locks and the task lock.
Replacing supplemental years leaves task versions unchanged and inspects issued
work while the shared revision is held.

Deleting a proven unused capacity allocation advances the shared planning and
affected iteration revisions while preserving task versions and issued work.
Read the member's planning-input context and supply its complete
`X-Expected-Revisions` on `DELETE /api/team-members/{member_id}`.
Use `unused_only=true` when the operation depends on the allocation remaining
unused. A current reference or retained task or routing history then returns
`allocation_not_unused`. The ordinary deletion path retains its existing
behavior for deliberately removing a referenced allocation.

The standalone command reads the authorized scope and retained history before
reserving the shared planning writer. A direct live reference can avoid this
history scan. Historical work grows with retained snapshot task nodes and
nonempty routing decisions. Known routing records are classified by their
version and exact bytes. The locked command rechecks the observed planning
revision, allocation references and any issued owner. An ordinary removal uses
its existing conservative task reservation if it cannot prove a planning-only
change. If a concurrent planning change invalidates an otherwise unused observation,
the guarded request asks for a fresh context.

A capacity row's availability percentage applies to its whole iteration. A
dated adjustment replaces that percentage from a start date through an end date
inside the row's iteration, and every capacity calculation (shared person
capacity, member capacity and workload, readiness, routing and the scheduler)
reads the adjusted percentage on those dates only. Read the member's
planning-input context, which lists its active adjustments, and send its
complete `X-Expected-Revisions` with
`POST /api/team-members/{member_id}/capacity-adjustments`. One command records
new adjustments and withdraws earlier ones together, so moving capacity between
two rows of the same person is two adjustments on two rows.
`POST /api/team-members/{member_id}/capacity-adjustments/preview` returns the
effective capacity of the row and of every row of the same person for the
changed dates and changes nothing. The command advances the shared planning
revision and the revisions of every iteration that has a row of the same
person, records a recovery snapshot of each, and writes a command audit entry.
It reserves no task version, so issued work stays current. A reduction on a date
where this row's issued work is scheduled returns `capacity_adjustment_in_use`
with the affected task and assignment IDs. Adjustments are never edited:
withdrawing one keeps it, with who withdrew it and why, in
`GET /api/team-members/{member_id}/capacity-adjustments?include_withdrawn=true`.
An adjustment is part of its row; it does not count as a use of an unused
allocation and is removed with the row. Iteration export and import do not
carry adjustments; record them again after an import.

Saved commitments in shared person capacity spread a task's known effort over
its baseline in proportion to the row's percentage on each date, so a date an
adjustment lowers carries less of the commitment. The scheduler places effort
hours with each date's own percentage as well. Its whole-task effort estimate,
which orders work for the scheduling pass rules and sizes the uninterrupted
slot it searches for, keeps the row's own percentage: that estimate has no
dates, and the forecast start and end dates still come from the dated
placement.

To check a proposed iteration start, end or calendar against the people's
other bookings before changing it, send the proposed fields to
`POST /api/iterations/{iteration_id}/date-move/preview`. It needs edit
permission on the iteration and changes nothing. For each person of the
iteration team it reports every date of the proposed period where the hours
the iteration's rows would request, added to the hours the person's rows in
other iterations already book, exceed the person's available hours, with dated
adjustments applied. Bookings in iterations you cannot read are reported only
as a total. Apply the move with the iteration update, sending the same fields
and the returned `expected_revisions`; the update is refused if the iteration
changed since the preview. Bookings in other iterations are not part of that
fence, so preview again if the returned `planning_revision` has moved on.
Agents use the `agent_preview_iteration_date_move` MCP tool and apply with
`agent_update_iteration`. To downgrade a database to a release
without adjustments, withdraw every active adjustment first; the downgrade
refuses to discard an active one.

To downgrade a database with annual selections to a release that supports only
one calendar per owner, export the iteration and profile selections and clear
them through their normal commands. Resolve any affected issued work first.
The downgrade refuses to discard a populated annual selection.

An existing iteration whose dates lie outside its primary calendar keeps its
dates, tasks and execution history after upgrade. Its working-day, capacity and
workload totals cover only selected years. Read `missing_calendar_years` and
select the actual annual records before applying its forecast. An uncovered
saved commitment in a different allocation can leave its proportional daily
effort unknown. The draft lists that warning and its visible capacity owner;
publishing a baseline requires complete commitment inputs.

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
