"""Runner APT preparation preserves signed sources and bounds stalled downloads."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import apt_runtime


class AptPreparation(unittest.TestCase):
    def test_legacy_and_deb822_sources_keep_signing_and_unrelated_repositories(self):
        for suffix in ('list', 'sources'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'sources.list.d').mkdir()
                source = root / 'sources.list.d' / f'ubuntu.{suffix}'
                original = ('URIs: http://azure.archive.ubuntu.com/ubuntu/\n'
                            'Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n'
                            'deb http://azure.archive.ubuntu.com/ubuntu noble-security main\n'
                            'deb https://apt.postgresql.org/pub/repos/apt noble-pgdg main\n')
                source.write_text(original)
                apt_runtime.prepare(root, 'amd64')
                expected = original.replace('http://azure.archive.ubuntu.com/ubuntu', 'https://archive.ubuntu.com/ubuntu')
                self.assertEqual(source.read_text(), expected)
                config = (root / 'apt.conf.d/80workchord-ci').read_text()
                self.assertIn('Acquire::Retries "2"', config)
                self.assertIn('Acquire::https::Timeout "15"', config)
                self.assertIn('APT::Update::Error-Mode "any"', config)
                self.assertNotIn('AllowInsecure', config)
                apt_runtime.prepare(root, 'amd64')
                self.assertEqual(source.read_text(), expected)

    def test_arm_sources_use_ports_and_only_exact_azure_host_is_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'sources.list'
            source.write_text('deb https://azure.archive.ubuntu.com/ubuntu noble main\n'
                              'deb http://azure.archive.ubuntu.com.example/ubuntu noble main\n')
            apt_runtime.prepare(root, 'arm64')
            self.assertEqual(source.read_text(), 'deb https://ports.ubuntu.com/ubuntu-ports noble main\n'
                             'deb http://azure.archive.ubuntu.com.example/ubuntu noble main\n')

    def test_unsupported_architecture_does_not_mutate_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                apt_runtime.prepare(Path(directory), 'unknown')
            self.assertEqual(list(Path(directory).iterdir()), [])
