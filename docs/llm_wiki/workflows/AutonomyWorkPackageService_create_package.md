# AutonomyWorkPackageService_create_package

**Entry point:** `autonomy_work_package_service.AutonomyWorkPackageService.create_package`
**Modules involved:** [agent_service](../modules/agent_service.md), [autonomy_canonical](../modules/autonomy_canonical.md), [autonomy_work_package_service](../modules/autonomy_work_package_service.md), [commands](../modules/commands.md), [models_autonomy](../modules/models_autonomy.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentConflictError`
2. `agent_service.AgentConflictError`
3. `agent_service.AgentConflictError`
4. `agent_service.AgentConflictError`
5. `commands.command_transaction`
6. `task_service.TaskService`
7. `autonomy_canonical.sha256_hex`
8. `models_autonomy.AgentWorkPackage`
9. `models_autonomy.AgentVerificationRequirement`
10. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [autonomy_canonical](../modules/autonomy_canonical.md)
- [autonomy_work_package_service](../modules/autonomy_work_package_service.md)
- [commands](../modules/commands.md)
- [models_autonomy](../modules/models_autonomy.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `autonomy_work_package_service.AutonomyWorkPackageService.create_package`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
