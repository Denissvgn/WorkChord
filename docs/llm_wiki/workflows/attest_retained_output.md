# attest_retained_output

**Entry point:** `retained_planning_output.attest_retained_output`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [github_links](../modules/github_links.md), [retained_planning_output](../modules/retained_planning_output.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.require_scope`
2. `agent_service.validate_idempotency_key`
3. `commands.command_transaction`
4. `agent_service.AgentPermissionError`
5. `agent_work_service.AgentWorkService`
6. `agent_work_service.AgentWorkService._lock_task`
7. `agent_work_service.AgentWorkService._lock_actors`
8. `agent_work_service.AgentWorkService._lock_task_assignments`
9. `agent_work_service.AgentWorkService._lock_task_runs`
10. `agent_work_service.AgentWorkService._idempotent_replay`
11. `agent_service.AgentConflictError`
12. `github_links.parse_github_url`
13. `github_links.parse_github_url`
14. `time.utc_now`
15. `agent_work_service.AgentWorkService._record_idempotency`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [github_links](../modules/github_links.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `retained_planning_output.attest_retained_output`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
