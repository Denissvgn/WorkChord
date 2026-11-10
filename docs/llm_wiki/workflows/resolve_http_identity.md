# resolve_http_identity

**Entry point:** `http_authority.resolve_http_identity`
**Modules involved:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [config](../modules/config.md), [http_authority](../modules/http_authority.md), [identity_service](../modules/identity_service.md), [security](../modules/security.md), [session_service](../modules/session_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `identity_service.IdentityService`
3. `authority.internal_authority`
4. `agent_service.AgentService.authenticate`
5. `agent_service.AgentService`
6. `authority.AuthorityError`
7. `authority.AuthorityError`
8. `authority.Authority`
9. `identity_service.IdentityService.actor_context`
10. `security.admin_api_key_is_valid`
11. `authority.AuthorityError`
12. `authority.AuthorityError`
13. `authority.AuthorityError`
14. `authority.Authority`
15. `session_service._get_session_by_token`
16. `identity_service.digest`
17. `authority.AuthorityError`
18. `authority.AuthorityError`
19. `session_service._get_session_by_token`
20. `authority.AuthorityError`
21. `authority.AuthorityError`
22. `identity_service.IdentityService.context`
23. `authority.AuthorityError`
24. `authority.AuthorityError`
25. `authority.Authority`

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
