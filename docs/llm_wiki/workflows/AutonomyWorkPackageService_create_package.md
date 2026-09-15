# AutonomyWorkPackageService_create_package

**Entry point:** `autonomy_work_package_service.AutonomyWorkPackageService.create_package`
**Modules involved:** [agent_service](../modules/agent_service.md), [autonomy_work_package_service](../modules/autonomy_work_package_service.md), [commands](../modules/commands.md), [models_autonomy](../modules/models_autonomy.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentConflictError`
2. `agent_service.AgentConflictError`
3. `agent_service.AgentConflictError`
4. `agent_service.AgentConflictError`
5. `models_autonomy.AgentWorkPackage`
6. `models_autonomy.AgentVerificationRequirement`
7. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [autonomy_work_package_service](../modules/autonomy_work_package_service.md)
- [commands](../modules/commands.md)
- [models_autonomy](../modules/models_autonomy.md)

## Behavior

This workflow starts at `autonomy_work_package_service.AutonomyWorkPackageService.create_package`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
