# TaskBriefService_require_review

**Entry point:** `task_brief_service.TaskBriefService.require_review`
**Modules involved:** [authority](../modules/authority.md), [autonomy_canonical](../modules/autonomy_canonical.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_brief_service](../modules/task_brief_service.md)

> One independence and evidence boundary for human and assigned-agent review.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `authority.AuthorityError`
3. `authority.AuthorityError`
4. `delivery_dependency_service.DeliveryDependencyService`
5. `authority.AuthorityError`
6. `autonomy_canonical.sha256_hex`
7. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_brief_service](../modules/task_brief_service.md)

## Behavior

This workflow starts at `task_brief_service.TaskBriefService.require_review`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
