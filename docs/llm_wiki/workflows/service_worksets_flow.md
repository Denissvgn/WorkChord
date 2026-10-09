# service_worksets_flow

**Entry point:** `service_worksets.run`
**Modules involved:** [delivery](../modules/delivery.md), [local_baseline](../modules/local_baseline.md), [models_agent](../modules/models_agent.md), [models_iteration](../modules/models_iteration.md), [models_task](../modules/models_task.md), [service_worksets](../modules/service_worksets.md), [source_binding](../modules/source_binding.md), [support_database](../modules/support_database.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source_binding.source_binding`
2. `support_database.assert_safe_test_database_url`
3. `delivery.seed_delivery_scenario`
4. `models_iteration.Iteration`
5. `models_task.Task`
6. `models_task.Task`
7. `models_agent.AgentRun`
8. `local_baseline.summarize`
9. `source_binding.verify_binding`

## Touches

- [delivery](../modules/delivery.md)
- [local_baseline](../modules/local_baseline.md)
- [models_agent](../modules/models_agent.md)
- [models_iteration](../modules/models_iteration.md)
- [models_task](../modules/models_task.md)
- [service_worksets](../modules/service_worksets.md)
- [source_binding](../modules/source_binding.md)
- [support_database](../modules/support_database.md)

## Behavior

This workflow starts at `service_worksets.run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
