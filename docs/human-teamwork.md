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

Older links keep working. Links to `/iterations`, `/roadmap`,
`/agent-pipeline`, `/agent-team/setup`, and `/calendar` open the place where
that content now lives, and they keep their query parameters.

## Get started

Start the workspace as described in the [README](../README.md), sign in, and open
**Overview**. It shows the **Get started** panel until you dismiss it in this browser.
It lists six steps. Each step opens the page that does it, and each step is
marked done from the workspace's data rather than from a checkbox:

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
5. **Add tasks.** Add the work for the iteration from the backlog or by import.
   The step opens Plan at **Work**.
6. **Build the schedule.** Build it from the tasks and capacity, then apply it.
   The step opens Plan at **Schedule** and is done when the schedule is applied.

When all six steps are done, the panel says so. **Dismiss** hides the panel in
this browser only. Reopen it from **Help → Setup guide**.

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
These absences apply across your allocations. Conflicting imported calendars
need an explicit choice. Review the calendar year and time zone; dates outside
its supported year remain uncertain and cannot be silently committed. Capacity
uses local calendar dates rather than shift start/end times; recorded execution
events retain their actual timestamps.

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
