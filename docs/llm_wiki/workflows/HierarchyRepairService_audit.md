# HierarchyRepairService_audit

**Entry point:** `hierarchy_repair_service.HierarchyRepairService.audit`
**Modules involved:** [authority](../modules/authority.md), [hierarchy_repair_service](../modules/hierarchy_repair_service.md), [services_work_metrics](../modules/services_work_metrics.md), [task_status_service](../modules/task_status_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `services_work_metrics.scoped_metric_tasks`
3. `task_status_service.TaskStatusService.derive_parent_status`
4. `services_work_metrics.task_signals`
5. `services_work_metrics.effective_work_flags`

## Touches

- [authority](../modules/authority.md)
- [hierarchy_repair_service](../modules/hierarchy_repair_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_status_service](../modules/task_status_service.md)

## Behavior

This workflow starts at `hierarchy_repair_service.HierarchyRepairService.audit`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
