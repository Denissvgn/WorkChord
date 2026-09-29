# source_phase

**Entry point:** `installed_wheel_postgresql_qualification._source_phase`
**Modules involved:** [database_migration_manifest](../modules/database_migration_manifest.md), [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md), [models_agent](../modules/models_agent.md), [models_calendar](../modules/models_calendar.md), [models_identity](../modules/models_identity.md), [models_iteration](../modules/models_iteration.md), [models_project](../modules/models_project.md), [models_task](../modules/models_task.md), [source](../modules/source.md), [upgrade_service](../modules/upgrade_service.md), [user_session](../modules/user_session.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `upgrade_service.bootstrap_database_schema`
2. `models_calendar.Calendar`
3. `models_project.Project`
4. `models_iteration.Iteration`
5. `models_task.Task`
6. `models_identity.Principal`
7. `models_identity.WorkspaceMembership`
8. `models_identity.ProjectMembership`
9. `models_agent.AgentActor`
10. `user_session.UserSession`
11. `database_migration_manifest.write_document`
12. `source.preflight_source`

## Touches

- [database_migration_manifest](../modules/database_migration_manifest.md)
- [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md)
- [models_agent](../modules/models_agent.md)
- [models_calendar](../modules/models_calendar.md)
- [models_identity](../modules/models_identity.md)
- [models_iteration](../modules/models_iteration.md)
- [models_project](../modules/models_project.md)
- [models_task](../modules/models_task.md)
- [source](../modules/source.md)
- [upgrade_service](../modules/upgrade_service.md)
- [user_session](../modules/user_session.md)

## Behavior

The installed package bootstraps an empty SQLite schema before adding representative planning records and identities. A human principal receives workspace membership and viewer access to the fixture project; the opaque session binds that principal with an expiry and CSRF value. These explicit fixture rows are distinct from schema creation, which seeds no application data. The source is then captured through the existing preflight and writer-drain evidence boundary.
