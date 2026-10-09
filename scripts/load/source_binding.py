"""Independently bind local measurements to the source that actually executes."""
import hashlib
import json
from pathlib import Path
import platform
import sys
from importlib.metadata import version


def source_binding():
    root = Path(__file__).resolve().parents[2]
    paths = sorted({*root.glob('backend/app/**/*.py'), *root.glob('scripts/load/*.py'),
                    *root.glob('backend/*requirements.lock')})
    files = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in paths}
    return {'method': 'executing_service_and_runner_files_sha256', 'files': files,
            'sha256': hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
            'python': sys.version, 'platform': platform.platform(), 'architecture': platform.machine(),
            'packages': {name: version(name) for name in ('SQLAlchemy', 'psycopg', 'greenlet', 'httpx')}}


def verify_binding(before):
    after = source_binding()
    if before['sha256'] != after['sha256']:
        raise ValueError('Executing source changed during measurement')
    return after
