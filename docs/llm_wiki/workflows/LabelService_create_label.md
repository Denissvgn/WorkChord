# LabelService_create_label

**Entry point:** `label_service.LabelService.create_label`
**Modules involved:** [commands](../modules/commands.md), [label_service](../modules/label_service.md), [language_service](../modules/language_service.md), [models_label](../modules/models_label.md)

> Create a user-managed label.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `language_service.resolve_runtime_ui_language`
2. `language_service.entity_not_found_message`
3. `models_label.Label`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [label_service](../modules/label_service.md)
- [language_service](../modules/language_service.md)
- [models_label](../modules/models_label.md)

## Behavior

This workflow starts at `label_service.LabelService.create_label`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
