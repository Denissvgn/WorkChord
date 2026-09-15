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

## Deployment and evidence boundaries

Managed team deployments require trusted authentication and project/workspace policy. That authority boundary is a product requirement, not a guarantee supplied by the current guest-session mechanism. An explicitly selected trusted-local deployment can support open collaboration among trusted participants. A guest session provides pseudonymous attribution and stores session metadata; it is not person authentication.

Application snapshots support bounded recovery of application state. They do not replace a database backup or authorize a production recovery operation. Provisioned actors, configured model metadata, successful protocol calls, and real independently accepted delivery are separate observations.

Time entry is an established audience need and a selected product extension, with its own delivery and acceptance work. This does not imply billing support or current availability. Streaming updates and a global scheduling optimizer require measurement before expansion. No productivity or cost benefit is assumed before observation with real project work.
