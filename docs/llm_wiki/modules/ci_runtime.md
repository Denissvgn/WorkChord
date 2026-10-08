# ci_runtime Module

**Path:** `scripts/ci/ci_runtime.py`

## Description

Shared native command execution with atomic progress receipts. Each command streams output to its log and the console, records timing and exit status, and receives the smaller of its command deadline and the remaining run budget. A workflow-supplied wall-clock deadline accounts for setup time before the Python process starts.

SIGINT and SIGTERM request cancellation through the normal control path. Owned process groups receive bounded termination and escalation, including descendants whose leader has exited. Linux zombies are recognized as already exited. Callers supply source binding, artifact requirements and temporary-workspace cleanup. Receipts start as running and become passed only after command outcomes, cleanup and registered validation complete; abrupt termination leaves an incomplete receipt.

Darwin permission-denied process-group probes are treated as absence only after a successful read-only inventory finds no executing members. A live denied group remains an error. Owned lifecycle deadlines, cancellation receipts and cleanup failures stay explicit.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `datetime`, `timezone` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `math` | `math` |
| `os` | `os` |
| `pathlib` | `Path` |
| `selectors` | `selectors` |
| `signal` | `signal` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `time` | `time` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CommandTimeout](../entities/CommandTimeout.md) | 28 | `RuntimeError` | — |
| [RunCancelled](../entities/RunCancelled.md) | 32 | `RuntimeError` | — |
| [RunReceipt](../entities/RunReceipt.md) | 109 | — | Own a bounded run; a killed process leaves a durable incomplete receipt. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `timestamp` | `()` | — | — |
| `positive_seconds` | `(value)` | — | — |
| `stop_process_group` | `(process, grace_seconds = 3)` | — | Terminate descendants as well as the leader, then reap the leader. |
| `junit_counts` | `(path)` | — | — |