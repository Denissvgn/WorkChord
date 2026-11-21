# TaskBriefService_require_review

**Entry point:** `task_brief_service.TaskBriefService.require_review`
**Modules involved:** [authority](../modules/authority.md), [autonomy_canonical](../modules/autonomy_canonical.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [review_provenance](../modules/review_provenance.md), [task_brief_service](../modules/task_brief_service.md)

> One independence and evidence boundary for human and assigned-agent review.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `review_provenance.different_publisher_required`
3. `commands.current_command`
4. `authority.AuthorityError`
5. `authority.AuthorityError`
6. `authority.AuthorityError`
7. `delivery_dependency_service.DeliveryDependencyService.ready`
8. `delivery_dependency_service.DeliveryDependencyService`
9. `authority.AuthorityError`
10. `autonomy_canonical.sha256_hex`
11. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [review_provenance](../modules/review_provenance.md)
- [task_brief_service](../modules/task_brief_service.md)

## Behavior

This workflow starts at `task_brief_service.TaskBriefService.require_review`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
