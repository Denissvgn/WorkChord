# convert_triage_item_to_backlog

**Entry point:** `triage.convert_triage_item_to_backlog`
**Modules involved:** [commands](../modules/commands.md), [routers_task_domain](../modules/routers_task_domain.md), [routers_triage](../modules/routers_triage.md), [schemas_triage](../modules/schemas_triage.md)

> Convert to a durable project task without scheduling it.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.command_transaction`
2. `routers_task_domain.domain_result`
3. `schemas_triage.TriageConvertToTaskResponse`

## Touches

- [commands](../modules/commands.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [routers_triage](../modules/routers_triage.md)
- [schemas_triage](../modules/schemas_triage.md)

## Behavior

This workflow starts at `triage.convert_triage_item_to_backlog`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
