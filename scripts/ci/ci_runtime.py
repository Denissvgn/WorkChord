"""Bounded native commands with streamed logs and atomic progress receipts."""

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def positive_seconds(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError('A finite positive timeout is required')
    return number


class CommandTimeout(RuntimeError):
    pass


class RunCancelled(RuntimeError):
    pass


def stop_process_group(process, grace_seconds=3):
    """Terminate descendants as well as the leader, then reap the leader."""
    def alive():
        process.poll()  # Reap an exited leader before probing its group.
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            if sys.platform != 'darwin':
                raise
            # Darwin can deny a group probe after its last member exits. Confirm
            # absence through a read-only group inventory rather than treating
            # a permission error as successful termination.
            result = subprocess.run(['ps', '-ax', '-o', 'pgid=,stat='], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                fields = line.split()
                if len(fields) >= 2 and fields[0] == str(process.pid) and not fields[1].startswith(('Z', 'X')):
                    raise
            return False
        if sys.platform.startswith('linux') and Path('/proc').is_dir():
            # Orphan zombies retain a group ID until init reaps them, but no
            # longer execute or hold resources such as sockets and log pipes.
            unknown = False
            for path in Path('/proc').iterdir():
                if not path.name.isdigit():
                    continue
                try:
                    fields = (path / 'stat').read_text().rpartition(')')[2].split()
                    if int(fields[2]) == process.pid and fields[0] not in {'Z', 'X'}:
                        return True
                except FileNotFoundError:
                    continue
                except (OSError, ValueError, IndexError):
                    unknown = True
            return unknown
        return True

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        process.wait(timeout=3)
        return True
    except PermissionError:
        if alive():
            raise
        process.wait(timeout=3)
        return True
    deadline = time.monotonic() + grace_seconds
    while alive() and time.monotonic() < deadline:
        time.sleep(0.02)
    graceful = not alive()
    if not graceful:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=3)
    return graceful


def junit_counts(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == 'testsuite' else root.findall('testsuite')
    counts = {key: sum(int(suite.get(key, 0)) for suite in suites)
              for key in ('tests', 'failures', 'errors', 'skipped')}
    counts['expected_failures'] = len(root.findall(".//skipped[@type='pytest.xfail']"))
    if (any(value < 0 for value in counts.values()) or counts['tests'] <= counts['skipped']
            or counts['failures'] or counts['errors']):
        raise ValueError(f'{path.name}: expected successful executed results')
    return counts


class RunReceipt:
    """Own a bounded run; a killed process leaves a durable incomplete receipt."""

    def __init__(self, output, *, checks, timeout_seconds, cleanup_grace=3):
        self.output = Path(output).resolve()
        if self.output.exists() and any(self.output.iterdir()):
            raise ValueError('Output must be a new or empty directory')
        self.output.mkdir(parents=True, exist_ok=True)
        self.started = time.monotonic()
        budget = positive_seconds(timeout_seconds)
        deadline_epoch = os.environ.get('WORKCHORD_CI_DEADLINE_EPOCH')
        if deadline_epoch is not None:
            budget = min(budget, max(0, positive_seconds(deadline_epoch) - time.time()))
        self.deadline = self.started + budget
        self.cleanup_grace = positive_seconds(cleanup_grace)
        self.cancel_signal = None
        self.services = []
        self.cleanups = []
        self.validators = []
        self.finalizers = []
        self.handlers = {}
        self.data = {'schema_version': 2, 'status': 'running', 'checks': list(checks),
                     'environment': 'native-processes', 'started_at': timestamp(),
                     'current_stage': 'initializing', 'commands': [], 'work_budget_seconds': budget}
        self.checkpoint()

    def checkpoint(self):
        self.data['updated_at'] = timestamp()
        self.data['duration_seconds'] = round(time.monotonic() - self.started, 3)
        temporary = self.output / '.receipt.tmp'
        temporary.write_text(json.dumps(self.data, indent=2) + '\n')
        os.replace(temporary, self.output / 'receipt.json')

    def __enter__(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.handlers[sig] = signal.signal(sig, self._cancel)
        return self

    def _cancel(self, signum, _frame):
        self.cancel_signal = self.cancel_signal or signum

    def check_budget(self):
        if self.cancel_signal:
            raise RunCancelled(f'Cancelled by signal {self.cancel_signal}')
        if time.monotonic() >= self.deadline:
            raise CommandTimeout('Run time budget exhausted')

    def _interrupted_status(self, error):
        if self.cancel_signal or isinstance(error, (RunCancelled, KeyboardInterrupt)):
            return 'cancelled'
        if isinstance(error, CommandTimeout):
            return 'timed_out'
        return 'failed'

    def _command(self, label, command, kind):
        self.check_budget()
        record = {'label': label, 'argv': [str(item) for item in command],
                  'kind': kind, 'status': 'running', 'started_at': timestamp(),
                  'duration_seconds': 0, 'log': f'{label}.log'}
        self.data['commands'].append(record)
        self.data['current_stage'] = label
        self.checkpoint()
        print(f'[{label}] starting', flush=True)
        return record

    def run(self, label, command, *, cwd, env, timeout, check=True):
        record = self._command(label, command, 'command')
        started = time.monotonic()
        deadline = min(self.deadline, started + positive_seconds(timeout))
        record['timeout_seconds'] = max(0, round(deadline - started, 3))
        heartbeat = started + 30
        process = None
        selector = selectors.DefaultSelector()
        try:
            with (self.output / record['log']).open('wb') as log:
                process = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, start_new_session=True)
                record['pid'] = process.pid
                self.checkpoint()
                os.set_blocking(process.stdout.fileno(), False)
                selector.register(process.stdout, selectors.EVENT_READ)
                while selector.get_map() or process.poll() is None:
                    self.check_budget()
                    if time.monotonic() >= deadline:
                        raise CommandTimeout(f'{label} exceeded its command timeout')
                    for service, entry, _handle, _started in self.services:
                        if service.poll() is not None:
                            raise RuntimeError(f"{entry['label']} exited unexpectedly ({service.returncode})")
                    for key, _ in selector.select(timeout=0.1):
                        chunk = os.read(key.fileobj.fileno(), 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        log.write(chunk)
                        log.flush()
                        if hasattr(sys.stdout, 'buffer'):
                            sys.stdout.buffer.write(chunk)
                            sys.stdout.buffer.flush()
                        else:
                            sys.stdout.write(chunk.decode(errors='replace'))
                            sys.stdout.flush()
                    if time.monotonic() >= heartbeat:
                        print(f'[{label}] still running ({time.monotonic() - started:.0f}s)', flush=True)
                        record['duration_seconds'] = round(time.monotonic() - started, 3)
                        self.checkpoint()
                        heartbeat = time.monotonic() + 30
                record['exit_code'] = process.wait(timeout=3)
                if not stop_process_group(process, self.cleanup_grace):
                    raise RuntimeError(f'{label} left descendants requiring forced cleanup')
                record['status'] = 'passed' if process.returncode == 0 else 'failed'
                if check and process.returncode:
                    raise RuntimeError(f'{label} failed with exit code {process.returncode}')
                return process.returncode
        except BaseException as error:
            record['status'] = self._interrupted_status(error)
            record['error'] = str(error)
            # Persist interruption before attempting cleanup.
            self.data['status'] = record['status']
            self.data['error'] = str(error)
            self.checkpoint()
            if process is not None:
                try:
                    record['cleanup_graceful'] = stop_process_group(process, self.cleanup_grace)
                    record['exit_code'] = process.returncode
                except Exception as cleanup_error:
                    self.data.setdefault('cleanup_errors', []).append(str(cleanup_error))
            raise
        finally:
            selector.close()
            if process is not None and process.stdout is not None:
                process.stdout.close()
            record['finished_at'] = timestamp()
            record['duration_seconds'] = round(time.monotonic() - started, 3)
            self.checkpoint()
            print(f"[{label}] {record['status']} ({record['duration_seconds']:.1f}s)", flush=True)

    def start(self, label, command, *, cwd, env):
        record = self._command(label, command, 'service')
        handle = (self.output / record['log']).open('wb')
        try:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=handle,
                                       stderr=subprocess.STDOUT, start_new_session=True)
        except BaseException:
            handle.close()
            record['status'] = 'failed'
            self.checkpoint()
            raise
        self.services.append((process, record, handle, time.monotonic()))
        record['pid'] = process.pid
        self.checkpoint()
        return process

    def __exit__(self, error_type, error, _traceback):
        status = self._interrupted_status(error) if error is not None else 'passed'
        if error is not None:
            self.data['error'] = str(error)
        if self.cancel_signal:
            status = 'cancelled'
        elif status == 'passed' and time.monotonic() >= self.deadline:
            status = 'timed_out'
        self.data.update(status=status if status != 'passed' else 'running', current_stage='cleanup')
        self.checkpoint()
        cleanup_started = time.monotonic()
        try:
            for process, record, handle, started in reversed(self.services):
                try:
                    exited_early = process.poll() is not None
                    graceful = stop_process_group(process, self.cleanup_grace)
                    record.update(status='failed' if exited_early or not graceful else 'stopped',
                                  exit_code=process.returncode, finished_at=timestamp(),
                                  duration_seconds=round(time.monotonic() - started, 3))
                    if exited_early or not graceful:
                        self.data.setdefault('cleanup_errors', []).append(f"{record['label']}: unexpected exit or forced cleanup")
                except Exception as exc:
                    self.data.setdefault('cleanup_errors', []).append(str(exc))
                finally:
                    handle.close()
                    self.checkpoint()
            for callbacks, key in ((self.finalizers, 'artifact_errors'), (self.cleanups, 'cleanup_errors'),
                                   (self.validators, 'artifact_errors')):
                for callback in callbacks:
                    try:
                        callback()
                    except Exception as exc:
                        self.data.setdefault(key, []).append(str(exc))
                    self.checkpoint()
            if self.cancel_signal:
                status = 'cancelled'
            if status == 'passed' and (self.data.get('artifact_errors') or self.data.get('cleanup_errors')
                    or any(item['status'] == 'failed' for item in self.data['commands'])):
                status = 'failed'
            self.data['artifacts'] = {str(path.relative_to(self.output)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(self.output.rglob('*')) if path.is_file() and path.name not in {'receipt.json', '.receipt.tmp'}}
            self.data.update(status=status, current_stage='complete', finished_at=timestamp(),
                             cleanup_duration_seconds=round(time.monotonic() - cleanup_started, 3))
        finally:
            self.checkpoint()
            for sig, handler in self.handlers.items():
                signal.signal(sig, handler)
        print(f'{self.data["status"]}: {self.output}', flush=True)
        return error is None or isinstance(error, (Exception, KeyboardInterrupt))

    @property
    def exit_code(self):
        if self.data['status'] == 'passed':
            return 0
        if self.data['status'] == 'cancelled':
            return 128 + (self.cancel_signal or signal.SIGINT)
        return 1
