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

# Repositories the hosted runner image preinstalls and no job here installs from. With the strict update
# mode above, a rate-limited response from one of them (HTTP 429) would fail the whole job.
UNUSED_RUNNER_HOSTS = frozenset({'packages.microsoft.com'})


def _repository_hosts(text: str) -> set[str]:
    """Hosts named by the repository lines of a one-line or deb822 source file."""
    hosts = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith(('deb ', 'deb-src ')) or line.lower().startswith('uris:'):
            hosts.update(re.findall(r'https?://([^/\s:]+)', line))
    return hosts


def disable_unused_sources(root: Path) -> None:
    """Set aside source files whose every repository is an unused runner repository."""
    directory = root / 'sources.list.d'
    for path in sorted([*directory.glob('*.list'), *directory.glob('*.sources')]):
        if not path.is_file():
            continue
        hosts = _repository_hosts(path.read_text())
        if hosts and hosts <= UNUSED_RUNNER_HOSTS:
            path.rename(path.with_name(path.name + '.disabled'))
            print(f'Disabled unused runner repository {path}')


def prepare(root: Path, architecture: str) -> None:
    """Replace the direct or mirror-list Ubuntu source; retain suites and signing."""
    if architecture not in ('amd64', 'arm64'):
        raise ValueError(f'Unsupported runner architecture: {architecture}')
    archive = ('https://archive.ubuntu.com/ubuntu' if architecture == 'amd64'
               else 'https://ports.ubuntu.com/ubuntu-ports')
    disable_unused_sources(root)
    paths = [root / 'sources.list']
    paths += sorted((root / 'sources.list.d').glob('*.list'))
    paths += sorted((root / 'sources.list.d').glob('*.sources'))
    for path in paths:
        if not path.is_file():
            continue
        original = path.read_text()
        updated = re.sub(r'https?://azure\.archive\.ubuntu\.com/ubuntu(?=/|\s|$)', archive, original)
        updated = re.sub(r'mirror\+file:/etc/apt/apt-mirrors\.txt(?=\s|$)', archive, updated)
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
