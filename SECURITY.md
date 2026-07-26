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

## Autonomous PostgreSQL execution boundary

The PostgreSQL autonomy package is fail closed. It validates externally signed
standing delegation, finite bootstrap slots, pinned public trust, immutable
evidence ancestry, exact-target action leases, and an external-CAS journal. The
autonomous path intentionally contains no private-key loader, local autonomous
signer, provider credential, release-publication adapter, or fallback that
converts an interactive approval into autonomous evidence. Legacy manual
evidence tools retain file-key support outside that mode, but reject file
private keys and file/embedded trust whenever
`WORKCHORD_EXECUTION_MODE=zero-human-agent-v1`.

Private resource identifiers and generations belong only in the restricted
class of the charter-selected immutable evidence store. They must not appear in
task prose, prompts, commits, ordinary logs, public projections, or generated
candidate notes. `reports/` is an untrusted cache and cannot establish a gate.

`workchord-agent-preflight` is an unsigned local diagnostic. Its output is never
accepted as autonomy or production evidence, and it exits nonzero while the
external charter, immutable archive, identities, remote KMS, WORM store,
provider adapters, and qualification reports are absent. Production execution
must also keep bootstrap and header-admin paths revoked and use only a current,
single-use, exact-target policy authorization.

The optional self-hosted server acceptance profile uses an internal-only
OpenBao dev server, a single-node MinIO object-lock bucket, and a single-node
Valkey AOF store. Their generated credentials live under ignored `.runtime/`
state, and their administrative ports are not published by the profile. Do not
expose those services or treat their receipt as production evidence. The
receipt schema fixes production authorization, production autonomy, and
production-gate satisfaction to `false` and keeps the program decision
`NO-SHIP`. OpenBao and MinIO administrative credentials are present only in
their service daemons and one-shot bootstrap jobs; they are withheld from the
acceptance container, which receives short-lived or bucket-scoped credentials.
The application listener defaults to loopback and requires a TLS reverse proxy
for remote access.

No WorkChord component has a release-publication destination or credential.
The immutable handoff renderer labels its output `NOT-PUBLISHED` and
`MANUAL-PUBLICATION-REQUIRED`; publication remains a separate manual process.
