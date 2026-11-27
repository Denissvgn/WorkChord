# command_transaction

**Entry point:** `commands.command_transaction`
**Modules involved:** [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [discussion_service](../modules/discussion_service.md), [task_reactivation_service](../modules/task_reactivation_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_reactivation_service.process_reactivation_checks`
2. `delivery_dependency_service.DeliveryDependencyService.reconcile`
3. `delivery_dependency_service.DeliveryDependencyService`
4. `discussion_service.DiscussionService.enqueue`
5. `discussion_service.DiscussionService`

## Touches

- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)

## Behavior

This workflow starts at `commands.command_transaction`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
