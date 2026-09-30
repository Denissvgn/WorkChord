# run_android_checks Module

**Path:** `scripts/ci/run_android_checks.py`

## Description

Builds a temporary Android source copy with the configured native JDK 17, SDK 34 and checksum-verified Gradle wrapper. Both debug and release variants must produce successful executed result sets, and the debug APK must be nonempty. Receipts bind artifacts and source stability; a packaged artifact does not establish device or server integration.

The Android client requires HTTPS in release builds and limits debug HTTP to explicit loopback/emulator hosts. NetworkClient disables redirect forwarding and verbose release logging; sensitive headers are redacted and endpoint changes clear credentials. MyWorkViewModel obtains authenticated identity from /api/auth/me and selects loaded leaf work by its linked human owner profile, with no guest-session ownership inference. Its existing iteration selection scope remains unchanged. Kotlin/XML behavior is outside the static extractor coverage and requires direct client-source inspection.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `datetime` | `datetime`, `timezone` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
| `run_disposable_checks` | `ROOT`, `source_digest` |
| `shutil` | `shutil` |
| `subprocess` | `subprocess` |
| `tempfile` | `tempfile` |
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