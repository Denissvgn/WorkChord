# Review Packet And Verdict

Use this reference to check one submitted task, record Accept or Request
changes, and hand rework to an explicit owner.

## Contents

- [Confirm the review is yours](#confirm-the-review-is-yours)
- [Build the review packet](#build-the-review-packet)
- [Check the delivery trace](#check-the-delivery-trace)
- [Check model evidence](#check-model-evidence)
- [Accept](#accept)
- [Request changes](#request-changes)
- [Stay present and follow a refusal's next step](#stay-present-and-follow-a-refusals-next-step)
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

If the assigned `review_selection` contains `review_evidence`, obtain the operator-prepared packet through the approved channel. Check the commit URL, the selected model binding, the expiry and the packet's SHA-256. For `source_only`, verify that the current task assessment explicitly permits review from source alone. For `source_and_tests`, check the named test results against their recorded digests. Use exactly those observations and the submitted source to evaluate each criterion. Send the digest of the packet you actually reviewed in `reviewed_packet_sha256` with the normal `observed_model` and `reviewed_candidate_digest`. Stop and return to the PM if the material is unavailable, stale or differs.

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
8. Delivery trace: check the task's GitHub links against the diff you
   reviewed, as in [Check The Delivery Trace](#check-the-delivery-trace).
9. Plan fit: read the task's assignee, dates, and milestone, and any
   `plan_gaps` the worker reported. Note a task that was done without an
   assignee, without calculated dates, or outside its milestone. These are
   notes for the PM under `limitations`; they are not criteria and never decide
   the verdict.

Do not treat a succeeded run, a green local check, a commit link, or the
worker's summary as enough by itself. Check the task's stated outcome.

Shape `evidence` as one entry per criterion plus the trace check, for example
`{"criteria": [{"id": "...", "revision": 1, "result": "pass", "note": "..."}],
"delivery_trace": {"result": "pass", "note": "..."}, "limitations": "..."}`,
within 100 bounded fields. `result` is `pass`, `fail`,
or `not_checked`, and `note` says what you checked or what must change. People
who review in WorkChord record the same `criteria` packet, so a worker reads one
rework format.

## Check The Delivery Trace

A task that changed a repository must lead to its code, and its code back to
the task. Read `task.external_links` in the complete context and the worker's
`delivery_trace` in the submission evidence, then confirm:

1. **The links exist.** GitHub links with `metadata_json.github_type`
   `branch`, `commit` (one per commit), and `pull_request` when the worker
   opened one. A server without `work-delivery-links-v1`, or a repository
   outside GitHub, carries the same URLs in the run's artifact links instead.
2. **They match the diff you reviewed.** The commits you inspected are exactly
   the linked commits (compare full SHAs), they are on the linked branch, and
   the linked pull request's head is that branch. A commit you reviewed that is
   not linked, or a linked commit you did not review, is a mismatch.
3. **The key goes both ways.** The branch name holds `wc-<task-id>`, and the
   commit messages and the pull request name `WC-<task-id>`, unless the worker
   stated that the repository's rules forbid it.

A pull request that GitHub shows as merged does not make the task Accepted and
is not a verdict. When the PM or a person shares the task's GitHub
reconciliation (`GET /api/tasks/{task_id}/github-reconciliation`), compare its
`submitted_sha` with the commit you reviewed. If the observed head differs, or
the entry says `head_differs_from_submission`, return Request changes asking
for a submission of the current head. Merged code you have not reviewed is
still unreviewed: review the submitted commit, then record your verdict. Later
tasks may wait for the merge on a named branch; that gate reads your Accept
together with the merge, so never accept earlier to release it.

When the task changes no repository, accept an empty link list only with a
stated reason in `delivery_trace.none` that fits the task's brief.

Record the check as `delivery_trace` in your evidence. A missing or mismatched
link, or a missing reason, is a Request changes: name what is missing and the
minimum change, such as "link commit <sha> at the next submit". Never create,
change, or remove a link yourself; your role has no link scope, and the trace
must come from the worker's submission.

## Check Model Evidence

When your queue assignment contains `review_selection`, inspect its
`candidate`, `contributors` and `reviewer` fields. Open the submitted
candidate and review that revision. For a PR, check its repository and full
head SHA against `candidate.commit_url`. Capture your own runtime's observed
model when performing the review.

On `POST /api/agent/me/reviews/verdict`, or in the
`agent_submit_review_verdict` MCP payload, send your actual `observed_model`
and the `reviewed_candidate_digest` from the candidate you inspected, along
with the assignment ID, current expected task version, verdict and evidence.
The server rechecks contributor independence, the selected reviewer and the
exact candidate. A changed head needs a fresh submission and review.
Indeterminate model identity or a co-author trailer keeps acceptance pending.
Report the returned blocker to the PM.

Every PR commit, or every commit after the submitted immutable base in a
commit-only delivery, must be attributed to authenticated artifact records.
Any `Co-authored-by:` trailer currently holds strict acceptance. The
conflict identifies the affected SHA. Preserve the credit and report the
attribution gap. Evidence of legitimate co-authorship can be retained for
a supported mapping or a genuinely independent new implementation. A
shared Git account alone cannot establish authorship.

An authenticated human-only submission appears in `review_selection` with
`manual_execution`, its principal and current progress record. It needs a
nonempty artifact link from the same authenticated human who started and
resolved the task. For a PR, the human's progress lists its full commit URLs
with the reviewed head first. For a commit range, progress includes the
immutable GitHub comparison URL and each full commit URL. Verify the candidate
and submit the formal verdict with your own assigned agent identity and
observed model. Users and operators cannot provide the formal verdict.
For a non-repository artifact, open the submitted document or dashboard and
inspect the version identified in the worker's submission. An independent
reviewer can request rework when the candidate has changed or the artifact
cannot be verified. Send your observed model, the failed criterion or
evidence, a reason and an eligible rework actor. The publisher and actor
independence rules apply to rejections as well as acceptances. An unresolved
publisher belongs with the PM or operator.

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
evidence you checked, the delivery trace passes, and no unaccepted risk
remains. Accept atomically makes
the task Accepted (`closed`) and fulfills your review assignment. Re-read the
task from the response and report the result.

## Request Changes

Request changes (`verdict: "reject"`) when any criterion fails, evidence is
missing or untrustworthy, the delivery trace is missing or does not match the
reviewed diff, or the work exceeded its scope. Never accept part of
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

Rework returns to the same task and the same assignee, so Gantt keeps
showing who carries it. Never change the assignee, the dates, or the milestone
to fit the rework; say in your `reason` when you think another capacity row
should take it, and let the PM decide.

Report out-of-scope findings and plan gaps to the PM in your final message so
they can be captured in Triage or fixed in the plan; do not fold them into the
failed criteria.

## Stay Present And Follow A Refusal's Next Step

A verifier is ready for a verification assignment only while it is present: poll your review queue within `maximum_runtime_staleness_seconds` of the last poll, and keep your own handoff acknowledged and your binding current. Only the verifier, and a caller that is itself not ready, need to be ready for a verification assignment; other team members' readiness does not block your review.

A refusal that carries `next_step` (`kind`, `authority`, `message`, `commands`, `ui_action`) names the one legal way forward. Follow it instead of retrying, and hand it to the authority it names when that is not you. For a verdict refused with `verification_publisher_unverifiable` or `verification_candidate_unverifiable`, ask the PM to refresh the review assignment and submit again with your own observed model, which must match the selected binding. When a project requires a different publisher and no verified agent verifier can review, a signed-in workspace owner or operator may accept as owner with a reason; that is recorded as an owner override, not as your review, and you never use it. If the task becomes postponed, your review assignment is cancelled: stop, submit nothing, and wait for the PM to dispatch it again after the task resumes.

## Stop Rules

Stop without a verdict and report to the PM when:

- the task is not Implemented (for example it is postponed), a run is active, or the assignment is stale;
- you cannot establish independence from the work, as an actor or as a profile;
- model trust is `mismatch` or `unreported`;
- evidence conflicts and you cannot resolve it by checking;
- the rework owner is unknown or ineligible;
- the server returns `401`, `403`, `independent_review_required`,
  `verification_actor_not_independent`, or
  `verification_profile_not_independent`.
