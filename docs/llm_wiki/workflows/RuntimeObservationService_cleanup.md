# RuntimeObservationService_cleanup

**Entry point:** `runtime_observation_service.RuntimeObservationService.cleanup`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [runtime_observation_service](../modules/runtime_observation_service.md), [time](../modules/time.md)

> Remove a bounded batch of observations older than the retention period.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_operator`
2. `config.get_settings`
3. `time.utc_now`
4. `authority.internal_authority`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [runtime_observation_service](../modules/runtime_observation_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `runtime_observation_service.RuntimeObservationService.cleanup`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
