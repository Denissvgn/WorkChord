"""WAL archive retention: segment selection and a point-in-time restore."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path

import pytest
import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PRUNE_SCRIPT = REPOSITORY_ROOT / "scripts/database_backup/prune_wal_archive.sh"
BASE_BACKUP_SCRIPT = REPOSITORY_ROOT / "scripts/database_backup/base_backup.sh"

# Stand-in with pg_archivecleanup's observable behaviour: names that sort
# before the oldest kept segment are removed (`-n` only lists them).
FAKE_ARCHIVECLEANUP = """#!/usr/bin/env bash
mode=$1; directory=$2; oldest=$3
for path in "${directory}"/*; do
  name=$(basename "${path}")
  [[ "${name}" =~ ^[0-9A-F]{24}(\\.[0-9A-F]{8}\\.backup)?$ ]] || continue
  if [[ "${name:0:24}" < "${oldest}" ]]; then
    if [[ "${mode}" == "-n" ]]; then echo "${path}"; else
      echo "pg_archivecleanup: removing file \\"${path}\\"" >&2; rm -f "${path}"
    fi
  fi
done
"""


def _segment(number: int, timeline: int = 1) -> str:
    return f"{timeline:08X}{0:08X}{number:08X}"


def _make_backup(root: Path, name: str, start_segment: str, *, verified: bool = True) -> Path:
    backup = root / name
    backup.mkdir(parents=True)
    (backup / "backup_label").write_text(
        f"START WAL LOCATION: 0/{start_segment[-8:]}000028 (file {start_segment})\n"
        "CHECKPOINT LOCATION: 0/00000000\nBACKUP METHOD: streamed\n"
    )
    if verified:
        (backup / "workchord-files.sha256").write_text("")
    return backup


@pytest.fixture
def layout(tmp_path: Path) -> dict[str, Path]:
    archive = tmp_path / "archive"
    backups = tmp_path / "backups"
    archive.mkdir()
    backups.mkdir()
    fake = tmp_path / "pg_archivecleanup"
    fake.write_text(FAKE_ARCHIVECLEANUP)
    fake.chmod(0o755)
    for number in range(1, 11):
        (archive / _segment(number)).write_text("wal")
    (archive / f"{_segment(4)}.00000028.backup").write_text("history")
    (archive / "00000002.history").write_text("timeline")
    return {"archive": archive, "backups": backups, "cleanup": fake}


def _run(layout: dict[str, Path], *arguments: str, **environment: str):
    env = {
        **os.environ,
        "WAL_ARCHIVE_DIR": str(layout["archive"]),
        "BASE_BACKUP_ROOT": str(layout["backups"]),
        "PG_ARCHIVECLEANUP": str(layout["cleanup"]),
        **environment,
    }
    return subprocess.run(
        ["bash", str(PRUNE_SCRIPT), *arguments],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _names(layout: dict[str, Path]) -> set[str]:
    return {path.name for path in layout["archive"].iterdir()}


def test_nothing_is_deleted_without_a_verified_base_backup(layout) -> None:
    before = _names(layout)
    result = _run(layout)
    assert result.returncode == 0
    assert "nothing deleted" in result.stdout
    assert _names(layout) == before

    # An unfinished backup (no checksum inventory) is not a verified one.
    _make_backup(layout["backups"], "workchord-20260101T000000Z", _segment(8), verified=False)
    (layout["backups"] / ".workchord-20260102T000000Z-abc").mkdir()
    result = _run(layout)
    assert result.returncode == 0
    assert "nothing deleted" in result.stdout
    assert _names(layout) == before


def test_missing_backup_directory_deletes_nothing(layout) -> None:
    shutil.rmtree(layout["backups"])
    before = _names(layout)
    result = _run(layout)
    assert result.returncode == 0
    assert _names(layout) == before


def test_segments_needed_by_the_newest_backup_are_kept(layout) -> None:
    _make_backup(layout["backups"], "workchord-20260101T000000Z", _segment(2))
    _make_backup(layout["backups"], "workchord-20260103T000000Z", _segment(6))
    _make_backup(layout["backups"], "workchord-20260105T000000Z", _segment(8), verified=False)

    result = _run(layout)

    assert result.returncode == 0, result.stderr
    assert f"from {_segment(6)} onward" in result.stdout
    kept = _names(layout)
    assert {_segment(n) for n in range(6, 11)} <= kept
    assert not any(_segment(n) in kept for n in range(1, 6))
    assert f"{_segment(4)}.00000028.backup" not in kept
    assert "00000002.history" in kept


def test_keep_backups_extends_the_window_to_older_backups(layout) -> None:
    _make_backup(layout["backups"], "workchord-20260101T000000Z", _segment(2))
    _make_backup(layout["backups"], "workchord-20260103T000000Z", _segment(6))

    result = _run(layout, WAL_PRUNE_KEEP_BACKUPS="2")

    assert result.returncode == 0, result.stderr
    kept = _names(layout)
    assert {_segment(n) for n in range(2, 11)} <= kept
    assert _segment(1) not in kept

    # More backups requested than exist uses the oldest one that does.
    result = _run(layout, WAL_PRUNE_KEEP_BACKUPS="9")
    assert result.returncode == 0
    assert _segment(2) in _names(layout)


def test_dry_run_lists_without_deleting_and_rerun_is_idempotent(layout) -> None:
    _make_backup(layout["backups"], "workchord-20260103T000000Z", _segment(6))
    before = _names(layout)

    result = _run(layout, "--dry-run")
    assert result.returncode == 0
    assert _segment(5) in result.stdout
    assert _segment(7) not in result.stdout
    assert _names(layout) == before

    assert _run(layout).returncode == 0
    after_first = _names(layout)
    second = _run(layout)
    assert second.returncode == 0
    assert "Removed 0" in second.stdout
    assert _names(layout) == after_first


def test_archive_that_lacks_the_start_segment_is_left_alone(layout) -> None:
    _make_backup(layout["backups"], "workchord-20260103T000000Z", _segment(42))
    before = _names(layout)
    result = _run(layout)
    assert result.returncode == 3
    assert "missing" in result.stderr
    assert _names(layout) == before


def test_invalid_keep_value_is_rejected(layout) -> None:
    result = _run(layout, WAL_PRUNE_KEEP_BACKUPS="0")
    assert result.returncode == 2


def test_compose_runs_the_retention_loop_against_both_volumes() -> None:
    compose = yaml.safe_load((REPOSITORY_ROOT / "docker-compose.yml").read_text())
    service = compose["services"]["wal-archive-retention"]
    volumes = service["volumes"]
    assert "workchord_postgresql_wal_archive:/var/lib/postgresql/wal-archive" in volumes
    assert "workchord_postgresql_backups:/backups:ro" in volumes
    assert service["restart"] == "unless-stopped"
    assert "prune_wal_archive.sh" in " ".join(service["command"])
    # The self-hosted overlay inherits archiving and this service from the base file.
    server = yaml.safe_load((REPOSITORY_ROOT / "docker-compose.server.yml").read_text())
    assert "archive_mode=on" in compose["services"]["postgres"]["command"]
    assert "command" not in server["services"]["postgres"]
    assert "wal-archive-retention" not in server["services"]


def _docker(*arguments: str, check: bool = True, **kwargs):
    return subprocess.run(
        ["docker", *arguments], capture_output=True, text=True, check=check, **kwargs
    )


@pytest.mark.integration
def test_point_in_time_restore_works_from_retained_backup_and_pruned_archive() -> None:
    if shutil.which("docker") is None:
        pytest.skip("docker is unavailable")
    image = "postgres:18.4-bookworm"
    if _docker("image", "inspect", image, check=False).returncode != 0:
        pytest.skip(f"{image} is not present locally")
    name = f"workchord-wal-retention-test-{uuid.uuid4().hex[:10]}"
    archive = "/var/lib/postgresql/wal-archive"
    server_command = (
        f"mkdir -p {archive} /backups && chown postgres:postgres {archive} && chmod 700 {archive} && "
        "exec docker-entrypoint.sh postgres -c wal_level=replica -c archive_mode=on "
        "-c archive_timeout=2s "
        f"-c 'archive_command=test ! -f {archive}/%f && cp %p {archive}/%f'"
    )

    def sql(statement: str, *, port: int = 5432) -> str:
        return _docker(
            "exec", name, "psql", "-h", "127.0.0.1", "-p", str(port), "-U", "postgres",
            "-X", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-c", statement,
        ).stdout.strip()

    def shell(script: str, *, user: str = "root") -> str:
        return _docker("exec", "-u", user, name, "bash", "-ec", script).stdout

    def switch_wal() -> None:
        sql("SELECT pg_switch_wal()")

    _docker(
        "run", "-d", "--name", name, "-e", "POSTGRES_HOST_AUTH_METHOD=trust",
        "--entrypoint", "bash", image, "-c", server_command,
    )
    try:
        for _ in range(60):
            if _docker("exec", name, "pg_isready", "-h", "127.0.0.1", "-U", "postgres", check=False).returncode == 0:
                # The image restarts once after initialisation; require two good checks.
                time.sleep(1)
                if _docker("exec", name, "pg_isready", "-h", "127.0.0.1", "-U", "postgres", check=False).returncode == 0:
                    break
            time.sleep(1)
        else:
            pytest.fail("PostgreSQL did not become ready")

        _docker("cp", str(BASE_BACKUP_SCRIPT), f"{name}:/opt/base_backup.sh")
        _docker("cp", str(PRUNE_SCRIPT), f"{name}:/opt/prune_wal_archive.sh")

        sql("CREATE TABLE marker (id int primary key, note text)")
        for number in range(3):
            sql(f"INSERT INTO marker VALUES ({number}, 'before-backup')")
            switch_wal()
        shell(
            "export DATABASE_BACKUP_URL=postgresql://postgres@127.0.0.1:5432/postgres "
            "DEPLOYMENT_ENVIRONMENT=test BACKUP_ENCRYPTION_CONFIRMED=true; "
            "bash /opt/base_backup.sh"
        )
        sql("INSERT INTO marker VALUES (10, 'after-backup')")
        switch_wal()
        time.sleep(1)
        target = sql("SELECT now()")
        time.sleep(1)
        sql("INSERT INTO marker VALUES (11, 'after-target')")
        switch_wal()
        time.sleep(3)

        listing_before = shell(f"ls {archive}").split()
        dry = shell("bash /opt/prune_wal_archive.sh --dry-run")
        assert "Dry run" in dry
        assert shell(f"ls {archive}").split() == listing_before
        pruned = shell("bash /opt/prune_wal_archive.sh")
        assert "Removed" in pruned and "Removed 0" not in pruned
        listing_after = shell(f"ls {archive}").split()
        assert 0 < len(listing_after) < len(listing_before)
        assert "Removed 0" in shell("bash /opt/prune_wal_archive.sh")

        shell(
            "set -e; backup=$(ls -d /backups/base/workchord-* | tail -n 1); "
            "mkdir /restore && cp -a \"${backup}/.\" /restore/ && chown -R postgres:postgres /restore "
            "&& chmod 700 /restore && touch /restore/recovery.signal && "
            f"printf \"restore_command = 'cp {archive}/%%f %%p'\\n"
            f"recovery_target_time = '{target}'\\nrecovery_target_action = promote\\n\" "
            ">> /restore/postgresql.auto.conf && chown postgres:postgres /restore/postgresql.auto.conf"
        )
        shell(
            "pg_ctl -D /restore -o '-p 5433 -c archive_mode=off -c listen_addresses=127.0.0.1' "
            "-l /tmp/restore.log -w -t 120 start",
            user="postgres",
        )
        rows = sql("SELECT string_agg(id::text, ',' ORDER BY id) FROM marker", port=5433)
        assert rows == "0,1,2,10"
    finally:
        _docker("rm", "-f", "-v", name, check=False)
