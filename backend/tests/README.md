# Backend test harness

Fast tests use an isolated temporary SQLite database and block unapproved
network access:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=backend \
  .venv/bin/python -m pytest -q -m "not postgresql" backend/tests
```

PostgreSQL integration tests require a local PostgreSQL 18 server and create a
fresh `workchord_test_<uuid>` database for every test. The lifecycle refuses
non-test environments, non-local hosts, or a database without that exact name
shape. Every owned database is force-dropped in fixture cleanup.

```bash
DEPLOYMENT_ENVIRONMENT=test \
POSTGRES_ADMIN_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/postgres \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=backend \
  .venv/bin/python -m pytest -q -m postgresql backend/tests
```

Psycopg is a packaged runtime dependency. CI pins PostgreSQL 18.4 by digest,
runs both dialect lanes, and validates the installed wheel outside the source
tree, including the `workchord-mcp`, `workchord-worker`,
`workchord-db-migrate`, `workchord-db-cutover`, and
`workchord-db-closeout` entry points plus their packaged evidence schemas.
