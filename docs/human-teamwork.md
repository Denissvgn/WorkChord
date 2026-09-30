# Working together in WorkChord

## Start with a person and a project

Sign in and ask a workspace operator to link your account to your human work
profile. A project manager grants access to the projects you need. Profile
ownership and project permissions are separate. See [identity and access](identity-and-recovery.md).

Open **My Work** for owned work across projects, including nested tasks and
backlog work. Its queues distinguish active, queued, blocked, and
awaiting-review work. **Review work** lists accessible work that another person
can review. Open a task to see its currently allowed actions and any blockers.

## Capture, assign, and estimate

1. Open **Tasks → Project backlog**, choose a project, and select **Capture a task**.
2. Give the task a title, a goal, and observable acceptance criteria. Add context
   and verification instructions when someone else needs them to do or review the work.
3. Select the responsible person. This ownership survives movement between
   iterations; an iteration's capacity allocation is a separate assignment.
4. Leave effort blank when it is unknown. Enter hours or days when you have an
   estimate. Zero means a known zero; a suggested template estimate remains
   marked as assumed until you deliberately replace it.

Triage can also convert a request directly into a project's backlog. An
iteration is optional for capture and urgent manual execution. AI assistance is
available through **Optional AI assistance**; no agent setup is needed for this workflow.

Use **Search tasks** or the command menu to find a task by title or ID. Results
include its project, iteration or backlog, and state. Task links keep the
surrounding view available when the editor closes. Modified saved-view filters
are local drafts: **Save changes** updates your view, **Save as…** creates a new
one, and **Reset to saved view** discards the modifications. Save before sharing
a view link; reloading restores its saved filters.

## Plan capacity and delivery prerequisites

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

## Execute, discuss, and review

Open **Work and review**, select an available action, and supply the requested
reason. Humans can start urgent backlog work manually. Record criterion progress
and evidence, then resolve the task for review. Another authorized reviewer
accepts it or requests rework. A resolved task is awaiting review; **closed**
means accepted work and uses the violet status color. Explicit blocks and
cancellation are separate from lifecycle status. Unblocking or reopening requires
the corresponding action; reopening invalidates current acceptance.

Use **Discussion** for questions and coordination. Choose mention recipients
from the authorized people search. Comments retain authorship, edit history,
and removal markers. Comments do not change execution evidence or task versions.
Follow a task and choose which discussion, mention, review, and block events
reach your inbox. **My Work → Inbox** supports read/unread state and delivery
status. Operators must run the dedicated [delivery worker](database-runtime-policy.md)
for queued notifications to arrive. Failed deliveries can be retried. Unsubscribing or losing access is
checked again before delivery; notification read state never changes task status.

If a save conflicts, keep your draft, reload the current record, and compare
before reapplying. Task and comment drafts stay in the same browser tab and
account for up to 24 hours. Signing out clears them. See [task semantics](task-domain.md)
for estimates, lifecycle, acceptance, and metric definitions, and
[recovery](identity-and-recovery.md#application-snapshots) for operator recovery.

For optional agent execution, start with [agent team setup](agent-team-setup.md).
