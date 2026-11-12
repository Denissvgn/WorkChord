# Review Packet And Verdict

Use this reference to check one submitted task, record Accept or Request
changes, and hand rework to an explicit owner.

## Contents

- [Confirm the review is yours](#confirm-the-review-is-yours)
- [Build the review packet](#build-the-review-packet)
- [Check model evidence](#check-model-evidence)
- [Accept](#accept)
- [Request changes](#request-changes)
- [Stop rules](#stop-rules)

## Confirm The Review Is Yours

1. Read the review queue and take its first item. The item carries the review
   assignment, the task, and its queue position.
2. Confirm the assignment purpose is `verification`, its actor is you, and its
   `not_before` time has passed.
3. Confirm the task is Implemented (`resolved`) and the assignment's task
   version equals the task version. A stale assignment is the PM's to refresh.
4. Confirm you did not do this work: you are not the actor that ran it or
   reported its progress. The server rejects a non-independent review with
   `independent_review_required`; never work around it.
5. Confirm your profile is not the profile of the task's assignee. The PM plans
   review with a reviewer profile other than the one that carries the work, and
   enforced model-aware routing refuses the same profile with
   `verification_profile_not_independent`. Where the server does not check it,
   stop and report to the PM all the same.

## Build The Review Packet

Read the complete context with the review assignment ID, then record:

1. The typed brief (`task.brief`) when present: goal, scope, exclusions,
   ordered acceptance criteria by stable `id` and `revision`, verification
   instructions, and artifact expectations. The legacy Markdown brief is not
   authoritative when the typed brief exists.
2. The current `brief_revision` and `artifact_revision`. Evidence from an older
   revision cannot support Accept.
3. The worker's criterion progress: every current criterion needs state
   `completed` and non-empty evidence for the current revisions.
4. The timeline: the submission summary, artifact, commit, and pull request
   links, and the latest run's terminal result. No run may still be active.
5. Dependencies: every delivery prerequisite must already be Accepted.
6. For each criterion, check the evidence yourself. Re-run or inspect the
   stated verification when authorized and safe. Record the check, environment,
   result, and limitations.
7. Scope: look for silent expansion, missing deliverables, skipped tests, and
   unresolved risks or warnings.
8. Plan fit: read the task's assignee, dates, and milestone, and any
   `plan_gaps` the worker reported. Note a task that was done without an
   assignee, without calculated dates, or outside its milestone. These are
   notes for the PM under `limitations`; they are not criteria and never decide
   the verdict.

Do not treat a succeeded run, a green local check, a commit link, or the
worker's summary as enough by itself. Check the task's stated outcome.

Shape `evidence` as one entry per criterion, for example
`{"criteria": [{"id": "...", "revision": 1, "result": "pass", "note": "..."}],
"limitations": "..."}`, within 100 bounded fields. `result` is `pass`, `fail`,
or `not_checked`, and `note` says what you checked or what must change. People
who review in WorkChord record the same `criteria` packet, so a worker reads one
rework format.

## Check Model Evidence

When the review or execution assignment is model-aware, read the selected
binding and the run's observed model and trust state:

| Trust state | Reviewer response |
| --- | --- |
| `matched` | Continue; describe it as self-reported, not attested |
| `mismatch` | Stop; report to the PM without a verdict |
| `unreported` | Stop; report to the PM without a verdict |
| `unverifiable` | Continue only under the PM's supervised handling; never call the model verified |

A queued model-aware review cannot be recorded while enforcement is inactive;
report that to the PM.

## Accept

Accept (`verdict: "pass"`) only when every current criterion passes with
evidence you checked and no unaccepted risk remains. Accept atomically makes
the task Accepted (`closed`) and fulfills your review assignment. Re-read the
task from the response and report the result.

## Request Changes

Request changes (`verdict: "reject"`) when any criterion fails, evidence is
missing or untrustworthy, or the work exceeded its scope. Never accept part of
a task.

Write the `reason` and `evidence` with:

- each failed criterion by `id`, the expected and the observed result;
- the check you ran and a short output summary;
- links to evidence and artifacts;
- severity and impact;
- whether the original scope is still valid;
- the minimum change required.

Set `rework_actor_id` to the worker the PM named in the review assignment, or
else to the worker whose submission you reviewed. Stop and ask the PM when that
worker is unknown, disabled, or not on the team. Request changes atomically
returns the task to `active`, fulfills your review assignment, and queues one
`rework` assignment for that worker.

Rework returns to the same task and the same assignee, so the Gantt chart keeps
showing who carries it. Never change the assignee, the dates, or the milestone
to fit the rework; say in your `reason` when you think another capacity row
should take it, and let the PM decide.

Report out-of-scope findings and plan gaps to the PM in your final message so
they can be captured in Triage or fixed in the plan; do not fold them into the
failed criteria.

## Stop Rules

Stop without a verdict and report to the PM when:

- the task is not Implemented, a run is active, or the assignment is stale;
- you cannot establish independence from the work, as an actor or as a profile;
- model trust is `mismatch` or `unreported`;
- evidence conflicts and you cannot resolve it by checking;
- the rework owner is unknown or ineligible;
- the server returns `401`, `403`, `independent_review_required`,
  `verification_actor_not_independent`, or
  `verification_profile_not_independent`.
