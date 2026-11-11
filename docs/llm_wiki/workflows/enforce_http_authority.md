# enforce_http_authority

**Entry point:** `http_authority.enforce_http_authority`
**Modules involved:** [authority](../modules/authority.md), [config](../modules/config.md), [http_authority](../modules/http_authority.md), [settings_read](../modules/settings_read.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `config.get_settings`
3. `authority.AuthorityError`
4. `authority.AuthorityError`
5. `authority.AuthorityError`
6. `authority.AuthorityError`
7. `authority.AuthorityError`
8. `authority.AuthorityError`
9. `authority.AuthorityError`
10. `authority.AuthorityError`
11. `authority.require_project`
12. `authority.AuthorityError`
13. `settings_read.settings_reader`
14. `authority.AuthorityError`
15. `authority.AuthorityError`

## Touches

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [settings_read](../modules/settings_read.md)

## Behavior

This workflow starts at `http_authority.enforce_http_authority`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
