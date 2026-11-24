#!/usr/bin/env python3
"""Seed the self-hosted server environment file from a running instance's file.

Adopting an existing database needs the same durable secrets the database and
the encrypted settings were created with. This script copies exactly those
(and a short list of operator settings) from the old environment file into a
new, private `server.env`, and generates fresh values for the identities that
the self-hosted layout adds. It never prints a value and never overwrites an
existing file. `accept_self_hosted.sh` then reads the file like any other
`server.env`.
"""

import argparse
import os
from pathlib import Path
import re
import secrets
import sys

# Created with the existing database or the stored settings; losing one is not recoverable.
CARRIED_REQUIRED = ['POSTGRES_PASSWORD', 'SETTINGS_ENCRYPTION_KEY', 'AGENT_BOOTSTRAP_API_KEY', 'WORKCHORD_ADMIN_API_KEY']
# Operator settings copied when the old file sets them.
CARRIED_OPTIONAL = ['WORKCHORD_AUTH_MODE', 'MODEL_AWARE_ROUTING_MODE', 'AGENT_TEAM_CREDENTIAL_SINK_REF',
    'AGENT_SKILL_BUNDLES_PUBLIC', 'AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256', 'CORS_ORIGINS']
# Settings the operator may add with --set; each is preserved by accept_self_hosted.sh.
SETTABLE = ['MCP_ALLOWED_HOSTS', 'MCP_ALLOWED_ORIGINS', 'AGENT_LAST_SEEN_INTERVAL_SECONDS', 'TRUSTED_PROXY_IPS',
    'WORKCHORD_AUTH_MODE', 'MODEL_AWARE_ROUTING_MODE', 'CORS_ORIGINS']
NAME = re.compile(r'[A-Z][A-Z0-9_]*')


def read_env(path):
    values = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '\'"':
            value = value[1:-1]
        values[key.strip()] = value
    return values


def quote(value):
    if "'" in value or '\n' in value:
        raise ValueError('A value with a quote or a newline cannot be written to the environment file')
    return value if re.fullmatch(r'[A-Za-z0-9_@%+=:,./-]*', value) else f"'{value}'"


def build(old, settings, http_port, postgres_port, bind, session_cookie_secure):
    missing = [name for name in CARRIED_REQUIRED if not old.get(name)]
    if missing:
        raise ValueError('The old environment file lacks: ' + ', '.join(missing))
    hexed = lambda size: secrets.token_hex(size)
    values = {name: old[name] for name in CARRIED_REQUIRED}
    values.update({name: old[name] for name in CARRIED_OPTIONAL if old.get(name)})
    values.update({
        'WORKCHORD_MIGRATOR_PASSWORD': hexed(24), 'WORKCHORD_RUNTIME_PASSWORD': hexed(24),
        'WORKCHORD_BACKUP_PASSWORD': hexed(24), 'MINIO_ROOT_USER': 'wc' + hexed(8), 'MINIO_ROOT_PASSWORD': hexed(24),
        'AUTONOMY_MINIO_ACCESS_KEY': 'wcaccept' + hexed(8), 'AUTONOMY_MINIO_SECRET_KEY': hexed(24),
        'OPENBAO_DEV_ROOT_TOKEN': hexed(24),
        'WORKCHORD_HTTP_BIND': bind, 'WORKCHORD_HTTP_PORT': str(http_port), 'POSTGRES_HOST_PORT': str(postgres_port),
        'WORKCHORD_SESSION_COOKIE_SECURE': 'true' if session_cookie_secure else 'false'})
    values.update({
        'DATABASE_MIGRATION_URL': f"postgresql+psycopg://workchord_migrator:{values['WORKCHORD_MIGRATOR_PASSWORD']}@postgres:5432/workchord",
        'DATABASE_RUNTIME_URL': f"postgresql+psycopg://workchord_runtime:{values['WORKCHORD_RUNTIME_PASSWORD']}@postgres:5432/workchord",
        'POSTGRES_BACKUP_URL': f"postgresql://workchord_backup:{values['WORKCHORD_BACKUP_PASSWORD']}@postgres:5432/workchord"})
    values['POSTGRES_DATABASE_URL'] = values['DATABASE_RUNTIME_URL']
    for item in settings:
        name, _, value = item.partition('=')
        if name not in SETTABLE or not value:
            raise ValueError(f'--set accepts NAME=VALUE for: {", ".join(SETTABLE)}')
        values[name] = value
    return values


def write(path, values):
    path = Path(path)
    if path.exists():
        raise FileExistsError('Refusing to overwrite an existing environment file')
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as stream:
        for name in sorted(values):
            if not NAME.fullmatch(name):
                raise ValueError('Invalid variable name')
            stream.write(f'{name}={quote(values[name])}\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--old-env', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='The new server.env (must not exist)')
    parser.add_argument('--http-port', type=int, default=8080)
    parser.add_argument('--postgres-port', type=int, default=55432)
    parser.add_argument('--bind', default='127.0.0.1')
    parser.add_argument('--session-cookie-secure', action='store_true',
        help='Mark session cookies Secure; leave off only for loopback-only plain HTTP')
    parser.add_argument('--set', dest='settings', action='append', default=[], metavar='NAME=VALUE')
    args = parser.parse_args(argv)
    try:
        values = build(read_env(args.old_env), args.settings, args.http_port, args.postgres_port, args.bind,
            args.session_cookie_secure)
        write(args.output, values)
    except (ValueError, FileExistsError, OSError) as error:
        print(f'Refused: {error}', file=sys.stderr)
        return 1
    print(f'Wrote {args.output} with {len(values)} variables (mode 600)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
