# Working together in WorkChord

This guide starts from an empty workspace and explains how the everyday work
fits together. It describes the current interface: one sidebar for the whole
app, with no work-area tabs.

## Find your way around

The sidebar lists ten destinations, in this order:

| Group | Destination | Use it to |
| --- | --- | --- |
| *(no heading)* | **Overview** | See what needs you now, what is in progress, and the Get started panel. |
| | **My Work** | See your tasks, the reviews waiting for you, your notifications, and your availability. |
| | **Triage** | Decide on incoming requests. A request is not a task until you convert it. |
| **Plan** | **Projects** | Group the work of each project or initiative. Its roadmap is a view of Projects. |
| | **Plan** | Manage iterations and capacity through six checkpoints. |
| | **Gantt** | See the saved schedule and what each task waits for. |
| **Deliver** | **Tasks** | Create, assign, and move tasks. The agent pipeline is a view of Tasks. |
| | **Analytics** | See what is done and accepted, and whether there is enough capacity. |
| **Setup** | **Team** | See the people and agents who do the work. Connect an agent and review the model catalog here. |
| | **Settings** | Change workspace rules and access. The work calendar is a section of Settings. |

Iterations and iteration capacity are managed in **Plan**. The six Plan
checkpoints are **Iteration**, **Capacity**, **Work**, **Blockers**,
**Schedule**, and **Review**. Work through them in order.

Older links keep working. Links to `/plan/master`, `/iterations`,
`/roadmap`, `/agent-pipeline`, `/agent-team/setup`, and `/calendar` open the place where
that content now lives, and they keep their query parameters.

## Get started

Start the workspace as described in the [README](../README.md), sign in, and open
**Overview**. It shows the **Get started** panel until all six steps are done or
you dismiss it in this browser. It lists six steps. Each step opens the page
that does it, and each step is marked done from the workspace's data rather
than from a checkbox:

1. **Say who you are.** Work as a work profile. In a trusted-local workspace,
   choose or add your profile from the account menu ("Add me"). In managed
   sign-in, an operator links your account to a profile. The step is done when
   this session works as a profile.
2. **Create a project.** A project holds the iterations and tasks of one piece
   of work. You create it in the panel. The step is done when a project exists.
3. **Create an iteration.** An iteration is the dated stretch of work you plan.
   The step opens Plan at its **Iteration** checkpoint.
4. **Add capacity.** Say who does the work in this iteration: add yourself,
   connect an agent, or add other profiles. The step opens Plan at **Capacity**.
   To connect an agent, see [agent team setup](agent-team-setup.md).
5. **Add tasks.** The step opens Plan at **Work**. A new workspace has an empty
   backlog, so create the first task there: choose **Open in Tasks**, type a
   title in the **Add a task** row, and press Enter. The task joins the
   iteration. **Import tasks** adds several at once. When a project's backlog
   has tasks, **Add from backlog** adds them to the iteration.
6. **Build the schedule.** The step opens Plan at **Schedule**. Before the
   schedule can be built, **Blockers** must be clear: every task needs an
   assignee and an effort in hours. On **Blockers**, choose **Preview
   assignments**, then **Assign** (its label gives the number of tasks). Enter
   each missing effort in hours and choose **Save**. Then, on **Schedule**,
   choose **Calculate schedule**, check the result, and choose **Apply
   schedule**. The step is done when the schedule is applied.

When all six steps are done, the panel hides from Overview by itself. **Dismiss**
hides it earlier, in this browser only. To see it again, open **Help**, then
**Setup guide**; it then shows "Every step is done. The schedule is applied."

## Start with a person and a project

Sign in and ask a workspace operator to link your account to your human work
profile. A project manager grants access to the projects you need. Profile
ownership and project permissions are separate. See [identity and access](identity-and-recovery.md).

Open **My Work** for owned work across projects, including nested tasks and
backlog work. Its queues are **Doing**, **Up next**, **Blocked**, and
**In review** (work you submitted that waits for a reviewer). **To review** lists
accessible work that another person can review. Open a task to see its currently allowed actions and any blockers.

## Capture and assign tasks

1. On **Tasks**, choose a project and **Backlog** in the scope bar, then select
   **Capture a task**.
2. Give the task a title, a goal, and observable acceptance criteria. Add context
   and verification instructions when someone else needs them to do or review the work.
3. Set the **Assignee**: the person or agent that does the task. This ownership
   survives movement between iterations. An iteration's capacity allocation is a
   separate assignment.
4. Enter **Effort** in hours, or leave it blank when it is unknown. The day
   equivalent appears as a hint. Zero means a known zero. A suggested template
   estimate remains marked as assumed until you deliberately replace it.
5. Add **Labels** to group related work. Use **Waits for** to name the tasks that
   must finish first, and **Earliest start** and **Due by** for date limits.

Triage can also convert a request directly into a project's backlog. An
iteration is optional for capture and urgent manual execution. AI assistance is
available through **Optional AI assistance**; no agent setup is needed for this workflow.

Use the command menu to find a task by title or ID in any project. Results
include its project, iteration or backlog, and state. On **Tasks**, the search
field narrows the list in place. Task links keep the surrounding view available
when the editor closes. The Tasks title names the view shown and opens the list
of saved views. Each filter shows as a chip you can remove. Changed filters stay
in the page link until you save them: **Save changes** updates your view,
**Save as…** creates a new one, and **Reset to saved view** discards the changes.

## Plan iterations and capacity

**Plan** is where you manage iterations and their capacity. Its **Blockers**
checkpoint lists what must be resolved first: missing assignees, missing effort
estimates, and unfinished prerequisites.

In **My Work → My availability**, choose your calendar and record absences.
These absences apply across your allocations. In Plan, select one work calendar
for every year of the iteration. Each date uses that year's weekends, holidays,
shortened days and normal hours. All selected years share one local time zone.
If you select a personal calendar, choose its additional years in your own
availability settings. An uncovered year or conflicting allocation rules hold
the forecast until the responsible owner selects the applicable record.
Recorded execution events retain their actual timestamps.

Routing within the primary calendar year retains the existing iteration-day
calculation and the member's iteration vacation records. For a period spanning
years, the routing calculation divides each working date's available hours by
its own year's normal hours and includes the member's applicable absences.

For each working date:

> Productive capacity = calendar hours after absence × allocation percentage
> × (1 − operational utilization) × productivity coefficient.

For a six-hour day, a 50% allocation, 20% operational utilization, and a 1.25
coefficient, productive capacity is **6 × 0.5 × 0.8 × 1.25 = 3 hours**.
Shortened days reduce the calendar hours first. Overlapping absence ranges are
counted once. Two full-time allocations exceed one person's available time,
even if each project looks reasonable on its own.

The capacity view separates available hours, allocations, productive hours,
and saved commitment effort. It rounds displayed hours to four decimals and
keeps unknown estimates visible. Saved effort is distributed over calendar
working hours for comparison; it is not a time-entry record. Private projects
contribute aggregate busy time without exposing their tasks or absence details.

Add **Delivery prerequisites** when another task or milestone must be accepted
first, including work in another project or iteration. These links are separate
from local schedule dependencies. Cycles are rejected. A milestone prerequisite
requires a completed milestone with accepted leaf work. A withdrawn acceptance
or inaccessible prerequisite makes the dependent work unavailable again.
Unlink a delivery prerequisite before deleting referenced work or changing its
project scope.

A task prerequisite can also name a **target branch** (`target_branch` on
`POST /api/tasks/{task_id}/delivery-dependencies`) when the dependent work needs
the prerequisite's code on that branch, not only its acceptance. It stays held
until the prerequisite is Accepted and a linked pull request is observed merged
into that branch. Readiness reads the stored GitHub observations and never calls
GitHub; run the prerequisite's GitHub catch-up to refresh them (a person uses **Run catch-up** on the task page; the PM agent uses `agent_run_github_catch_up`). The hold is
listed as `delivery_holds` on the agent pipeline and the task context, each with
its reason, the observed pull requests and the next owner: the reviewer for an
open pull request awaiting acceptance, the worker for unfinished work, and the
PM for a merge that is not yet observed or confirmed, a merge on another branch, a closed prerequisite whose acceptance no longer matches its version (reopen it; the reviewer must accept it again) or a canceled one (record a replacement). A merge never accepts a task, and an observed merge keeps the prerequisite's acceptance unless its head moved after acceptance or is missing, which makes the acceptance stale. An
ordinary dependency (`depends_on`) is unchanged and releases the dependent task
once its predecessor is Implemented.

To change the branch of an existing prerequisite, send
`PATCH /api/tasks/{task_id}/delivery-dependencies/{edge_id}` with
`{expected_version, target_branch}`; `target_branch: null` keeps only the
Accepted gate. It needs the same edit access as adding the prerequisite, records
`delivery_prerequisite_retargeted` on the task timeline, changes the task's
version and re-evaluates readiness at once, so the dependent work is released or
held by the new branch.

The PM agent, or any agent with the same project access, uses the MCP tools
`agent_list_delivery_dependencies`, `agent_add_delivery_dependency` and
`agent_retarget_delivery_dependency` for these commands, and
`agent_get_github_reconciliation` and `agent_run_github_catch_up` for a task's
GitHub reconciliation (`GET /api/tasks/{task_id}/github-reconciliation`) and
catch-up (`POST /api/tasks/{task_id}/github-reconciliation/catch-up`). The add
and retarget tools are audited planning commands that take an idempotency key, a
rationale and a correlation ID; their receipt carries the prerequisite list.

Use the task's work controls to commit it to an iteration or return planned
work to the backlog. Preview the schedule before applying it. A preview saves
nothing. Shared availability changes invalidate its planning revision; reload
and calculate again after a conflict. Overallocated capacity prevents a new
schedule commitment. Allocations must have durable profiles, and forecast dates
must fit within their allocated iteration before commitment. Existing commitments remain visible for reconciliation;
the scheduler does not silently redistribute another project's allocations.

## Read the delivery signals

A task committed to start Monday but actually started Wednesday is **late to
start**, even if it still finishes within its iteration. Unimplemented work
with an end date before today is **overdue**. A forecast ending next Monday
when its iteration ends Friday is **iteration overflow**, even before either
date has passed. A resolved task counts as implemented; it counts as accepted
only after a current, attributed review. These signals answer different questions.

## Work, discuss, and review

Open **Work and review** on a task, select an available action, and supply the
requested reason. Humans can start urgent backlog work manually. Record
criterion progress and evidence, then resolve the task for review. Another
authorized reviewer accepts it or requests rework. A resolved task is awaiting
review; **closed** means accepted work and uses the violet status color.
When a project requires a different review publisher, a person's review does not
accept work: **Accept** stays unavailable and says it needs an assigned agent
verifier. A signed-in workspace owner or operator can still close one resolved task
with **Accept as owner** under **Work and review**. Give a reason, which is
required, and choose the action; it also works from the keyboard, and the result is
announced. The project's policy stays on and covers only that task. **Review
history** shows the acceptance with an **Owner override** label and your reason, so
it is never read as an independent review, and the task's Activity records it too.
If you executed the work yourself, the action is not offered to you: ask another
owner or operator to accept it, or use the API with `X-Review-Override: true`. If you
only wrote the task's current evidence, the server refuses the acceptance and the
page shows its message; the web interface does not send that override.

**Accept as owner** needs a person who is signed in. A trusted-local workspace
browser with no signed-in person is not an owner or operator, even though it can
otherwise edit: the page says so instead of offering the action. Sign in as a
workspace owner or operator, reload the task, and accept it. A person who may review
but is not an owner or operator is told to ask one of them, or to assign an agent
verifier. The page can only explain this where the server reports that the project
needs a verified agent publisher. A person without review permission, and a paired
read-only observer, instead see the ordinary reason Accept is unavailable; a paired
observer is also told to sign in as a person with review permission.

Work that was resolved outside recorded runs has no executor on record, so no
verifier can be selected for it. The PM agent records who executed it with
`agent_record_manual_provenance` once the pull request is linked to the task and
every commit of it is listed; a human executor can only be recorded by a
signed-in person, so the PM asks the owner. When a refusal names a next step, the
PM agent or the page follows it instead of asking anyone to switch the review
policy off.

**Postpone** stops planned, active or resolved work without canceling it. Give a
reason and one or more requirements (a task is accepted or resolved, a triage item
is resolved, a date arrives, or the owner decides); the form lists what the
postponement releases before you confirm. A PM agent does the same with
`agent_postpone_task`, `agent_reactivate_task` and `agent_get_task_postponement`.
Postponed work is not scheduled, holds no capacity, is not offered to agents or
verifiers, and returns to Planned (or Resolved) by itself when every requirement is
met, or when someone chooses **Reactivate**. Only the workspace owner records an
owner-decision requirement. Cancel work only when it will never be done. When
another task already delivered the work and is closed or accepted, use
**Supersede** instead of reopening anything: the original is withdrawn with its
history, and its dependents and release membership move to the successor.
Canceled and superseded work is shown as ended in Tasks, Board and Analytics.

Explicit blocks and cancellation are separate from lifecycle status. A block
comes from **Report blocker**, used by a person or an agent; either way the task
shows the reason, appears in the **Blocked** view, and its Activity names who
reported it. Unblocking or reopening requires the corresponding action; reopening
invalidates current acceptance.

Use **Discussion** for questions and coordination. Choose mention recipients
from the authorized people search. Comments retain authorship, edit history,
and removal markers. Comments do not change execution evidence or task versions.
Follow a task and choose which discussion, mention, review, and block events
reach your **Notifications** in **My Work**. Notifications show read/unread
state and delivery status. Operators must run the dedicated [delivery worker](database-runtime-policy.md)
for queued notifications to arrive. Failed deliveries can be retried. Unsubscribing or losing access is
checked again before delivery; reading a notification never changes task status.

If a save conflicts, keep your draft, reload the current record, and compare
before reapplying. Task and comment drafts stay in the same browser tab and
account for up to 24 hours. Signing out clears them. See [task semantics](task-domain.md)
for estimates, lifecycle, acceptance, and metric definitions, and
[recovery](identity-and-recovery.md#application-snapshots) for operator recovery.

## Connect agents

Agents that do or check work are members of the team. Open **Team → Connect**,
or choose **Connect an agent** from the command menu, to connect one. The
[agent team setup](agent-team-setup.md) guide describes the five questions, the
runtime steps, and the advanced manifest path.
Each handoff names a runtime instance (`runtime_instance_id`). The agent returns it
unchanged in its acknowledgement, and team status shows whether the identity is
current, stale, changed or unknown for each member. After a credential is
recovered or a member is replaced, give the runtime the new handoff and have it
acknowledge again; do not copy a handoff to another runtime.

Before an operator imports an iteration plan file, the PM agent can run a dry run
(`agent_preview_iteration_import`) that shows every created, changed and removed
row and returns a `review_digest`. The operator imports the unchanged file with
that digest, and the import applies exactly the reviewed changes or is refused.
