# run_server_acceptance

**Entry point:** `server_acceptance.run_server_acceptance`
**Modules involved:** [autonomy_canonical](../modules/autonomy_canonical.md), [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md), [build_identity](../modules/build_identity.md), [loader](../modules/loader.md)

> Run the bounded self-hosted acceptance predicates and seal the report.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `build_identity.load_backend_build_identity`
2. `autonomy_canonical.sha256_hex`
3. `loader.load_postgresql_contract_bundle`
4. `autonomy_canonical.sha256_hex`
5. `autonomy_canonical.canonical_json_bytes`
6. `autonomy_canonical.canonical_json_bytes`
7. `autonomy_canonical.sha256_hex`

## Touches

- [autonomy_canonical](../modules/autonomy_canonical.md)
- [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md)
- [build_identity](../modules/build_identity.md)
- [loader](../modules/loader.md)

## Behavior

This workflow starts at `server_acceptance.run_server_acceptance`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
