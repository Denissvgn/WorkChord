# 20260515_0024_move_portfolio_ownership_to_profiles Module

**Path:** `backend/app/migrations/versions/20260515_0024_move_portfolio_ownership_to_profiles.py`

## Description

Move portfolio ownership to team member profiles.

Revision ID: 20260515_0024
Revises: 20260510_0023
Create Date: 2026-05-15

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `collections.abc` | `Iterable`, `Sequence` |
| `datetime` | `datetime` |
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
| `_normalize_text_key` | `(value: str \| None) -> str` | — | — |
| `_find_profile_id` | `(connection, *, email: str \| None, name: str \| None) -> int \| None` | — | — |
| `_create_profile_for_member` | `(connection, member: dict) -> int` | — | — |
| `_resolve_profile_id` | `(connection, member: dict) -> int` | — | — |
| `_backfill_owner_profiles` | `(connection, *, table_name: str, rows: Iterable[dict]) -> None` | — | — |
| `upgrade` | `() -> None` | — | — |
| `downgrade` | `() -> None` | — | — |
