# AgentRoutingService__build_preview

**Entry point:** `agent_routing_service.AgentRoutingService._build_preview`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [query_limits](../modules/query_limits.md), [review_provenance](../modules/review_provenance.md), [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md), [routing_qualification_key_service](../modules/routing_qualification_key_service.md), [services_review_evidence](../modules/services_review_evidence.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup_service.AgentTeamSetupService.membership_boundary`
2. `agent_team_setup_service.AgentTeamSetupService`
3. `query_limits.CollectionLimitExceededError`
4. `query_limits.CollectionLimitExceededError`
5. `task_service.TaskVersionConflictError`
6. `agent_routing.TaskRoutingAssessmentResponse.from_record`
7. `routing_qualification_key_service.active_qualification_keys`
8. `review_provenance.different_publisher_required`
9. `review_provenance.review_history`
10. `review_provenance.execution_profile_history`
11. `services_review_evidence.resolve`
12. `services_review_evidence.assignment_observation`
13. `agent_routing_policy.canonical_routing_json_bytes`
14. `review_provenance.historical_profile`
15. `agent_routing_policy.evaluate_actor_authorization`
16. `agent_service.actor_scopes`
17. `agent_routing_policy.evaluate_assignment_compatibility`
18. `agent_routing_policy.evaluate_required_skills`
19. `query_limits.CollectionLimitExceededError`
20. `agent_routing_policy.evaluate_model_envelope`
21. `services_review_evidence.requirements_for`
22. `agent_routing_policy.routing_candidate_rank_key`
23. `time.as_utc`
24. `routing_calibration_contract_service.approved_calibration_contract_count`
25. `agent_routing_policy.canonical_routing_json_bytes`
26. `agent_routing.AgentRoutingPreviewResponse`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [query_limits](../modules/query_limits.md)
- [review_provenance](../modules/review_provenance.md)
- [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md)
- [routing_qualification_key_service](../modules/routing_qualification_key_service.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService._build_preview`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
