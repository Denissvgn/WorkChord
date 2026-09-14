# Dockerfile.frontend

**Path:** `Dockerfile.frontend`
**Base Image(s):** `${NODE_IMAGE}`, `${NGINX_IMAGE}`

## Build Stages

| Stage | Base Image |
|-------|-----------|
| `builder` | `${NODE_IMAGE}` |
| *(final)* | `${NGINX_IMAGE}` |

## Exposed Ports

- `80`

## Build Arguments

| Argument | Default |
|----------|---------|
| `NODE_IMAGE` | `node:22.23.1-alpine3.23@sha256:8516dce0483394d5708d4b2ee6cacb79fb1d617ea4e2787c2120bcca92ce372e` |
| `NGINX_IMAGE` | `nginx:1.28.3-alpine3.23@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236` |
| `WORKCHORD_VERSION` | `1.7.0` |
| `WORKCHORD_SOURCE_REVISION` | `unknown` |
| `WORKCHORD_SOURCE_REVISION` | — |
| `WORKCHORD_VERSION` | — |
| `WORKCHORD_SOURCE_REVISION` | — |

**Working Directory:** `/app`

## Entry Point

**CMD:** `["nginx", "-g", "daemon off;"]`

## File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `frontend/package*.json` | `./` | — |
| `COPY` | `frontend` | `.` | — |
| `COPY` | `scripts/build_frontend_image_identity.mjs` | `/tmp/build_frontend_image_identity.mjs` | — |
| `COPY` | `/app/dist` | `/usr/share/nginx/html` | `builder` |
| `COPY` | `/tmp/workchord-build.json` | `/usr/share/nginx/html/.well-known/workchord-build.json` | `builder` |
| `COPY` | `frontend/nginx.conf` | `/etc/nginx/conf.d/default.conf` | — |

## Labels

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `WorkChord frontend` |
| `org.opencontainers.image.version` | `${WORKCHORD_VERSION}` |
| `org.opencontainers.image.licenses` | `MIT` |
| `org.opencontainers.image.revision` | `${WORKCHORD_SOURCE_REVISION}` |

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
