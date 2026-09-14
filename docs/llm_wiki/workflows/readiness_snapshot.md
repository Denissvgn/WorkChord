# readiness_snapshot

**Entry point:** `observability.readiness_snapshot`
**Modules involved:** [app_database](../modules/app_database.md), [config](../modules/config.md), [maintenance](../modules/maintenance.md), [observability](../modules/observability.md), [upgrade_service](../modules/upgrade_service.md)

> Check connectivity, a short query, schema head, and drain evidence.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `upgrade_service.head_revision`
3. `app_database.database_runtime_summary`
4. `maintenance.maintenance_state`
5. `maintenance.maintenance_state`
6. `app_database.database_runtime_summary`

## Touches

- [app_database](../modules/app_database.md)
- [config](../modules/config.md)
- [maintenance](../modules/maintenance.md)
- [observability](../modules/observability.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `observability.readiness_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
