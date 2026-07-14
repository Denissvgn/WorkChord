# WorkChord

WorkChord is a self-hosted planning and delivery workspace for human teams and
agent-assisted execution. It brings projects, iterations, triage, task trees,
capacity, Gantt and roadmap views, release planning, audit history, REST APIs,
and authenticated MCP workflows into one application.

## Included components

- A FastAPI and SQLAlchemy backend with SQLite storage and Alembic migrations.
- A React and Vite frontend with English and Russian interfaces.
- Docker Compose profiles for local and production-style deployments.
- Portable WorkChord planner and worker role packages for agent integrations.

## Requirements

- Python 3.11, 3.12, or 3.13
- Node.js 22 and npm
- Docker with Compose v2, if you prefer containers

## Local setup

Create the project environment and install the application dependencies:

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ./backend
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

For a local container deployment:

```bash
cp .env.example .env
docker compose up --build
```

The backend data is stored in the `workchord_data` volume. Back up that volume
before upgrades. `docker-compose.prod.yml` is the hardened deployment profile;
it requires exact image references, HTTPS origins, host allowlists, proxy trust,
and production secrets supplied through the environment.

## Configuration

`.env.example` lists supported environment settings. At minimum, use a strong
`SETTINGS_ENCRYPTION_KEY` before saving runtime credentials. Keep `.env`, API
keys, database files, and certificates outside version control.

The protected control plane uses `WORKCHORD_ADMIN_API_KEY`. Agent provisioning
uses `AGENT_BOOTSTRAP_API_KEY`; normal MCP actors should receive separate,
least-privilege credentials.

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
