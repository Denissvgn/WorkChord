# test_wal_archive_retention Module

**Path:** `backend/tests/database/test_wal_archive_retention.py`

## Description

WAL archive retention: segment selection and a point-in-time restore.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `os` | `os` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `shutil` | `shutil` |
| `subprocess` | `subprocess` |
| `time` | `time` |
| `uuid` | `uuid` |
| `yaml` | `yaml` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_segment` | `(number: int, timeline: int = 1) -> str` | — | — |
| `_make_backup` | `(root: Path, name: str, start_segment: str, *, verified: bool = True) -> Path` | — | — |
| `layout` | `(tmp_path: Path) -> dict[str, Path]` | `@pytest.fixture` | — |
| `_run` | `(layout: dict[str, Path], *arguments: str, **environment: str)` | — | — |
| `_names` | `(layout: dict[str, Path]) -> set[str]` | — | — |
| `test_nothing_is_deleted_without_a_verified_base_backup` | `(layout) -> None` | — | — |
| `test_missing_backup_directory_deletes_nothing` | `(layout) -> None` | — | — |
| `test_segments_needed_by_the_newest_backup_are_kept` | `(layout) -> None` | — | — |
| `test_keep_backups_extends_the_window_to_older_backups` | `(layout) -> None` | — | — |
| `test_dry_run_lists_without_deleting_and_rerun_is_idempotent` | `(layout) -> None` | — | — |
| `test_archive_that_lacks_the_start_segment_is_left_alone` | `(layout) -> None` | — | — |
| `test_failing_cleanup_is_reported_not_swallowed` | `(layout) -> None` | — | — |
| `test_invalid_keep_value_is_rejected` | `(layout) -> None` | — | — |
| `test_compose_runs_the_retention_loop_against_both_volumes` | `() -> None` | — | — |
| `_docker` | `(*arguments: str, check: bool = True, **kwargs)` | — | — |
| `test_point_in_time_restore_works_from_retained_backup_and_pruned_archive` | `() -> None` | `@pytest.mark.integration` | — |
