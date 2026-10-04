# DeliveryMetricsService_report

**Entry point:** `delivery_metrics_service.DeliveryMetricsService.report`
**Modules involved:** [authority](../modules/authority.md), [delivery_metrics](../modules/delivery_metrics.md), [delivery_metrics_service](../modules/delivery_metrics_service.md), [query_limits](../modules/query_limits.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `time.as_utc`
3. `time.utc_now`
4. `query_limits.CollectionLimitExceededError`
5. `query_limits.CollectionLimitExceededError`
6. `authority.internal_authority`
7. `delivery_metrics.DeliveryQueueItem`
8. `time.as_utc`
9. `query_limits.CollectionLimitExceededError`
10. `time.as_utc`
11. `delivery_metrics.DeliveryQueueItem`
12. `time.as_utc`
13. `delivery_metrics.DeliveryMetricsResponse`

## Touches

- [authority](../modules/authority.md)
- [delivery_metrics](../modules/delivery_metrics.md)
- [delivery_metrics_service](../modules/delivery_metrics_service.md)
- [query_limits](../modules/query_limits.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `delivery_metrics_service.DeliveryMetricsService.report`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
