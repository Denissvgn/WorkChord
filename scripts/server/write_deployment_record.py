#!/usr/bin/env python3
"""Write the deployment record of a self-hosted WorkChord instance.

The record names the exact images of every service, the source revision and
release version, the Compose project, the folder, the database volumes, the
time, the operator, and the deployment it replaces. It holds no secrets: paths
and identities only. A later scratch twin of the instance starts from it.
"""

import argparse
import datetime
import getpass
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
RECORD_NAME = 'deployment-record.json'
PROJECT_LABEL = 'com.docker.compose.project'
SERVICE_LABEL = 'com.docker.compose.service'
DATABASE_VOLUMES = {
    'data': 'workchord_postgresql18_data',
    'wal_archive': 'workchord_postgresql_wal_archive',
    'backups': 'workchord_postgresql_backups',
}


def docker(*args):
    return subprocess.check_output(['docker', *args], text=True).strip()


def git(folder, *args):
    return subprocess.check_output(['git', '-C', str(folder), *args], text=True).strip()


def parse_json_lines(text):
    """Accept both a JSON array and one JSON object per line."""
    text = text.strip()
    if not text:
        return []
    if text.startswith('['):
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def image_identity(reference):
    """Return the immutable identity of one local image."""
    item = json.loads(docker('image', 'inspect', reference))[0]
    return {'image_id': item['Id'], 'repo_digests': sorted(item.get('RepoDigests') or []),
        'platform': f"{item.get('Os', '')}/{item.get('Architecture', '')}"}


def container_service(container):
    item = json.loads(docker('inspect', container))[0]
    return (item.get('Config', {}).get('Labels') or {}).get(SERVICE_LABEL, container)


def compose_images(project, compose_args):
    """Images of the containers a Compose project holds, read from `docker compose images`."""
    rows = parse_json_lines(docker('compose', '--project-name', project, *compose_args, 'images', '--format', 'json'))
    services = []
    for row in rows:
        reference = row['Repository'] + (':' + row['Tag'] if row.get('Tag') and row['Tag'] != '<none>' else '')
        services.append({'service': container_service(row['ContainerName']), 'container': row['ContainerName'],
            'image': reference, **image_identity(row['ID'])})
    return sorted(services, key=lambda item: (item['service'], item['container'] or ''))


def project_images(project):
    """Images of the containers of any Compose project, read with `docker inspect`."""
    identities = docker('ps', '-aq', '--filter', f'label={PROJECT_LABEL}={project}').splitlines()
    services = []
    for identity in identities:
        item = json.loads(docker('inspect', identity))[0]
        labels = item.get('Config', {}).get('Labels') or {}
        image = image_identity(item['Image'])
        services.append({'service': labels.get(SERVICE_LABEL, item.get('Name', '').lstrip('/')),
            'container': item.get('Name', '').lstrip('/'), 'image': item.get('Config', {}).get('Image'), **image})
    return sorted(services, key=lambda item: (item['service'], item['container'] or ''))


def project_volumes(project):
    names = docker('volume', 'ls', '--filter', f'label={PROJECT_LABEL}={project}', '--format', '{{.Name}}').splitlines()
    return sorted(names)


def database_volumes(project, names):
    found = {}
    for role, suffix in DATABASE_VOLUMES.items():
        expected = f'{project}_{suffix}'
        found[role] = expected if expected in names else None
    return found


def release_version(folder):
    with (Path(folder) / 'backend' / 'pyproject.toml').open('rb') as handle:
        return tomllib.load(handle)['project']['version']


def source_identity(folder):
    revision = git(folder, 'rev-parse', 'HEAD')
    try:
        tag = git(folder, 'describe', '--tags', '--exact-match', 'HEAD')
    except subprocess.CalledProcessError:
        tag = None
    dirty = bool(git(folder, 'status', '--porcelain', '--untracked-files=normal'))
    return {'revision': revision, 'tag': tag, 'worktree_clean': not dirty}


def replaced_deployment(args, destination):
    """Describe what this record replaces: an explicit project or file, else the prior record."""
    if args.replaces_project:
        services = project_images(args.replaces_project)
        value = {'kind': 'compose-project', 'compose_project': args.replaces_project,
            'source_revision': args.replaces_revision, 'workchord_version': args.replaces_version,
            'volumes': project_volumes(args.replaces_project), 'services': services}
        if not services:
            value['note'] = 'No containers were found for this project when the record was written'
        return value
    source = Path(args.replaces_record) if args.replaces_record else (destination if destination.is_file() else None)
    if source is None:
        return None
    previous = json.loads(source.read_text())
    return {'kind': 'record', 'recorded_at': previous.get('written_at'), 'compose_project': previous.get('compose_project'),
        'source_revision': previous.get('source', {}).get('revision'), 'workchord_version': previous.get('workchord_version'),
        'services': previous.get('services', []), 'volumes': previous.get('database_volumes')}


def build_record(args, destination):
    folder = Path(args.folder).resolve()
    compose_files = [str(folder / name) for name in args.compose_file]
    compose_args = ['--env-file', str(Path(args.env_file)), *[item for path in compose_files for item in ('-f', path)], '--profile', '*']
    volumes = database_volumes(args.project, project_volumes(args.project))
    services = compose_images(args.project, compose_args)
    if not services:
        raise ValueError('No containers were found for the Compose project; start the stack first')
    return {'schema_version': SCHEMA_VERSION,
        'written_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'operator': args.operator or getpass.getuser(),
        'workchord_version': release_version(folder),
        'source': source_identity(folder),
        'compose_project': args.project,
        'folder': str(folder),
        'compose_files': compose_files,
        'env_file': str(Path(args.env_file)),
        'credential_sink': str(Path(args.credential_sink)),
        'database_volumes': volumes,
        'services': services,
        'replaces': replaced_deployment(args, destination)}


def write_record(record, destination):
    """Write atomically and archive a record that already exists."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file():
        previous = json.loads(destination.read_text())
        stamp = str(previous.get('written_at', 'unknown')).replace(':', '').replace('-', '')
        archive = destination.parent / 'deployments' / f"{stamp}-{previous.get('compose_project', 'unknown')}.json"
        archive.parent.mkdir(exist_ok=True)
        if not archive.exists():
            archive.write_text(destination.read_text())
    handle, temporary = tempfile.mkstemp(dir=destination.parent, prefix='.deployment-record-')
    with os.fdopen(handle, 'w') as stream:
        stream.write(json.dumps(record, indent=2, sort_keys=True) + '\n')
    os.chmod(temporary, 0o644)
    os.replace(temporary, destination)
    return destination


def parser():
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument('--folder', type=Path, default=ROOT, help='The instance folder (the release checkout)')
    argument_parser.add_argument('--project', default='workchord-server')
    argument_parser.add_argument('--env-file', type=Path)
    argument_parser.add_argument('--compose-file', action='append', default=None, help='Relative to the folder; repeatable')
    argument_parser.add_argument('--credential-sink', type=Path)
    argument_parser.add_argument('--output', type=Path)
    argument_parser.add_argument('--operator')
    argument_parser.add_argument('--replaces-project', help='Compose project of the deployment being replaced (read-only inspection)')
    argument_parser.add_argument('--replaces-revision')
    argument_parser.add_argument('--replaces-version')
    argument_parser.add_argument('--replaces-record', type=Path, help='A previous record file')
    return argument_parser


def main(argv=None):
    args = parser().parse_args(argv)
    folder = args.folder.resolve()
    runtime = folder / '.runtime' / 'autonomy'
    args.env_file = args.env_file or runtime / 'server.env'
    args.compose_file = args.compose_file or ['docker-compose.yml', 'docker-compose.server.yml']
    args.credential_sink = args.credential_sink or runtime / 'credential-sink'
    destination = args.output or runtime / RECORD_NAME
    destination = Path(destination)
    record = build_record(args, destination)
    path = write_record(record, destination)
    print(f'Wrote {path}')


if __name__ == '__main__':
    main()
