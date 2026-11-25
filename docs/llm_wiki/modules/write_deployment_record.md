# write_deployment_record Module

**Path:** `scripts/server/write_deployment_record.py`

## Description

Write the deployment record of a self-hosted WorkChord instance.

The record names the exact images of every service, the source revision and
release version, the Compose project, the folder, the database volumes, the
time, the operator, and the deployment it replaces. It holds no secrets: paths
and identities only. A later scratch twin of the instance starts from it.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `datetime` | `datetime` |
| `getpass` | `getpass` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |
| `tempfile` | `tempfile` |
| `tomllib` | `tomllib` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `docker` | `(*args)` | — | — |
| `git` | `(folder, *args)` | — | — |
| `parse_json_lines` | `(text)` | — | Accept both a JSON array and one JSON object per line. |
| `image_identity` | `(reference)` | — | Return the immutable identity of one local image. |
| `container_service` | `(container)` | — | — |
| `compose_images` | `(project, compose_args)` | — | Images of the containers a Compose project holds, read from `docker compose images`. |
| `project_images` | `(project)` | — | Images of the containers of any Compose project, read with `docker inspect`. |
| `project_volumes` | `(project)` | — | — |
| `database_volumes` | `(project, names)` | — | — |
| `release_version` | `(folder)` | — | — |
| `source_identity` | `(folder)` | — | — |
| `replaced_deployment` | `(args, destination)` | — | Describe what this record replaces: an explicit project or file, else the prior record. |
| `build_record` | `(args, destination)` | — | — |
| `write_record` | `(record, destination)` | — | Write atomically and archive a record that already exists. |
| `parser` | `()` | — | — |
| `main` | `(argv = None)` | — | — |
