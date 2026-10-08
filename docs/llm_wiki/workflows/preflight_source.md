# preflight_source

**Entry point:** `source.preflight_source`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_manifest](../modules/database_migration_manifest.md), [project_identity](../modules/project_identity.md), [source](../modules/source.md)

> Create, validate, and manifest a stable SQLite migration snapshot.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `database_migration_manifest.read_document`
2. `project_identity.sqlite_project_allocation_floor`
3. `project_identity.sqlite_project_allocation_floor`
4. `catalog.catalog_entries`
5. `database_migration_manifest.sha256_bytes`
6. `database_migration_manifest.canonical_json_bytes`
7. `catalog.transfer_order`
8. `database_migration_manifest.write_document`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [project_identity](../modules/project_identity.md)
- [source](../modules/source.md)

## Behavior

This workflow starts at `source.preflight_source`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
