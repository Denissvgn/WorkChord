# run_post_migration_repairs

**Entry point:** `upgrade_service.run_post_migration_repairs`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [commands](../modules/commands.md), [github_status_automation_service](../modules/github_status_automation_service.md), [identity_service](../modules/identity_service.md), [label_service](../modules/label_service.md), [maintenance](../modules/maintenance.md), [saved_view_service](../modules/saved_view_service.md), [system_settings_service](../modules/system_settings_service.md), [template_service](../modules/template_service.md), [upgrade_service](../modules/upgrade_service.md)

> Run idempotent seeders and compatibility repairs after migrations.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `maintenance.require_background_writes_enabled`
2. `identity_service.initialize_control_plane`
3. `commands.commit_or_flush`
4. `calendar_service.CalendarService.get_or_create_default`
5. `calendar_service.CalendarService`
6. `template_service.TemplateService.seed_default_templates`
7. `template_service.TemplateService`
8. `label_service.LabelService.seed_default_labels`
9. `label_service.LabelService`
10. `saved_view_service.SavedViewService.seed_default_views`
11. `saved_view_service.SavedViewService`
12. `github_status_automation_service.GitHubStatusAutomationService.seed_default_rules`
13. `github_status_automation_service.GitHubStatusAutomationService`
14. `system_settings_service.RuntimeSettingsService.migrate_legacy_email_settings`
15. `system_settings_service.RuntimeSettingsService`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [github_status_automation_service](../modules/github_status_automation_service.md)
- [identity_service](../modules/identity_service.md)
- [label_service](../modules/label_service.md)
- [maintenance](../modules/maintenance.md)
- [saved_view_service](../modules/saved_view_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [template_service](../modules/template_service.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `upgrade_service.run_post_migration_repairs`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
