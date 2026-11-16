# RuntimeObservationService_record

**Entry point:** `runtime_observation_service.RuntimeObservationService.record`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [models_runtime_observation](../modules/models_runtime_observation.md), [runtime_observation_service](../modules/runtime_observation_service.md), [time](../modules/time.md)

> Append one observation; repeating the same key and content returns the first row.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `authority.AuthorityError`
3. `time.utc_now`
4. `config.get_settings`
5. `authority.AuthorityError`
6. `models_runtime_observation.AgentRuntimeObservation`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [models_runtime_observation](../modules/models_runtime_observation.md)
- [runtime_observation_service](../modules/runtime_observation_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `runtime_observation_service.RuntimeObservationService.record`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
