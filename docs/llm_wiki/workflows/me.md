# me

**Entry point:** `identity.me`
**Modules involved:** [config](../modules/config.md), [http_authority](../modules/http_authority.md), [identity_service](../modules/identity_service.md), [routers_identity](../modules/routers_identity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `http_authority.resolve_http_identity`
2. `config.get_settings`
3. `identity_service.local_work_profile`

## Touches

- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
- [routers_identity](../modules/routers_identity.md)

## Behavior

This workflow starts at `identity.me`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
