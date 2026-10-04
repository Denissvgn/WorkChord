# ExecutionUsageService_summary

**Entry point:** `execution_usage_service.ExecutionUsageService.summary`
**Modules involved:** [authority](../modules/authority.md), [delivery_metrics_service](../modules/delivery_metrics_service.md), [execution_usage_service](../modules/execution_usage_service.md), [query_limits](../modules/query_limits.md), [schemas_execution_usage](../modules/schemas_execution_usage.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `time.utc_now`
3. `query_limits.CollectionLimitExceededError`
4. `delivery_metrics_service.DeliveryMetricsService`
5. `schemas_execution_usage.ExecutionUsageSummary`

## Touches

- [authority](../modules/authority.md)
- [delivery_metrics_service](../modules/delivery_metrics_service.md)
- [execution_usage_service](../modules/execution_usage_service.md)
- [query_limits](../modules/query_limits.md)
- [schemas_execution_usage](../modules/schemas_execution_usage.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `execution_usage_service.ExecutionUsageService.summary`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
