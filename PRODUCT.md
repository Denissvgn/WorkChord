# WorkChord

WorkChord helps human-led teams plan and deliver project work, with optional external agents. Its intended audience is a small team that needs to understand ownership, dependencies, available capacity, and the evidence that work meets its brief.

## Available capabilities

The application groups tasks into projects and iterations, schedules work against calendars and iteration capacity, and presents List, Board, Gantt, and roadmap views. It provides intake and triage, task history, agent assignment and claim protocols, and separate verification records. External agents connect through REST or MCP; configuring an actor or a model binding does not start an execution runtime.

The Android companion is a source application with a smaller feature set. Its capabilities must be assessed separately from the web application.

## Product direction

The intended everyday workflow is capture → assign → do → review. A project backlog should support work before a scheduling commitment. Human manual work should be explicit, while agent dispatch should continue to require an assigned actor, a sufficient brief, and valid execution context. These are product requirements; availability depends on the corresponding server and client support.

- A **principal** authenticates a person or agent. A **profile** is the durable owner identity. An iteration **capacity allocation** describes availability. An execution **actor** performs assigned work. These concepts have explicit links and are not interchangeable.
- A task retains the lifecycle values `planned`, `active`, `resolved`, and `closed`. Blockage and cancellation need explicit commands or facets. Reopening requires an authorized, recorded command.
- **Implemented** means execution reports the work done. **Accepted** means an authorized independent reviewer has accepted evidence against the current brief. Progress and checkboxes alone do not establish acceptance.
- Estimates use effort hours and a declared hours-per-working-day conversion. An unknown estimate remains unknown. Calendar dates and UTC event instants have different meanings.
- A person's available capacity is shared across projects. Project access must govern reads, writes, counts, derived views, and agent operations consistently.

## Structure of the interface

These statements describe how the web application is organised. [DESIGN.md](DESIGN.md#structure-of-the-interface) holds the matching navigation, scope, page frame and colour rules.

### Destinations

The web application has ten destinations, in this order: three without a group, then the groups Plan, Deliver and Setup.

- **Overview** shows the state of the work in scope and the next step to take.
- **My Work** gathers what the signed-in person has to act on: their assigned tasks, the work they review, and Notifications.
- **Triage** is where incoming requests are reviewed and each request receives one disposition.
- Group **Plan**:
  - **Projects** lists the projects with their owners and status, and its Roadmap view shows them over time.
  - **Plan** takes the iteration in scope through the six planning checkpoints, from setting up the iteration to reviewing it.
  - **Gantt** shows the schedule of the work in scope over time, with dependencies and date limits.
- Group **Deliver**:
  - **Tasks** lists, filters and edits the tasks in scope as a list, a board or the agent pipeline.
  - **Analytics** reports delivery for the work in scope: status, flow, whether work is on track, and execution usage.
- Group **Setup**:
  - **Team** manages the people, agents and models that do the work, including agent connection and the model catalog.
  - **Settings** holds personal preferences and workspace configuration in four groups.

### Names in the interface

- **Iteration** is the name for a bounded period of work; the interface never calls it a planning period, sprint or cycle.
- **Plan** is the page, and a **checkpoint** is one of its six units: Iteration, Capacity, Work, Blockers, Schedule and Review.
- **Assignee** is the person or agent that does a task, **Reviewer** is the person or agent that checks it, and **Owner** is used for projects and initiatives.
- **Labels** is the interface name for task labels; the interface never calls them tags.
- **Waits for** names a task's dependencies.
- **Earliest start** and **Due by** name a task's date limits.
- **Effort** is entered in hours, and its conversion to working days is shown as a hint.
- **Triage** is the page, and a **request** is one of its items.
- **Notifications** is the My Work queue for events that concern the signed-in person; the interface does not call it Inbox.
- **Gantt** is the name of the schedule page everywhere in the interface.

### One assignee

- A task shows one Assignee, which is the capacity row of a person or of an agent, with an icon that shows which kind it is.
- When the Assignee is an agent, one status line under its name gives the dispatch state, the same for every reader:
  - **No agent connected**: no enabled agent is connected to the agent's profile and nothing has been sent.
  - **Not sent to the agent yet**: an agent is connected but the task has not been sent to it. The task view offers Send to the agent instead of Start work.
  - **Queued**: the task has been sent and the agent has not begun.
  - **Working**: the agent has begun.
  - **Waiting for review**: the work has been submitted.
  - **Agent status unknown**: shown only for an assignee known to be an agent while a read the line needs (whether the agent is connected, or whether the task has been sent) is loading or has failed. Until the team read says the assignee is an agent, the assignee shows no status line.
- A closed task shows no status line.
- Reviewer is shown beside Assignee.
- Owner is not shown on a task unless it is known to differ from the assignee's profile; while that profile cannot be read, Owner stays hidden. It stays editable under More.

### Plan

- Plan is one page at `/plan` for the iteration in scope.
- Plan lists the six checkpoints as sections in this order: Iteration, Capacity, Work, Blockers, Schedule, Review; the first incomplete checkpoint is open.
- Each section states its result in one line and lets its common action be done in place.
- A section links to a full page only where one exists, which is Tasks or Gantt.
- Planning progress is shown as "n of 6" on the Plan page and as a counter on the Plan navigation item, and nowhere else.
- Checkpoint states come from the server's planning-readiness response and are never computed in the browser.

### Settings

Settings has four groups.

- **My preferences:** theme and keyboard shortcuts, saved in this browser.
- **Workspace:** language for the interface and for AI output, work calendar, scheduling, templates and labels, and notifications.
- **Connections:** GitHub, webhooks, web intake and the AI provider.
- **Access and system:** access keys, runtime and about.

Every section header says where its setting is saved: in this browser or for the whole workspace. One Unlock editing control serves all protected sections. People, agents and models are managed in Team, not in Settings.

### First run

- Overview shows a Get started panel with six steps: Say who you are, Create a project, Create an iteration, Add capacity, Add tasks, Build the schedule.
- Each step opens the real page where that step is done.
- A step is marked done from the workspace data, never from a stored flag.
- Every empty page shows one sentence and one button for the single next step.

## Deployment and evidence boundaries

Managed team deployments require trusted authentication and project/workspace policy. That authority boundary is a product requirement, not a guarantee supplied by the current guest-session mechanism. An explicitly selected trusted-local deployment can support open collaboration among trusted participants. A guest session provides pseudonymous attribution and stores session metadata; it is not person authentication.

Application snapshots support bounded recovery of application state. They do not replace a database backup or authorize a production recovery operation. Provisioned actors, configured model metadata, successful protocol calls, and real independently accepted delivery are separate observations.

Time entry is an established audience need and a selected product extension, with its own delivery and acceptance work. This does not imply billing support or current availability. Streaming updates and a global scheduling optimizer require measurement before expansion. No productivity or cost benefit is assumed before observation with real project work.
