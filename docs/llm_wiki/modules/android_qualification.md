# android_qualification Module

**Path:** `scripts/ci/android_qualification.py`

## Description

Release-behavior qualification confined to an explicitly owned ARM64 emulator.

Qualification validates environment and emulator ownership before writes, requires nonce-marked strict HTTPS API/browser and synthetic issuer origins, verifies emulator system CA identity, and uses an isolated browser fixture. Exact APK hashes, generated certificate identity and same-identity rebuild equivalence gate installation. Required scenario inventory and executed status events must match without skips; controlled offline and web-peer stages precede independent readback. No production signer, physical-device claim or shipping trust exception is accepted.

Owned emulator controllers drain before resource cleanup. Device-scoped reverse mappings are checked by exact source/destination; acquisition refuses rebinding, replaced resources remain untouched, and independent cleanup failures are aggregated.

## Imports

| Source | Symbols |
|--------|---------|
| `base64` | `base64` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `platform` | `platform` |
| `re` | `re` |
| `secrets` | `secrets` |
| `ssl` | `ssl` |
| `subprocess` | `subprocess` |
| `threading` | `threading` |
| `time` | `time` |
| `urllib.parse` | `urlsplit` |
| `urllib.request` | `build_opener`, `HTTPSHandler`, `HTTPRedirectHandler` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [NoRedirect](../entities/NoRedirect.md) | 69 | `HTTPRedirectHandler` | — |
| [Qualification](../entities/Qualification.md) | 130 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `load_inputs` | `(path, expected_source, expected_revision)` | — | — |
| `fixture_probe` | `(data)` | — | — |
| `required_cases` | `(project)` | — | — |
| `executed_case` | `(output, classname, method)` | — | — |
| `manifest_flags` | `(text)` | — | — |