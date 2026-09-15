# AutonomyWorkPackageService_submit_requirement

**Entry point:** `autonomy_work_package_service.AutonomyWorkPackageService.submit_requirement`
**Modules involved:** [agent_service](../modules/agent_service.md), [autonomy_canonical](../modules/autonomy_canonical.md), [autonomy_work_package_service](../modules/autonomy_work_package_service.md), [commands](../modules/commands.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `autonomy_canonical.sha256_hex`
2. `agent_service.AgentConflictError`
3. `agent_service.AgentConflictError`
4. `time.utc_now`
5. `autonomy_canonical.sha256_hex`
6. `autonomy_canonical.sha256_hex`
7. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [autonomy_work_package_service](../modules/autonomy_work_package_service.md)
- [commands](../modules/commands.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `autonomy_work_package_service.AutonomyWorkPackageService.submit_requirement`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
