# get_or_create_session

**Entry point:** `session_service.get_or_create_session`
**Modules involved:** [config](../modules/config.md), [maintenance](../modules/maintenance.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

> Resolve an opaque token or create a fresh session without IP ownership.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `maintenance.MaintenanceModeError`
3. `time.utc_now`
4. `config.get_settings`
5. `time.as_utc`

## Touches

- [config](../modules/config.md)
- [maintenance](../modules/maintenance.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `session_service.get_or_create_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
