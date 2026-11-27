# TaskReplacementService__move_dependents

**Entry point:** `task_replacement_service.TaskReplacementService._move_dependents`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [models_delivery_dependency](../modules/models_delivery_dependency.md), [task_replacement_service](../modules/task_replacement_service.md)

> Point each dependent at the replacement; prerequisite identity, not dependent work, changes.

A dependent keeps its version, so work already issued for it stays valid,
and its downstream evidence is not invalidated by this re-pointing. With
``delivered`` (a supersession), a schedule dependent of an original whose
successor is in another iteration gets a delivery prerequisite on the
successor instead of a schedule edge (action ``converted``).

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `authority.require_project`
3. `models_delivery_dependency.DeliveryDependency`
4. `commands.PlanningConflict`
5. `delivery_dependency_service.DeliveryDependencyService.validate_cycles`
6. `delivery_dependency_service.DeliveryDependencyService`
7. `commands.PlanningConflict`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [models_delivery_dependency](../modules/models_delivery_dependency.md)
- [task_replacement_service](../modules/task_replacement_service.md)

## Behavior

Points each schedule and delivery dependent of the original at the replacement, merging duplicates and removing self-edges. A dependent keeps its version, so issued work stays valid. The decider needs edit access to every dependent project, schedule dependents can follow only a replacement in the original's iteration, and a resulting cycle refuses the whole command.
