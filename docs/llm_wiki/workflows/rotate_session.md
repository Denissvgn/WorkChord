# rotate_session

**Entry point:** `session_service.rotate_session`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [session_service](../modules/session_service.md), [time](../modules/time.md)

> Rotate a raw token while preserving ownership links on the session row.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `identity_service.require_identity_writes`
2. `time.as_utc`
3. `time.utc_now`
4. `authority.AuthorityError`
5. `time.utc_now`
6. `identity_service.session_lifetimes`
7. `identity_service.renewable_until`
8. `authority.AuthorityError`
9. `config.get_settings`
10. `commands.commit_or_flush`
11. `config.get_settings`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `session_service.rotate_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
