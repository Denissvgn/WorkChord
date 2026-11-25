# test_deployment_record Module

**Path:** `backend/tests/test_deployment_record.py`

## Description

The deployment record names every image, the source and the deployment it replaces.

## Imports

| Source | Symbols |
|--------|---------|
| `json` | `json` |
| `pytest` | `pytest` |
| `scripts.server` | `seed_adoption_env`, `write_deployment_record` |
| `stat` | `stat` |
| `subprocess` | `subprocess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 2 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_folder` | `(tmp_path)` | — | — |
| `_fake_docker` | `(images_rows, containers, volumes = ())` | — | Answer the read-only docker calls the script makes. |
| `_git` | `(folder, *args)` | — | — |
| `test_record_names_images_source_volumes_and_operator` | `(tmp_path, monkeypatch)` | — | — |
| `test_record_describes_the_replaced_project_and_archives_an_existing_record` | `(tmp_path, monkeypatch)` | — | — |
| `test_record_refuses_a_project_without_containers` | `(tmp_path, monkeypatch)` | — | — |
| `test_dirty_worktree_and_missing_tag_are_reported` | `(tmp_path, monkeypatch)` | — | — |
| `test_seed_copies_durable_values_generates_new_identities_and_never_overwrites` | `(tmp_path, capsys)` | — | — |
| `test_seed_refuses_incomplete_old_files_and_unknown_settings` | `(tmp_path)` | — | — |
