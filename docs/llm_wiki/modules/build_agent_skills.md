# build_agent_skills Module

**Path:** `scripts/build_agent_skills.py`

## Description

Generated submission tables include the optional typed `criterion_progress` packet alongside artifacts and version/fence fields. A complete schema-field parity assertion guards against the prose and generated table advertising different submission contracts.

Canonical role guidance requires stable criterion IDs and revisions for submission and independent review. Package identities and example manifest checksum pins must advance together; frozen published role and catalog identities remain append-only.

Validate and reproducibly package WorkChord role skills.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `binascii` | `binascii` |
| `contextlib` | `contextmanager` |
| `ctypes` | `ctypes` |
| `datetime` | `datetime`, `timezone` |
| `fcntl` | `fcntl` |
| `hashlib` | `hashlib` |
| `io` | `io` |
| `ipaddress` | `ipaddress` |
| `json` | `json` |
| `msvcrt` | `msvcrt` |
| `os` | `os` |
| `pathlib` | `Path`, `PurePosixPath` |
| `re` | `re` |
| `shutil` | `shutil` |
| `stat` | `stat` |
| `struct` | `struct` |
| `sys` | `sys` |
| `tarfile` | `tarfile` |
| `tempfile` | `tempfile` |
| `typing` | `Any`, `Iterable`, `Iterator` |
| `urllib.parse` | `unquote`, `urlsplit` |
| `zipfile` | `zipfile` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SkillPackError](../entities/SkillPackError.md) | 812 | `ValueError` | Raised when skill source, catalog, or archive validation fails. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_contract_parameters` | `(required: Iterable[str] = (), optional: Iterable[str] = ()) -> list[dict[str, Any]]` | — | Build an ordered, JSON-compatible operation-parameter declaration. |
| `_assigned_work_operation` | `(operation_id: str, audience: str, method: str, path: str, tool: str, summary: str, *, body_model: str \| None = None, body_required: Iterable[str] = (), body_optional: Iterable[str] = (), path_required: Iterable[str] = (), query_optional: Iterable[str] = (), header_required: Iterable[str] = (), header_optional: Iterable[str] = (), tool_required: Iterable[str] = (), tool_optional: Iterable[str] = (), required_feature: str \| None = None) -> dict[str, Any]` | — | Build one canonical REST/Pydantic/MCP operation declaration. |
| `_sha256` | `(data: bytes) -> str` | — | — |
| `_canonical_json` | `(value: Any) -> bytes` | — | — |
| `_validate_relative_path` | `(path: str, *, context: str) -> PurePosixPath` | — | — |
| `_validate_semver` | `(value: Any, *, field: str) -> str` | — | — |
| `_validate_compatibility` | `(value: Any) -> str` | — | — |
| `_collect_role_files` | `(role_dir: Path) -> dict[str, bytes]` | — | — |
| `_parse_frontmatter` | `(skill_bytes: bytes, *, folder_name: str) -> dict[str, str]` | — | — |
| `_local_markdown_targets` | `(text: str) -> Iterable[str]` | — | — |
| `_validate_references` | `(folder_name: str, files: dict[str, bytes]) -> None` | — | — |
| `_is_private_url` | `(raw_url: str) -> bool` | — | — |
| `_validate_content` | `(folder_name: str, files: dict[str, bytes]) -> None` | — | — |
| `validate_role_source` | `(role_dir: Path) -> dict[str, bytes]` | — | Validate one canonical role folder and return its ordered file bytes. |
| `_format_generated_parameters` | `(parameters: list[dict[str, Any]]) -> str` | — | — |
| `_format_generated_rest` | `(operation: dict[str, Any]) -> str` | — | — |
| `_format_generated_mcp` | `(operation: dict[str, Any]) -> str` | — | — |
| `render_assigned_work_contract_markdown` | `() -> str` | — | Render the canonical assigned-work contract as one reusable Markdown block. |
| `_generated_contract_block` | `(text: str, *, context: str) -> str` | — | — |
| `_replace_generated_contract_block` | `(text: str, *, context: str) -> str` | — | — |
| `render_openai_adapter` | `(role_dir: Path) -> bytes` | — | Derive deterministic optional UI metadata from one portable SKILL.md. |
| `sync_generated_skill_sources` | `(repository_root: Path = REPOSITORY_ROOT, skills_dir: Path = DEFAULT_SKILLS_DIR) -> list[Path]` | — | Synchronize shared references and optional adapters from canonical sources. |
| `validate_generated_skill_sources` | `(repository_root: Path = REPOSITORY_ROOT, skills_dir: Path = DEFAULT_SKILLS_DIR) -> None` | — | Fail when generated role/manual blocks or adapters drift from their sources. |
| `_zip_bytes` | `(folder_name: str, files: dict[str, bytes]) -> bytes` | — | — |
| `_deterministic_gzip` | `(data: bytes) -> bytes` | — | Return a gzip stream whose stored DEFLATE blocks do not depend on zlib. |
| `_tar_gz_bytes` | `(folder_name: str, files: dict[str, bytes]) -> bytes` | — | — |
| `_archive_records` | `(folder_name: str, version: str, files: dict[str, bytes]) -> tuple[list[dict[str, Any]], dict[str, bytes]]` | — | — |
| `generate_catalog` | `(skills_dir: Path) -> tuple[dict[str, Any], dict[str, bytes]]` | — | Generate the canonical catalog and reproducible role archive bytes. |
| `write_catalog` | `(skills_dir: Path) -> Path` | — | Regenerate catalog.json from validated canonical skill folders. |
| `_catalog_skill_files` | `(catalog: dict[str, Any], folder_name: str) -> dict[str, dict[str, Any]]` | — | — |
| `_catalog_entry_digest` | `(skill: dict[str, Any]) -> str` | — | Return the immutable content identity for one independently versioned role. |
| `_catalog_release_digest` | `(catalog: dict[str, Any]) -> str` | — | Return the immutable identity shared by one catalog and plugin version. |
| `_load_release_baseline` | `(skills_dir: Path) -> dict[str, Any] \| None` | — | Load and strictly validate the append-only published-version baseline. |
| `_validate_release_baseline` | `(skills_dir: Path, catalog: dict[str, Any], *, require_current: bool) -> None` | — | Prevent published role/version bytes from being changed in place. |
| `validate_catalog` | `(skills_dir: Path, *, require_frozen: bool = True) -> dict[str, Any]` | — | Validate catalog fields, file coverage, digests, and generated archive metadata. |
| `freeze_release` | `(skills_dir: Path) -> Path` | — | Append each current role/version identity to the immutable baseline. |
| `_expected_archive_members` | `(catalog: dict[str, Any], folder_name: str) -> dict[str, dict[str, Any]]` | — | — |
| `_validate_member_names` | `(names: Iterable[str], *, context: str) -> list[str]` | — | — |
| `_validated_archive_members` | `(archive_name: str, archive_bytes: bytes, catalog: dict[str, Any], folder_name: str) -> dict[str, bytes]` | — | Return validated regular-file members read from one in-memory snapshot. |
| `validate_archive` | `(archive_path: Path, catalog: dict[str, Any], folder_name: str) -> None` | — | Validate an exact role archive without extracting it. |
| `build_release` | `(skills_dir: Path, output_dir: Path) -> dict[str, Any]` | — | Build and validate deterministic role archives plus their checksum index. |
| `build_codex_plugin` | `(skills_dir: Path, output_dir: Path) -> Path` | — | Generate a Codex plugin adapter from the canonical validated role folders. |
| `_inspect_regular_tree` | `(root: Path) -> set[str]` | — | Return a tree inventory while rejecting links and special entries. |
| `_fsync_tree` | `(root: Path) -> None` | — | Flush staged regular files and directories before publication. |
| `_rename_exchange` | `(first: Path, second: Path) -> bool` | — | Atomically exchange two trees on Linux; return false when unavailable. |
| `_replace_built_tree` | `(destination: Path, expected_files: set[str], populate: Any) -> None` | — | Publish one validated allowlisted tree without exposing partial output. |
| `_load_release` | `(release_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]` | — | Validate release metadata and every declared artifact checksum. |
| `_release_skill` | `(catalog: dict[str, Any], skill_name: str, version: str) -> dict[str, Any]` | — | — |
| `_read_install_lock` | `(destination: Path) -> dict[str, Any]` | — | — |
| `_fsync_directory` | `(path: Path) -> None` | — | Persist directory-entry changes where the platform exposes directory fsync. |
| `_write_atomic_json` | `(destination: Path, filename: str, payload: dict[str, Any]) -> None` | — | — |
| `_write_install_lock` | `(destination: Path, payload: dict[str, Any]) -> None` | — | — |
| `_read_transaction` | `(destination: Path) -> dict[str, Any] \| None` | — | — |
| `_write_transaction` | `(destination: Path, payload: dict[str, Any]) -> None` | — | — |
| `_clear_transaction` | `(destination: Path) -> None` | — | — |
| `_destination_mutation_lock` | `(destination: Path, *, create: bool = False) -> Iterator[None]` | `@contextmanager` | Hold a process-lifetime advisory lock while mutating one destination. |
| `_extract_validated_archive` | `(archive_path: Path, archive_record: dict[str, Any], catalog: dict[str, Any], skill_name: str, destination: Path) -> Path` | — | Validate and extract one immutable in-memory snapshot into staging. |
| `_validate_installed` | `(destination: Path, catalog: dict[str, Any], skill_name: str, version: str) -> None` | — | — |
| `_validate_recorded_install` | `(role_dir: Path, skill_name: str, file_records: Any) -> None` | — | Validate a managed current or backup copy against its locked file hashes. |
| `_remove_managed_path` | `(path: Path) -> None` | — | Remove one managed path without following a substituted symlink. |
| `_validated_backup_root` | `(destination: Path, *, require_exists: bool = False) -> Path` | — | Return the real backup directory only when it is directly contained. |
| `_validated_backup_child` | `(backups: Path, child_name: str) -> Path` | — | Return one non-symlink direct child of the validated backup root. |
| `_path_present` | `(path: Path) -> bool` | — | — |
| `_validate_role_record` | `(path: Path, skill_name: str, record: Any) -> None` | — | — |
| `_validated_stage_paths` | `(destination: Path, stage_name: Any, skill_name: str) -> tuple[Path, Path]` | — | — |
| `_validate_transaction` | `(payload: dict[str, Any]) -> tuple[str, str]` | — | — |
| `_set_transaction_phase` | `(destination: Path, payload: dict[str, Any], phase: str) -> None` | — | — |
| `_begin_transaction` | `(destination: Path, *, operation: str, skill_name: str, before_lock: dict[str, Any], after_lock: dict[str, Any], stage_name: str \| None = None) -> dict[str, Any]` | — | — |
| `_clone_json_object` | `(payload: dict[str, Any]) -> dict[str, Any]` | — | — |
| `_validate_install_final` | `(destination: Path, payload: dict[str, Any], skill_name: str) -> None` | — | — |
| `_recover_install_transaction` | `(destination: Path, payload: dict[str, Any], skill_name: str) -> None` | — | — |
| `_validate_rollback_final` | `(destination: Path, payload: dict[str, Any], skill_name: str) -> None` | — | — |
| `_recover_rollback_transaction` | `(destination: Path, payload: dict[str, Any], skill_name: str) -> None` | — | — |
| `_recover_uninstall_transaction` | `(destination: Path, payload: dict[str, Any], skill_name: str) -> None` | — | — |
| `_recover_interrupted_transaction` | `(destination: Path) -> None` | — | — |
| `install_skill` | `(release_dir: Path, destination: Path, skill_name: str, version: str, archive_format: str) -> None` | — | Atomically install or upgrade one exact skill and retain one rollback copy. |
| `validate_installed_skill` | `(release_dir: Path, destination: Path, skill_name: str) -> None` | — | Validate an installed role against the exact version in its lock record. |
| `rollback_skill` | `(destination: Path, skill_name: str) -> None` | — | Swap the current installation with its retained rollback copy. |
| `uninstall_skill` | `(destination: Path, skill_name: str) -> None` | — | Remove one managed skill, its rollback copy, and its lock entry. |
| `_parser` | `() -> argparse.ArgumentParser` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |