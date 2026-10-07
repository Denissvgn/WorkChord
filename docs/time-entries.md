# Recorded time

Time entry is optional. Set `TIME_ENTRIES_ENABLED=true`, apply the database upgrade with `./scripts/upgrade_database.sh`, and restart the backend. Human sign-in is required; trusted-local guest identity and agent credentials cannot author personal work records. Disabling the setting hides the feature and blocks its API without deleting records. Re-enable it to access retained records.

Record whole minutes, an explicit local work date, and an IANA timezone such as `Europe/Madrid` or `UTC`. Dates describe the author's selected work date; server creation and correction timestamps are UTC instants. A record contains 1–1,440 minutes, and an author's active records for one work date cannot exceed 1,440 minutes across projects.

Every record belongs to an explicit project and its signed-in author. It may describe project work without a task, or leaf task work in that project. Individual records, notes and correction history are private to their author and require current project access. Workspace ownership does not expose another person's records through this API. Operators with physical database or backup access remain trusted administrators.

Create records through `POST /api/time-entries` using a unique UUID `request_id`. Retrying the same payload returns the existing record's current state; reusing that ID for different content returns a structured conflict. Corrections use `PUT /api/time-entries/{entry_id}` with `expected_version` and a reason. Void mistakes through `POST /api/time-entries/{entry_id}/void`; voided records remain in history and no longer contribute recorded minutes. Stale corrections return HTTP 409 with the author's current record. Never silently retry a stale correction against a newer version.

Read personal records through bounded `GET /api/time-entries` pages, optionally filtered by project, task or work-date range. Carry `upper_id` and `next_after_id` until `has_more` is false. Changing filters starts a fresh live read. `GET /api/time-entries/{entry_id}/history` provides bounded correction history. Interactive API documentation describes the complete payloads.

Project, task and author associations are retained as recording-scope identities. Moving or deleting tasks does not move their recorded time into another project or erase corrections. Correct the minutes, date, timezone or note; void and record a new entry to change an association. Application task snapshots do not rewind this ledger. Full authorized database backups retain records and their history; task exports are not backups of personal time.

Recorded time is distinct from estimates, calendar capacity, provider usage and lead/cycle time. Missing records do not mean zero work, and task status changes do not manufacture historical hours. Recording time does not start, resolve or accept a task and does not change scheduling revisions. This capability does not provide billing or payroll.

## Entry and reporting workflow

Open **Time entries** in a task editor to record or correct your work. Project details also provide **Recorded time and estimates**, with date filters, your personal records and project work without a task. Corrections and voids require a reason. On a version conflict, reload the saved entry, compare it with your retained draft and explicitly adopt the current version before saving again.

Reports default to **My recorded time**. Project managers can select **Project totals** for aggregated recorded minutes and coverage, without another author's individual records, notes or correction history. Coverage means that a task has some records in the selected period; it does not prove all its work was recorded. Current task estimates describe the full task and may differ from estimates at recording time. A moved or deleted task retains its original recording label and minutes in the original project, with its current estimate unavailable.

`GET /api/time-entries/report` returns bounded task rows and independent whole-scope totals for an ordered work-date range of at most 366 days. Carry the page's `upper_id`; totals remain live and are not calculated from the displayed page. Project work without a task is shown separately. Unknown recorded time or estimates remain blank/unknown rather than zero.

Use **Export my entries** for your personal records, including void markers and observed versions, or **Export totals** for the selected report scope. `GET /api/time-entries/export` provides CSV with at most 5,000 rows; larger exports fail explicitly. CSV exports preserve minute units and empty unknown values, and neutralize spreadsheet-formula prefixes in text. Personal exports never include another author's records, even for a project manager. CSV exports are reconciliation views, not a substitute for a full database backup or complete correction history.

See [identity and recovery](identity-and-recovery.md), [task semantics](task-domain.md), and [database backup and restore](runbooks/postgresql-backup-restore.md).
