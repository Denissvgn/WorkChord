# AutonomyWorkPackageService_activate_requirements

**Entry point:** `autonomy_work_package_service.AutonomyWorkPackageService.activate_requirements`
**Modules involved:** [agent_service](../modules/agent_service.md), [autonomy_canonical](../modules/autonomy_canonical.md), [autonomy_work_package_service](../modules/autonomy_work_package_service.md), [commands](../modules/commands.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `autonomy_canonical.sha256_hex`
3. `agent_service.AgentConflictError`
4. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [autonomy_work_package_service](../modules/autonomy_work_package_service.md)
- [commands](../modules/commands.md)

## Behavior

This workflow starts at `autonomy_work_package_service.AutonomyWorkPackageService.activate_requirements`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
