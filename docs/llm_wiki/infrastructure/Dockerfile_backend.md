# Dockerfile.backend

**Path:** `Dockerfile.backend`
**Base Image(s):** `${NODE_IMAGE}`, `${PYTHON_IMAGE}`, `${PYTHON_IMAGE}`

## Build Stages

| Stage | Base Image |
|-------|-----------|
| `frontend-identity` | `${NODE_IMAGE}` |
| `builder` | `${PYTHON_IMAGE}` |
| *(final)* | `${PYTHON_IMAGE}` |

## Build Arguments

| Argument | Default |
|----------|---------|
| `PYTHON_IMAGE` | `python:3.12.13-slim-bookworm@sha256:8a7e7cc04fd3e2bd787f7f24e22d5d119aa590d429b50c95dfe12b3abe52f48b` |
| `NODE_IMAGE` | `node:22.23.1-alpine3.23@sha256:8516dce0483394d5708d4b2ee6cacb79fb1d617ea4e2787c2120bcca92ce372e` |
| `WORKCHORD_VERSION` | `1.7.0` |
| `WORKCHORD_SOURCE_REVISION` | `unknown` |
| `WORKCHORD_SOURCE_REVISION` | — |
| `WORKCHORD_VERSION` | — |
| `WORKCHORD_SOURCE_REVISION` | — |

## Environment Variables

| Variable | Default |
|----------|---------|
| `PATH` | `/root/.local/bin:$PATH` |
| `PYTHONUNBUFFERED` | `1` |
| `PYTHONDONTWRITEBYTECODE` | `1` |
| `WORKCHORD_AGENT_SKILL_ARTIFACTS_DIR` | `/app/agent-skill-artifacts` |

**Working Directory:** `/app`

## Entry Point

**CMD:** `["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]`

## File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `frontend/package*.json` | `./` | — |
| `COPY` | `frontend` | `.` | — |
| `COPY` | `scripts/build_frontend_image_identity.mjs` | `/tmp/build_frontend_image_identity.mjs` | — |
| `COPY` | `backend/build-requirements.lock`, `backend/requirements.lock` | `./` | — |
| `COPY` | `backend` | `/tmp/workchord-backend` | — |
| `COPY` | `/root/.local` | `/root/.local` | `builder` |
| `COPY` | `/tmp/workchord-frontend-build.json` | `/app/workchord-frontend-build.json` | `frontend-identity` |
| `COPY` | `agent-skills` | `/app/agent-skills` | — |
| `COPY` | [`scripts/build_agent_skills.py`](../modules/build_agent_skills.md) | `/app/scripts/build_agent_skills.py` | — |

## Labels

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `WorkChord backend` |
| `org.opencontainers.image.version` | `${WORKCHORD_VERSION}` |
| `org.opencontainers.image.licenses` | `MIT` |
| `org.opencontainers.image.revision` | `${WORKCHORD_SOURCE_REVISION}` |

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
