# Dockerfile.backend

**Path:** `Dockerfile.backend`
**Base Image(s):** `${NODE_IMAGE}`, `${PYTHON_IMAGE}`, `${PYTHON_IMAGE}`

**Configuration view:** source declarations owned by each stage.

Image defaults, variable expansion, and Docker's inheritance/reset rules also affect effective configuration. External base-image defaults remain unknown here.

## Build Arguments

| Global argument (before FROM) | Default |
|----------|---------|
| `PYTHON_IMAGE` | `python:3.12.13-slim-bookworm@sha256:8a7e7cc04fd3e2bd787f7f24e22d5d119aa590d429b50c95dfe12b3abe52f48b` |
| `NODE_IMAGE` | `node:22.23.1-alpine3.23@sha256:8516dce0483394d5708d4b2ee6cacb79fb1d617ea4e2787c2120bcca92ce372e` |
| `WORKCHORD_VERSION` | `1.8.0` |
| `WORKCHORD_SOURCE_REVISION` | `unknown` |

## Build Stages

### Stage 1 `frontend-identity`

**FROM:** `${NODE_IMAGE}` (source line 8)

**Base relationship:** external or unresolved base; inherited defaults are unknown.

#### Build Arguments

| Argument | Default |
|----------|---------|
| `WORKCHORD_SOURCE_REVISION` | — |

**Declared WORKDIR:** `/frontend`

#### File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `frontend/package*.json` | `./` | — |
| `COPY` | `frontend` | `.` | — |
| `COPY` | [`scripts/build_frontend_image_identity.mjs`](../modules/build_frontend_image_identity.md) | `/tmp/build_frontend_image_identity.mjs` | — |

### Stage 2 `builder`

**FROM:** `${PYTHON_IMAGE}` (source line 24)

**Base relationship:** external or unresolved base; inherited defaults are unknown.

**Declared WORKDIR:** `/app`

#### File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `backend/build-requirements.lock`, `backend/requirements.lock` | `./` | — |
| `COPY` | `backend` | `/tmp/workchord-backend` | — |

### Stage 3

**FROM:** `${PYTHON_IMAGE}` (source line 57)

**Base relationship:** external or unresolved base; inherited defaults are unknown.

#### Build Arguments

| Argument | Default |
|----------|---------|
| `WORKCHORD_VERSION` | — |
| `WORKCHORD_SOURCE_REVISION` | — |

#### Environment Variables

| Variable | Default |
|----------|---------|
| `PATH` | `/root/.local/bin:$PATH` |
| `PYTHONUNBUFFERED` | `1` |
| `PYTHONDONTWRITEBYTECODE` | `1` |
| `WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR` | `/app/agent-skill-artifacts` |

**Declared WORKDIR:** `/app`

#### Entry Point

**CMD:** `["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]`

#### File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `/root/.local` | `/root/.local` | `builder` |
| `COPY` | `/tmp/workchord-frontend-build.json` | `/app/workchord-frontend-build.json` | `frontend-identity` |
| `COPY` | `agent-skills` | `/app/agent-skills` | — |
| `COPY` | [`scripts/build_agent_skills.py`](../modules/build_agent_skills.md) | `/app/scripts/build_agent_skills.py` | — |

#### Labels

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `WorkChord backend` |
| `org.opencontainers.image.version` | `${WORKCHORD_VERSION}` |
| `org.opencontainers.image.licenses` | `MIT` |
| `org.opencontainers.image.revision` | `${WORKCHORD_SOURCE_REVISION}` |

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
