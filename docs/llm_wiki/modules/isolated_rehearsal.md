# isolated_rehearsal Module

**Path:** `scripts/server/isolated_rehearsal.py`

## Description

Own isolated Compose resources without reusing operator credentials or data.

Isolated Compose runs use a fresh private runtime directory, unique project and image prefix, and a native platform matching the Docker engine. Every resource carries a run owner label; operations reject unrelated resources, selected images are checked before launch, and cleanup removes only reobserved owned identities while retaining failure evidence.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
| `secrets` | `secrets` |
| `socket` | `socket` |
| `subprocess` | `subprocess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `docker` | `(*args)` | — | — |
| `resources` | `(project)` | — | — |
| `load_marker` | `(root)` | — | — |
| `verify` | `(root)` | — | — |
| `prepare` | `(root, project, platform)` | — | — |
| `ownership_override` | `(marker, definition)` | — | — |
| `verify_images` | `(marker, images)` | — | — |
| `cleanup` | `(root)` | — | — |
| `main` | `()` | — | — |
