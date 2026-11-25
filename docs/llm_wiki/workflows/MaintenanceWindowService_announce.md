# MaintenanceWindowService_announce

**Entry point:** `maintenance_window_service.MaintenanceWindowService.announce`
**Modules involved:** [commands](../modules/commands.md), [maintenance_window_service](../modules/maintenance_window_service.md), [models_maintenance](../modules/models_maintenance.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `models_maintenance.MaintenanceWindow`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [maintenance_window_service](../modules/maintenance_window_service.md)
- [models_maintenance](../modules/models_maintenance.md)
- [time](../modules/time.md)

## Behavior

A coordinated control-plane maintenance window has one open window at a time. Announcing it closes admission for new work at once; work already holding a live claim keeps renewing and may finish. The operator can begin only when every live claim owner has acknowledged for the claim's current generation, each lease outlives the bounded outage plus its margin, no running run lacks a live claim and every PM has a notice receipt. A PM notice is recorded evidence of notification, never run-owner consent. Closing or cancelling reopens admission. Announce validates a bounded window of at most 24 hours ending in the future, refuses a second open window and closes admission.
