# record_review_evidence

**Entry point:** `review_evidence.record_review_evidence`
**Modules involved:** [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [query_limits](../modules/query_limits.md), [review_provenance](../modules/review_provenance.md), [schemas_agent_planning](../modules/schemas_agent_planning.md), [services_review_evidence](../modules/services_review_evidence.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `agent_service.is_admin_key_principal`
3. `agent_service.actor_has_scope`
4. `authority.AuthorityError`
5. `schemas_agent_planning.AgentPlanningCommandContext`
6. `review_provenance.digest`
7. `commands.command_transaction`
8. `agent_routing_service.AgentRoutingService`
9. `agent_routing_service.AgentRoutingService._lock_task`
10. `time.utc_now`
11. `query_limits.CollectionLimitExceededError`
12. `review_provenance.select_reviewer`
13. `time.as_utc`
14. `review_provenance.digest`
15. `models_agent.TaskEvent`

## Touches

- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [query_limits](../modules/query_limits.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `review_evidence.record_review_evidence`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
