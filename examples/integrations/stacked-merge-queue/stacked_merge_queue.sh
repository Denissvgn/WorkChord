#!/usr/bin/env zsh
# Stacked merge queue for a repository whose PRs regenerate shared files (for example a
# generated architecture wiki) and whose tasks are tracked in WorkChord.
#
# Usage:
#   stacked_merge_queue.sh "<branch>:<task id>:<regeneration commit subject>" ...
#   DRY=1 stacked_merge_queue.sh ...          # read-only status of every item
#
# Up to DEPTH PRs are in CI at once. Item k is prepared on top of item k-1's branch, so when
# k-1 merges, k is only behind main and merges on its own green CI. Items merge strictly in
# order, bottom first.
#
# Safety: never force-pushes, never deletes or resets a remote branch, never closes a PR;
# merges only the bottom item with --match-head-commit after green CI and an approved review
# (REQUIRE_APPROVAL=0 leaves review to branch protection); re-runs failed jobs once per head;
# stops on a second failure or on a merge conflict it cannot resolve; can be rerun with the
# same arguments to resume (merged items are skipped, prepared ones reused). It never writes
# WorkChord task statuses: it only reads each task after its merge and reports STATUS DRIFT.
#
# Configuration (environment):
#   REPO           checkout used for fetch and GitHub queries            (default: .)
#   WORKTREE       a separate clean worktree the queue may switch freely (required)
#   BODY_DIR       PR bodies: <branch with / as ->.md, first line "# <title>" (required)
#   REGEN_CMD      regenerates shared files and commits them with the subject in $1
#                  (optional; prints "no changes" when there is nothing to commit)
#   RESOLVE_CMD    resolves known mechanical conflicts in the current checkout (optional)
#   GENERATED_DIR  conflicts under this repository-relative path take the base's version
#                  (optional; absolute paths and ".." are refused)
#   REQUIRE_APPROVAL  1 (default) merges only PRs whose review decision is APPROVED; 0 leaves
#                  review to branch protection
#   DEPTH          PRs in CI at once                                     (default: 3)
#   WORKCHORD_URL  e.g. https://workchord.example.com/api                (optional)
#   WORKCHORD_API_KEY  key used only to read tasks, from the environment, never printed
#   STATE_DIR      lock and bookkeeping (default: per repository, under TMPDIR)
set -u
: ${REPO:=.} ${DEPTH:=3} ${GENERATED_DIR:=} ${REGEN_CMD:=} ${RESOLVE_CMD:=} ${REQUIRE_APPROVAL:=1}
: ${WORKTREE:?set WORKTREE} ${BODY_DIR:?set BODY_DIR}
if [[ -n $GENERATED_DIR ]] && [[ $GENERATED_DIR == /* || $GENERATED_DIR == *..* ]]; then
  print -u2 "GENERATED_DIR must be a repository-relative path without '..'"; exit 2; fi
GENERATED_DIR=${GENERATED_DIR%/}
if [ -n "${WORKCHORD_URL:-}" ] && [ -z "${WORKCHORD_API_KEY:-}" ]; then
  print -u2 "WORKCHORD_URL is set but WORKCHORD_API_KEY is not"; exit 2; fi
REPO_KEY=$(git -C $REPO remote get-url origin 2>/dev/null | (shasum 2>/dev/null || sha1sum) | cut -c1-12)
STATE_DIR=${STATE_DIR:-${TMPDIR:-/tmp}/stacked-merge-queue-${REPO_KEY:-local}}; mkdir -p $STATE_DIR
NOCHANGE=$STATE_DIR/nochange.txt; touch $NOCHANGE; LOCK=$STATE_DIR/lock
log(){ print -r -- "$(date +%H:%M) $*"; }

# --- WorkChord task check (read-only) ---------------------------------------------------------
# Task statuses are never written here: the worker's submit, a verifier's pass verdict or an
# owner's acceptance move them. After a merge the task should be closed; if it is not, a
# verdict, an acceptance or an open prerequisite is missing.
task_status(){
  curl -fsS "$WORKCHORD_URL/tasks/$1" -H "X-Agent-API-Key: $WORKCHORD_API_KEY" |
    python3 -c "import json,sys; print(json.load(sys.stdin)['status'])"
}
check_task(){  # check_task TASK PR
  [ -n "${WORKCHORD_URL:-}" ] || return 0
  local st; st=$(task_status $1 2>/dev/null)
  [ "$st" = closed ] && log "task $1 closed" ||
    log "STATUS DRIFT: task $1 is '${st:-unreadable}' after PR #$2 merged; check for a pass verdict or owner acceptance and for open prerequisites"
  return 0
}

# --- GitHub ------------------------------------------------------------------------------------
cd $REPO
fetch(){ git fetch -q origin || { sleep 30; git fetch -q origin; }; }
open_pr(){ gh pr list --head $1 --state open --json number --jq '.[0].number // empty' 2>/dev/null; }
merged_pr(){ gh pr list --head $1 --state merged --json number --jq '.[0].number // empty' 2>/dev/null; }
approved(){ [ "$REQUIRE_APPROVAL" = 0 ] || [ "$(gh pr view $1 --json reviewDecision --jq .reviewDecision 2>/dev/null)" = APPROVED ]; }
pr_state(){ gh pr view $1 --json headRefOid,mergeStateStatus,statusCheckRollup --jq '[.mergeStateStatus, .headRefOid,
  ([.statusCheckRollup[]|select(.status!="COMPLETED")]|length),
  ([.statusCheckRollup[]|select(.status=="COMPLETED" and (.conclusion|IN("SUCCESS","SKIPPED","NEUTRAL")|not))]|length),
  (.statusCheckRollup|length)]|@tsv' 2>/dev/null; }

typeset -a BR TK SJ; typeset -A RERUN BLOCKED
for item in "$@"; do BR+=${item%%:*}; r=${item#*:}; TK+=${r%%:*}; SJ+=${r#*:}; done
N=${#BR}; (( N )) || { log "no items"; exit 1; }
first=1
base_of(){ (( $1 > first )) && print origin/${BR[$(($1-1))]} || print origin/main; }
valid(){  # branch holds every commit of its base and its tip is the regeneration commit
  git rev-parse -q --verify origin/$1 >/dev/null || return 1
  [ -z "$(git rev-list --no-merges origin/$1..$2 | head -1)" ] || return 1
  [ -z "$REGEN_CMD" ] && return 0
  [[ "$(git log -1 --format=%s origin/$1)" == "${3}"* ]] || grep -qx "$(git rev-parse origin/$1)" $NOCHANGE
}

prepare(){  # prepare BRANCH BASE SUBJECT
  ( cd $WORKTREE || exit 1
    [ -z "$(git status --porcelain --untracked-files=no)" ] || { log "STOP: $WORKTREE is not clean"; exit 9; }
    git fetch -q origin && git switch -q -C $1 origin/$1 || exit 1
    if [ -n "$(git rev-list --no-merges HEAD..$2 | head -1)" ] && ! git merge -q --no-edit $2; then
      [ -n "$RESOLVE_CMD" ] && eval "$RESOLVE_CMD"
      if [ -n "$GENERATED_DIR" ]; then
        git diff --name-only --diff-filter=U | grep -qF -e "$GENERATED_DIR/" && {
          git rm -r -q --cached -- "$GENERATED_DIR"; rm -rf -- "./$GENERATED_DIR"; git checkout $2 -- "$GENERATED_DIR"; }
      fi
      U=$(git diff --name-only --diff-filter=U)
      [ -z "$U" ] || { log "STOP: conflicts with $2 need a person:"; print -r -- "$U"; git merge --abort; exit 4; }
      git commit -q --no-edit || exit 1
    fi
    if [ -n "$REGEN_CMD" ]; then
      O=$(eval "$REGEN_CMD \"\$3\"" 2>&1) || { print -r -- "$O" | tail -5; log "STOP: regeneration failed"; exit 6; }
      print -r -- "$O" | grep -q "no changes" && git rev-parse HEAD >> $NOCHANGE
    fi
    git push -q origin $1 || { log "STOP: push of $1 rejected"; exit 5; }
    if [ -z "$(open_pr $1)" ]; then
      F=$BODY_DIR/${1//\//-}.md; [ -f $F ] || { log "STOP: no PR body at $F"; exit 7; }
      tail -n +2 $F > $STATE_DIR/body.md
      gh pr create --base main --head $1 --title "$(head -1 $F | sed 's/^# *//')" --body-file $STATE_DIR/body.md >/dev/null || exit 8
      log "opened PR #$(open_pr $1)"
    fi
    git switch -q --detach origin/main ) || return 1
}

if [ "${DRY:-0}" = 1 ]; then
  fetch
  for (( k = 1; k <= N; k++ )); do
    m=$(merged_pr ${BR[$k]}); [ -n "$m" ] && { print "$k ${BR[$k]}: merged #$m"; continue; }
    valid ${BR[$k]} $(base_of $k) "${SJ[$k]}" && v=valid || v=needs-prepare
    print "$k ${BR[$k]} task ${TK[$k]}: $v, open PR '$(open_pr ${BR[$k]})'"
  done; exit 0
fi

mkdir $LOCK 2>/dev/null || { log "STOP: another queue holds $LOCK"; exit 2; }
trap 'rmdir $LOCK 2>/dev/null' EXIT INT TERM
while (( first <= N )) && m=$(merged_pr ${BR[$first]}) && [ -n "$m" ]; do
  log "already merged: ${BR[$first]} (#$m)"; check_task ${TK[$first]} $m; (( first++ ))
done

while (( first <= N )); do
  fetch
  last=$(( first + DEPTH - 1 )); (( last > N )) && last=$N
  for (( k = first; k <= last; k++ )); do          # prepare the window, bottom first
    B=${BR[$k]}; [ -n "${BLOCKED[$B]:-}" ] && break
    if ! valid $B $(base_of $k) "${SJ[$k]}" || [ -z "$(open_pr $B)" ]; then
      log "=== prepare $B on $(base_of $k)"
      prepare $B $(base_of $k) "${SJ[$k]}" && fetch || { BLOCKED[$B]=1; log "BLOCKED $B"; break; }
    fi
  done
  for (( k = first; k <= last; k++ )); do          # one re-run per failed head (flakes)
    B=${BR[$k]}; PR=$(open_pr $B); [ -n "$PR" ] || continue
    read st sha pend bad total <<< "$(pr_state $PR)"
    if [ "$pend" = 0 ] && [ "${bad:-0}" != 0 ] && [ -z "${RERUN[$sha]:-}" ]; then
      RUN=$(gh run list --branch $B --commit $sha --json databaseId --jq '.[0].databaseId // empty')
      [ -n "$RUN" ] && { log "PR #$PR failed at ${sha:0:9}; re-running failed jobs once"; gh run rerun $RUN --failed >/dev/null 2>&1; }
      RERUN[$sha]=$(date +%s)
    fi
  done
  B=${BR[$first]}; T=${TK[$first]}                  # act on the bottom item only
  [ -n "${BLOCKED[$B]:-}" ] && { log "STOP: $B is blocked; fix it and rerun with the same items"; exit 4; }
  PR=$(open_pr $B); [ -n "$PR" ] || { sleep 60; continue; }
  read st sha pend bad total <<< "$(pr_state $PR)"
  if [ "${st:-}" = DIRTY ]; then prepare $B origin/main "${SJ[$first]}" || BLOCKED[$B]=1; continue; fi
  if [ -z "${st:-}" ] || [ "${total:-0}" = 0 ] || [ "$pend" != 0 ] || [ "$st" = UNKNOWN ]; then sleep 60; continue; fi
  if [ "$bad" != 0 ]; then
    if [ -n "${RERUN[$sha]:-}" ] && (( $(date +%s) - RERUN[$sha] > 300 )); then
      log "STOP: PR #$PR failed CI after one re-run"; exit 4; fi
    sleep 60; continue
  fi
  if [[ $st == (CLEAN|BEHIND) ]] && ! approved $PR; then log "PR #$PR is green but not approved; waiting"; sleep 60
  elif [[ $st == (CLEAN|BEHIND) ]]; then
    gh pr merge $PR --merge --match-head-commit $sha >/dev/null 2>&1 || { log "merge of #$PR refused; retrying"; sleep 60; continue; }
    log "MERGED #$PR $B"; check_task $T $PR; (( first++ ))
  else sleep 60; fi
done
log "QUEUE DONE"
