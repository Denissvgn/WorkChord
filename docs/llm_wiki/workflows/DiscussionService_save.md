# DiscussionService_save

**Entry point:** `discussion_service.DiscussionService.save`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [discussion_service](../modules/discussion_service.md), [models_discussion](../modules/models_discussion.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `commands.PlanningConflict`
3. `commands.PlanningConflict`
4. `models_discussion.TaskComment`
5. `models_discussion.TaskCommentRevision`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [discussion_service](../modules/discussion_service.md)
- [models_discussion](../modules/models_discussion.md)

## Behavior

Requires a durable human principal and task contribution authority. It locks and rechecks the task scope, validates structured mention targets, then writes the comment, retained revision and notification intents atomically. Task execution evidence and task/planning versions remain unchanged. Edits additionally require the current comment version.
