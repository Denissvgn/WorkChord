# AgentRoutingService_create_assessment

**Entry point:** `agent_routing_service.AgentRoutingService.create_assessment`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [task_service](../modules/task_service.md)

> Append one server-attributed assessment for the current task version.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `task_service.TaskVersionConflictError`
3. `agent_routing_policy.review_mode_meets`
4. `agent_routing.TaskRoutingAssessmentCreate`
5. `models_agent.TaskRoutingAssessment`
6. `agent_routing.TaskRoutingAssessmentResponse.from_record`
7. `agent_routing_observability.record_routing_operational_event`
8. `agent_routing.TaskRoutingAssessmentMutationReceipt`
9. `models_agent.AgentIdempotencyRecord`
10. `commands.commit_or_flush`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService.create_assessment`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
