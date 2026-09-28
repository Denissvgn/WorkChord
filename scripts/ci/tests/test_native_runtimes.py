"""Native orchestration preserves isolation, real result requirements and cleanup."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import Mock, patch

import yaml

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parents[1]
sys.path.insert(0, str(SCRIPTS))
import postgres_runtime
import run_android_checks as android
import run_disposable_checks as checks


class WorkflowContracts(unittest.TestCase):
    def test_android_cleartext_is_restricted_to_debug_loopback_hosts(self):
        root = REPO / 'android-companion/app/src'
        main = ET.parse(root / 'main/res/xml/network_security_config.xml').getroot()
        self.assertEqual(main.find('base-config').attrib['cleartextTrafficPermitted'], 'false')
        self.assertEqual(main.findall('domain-config'), [])
        debug = ET.parse(root / 'debug/res/xml/network_security_config.xml').getroot()
        self.assertEqual(debug.find('base-config').attrib['cleartextTrafficPermitted'], 'false')
        self.assertEqual({domain.text for domain in debug.findall('domain-config/domain')}, {'10.0.2.2', '127.0.0.1', 'localhost'})
        self.assertTrue(all(domain.attrib['includeSubdomains'] == 'false' for domain in debug.findall('domain-config/domain')))

    def test_automatic_workflows_do_not_pull_or_build_images(self):
        for path in (REPO / '.github/workflows').glob('*.yml'):
            document = yaml.safe_load(path.read_text())
            triggers = document.get('on', document.get(True, {}))
            if not any(name in triggers for name in ('pull_request', 'push', 'pull_request_target')):
                continue
            for job in document['jobs'].values():
                self.assertNotIn('services', job, str(path))
                self.assertNotIn('container', job, str(path))
                for step in job['steps']:
                    self.assertFalse(step.get('uses', '').startswith('docker://'))
                    script = step.get('run', '')
                    self.assertNotIn('accept_self_hosted.sh', script)
                    self.assertNotRegex(script, r'docker\s+(?:build|pull|run|create)\b')
        action = yaml.safe_load((REPO / '.github/actions/native-postgres/action.yml').read_text())
        self.assertEqual(action['runs']['using'], 'composite')
        self.assertTrue(all('docker' not in step.get('run', '') for step in action['runs']['steps']))

    def test_deployment_acceptance_remains_explicit_and_checks_twice(self):
        document = yaml.safe_load((REPO / '.github/workflows/deployment-acceptance.yml').read_text())
        self.assertEqual(set(document.get('on', document.get(True))), {'workflow_dispatch'})
        steps = document['jobs']['server-acceptance']['steps']
        self.assertEqual(sum(step.get('run', '').count('./scripts/server/accept_self_hosted.sh') for step in steps), 2)
        self.assertTrue(any(step.get('if') == 'always()' and 'down' in step.get('run', '') for step in steps))

    def test_all_workflow_and_composite_scripts_parse_as_bash(self):
        paths = list((REPO / '.github/workflows').glob('*.yml')) + list((REPO / '.github/actions').glob('*/action.yml'))
        for path in paths:
            document = yaml.safe_load(path.read_text())
            groups = document.get('jobs', {'composite': document.get('runs', {})}).values()
            for group in groups:
                for step in group.get('steps', []):
                    script = step.get('run')
                    if script:
                        result = subprocess.run(['bash', '-n'], input=script, text=True, capture_output=True)
                        self.assertEqual(result.returncode, 0, f'{path}: {result.stderr}')


class NativeChecks(unittest.TestCase):
    def test_connection_parameters_cannot_override_the_loopback_host(self):
        for url in ('postgresql://fixture@127.0.0.1/postgres?host=remote.example',
                    'postgresql://fixture@localhost/production', 'https://localhost/postgres'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                checks.validate_admin_url(url)
        checks.validate_admin_url('postgresql+psycopg://fixture@127.0.0.1:55432/postgres')

    def test_service_cleanup_reaps_exited_processes_and_escalates_timeouts(self):
        process = Mock(pid=123)
        with patch.object(checks.os, 'killpg', side_effect=ProcessLookupError):
            self.assertTrue(checks.stop_process_group(process))
        process.wait.assert_called_once_with(timeout=15)
        process = Mock(pid=123)
        process.wait.side_effect = [subprocess.TimeoutExpired('fixture', 15), 0]
        with patch.object(checks.os, 'killpg') as kill:
            self.assertFalse(checks.stop_process_group(process))
            self.assertEqual([call.args[1] for call in kill.call_args_list], [checks.signal.SIGTERM, checks.signal.SIGKILL])

    def test_application_secrets_are_not_inherited(self):
        with patch.dict(os.environ, {'PATH': '/tools', 'HOME': '/user', 'DATABASE_URL': 'production',
            'OIDC_CLIENT_SECRET': 'private', 'VITE_PRIVATE_KEY': 'private',
            'POSTGRES_ADMIN_URL': 'postgresql://fixture@localhost/postgres'}, clear=True):
            environment = checks.runtime_environment()
        self.assertNotIn('DATABASE_URL', environment)
        self.assertNotIn('OIDC_CLIENT_SECRET', environment)
        self.assertNotIn('VITE_PRIVATE_KEY', environment)
        self.assertEqual(environment['HOME'], '/user')
        self.assertIn('localhost', environment['NO_PROXY'])

    def run_backend(self, *, write_results, remote=False):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'results'
            calls = []
            def execute(argv, **kwargs):
                calls.append(argv)
                self.assertNotIn('docker', argv)
                if write_results:
                    for value in argv:
                        if str(value).startswith('--junitxml='):
                            Path(str(value).partition('=')[2]).write_text('<testsuite tests="3" failures="0" errors="0" skipped="0"/>')
                return subprocess.CompletedProcess(argv, 0)
            environment = {'POSTGRES_ADMIN_URL': 'postgresql://fixture@' + ('remote.example' if remote else '127.0.0.1') + '/postgres'}
            with patch.dict(os.environ, environment), patch.object(sys, 'argv', ['checks', '--backend-only', '--output', str(output)]), \
                 patch.object(checks, 'source_digest', return_value='unchanged'), \
                 patch.object(subprocess, 'check_output', return_value='revision\n'), patch.object(subprocess, 'run', side_effect=execute):
                result = checks.main()
            return result, json.loads((output / 'receipt.json').read_text()), calls

    def test_empty_results_cannot_be_reported_as_success(self):
        code, receipt, _ = self.run_backend(write_results=False)
        self.assertEqual(code, 1)
        self.assertEqual(receipt['status'], 'failed')
        self.assertEqual(len(receipt['artifact_errors']), 2)

    def test_both_database_results_are_required_and_recorded(self):
        code, receipt, calls = self.run_backend(write_results=True)
        self.assertEqual(code, 0)
        self.assertEqual(set(receipt['junit']), {'sqlite.xml', 'postgresql.xml'})
        self.assertEqual(receipt['environment'], 'native-processes')
        self.assertEqual(len([argv for argv in calls if 'pytest' in argv]), 2)

    def test_remote_database_is_rejected_before_any_command(self):
        code, receipt, calls = self.run_backend(write_results=True, remote=True)
        self.assertEqual(code, 1)
        self.assertIn('loopback', receipt['error'])
        self.assertEqual(calls, [])


class PostgresOwnership(unittest.TestCase):
    def test_unowned_cluster_cannot_be_stopped(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(subprocess, 'run') as run:
            with patch.object(sys, 'argv', ['pg', 'stop', '--data-dir', directory, '--bin-dir', '/tools']), self.assertRaises(SystemExit):
                postgres_runtime.main()
            run.assert_not_called()

    def test_start_uses_builtin_locale_and_removes_password_file(self):
        with tempfile.TemporaryDirectory() as directory:
            data = Path(directory) / 'new cluster'
            calls = []
            def execute(argv, **kwargs):
                calls.append(argv)
                if Path(argv[0]).name == 'initdb':
                    data.mkdir()
                    password = Path(next(value.split('=', 1)[1] for value in argv if value.startswith('--pwfile=')))
                    self.assertEqual(password.stat().st_mode & 0o777, 0o600)
                    self.assertEqual(password.read_text(), 'fixture-only\n')
                return subprocess.CompletedProcess(argv, 0)
            with patch.dict(os.environ, {'WORKCHORD_CI_POSTGRES_PASSWORD': 'fixture-only'}), \
                 patch.object(sys, 'argv', ['pg', 'start', '--data-dir', str(data), '--bin-dir', '/tools']), \
                 patch.object(subprocess, 'check_output', return_value='postgres (PostgreSQL) 18.4 (Ubuntu package)'), \
                 patch.object(subprocess, 'run', side_effect=execute):
                self.assertEqual(postgres_runtime.main(), 0)
            self.assertIn('--locale-provider=builtin', calls[0])
            self.assertIn('--builtin-locale=PG_UNICODE_FAST', calls[0])
            self.assertTrue((data / postgres_runtime.MARKER).is_file())
            self.assertEqual(list(Path(directory).glob('workchord-pg-password-*')), [])


class AndroidArtifacts(unittest.TestCase):
    def check_run(self, *, results=True, apk=True, gradle_code=0, skip_release=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'android-companion'
            wrapper = project / 'gradle/wrapper'
            wrapper.mkdir(parents=True)
            shutil.copyfile(REPO / 'android-companion/gradle/wrapper/gradle-wrapper.jar', wrapper / 'gradle-wrapper.jar')
            (project / 'gradlew').write_text('fixture wrapper')
            sdk = root / 'sdk'
            (sdk / 'platforms/android-34').mkdir(parents=True)
            (sdk / 'platforms/android-34/android.jar').write_bytes(b'fixture')
            (sdk / 'build-tools/34.0.0').mkdir(parents=True)
            output = root / 'results'
            def execute(argv, **kwargs):
                self.assertNotIn('docker', argv)
                self.assertIn('testDebugUnitTest', argv)
                self.assertIn('testReleaseUnitTest', argv)
                self.assertIn('assembleDebug', argv)
                cwd = Path(kwargs['cwd'])
                if results:
                    for variant in ('Debug', 'Release'):
                        xml = cwd / f'app/build/test-results/test{variant}UnitTest/TEST-fixture.xml'
                        xml.parent.mkdir(parents=True)
                        skipped = int(skip_release and variant == 'Release')
                        xml.write_text(f'<testsuite tests="1" failures="0" errors="0" skipped="{skipped}"/>')
                if apk:
                    artifact = cwd / 'app/build/outputs/apk/debug/app-debug.apk'
                    artifact.parent.mkdir(parents=True)
                    artifact.write_bytes(b'fixture apk')
                return subprocess.CompletedProcess(argv, gradle_code)
            def stdout(argv, **kwargs):
                return 'openjdk version "17.0.16"\n' if '-version' in argv else 'revision\n'
            with patch.dict(os.environ, {'ANDROID_HOME': str(sdk)}), patch.object(android, 'ROOT', root), \
                 patch.object(android, 'source_digest', return_value='unchanged'), \
                 patch.object(sys, 'argv', ['android', '--output', str(output)]), \
                 patch.object(subprocess, 'run', side_effect=execute), patch.object(subprocess, 'check_output', side_effect=stdout):
                code = android.main()
            return code, json.loads((output / 'receipt.json').read_text())

    def test_native_gradle_keeps_results_and_apk(self):
        code, receipt = self.check_run()
        self.assertEqual(code, 0)
        self.assertEqual(receipt['junit']['tests'], 2)
        self.assertFalse(receipt['integration_coverage'])
        self.assertIn('apk/app-debug.apk', receipt['artifacts'])

    def test_missing_outputs_and_failed_gradle_do_not_pass(self):
        for options in ({'results': False}, {'apk': False}, {'gradle_code': 1}, {'skip_release': True}):
            with self.subTest(options=options):
                code, receipt = self.check_run(**options)
                self.assertEqual(code, 1)
                self.assertEqual(receipt['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
