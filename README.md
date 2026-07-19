# WorkChord

WorkChord is a self-hosted planning and delivery workspace for human teams and
agent-assisted execution. It brings projects, iterations, triage, task trees,
capacity, Gantt and roadmap views, release planning, audit history, REST APIs,
and authenticated MCP workflows into one application.

## Included components

- A FastAPI and SQLAlchemy backend with PostgreSQL integration storage,
  Alembic migrations, and an explicit SQLite development/migration-source
  compatibility path.
- A React and Vite frontend with English and Russian interfaces.
- Docker Compose profiles for local and production-style deployments.
- Portable WorkChord planner and worker role packages for agent integrations.

## Requirements

- Python 3.11, 3.12, or 3.13
- Node.js 22 and npm
- Docker with Compose v2, if you prefer containers

## Local setup

Create the project environment and install the locked build and application
dependencies:

```bash
python3.12 -m venv .venv
.venv/bin/pip install --require-hashes -r backend/build-requirements.lock
.venv/bin/pip install --require-hashes -r backend/requirements.lock
.venv/bin/pip install --no-build-isolation --no-deps -e ./backend
npm ci --prefix frontend
cp .env.example .env
```

Generate strong local secrets and copy the values you need into `.env`:

```bash
.venv/bin/python scripts/api_keys/generate_workchord_keys.py
```

Prepare the database, then start the backend and frontend in separate
terminals:

```bash
./scripts/upgrade_database.sh
(cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8001)
npm --prefix frontend run dev
```

Open `http://localhost:5173`. The API health endpoint is
`http://localhost:8001/health`, and interactive API documentation is available
at `http://localhost:8001/docs`.

The MCP command is installed with the backend package:

```bash
.venv/bin/workchord-mcp --help
```

## Docker

For a clean local PostgreSQL container deployment:

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build --detach
docker compose ps
```

The integration stack runs PostgreSQL 18 and stores its cluster, WAL archive,
and backup artifacts in separate major-version-aware volumes. Do not copy a
live database volume. Use the checksummed logical/base backup jobs and prove an
isolated restore as described in the
[backup and restore runbook](docs/runbooks/postgresql-backup-restore.md).

`docker-compose.prod.yml` is the hardened PostgreSQL deployment profile. It
requires separate migration, runtime, and backup credentials; exact image
identities; verified database TLS; HTTPS origins; host allowlists; proxy trust;
and independently managed secrets. Start with the
[PostgreSQL operator and developer guide](docs/runbooks/postgresql-operations.md)
rather than adapting the local defaults for production.

## Configuration

`.env.example` lists supported environment settings. At minimum, use a strong
`SETTINGS_ENCRYPTION_KEY` before saving runtime credentials. Keep `.env`, API
keys, database files, and certificates outside version control.

The direct Python development default remains SQLite only for local work and
tests. PostgreSQL is the integration and production target, and production
fails closed when it is configured with SQLite. Database URL, pool, TLS,
process-role, migration, maintenance, and readiness policies are indexed in
the [database operations guide](docs/runbooks/postgresql-operations.md).

The protected control plane uses `WORKCHORD_ADMIN_API_KEY`. Agent provisioning
uses `AGENT_BOOTSTRAP_API_KEY`; normal MCP actors should receive separate,
least-privilege credentials.

## PostgreSQL migration and capacity

The pre-cutover runbook set is deliberately fail closed:

- [SQLite source migration](docs/runbooks/sqlite-to-postgresql-migration.md)
- [cutover, rollback, and stop conditions](docs/runbooks/sqlite-to-postgresql-cutover.md)
- [security and credential rotation](docs/runbooks/postgresql-security.md)
- [backup, PITR, and isolated restore](docs/runbooks/postgresql-backup-restore.md)
- [scale and resilience qualification](docs/runbooks/postgresql-qualification.md)
- [signed rehearsal and production-cutover evidence](docs/runbooks/postgresql-rehearsal-cutover-evidence.md)
- [post-cutover release publication and independent closeout](docs/runbooks/postgresql-postcutover-release-and-closeout.md)
- [troubleshooting](docs/runbooks/postgresql-troubleshooting.md)

Qualification can certify only **1,250 opaque browser identities, 250 active
browser sessions, and 200 concurrent MCP/agent clients** under the frozen
workload contract. Opaque identities are not authenticated people;
authentication, RBAC, and any people-based capacity claim are separate scope.
The repository's load tooling is not itself qualification evidence: three
complete, consecutive, independently reviewed production-shaped attempts are
required before migration rehearsal or production cutover.

This repository supports the production PostgreSQL path but does not by itself
assert that a particular deployment has cut over. Post-cutover release notes
and a final SHIP decision are generated only from the trusted production
evidence chain; missing production evidence remains NO-SHIP.

The autonomous migration control-plane foundation also installs a fail-closed
diagnostic:

```bash
workchord-agent-preflight
```

The current diagnostic deliberately accepts no external evidence and exits
`2`, listing the missing charter, immutable archive, identity/KMS/WORM,
adapter, and qualification predicates. Its JSON is explicitly unsigned and is
not a release or production authorization. See the
[autonomous execution preflight runbook](docs/runbooks/postgresql-autonomous-execution-preflight.md).

## Agent role packages

Canonical planner and worker roles live in `agent-skills/`. Validate or build
their deterministic archives with:

```bash
.venv/bin/python scripts/build_agent_skills.py validate
.venv/bin/python scripts/build_agent_skills.py build --output-dir dist/agent-skills
.venv/bin/python scripts/build_agent_skills.py build-codex-plugin \
  --output-dir adapters/codex/workchord-agent-roles
```

The tracked Codex adapter is generated from the canonical role folders. Rebuild
it after role changes; CI compares the committed tree with a clean generation.

Public bundle delivery is disabled by default. If enabled, pin the exact
official checksum with `AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256`.

## License

WorkChord is released under the [MIT License](LICENSE). Third-party components
remain subject to their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
