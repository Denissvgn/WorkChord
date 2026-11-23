# issuer_identity

**Entry point:** `review_evidence._issuer_identity`
**Modules involved:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [services_review_evidence](../modules/services_review_evidence.md)

> Read the issuing principal's current authority and attributable identities inside the server.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.current_command`
2. `authority.internal_authority`
3. `config.get_settings`
4. `agent_service.actor_has_scope`

## Touches

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [services_review_evidence](../modules/services_review_evidence.md)

## Behavior

This workflow starts at `review_evidence._issuer_identity`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
