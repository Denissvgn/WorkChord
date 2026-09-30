# AgentRoutingService__build_preview

**Entry point:** `agent_routing_service.AgentRoutingService._build_preview`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [query_limits](../modules/query_limits.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup_service.AgentTeamSetupService`
2. `query_limits.CollectionLimitExceededError`
3. `query_limits.CollectionLimitExceededError`
4. `task_service.TaskVersionConflictError`
5. `agent_routing.TaskRoutingAssessmentResponse.from_record`
6. `agent_routing_policy.canonical_routing_json_bytes`
7. `agent_routing_policy.evaluate_actor_authorization`
8. `agent_service.actor_scopes`
9. `agent_routing_policy.evaluate_assignment_compatibility`
10. `agent_routing_policy.evaluate_required_skills`
11. `query_limits.CollectionLimitExceededError`
12. `agent_routing_policy.evaluate_model_envelope`
13. `agent_routing_policy.routing_candidate_rank_key`
14. `time.as_utc`
15. `agent_routing_policy.canonical_routing_json_bytes`
16. `agent_routing_policy.canonical_routing_json_bytes`
17. `agent_routing.AgentRoutingPreviewResponse`
18. `agent_routing_policy.validate_routing_packet_size`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [query_limits](../modules/query_limits.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService._build_preview`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
