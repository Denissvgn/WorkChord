# Execution usage and advisory budgets

An authorized runtime records usage against an exact run using
`POST /api/agent/runs/{run_id}/usage` or `agent_record_execution_usage`.
Read the current report with the corresponding GET or
`agent_get_execution_usage` before appending a correction.

Declare `reporting_mode: attempt_total`, a deterministic `report_id`, source,
provenance, UTC interval and coverage. Named quantities retain observed zero
and explicit unknown values. Complete coverage requires a reported quantity
or cost; unavailable coverage contains no measured values. Delta reports are
not accepted by this interface.

Identical report content replays its receipt. Reusing an ID for different
content conflicts. A correction uses a new ID and the current
`expected_previous_digest`; earlier reports remain immutable and the latest
attempt total is counted once. The limit is 32 report revisions per attempt.
Reporting preserves execution state, claim ownership and task acceptance.

Optional reported cost requires its currency. Optional pricing basis captures
the unit, price amount and quantity, currency, source, quote timestamp and
version. Estimates use that saved basis; changing model metadata does not
reprice existing reports. Currencies remain separate, with no implicit
conversion. Quantity precision is six decimal places; money preserves up to
twelve decimal places. Unknown values remain unknown.

Reports are actor declarations, with `independently_reconciled: false`.
Simulation quantities and costs have separate totals and are excluded from
measured spending. Explicit human effort requires manual-report provenance;
elapsed cycle or review time does not supply labor effort.

Analytics and `GET /api/tasks/execution-usage` expose authorized scoped totals,
missing/partial reports, accepted-outcome linkage, review/rework/recovery
observations and optional advisory budgets. Scope remains the first report's
scope through corrections. The window includes attempts started or reports
received within its bounds. Budget comparisons use covered reports in the
selected currency and do not change execution policy. Independently reconcile
provider receipts before treating declarations as verified spending.

See [delivery analytics](delivery-analytics.md) for outcome and duration
definitions, and [identity and recovery](identity-and-recovery.md) for access
and version controls.
