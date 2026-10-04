# build_examples

**Entry point:** `generate_mobile_contract_fixtures.build_examples`
**Modules involved:** [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md), [schemas_task](../modules/schemas_task.md), [schemas_task_brief](../modules/schemas_task_brief.md), [schemas_task_domain](../modules/schemas_task_domain.md), [session_service](../modules/session_service.md), [task_detail](../modules/task_detail.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_task_brief.TaskBrief`
2. `schemas_task_brief.BriefCriterion`
3. `schemas_task.TaskResponse`
4. `task_detail.TaskReference`
5. `task_detail.TaskReferencePage`
6. `task_detail.TaskReferencePage`
7. `task_detail.TaskDetailResponse`
8. `schemas_task_domain.TaskActionsResponse`
9. `schemas_task_domain.TaskActionAvailability`
10. `schemas_task_domain.TaskActionAvailability`
11. `schemas_task.TaskStatusChangeResponse`
12. `schemas_task.CascadeUpdateInfo`
13. `schemas_task_brief.TaskReviewResponse`
14. `session_service._cookie_options`
15. `task_service.TaskVersionConflictError`

## Touches

- [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_task_brief](../modules/schemas_task_brief.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [session_service](../modules/session_service.md)
- [task_detail](../modules/task_detail.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `generate_mobile_contract_fixtures.build_examples`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
