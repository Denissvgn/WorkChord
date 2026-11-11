# choose_local_profile

**Entry point:** `identity.choose_local_profile`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md)

> Record which person profile a trusted-local session works as; local, not verified.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.AuthorityError`
3. `identity_service.local_work_profile`
4. `authority.AuthorityError`
5. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)

## Behavior

This workflow starts at `identity.choose_local_profile`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
