# 20260928_0001_initial_schema Module

**Path:** `backend/app/migrations/versions/20260928_0001_initial_schema.py`

## Description

Create the complete initial WorkChord schema.

This revision is a frozen schema definition. Future changes belong in new
revisions; importing application model metadata here would change history.
Schema creation does not seed identities, settings, or other application rows.

The initial revision creates all 68 application tables without data backfills. It preserves UTC timestamp types, portable Boolean defaults, partial unique indexes, recovery history and deletion fences. SQLite retains task AUTOINCREMENT and inline references; PostgreSQL installs cyclic foreign keys after the referenced tables exist. Downgrade refuses destructive removal and directs recovery to a matching backup and application image.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
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
| `upgrade` | `()` | — | — |
| `downgrade` | `()` | — | — |