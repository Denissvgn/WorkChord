# AgentPlanningService__schedule_input_digest

**Entry point:** `agent_planning_service.AgentPlanningService._schedule_input_digest`
**Modules involved:** [agent_planning_service](../modules/agent_planning_service.md), [agent_service](../modules/agent_service.md), [calendar_rules](../modules/calendar_rules.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md)

> Hash every mutable input consumed by ``SchedulerService``.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentConflictError`
2. `commands.current_command`
3. `capacity_service.CapacityService`
4. `calendar_rules.AnnualCalendars.for_iteration`
5. `capacity_service.CapacityService.coverage_for`

## Touches

- [agent_planning_service](../modules/agent_planning_service.md)
- [agent_service](../modules/agent_service.md)
- [calendar_rules](../modules/calendar_rules.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)

## Behavior

This workflow starts at `agent_planning_service.AgentPlanningService._schedule_input_digest`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
