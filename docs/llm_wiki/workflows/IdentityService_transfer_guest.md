# IdentityService_transfer_guest

**Entry point:** `identity_service.IdentityService.transfer_guest`
**Modules involved:** [authority](../modules/authority.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `authority.require_operator`
3. `authority.AuthorityError`
4. `authority.AuthorityError`
5. `authority.internal_authority`
6. `authority.AuthorityError`
7. `authority.AuthorityError`
8. `time.as_utc`
9. `time.utc_now`
10. `authority.AuthorityError`
11. `authority.AuthorityError`
12. `models_identity.OwnershipTransfer`
13. `time.utc_now`
14. `models_identity.CommandAudit`

## Touches

- [authority](../modules/authority.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `identity_service.IdentityService.transfer_guest`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
