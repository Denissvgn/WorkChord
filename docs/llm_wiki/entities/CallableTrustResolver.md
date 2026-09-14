# CallableTrustResolver

**Location:** `backend/app/autonomy/signing.py:154`
**Kind:** Class
**Bases:** —
**Module:** [signing](../modules/signing.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Small adapter for provider SDK integrations and deterministic tests.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `callback` | `Callable[[str, str], PublicTrustAnchor]` | *required* | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `resolve` | `(*, key_ref: str, key_version: str) -> PublicTrustAnchor` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [signing](../modules/signing.md) | 1 | `callback` |
