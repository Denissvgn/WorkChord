# SchedulerService___init__

**Entry point:** `scheduler_service.SchedulerService.__init__`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [scheduler_service](../modules/scheduler_service.md), [scheduling_rules_service](../modules/scheduling_rules_service.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `calendar_service.CalendarService`
2. `task_service.TaskService`
3. `team_service.TeamService`
4. `scheduling_rules_service.SchedulingRulesService.get_instance`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [scheduler_service](../modules/scheduler_service.md)
- [scheduling_rules_service](../modules/scheduling_rules_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `scheduler_service.SchedulerService.__init__`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
