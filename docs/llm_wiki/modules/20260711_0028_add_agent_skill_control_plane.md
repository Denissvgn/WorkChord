# 20260711_0028_add_agent_skill_control_plane Module

**Path:** `backend/app/migrations/versions/20260711_0028_add_agent_skill_control_plane.py`

## Description

Add actor assignments, fenced work, and durable idempotency.

Revision ID: 20260711_0028
Revises: 20260709_0027
Create Date: 2026-07-11 00:00:00.000000

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `collections.abc` | `Sequence` |
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
| `_columns` | `(table_name: str) -> set[str]` | — | — |
| `upgrade` | `() -> None` | — | — |
| `downgrade` | `() -> None` | — | — |
