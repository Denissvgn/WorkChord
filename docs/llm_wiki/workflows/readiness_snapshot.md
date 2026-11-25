# readiness_snapshot

**Entry point:** `observability.readiness_snapshot`
**Modules involved:** [app_database](../modules/app_database.md), [app_maintenance](../modules/app_maintenance.md), [config](../modules/config.md), [observability](../modules/observability.md), [upgrade_service](../modules/upgrade_service.md)

> Check connectivity, a short query, schema head, and drain evidence.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `upgrade_service.head_revision`
3. `app_database.database_runtime_summary`
4. `app_maintenance.maintenance_state`
5. `app_maintenance.maintenance_state`
6. `app_database.database_runtime_summary`

## Touches

- [app_database](../modules/app_database.md)
- [app_maintenance](../modules/app_maintenance.md)
- [config](../modules/config.md)
- [observability](../modules/observability.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `observability.readiness_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
