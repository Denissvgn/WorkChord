# TaskStatusService__apply_transition

**Entry point:** `task_status_service.TaskStatusService._apply_transition`
**Modules involved:** [outbound_webhook_service](../modules/outbound_webhook_service.md), [services_work_metrics](../modules/services_work_metrics.md), [task_status_log](../modules/task_status_log.md), [task_status_service](../modules/task_status_service.md), [time](../modules/time.md)

> Run the shared mutation, audit, delivery, and notification semantics.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `services_work_metrics.working_today`
2. `time.utc_now`
3. `task_status_log.TaskStatusLog`
4. `outbound_webhook_service.OutboundWebhookService`

## Touches

- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_status_log](../modules/task_status_log.md)
- [task_status_service](../modules/task_status_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_status_service.TaskStatusService._apply_transition`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
