#!/usr/bin/env python3
"""Own isolated Compose resources without reusing operator credentials or data."""

import argparse
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MARKER = '.workchord-rehearsal.json'
OWNER_LABEL = 'workchord.rehearsal-owner'
PROJECT_LABEL = 'com.docker.compose.project'


def docker(*args):
    return subprocess.check_output(['docker', *args], text=True).strip()


def resources(project):
    result = {}
    for kind, command in [('containers', ['ps', '-aq']), ('volumes', ['volume', 'ls', '-q']), ('networks', ['network', 'ls', '-q'])]:
        identities = docker(*command, '--filter', f'label={PROJECT_LABEL}={project}').splitlines()
        rows = []
        for identity in identities:
            inspect = ['inspect', identity] if kind == 'containers' else [kind[:-1], 'inspect', identity]
            item = json.loads(docker(*inspect))[0]
            labels = item.get('Config', {}).get('Labels', {}) if kind == 'containers' else item.get('Labels', {})
            rows.append({'id': identity, 'name': item.get('Name'), 'owner': (labels or {}).get(OWNER_LABEL)})
        result[kind] = rows
    return result


def load_marker(root):
    root = Path(root)
    path = root / MARKER
    if root.is_symlink() or path.is_symlink() or not path.is_file() or path.stat().st_uid != os.getuid() or path.stat().st_mode & 0o077:
        raise ValueError('A private run-owned marker is required')
    value = json.loads(path.read_text())
    if value['runtime_root'] != str(root.resolve()) or not re.fullmatch(r'workchord-rehearsal-[a-z0-9-]{1,48}', value['project']):
        raise ValueError('Ownership marker identity mismatch')
    return value


def verify(root):
    marker = load_marker(root)
    found = resources(marker['project'])
    if any(row['owner'] != marker['owner'] for rows in found.values() for row in rows):
        raise ValueError('Refusing to use resources owned by another run')
    return marker, found


def prepare(root, project, platform):
    root = Path(root)
    if not re.fullmatch(r'/[A-Za-z0-9_./-]+', str(root)):
        raise ValueError('Use a shell-safe absolute runtime path without spaces or control characters')
    if not root.is_absolute() or not re.fullmatch(r'workchord-rehearsal-[a-z0-9-]{1,48}', project):
        raise ValueError('Use a unique rehearsal project and absolute fresh runtime path')
    reserved = (ROOT / '.runtime/autonomy').resolve()
    resolved = root.resolve()
    if resolved == reserved or reserved in resolved.parents or resolved in reserved.parents:
        raise ValueError('The operator runtime must remain separate')
    if root.exists() or any(resources(project).values()):
        raise ValueError('Use fresh runtime and project identities; existing resources are never adopted')
    architecture = docker('info', '--format', '{{.Architecture}}')
    native = {'aarch64': 'arm64', 'arm64': 'arm64', 'x86_64': 'amd64', 'amd64': 'amd64'}.get(architecture)
    if platform != 'linux/' + str(native):
        raise ValueError('The selected platform must match the native Docker engine')
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    marker = {'schema_version': 1, 'project': project, 'runtime_root': str(resolved), 'platform': platform,
        'owner': secrets.token_hex(16), 'source_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}
    path = root / MARKER
    path.write_text(json.dumps(marker, sort_keys=True) + '\n'); path.chmod(0o600)
    return marker


def ownership_override(marker, definition):
    owner = {OWNER_LABEL: marker['owner']}
    result = {'services': {}, 'volumes': {}, 'networks': {}}
    for name, service in definition.get('services', {}).items():
        if service.get('container_name') and not service['container_name'].startswith(marker['project'] + '-'):
            raise ValueError('A fixed container name would escape isolation')
        result['services'][name] = {'platform': marker['platform'], 'labels': owner}
        if service.get('build'):
            result['services'][name]['build'] = {'platforms': [marker['platform']]}
    for kind in ['volumes', 'networks']:
        for name, resource in definition.get(kind, {}).items():
            if resource and resource.get('external'):
                raise ValueError('External resources cannot be adopted by a rehearsal')
            result[kind][name] = {'name': marker['project'] + '_' + name, 'labels': owner}
    return result


def verify_images(marker, images):
    for reference in sorted(set(images)):
        item = json.loads(docker('image', 'inspect', reference))[0]
        if f"{item['Os']}/{item['Architecture']}" != marker['platform']:
            raise ValueError('Selected image architecture does not match the native platform')


def cleanup(root):
    marker = load_marker(root)
    found = resources(marker['project'])
    removed, retained, failures = [], [], []
    for kind in ['containers', 'networks', 'volumes']:
        for row in found[kind]:
            if row['owner'] != marker['owner']:
                retained.append({'kind': kind, 'id': row['id']}); continue
            # Re-observe the exact identity immediately before its removal.
            current = resources(marker['project'])[kind]
            if not any(item['id'] == row['id'] and item['owner'] == marker['owner'] for item in current):
                raise ValueError('Resource ownership changed during cleanup')
            args = ['rm', '-f', row['id']] if kind == 'containers' else [kind[:-1], 'rm', row['id']]
            try:
                docker(*args); removed.append({'kind': kind, 'id': row['id']})
            except subprocess.CalledProcessError as cause:
                failures.append({'kind': kind, 'id': row['id'], 'exit_code': cause.returncode})
    result = {'removed': removed, 'unrelated_retained': retained, 'failures': failures, 'remaining': resources(marker['project'])}
    path = Path(root) / 'cleanup-results.json'; path.write_text(json.dumps(result, indent=2) + '\n'); path.chmod(0o600)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'verify', 'override', 'images', 'cleanup'])
    parser.add_argument('--runtime-root', type=Path, required=True)
    parser.add_argument('--project')
    parser.add_argument('--platform', default='linux/arm64')
    args = parser.parse_args()
    if args.action == 'run':
        marker = prepare(args.runtime_root, args.project or '', args.platform)
        environment = {key: value for key, value in os.environ.items() if key in {'PATH', 'HOME', 'TMPDIR', 'DOCKER_HOST', 'DOCKER_CONTEXT'}}
        def free_port():
            with socket.socket() as listener:
                listener.bind(('127.0.0.1', 0)); return str(listener.getsockname()[1])
        environment.update(WORKCHORD_HTTP_PORT=free_port(), POSTGRES_HOST_PORT=free_port())
        environment.update(WORKCHORD_COMPOSE_PROJECT=marker['project'], WORKCHORD_ACCEPTANCE_RUNTIME_DIR=marker['runtime_root'],
            WORKCHORD_IMAGE_PREFIX=marker['project'], WORKCHORD_CONTAINER_PLATFORM=marker['platform'], DOCKER_DEFAULT_PLATFORM=marker['platform'])
        try:
            subprocess.run([str(ROOT / 'scripts/server/accept_self_hosted.sh')], cwd=ROOT, env=environment, check=True)
        finally:
            result = cleanup(args.runtime_root)
            if result['failures']: raise RuntimeError('Owned cleanup incomplete; inspect cleanup-results.json')
    elif args.action == 'cleanup':
        result = cleanup(args.runtime_root)
        print(json.dumps(result))
        if result['failures']: raise SystemExit(1)
    else:
        marker, found = verify(args.runtime_root)
        if args.action == 'verify':
            if args.project and marker['project'] != args.project: raise ValueError('Project identity mismatch')
        elif args.action == 'override':
            definition = json.load(__import__('sys').stdin)
            path = args.runtime_root / 'ownership.compose.json'; path.write_text(json.dumps(ownership_override(marker, definition)) + '\n'); path.chmod(0o600)
        else:
            verify_images(marker, __import__('sys').stdin.read().splitlines())
        path = args.runtime_root / 'owned-resources.json'; path.write_text(json.dumps({'source_revision': marker['source_revision'], 'project': marker['project'], 'platform': marker['platform'], 'resources': found}, indent=2) + '\n'); path.chmod(0o600)


if __name__ == '__main__':
    main()
