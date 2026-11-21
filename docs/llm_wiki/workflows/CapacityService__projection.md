# CapacityService__projection

**Entry point:** `capacity_service.CapacityService._projection`
**Modules involved:** [authority](../modules/authority.md), [calendar_rules](../modules/calendar_rules.md), [capacity_service](../modules/capacity_service.md), [services_work_metrics](../modules/services_work_metrics.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `calendar_rules.AnnualCalendars`
3. `calendar_rules.AnnualCalendars.for_iteration`
4. `services_work_metrics.included_work_ids`

## Touches

- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [capacity_service](../modules/capacity_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `capacity_service.CapacityService._projection`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
