# service_worksets_flow

**Entry point:** `service_worksets.run`
**Modules involved:** [delivery](../modules/delivery.md), [local_baseline](../modules/local_baseline.md), [models_agent](../modules/models_agent.md), [models_iteration](../modules/models_iteration.md), [models_task](../modules/models_task.md), [service_worksets](../modules/service_worksets.md), [support_database](../modules/support_database.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `support_database.assert_safe_test_database_url`
2. `delivery.seed_delivery_scenario`
3. `models_iteration.Iteration`
4. `models_task.Task`
5. `models_task.Task`
6. `models_agent.AgentRun`
7. `local_baseline.summarize`

## Touches

- [delivery](../modules/delivery.md)
- [local_baseline](../modules/local_baseline.md)
- [models_agent](../modules/models_agent.md)
- [models_iteration](../modules/models_iteration.md)
- [models_task](../modules/models_task.md)
- [service_worksets](../modules/service_worksets.md)
- [support_database](../modules/support_database.md)

## Behavior

This workflow starts at `service_worksets.run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
