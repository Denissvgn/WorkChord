# run_android_checks Module

**Path:** `scripts/ci/run_android_checks.py`

## Description

Builds a temporary Android source copy with native JDK 17, SDK 34 and the checksum-verified Gradle wrapper. The shared command runner records progress and deadlines before Gradle starts and collects available outputs after interruption. Both debug and release variants require successful executed result sets, and the debug APK must be nonempty. Artifact digests and source stability remain bound to the final receipt. A packaged artifact does not establish device or server integration.

The Android client requires HTTPS in release builds and limits debug HTTP to explicit loopback/emulator hosts. NetworkClient disables redirect forwarding and verbose release logging; sensitive headers are redacted and endpoint changes clear credentials. MyWorkViewModel obtains authenticated identity from /api/auth/me and selects loaded leaf work by its linked human owner profile, with no guest-session ownership inference. Its existing iteration selection scope remains unchanged. Kotlin/XML behavior is outside the static extractor coverage and requires direct client-source inspection.

An explicit paired release-qualification/input-manifest mode retains the ordinary debug baseline and confines release installation to a fresh owned ARM64 emulator with existing licensed tools. It builds an ephemeral qualification signing identity, binds APK/certificate/manifest identities, rejects missing or skipped required scenarios and cleans only matching installed artifacts. Shipping cleartext and trust resources remain unchanged. Source safety contracts do not establish compiled or live Android execution.

## Imports

| Source | Symbols |
|--------|---------|
| `android_qualification` | `load_inputs`, `Qualification` |
| `argparse` | `argparse` |
| `ci_runtime` | `RunReceipt`, `positive_seconds` |
| `hashlib` | `hashlib` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
| `run_disposable_checks` | `ROOT`, `source_digest`, `bind_source` |
| `shutil` | `shutil` |
| `tempfile` | `tempfile` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 3 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `main` | `()` | — | — |