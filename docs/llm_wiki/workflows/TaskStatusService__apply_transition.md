# TaskStatusService__apply_transition

**Entry point:** `task_status_service.TaskStatusService._apply_transition`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [services_work_metrics](../modules/services_work_metrics.md), [task_reactivation_service](../modules/task_reactivation_service.md), [task_status_log](../modules/task_status_log.md), [task_status_service](../modules/task_status_service.md), [time](../modules/time.md)

> Run the shared mutation, audit, delivery, and notification semantics.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `services_work_metrics.working_today`
2. `time.utc_now`
3. `identity_service.acting_principal_id`
4. `task_status_log.TaskStatusLog`
5. `authority.internal_authority`
6. `outbound_webhook_service.OutboundWebhookService.enqueue_status_change`
7. `outbound_webhook_service.OutboundWebhookService`
8. `task_reactivation_service.request_reactivation_check`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [task_status_log](../modules/task_status_log.md)
- [task_status_service](../modules/task_status_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_status_service.TaskStatusService._apply_transition`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
