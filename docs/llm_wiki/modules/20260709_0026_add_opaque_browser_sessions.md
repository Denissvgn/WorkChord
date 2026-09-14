# 20260709_0026_add_opaque_browser_sessions Module

**Path:** `backend/app/migrations/versions/20260709_0026_add_opaque_browser_sessions.py`

## Description

Replace IP ownership with opaque browser-session tokens.

Revision ID: 20260709_0026
Revises: 20260516_0025
Create Date: 2026-07-09 00:26:00.000000

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `collections.abc` | `Sequence` |
| `secrets` | `secrets` |
| `sqlalchemy` | `sa` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `upgrade` | `() -> None` | — | — |
| `downgrade` | `() -> None` | — | — |
