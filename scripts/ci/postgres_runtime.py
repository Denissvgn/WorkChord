#!/usr/bin/env python3
"""Own an isolated PostgreSQL cluster on a native runner."""

import argparse
import os
import re
import shlex
from pathlib import Path
import subprocess
import tempfile


MARKER = '.workchord-ci-cluster'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'stop'])
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--bin-dir', type=Path, required=True)
    parser.add_argument('--port', type=int, default=55432)
    args = parser.parse_args()
    data = args.data_dir.resolve()
    binaries = args.bin_dir.resolve()
    if not 1024 <= args.port <= 65535:
        parser.error('Use an unprivileged local port')
    if args.action == 'stop':
        if not (data / MARKER).is_file():
            if data.exists():
                parser.error('Refusing to stop a cluster not created by this helper')
            return 0
        if (data / 'postmaster.pid').exists():
            subprocess.run([str(binaries / 'pg_ctl'), '-D', str(data), '-m', 'fast', '-w', 'stop'], check=True)
        return 0
    if data.exists():
        parser.error('Use a new data directory; existing clusters are never overwritten')
    version = subprocess.check_output([str(binaries / 'postgres'), '--version'], text=True)
    if not re.search(r'\(PostgreSQL\) 18\.', version):
        parser.error('PostgreSQL 18 is required')
    password = os.environ.get('WORKCHORD_CI_POSTGRES_PASSWORD')
    if not password or '\n' in password or '\r' in password:
        parser.error('Set WORKCHORD_CI_POSTGRES_PASSWORD to a nonempty single-line value')
    data.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', prefix='workchord-pg-password-', dir=data.parent) as secret:
        secret.write(password + '\n')
        secret.flush()
        subprocess.run([str(binaries / 'initdb'), '-D', str(data), '-U', 'postgres',
            '--auth-host=scram-sha-256', '--auth-local=scram-sha-256', '--pwfile=' + secret.name,
            '--encoding=UTF8', '--locale-provider=builtin', '--builtin-locale=PG_UNICODE_FAST'], check=True)
    (data / MARKER).write_text('isolated runner cluster\n')
    subprocess.run([str(binaries / 'pg_ctl'), '-D', str(data), '-l', str(data / 'server.log'),
        '-o', f'-h 127.0.0.1 -p {args.port} -k {shlex.quote(str(data))} -c max_connections=150', '-w', 'start'], check=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
