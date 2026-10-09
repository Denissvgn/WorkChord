#!/usr/bin/env python3
"""Build Android with native JDK 17, SDK 34 and the checksum-pinned Gradle wrapper."""

import argparse
import hashlib
import os
import re
import shutil
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

from run_disposable_checks import ROOT, source_digest, bind_source
from ci_runtime import RunReceipt, positive_seconds
from android_qualification import load_inputs, Qualification


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--timeout-seconds', type=positive_seconds, default=1200)
    parser.add_argument('--release-qualification', action='store_true')
    parser.add_argument('--qualification-inputs', type=Path)
    args = parser.parse_args()
    if args.release_qualification != bool(args.qualification_inputs):
        parser.error('--release-qualification and --qualification-inputs must be selected together')
    output = args.output or Path(tempfile.mkdtemp(prefix='workchord-android-'))
    try:
        run = RunReceipt(output, checks=['android'], timeout_seconds=args.timeout_seconds)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    with run:
        bind_source(run, source_digest)
        run.data['integration_coverage'] = False
        workspace = tempfile.TemporaryDirectory(prefix='workchord-android-runtime-')
        run.cleanups.append(workspace.cleanup)
        project = Path(workspace.name) / 'project'
        shutil.copytree(ROOT / 'android-companion', project,
            ignore=shutil.ignore_patterns('build', '.gradle', '.idea', '.kotlin', 'local.properties', '.DS_Store'))
        env = os.environ.copy()
        env['GRADLE_USER_HOME'] = str(Path(workspace.name) / 'gradle-cache')
        java = Path(env['JAVA_HOME']) / 'bin/java' if env.get('JAVA_HOME') else Path('java')
        run.run('java-version', [str(java), '-version'], cwd=project, env=env, timeout=30)
        version = (run.output / 'java-version.log').read_text()
        if not re.search(r'version "17[.\"]', version):
            raise RuntimeError('JDK 17 is required')
        sdk = Path(env.get('ANDROID_HOME') or env.get('ANDROID_SDK_ROOT') or '')
        if not (sdk / 'platforms/android-34/android.jar').is_file() or not (sdk / 'build-tools/34.0.0').is_dir():
            raise RuntimeError('Install Android SDK platform 34 and build-tools 34.0.0')
        wrapper = project / 'gradle/wrapper/gradle-wrapper.jar'
        if hashlib.sha256(wrapper.read_bytes()).hexdigest() != 'cb0da6751c2b753a16ac168bb354870ebb1e162e9083f116729cec9c781156b8':
            raise RuntimeError('Gradle wrapper checksum mismatch')
        qualification = None
        if args.release_qualification:
            if not (sdk / 'licenses/android-sdk-license').is_file() or not (sdk / 'licenses/android-sdk-license').read_text().strip():
                raise RuntimeError('Provide an existing licensed SDK; this runner does not install components or accept terms')
            for tool in ('aapt2', 'apksigner'):
                if not (sdk / 'build-tools/34.0.0' / tool).is_file():
                    raise RuntimeError('The licensed SDK requires complete Build Tools 34.0.0')
            inputs = load_inputs(args.qualification_inputs, run.data['source_sha256'], run.data['revision'])
            qualification = Qualification(run, project, Path(workspace.name), env, inputs, sdk)
            qualification.prepare()
            browser = Path(workspace.name) / 'browser'
            browser.mkdir()
            shutil.copyfile(ROOT / 'scripts/ci/android_web_peer.mjs', browser / 'android_web_peer.mjs')
            run.run('qualification-browser-runtime', ['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', 'playwright@1.59.1'],
                    cwd=browser, env=env, timeout=180)
            env['PLAYWRIGHT_BROWSERS_PATH'] = str(Path(workspace.name) / 'browsers')
            run.run('qualification-browser-install', ['npx', '--no-install', 'playwright', 'install', 'chromium'],
                    cwd=browser, env=env, timeout=180)
            env['NODE_EXTRA_CA_CERTS'] = inputs['ca_file']
            env['WORKCHORD_QUALIFICATION_SPKI'] = inputs['tls_spki_sha256']
        def collect_results():
            for label, relative in (('unit-results', 'app/build/test-results/testDebugUnitTest'),
                                    ('release-unit-results', 'app/build/test-results/testReleaseUnitTest'),
                                    ('unit-report', 'app/build/reports/tests/testDebugUnitTest'),
                                    ('release-unit-report', 'app/build/reports/tests/testReleaseUnitTest'),
                                    ('apk', 'app/build/outputs/apk/debug')):
                if (project / relative).is_dir():
                    if not (run.output / label).exists():
                        shutil.copytree(project / relative, run.output / label)
        run.finalizers.append(collect_results)
        def validate_results():
            run.data['junit_variants'] = {}
            totals = {key: 0 for key in ('tests', 'failures', 'errors', 'skipped', 'expected_failures')}
            for directory in ('unit-results', 'release-unit-results'):
                files = list((run.output / directory).glob('TEST-*.xml'))
                if not files:
                    raise ValueError(f'Missing executed Android results: {directory}')
                # A variant may contain an individually skipped suite; validate the aggregate.
                counts = {key: 0 for key in totals}
                for path in files:
                    root = ET.parse(path).getroot()
                    for key in ('tests', 'failures', 'errors', 'skipped'):
                        counts[key] += int(root.get(key, 0))
                run.data['junit_variants'][directory] = counts
                if any(v < 0 for v in counts.values()) or counts['tests'] <= counts['skipped'] or counts['failures'] or counts['errors']:
                    raise ValueError(f'Android variant requires successful executed results: {directory}')
                for key in totals:
                    totals[key] += counts[key]
            run.data['junit'] = totals
            apks = list((run.output / 'apk').glob('*.apk'))
            if len(apks) != 1 or apks[0].stat().st_size <= 0:
                raise ValueError('Android requires one nonempty debug APK')
        run.validators.append(validate_results)
        run.data['toolchain'] = {'jdk': version.strip(), 'gradle': '8.7', 'agp': '8.5.2', 'compile_sdk': 34, 'build_tools': '34.0.0'}
        run.run('gradle', [str(project / 'gradlew'), '--no-daemon', '--max-workers=2',
            '--project-cache-dir', str(Path(workspace.name) / 'gradle-project-cache'),
            'testDebugUnitTest', 'testReleaseUnitTest', 'assembleDebug',
            *(['assembleRelease', 'assembleReleaseAndroidTest'] if qualification else [])],
            cwd=project, env=env, timeout=1200)
        if qualification:
            qualification.exercise(collect_results)
    return run.exit_code


if __name__ == '__main__':
    raise SystemExit(main())
