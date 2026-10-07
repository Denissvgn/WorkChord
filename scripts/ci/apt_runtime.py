"""Prepare job-local APT sources for bounded signed package installation."""

import argparse
from pathlib import Path
import re
import subprocess


APT_CONFIG = '''Acquire::Retries "2";
Acquire::http::Timeout "15";
Acquire::https::Timeout "15";
APT::Update::Error-Mode "any";
'''


def prepare(root: Path, architecture: str) -> None:
    """Replace only the hosted Ubuntu Azure mirror; retain suites and signing."""
    if architecture not in ('amd64', 'arm64'):
        raise ValueError(f'Unsupported runner architecture: {architecture}')
    archive = ('https://archive.ubuntu.com/ubuntu' if architecture == 'amd64'
               else 'https://ports.ubuntu.com/ubuntu-ports')
    paths = [root / 'sources.list']
    paths += sorted((root / 'sources.list.d').glob('*.list'))
    paths += sorted((root / 'sources.list.d').glob('*.sources'))
    for path in paths:
        if not path.is_file():
            continue
        original = path.read_text()
        updated = re.sub(r'https?://azure\.archive\.ubuntu\.com/ubuntu(?=/|\s|$)', archive, original)
        if updated != original:
            path.write_text(updated)
            print(f'Prepared Ubuntu mirror in {path}')
    config = root / 'apt.conf.d' / '80workchord-ci'
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(APT_CONFIG)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    architecture = subprocess.check_output(['dpkg', '--print-architecture'], text=True).strip()
    prepare(Path('/etc/apt'), architecture)


if __name__ == '__main__':
    main()
