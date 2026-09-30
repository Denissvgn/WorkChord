# scripts/ci/Dockerfile.checks

**Path:** `scripts/ci/Dockerfile.checks`
**Base Image(s):** `python:3.12.13-slim-bookworm@sha256:8a7e7cc04fd3e2bd787f7f24e22d5d119aa590d429b50c95dfe12b3abe52f48b`

## Environment Variables

| Variable | Default |
|----------|---------|
| `WORKCHORD_AUTH_MODE` | `trusted_local` |
| `DEPLOYMENT_ENVIRONMENT` | `test` |
| `DATABASE_SSL_MODE` | `disable` |
| `PYTHONDONTWRITEBYTECODE` | `1` |
| `PYTHONPYCACHEPREFIX` | `/tmp/workchord-pycache` |

**Working Directory:** `/tmp/workchord`

## Entry Point

**CMD:** `["python", "--version"]`

## File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `backend/build-requirements.lock`, `backend/requirements.lock`, `backend/test-requirements.lock` | `./` | — |
| `COPY` | `backend` | `./backend` | — |

## Notes

This image installs the hash-locked backend toolchain. Execution runners mount current source read-only and place mutable application state inside disposable containers. The production build-context exclusions intentionally omit repository verification directories from this image; its default command only reports the Python version.
