"""The deployment record names every image, the source and the deployment it replaces."""
import json
import stat
import subprocess

import pytest

from scripts.server import seed_adoption_env as seed
from scripts.server import write_deployment_record as record


def _folder(tmp_path):
    folder = tmp_path / 'instance'
    (folder / 'backend').mkdir(parents=True)
    (folder / 'backend' / 'pyproject.toml').write_text('[project]\nname = "workchord"\nversion = "9.9.9"\n')
    return folder


def _fake_docker(images_rows, containers, volumes=()):
    """Answer the read-only docker calls the script makes."""
    inventory = {'abc': {'Id': 'sha256:aaa', 'RepoDigests': ['postgres@sha256:111'], 'Os': 'linux', 'Architecture': 'arm64'},
        'def': {'Id': 'sha256:bbb', 'RepoDigests': [], 'Os': 'linux', 'Architecture': 'arm64'}}

    def run(*args):
        if args[:2] == ('compose', '--project-name'):
            assert args[-3:] == ('images', '--format', 'json')
            return '\n'.join(json.dumps(row) for row in images_rows)
        if args[:2] == ('image', 'inspect'):
            return json.dumps([inventory[args[2]]])
        if args[0] == 'inspect':
            return json.dumps([containers[args[1]]])
        if args[:2] == ('volume', 'ls'):
            return '\n'.join(volumes)
        if args[:2] == ('ps', '-aq'):
            return '\n'.join(containers)
        raise AssertionError(args)
    return run


def _git(folder, *args):
    if args == ('rev-parse', 'HEAD'):
        return '1234567890abcdef'
    if args[0] == 'describe':
        return 'v9.9.9'
    return ''


def test_record_names_images_source_volumes_and_operator(tmp_path, monkeypatch):
    folder = _folder(tmp_path)
    rows = [{'ContainerName': 'workchord-server-backend-1', 'Repository': 'workchord-backend', 'Tag': '1234567890abcdef', 'ID': 'abc'},
        {'ContainerName': 'workchord-server-frontend-1', 'Repository': 'workchord-frontend', 'Tag': '1234567890abcdef', 'ID': 'def'}]
    containers = {'workchord-server-backend-1': {'Config': {'Labels': {record.SERVICE_LABEL: 'backend'}}},
        'workchord-server-frontend-1': {'Config': {'Labels': {record.SERVICE_LABEL: 'frontend'}}}}
    volumes = ['workchord-server_workchord_postgresql18_data', 'workchord-server_workchord_postgresql_wal_archive',
        'workchord-server_workchord_server_data']
    monkeypatch.setattr(record, 'docker', _fake_docker(rows, containers, volumes))
    monkeypatch.setattr(record, 'git', _git)
    output = tmp_path / 'record' / 'deployment-record.json'
    record.main(['--folder', str(folder), '--env-file', str(tmp_path / 'server.env'), '--operator', 'ops',
        '--credential-sink', str(tmp_path / 'sink'), '--output', str(output)])
    value = json.loads(output.read_text())
    assert value['schema_version'] == 1 and value['operator'] == 'ops'
    assert value['workchord_version'] == '9.9.9'
    assert value['source'] == {'revision': '1234567890abcdef', 'tag': 'v9.9.9', 'worktree_clean': True}
    assert value['compose_project'] == 'workchord-server' and value['folder'] == str(folder.resolve())
    assert value['database_volumes'] == {'data': 'workchord-server_workchord_postgresql18_data',
        'wal_archive': 'workchord-server_workchord_postgresql_wal_archive', 'backups': None}
    backend = next(item for item in value['services'] if item['service'] == 'backend')
    assert backend['image_id'] == 'sha256:aaa' and backend['repo_digests'] == ['postgres@sha256:111']
    assert backend['image'] == 'workchord-backend:1234567890abcdef'
    assert {item['service'] for item in value['services']} == {'backend', 'frontend'}
    assert value['replaces'] is None
    assert stat.S_IMODE(output.stat().st_mode) == 0o644
    assert 'password' not in output.read_text().lower()


def test_record_describes_the_replaced_project_and_archives_an_existing_record(tmp_path, monkeypatch):
    folder = _folder(tmp_path)
    rows = [{'ContainerName': 'workchord-server-backend-1', 'Repository': 'workchord-backend', 'Tag': 'x', 'ID': 'abc'}]
    containers = {'workchord-server-backend-1': {'Config': {'Labels': {record.SERVICE_LABEL: 'backend'}}},
        'old-backend-1': {'Name': '/old-backend-1', 'Image': 'def', 'Config': {'Image': 'sha256:bbb', 'Labels': {record.SERVICE_LABEL: 'backend'}}}}
    fake = _fake_docker(rows, containers, ['old_workchord_postgresql18_data'])

    def routed(*args):
        if args[:2] == ('ps', '-aq'):
            assert args[-1] == 'label=com.docker.compose.project=old'
            return 'old-backend-1'
        return fake(*args)
    monkeypatch.setattr(record, 'docker', routed)
    monkeypatch.setattr(record, 'git', _git)
    output = tmp_path / 'deployment-record.json'
    arguments = ['--folder', str(folder), '--env-file', str(tmp_path / 'e'), '--output', str(output), '--operator', 'ops']
    record.main(arguments + ['--replaces-project', 'old', '--replaces-revision', 'a79d60b8c', '--replaces-version', '1.8.0'])
    first = json.loads(output.read_text())
    assert first['replaces']['compose_project'] == 'old' and first['replaces']['source_revision'] == 'a79d60b8c'
    assert first['replaces']['services'][0]['image_id'] == 'sha256:bbb'
    assert first['replaces']['volumes'] == ['old_workchord_postgresql18_data']
    # A second record replaces the first one and archives it.
    record.main(arguments)
    second = json.loads(output.read_text())
    assert second['replaces']['kind'] == 'record' and second['replaces']['compose_project'] == 'workchord-server'
    assert second['replaces']['source_revision'] == '1234567890abcdef'
    assert len(list((tmp_path / 'deployments').glob('*.json'))) == 1


def test_record_refuses_a_project_without_containers(tmp_path, monkeypatch):
    folder = _folder(tmp_path)
    monkeypatch.setattr(record, 'docker', _fake_docker([], {}))
    monkeypatch.setattr(record, 'git', _git)
    with pytest.raises(ValueError, match='No containers'):
        record.main(['--folder', str(folder), '--env-file', str(tmp_path / 'e'), '--output', str(tmp_path / 'r.json')])
    assert not (tmp_path / 'r.json').exists()


def test_dirty_worktree_and_missing_tag_are_reported(tmp_path, monkeypatch):
    def run(folder, *args):
        if args[0] == 'describe':
            raise subprocess.CalledProcessError(128, args)
        return 'deadbeef' if args[0] == 'rev-parse' else ' M file'
    monkeypatch.setattr(record, 'git', run)
    assert record.source_identity(tmp_path) == {'revision': 'deadbeef', 'tag': None, 'worktree_clean': False}


def test_seed_copies_durable_values_generates_new_identities_and_never_overwrites(tmp_path, capsys):
    old = tmp_path / 'old.env'
    old.write_text('# comment\nPOSTGRES_PASSWORD=pg\nSETTINGS_ENCRYPTION_KEY=key=\nAGENT_BOOTSTRAP_API_KEY=boot\n'
        'WORKCHORD_ADMIN_API_KEY=admin\nCORS_ORIGINS=["http://127.0.0.1:8480"]\nWEB_INTAKE_TOKEN=unrelated\n')
    output = tmp_path / 'server.env'
    assert seed.main(['--old-env', str(old), '--output', str(output), '--http-port', '8480',
        '--set', 'AGENT_LAST_SEEN_INTERVAL_SECONDS=60']) == 0
    assert 'pg' not in capsys.readouterr().out.replace(str(tmp_path), '')
    values = seed.read_env(output)
    assert values['POSTGRES_PASSWORD'] == 'pg' and values['SETTINGS_ENCRYPTION_KEY'] == 'key='
    assert values['CORS_ORIGINS'] == '["http://127.0.0.1:8480"]'
    assert values['WORKCHORD_HTTP_PORT'] == '8480' and values['WORKCHORD_SESSION_COOKIE_SECURE'] == 'false'
    assert values['AGENT_LAST_SEEN_INTERVAL_SECONDS'] == '60'
    assert 'WEB_INTAKE_TOKEN' not in values
    assert len(values['WORKCHORD_RUNTIME_PASSWORD']) == 48
    assert values['DATABASE_RUNTIME_URL'].startswith('postgresql+psycopg://workchord_runtime:')
    assert values['POSTGRES_BACKUP_URL'].endswith('@postgres:5432/workchord')
    assert stat.S_IMODE(output.stat().st_mode) == 0o600
    assert values['AUTONOMY_EVIDENCE_ACCESS_KEY'].startswith('wcaccept')
    assert values['EVIDENCE_STORE_ROOT_ACCESS_KEY'] != values['AUTONOMY_EVIDENCE_ACCESS_KEY']
    assert not any(name.startswith(('MINIO_', 'AUTONOMY_MINIO_')) for name in values)
    assert len(values['WORKCHORD_READINESS_DETAIL_TOKEN']) == 48
    assert seed.main(['--old-env', str(old), '--output', str(output)]) == 1


def test_seed_migrates_an_existing_server_env_in_place(tmp_path, capsys):
    env = tmp_path / 'server.env'
    env.write_text("POSTGRES_PASSWORD=pg\nMINIO_ROOT_USER=wcold\nMINIO_ROOT_PASSWORD=oldsecret\n"
        "AUTONOMY_MINIO_ACCESS_KEY=wcacceptold\nAUTONOMY_MINIO_SECRET_KEY=oldaccept\n"
        "MCP_ALLOWED_HOSTS='[\"localhost:*\"]'\n")
    env.chmod(0o640)
    assert seed.main(['--migrate-env', str(env)]) == 0
    output = capsys.readouterr().out
    assert 'oldsecret' not in output and 'MINIO_ROOT_USER' in output
    text = env.read_text()
    values = seed.read_env(env)
    assert 'MINIO' not in text
    assert "MCP_ALLOWED_HOSTS='[\"localhost:*\"]'" in text and values['POSTGRES_PASSWORD'] == 'pg'
    assert values['AUTONOMY_EVIDENCE_ACCESS_KEY'].startswith('wcaccept')
    assert len(values['EVIDENCE_STORE_ROOT_SECRET_KEY']) == 48
    assert len(values['WORKCHORD_READINESS_DETAIL_TOKEN']) == 48
    assert stat.S_IMODE(env.stat().st_mode) == 0o600
    assert seed.main(['--migrate-env', str(env)]) == 0
    assert 'needs no migration' in capsys.readouterr().out
    assert seed.read_env(env) == values
    assert sorted(path.name for path in tmp_path.iterdir()) == ['server.env']
    # A file already on the new store gains only the token, and keeps an existing one.
    env.write_text('POSTGRES_PASSWORD=pg\n' + ''.join(
        f'{name}={values[name]}\n' for name in values if name.startswith(('EVIDENCE_', 'AUTONOMY_EVIDENCE_'))))
    assert seed.main(['--migrate-env', str(env)]) == 0
    assert 'added WORKCHORD_READINESS_DETAIL_TOKEN (mode 600)' in capsys.readouterr().out
    token = seed.read_env(env)['WORKCHORD_READINESS_DETAIL_TOKEN']
    assert seed.main(['--migrate-env', str(env)]) == 0
    assert seed.read_env(env)['WORKCHORD_READINESS_DETAIL_TOKEN'] == token
    with pytest.raises(SystemExit):
        seed.main(['--migrate-env', str(env), '--output', str(tmp_path / 'other.env')])
    assert seed.main(['--migrate-env', str(tmp_path / 'missing.env')]) == 1


def test_seed_refuses_incomplete_old_files_and_unknown_settings(tmp_path):
    old = tmp_path / 'old.env'
    old.write_text('POSTGRES_PASSWORD=pg\n')
    assert seed.main(['--old-env', str(old), '--output', str(tmp_path / 'a.env')]) == 1
    assert not (tmp_path / 'a.env').exists()
    old.write_text('POSTGRES_PASSWORD=pg\nSETTINGS_ENCRYPTION_KEY=k\nAGENT_BOOTSTRAP_API_KEY=b\nWORKCHORD_ADMIN_API_KEY=a\n')
    assert seed.main(['--old-env', str(old), '--output', str(tmp_path / 'b.env'), '--set', 'POSTGRES_PASSWORD=x']) == 1
