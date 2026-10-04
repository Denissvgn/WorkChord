# Delivery and review analytics

Analytics uses recorded workflow instants and authorized project or iteration
scope. The window includes acceptance, rejection, cancellation and reopen
events within its UTC bounds. Earlier observations may supply the beginning of
an accepted delivery's duration. Reports load window observations plus bounded
prior episode state for relevant and unfinished tasks, rather than all lifetime
events. Coverage identifies those pre-window seeds separately. Older captures
still establish coverage for current tasks even when their completed episodes
fall outside the window.

| Measure | Definition |
| --- | --- |
| Accepted deliverables | Distinct task identities accepted during the window; repeated acceptance events are counted separately |
| Lead time | First recorded capture to acceptance |
| Cycle time | Most recent active or reopened episode to acceptance, including waiting and rework |
| Review delay | Most recent resolution to acceptance |
| Incomplete samples | A known beginning with no terminal outcome at the observation cutoff |
| Missing samples | An accepted delivery without the required recorded beginning |

Durations use elapsed seconds, rounded to milliseconds; the view converts them
to elapsed days of 24 hours. Each mean and median has its own sample count.
Incomplete samples are excluded from averages. Estimates, working-day effort,
status dates and imported lifecycle states do not create measured durations.
An empty sample has an unknown duration, while a measured zero remains zero.

Scope is retained at observation time. Grouping, moves and task deletion do not
rewrite earlier accepted delivery facts. Structural parents do not count as
delivered work. Cancellation ends the observed open episode; reopening starts
another active episode. Restoration clears the current execution boundary and
does not invent a new original capture time. An outcome outside the selected
scope may leave its earlier scoped history incomplete.

Older records without observations remain explicitly uncovered. Closed work
with unknown acceptance is separate from accepted delivery. The view reports
coverage and provides bounded queues for review and execution ownership that
needs attention; opening a task rechecks its current actions and permissions.

The additive observation migration creates no guessed historical events.
Preserve the observation table with the rest of the database's immutable
history when backing up or restoring. See [identity and recovery](identity-and-recovery.md)
for version controls and recovery boundaries.
