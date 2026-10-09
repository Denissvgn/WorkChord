# WorkChord

[![CI (main)](https://github.com/Denissvgn/WorkChord/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/Denissvgn/WorkChord/actions/workflows/ci.yml)
[![Release status: unreleased](https://img.shields.io/badge/release-unreleased-yellow)](https://github.com/Denissvgn/WorkChord/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[![Python 3.11–3.13](https://img.shields.io/badge/Python-3.11%E2%80%933.13-3776AB?logo=python&logoColor=white)](backend/pyproject.toml)
[![Node.js 22.23.1](https://img.shields.io/badge/Node.js-22.23.1-5FA04E?logo=nodedotjs&logoColor=white)](.github/workflows/ci.yml)
[![FastAPI 0.139.0](https://img.shields.io/badge/FastAPI-0.139.0-009688?logo=fastapi&logoColor=white)](backend/requirements.lock)
[![SQLAlchemy 2.0.51](https://img.shields.io/badge/SQLAlchemy-2.0.51-D71F00?logo=sqlalchemy&logoColor=white)](backend/requirements.lock)
[![PostgreSQL 18](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)](docker-compose.yml)
[![React 19.2.3](https://img.shields.io/badge/React-19.2.3-149ECA?logo=react&logoColor=white)](frontend/package-lock.json)
[![Vite 7.3.6](https://img.shields.io/badge/Vite-7.3.6-646CFF?logo=vite&logoColor=white)](frontend/package-lock.json)

CI tracks `main`; versions reflect supported runtimes and locked dependencies.

WorkChord is a self-hosted workspace for human-led teams to capture, plan,
deliver, and review project work. External agents can participate through
authenticated REST and MCP APIs, using their own execution runtimes.

- **Teamwork:** project backlogs, task trees, ownership, discussion, and review with evidence.
- **Planning:** calendars, shared capacity, dependencies, and List, Board, Gantt, and roadmap views.
- **Recorded time:** optional private entries and scoped totals for project managers.

The web interface supports English and Russian. An [Android companion](android-companion/)
provides mobile task access.

## Get started

For a local PostgreSQL workspace, use Docker with Compose v2:

```bash
cp .env.example .env
```

Configure sign-in and application secrets in `.env` using the
[identity setup guide](docs/identity-and-recovery.md). Managed sign-in is the
default; an isolated workspace can explicitly select `trusted_local` mode.

```bash
docker compose up --build --detach
```

Open [localhost](http://localhost) (port 80 by default), then follow the identity
guide to establish the first owner.

For native Python/Node.js setup and local API documentation, follow
[local development](docs/local-development.md), which uses SQLite by default.
For a shared server, follow the deployment guides below.

## Documentation

| Topic | Guides |
| --- | --- |
| Working together | [Quickstart](docs/human-teamwork.md) · [Task semantics](docs/task-domain.md) · [Delivery analytics](docs/delivery-analytics.md) |
| Accounts and mobile access | [Sign-in, permissions, Android connection, and recovery](docs/identity-and-recovery.md) |
| Recorded time | [Enable time entry, privacy, reports, and exports](docs/time-entries.md) |
| External agents | [Runtime integration](docs/external-agent-runtime.md) · [Team setup](docs/agent-team-setup.md) · [Usage and pricing](docs/execution-usage.md) |
| Self-hosting | [Server setup](docs/runbooks/self-hosted-server-acceptance.md) · [PostgreSQL deployment](docs/runbooks/postgresql-deployment.md) |
| Operations | [Operator guide](docs/runbooks/postgresql-operations.md) · [Backup and restore](docs/runbooks/postgresql-backup-restore.md) · [Troubleshooting](docs/runbooks/postgresql-troubleshooting.md) |
| Configuration | [Environment settings](.env.example) |

## License

[MIT](LICENSE). See [third-party notices](THIRD_PARTY_NOTICES.md) for bundled components.
