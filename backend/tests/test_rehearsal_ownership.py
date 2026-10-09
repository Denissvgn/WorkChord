"""Isolation cannot adopt operator paths, names, architectures or unrelated resources."""
import json
import subprocess
import pytest
from scripts.server import isolated_rehearsal as isolation


def test_prepare_refuses_existing_and_operator_paths(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, 'resources', lambda project: {'containers': [], 'networks': [], 'volumes': []})
    with pytest.raises(ValueError, match='operator runtime'):
        isolation.prepare(isolation.ROOT / '.runtime/autonomy', 'workchord-rehearsal-safe', 'linux/arm64')
    with pytest.raises(ValueError, match='fresh'):
        isolation.prepare(tmp_path, 'workchord-rehearsal-safe', 'linux/arm64')
    with pytest.raises(ValueError, match='unique'):
        isolation.prepare(tmp_path / 'fresh', 'workchord-server', 'linux/arm64')


def test_platform_and_fixed_external_names_fail_before_launch(tmp_path, monkeypatch):
    monkeypatch.setattr(isolation, 'resources', lambda project: {'containers': [], 'networks': [], 'volumes': []})
    monkeypatch.setattr(isolation, 'docker', lambda *args: 'aarch64')
    with pytest.raises(ValueError, match='native'):
        isolation.prepare(tmp_path / 'fresh', 'workchord-rehearsal-safe', 'linux/amd64')
    marker = {'owner': 'owned', 'project': 'workchord-rehearsal-safe', 'platform': 'linux/arm64'}
    with pytest.raises(ValueError, match='External'):
        isolation.ownership_override(marker, {'volumes': {'data': {'external': True}}})
    with pytest.raises(ValueError, match='fixed'):
        isolation.ownership_override(marker, {'services': {'backend': {'container_name': 'workchord-server-backend'}}})
    result = isolation.ownership_override(marker, {'services': {'backend': {'build': {'context': '.'}}}, 'volumes': {'data': {}}, 'networks': {'app': {}}})
    assert result['services']['backend']['platform'] == 'linux/arm64'
    assert result['services']['backend']['build']['platforms'] == ['linux/arm64']
    assert result['volumes']['data']['name'] == 'workchord-rehearsal-safe_data'


def test_cleanup_removes_only_matching_identities_and_keeps_failure_evidence(tmp_path, monkeypatch):
    marker = {'owner': 'owned', 'project': 'workchord-rehearsal-safe', 'runtime_root': str(tmp_path.resolve()), 'platform': 'linux/arm64'}
    path = tmp_path / isolation.MARKER; path.write_text(json.dumps(marker)); path.chmod(0o600)
    inventory = {'containers': [{'id': 'owned-container', 'owner': 'owned'}, {'id': 'unrelated-container', 'owner': 'someone-else'}],
        'networks': [], 'volumes': [{'id': 'owned-volume', 'owner': 'owned'}]}
    monkeypatch.setattr(isolation, 'resources', lambda project: inventory)
    calls = []
    def remove(*args):
        calls.append(args)
        if args[-1] == 'owned-volume': raise subprocess.CalledProcessError(1, args)
        inventory['containers'] = [row for row in inventory['containers'] if row['id'] != args[-1]]
    monkeypatch.setattr(isolation, 'docker', remove)
    result = isolation.cleanup(tmp_path)
    assert ('rm', '-f', 'unrelated-container') not in calls
    assert result['unrelated_retained'] == [{'kind': 'containers', 'id': 'unrelated-container'}]
    assert result['failures'] == [{'kind': 'volumes', 'id': 'owned-volume', 'exit_code': 1}]
    assert (tmp_path / 'cleanup-results.json').is_file()
