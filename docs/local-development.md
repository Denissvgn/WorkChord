# Run WorkChord from source

Use Python 3.11–3.13 and Node.js 22 with npm. The commands below use Python 3.12
and start from the repository root.

A SQLite database needs SQLite 3.35 or later, as linked into Python's `sqlite3`
module. Check it with `python3 -c "import sqlite3; print(sqlite3.sqlite_version)"`.

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

### Install the wiki tool

The wiki in `docs/llm_wiki/` is maintained with llm-wiki 6.1.1: the
`agent-wiki-cli` package and its `llm-wiki-engine` dependency, both at 6.1.1.
Use that version for every command that writes the wiki. An older writer
rewrites records it does not understand, and a newer reader then refuses the
wiki and asks for a complete recovery.

6.1.1 is not yet on PyPI. Until it is, install it from the upstream source at
the commit that carries the 6.1.1 release:

```bash
git clone https://github.com/Denissvgn/python-wiki-llm.git <llm-wiki source>
git -C <llm-wiki source> checkout cbbf3ebbaf4e0b539fc7ceee8ec2d516280bf455
.venv/bin/pip install "<llm-wiki source>/src" "<llm-wiki source>"
.venv/bin/llm-wiki --version
```

The first path installs `llm-wiki-engine` and the second `agent-wiki-cli`; the
version check prints `llm-wiki 6.1.1`. Once
`.venv/bin/pip index versions agent-wiki-cli` lists 6.1.1, switch to the
published release:

```bash
.venv/bin/pip uninstall -y agent-wiki-cli llm-wiki-engine
.venv/bin/pip install "agent-wiki-cli==6.1.1"
```

Uninstall first: pip treats the source install as the same version and would
otherwise keep it. The published release carries the same code, so the wiki
needs no further change.

After installing or switching, refresh the managed agent instructions and
references, and prepare the TypeScript extractor helper (it needs Node.js):

```bash
.venv/bin/llm-wiki upgrade --src-dir . --wiki-dir docs/llm_wiki --agent generic --quality-hints --skills --issue-reporting
.venv/bin/llm-wiki prepare-extractors --src-dir .
```

### Run the writer from a normal checkout

Run every command that writes the wiki from a normal checkout, one whose
`.git` is a directory, for example a fresh `git clone`. Previews
(`sync --dry-run`), `lint` and `ci-check` can run anywhere.

Writers before 6.1.1 had two defects in linked worktrees, where `.git` is a
file. A sync there recorded the working tree as `dirty` even when it was clean
([python-wiki-llm#187](https://github.com/Denissvgn/python-wiki-llm/issues/187)),
so no later preview of the committed wiki reached a fixpoint. They also kept
their locks under the nearest `.git` directory, which for a nested worktree is
the enclosing repository. 6.1.1 fixes both: a sync in a clean linked worktree
records `clean`, a wiki committed with a `dirty` record is corrected by its
next sync, and locks stay in the worktree's own Git directory. The
full-reconstruction profile below has been qualified from a normal checkout
only, so keep the release refresh there. The workaround for an older writer is
the same normal checkout.

Before a writing run, confirm the checkout with the preflight:

```bash
.venv/bin/python scripts/ci/wiki_lock_root_preflight.py --checkout <checkout>
```

The preflight reads Git metadata only. It prints the lock root that a writer
before 6.1.1 would use and exits non-zero when that root is not the repository
the checkout belongs to. It passes in a normal checkout and refuses a nested
linked worktree. It does not open locks or run the writer.

When the preflight refuses, run the writer from a separate clone that has its
own `.git` directory and shares object storage with the repository:

```bash
git clone --shared <WorkChord repository> <isolated clone directory>
.venv/bin/python scripts/ci/wiki_lock_root_preflight.py --checkout <isolated clone directory>
```

Run the wiki commands from that clone once the preflight passes.

### Replay the wiki from a canonical checkout

A preview (`sync --dry-run`) never reads the extraction cache, while an
ordinary owning `sync` reads it. Before 6.1.1, a list built from a cached
mapping, for example the unresolved keyword settings recorded for a FastAPI
application, could come out in a different order in the two runs. The advisory
`llm-wiki/sync-analysis-v2.payload_hash` then differed and the owning run
rewrote packed objects that the preview did not report. 6.1.1 records the same
commitment in both runs.

Use one full-reconstruction profile for both the preview and the owning run.
It ignores the extraction cache and the reused analysis, so both runs build
their evidence from fresh extraction of identical inputs:

```bash
.venv/bin/python scripts/ci/wiki_lock_root_preflight.py --checkout <checkout>
llm-wiki sync --dry-run --rebuild-cache --rebuild-knowledge --jobs 1 --src-dir . --wiki-dir docs/llm_wiki
llm-wiki sync --rebuild-cache --rebuild-knowledge --jobs 1 --src-dir . --wiki-dir docs/llm_wiki
```

- Run the preflight first and stop if it refuses.
- Review the complete preview, then run the owning command with exactly the same
  arguments minus `--dry-run`. Add the same `--source-selection <profile>`,
  `--cache-dir` and `--helper-cache-dir` values to both commands when the
  repository uses them.
- Do not substitute `--no-cache`: it skips the analysis capture entirely, so the
  run does not produce the evidence commitment that the other modes compare. An ordinary
  `sync` (warm cache) remains valid for everyday maintenance, but do not compare
  its result with a preview.
- Run both commands from a normal checkout (see above). A fresh clone needs its
  own prepared extractor helper: run `llm-wiki prepare-extractors --src-dir .`
  once before the preview.
- Compare previews only in checkouts at the same absolute path as the one that
  ran the owning sync. In 6.1.1 the `llm-wiki/sync-analysis-v2` commitment
  includes the absolute source root, so a clone elsewhere reports a changed
  knowledge index and manifest (about 15 packed objects) although every
  source, page and concept matches. `lint --strict` and `ci-check` pass in
  either location.
- A full run takes roughly ten minutes. Afterwards, run the same preview again
  and confirm it reports no changes, then run `llm-wiki lint --strict --jobs 1`
  and `llm-wiki ci-check --format json --jobs 1` with the same source and wiki
  arguments, and confirm the ownership records are unchanged.
