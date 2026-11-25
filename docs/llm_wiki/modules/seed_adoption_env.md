# seed_adoption_env Module

**Path:** `scripts/server/seed_adoption_env.py`

## Description

Seed the self-hosted server environment file from a running instance's file.

Adopting an existing database needs the same durable secrets the database and
the encrypted settings were created with. This script copies exactly those
(and a short list of operator settings) from the old environment file into a
new, private `server.env`, and generates fresh values for the identities that
the self-hosted layout adds. It never prints a value and never overwrites an
existing file. `accept_self_hosted.sh` then reads the file like any other
`server.env`.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
| `secrets` | `secrets` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `read_env` | `(path)` | — | — |
| `quote` | `(value)` | — | — |
| `build` | `(old, settings, http_port, postgres_port, bind, session_cookie_secure)` | — | — |
| `write` | `(path, values)` | — | — |
| `main` | `(argv = None)` | — | — |
