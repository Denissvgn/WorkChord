# run_android_checks Module

**Path:** `scripts/ci/run_android_checks.py`

## Description

Builds the Android source in an isolated Linux amd64 JDK/SDK container using the checked-in, checksum-verified Gradle wrapper. It collects a debug APK and machine-readable execution results, records the source digest before and after execution, and removes the owned container. A build artifact does not establish device behavior or server integration.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `datetime` | `datetime`, `timezone` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `pathlib` | `Path` |
| `run_disposable_checks` | `ROOT`, `source_digest` |
| `subprocess` | `subprocess` |
| `tempfile` | `tempfile` |
| `uuid` | `uuid4` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `main` | `()` | — | — |
