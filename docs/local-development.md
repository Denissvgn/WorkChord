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

On Apple Silicon, use the following command for the runtime dependency install.
macOS reports `arm64` for the architecture. This selects the `greenlet` wheel
that SQLAlchemy needs for async sessions, using the version and hashes in the lockfile.

```bash
sed "/^greenlet==/s/'aarch64'/'arm64'/" backend/requirements.lock |
  .venv/bin/pip install --require-hashes -r /dev/stdin
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
  in `backend/.env`. Settings are readable there; changing them still requires operator credentials.

Personal time recording requires human sign-in and `TIME_ENTRIES_ENABLED=true`;
see [recorded time](time-entries.md).

## Start

Initialize the schema, then run the data repairs that prepare the workspace.
Each command uses its own database role and a one-connection pool.

```bash
DATABASE_PROCESS_ROLE=migration DATABASE_POOL_SIZE=1 DATABASE_MAX_OVERFLOW=0 \
  ./scripts/upgrade_database.sh --no-repairs
DATABASE_PROCESS_ROLE=repair DATABASE_POOL_SIZE=1 DATABASE_MAX_OVERFLOW=0 \
  ./scripts/upgrade_database.sh --repairs-only
```

Start the backend and frontend in separate terminals, each from the repository root:

```bash
(cd backend && ../.venv/bin/uvicorn app.main:app --reload --port 8001)
```

```bash
npm --prefix frontend run dev -- --host localhost
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

The [container quickstart](../README.md#get-started) runs a local PostgreSQL
workspace. For shared deployments, use the
[server](runbooks/self-hosted-server-acceptance.md) and
[PostgreSQL](runbooks/postgresql-deployment.md) guides.

## Maintain the LLM wiki

The wiki writer keeps its storage and governance locks under the nearest
directory named `.git` above the checkout it runs from. A linked worktree
stores `.git` as a file, which the writer skips, so a worktree nested inside
another checkout can place those locks in the enclosing repository. Before
running the writer from a worktree, check where the locks would go:

```bash
.venv/bin/python scripts/ci/wiki_lock_root_preflight.py --checkout <checkout>
```

The preflight reads Git metadata only. It prints the effective lock root and
exits non-zero when that root is not the repository the checkout belongs to.
It does not open locks or run the writer.

When the preflight refuses, run the writer from an isolated clone that has its
own `.git` directory and shares object storage with the repository:

```bash
git clone --shared <WorkChord repository> <isolated clone directory>
.venv/bin/python scripts/ci/wiki_lock_root_preflight.py --checkout <isolated clone directory>
```

Run the wiki commands from the isolated clone once the preflight passes.
