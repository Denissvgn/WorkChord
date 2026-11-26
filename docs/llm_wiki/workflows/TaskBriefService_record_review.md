# TaskBriefService_record_review

**Entry point:** `task_brief_service.TaskBriefService.record_review`
**Modules involved:** [commands](../modules/commands.md), [identity_service](../modules/identity_service.md), [models_task_brief](../modules/models_task_brief.md), [task_brief_service](../modules/task_brief_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.acting_principal_id`
2. `commands.current_command`
3. `models_task_brief.TaskReviewRecord`

## Touches

- [commands](../modules/commands.md)
- [identity_service](../modules/identity_service.md)
- [models_task_brief](../modules/models_task_brief.md)
- [task_brief_service](../modules/task_brief_service.md)

## Behavior

This workflow starts at `task_brief_service.TaskBriefService.record_review`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
