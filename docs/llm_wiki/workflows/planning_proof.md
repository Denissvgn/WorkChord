# planning_proof

**Entry point:** `planning_window_reconciliation._planning_proof`
**Modules involved:** [agent_planning_service](../modules/agent_planning_service.md), [execution_planning_window](../modules/execution_planning_window.md), [planning_window_reconciliation](../modules/planning_window_reconciliation.md), [snapshot_service](../modules/snapshot_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_planning_service.AgentPlanningService._request_hash`
2. `snapshot_service.SnapshotService._task_to_export`
3. `snapshot_service.SnapshotService`
4. `execution_planning_window.digest`
5. `execution_planning_window.digest`

## Touches

- [agent_planning_service](../modules/agent_planning_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [snapshot_service](../modules/snapshot_service.md)

## Behavior

This workflow starts at `planning_window_reconciliation._planning_proof`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
