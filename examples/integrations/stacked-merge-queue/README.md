# Stacked merge queue

An example script for repositories where several pull requests regenerate the same
shared files (generated documentation, contract fixtures) and each pull request
belongs to a WorkChord task. Merging such pull requests in parallel makes every
merge conflict the others, and a conflicting pull request gets no CI. The queue
avoids that by stacking them and merging one at a time.

It is an example to adapt, not part of the product. It needs `zsh`, `git`, the
GitHub CLI (`gh`, signed in) and `python3`; `curl` is needed only for the WorkChord
status updates.

## What it does

- Takes an ordered list of `branch:task id:regeneration commit subject` items.
- Keeps up to `DEPTH` pull requests in CI at once. Item k is prepared on top of
  item k-1's branch, so when k-1 merges, k is only behind `main` and merges on its
  own green CI.
- Merges strictly bottom first, using `--match-head-commit` so only the checked head
  can merge.
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
| `GENERATED_DIR` | Conflicts under this path take the base's version. Optional. |
| `DEPTH` | Pull requests in CI at once. Default: 3. |
| `STATE_DIR` | Lock, rerun and no-change bookkeeping. Default: a folder under `TMPDIR`. |
| `WORKCHORD_URL` | API base, for example `https://workchord.example.com/api`. Without it the status updates are skipped. |
| `WORKCHORD_API_KEY` | Agent or operator key, read from the environment and never printed. |
| `CLOSE_REASON` | Reason recorded when a task is closed after its merge. |
| `DRY` | Set to `1` for the read-only status. |

## WorkChord status flow

The queue follows the task lifecycle planned, active, resolved, closed:

1. When a pull request is opened for an item, the task is marked resolved: its work
   is pushed and the pull request is open for review. A task still `planned` is moved
   to `active` first, because the server refuses planned to resolved while
   prerequisites are open.
2. After the pull request merges, the task is closed with `CLOSE_REASON`, without any
   override.
3. If a task is not closed afterwards (for example its prerequisites or its review
   outcome are still open), the queue logs `STATUS DRIFT` with the task's actual
   status. Fix the cause in WorkChord; the queue does not force the status.

Record the review outcome in WorkChord (the verification flow, or owner acceptance
with a reason) before the merge, or the close will be refused and reported as drift.

## Safety rules

- Never force-pushes, never deletes or resets a remote branch, never closes a pull
  request.
- Merges only the bottom item, only after green CI, only for the head it checked.
- Pushes only the item branches it prepares, and only new commits.
- Stops instead of guessing: on a dirty worktree, a push rejection, a failed
  regeneration, a second CI failure, or a merge conflict that `RESOLVE_CMD` and
  `GENERATED_DIR` cannot resolve.
- A lock directory in `STATE_DIR` keeps two queues from running at once.
- The API key is only sent as a request header and is never logged.
