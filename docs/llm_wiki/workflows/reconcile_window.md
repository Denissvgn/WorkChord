# reconcile_window

**Entry point:** `planning_window_reconciliation.reconcile_window`
**Modules involved:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [models_agent](../modules/models_agent.md), [models_identity](../modules/models_identity.md), [planning_window_reconciliation](../modules/planning_window_reconciliation.md), [schemas_agent_planning](../modules/schemas_agent_planning.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `agent_service.is_admin_key_principal`
3. `agent_service.actor_has_scope`
4. `authority.AuthorityError`
5. `schemas_agent_planning.AgentPlanningCommandContext`
6. `commands.command_transaction`
7. `execution_planning_window.digest`
8. `agent_model_catalog_service.AgentModelConflictError`
9. `task_service.TaskService.get_by_id`
10. `task_service.TaskService`
11. `execution_planning_window.live_assignments`
12. `execution_planning_window.original_ownership`
13. `execution_planning_window.make_window`
14. `execution_planning_window.seal_authority`
15. `execution_planning_window.digest`
16. `agent_model_catalog_service.AgentModelConflictError`
17. `models_agent.TaskEvent`
18. `models_identity.CommandAudit`

## Touches

- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [models_agent](../modules/models_agent.md)
- [models_identity](../modules/models_identity.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `planning_window_reconciliation.reconcile_window`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
