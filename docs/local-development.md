# Run WorkChord from source

Use Python 3.11–3.13 and Node.js 22 with npm. The commands below use Python 3.12
and start from the repository root.

## Install

```bash
python3.12 -m venv .venv
.venv/bin/pip install --require-hashes -r backend/build-requirements.lock
.venv/bin/pip install --require-hashes -r backend/requirements.lock
.venv/bin/pip install --no-build-isolation --no-deps -e ./backend
npm ci --prefix frontend
cp .env.example backend/.env
```

## Configure access

Edit `backend/.env`. Backend settings load `.env` from the process's working
directory; the commands below run the database initializer and API from
`backend/`. The default SQLite database is `backend/workchord.db`.

Generate local application secrets and copy the relevant values into `backend/.env`:

```bash
.venv/bin/python scripts/api_keys/generate_workchord_keys.py
```

Choose an access mode before starting:

- **Managed sign-in:** configure the OIDC provider and operator credentials as
  described in [identity setup](identity-and-recovery.md). For the frontend
  below, use the callback `http://localhost:5173/api/auth/callback`.
- **Isolated local workspace:** explicitly set `WORKCHORD_AUTH_MODE=trusted_local`
  in `backend/.env`. Operator settings still require operator credentials.

Personal time recording requires human sign-in and `TIME_ENTRIES_ENABLED=true`;
see [recorded time](time-entries.md).

## Start

Initialize the configured database:

```bash
./scripts/upgrade_database.sh
```

Start the backend and frontend in separate terminals, each from the repository root:

```bash
(cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8001)
```

```bash
npm --prefix frontend run dev
```

Open [localhost:5173](http://localhost:5173). The frontend proxies `/api` to the
backend on port 8001. Backend health and API documentation are available at
[localhost:8001/health](http://localhost:8001/health) and
[localhost:8001/docs](http://localhost:8001/docs).

For managed sign-in, establish the first owner through the
[identity guide](identity-and-recovery.md#establish-ownership-and-grant-access),
then follow the [teamwork quickstart](human-teamwork.md).

## Integrations and hosting

[External agent integration](external-agent-runtime.md) describes REST/MCP
credentials and runtime setup. Provide the provisioned actor's
`MCP_AGENT_API_KEY` in the process environment, then run local stdio MCP from
`backend/` so it uses the same database and settings as the API:

```bash
(cd backend && ../.venv/bin/workchord-mcp --transport stdio)
```

The container workspace uses PostgreSQL and reads the repository-root `.env`;
see [container setup](../README.md#get-started). For shared deployments, use the
[server](runbooks/self-hosted-server-acceptance.md) and
[PostgreSQL](runbooks/postgresql-deployment.md) guides.
