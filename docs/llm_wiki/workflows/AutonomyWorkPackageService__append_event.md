# AutonomyWorkPackageService__append_event

**Entry point:** `autonomy_work_package_service.AutonomyWorkPackageService._append_event`
**Modules involved:** [autonomy_canonical](../modules/autonomy_canonical.md), [autonomy_work_package_service](../modules/autonomy_work_package_service.md), [models_autonomy](../modules/models_autonomy.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `models_autonomy.AgentVerificationEvent`
3. `autonomy_canonical.sha256_hex`

## Touches

- [autonomy_canonical](../modules/autonomy_canonical.md)
- [autonomy_work_package_service](../modules/autonomy_work_package_service.md)
- [models_autonomy](../modules/models_autonomy.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `autonomy_work_package_service.AutonomyWorkPackageService._append_event`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
