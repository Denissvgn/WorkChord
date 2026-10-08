# RunReceipt

**Location:** `scripts/ci/ci_runtime.py:109`
**Kind:** Class
**Bases:** —
**Module:** [ci_runtime](../modules/ci_runtime.md)

## Description

Owns command and service lifetimes, streamed logs, monotonic timings, atomic progress checkpoints and registered finalization callbacks. Commands run in separate process groups with bounded deadlines. A failed command remains a failure even when its caller continues to gather other results. Terminal outcomes distinguish failed, timed_out and cancelled from passed. A hard-killed owner may leave running state, which does not establish completion.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(output, *, checks, timeout_seconds, cleanup_grace = 3)` | — | — |
| `checkpoint` | `()` | — | — |
| `__enter__` | `()` | — | — |
| `_cancel` | `(signum, _frame)` | — | — |
| `check_budget` | `()` | — | — |
| `_interrupted_status` | `(error)` | — | — |
| `_command` | `(label, command, kind)` | — | — |
| `run` | `(label, command, *, cwd, env, timeout, check = True)` | — | — |
| `start` | `(label, command, *, cwd, env)` | — | — |
| `__exit__` | `(error_type, error, _traceback)` | — | — |
| `exit_code` | `()` | `@property` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [ci_runtime](../modules/ci_runtime.md) | 11 | — |
