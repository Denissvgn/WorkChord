# run_post_migration_repairs

**Entry point:** `upgrade_service.run_post_migration_repairs`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [github_status_automation_service](../modules/github_status_automation_service.md), [label_service](../modules/label_service.md), [maintenance](../modules/maintenance.md), [saved_view_service](../modules/saved_view_service.md), [system_settings_service](../modules/system_settings_service.md), [template_service](../modules/template_service.md), [upgrade_service](../modules/upgrade_service.md)

> Run idempotent seeders and compatibility repairs after migrations.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `maintenance.require_background_writes_enabled`
2. `calendar_service.CalendarService`
3. `template_service.TemplateService`
4. `label_service.LabelService`
5. `saved_view_service.SavedViewService`
6. `github_status_automation_service.GitHubStatusAutomationService`
7. `system_settings_service.RuntimeSettingsService`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [github_status_automation_service](../modules/github_status_automation_service.md)
- [label_service](../modules/label_service.md)
- [maintenance](../modules/maintenance.md)
- [saved_view_service](../modules/saved_view_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [template_service](../modules/template_service.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `upgrade_service.run_post_migration_repairs`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
