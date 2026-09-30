# WorkChord

WorkChord is a self-hosted workspace for planning and delivering team work.
Organize projects and task trees, assign owners, plan capacity, and follow work
through execution and review. Gantt, board, and roadmap views share the same
tasks. Agent assistance is optional through REST and authenticated MCP APIs.

Built with FastAPI, SQLAlchemy, React, and Vite. The web interface supports
English and Russian. PostgreSQL is the deployment database; SQLite is supported
for local development.

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

## Container setup

```bash
cp .env.example .env
# Configure secrets and sign-in settings in .env before starting.
docker compose up --build --detach
```

Managed sign-in is the default. Follow the [identity setup guide](docs/identity-and-recovery.md)
to configure your provider and establish the first owner. For an isolated local
workspace, that guide also describes the explicit trusted-local mode.

## Documentation

- **Using WorkChord:** [human teamwork quickstart](docs/human-teamwork.md) · [task and metric semantics](docs/task-domain.md)
- **Accounts and recovery:** [sign-in, permissions, sessions, and snapshots](docs/identity-and-recovery.md)
- **Configuration:** [environment settings](.env.example)
- **Self-hosting:** [server setup](docs/runbooks/self-hosted-server-acceptance.md) · [deployment topology](docs/runbooks/postgresql-deployment.md)
- **Database operations:** [operator guide and runbook index](docs/runbooks/postgresql-operations.md) · [backup and restore](docs/runbooks/postgresql-backup-restore.md) · [troubleshooting](docs/runbooks/postgresql-troubleshooting.md)
- **Agent integrations:** [team setup](docs/agent-team-setup.md) · [planner role](agent-skills/workchord-pm/SKILL.md) · [worker role](agent-skills/workchord-worker/SKILL.md) · [model routing](docs/runbooks/model-aware-routing.md)
- **API reference:** interactive documentation at `/docs` on your backend instance

## License

[MIT](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for bundled components.
