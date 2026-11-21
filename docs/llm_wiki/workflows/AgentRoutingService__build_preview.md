# AgentRoutingService__build_preview

**Entry point:** `agent_routing_service.AgentRoutingService._build_preview`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [query_limits](../modules/query_limits.md), [review_provenance](../modules/review_provenance.md), [services_review_evidence](../modules/services_review_evidence.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup_service.AgentTeamSetupService.membership_boundary`
2. `agent_team_setup_service.AgentTeamSetupService`
3. `query_limits.CollectionLimitExceededError`
4. `query_limits.CollectionLimitExceededError`
5. `task_service.TaskVersionConflictError`
6. `agent_routing.TaskRoutingAssessmentResponse.from_record`
7. `review_provenance.different_publisher_required`
8. `review_provenance.review_history`
9. `services_review_evidence.resolve`
10. `services_review_evidence.assignment_observation`
11. `agent_routing_policy.canonical_routing_json_bytes`
12. `review_provenance.historical_profile`
13. `agent_routing_policy.evaluate_actor_authorization`
14. `agent_service.actor_scopes`
15. `agent_routing_policy.evaluate_assignment_compatibility`
16. `agent_routing_policy.evaluate_required_skills`
17. `query_limits.CollectionLimitExceededError`
18. `agent_routing_policy.evaluate_model_envelope`
19. `services_review_evidence.requirements_for`
20. `agent_routing_policy.routing_candidate_rank_key`
21. `time.as_utc`
22. `agent_routing_policy.canonical_routing_json_bytes`
23. `agent_routing.AgentRoutingPreviewResponse`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [query_limits](../modules/query_limits.md)
- [review_provenance](../modules/review_provenance.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService._build_preview`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
