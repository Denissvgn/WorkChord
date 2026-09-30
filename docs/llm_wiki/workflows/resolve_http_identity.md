# resolve_http_identity

**Entry point:** `http_authority.resolve_http_identity`
**Modules involved:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [config](../modules/config.md), [http_authority](../modules/http_authority.md), [identity_service](../modules/identity_service.md), [security](../modules/security.md), [session_service](../modules/session_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `identity_service.IdentityService`
3. `authority.internal_authority`
4. `agent_service.AgentService`
5. `authority.AuthorityError`
6. `authority.AuthorityError`
7. `authority.Authority`
8. `security.admin_api_key_is_valid`
9. `authority.AuthorityError`
10. `authority.AuthorityError`
11. `authority.AuthorityError`
12. `authority.Authority`
13. `session_service._get_session_by_token`
14. `identity_service.digest`
15. `authority.AuthorityError`
16. `authority.AuthorityError`
17. `session_service._get_session_by_token`
18. `authority.AuthorityError`
19. `authority.AuthorityError`
20. `authority.AuthorityError`
21. `authority.AuthorityError`
22. `authority.Authority`

## Touches

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
- [security](../modules/security.md)
- [session_service](../modules/session_service.md)

## Behavior

This workflow starts at `http_authority.resolve_http_identity`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
