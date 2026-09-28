# 20260916_0039_task_deletion_fences Module

**Path:** `backend/app/migrations/versions/20260916_0039_task_deletion_fences.py`

## Description

Retain deletion versions for safe task identity restoration.

Adds an independent deletion-fence table with a positive-version constraint. Historical deletions are left unknown. Downgrade requires restoring a complete backup with its matching application image because dropping the fence would invalidate recovery guarantees.

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