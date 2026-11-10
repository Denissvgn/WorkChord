# AgentTeamSetupService___init__

**Entry point:** `agent_team_setup_service.AgentTeamSetupService.__init__`
**Modules involved:** [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md), [agent_team_credentials](../modules/agent_team_credentials.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [config](../modules/config.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `agent_team_credentials.FilesystemAgentTeamCredentialSink`
3. `agent_skill_bundle_service.AgentSkillBundleService`

## Touches

- [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md)
- [agent_team_credentials](../modules/agent_team_credentials.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [config](../modules/config.md)

## Behavior

Construction retains the caller's database session and supplied credential sink, or configures the filesystem sink from server settings. It uses an explicitly supplied bundle service when present and otherwise creates the default service for deployed role artifacts.

Release integrity is evaluated when compatibility checks request the catalog, rather than during construction. The catalog is a defensive typed copy of the validated release; unavailable or invalid artifacts become the stable `agent_team_skill_catalog_unavailable` conflict.
