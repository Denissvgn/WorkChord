"""Exercise cancellation, deadlines and durable command results with real processes."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ci_runtime import RunReceipt, stop_process_group


class CommandLifecycle(unittest.TestCase):
    def test_darwin_permission_probe_requires_confirmed_group_absence(self):
        process = Mock(pid=177)
        process.poll.return_value = 0
        with patch('ci_runtime.sys.platform', 'darwin'), patch('ci_runtime.os.killpg', side_effect=PermissionError()), patch('ci_runtime.subprocess.run', return_value=Mock(stdout='', returncode=0)):
            self.assertTrue(stop_process_group(process))
        with patch('ci_runtime.sys.platform', 'darwin'), patch('ci_runtime.os.killpg', side_effect=PermissionError()), patch('ci_runtime.subprocess.run', return_value=Mock(stdout='177 S\n', returncode=0)):
            with self.assertRaises(PermissionError):
                stop_process_group(process)

    def test_running_receipt_exists_before_command_and_success_is_finalized(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'results'
            with RunReceipt(output, checks=['fixture'], timeout_seconds=10) as run:
                run.run('inspect', [sys.executable, '-c',
                    'import json,sys; r=json.load(open(sys.argv[1])); '
                    'assert r["status"]=="running"; '
                    'assert r["current_stage"]=="inspect"; print("live output",flush=True)',
                    str(output / 'receipt.json')], cwd=directory, env=os.environ.copy(), timeout=5)
            receipt = json.loads((output / 'receipt.json').read_text())
            self.assertEqual(run.exit_code, 0)
            self.assertEqual(receipt['status'], 'passed')
            self.assertEqual(receipt['commands'][0]['status'], 'passed')
            self.assertGreater(receipt['commands'][0]['duration_seconds'], 0)
            self.assertIn('live output', (output / 'inspect.log').read_text())

    def test_failure_cannot_be_hidden_by_continue_after_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with RunReceipt(Path(directory) / 'results', checks=['fixture'], timeout_seconds=10) as run:
                run.run('bad', [sys.executable, '-c', 'raise SystemExit(7)'],
                        cwd=directory, env=os.environ.copy(), timeout=5, check=False)
            self.assertEqual(run.data['status'], 'failed')
            self.assertEqual(run.data['commands'][0]['exit_code'], 7)

    def test_timeout_kills_descendants_even_when_the_parent_exits_on_term(self):
        with tempfile.TemporaryDirectory() as directory:
            pid_file = Path(directory) / 'child.pid'
            program = ('import subprocess,sys,time; '
                       'p=subprocess.Popen([sys.executable,"-c",'
                       '"import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(60)"]); '
                       'open(sys.argv[1],"w").write(str(p.pid)); time.sleep(60)')
            with RunReceipt(Path(directory) / 'results', checks=['fixture'],
                            timeout_seconds=10, cleanup_grace=0.2) as run:
                run.run('hang', [sys.executable, '-c', program, str(pid_file)],
                        cwd=directory, env=os.environ.copy(), timeout=0.6)
            self.assertEqual(run.data['status'], 'timed_out')
            self.assertEqual(run.data['commands'][0]['status'], 'timed_out')
            pid = int(pid_file.read_text())
            state = subprocess.run(['ps', '-o', 'stat=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
            self.assertTrue(not state or state.startswith('Z'), state)

    def test_service_descendants_that_exit_on_term_are_cleaned_successfully(self):
        with tempfile.TemporaryDirectory() as directory:
            ready = Path(directory) / 'ready'
            program = ('import subprocess,sys,time; '
                       'subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"]); '
                       'open(sys.argv[1],"w").write("ready"); time.sleep(60)')
            with RunReceipt(Path(directory) / 'results', checks=['fixture'], timeout_seconds=10, cleanup_grace=0.5) as run:
                run.start('service', [sys.executable, '-c', program, str(ready)], cwd=directory, env=os.environ.copy())
                deadline = time.monotonic() + 5
                while not ready.exists() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(ready.exists())
            self.assertEqual(run.data['status'], 'passed', run.data.get('cleanup_errors'))
            self.assertEqual(run.data['commands'][0]['status'], 'stopped')

    def test_job_budget_limits_a_longer_command_deadline(self):
        with tempfile.TemporaryDirectory() as directory:
            with RunReceipt(Path(directory) / 'results', checks=['fixture'],
                            timeout_seconds=0.2, cleanup_grace=0.1) as run:
                run.run('hang', [sys.executable, '-c', 'import time; time.sleep(60)'],
                        cwd=directory, env=os.environ.copy(), timeout=60)
            self.assertEqual(run.data['status'], 'timed_out')
            self.assertLess(run.data['duration_seconds'], 5)

    def test_sigterm_persists_cancellation_and_stops_active_command(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            program = '''
import os,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from ci_runtime import RunReceipt, stop_process_group
with RunReceipt(Path(sys.argv[2])/'results',checks=['fixture'],timeout_seconds=20,cleanup_grace=0.2) as run:
    run.run('active',[sys.executable,'-c','import time,sys; open(sys.argv[1],"w").write("ready"); time.sleep(60)',str(Path(sys.argv[2])/'ready')],cwd=sys.argv[2],env=os.environ.copy(),timeout=15)
raise SystemExit(run.exit_code)
'''
            process = subprocess.Popen([sys.executable, '-c', program, str(Path(__file__).resolve().parents[1]), directory],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            try:
                deadline = time.monotonic() + 10
                while not (root / 'ready').exists() and time.monotonic() < deadline:
                    if process.poll() is not None:
                        self.fail(process.stderr.read().decode())
                    time.sleep(0.02)
                self.assertTrue((root / 'ready').exists())
                process.send_signal(signal.SIGTERM)
                self.assertEqual(process.wait(timeout=5), 143)
                receipt = json.loads((root / 'results/receipt.json').read_text())
                self.assertEqual(receipt['status'], 'cancelled')
                self.assertEqual(receipt['commands'][0]['status'], 'cancelled')
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)
                process.stderr.close()

    def test_elapsed_setup_reduces_work_budget(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'WORKCHORD_CI_DEADLINE_EPOCH': str(time.time() - 1)}):
            with RunReceipt(Path(directory) / 'results', checks=['fixture'], timeout_seconds=60) as run:
                run.check_budget()
            self.assertEqual(run.data['status'], 'timed_out')
            self.assertEqual(run.data['commands'], [])
            self.assertEqual(run.data['work_budget_seconds'], 0)

    def test_hard_kill_leaves_an_incomplete_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'results'
            program = """
import os,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from ci_runtime import RunReceipt, stop_process_group
with RunReceipt(Path(sys.argv[2]),checks=['fixture'],timeout_seconds=60) as run:
    run.run('active',[sys.executable,'-c','import time; time.sleep(60)'],cwd=sys.argv[2],env=os.environ.copy(),timeout=55)
"""
            process = subprocess.Popen([sys.executable, '-c', program, str(Path(__file__).resolve().parents[1]), str(output)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            child_pid = None
            try:
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    if (output / 'receipt.json').exists():
                        receipt = json.loads((output / 'receipt.json').read_text())
                        if receipt['commands'] and receipt['commands'][0].get('pid'):
                            child_pid = receipt['commands'][0]['pid']
                            break
                    time.sleep(0.02)
                self.assertIsNotNone(child_pid)
                process.kill()
                process.wait(timeout=5)
                receipt = json.loads((output / 'receipt.json').read_text())
                self.assertEqual(receipt['status'], 'running')
                self.assertEqual(receipt['commands'][0]['status'], 'running')
            finally:
                if child_pid:
                    try:
                        os.killpg(child_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)
                process.stderr.close()

    def test_receipt_survives_cleanup_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            with RunReceipt(Path(directory) / 'results', checks=['fixture'], timeout_seconds=10) as run:
                run.cleanups.append(lambda: (_ for _ in ()).throw(RuntimeError('cleanup failed')))
            self.assertEqual(run.data['status'], 'failed')
            self.assertIn('cleanup failed', run.data['cleanup_errors'][0])
            self.assertTrue((Path(directory) / 'results/receipt.json').is_file())


if __name__ == '__main__':
    unittest.main()
