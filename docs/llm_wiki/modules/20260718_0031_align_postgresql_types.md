# 20260718_0031_align_postgresql_types Module

**Path:** `backend/app/migrations/versions/20260718_0031_align_postgresql_types.py`

## Description

Align UTC timestamps, legacy nullability, and PostgreSQL sequences.

Revision ID: 20260718_0031
Revises: 20260718_0030
Create Date: 2026-07-18 00:31:00.000000

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `collections.abc` | `Sequence` |
| `sqlalchemy` | `sa` |
| `typing` | `Any` |

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
| `_align_nullability` | `(*, nullable: bool) -> None` | — | — |
| `_align_postgresql_timestamps` | `(*, timezone: bool) -> None` | — | — |
| `_repair_postgresql_sequences` | `() -> None` | — | — |
| `upgrade` | `() -> None` | — | — |
| `downgrade` | `() -> None` | — | — |
