# Stacked merge queue

An example script for repositories where several pull requests regenerate the same
shared files (generated documentation, contract fixtures) and each pull request
belongs to a WorkChord task. Merging such pull requests in parallel makes every
merge conflict the others, and a conflicting pull request gets no CI on GitHub. The queue
avoids that by stacking them and merging one at a time.

It is an example to adapt, not part of the product. It needs `zsh`, `git`, the
GitHub CLI (`gh`, signed in) and `python3`; `curl` is needed only for the read-only
WorkChord task check.

## What it does

- Takes an ordered list of `branch:task id:regeneration commit subject` items.
- Keeps up to `DEPTH` pull requests in CI at once. Item k is prepared on top of
  item k-1's branch, so when k-1 merges, k is only behind `main` and merges on its
  own green CI.
- Merges strictly bottom first, using `--match-head-commit` so only the checked head
  can merge, and only when the pull request's review decision is `APPROVED`
  (see `REQUIRE_APPROVAL`).
- Reruns the failed jobs once per head commit, to absorb flaky checks. A second
  failure stops the queue.
- Is restart-safe: run it again with the same arguments. Merged items are skipped
  and prepared branches are reused when they still contain their base and end in the
  regeneration commit.
- Runs read-only with `DRY=1`, printing each item as merged, valid or needing
  preparation.

```sh
WORKTREE=~/queue-worktree BODY_DIR=~/pr-bodies \
REGEN_CMD='scripts/regenerate-shared-files.sh' \
  ./stacked_merge_queue.sh \
    "feature/a:101:Regenerate shared files for a" \
    "feature/b:102:Regenerate shared files for b"
```

## Environment variables

| Variable | Meaning |
| --- | --- |
| `WORKTREE` | Required. A separate clean worktree the queue may switch freely. |
| `BODY_DIR` | Required. Pull request bodies named `<branch with / as ->.md`; the first line is `# <title>`. |
| `REPO` | Checkout used for fetching and GitHub queries. Default: the current directory. |
| `REGEN_CMD` | Regenerates the shared files and commits them with the subject passed as `$1`. Print `no changes` when there is nothing to commit. Optional. |
| `RESOLVE_CMD` | Resolves known mechanical merge conflicts in the current checkout. Optional. |
| `GENERATED_DIR` | Repository-relative path; conflicts under it take the base's version. Absolute paths and `..` are refused. Optional. |
| `REQUIRE_APPROVAL` | `1` (default) merges only approved pull requests. `0` leaves review to branch protection. |
| `DEPTH` | Pull requests in CI at once. Default: 3. |
| `STATE_DIR` | Lock, rerun and no-change bookkeeping. Default: a folder under `TMPDIR` keyed by the repository's remote URL. |
| `WORKCHORD_URL` | API base, for example `https://workchord.example.com/api`. Without it the task check is skipped. |
| `WORKCHORD_API_KEY` | Key used only to read tasks, from the environment and never printed. Required when `WORKCHORD_URL` is set. |
| `DRY` | Set to `1` for the read-only status. |

## WorkChord task check

The queue never writes task statuses. They move through the lifecycle planned,
active, resolved, closed by WorkChord's own flows: the worker's submit resolves
the task, a person resolves manual work, and a pass verdict from the verifier or
an owner's acceptance closes it. Agent keys are refused on the status route, and
a status write from outside those flows would bypass the execution fence.

After each merge the queue reads the task. If it is not `closed`, it logs
`STATUS DRIFT` with the actual status. Check for a missing pass verdict or owner
acceptance, and for prerequisites that are still open; then resolve that in
WorkChord. A pull request that merged before its review was recorded is the usual
cause.

## Safety rules

- Never force-pushes, never deletes or resets a remote branch, never closes a pull
  request.
- Merges only the bottom item, only after green CI and an approved review (unless
  `REQUIRE_APPROVAL=0`), only for the head it checked.
- Writes nothing to WorkChord.
- Pushes only the item branches it prepares, and only new commits.
- Stops instead of guessing: on a dirty worktree, a push rejection, a failed
  regeneration, a second CI failure, or a merge conflict that `RESOLVE_CMD` and
  `GENERATED_DIR` cannot resolve.
- A lock directory in `STATE_DIR` keeps two queues from running at once.
- The API key is only sent as a request header for reading and is never logged.
- `GENERATED_DIR` is checked before anything is removed.
