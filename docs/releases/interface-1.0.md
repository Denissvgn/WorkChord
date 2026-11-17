# Interface simplification 1.0

The workspace now has one sidebar for the whole app. The three work areas and
their top-bar tabs are gone, and the pages you use every day sit in ten
destinations in a fixed order. Old addresses keep working: each one redirects to
its new place and keeps any query parameters it was opened with.

## Where things moved

Each old place is shown with its new place. "Sidebar" means the destination is a
top-level item in the new sidebar.

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

The sidebar lists the destinations in this order: **Overview, My Work, Triage**;
then group **Plan**: Projects, Plan, Gantt; then group **Deliver**: Tasks,
Analytics; then group **Setup**: Team, Settings.

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

## First run: the Get started steps

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
6. **Build the schedule.** Build the schedule from the tasks and capacity, then
   apply it. Opens Plan at its Schedule step. The workspace is set up once the
   schedule is applied.

Dismiss hides the panel in this browser. To bring it back, open **Help**, then
**Setup guide**.

### The sample project

Get started also offers **Load a sample project**. It creates a complete
example to explore: two milestones, two capacity rows (you and a sample agent),
eight linked tasks, and an iteration with a schedule. Open Plan after loading it
to look around.

To remove it, choose **Remove sample data** in the panel. The panel lists every
record the sample created and deletes them, including the sample iteration and
schedule. Your own profile is kept. If a removal stops partway, the records that
remain are listed so you can retry.

## What an operator must do after upgrading

Reinstall the three role skill packages at the new versions. Install each one
from the server skill catalog and check its SHA-256 digest against the catalog
entry.

| Role package | Reinstall this version | Previous version |
| --- | --- | --- |
| `workchord-pm` | 1.15.2 | 1.15.0 |
| `workchord-worker` | 1.15.1 | 1.15.0 |
| `workchord-reviewer` | 1.3.2 | 1.3.0 |

The catalog that lists these packages is version 1.17.1. A runtime that uses the
tracked Codex role adapter instead (`adapters/codex/workchord-agent-roles`)
should take the adapter from this release, plugin version 1.17.1, which carries
the same three role skills. The setup steps for each runtime are in
[agent team setup](../agent-team-setup.md).

Nothing else needs to be done. This release has no database migration and no
server setting or environment variable to change. The example team file in
`config/examples` now pins the three versions above; it is an example, not a
setting your workspace reads.
