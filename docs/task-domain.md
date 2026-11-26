# Tasks, briefs and delivery

Tasks can belong to a project backlog before they are committed to an iteration. A task keeps its ID and human owner when its schedule commitment changes. Neither ownership field authenticates a caller.

## Names people see

The interface uses these names on tasks:

- **Assignee**: the person or agent that does the task. It is the iteration
  capacity allocation behind `assignee_id`.
- **Reviewer**: the person or agent that checks the work and its evidence.
- **Owner**: the durable human owner, `owner_profile_id`. A task shows it when
  that person differs from the Assignee. Projects and initiatives have one owner
  each, shown as **Owner** on their own pages.
- **Labels**: names that organize tasks and requests.
- **Waits for**: the prerequisite tasks that must finish before this task can start.
  These are local schedule dependencies, separate from delivery prerequisites.
- **Earliest start** and **Due by**: the date limits for the task, the earliest
  day it may start and the latest day it should finish.
- **Effort**: entered in hours. The day equivalent is shown as a hint, using the
  calendar's nominal workday.

## Capture and schedule

`POST /api/projects/{project_id}/backlog` accepts the task creation contract without an iteration. Existing `POST /api/iterations/{iteration_id}/tasks` requests retain their iteration scope. Backlog tasks require a project and cannot have a capacity allocation.

`GET /api/tasks/{task_id}/actions` returns permitted commands and reasons unavailable commands cannot run. `POST /api/tasks/{task_id}/commands` takes an action, `expected_version` and a reason. Available actions include manual start and resolution, blocking, cancellation, reopening, and committing or returning work to the project backlog. A commitment also supplies `iteration_id`.

Cancellation retains lifecycle history and invalidates agent execution ownership. Canceling an active claim requires the current claim generation, running run IDs and live assignment IDs returned by the actions endpoint. Reopening invalidates current acceptance. Agent execution continues through the assigned-work protocol with its current claim fence; manual execution is for humans.

## Deferred and optional work

`is_deferred` and `is_optional` are scheduling policy fields inherited through a task's complete ancestry. Deferred leaves are excluded from active required work and ordinary queue/execution eligibility. Optional leaves remain distinguishable from required commitments. Structural parents do not add delivered work; canceled and deferred work do not increase required completion or acceptance denominators. Deferral retains identity, content and history. Use the current actions projection to determine which commands are available after policy or ownership changes.

Scheduling day boundaries use the project's IANA timezone, with the availability calendar used for work without a project. An author's recorded-time work date remains an explicit local date with its separately selected timezone. Capacity reflects current shared calendars and absences; task recovery points restore their supported planning state while those shared inputs remain current.

## Estimates

`effort_hours` is authoritative; it is the value people enter in the task form. `effort_days` is derived using `nominal_day_hours`, independent of personal availability and productivity coefficients, and the form shows it as a hint. A calendar declares its nominal workday; the compatibility default is eight hours. Inputs supplying both units must agree. Hours are rounded to six decimal places.

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

Under `require_different_review_publisher`, ordinary acceptance needs a pass from an assigned agent verifier with a verified publisher, so a person's review is refused with `verified_publisher_review_required`. A signed-in workspace owner or operator can accept one resolved task anyway with `POST /api/tasks/{task_id}/owner-acceptance` and `{expected_version, brief_revision, artifact_revision, reason, evidence}`. The request needs the task's current version and brief and artifact revisions, and a non-empty `reason`. The project policy stays on: the override covers only that task at those revisions in that request, and every other task in the project still needs a verified publisher. All other acceptance checks still apply: current criterion evidence, delivery prerequisites, work-package verification and replacement holds. An owner who executed the work or authored its current evidence must also send `X-Review-Override: true`; the body `reason` is the reason recorded for it. On this path the header waives only that self-review rule, never criterion evidence or any other check. The admin API key and a trusted-local install with no signed-in person cannot use this path; sign in as an owner or operator first. The command refuses:

- `owner_acceptance_required`: the caller is not a signed-in human workspace owner or operator. A project manager, a reviewer, an agent, the operator API key, a paired observer and a trusted-local browser with no signed-in person are all refused.
- `override_reason_required` (or a validation error): the reason is missing or blank.
- `owner_override_not_required`: the project does not require a different review publisher. Use an ordinary review instead.

The acceptance is recorded as an owner override, never as an independent review. In `GET /api/tasks/{task_id}/reviews` and `/reviews/current` its `kind` is `owner_override`; ordinary reviews have `kind` `review`. The task timeline gets an `owner_acceptance_override` event with the reason. Every command audit row the request writes carries the reason and `owner_acceptance_override_task_ids`. In `GET /api/tasks/delivery-metrics`, `owner_override_acceptance_events` counts these acceptances separately. They are still included in `acceptance_events`.

## Manual provenance for work resolved outside recorded runs

Under `require_different_review_publisher`, a verifier needs to know who executed the work. Work that was implemented locally and merged as a pull request outside WorkChord runs, and then marked resolved, has no runs and no authenticated `start_manual`/`resolve_manual` history, so a verification assignment is refused with `verification_publisher_unverifiable`. Recording manual execution afterwards is not possible, because `start_manual` needs planned work. Record its provenance instead. The task stays resolved, and a normal independent review follows.

Send `POST /api/tasks/{task_id}/manual-provenance`, `POST /api/agent/planning/tasks/{task_id}/manual-provenance` with the usual planning command headers, or the MCP tool `agent_record_manual_provenance`, with `{expected_version, artifact_revision, executor, head_commit_url, commit_urls, pr_url, base_commit_url, reason}`:

- `executor` names who executed the work: `{"kind": "human", "principal_id": ...}` or `{"kind": "agent", "actor_id": ..., "model_binding_id": ...}`. A human's linked profile counts as theirs. An agent's profile, model binding and publisher are captured at the moment of the record. Without `model_binding_id`, the actor's default binding is used. An agent whose binding has no publisher, or an actor without a profile, is refused with `manual_provenance_executor_unattributable`.
- `head_commit_url` is the delivered head as an immutable GitHub commit. `commit_urls` lists every commit the executor contributed; the head is always included. The verifier's candidate check requires every commit in the pull request or range to be one of them.
- `pr_url` names the pull request that carries the head, or `base_commit_url` names the commit the work started from. One of them is required.
- `artifact_revision` must be the task's current artifact revision, and `reason` says why the work ran outside recorded runs.

Only a signed-in workspace owner or operator, a project manager, or the project's PM agent can record provenance. The operator API key, a trusted-local browser with no signed-in person and a paired observer are refused with `provenance_recorder_required`. The task must be resolved, uncanceled leaf work (`manual_provenance_requires_resolved_work`) with no agent runs, claims, live or fulfilled execution assignments, or authenticated manual execution of the current artifact (`manual_provenance_execution_recorded`); such execution supplies its own provenance. Stale versions and revisions, malformed URLs and a candidate that cannot be verified are refused with 409 or 422.

The record does not change status, progress or evidence, and it does not reopen or accept the task. The task's version advances, the response returns the record, and the task timeline gets a `manual_provenance_recorded` event with the recorder, executor, commits and reason. Every command audit row of the request carries the reason. Review uses the latest record while the task's brief and artifact revisions stay the same; a later artifact or brief change makes the record stale. A human executor is reviewed like authenticated manual execution: the verifier must be a separate automation-enabled verification profile. An agent executor is an ordinary contributor: a verifier with the executor's actor, profile or publisher fails independence (`verification_publisher_not_independent` for the publisher).

A verification assignment whose candidate is already known to be unverifiable is not created. It is refused with `verification_candidate_unverifiable`; `missing` names the absent facts. When the task has no recorded runs, `remedy` points at the manual provenance command. When manual execution is missing, the `verification_publisher_unverifiable` refusal includes the same `remedy`.

## Clean replacement of unattributable work

Under `require_different_review_publisher`, every run of a task counts as a contributor, and a reviewer needs a known publisher that differs from every contributor's. A task whose runs were executed without a model binding therefore can never be accepted. When its work must be done again, the project's PM actor or a project manager or workspace operator records a clean replacement instead of rerunning the same task.

Create the replacement as an ordinary planned task in the same project (and the same milestone, if any; in the same iteration when the original has schedule dependents). Then send `POST /api/tasks/{original_id}/replacement`, `POST /api/agent/planning/tasks/{original_id}/replacement` with the usual planning command headers, or the MCP tool `agent_record_task_replacement`, with `{replacement_task_id, expected_original_version, expected_replacement_version, reason, owner_decision, base_commit_url, carried_run_ids}`:

- `owner_decision` records the owner's decision that authorizes the replacement; `reason` says why the original cannot be attributed.
- `base_commit_url` is the immutable GitHub commit the replacement is built from.
- `carried_run_ids` lists the original's runs whose commits the replacement reuses. Send an empty list for a clean rebuild.

The original must be unaccepted leaf work without live execution, and the replacement must be planned work with no attempts, assignments or acceptance. The command keeps the original with its attempts, artifacts and unknown attribution, withdraws it from delivery counts as replaced work, points its schedule and delivery dependents at the replacement, and adds the replacement to open releases that listed the original. The original's version changes; the replacement, its dependents and unrelated work keep theirs, so work already issued for them stays valid.

Only the replacement can be accepted. The original cannot be reviewed, accepted or reopened. The replacement is reviewed on its own runs plus every carried run, so a replacement that carries commits from an unattributed run stays held: verification assignment fails with `replacement_contribution_unattributed`, and acceptance is refused under any review policy. A carried run with attribution is an ordinary contributor, and its commits count as attributed in the candidate check. Under any review policy, the actor and profile that executed a carried run cannot verify the replacement. A replacement whose own work later proves unattributable can itself be replaced; runs carried from it bring along whatever it carried in turn.

`GET /api/tasks/{task_id}/replacement`, `GET /api/agent/planning/tasks/{task_id}/replacement` or `agent_get_task_replacement` returns the disposition for either task: who decided, when and why, the owner decision, the review policy at the decision and now, the original's attempts with their missing attribution, the replacement's recorded base and current submitted candidate and contributors, the carried contributions, the moved dependents and releases, and whether the deliverable is clean or held. A task that takes part in a disposition cannot be deleted. An iteration or backlog restore that would change such a task's canceled state or status, or any dependency that touches one, is refused with `restore_conflicts_with_task_replacement`; restore a snapshot taken after the replacement instead.

## External links

`POST /api/tasks/{task_id}/external-links` attaches a link to a task with a provider: `github`, `gitlab`, `figma`, `sentry`, `custom` or `agdash`. Display links must be absolute http(s) URLs without credentials, and private or loopback hosts are refused. The one exception is an `agdash` link, which names an agent session observed on one computer: it may point at a loopback host (`localhost`, `127.0.0.1` or `[::1]`), because the server never fetches display links, and it opens only on the computer that observed the session. Private network addresses stay refused for it too. Repeating an `agdash` link with the same `external_key` on the same task returns the existing link instead of adding another. An update that changes the provider or URL is checked against the resulting pair. Creating a link needs edit access to the task.

## Bounded reads and recovery

`GET /api/tasks/{task_id}/detail` returns the task with bounded parent, child and dependency context. Child and dependency pages expose `has_more` and `next_after_id`; parent context exposes its completeness. This UI projection explicitly declares that it is not complete execution context. `GET /api/tasks/lookup` supports project, iteration, backlog and text filters with deterministic ID pagination. These pages describe live data, not a fixed snapshot. Foreground work, discussion, notifications and recorded-time lists refresh the current head and at most four retained pages. Use explicit reload for older pages or changed filters. Loading errors expose retry; authentication or access loss clears private rows and actions. A write with an unknown outcome requires current-state comparison before an explicit retry.

`GET /api/tasks/review-queue` lists independently reviewable resolved work within the caller's review scope. Owner selectors use `/api/tasks/owner-options`, which returns public display information for eligible human owners.

Project backlog recovery points use the same transactional database snapshot store as iteration recovery. List them at `/api/projects/{project_id}/backlog/snapshots`. Restore with `/api/projects/{project_id}/backlog/snapshots/{snapshot_id}/restore`, supplying the complete current task-version map and a reason. Restore preserves task identity and immutable brief history while invalidating current progress and acceptance. Application snapshots do not replace a complete database backup.

Task deletion retains a durable version fence in the same transaction, including deleted subtasks. Scheduled and backlog restoration allocate versions above the saved task, current task, deletion fence and retained history, so an old editor cannot overwrite restored work. If a task was deleted before its last version was recorded, restoring its ID returns HTTP 409 with code `snapshot_version_history_unknown`. Recover that data from a complete database backup and its matching application image; an application snapshot alone cannot establish a safe version.

Moving backlog work between projects requires edit permission in both projects. The complete subtree must retain all its dependencies within the destination scope; moves that strand incoming or outgoing dependencies are rejected atomically. Project summaries include nested backlog leaves and count explicit blocks as well as unavailable prerequisites.

## Compatibility and migration

`GET /api/tasks/capabilities` reports installed domain support and backfill readiness. REST and MCP share action and capability projections. Existing task update versions remain optional on supported legacy routes while `STRICT_MUTATION_VERSIONS=false`; strict mode requires observed versions and revisions. New explicit commands require their supplied versions in either mode. A supplied stale version is rejected in both modes. Compare retained intent with current state before applying again.

The legacy `/api/triage/{triage_item_id}/convert-to-task` endpoint still requires `iteration_id`. Unscheduled conversion uses the explicit `/api/triage/{triage_item_id}/convert-to-backlog` endpoint and requires `project_id`.

### Source links on requests and tasks

Requests (triage items) and tasks share one source link policy. A source link is displayed, never fetched, and may be a public `http(s)` address, a path inside this instance such as `/tasks?project=6`, or an address of this same instance. This instance means a loopback host (`localhost`, `*.localhost`, `127.0.0.0/8`, `::1`, on any port) or the host and port of the optional `PUBLIC_BASE_URL` setting. An address of this instance is stored as its relative path, so it keeps working wherever the instance is opened. Private, link-local and reserved addresses, other schemes, protocol-relative paths and embedded credentials are refused.

- Creating or editing a request through `POST /api/triage`, `PUT /api/triage/{triage_item_id}`, the controlled web intake, the agent planning routes or the MCP tools `workspace_create_triage_item` and `workspace_update_triage_item` returns a refused link as HTTP 400 (MCP: the tool error) with the named code `intake_source_link_not_allowed`. The body carries `field` (`source_url`), a `message` and a `next_step`. The Triage page shows the same text beside the Source URL field.
- `convert-to-task` and `convert-to-backlog` (and their MCP and agent planning equivalents) never fail on the link. A link to this instance is carried to the task as a relative path; a refused link is left off the task. Either change is reported in the response under `source_link` as `{action: "rewritten" | "dropped", original, task_source_url, message}`; the field is absent when the link was carried over unchanged or there was none. The request keeps its original link.
- Requests stored before this policy that hold such a link stay readable, editable (an unchanged link is accepted as stored) and convertible.

Operators can inspect paginated backfill diagnostics at `/api/tasks/migration-diagnostics`. The migration preserves IDs and original values, and backfill completion markers allow completed rows to remain unchanged on resumption. SQLite rebuilds are transactional and verify foreign-key integrity before committing. Removing the expanded schema would lose backlog, ownership and review information; rollback requires a complete backup and the matching application image.
