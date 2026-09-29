# Tasks, briefs and delivery

Tasks can belong to a project backlog before they are committed to an iteration. A task keeps its ID and human owner when its schedule commitment changes. `owner_profile_id` identifies the durable human owner; `assignee_id` identifies an iteration capacity allocation. Neither field authenticates a caller.

## Capture and schedule

`POST /api/projects/{project_id}/backlog` accepts the task creation contract without an iteration. Existing `POST /api/iterations/{iteration_id}/tasks` requests retain their iteration scope. Backlog tasks require a project and cannot have a capacity allocation.

`GET /api/tasks/{task_id}/actions` returns permitted commands and reasons unavailable commands cannot run. `POST /api/tasks/{task_id}/commands` takes an action, `expected_version` and a reason. Available actions include manual start and resolution, blocking, cancellation, reopening, and committing or returning work to the project backlog. A commitment also supplies `iteration_id`.

Cancellation retains lifecycle history and invalidates agent execution ownership. Canceling an active claim requires the current claim generation, running run IDs and live assignment IDs returned by the actions endpoint. Reopening invalidates current acceptance. Agent execution continues through the assigned-work protocol with its current claim fence; manual execution is for humans.

## Estimates

`effort_hours` is authoritative. `effort_days` is derived using `nominal_day_hours`, independent of personal availability and productivity coefficients. A calendar declares its nominal workday; the compatibility default is eight hours. Inputs supplying both units must agree. Hours are rounded to six decimal places.

Unknown effort is `null`; zero is a known zero. `estimate_provenance` distinguishes `unknown`, `assumed` and `estimated`. Forecast scheduling requires a positive estimate and reports unavailable work and prerequisites explicitly. Manual human work can start without an estimate or forecast dates.

Changing an iteration's calendar refreshes the nominal workday and derived days for its tasks while retaining authoritative hours and estimate provenance.

New tasks retain unknown effort until an estimate is supplied. A capacity allocation does not imply a human owner. Preserved historical provenance remains distinct from explicit ownership and estimates.

## Briefs and evidence

The `brief` object contains a schema version, goal, context, scope, exclusions, acceptance criteria, verification approach and artifact expectations. Each criterion has a stable ID and a content revision. Reordering preserves the ID; changing its wording or verification increments its revision. Brief edits use the existing task version and invalidate stale execution context.

`PUT /api/tasks/{task_id}/brief` accepts `{expected_version, brief}`. Legacy descriptions remain editable until deliberately converted. `POST /api/tasks/{task_id}/brief/convert` previews conversion by default; `apply: true` applies it with the supplied version. Supported English and Russian headings and checklist items are parsed conservatively. Original text and unresolved conversion notes remain available. Historical checkmarks do not establish acceptance.

After conversion, Markdown is derived from the canonical brief. A conflicting legacy description write is rejected. AI suggestions and template defaults supply draft fields; the user chooses which fields to apply.

A template's structured brief takes precedence over its legacy description and checklist. Applying it to a new task preserves its content and creates new criterion IDs at revision 1. Dependency changes invalidate current progress and acceptance through both task updates and individual dependency commands; prior evidence remains in history.

`POST /api/tasks/{task_id}/progress` saves criterion states, evidence and artifact links separately from acceptance. It requires the current task version and criterion revisions. An agent supplies criterion progress through its fenced assigned-work submission.

`POST /api/tasks/{task_id}/review` records an independent acceptance or rejection with the current task, brief and artifact revisions and a reason. A reviewer cannot accept work they executed or whose current progress evidence they authored. Existing privileged override policy requires explicit operator authority and a recorded reason. Ordinary task review cannot replace a work package's trusted verifier protocol; package verification is bound to its captured task, brief and artifact context. Historical verdicts remain available after later edits invalidate acceptance.

## Bounded reads and recovery

`GET /api/tasks/{task_id}/detail` returns the task with bounded parent, child and dependency context. Child and dependency pages expose `has_more` and `next_after_id`; parent context exposes its completeness. This UI projection explicitly declares that it is not complete execution context. `GET /api/tasks/lookup` supports project, iteration, backlog and text filters with deterministic ID pagination. These pages describe live data, not a fixed snapshot.

`GET /api/tasks/review-queue` lists independently reviewable resolved work within the caller's review scope. Owner selectors use `/api/tasks/owner-options`, which returns public display information for eligible human owners.

Project backlog recovery points use the same transactional database snapshot store as iteration recovery. List them at `/api/projects/{project_id}/backlog/snapshots`. Restore with `/api/projects/{project_id}/backlog/snapshots/{snapshot_id}/restore`, supplying the complete current task-version map and a reason. Restore preserves task identity and immutable brief history while invalidating current progress and acceptance. Application snapshots do not replace a complete database backup.

Task deletion retains a durable version fence in the same transaction, including deleted subtasks. Scheduled and backlog restoration allocate versions above the saved task, current task, deletion fence and retained history, so an old editor cannot overwrite restored work. If a task was deleted before its last version was recorded, restoring its ID returns HTTP 409 with code `snapshot_version_history_unknown`. Recover that data from a complete database backup and its matching application image; an application snapshot alone cannot establish a safe version.

Moving backlog work between projects requires edit permission in both projects. The complete subtree must retain all its dependencies within the destination scope; moves that strand incoming or outgoing dependencies are rejected atomically. Project summaries include nested backlog leaves and count explicit blocks as well as unavailable prerequisites.

## Compatibility and migration

`GET /api/tasks/capabilities` reports installed domain support and backfill readiness. REST and MCP share action and capability projections. Existing task update versions remain optional on supported legacy routes; new explicit commands require their supplied versions.

The legacy `/api/triage/{triage_item_id}/convert-to-task` endpoint still requires `iteration_id`. Unscheduled conversion uses the explicit `/api/triage/{triage_item_id}/convert-to-backlog` endpoint and requires `project_id`.

Operators can inspect paginated backfill diagnostics at `/api/tasks/migration-diagnostics`. The migration preserves IDs and original values, and backfill completion markers allow completed rows to remain unchanged on resumption. SQLite rebuilds are transactional and verify foreign-key integrity before committing. Removing the expanded schema would lose backlog, ownership and review information; rollback requires a complete backup and the matching application image.
