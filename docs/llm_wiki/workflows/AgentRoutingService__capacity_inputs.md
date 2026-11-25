# AgentRoutingService__capacity_inputs

**Entry point:** `agent_routing_service.AgentRoutingService._capacity_inputs`
**Modules involved:** [agent_routing_service](../modules/agent_routing_service.md), [calendar_rules](../modules/calendar_rules.md), [capacity_adjustments](../modules/capacity_adjustments.md), [capacity_service](../modules/capacity_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `capacity_service.CapacityService`
2. `calendar_rules.AnnualCalendars`
3. `calendar_rules.AnnualCalendars.working_dates`
4. `capacity_adjustments.load_dated_availability`
5. `capacity_service.CapacityService.coverage_for`
6. `capacity_service.CapacityService.absence_ranges`

## Touches

- [agent_routing_service](../modules/agent_routing_service.md)
- [calendar_rules](../modules/calendar_rules.md)
- [capacity_adjustments](../modules/capacity_adjustments.md)
- [capacity_service](../modules/capacity_service.md)

## Behavior

Builds the per-row capacity inputs of a routing preview from the effort already allocated in the iteration; it is a bounded static projection, so confirm the exact inputs against the source.
