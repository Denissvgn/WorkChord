# Team, Capacity, and Calendar

Use this reference to create a feasible execution timebox and staff it with reusable profiles plus iteration-scoped capacity.

## Contents

- [Create the outcome and timebox](#create-the-outcome-and-timebox)
- [Configure calendars and iterations](#configure-calendars-and-iterations)
- [Configure reusable profiles](#configure-reusable-profiles)
- [Create iteration capacity rows](#create-iteration-capacity-rows)
- [Read the live routing inventory](#read-the-live-routing-inventory)
- [Review capacity and workload](#review-capacity-and-workload)
- [Complete phase contracts](#complete-phase-contracts)

## Create the Outcome and Timebox

1. Select an initiative only when several projects contribute to one strategic goal.
2. Create or select one accountable project for the outcome.
3. Set a project owner or reusable owner profile, status, health, start date, target date, and initiative link deliberately.
4. Create milestones for intermediate outcomes through
   `agent_create_project_milestone` or the matching agent-planning REST route;
   use a release record only for a shipping or rollout boundary.
5. Create a real iteration for executable work. Link it to the project when the timebox is project-scoped.
6. Keep cross-project work in an unscoped iteration only when the operating model intentionally shares capacity.
7. Re-read project, milestone, release, and iteration IDs before attaching tasks.

Do not use a task as a substitute for a project update, milestone, release, or iteration. Do not place unclear requests directly into an iteration.

## Configure Calendars and Iterations

### Calendar sequence

1. Read existing calendars before creating one.
2. Select the correct year, weekend-day indexes (`0` for Monday through `6` for Sunday), holidays, and shortened days.
3. Import public or CSV holidays only through the supported import surface; inspect imported, skipped, and error counts.
4. Query working days across the proposed iteration dates.
5. Create the iteration with `name`, `calendar_id`, optional `project_id`, `start_date`, `end_date`, and optional `manager_email`.
6. Use an iteration series only for genuinely repeated, back-to-back timeboxes. Check every generated date and project link.
7. Re-read the iteration and its computed `working_days`.

Stop when the calendar year does not cover the iteration, the dates overlap an unintended timebox, or the project boundary is unclear.

## Configure Reusable Profiles

Create one reusable `TeamMemberProfile` per stable person or agent capability identity. Set:

- `display_name`, optional contact and headline;
- a concise summary of responsibilities and operating limits;
- notes that remain safe for routing context;
- `automation_enabled` according to the deployment's current recommendation policy.

Add profile skills with:

- a stable `skill_key` and human `skill_name`;
- a category;
- level and interest from `1` to `5`;
- `is_weakness=true` for material routing constraints;
- normalized keywords and explanatory notes.

Treat these values as recommendation evidence only. Never grant scopes, create an actor, assign an execution lease, or expose a secret because a profile matches a capability.

Prefer a few specific skills over a keyword dump. Record weaknesses that should lower routing confidence, such as missing domain knowledge, unsafe production access, or weak review independence.

## Create Iteration Capacity Rows

Add each participating profile to the iteration as a `TeamMember`. Treat this row as capacity ownership for that timebox.

Set and review:

| Field | Meaning | Review rule |
| --- | --- | --- |
| `profile_id` | Reusable capability identity | Link the intended profile; avoid duplicate capacity rows unless explicitly partitioning capacity. |
| `name`, `position`, `email` | Iteration display identity | Keep aligned with the profile where practical. |
| `availability_percent` | Portion of the timebox available to project work | Reduce for part-time or shared allocation. |
| `professionalism_coefficient` | Delivery-efficiency adjustment, constrained to `0.5..5.0` | Use documented team policy; do not inflate it to force a schedule. |
| `operational_utilization` | Portion reserved for operations and non-plan work | Set expected interrupt load before scheduling. |
| vacations | Date ranges unavailable during the iteration | Add all known absences before final scheduling. |

Use bulk team or vacation import only after previewing the source text or CSV and identifying the target iteration. Inspect skipped rows and errors; do not treat a partial import as complete.

Ensure every task `assignee_id` points to a team-member row from the same iteration. Do not assign a reusable profile ID or an actor ID to this field.

## Read the Live Routing Inventory

When the server advertises `model-aware-routing-v1`, read its provider-neutral
model catalog and enriched exact actor roster before assessment or dispatch.
For each candidate, keep these layers separate:

| Layer | Evidence to read | What it cannot prove |
| --- | --- | --- |
| Reusable profile | Kind, automation flag, assignment modes, precise skills, levels, weaknesses | Actor identity, permission, live runtime, or capacity |
| Iteration capacity owner | Workload, availability, vacations, schedule | Authenticated dispatch identity or model capability |
| Exact actor | Enabled state, role, scopes, profile binding, queue revision, last seen, current work | Model adequacy by itself |
| Active model binding | Stable catalog key, binding/catalog revisions, reasoning/context tiers, modality/tool/data-policy tags, cost/latency tiers, verification freshness | Credentials, provider access, or cryptographic runtime attestation |

Use only active bindings and live catalog metadata. Treat the configured alias
as intended runtime and the worker's later observed model as self-reported
evidence. Do not derive a tier from a provider-facing model name, profile prose,
or price. A capability match never bypasses actor scopes, purpose compatibility,
queue policy, schedule, workload, or vacation gates.

A normal PM may read this secret-free inventory but must not create, edit,
enable, disable, or rebind model metadata. Ask an operator to correct missing or
stale catalog/binding data. If the feature, catalog, roster, or required
metadata is absent, stop automated model-aware selection and record a supervised
compatibility-routing handoff; never fill the gap from memory or inference.

## Review Capacity and Workload

For every prospective capacity owner:

1. Read member vacations.
2. Read member capacity and inspect `working_days`, `vacation_days`, `available_days`, `effective_days`, `adjusted_days`, and `hours`.
3. Read workload and inspect `capacity_days`, `allocated_days`, `free_days`, `workload_percent`, and `workload_status`.
4. Investigate yellow or red workload before assigning more work.
5. Compare task effort, constraints, dependencies, and iteration dates with the free capacity.
6. Re-run scheduling and re-read workload after assignment or effort changes.

Until the live capabilities contract states that aggregate iteration capacity and member vacation calculations are reconciled, use per-member capacity and workload detail for assignment decisions. Record any difference from the iteration summary rather than choosing the more convenient number.

Do not hide overload by lowering effort, increasing professionalism, or removing vacations. Adjust scope, dates, allocation, assignee, or deferral explicitly.

## Complete Phase Contracts

### Phase 2: Define the outcome hierarchy

**Preconditions**

- Confirm authority and the intended outcome.
- Resolve whether the work belongs to an existing project or new project.

**Required reads**

- Read initiatives, projects, summaries, milestones, releases, calendars, and iterations.
- Read current project updates and target-date risk before changing health or dates.

**Allowed mutations**

- Create or update initiative, project, milestone, release, calendar, and iteration records within granted authority.
- Preserve accepted source and ownership links.

**Exit and postcondition checks**

- Re-read the full hierarchy and confirm one accountable project plus one real execution iteration, or record an explicit Triage disposition.
- Confirm dates and ownership do not conflict.

**Evidence and stop rules**

- Record chosen IDs, date rationale, owner, health rationale, and source.
- Stop on ambiguous ownership, unsupported project mutations, invalid dates, or a required operator approval.

### Phase 3: Set up the team and dispatch roster

**Preconditions**

- Confirm the iteration and calendar.
- Obtain approved staffing and expected operational load.

**Required reads**

- Read profiles and skills, iteration team, vacations, capacity, workload, and—when supported—the enabled actor roster with profile bindings, active model bindings, catalog revisions, and last-seen evidence.

**Allowed mutations**

- Create or update profiles and profile skills.
- Add or update iteration team rows and vacations.
- Request actor provisioning or profile binding from an operator; do not perform secret administration.

**Exit and postcondition checks**

- Re-read each capacity row, vacation list, capacity, and workload.
- Confirm every intended automated target is already provisioned, enabled,
  purpose-compatible, separately authorized, and backed by current live metadata
  before later dispatch. Do not call this task-specific eligibility until a
  current assessment and routing preview apply the remaining hard gates.

**Evidence and stop rules**

- Record capacity assumptions, overload decisions, profile-skill rationale,
  actor/binding revisions, metadata freshness, availability evidence, and
  unresolved staffing risks.
- Stop when capacity is negative without an accepted mitigation, vacations are
  incomplete, required live routing metadata is unavailable, or a
  profile/model match is being mistaken for permission or dispatch eligibility.
