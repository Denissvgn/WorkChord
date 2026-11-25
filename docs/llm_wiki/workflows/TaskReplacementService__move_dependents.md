# TaskReplacementService__move_dependents

**Entry point:** `task_replacement_service.TaskReplacementService._move_dependents`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_replacement_service](../modules/task_replacement_service.md)

> Point each dependent at the replacement; prerequisite identity, not dependent work, changes.

A dependent keeps its version, so work already issued for it stays valid,
and its downstream evidence is not invalidated by this re-pointing.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `authority.require_project`
3. `commands.PlanningConflict`
4. `delivery_dependency_service.DeliveryDependencyService.validate_cycles`
5. `delivery_dependency_service.DeliveryDependencyService`
6. `commands.PlanningConflict`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)

## Behavior

Points each schedule and delivery dependent of the original at the replacement, merging duplicates and removing self-edges. A dependent keeps its version, so issued work stays valid. The decider needs edit access to every dependent project, schedule dependents can follow only a replacement in the original's iteration, and a resulting cycle refuses the whole command.
