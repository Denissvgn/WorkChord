# Interface 1.1

Version 1.1 is the first release of the simplified interface. The 1.0 release was
deferred, so these notes cover the 1.0 interface changes as well as the 1.1 changes.

## What changed for people

### One sidebar and ten destinations

The workspace has one sidebar for the whole app. The three work areas and their
top-bar tabs are gone, and the pages you use every day sit in ten destinations in
a fixed order:

**Overview, My Work, Triage**; then group **Plan**: Projects, Plan, Gantt; then
group **Deliver**: Tasks, Analytics; then group **Setup**: Team, Settings.

The scope bar sits above the page and sets which project, iteration or backlog you
are looking at. On phones it stays at the top of the page.

### Where things moved

Each old place is shown with its new place. "Sidebar" means the destination is a
top-level item in the sidebar.

| Old place | New place |
| --- | --- |
| Delivery Hub: Overview | Overview (sidebar) |
| Delivery Hub: My Work | My Work (sidebar) |
| Delivery Hub: Triage | Triage (sidebar) |
| Delivery Hub: Projects | Projects (sidebar, Plan group) |
| Delivery Hub: Tasks | Tasks (sidebar, Deliver group) |
| Delivery Hub: Agent Pipeline | Tasks, pipeline layout (`/tasks?layout=pipeline`) |
| Timeline & Planning: Plan | Plan (sidebar, Plan group) |
| Timeline & Planning: Gantt | Gantt (sidebar, Plan group) |
| Timeline & Planning: Roadmap | Projects, roadmap view (`/projects?view=roadmap`) |
| Timeline & Planning: Iterations, and iteration capacity | Plan, Iterations panel (`/plan?panel=iterations`) |
| Timeline & Planning: Calendar | Settings, Work calendar section (`/settings?tab=calendar`) |
| Resource & Settings: Team | Team (sidebar, Setup group) |
| Resource & Settings: Analytics | Analytics (sidebar, Deliver group) |
| Resource & Settings: Agent Team Setup, agent connection | Team, Connect tab (`/team?tab=connect`) |
| Resource & Settings: Agent Team Setup, model catalog | Team, Models tab (`/team?tab=models`) |
| Resource & Settings: Settings | Settings (sidebar, Setup group) |
| Top-bar tabs for the three work areas | Sidebar groups: Plan, Deliver and Setup |

Roadmap, the agent pipeline, Iterations, the work calendar and Connect an agent
stay reachable from the command menu (Ctrl/⌘ K).

### Old addresses

Bookmarks and links to these addresses open their new places. Query parameters
you add to an old address are kept on the new one.

| Old address | Opens |
| --- | --- |
| `/plan/master` | `/plan` |
| `/iterations` | `/plan?panel=iterations` |
| `/roadmap` | `/projects?view=roadmap` |
| `/agent-pipeline` | `/tasks?layout=pipeline` |
| `/agent-team/setup` | `/team?tab=connect` |
| `/calendar` | `/settings?tab=calendar`, which the page shows as the Work calendar section |

### Plan's six checkpoints

Plan shows six checkpoints in order, and the counter reads "done of 6":

1. **Iteration**: done when the iteration's start and end dates both fall in the
   year of its work calendar. Otherwise it needs attention.
2. **Team**: done when people are added and each has capacity in the iteration. With
   no people it is next; a person without capacity needs attention.
3. **Work**: done when the iteration has tasks. A parent task that has subtasks is
   counted through its subtasks. With no tasks it is next.
4. **Blockers**: done when no planned, non-deferred task lacks an assignee or effort,
   and no task that an agent is working on lacks an assignee. Otherwise it needs
   attention. Blocked until the iteration has tasks.
5. **Schedule**: done when the first four checkpoints are all done and every planned,
   non-deferred task has effort, a start and an end inside the iteration's dates,
   and a planned start that has not already passed. Deferred work is left out. While
   any earlier checkpoint is not done, Schedule is blocked, even if the tasks
   already have dates. When the earlier checkpoints are done but a task lacks dates,
   Schedule is next. This checks the dates on the tasks; it does not record that a
   schedule was applied.
6. **Review**: done when the schedule is done and no at-risk signal is open: no
   at-risk task, no overloaded person, and no uncertain item. While a signal is
   open, Review needs attention. Blocked until the schedule is done.

Each checkpoint is done, needs attention, is next, or is blocked until an earlier
checkpoint is done. Completing Review does not mean a person has read the plan; it
means the server's checks above pass. The server works these states out, so Plan and
the API agree.

### First run: the Get started steps

A new workspace opens on Overview with a **Get started** panel. It holds six
steps, taken in this order. A step is done when its result exists in the
workspace; nothing is ticked by hand.

1. **Say who you are.** Choose a person profile for this browser. This is a
   choice on this browser, not a verified sign-in. Done on Overview.
2. **Create a project.** Done on Overview.
3. **Create an iteration.** Opens Plan at its Iteration step.
4. **Add capacity.** Say who does the work in the iteration: add yourself,
   connect an agent, or add other profiles. Opens Plan at its Capacity step.
5. **Add tasks.** Add the iteration's work in Plan, from the backlog or by
   import. Opens Plan at its Work step.
6. **Build the schedule.** Build the schedule from the tasks and capacity. Opens
   Plan at its Schedule step. The step is done when Plan's Schedule checkpoint is
   done: the iteration, team, work and blockers checkpoints are done first, and
   then every planned, non-deferred task has effort and dates inside the iteration.
   Dates on the tasks alone do not finish it while an earlier checkpoint is open.

Dismiss hides the panel in this browser. To bring it back, open **Help**, then
**Setup guide**.

#### The sample project

Get started also offers **Load a sample project**. It creates a complete example
to explore: two milestones, two capacity rows (you and a sample agent), eight
linked tasks, and an iteration with a schedule. Open Plan after loading it to look
around.

To remove it, choose **Remove sample data** in the panel. The panel lists every
record the sample created and deletes them, including the sample iteration and
schedule. Your own profile is kept. If a removal stops partway, the records that
remain are listed so you can retry. The scope you had open before the sample was
removed is restored.

## 1.1 changes

### Access and connection

- Connecting the first agent works with the admin key alone.
- The admin key can manage model bindings and read profile presets, so an operator
  with only the admin key can administer models.
- Connect steps say what is wrong, use one name for the agent, and stay reachable
  while the agent waits for its runtime. The Connect handoff stays available until
  the runtime acknowledges it.
- Team shows "Agent status unknown" while the team read is pending or has failed,
  rather than a stale status.
- Team Models has one primary action.
- Changing the admin key keeps the page open. While editing is unlocked, Start work
  and Submit are hidden, and the page and its actions stay true to the state.
- A person who accepts work is recorded by the local person profile chosen in this
  browser. This is a record of the choice, not a verified sign-in.
- Readers without access to a person's full profile still see that person's
  reader-safe part, such as the name and whether the assignee is a person or an agent.

### Planning and delivery

- Plan's hours table refreshes with the page, and Schedule shows hours per assignee.
- Plan reads its checkpoint states and counters from the server.
- Deferred work is left out of the schedule and out of "Every task has dates".
  Calendars that do not cover an iteration's years are flagged.
- A task with calculated dates counts as dated before the schedule is applied.
- "Every task has dates" is judged from the iteration's task list. A parent task
  without subtasks is judged by its own dates.
- A holiday and a short day are shown apart in the work calendar, and a calendar
  must cover the iteration's dates.
- An unstarted task whose planned start has passed names the missed start as the
  reason it is late.
- Plan Review and Edit iteration explain what they need. Update stays disabled until
  an iteration conflict is resolved, and the opened iteration is kept as the
  conflict baseline when the list refreshes.
- Start work is one click, and a task offers dispatch to an agent instead of a
  manual start.
- A task in the at-risk list links to its review, and the list says why the task is
  at risk.
- Brief creation is direct and explains the acceptance requirements. Edit brief and
  Review say what they need.
- Analytics has a Backlog mode and an All projects mode. Each counts only the work
  that matches its mode. Metric lists are paged, so a list shows the same number as
  its count.

### Traceability

- A task can be traced to the code it produced. Agents link the task's branch when
  they begin work, and its commits and pull request when they submit. The links show
  on the task as GitHub links.
- Commits and pull requests name their task, so the trace also works from the code
  back to the task.
- A reviewer checks that the links match the reviewed change before accepting it.
  The PM counts a task as done only when it has a commit or pull request link, or a
  stated reason why no repository changed.
- A shipped release can be linked to its merge pull request or tag.

### Layout and words

- The sidebar fits a 1024 px window, and the scope bar works on phones.
- Release pages use the page frame, and the page header shows when a project or
  release is not found.
- Status groups are translated, and a legacy status and its active status are shown
  as one group.
- Status names are shown, not internal codes.
- Calendar holidays and override dates use neutral marks and hatching.
- Colours keep to their meanings, and metadata badges are neutral.
- Settings search finds labels chosen at run time.
- A saved scope is restored reliably after the sample is removed, and a remembered
  scope survives a pending URL update.
- Accept hints end with a full stop.
- Each interface concept has one name across the pages and the agent role guidance.

## What an operator must do after upgrading

### Role skill packages

Reinstall the three role skill packages at the versions in the server skill catalog
(catalog version 1.18.0). Install each one from the catalog and check its SHA-256
digest against the catalog entry.

| Role package | Version in this release | Previous version |
| --- | --- | --- |
| `workchord-pm` | 1.16.0 | 1.15.0 |
| `workchord-worker` | 1.16.0 | 1.15.0 |
| `workchord-reviewer` | 1.4.0 | 1.3.0 |

If your workspace already runs these versions, nothing needs to be reinstalled.
A runtime that uses the tracked Codex role adapter
(`adapters/codex/workchord-agent-roles`) should take the adapter from this release,
plugin version 1.18.0, which carries the same three role skills. The setup steps for
each runtime are in [agent team setup](../agent-team-setup.md). The example team
file in `config/examples` pins the three versions above; it is an example, not a
setting your workspace reads.

### Database

This release has no database migration. Nothing needs to be run beyond the normal
upgrade, and no server setting or environment variable needs to change.

### Changes for API clients

All of the following are optional and additive. Existing requests keep working.

- `GET /api/tasks/delivery-metrics` and `GET /api/tasks/execution-usage` accept
  `backlog`, `all_projects` and `all_projects_backlog` (boolean, default `false`).
  `all_projects=true` aggregates every accessible project and must be sent without
  `project_id`, `iteration_id` and `backlog=true`; the server rejects the
  combination. `all_projects_backlog=true` limits an all-projects request to work
  with no iteration and is rejected without `all_projects=true`. `backlog=true`
  needs one `project_id` and no `iteration_id`. A request still needs a project, an
  iteration, or `all_projects=true`.
- `GET /api/tasks/metric-matches` accepts `limit` (1 to 500, default 200) and
  `after_id` (default none). Its response adds `has_more` and `next_after_id`; pass
  `next_after_id` as `after_id` to get the next page.
- Task responses name the kind of each assignee in `assignee.kind`: `human`, `agent`
  or `hybrid`, or `null` when it is not known. It is read-only.
- Team member responses embed the reader-safe profile part for every reader, and
  carry `agent_connected` (boolean, read-only): true when an enabled agent is bound
  to the profile. It names no agent.
- These routes under `/api/agent/` accept the `X-Admin-API-Key` header when no
  agent key is sent: `GET /agent/profile-presets`, the model catalog list, create,
  update and disable routes (`GET` and `POST /agent/model-catalog`, `PATCH` and
  `POST .../disable` on `/agent/model-catalog/{catalog_id}`), and all model
  binding routes (`/agent/model-bindings`). Reading one catalog entry and applying
  a profile preset still need an agent key. Agent keys keep working as before.
- `POST /api/agent/me/work/begin` accepts `branch_url`, and
  `POST /api/agent/me/work/submit` accepts `branch_url` and `commit_urls` (a list of
  GitHub commit URLs with the full SHA). Each is optional. WorkChord links them, and the
  existing `pr_url` and `commit_url` fields, to the task as GitHub links in the same command, without
  changing the task's version, and skips links the task already has. Servers that
  support this list `work-delivery-links-v1` in their features.
- GitHub links accept commit URLs (full SHA only) and release tag URLs. The MCP tool
  `workspace_create_release_github_link` links a release to its merge pull request
  or tag. A GitHub link that already exists on the task or release is reported as a
  structured conflict.

Check the current API schemas when you update a client.
