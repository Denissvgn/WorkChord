# apt_runtime Module

**Path:** `scripts/ci/apt_runtime.py`

## Description

Prepare job-local APT sources for bounded signed package installation. The native PostgreSQL action and browser dependency installer run this helper before APT. It replaces the direct Azure Ubuntu archive URL or the hosted runner’s exact `mirror+file:/etc/apt/apt-mirrors.txt` reference in legacy and deb822 sources, selects the main HTTPS archive on AMD64 or Ubuntu Ports on ARM64, and preserves suites, components, signing keys and third-party sources. Persistent job-local APT configuration bounds HTTP/HTTPS inactivity to 15 seconds with two retries; update errors fail instead of silently accepting incomplete indexes.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `pathlib` | `Path` |
| `re` | `re` |
| `subprocess` | `subprocess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `prepare` | `(root: Path, architecture: str) -> None` | — | Replace the direct or mirror-list Ubuntu source; retain suites and signing. |
| `main` | `() -> None` | — | — |