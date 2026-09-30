# GitHub Actions: CI

**Path:** `.github/workflows/ci.yml`
**Type:** `github_actions`

## Triggers

- `pull_request`
- `push`
- `workflow_dispatch`

## Jobs

| Job | Display Name | Runs On | Needs | Steps |
|---|---|---|---|---:|
| `packaging` | `Packaging and contracts` | `ubuntu-24.04` | — | 15 |
| `backend` | `Backend (${{ matrix.scope }})` | `ubuntu-24.04` | — | 8 |
| `frontend` | `Frontend checks` | `ubuntu-24.04` | — | 6 |
| `clients` | `Browser and Android checks` | — | — | 0 |
| `build` | `Source and build checks` | `ubuntu-24.04` | `packaging`, `backend`, `frontend`, `clients` | 1 |

### packaging

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 - uses `actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238`
- Set up native PostgreSQL - uses `./.github/actions/native-postgres`
- Create the project environment - runs `python -m venv .venv`
- Install the backend - runs `.venv/bin/pip install --require-hashes -r backend/build-requirements.lock .venv/bin/pip install --require-hashes -r backend/requirements.lock .venv/bin/pip install --require-hashes -r backend/test-requirements.lock .venv/bin/pip install --no-build-isolation --no-deps -e ./backend`
- Validate native runtime helpers - runs `.venv/bin/python -m unittest discover -s scripts/ci/tests -v`
- Validate the backend wheel boundary - runs `wheel_dir="$(mktemp -d)" .venv/bin/pip wheel --no-build-isolation --no-deps --wheel-dir "$wheel_dir" ./backend .venv/bin/python - "$wheel_dir" backend/app/migrations <<'PY' from pathlib import Path from sys import argv from zipfile import ZipFile wheels = sorted(Path(argv[1]).glob("*.whl")) if len(wheels) != 1: raise SystemExit(f"Expected one backend wheel, found: {wheels}") with ZipFile(wheels[0]) as archive: members = set(archive.namelist()) required = { "app/__init__.py", "app/build_identity.py", "app/main.py", "app/mcp_server.py", "app/cli/worker.py", "app/cli/cutover.py", "app/cli/closeout.py", "app/cli/server_acceptance.py", "app/autonomy/server_acceptance.py", "app/database_migration/cutover.py", "app/database_migration/closeout.py", "app/database_migration/postgresql-cutover-execution-v1.schema.json", "app/database_migration/postgresql-postcutover-publication-input-v1.schema.json", "app/database_migration/postgresql-closeout-observations-v1.schema.json", "app/autonomy/contracts/postgresql/contract-manifest-v1.json", "app/autonomy/contracts/postgresql/autonomous-dag-v1.json", "app/autonomy/contracts/postgresql/status-rules-v1.json", "app/autonomy/contracts/postgresql/postgresql-capacity-contract-v1.json", "app/autonomy/contracts/postgresql/postgresql-data-lifecycle-policy-v1.json", "app/autonomy/contracts/postgresql/postgresql-load-result-v1.schema.json", "app/autonomy/contracts/postgresql/postgresql-precutover-qualification-v1.schema.json", "app/autonomy/contracts/postgresql/postgresql-resilience-observations-v1.schema.json", "app/config/scheduling_rules.yaml", } source_migrations = Path(argv[2]) required_migrations = { f"app/migrations/{path.relative_to(source_migrations).as_posix()}" for path in source_migrations.rglob("*") if path.is_file() and "__pycache__" not in path.parts } required.update(required_migrations) missing = sorted(required - members) if missing: raise SystemExit(f"Missing backend wheel members: {missing}") unexpected = sorted( name for name in members if ( name.startswith("alembic/") or name == "alembic.ini" or "__pycache__/" in name or name.endswith(".pyc") ) ) if unexpected: raise SystemExit( f"Top-level Alembic resources unexpectedly included: {unexpected}" ) PY wheel="$(find "$wheel_dir" -maxdepth 1 -name '*.whl' -print -quit)" installed_wheel_venv="$(mktemp -d)" python -m venv "$installed_wheel_venv" "$installed_wheel_venv/bin/pip" install --require-hashes -r backend/requirements.lock "$installed_wheel_venv/bin/pip" install --no-deps "$wheel" ( cd "$(mktemp -d)" export DATABASE_URL="sqlite+aiosqlite:///./workchord.db" "$installed_wheel_venv/bin/python" - <<'PY' from app.main import app from app.autonomy.contracts.postgresql import load_postgresql_contract_bundle from app.services.upgrade_service import head_revision, run_alembic_upgrade assert app.title == "WorkChord API" bundle = load_postgresql_contract_bundle() assert len(bundle.members) == 7 assert bundle.archive_verified is False assert bundle.blocker_codes == ("immutable-contract-archive-unavailable",) before, _, after = run_alembic_upgrade(backup=False, run_repairs=False) assert before.state == "empty" assert after.is_current assert after.current_revision == head_revision() PY "$installed_wheel_venv/bin/workchord-mcp" --help >/dev/null "$installed_wheel_venv/bin/workchord-worker" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-migrate" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-cutover" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-closeout" --help >/dev/null "$installed_wheel_venv/bin/workchord-agent-preflight" --help >/dev/null "$installed_wheel_venv/bin/workchord-server-acceptance" --help >/dev/null ) "$installed_wheel_venv/bin/python" \ scripts/ci/installed_wheel_postgresql_qualification.py \ --admin-url "$POSTGRES_ADMIN_URL"`
- Validate Python source and migrations - runs `PYTHONPYCACHEPREFIX=/tmp/workchord-pycache .venv/bin/python -m compileall -q backend/app scripts (cd backend && PYTHONPYCACHEPREFIX=/tmp/workchord-pycache ../.venv/bin/alembic -c app/migrations/alembic.ini heads) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=backend .venv/bin/python -c "from app.main import app; assert app.title == 'WorkChord API'; assert app.version == '1.7.0'" .venv/bin/python scripts/generate_client_contract.py --check .venv/bin/python scripts/generate_agent_team_contract.py --output /tmp/agent-team-master-v1.schema.json .venv/bin/python scripts/generate_agent_team_report_contract.py --output /tmp/agent-team-setup-report-v1.schema.json`
- Validate the PostgreSQL qualification harness contract - runs `qualification_dir="$(mktemp -d)" PYTHONPATH=backend .venv/bin/python scripts/load/seed.py \ --profile full \ --dry-run \ --manifest "$qualification_dir/full-seed-plan.json" for profile in human_peak_v1 mixed_peak_v1 connection_surge_v1 external_llm_wait_v1; do PYTHONPATH=backend .venv/bin/python scripts/load/run.py \ --profile "$profile" \ --phase dry \ --base-url http://127.0.0.1:8001 \ --authorize-host 127.0.0.1:8001 \ --environment test \ --output "$qualification_dir/$profile-dry.json" done cp -R "$qualification_dir" /tmp/workchord-qualification-contracts PYTHONPATH=backend .venv/bin/python \ scripts/ci/check_model_aware_routing_closeout.py \ --require-tracked \ --output /tmp/workchord-qualification-contracts/model-aware-routing-closeout.json`
- Validate PostgreSQL operator documentation - runs `.venv/bin/python scripts/ci/check_postgresql_documentation.py`
- workchord-qualification-contracts - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- Validate agent role packages - runs `.venv/bin/python scripts/build_agent_skills.py validate .venv/bin/python scripts/build_agent_skills.py build --output-dir /tmp/workchord-agent-skills .venv/bin/python scripts/build_agent_skills.py build-codex-plugin --output-dir /tmp/workchord-codex-plugin diff -ru adapters/codex/workchord-agent-roles /tmp/workchord-codex-plugin`
- Validate the local Compose profile - runs `docker compose config --quiet docker compose \ -f docker-compose.yml \ -f docker-compose.server.yml \ --profile autonomy \ config --quiet`
- Stop the job-owned PostgreSQL cluster - runs `>-`

### backend

- Reserve cleanup and artifact time - runs `python3 - <<'PYTHON' import os import time deadline = time.time() + int(os.environ["JOB_BUDGET_MINUTES"]) * 60 - 180 with open(os.environ["GITHUB_ENV"], "a") as output: output.write(f"WORKCHORD_CI_DEADLINE_EPOCH={deadline}\n") PYTHON`
- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- Set up native PostgreSQL - uses `./.github/actions/native-postgres`
- Install the backend - runs `python -m venv .venv .venv/bin/pip install --require-hashes -r backend/build-requirements.lock .venv/bin/pip install --require-hashes -r backend/requirements.lock .venv/bin/pip install --require-hashes -r backend/test-requirements.lock .venv/bin/pip install --no-build-isolation --no-deps -e ./backend`
- Run the selected database suite - runs `>-`
- backend-${{ matrix.scope }}-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- Stop the job-owned PostgreSQL cluster - runs `>-`

### frontend

- Reserve cleanup and artifact time - runs `python3 - <<'PYTHON' import os import time deadline = time.time() + int(os.environ["JOB_BUDGET_MINUTES"]) * 60 - 180 with open(os.environ["GITHUB_ENV"], "a") as output: output.write(f"WORKCHORD_CI_DEADLINE_EPOCH={deadline}\n") PYTHON`
- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 - uses `actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238`
- Run frontend checks - runs `>-`
- frontend-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

### clients


### build

- Require every check to finish successfully - runs `python3 - <<'PYTHON' import json import os results = json.loads(os.environ["CHECK_RESULTS"]) expected = {"packaging", "backend", "frontend", "clients"} if set(results) != expected: raise SystemExit("Required check inventory differs") failed = {name: value["result"] for name, value in results.items() if value["result"] != "success"} if failed: raise SystemExit(f"Required checks did not succeed: {failed}") print("All required checks completed successfully") PYTHON`

## Notes

Automatic PR/main CI runs dedicated SQLite/PostgreSQL scopes, a single frontend scope, packaging/contracts, and a reusable browser/Android workflow. Full backend and frontend workloads are not repeated inside browser jobs. Native PostgreSQL, pinned Python/Node versions and dependency caches remain in use. Static Compose configuration requires no image pulls; full deployment acceptance remains separately dispatched.

The final aggregate retains the Source and build checks status name and requires packaging, both database variants, frontend and the browser/Android workflow to succeed. Failed, cancelled, skipped or missing required dependency results cannot pass. Native runner jobs establish a deadline before setup, reserving three minutes for cleanup and artifact upload. Workflow definitions do not themselves establish hosted completion.
