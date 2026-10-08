# main

**Entry point:** `server_acceptance.main`
**Modules involved:** [acceptance_artifacts](../modules/acceptance_artifacts.md), [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md), [build_identity](../modules/build_identity.md), [cli_server_acceptance](../modules/cli_server_acceptance.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `acceptance_artifacts.verify_exported_artifacts`
2. `build_identity.load_backend_build_identity`
3. `autonomy_server_acceptance.verify_receipt_trusted_signer`
4. `autonomy_server_acceptance.verify_receipt_current_build`
5. `build_identity.load_backend_build_identity`
6. `build_identity.load_backend_build_identity`
7. `autonomy_server_acceptance.ServerAcceptanceConfig`
8. `autonomy_server_acceptance.run_server_acceptance`
9. `autonomy_server_acceptance.ServerAcceptanceError`
10. `autonomy_server_acceptance.build_blocked_result`
11. `autonomy_server_acceptance.build_blocked_result`
12. `autonomy_server_acceptance.ServerAcceptanceError`
13. `autonomy_server_acceptance.build_blocked_result`

## Touches

- [acceptance_artifacts](../modules/acceptance_artifacts.md)
- [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md)
- [build_identity](../modules/build_identity.md)
- [cli_server_acceptance](../modules/cli_server_acceptance.md)

## Behavior

This workflow starts at `server_acceptance.main`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
