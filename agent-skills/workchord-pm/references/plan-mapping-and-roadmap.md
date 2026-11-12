# Plan Mapping and Roadmap

Use this reference when the work already exists as a plan outside WorkChord, such as a plan document, a task index, or a generated task file, and you must load it so that people can read it on the Roadmap, the plan page, the task list, and the Gantt chart. Use it also to check a plan that someone else loaded.

## Contents

- [Know what a loaded plan looks like](#know-what-a-loaded-plan-looks-like)
- [Map each plan concept to a record](#map-each-plan-concept-to-a-record)
- [Staff the iteration with the agents that do the work](#staff-the-iteration-with-the-agents-that-do-the-work)
- [Choose the assignee of each task](#choose-the-assignee-of-each-task)
- [Load in this order](#load-in-this-order)
- [Keep the schedule calculated](#keep-the-schedule-calculated)
- [Keep the Roadmap true](#keep-the-roadmap-true)
- [Check the plan before you report it](#check-the-plan-before-you-report-it)
- [Shortcuts that leave the plan unreadable](#shortcuts-that-leave-the-plan-unreadable)
- [When an operator imports the plan](#when-an-operator-imports-the-plan)

## Know What a Loaded Plan Looks Like

Loading tasks is one fifth of the job. A person judges the plan in five places, and each place reads different records:

| Where people look | What they must see | Records that produce it |
| --- | --- | --- |
| Roadmap | A dated bar for every project under its initiative, with milestone markers | Project `start_date` and `target_date`; milestone `target_date` |
| Projects | Status that matches reality, a health value, an owner | Project `status`, `health`, `owner_profile_id`; project updates |
| Plan page | 6 of 6 checkpoints | Capacity rows, assigned leaves with effort, an applied schedule |
| Tasks | An assignee on every planned leaf and a milestone on every task that belongs to one | `assignee_id`, `milestone_id` |
| Gantt chart | A calculated bar for every planned leaf, and one sequence per assignee | Schedule preview and apply |

A project with no dates and no dated milestone has no bar on the Roadmap, however many tasks it holds. A task without an assignee has no calculated dates, so the Gantt chart cannot show when it happens.

## Map Each Plan Concept to a Record

Give every fact in the source plan one WorkChord record. A tag may repeat a fact as a filter; it must never be the only place the fact lives, because people cannot group, date, assign, or schedule by a tag.

| Plan concept | WorkChord record | Not |
| --- | --- | --- |
| Programme or theme that spans projects | Initiative, linked through the project's `initiative_id` | A tag or a title prefix |
| Deliverable with an owner and a target | Project with `start_date`, `target_date`, `status`, and `owner_profile_id` | An iteration name |
| Phase, stage, or intermediate outcome | Milestone record with a `target_date`, and `milestone_id` on its tasks | A `phase:*` or `milestone:*` tag, or an ID prefix |
| Shipping or rollout boundary | Release record | A milestone |
| Period in which the work is done | Iteration with a calendar | A project date range |
| The plan's own task ID | `external_key`; you may also prefix the title with it | The WorkChord task ID |
| Task text | Typed `brief` | Description only |
| Estimate | `effort_hours` | Start and end dates |
| "B needs A first" | `depends_on` on B | Prose, sort order, or priority |
| "Not before this date", "no later than this date" | `min_start_date`, `max_end_date` | `start_date`, `end_date` |
| The person, agent, or model that does the task | Capacity row in `assignee_id`, then an agent assignment at dispatch | A `model:*`, `agent:*`, or `owner:*` tag |
| Reviewer | The reviewer profile's capacity row, `reviewer_profile_id` on the execution assignment, then a verification assignment after submit | A sentence in the brief only |
| Difficulty band or model tier | Routing assessment when the server advertises model-aware routing; otherwise the headed paragraph in the brief's `context` | A `band:*` or `effort:*` tag |
| Kind of work | The governed `agent` label plus one active `cap:*` label | A free-text class tag only |
| Dates written in the source plan | Nothing. The scheduler calculates dates. | `start_date`, `end_date` |

When the source plan carries a real external date, record it as a constraint or as a milestone or project target, and name its source in the brief.

## Staff the Iteration with the Agents That Do the Work

An agent team is staffed like a team of people: each agent that carries work has a reusable profile, and that profile has one capacity row in the iteration.

Three server rules decide the shape:

- An agent is bound to at most one profile. An operator sets the binding; you read it on the agent roster.
- An iteration holds at most one capacity row per profile.
- The scheduler places one row's tasks one after another and places different rows side by side. An agent also works on one task at a time. So a row is an agent's queue, and the Gantt chart grouped by assignee shows what each agent does next.

When two agents share one profile, they share one row, and the schedule shows their work as one sequence. Ask the operator for a profile per agent when they must work side by side.

1. Read the agent roster. List every enabled worker and reviewer with its profile binding. An agent without a profile cannot carry planned effort; ask the operator to bind it.
2. Read each profile. An agent profile has kind `agent` or `hybrid`, automation enabled, and an assignment mode of `execution` for workers or `verification` for reviewers. Enforced model-aware routing refuses anything else with `profile_kind_human`, `profile_automation_disabled`, or `profile_assignment_mode_missing`.
3. Create one capacity row per profile and pass its `profile_id`. A row created without `profile_id` is matched to a profile by email or name, and otherwise creates a new human profile that no agent is bound to.
4. Set `availability_percent`, `operational_utilization`, and `professionalism_coefficient` from the team's policy. New rows reserve 20 percent for operations; keep that only when the agent really has other duties in this period.
5. Add the reviewer profiles as rows too. Verification routing finds a reviewer's row by its profile, and review load is then visible beside the work.
6. Add a row for every person who carries a task, such as a sign-off or a manual step.
7. Read `plan-readiness` and require the `team` checkpoint to be `done`.

## Choose the Assignee of Each Task

Set `assignee_id` to the row of the profile whose agent you intend to dispatch. The server holds you to it later: an execution assignment's `team_member_id` must equal the task's assignee, and under enforced model-aware routing the dispatched agent's profile must equal the assignee row's profile. It reports a gap as `capacity_owner_missing` or `actor_capacity_profile_mismatch`.

- When the source plan names a model or tier per task, find the agent bound to it and assign that agent's row. Do not keep the choice in a tag.
- When the plan names a ladder of fallbacks, assign the first rung. A later escalation is a reassignment to the next row followed by a new schedule preview.
- When the plan names nobody, ask a person who should take the tasks. Group the leaves by capability label, read the assignee recommendations and each row's workload, propose a row per group, and assign only after the person answers. The question and its record are described in [Prepare the team for the plan](team-capacity-and-calendar.md#prepare-the-team-for-the-plan).
- Assign a person's task to that person's row, without the `agent` label.

Choose the reviewer in the same pass. The reviewer's profile must differ from the assignee's profile; enforced model-aware routing refuses the review otherwise with `verification_profile_not_independent`. Record the choice under "Handoff and escalation" in the brief and pass it as `reviewer_profile_id` when you create the execution assignment.

## Load in This Order

Each step is one audited command per record, in the order below. Derive each idempotency key from the plan's own ID for the record, so that a second run of the same load changes nothing.

1. **Authority.** Confirm `planning:write` and `team:write`. Without `team:write` you cannot staff the iteration; stop and name the person who must.
2. **Project.** Create or update it with `start_date`, `target_date`, `owner_profile_id`, and `initiative_id`. Select an existing initiative. The agent contract has no initiative command, so ask a person to create a missing one.
3. **Milestones.** Create one record per phase or intermediate outcome, with the target date the plan commits to. Leave the date empty when the plan commits to none; step 9 fills it.
4. **Iteration.** Create it with a calendar that covers its dates. Start it on the day work may begin: no task can start, and no date is calculated, before the iteration starts.
5. **People and capacity.** Prepare the team: check the existing profiles, rows, and agents against the workers the plan names, add the missing ones, and ask a person who takes the tasks for which the plan names nobody. Read `plan-readiness` until `team` is `done`.
6. **Tasks.** Create predecessors before the tasks that depend on them, because `depends_on` takes WorkChord task IDs. Send for each leaf: `title`, typed `brief`, `effort_hours`, `priority`, `assignee_id`, `milestone_id`, `project_id`, `depends_on`, `tags`, `external_key`, and `source`. Send `min_start_date` or `max_end_date` only for a real constraint. Send no `start_date` and no `end_date`.
7. **Compare.** Re-read the iteration's tasks. Every plan ID appears once as an `external_key`, and the dependency edges equal the plan's. `depends_on` works inside one iteration; when a task waits for work in another iteration, ask a person to record the delivery prerequisite unless the live contract gives you a command for it.
8. **Schedule.** Preview, read every `unscheduled` entry with its reason code, correct the input it names, and apply.
9. **Roadmap.** Read the calculated end of each milestone's last task. Fill an empty milestone `target_date` with it. When a committed date is earlier than the calculated end, report the gap; do not move the commitment.
10. **Check.** Run [Check the plan before you report it](#check-the-plan-before-you-report-it).
11. **Dispatch.** Only now create agent assignments, with `team_member_id` equal to the task's assignee and `reviewer_profile_id` set. Give each agent's queue the order its row has on the Gantt chart.
12. **Report.** Publish a project update with the plan size, the calculated end, and the open risks.

## Keep the Schedule Calculated

The server refuses to begin work on a task with `schedule_missing` when the task has no dates. That is an answer from the plan, not an obstacle to remove: the task was never scheduled, usually because it has no assignee or no effort value. Fix the input and schedule. Do not write dates to clear it.

The schedule you apply is a forecast. What keeps the order of the work is the dependency links and each agent's queue:

- When the server advertises `schedule-follows-actuals-v1`, an agent begins a task as soon as its dependencies are done, whatever its calculated date. The server then moves that task to today and recalculates the planned work behind it, and does the same when the task is submitted. Agents that work faster than the estimates never wait for the calendar, and the Gantt chart keeps showing what is true.
- Record every real ordering rule as a dependency. An order that exists only in the dates is not enforced.
- Record a real "not before" as `min_start_date` on the task or as the assignment's not-before time. The server holds such a task back with `min_start_future` or `not_before_future`.
- On an older server, a task waits for its calculated start date (`scheduled_start_future`), and finishing early frees nothing. Tell the person who owns the plan; do not write dates to work around it.

A calculation you run moves Planned leaves only. Tasks that are Active, Implemented, or Accepted keep their dates. Preview again after every change to an assignee, effort value, dependency, constraint, capacity row, or vacation.

## Keep the Roadmap True

The Roadmap reads project and milestone records, never tasks. Update them as the work moves:

| Record | Set | When |
| --- | --- | --- |
| Project `status` | `planned` → `active` | The first task of the project starts |
| Project `status` | `completed`, `paused`, or `canceled` | The outcome is accepted, on hold, or dropped |
| Project `health` | `on_track`, `at_risk`, or `off_track` | With every project update; `unknown` is valid only before the first update |
| Project `target_date` | The committed date | At planning; later only with the owner's recorded approval |
| Milestone `status` | `active`, then `completed` | Its first task starts; its last task is Accepted |
| Milestone `target_date` | The committed or calculated date | At planning, and after a schedule change that the owner accepted |

Initiative owner, health, and target date belong to a person. Report an initiative that has none of them as a gap in your project update.

## Check the Plan Before You Report It

Read these values and put them in your report. A plan passes when every row holds.

| Check | Read | Pass |
| --- | --- | --- |
| Roadmap bar | Project | `start_date` and `target_date` are set |
| Project ownership | Project | `owner_profile_id` is set, and `status` matches the work |
| Milestones | Project milestones | One record per plan phase, each with a `target_date` |
| People and capacity | `plan-readiness` | `team` is `done`; every row has a profile |
| Agent rows | Agent roster and iteration team | Every agent you will dispatch is bound to a profile that has a row |
| Assignees | `plan-readiness` | `tasks_without_assignee` is `0` |
| Estimates | `plan-readiness` | `tasks_without_effort` is `0` |
| Milestone links | Tasks | Every task of a plan phase has that `milestone_id` |
| Dependencies | Tasks | The edges equal the source plan's |
| Schedule | Schedule preview | `unscheduled` is empty, or each entry has a recorded reason and owner |
| Checkpoints | `plan-readiness` | 6 of 6. When `review` is `warn`, report 5 of 6 and name every risk it counts |
| Gantt chart | Iteration Gantt | Every planned leaf has dates; no leaf is dated without an assignee |

Report the result as numbers: tasks, assigned, scheduled, milestones, calculated end, and "n of 6". When a row fails, name it, the count, and the person who must act.

## Shortcuts That Leave the Plan Unreadable

Each of these makes a plan look loaded while people can read neither who does the work nor when:

- **Loading tasks into an iteration that has no capacity rows.** Every task stays unassigned, and the plan stops at 2 of 6.
- **Writing start and end dates so that tasks count as scheduled or ready.** The dates say nothing about capacity or order, and the next calculation clears them. Telling people not to press Schedule is a sign that the dates are not real.
- **Giving every task the same start date so that agents may start at once.** Order then lives only outside WorkChord. Record the order as dependencies, assign rows, and schedule; agents start work whose dependencies are done, and the dates follow.
- **Keeping phases, models, agents, or reviewers in tags.** People cannot group, date, or assign by them, and the Roadmap stays empty.
- **Deleting an iteration and loading it again to change dates.** Task IDs, history, and assignments are lost. Change inputs and schedule.
- **Leaving the project without dates, status, or owner** because the tasks are in. The Roadmap reads the project, not its tasks.
- **Using the admin key or an application route** because the agent contract felt slow for a large plan. Load through the audited planning commands, or hand the import to an operator as described below.

## When an Operator Imports the Plan

The iteration import route takes one plan document and requires the admin key. It is an operator surface: never call it with an agent key, and never ask for the admin key. When an operator will import a document you prepare, the document must already describe a complete plan:

- `team_members` holds one entry per capacity row, and each `name` equals the display name of an existing profile. The import matches rows to profiles by name; an unmatched name creates a new human profile.
- Every leaf task has `assignee_name` equal to one of those names, `effort_hours`, a typed `brief`, `external_key`, `dependency_external_keys`, `tags`, and `milestone_id` of a milestone that already exists in the project.
- No task has `start_date` or `end_date`.

After the import:

1. The new iteration's name starts with "Imported:". Ask the operator to rename it, or rename it yourself with the iteration update command.
2. Re-read the iteration team. Confirm that each row links the intended profile.
3. Preview and apply the schedule yourself, then run [Check the plan before you report it](#check-the-plan-before-you-report-it).

A document with an empty `team_members` list produces a plan at 2 of 6. Return it to its author instead of repairing the result task by task.
