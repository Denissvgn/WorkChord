# reconcile_execution_request

**Entry point:** `execution_reconciliation.reconcile_execution_request`
**Modules involved:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [execution_reconciliation](../modules/execution_reconciliation.md), [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `agent_service.is_admin_key_principal`
3. `agent_service.actor_has_scope`
4. `authority.AuthorityError`
5. `schemas_agent_planning.AgentPlanningCommandContext`

## Touches

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Behavior

This workflow starts at `execution_reconciliation.reconcile_execution_request`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
