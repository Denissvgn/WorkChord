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
| `build` | `Source and build checks` | `ubuntu-24.04` | — | 19 |

### build

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 - uses `actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238`
- Set up native PostgreSQL - uses `./.github/actions/native-postgres`
- Create the project environment - runs `python -m venv .venv`
- Install the backend - runs `.venv/bin/pip install --require-hashes -r backend/build-requirements.lock .venv/bin/pip install --require-hashes -r backend/requirements.lock .venv/bin/pip install --require-hashes -r backend/test-requirements.lock .venv/bin/pip install --no-build-isolation --no-deps -e ./backend`
- Validate native runtime helpers - runs `.venv/bin/python -m unittest discover -s scripts/ci/tests -v`
- Run the focused backend routing contracts - runs `>-`
- Run the backend database harness - runs `.venv/bin/python -m pytest -q \ -o cache_dir=/tmp/workchord-backend-pytest-cache \ -m "not postgresql" backend/tests .venv/bin/python -m pytest -q \ -o cache_dir=/tmp/workchord-backend-pytest-cache \ -m postgresql backend/tests test -s "$WORKCHORD_SCHEMA_DIFF_ARTIFACT"`
- workchord-schema-diff - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- Validate the backend wheel boundary - runs `wheel_dir="$(mktemp -d)" .venv/bin/pip wheel --no-build-isolation --no-deps --wheel-dir "$wheel_dir" ./backend .venv/bin/python - "$wheel_dir" backend/app/migrations <<'PY' from pathlib import Path from sys import argv from zipfile import ZipFile wheels = sorted(Path(argv[1]).glob("*.whl")) if len(wheels) != 1: raise SystemExit(f"Expected one backend wheel, found: {wheels}") with ZipFile(wheels[0]) as archive: members = set(archive.namelist()) required = { "app/__init__.py", "app/build_identity.py", "app/main.py", "app/mcp_server.py", "app/cli/worker.py", "app/cli/cutover.py", "app/cli/closeout.py", "app/cli/server_acceptance.py", "app/autonomy/server_acceptance.py", "app/database_migration/cutover.py", "app/database_migration/closeout.py", "app/database_migration/postgresql-cutover-execution-v1.schema.json", "app/database_migration/postgresql-postcutover-publication-input-v1.schema.json", "app/database_migration/postgresql-closeout-observations-v1.schema.json", "app/autonomy/contracts/postgresql/contract-manifest-v1.json", "app/autonomy/contracts/postgresql/autonomous-dag-v1.json", "app/autonomy/contracts/postgresql/status-rules-v1.json", "app/autonomy/contracts/postgresql/postgresql-capacity-contract-v1.json", "app/autonomy/contracts/postgresql/postgresql-data-lifecycle-policy-v1.json", "app/autonomy/contracts/postgresql/postgresql-load-result-v1.schema.json", "app/autonomy/contracts/postgresql/postgresql-precutover-qualification-v1.schema.json", "app/autonomy/contracts/postgresql/postgresql-resilience-observations-v1.schema.json", "app/config/scheduling_rules.yaml", } source_migrations = Path(argv[2]) required_migrations = { f"app/migrations/{path.relative_to(source_migrations).as_posix()}" for path in source_migrations.rglob("*") if path.is_file() and "__pycache__" not in path.parts } required.update(required_migrations) missing = sorted(required - members) if missing: raise SystemExit(f"Missing backend wheel members: {missing}") unexpected = sorted( name for name in members if ( name.startswith("alembic/") or name == "alembic.ini" or "__pycache__/" in name or name.endswith(".pyc") ) ) if unexpected: raise SystemExit( f"Top-level Alembic resources unexpectedly included: {unexpected}" ) PY wheel="$(find "$wheel_dir" -maxdepth 1 -name '*.whl' -print -quit)" installed_wheel_venv="$(mktemp -d)" python -m venv "$installed_wheel_venv" "$installed_wheel_venv/bin/pip" install --require-hashes -r backend/requirements.lock "$installed_wheel_venv/bin/pip" install --no-deps "$wheel" ( cd "$(mktemp -d)" export DATABASE_URL="sqlite+aiosqlite:///./workchord.db" "$installed_wheel_venv/bin/python" - <<'PY' from app.main import app from app.autonomy.contracts.postgresql import load_postgresql_contract_bundle from app.services.upgrade_service import head_revision, run_alembic_upgrade assert app.title == "WorkChord API" bundle = load_postgresql_contract_bundle() assert len(bundle.members) == 7 assert bundle.archive_verified is False assert bundle.blocker_codes == ("immutable-contract-archive-unavailable",) before, _, after = run_alembic_upgrade(backup=False, run_repairs=False) assert before.state == "empty" assert after.is_current assert after.current_revision == head_revision() PY "$installed_wheel_venv/bin/workchord-mcp" --help >/dev/null "$installed_wheel_venv/bin/workchord-worker" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-migrate" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-cutover" --help >/dev/null "$installed_wheel_venv/bin/workchord-db-closeout" --help >/dev/null "$installed_wheel_venv/bin/workchord-agent-preflight" --help >/dev/null "$installed_wheel_venv/bin/workchord-server-acceptance" --help >/dev/null ) "$installed_wheel_venv/bin/python" \ scripts/ci/installed_wheel_postgresql_qualification.py \ --admin-url "$POSTGRES_ADMIN_URL"`
- Validate Python source and migrations - runs `PYTHONPYCACHEPREFIX=/tmp/workchord-pycache .venv/bin/python -m compileall -q backend/app scripts (cd backend && PYTHONPYCACHEPREFIX=/tmp/workchord-pycache ../.venv/bin/alembic -c app/migrations/alembic.ini heads) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=backend .venv/bin/python -c "from app.main import app; assert app.title == 'WorkChord API'; assert app.version == '1.7.0'" .venv/bin/python scripts/generate_agent_team_contract.py --output /tmp/agent-team-master-v1.schema.json .venv/bin/python scripts/generate_agent_team_report_contract.py --output /tmp/agent-team-setup-report-v1.schema.json`
- Validate the PostgreSQL qualification harness contract - runs `qualification_dir="$(mktemp -d)" PYTHONPATH=backend .venv/bin/python scripts/load/seed.py \ --profile full \ --dry-run \ --manifest "$qualification_dir/full-seed-plan.json" for profile in human_peak_v1 mixed_peak_v1 connection_surge_v1 external_llm_wait_v1; do PYTHONPATH=backend .venv/bin/python scripts/load/run.py \ --profile "$profile" \ --phase dry \ --base-url http://127.0.0.1:8001 \ --authorize-host 127.0.0.1:8001 \ --environment test \ --output "$qualification_dir/$profile-dry.json" done cp -R "$qualification_dir" /tmp/workchord-qualification-contracts PYTHONPATH=backend .venv/bin/python \ scripts/ci/check_model_aware_routing_closeout.py \ --require-tracked \ --output /tmp/workchord-qualification-contracts/model-aware-routing-closeout.json`
- Validate PostgreSQL operator documentation - runs `.venv/bin/python scripts/ci/check_postgresql_documentation.py`
- workchord-qualification-contracts - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- Validate agent role packages - runs `.venv/bin/python scripts/build_agent_skills.py validate .venv/bin/python scripts/build_agent_skills.py build --output-dir /tmp/workchord-agent-skills .venv/bin/python scripts/build_agent_skills.py build-codex-plugin --output-dir /tmp/workchord-codex-plugin diff -ru adapters/codex/workchord-agent-roles /tmp/workchord-codex-plugin`
- Install and validate the frontend - runs `npm ci npm run test:run npm run lint npm run build`
- Validate the local Compose profile - runs `docker compose config --quiet docker compose \ -f docker-compose.yml \ -f docker-compose.server.yml \ --profile autonomy \ config --quiet`
- Stop the job-owned PostgreSQL cluster - runs `>-`

## Notes

Automatic PR/main checks install native PostgreSQL 18 from signed distribution packages and use a job-owned loopback cluster. Python and Node setup remain pinned. Compose configuration is parsed locally without pulling or building images. Full Compose deployment acceptance is separately dispatched, while database, packaging, contract and frontend checks remain in the automatic workflow.
