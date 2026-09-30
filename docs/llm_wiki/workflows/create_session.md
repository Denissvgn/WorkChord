# create_session

**Entry point:** `session_service._create_session`
**Modules involved:** [commands](../modules/commands.md), [config](../modules/config.md), [session_service](../modules/session_service.md), [time](../modules/time.md), [user_session](../modules/user_session.md)

> Create an isolated session, retrying the vanishingly rare unique collision.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `user_session.UserSession`
3. `time.utc_now`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [session_service](../modules/session_service.md)
- [time](../modules/time.md)
- [user_session](../modules/user_session.md)

## Behavior

This workflow starts at `session_service._create_session`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
