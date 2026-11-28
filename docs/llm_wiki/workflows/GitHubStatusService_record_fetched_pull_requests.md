# GitHubStatusService_record_fetched_pull_requests

**Entry point:** `github_status_service.GitHubStatusService.record_fetched_pull_requests`
**Modules involved:** [commands](../modules/commands.md), [github_reconciliation_service](../modules/github_reconciliation_service.md), [github_status_service](../modules/github_status_service.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> Record several already fetched links of one task under one task revision.

Runs inside one command: the task context (planning, iteration, task) is
reserved once, then each link is locked and saved in order. A raised
error rolls back every link together; a provider error is cached on its
link like any other observation.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.command_transaction`
2. `github_reconciliation_service.observed_head_keeps_acceptance`
3. `task_context_revision_service.reserve_task_context_revision`

## Touches

- [commands](../modules/commands.md)
- [github_reconciliation_service](../modules/github_reconciliation_service.md)
- [github_status_service](../modules/github_status_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

Catch-up fetches every link before any lock is taken; this step then records them in one command transaction. A link that no longer exists is skipped, and an observation older than the stored one is skipped. If anything is left to record, the task context is reserved once as a single `github_status_refresh` revision, outcome `provider_error` when every recorded item failed. The revision preserves acceptance only when each observed head is still the commit acceptance covers (`observed_head_keeps_acceptance`: the last submitted commit for the link, else the previously recorded head, and acceptance is kept when none was recorded before; an observation that names no head does not keep it). Each item is then applied under its link row lock, a provider error is cached on its link, and a merge or unmerged closure is recorded as a task event once, keyed by link, status and merge commit or close time. Any other error rolls back all links.
