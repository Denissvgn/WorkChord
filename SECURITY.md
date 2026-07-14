# Security policy

## Supported versions

Security fixes target the newest published `1.x` release of WorkChord.

## Reporting a vulnerability

Use the repository's private **Security → Report a vulnerability** flow. Include
the affected version or commit, deployment mode, reproduction steps, impact,
and any proposed mitigation. Do not open a public issue or include live secrets.

Maintainers aim to acknowledge complete reports within seven calendar days,
triage impact, coordinate a fix, and agree on a disclosure window. If private
advisories are unavailable, ask a known maintainer privately for a secure
reporting channel before sharing exploit details.

## Operator responsibilities

- Terminate TLS at a trusted proxy and keep secure cookies enabled in production.
- Configure explicit MCP host and origin allowlists.
- Use separate, least-privilege actor keys and rotate exposed credentials.
- Protect `SETTINGS_ENCRYPTION_KEY`, databases, backups, and signing secrets.
- Keep private-network egress disabled unless a reviewed integration requires it.
- Never place secrets in task prose, logs, screenshots, or public issues.

Public agent-role bundles are fail-closed: enabling delivery requires the exact
trusted checksum in `AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256`.
