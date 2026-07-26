# Third-party notices

WorkChord is distributed under the MIT License. Third-party packages and base
images retain their own copyright and license terms.

The dependency inventories for this source tree are:

- `backend/requirements.lock` for the Python runtime.
- `frontend/package-lock.json` for the frontend build and runtime.
- `Dockerfile.backend` and `Dockerfile.frontend` for pinned container base images.
- `docker-compose.server.yml` for pinned optional server-service images.

The optional self-hosted server profile references these separately distributed
container images:

- OpenBao, licensed under MPL-2.0.
- MinIO Server and MinIO Client, licensed under AGPL-3.0.
- Valkey, licensed under BSD-3-Clause.

Those images are pulled from their publishers and are not vendored into the
WorkChord source tree.

This repository does not intentionally vendor third-party source code. Any
future vendored code, fonts, media, or other assets must add their source,
license, and required notice text here before publication.

Resolve license questions against the exact package version and source recorded
in these inventories rather than an unversioned package name.
