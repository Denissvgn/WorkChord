# AgentRunReadService_list

**Entry point:** `agent_run_read_service.AgentRunReadService.list`
**Modules involved:** [agent_run_read](../modules/agent_run_read.md), [agent_run_read_service](../modules/agent_run_read_service.md), [authority](../modules/authority.md), [execution_usage_service](../modules/execution_usage_service.md), [schemas_agent](../modules/schemas_agent.md)

> Runs of the tasks this request's reader can see, newest first.

Rows follow the request's ORM read scope. The actors and usage reports
the visible runs name are then read internally.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `execution_usage_service.run_identity`
2. `authority.internal_authority`
3. `agent_run_read.AgentRunReadItem`
4. `schemas_agent.AgentAssignmentActorSummary`
5. `agent_run_read.AgentRunHarness`
6. `execution_usage_service.ExecutionUsageService.response`

## Touches

- [agent_run_read](../modules/agent_run_read.md)
- [agent_run_read_service](../modules/agent_run_read_service.md)
- [authority](../modules/authority.md)
- [execution_usage_service](../modules/execution_usage_service.md)
- [schemas_agent](../modules/schemas_agent.md)

## Behavior

This workflow starts at `agent_run_read_service.AgentRunReadService.list`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
