# reconcile_execution

**Entry point:** `execution_reconciliation.reconcile_execution`
**Modules involved:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [execution_reconciliation](../modules/execution_reconciliation.md), [models_agent](../modules/models_agent.md), [models_identity](../modules/models_identity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `authority.AuthorityError`
3. `commands.command_transaction`
4. `agent_team_setup_service._digest`
5. `agent_team_setup_service._digest`
6. `agent_model_catalog_service.AgentModelConflictError`
7. `agent_team_setup_service._digest`
8. `agent_model_catalog_service.AgentModelConflictError`
9. `models_agent.TaskEvent`
10. `models_identity.CommandAudit`

## Touches

- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [models_agent](../modules/models_agent.md)
- [models_identity](../modules/models_identity.md)

## Behavior

The operator previews a single run to see the evidence digest and any missing attribution. Apply locks that run and compares the digest again. An exact idempotent retry returns the first response. A mismatched digest requires a new preview, and conflicting stored evidence stays visible in the result.
