# Coordinated maintenance window for a release

A shared WorkChord server changes only by a WorkChord release. The default
rule is simple: deploy when no project has a running run and there is no live
claim. Wait for work to finish naturally, then confirm both counts are zero
before you stop the service.

A coordinated maintenance window is the only exception. It lets a release
restart the server while a long-running worker keeps its live claim. The
window protects only the live claims whose owners acknowledged it themselves.

## What counts as consent

Only one thing admits a live claim to a window: the claim owner's own
acknowledgement, sent with its agent key and bound to the claim's current
fence. The fence is the task, claim ID and claim generation. None of the
following counts as consent:

- a lease that would outlive the outage anyway;
- no requests from the worker for a while;
- a statement from a PM, an operator or another agent;
- a message outside WorkChord.

A new claim generation needs a new acknowledgement. A recorded PM notice says
only that the PM was told about the window. It never admits a claim.

## Roles

- **Operator** (operator key or workspace operator). Announces, begins,
  completes or cancels the window, and records notices sent through other
  channels.
- **Run owner** (the worker agent that holds the live claim). Acknowledges the
  window, renews with enough margin, and finishes its work.
- **PM** (each enabled, active agent with the PM role). Records that it has
  received the notice and tells its team.

## 1. Prepare

Before you announce a window:

1. Verify the backup and restore for the release, as the
   [backup runbook](postgresql-backup-restore.md) describes.
2. Review the release and its migration.
3. Choose `max_outage_seconds`. This is the longest time the server may stay
   unavailable. Use a value from a rehearsal of the same release on a copy of
   the data. If you have not measured it, do not guess: drain to zero instead.
4. Choose `expiry_margin_seconds`, the extra lease time beyond the outage. The
   default is 900 seconds.

## 2. Announce: admission closes

~~~bash
curl -sS -X POST "$WORKCHORD_URL/api/maintenance-windows" \
  -H "X-Admin-API-Key: $WORKCHORD_ADMIN_API_KEY" -H 'Content-Type: application/json' \
  -d '{"release_label": "<release>", "reason": "<what changes>",
       "planned_start_at": "<UTC time>", "planned_end_at": "<UTC time>",
       "max_outage_seconds": 300, "expiry_margin_seconds": 900}'
~~~

The window can last at most 24 hours, and the outage must fit inside it. Only
one window can be open at a time.

From this moment, no new work starts. Atomic begin, a direct task claim and a
run start through REST or MCP are refused with HTTP 409 and the code
`maintenance_window_admission_closed`. The refusal includes the window ID and
planned end. Work that already holds a live claim is not affected: it can
renew, record a checkpoint, submit or fail as usual. PMs can still plan and
queue work, but nothing begins until the window closes.

## 3. Notify every PM

Every PM must have a notice receipt before the window can begin. Choose one
of two ways for each PM:

- The PM reads `GET /api/agent/me/maintenance-windows/current` and records
  `POST /api/agent/me/maintenance-windows/{window_id}/notice-receipt` with its
  own key.
- You tell the PM through another channel and record it:
  `POST /api/maintenance-windows/{window_id}/notices` with `actor_id`,
  `channel` and `reference`, such as a message or change ID.

The PM then tells its team, including every run owner on that team.

## 4. Run owners acknowledge and renew

A run owner reads `GET /api/agent/me/maintenance-windows/current`. The
response shows the window, `minimum_lease_seconds` (the outage plus the
margin), and each of the owner's live claims with `acknowledged`.

To keep the claim through the window, the owner sends:

~~~bash
curl -sS -X POST "$WORKCHORD_URL/api/agent/me/maintenance-windows/<window_id>/acknowledge" \
  -H "X-Agent-API-Key: $WORKER_KEY" -H 'Content-Type: application/json' \
  -d '{"task_id": <task>, "claim_id": "<claim id>", "claim_generation": <generation>,
       "run_id": <run>}'
~~~

Repeating the same acknowledgement returns the same receipt. The owner then
keeps renewing as usual, with `lease_seconds` at least `minimum_lease_seconds`
plus its normal renewal interval. When the window begins, the lease must last
until the begin time plus the outage plus the margin.

An owner that prefers to finish first submits or fails its work instead. A
released claim needs no acknowledgement.

## 5. Check readiness

`GET /api/maintenance-windows/{window_id}` returns the receipts and
`readiness.blockers`. The window can begin only when the list is empty.

| Blocker | What to do |
|---|---|
| `window_not_started` | Wait for the planned start. |
| `window_no_longer_fits` | The outage no longer fits before the planned end. Cancel and announce a new window. |
| `owner_acknowledgement_missing` | Wait for that owner to acknowledge or to finish. Never begin without it. |
| `lease_margin_insufficient` | The owner must renew with a longer lease. |
| `running_run_without_live_claim` | The run's lease has expired. A PM recovers it with the expired-lease procedure in the [routing runbook](model-aware-routing.md). |
| `pm_notice_missing` | Notify that PM and record the receipt. |

If an owner does not acknowledge, cancel the window
(`POST /api/maintenance-windows/{window_id}/cancel`) or wait for the work to
finish. Do not deploy.

## 6. Begin and drain in-flight writes

`POST /api/maintenance-windows/{window_id}/begin` checks every blocker again.
If any remains, it refuses with `maintenance_window_not_ready` and lists them.
Otherwise it records the actual start time and the protected claims, each with
its task, owner, claim generation, expiry, run and assignment.

Then drain writes that are already in progress:

1. Fetch `/health/ready` from every replica. Wait until each one reports zero
   active mutations and transactions.
2. Read the window again. `readiness.unprotected_live_claims` must be empty.
   If any claim appears there, stop: complete the window as `rolled_back`
   without deploying and investigate.
3. Stop the web and worker services.

A protected worker's request that arrives during the outage fails with a
connection error or HTTP 503. The worker retries the same request with the same
idempotency key once the server is ready again. The server returns the
original result if the first attempt was recorded.

## 7. Restart

Run the migration and start the services, as the
[operations runbook](postgresql-operations.md) describes. Wait for
`/health/ready` to report the exact schema head on every replica. Keep the
outage within `max_outage_seconds`.

If the outage runs longer, protected leases expire at the time recorded in the
window. Never renew a lease for its owner and never edit claim fields. An
expired claim follows the PM's expired-lease recovery.

## 8. Resume and close

Protected workers renew with the same claim ID and claim generation, then
continue and submit. Close the window:

~~~bash
curl -sS -X POST "$WORKCHORD_URL/api/maintenance-windows/<window_id>/complete" \
  -H "X-Admin-API-Key: $WORKCHORD_ADMIN_API_KEY" -H 'Content-Type: application/json' \
  -d '{"outcome": "completed", "note": "<what happened>"}'
~~~

The window records the actual end time and, for each protected claim, one of:

- `preserved`: the same owner holds the same claim generation, and its lease is
  live;
- `finished`: the owner submitted or failed its run;
- `lost`: the lease expired or the claim generation changed.

Admission reopens as soon as the window closes. Report any `lost` claim to the
team's PM.

## Rollback

If the release fails after the window begins, restore service with the
previous release, as the [operations runbook](postgresql-operations.md)
describes. Then complete the window with `"outcome": "rolled_back"`. The
same resumption states apply.

PostgreSQL recovery is forward-only. A database restore discards writes made
after its recovery point, including renewals. Treat each protected claim by
its recorded resumption state, and recover lost claims through the PM.

## Limits

- The window covers agent work claims only. The outbound delivery worker's
  leases recover through lease expiry, as the
  [operations runbook](postgresql-operations.md) describes.
- `MAINTENANCE_MODE` fences every REST and MCP write, including protected
  renewals. If a release uses a fenced mode, count that time as outage.
- `GET /api/maintenance-windows` lists every coordinated window with its
  planned bounds, actual start and end, protected claims, resumption and
  outcome. `GET /api/maintenance-windows/{window_id}` adds its receipts.
