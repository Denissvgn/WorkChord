"""Release-behavior qualification confined to an explicitly owned ARM64 emulator."""
import hashlib
import base64
import json
import os
from pathlib import Path
import platform
import re
import secrets
import ssl
import subprocess
import threading
import time
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPSHandler, HTTPRedirectHandler
import xml.etree.ElementTree as ET

APP = 'com.workchord.android'
TEST_APP = APP + '.test'
RUNNER = TEST_APP + '/androidx.test.runner.AndroidJUnitRunner'


def load_inputs(path, expected_source, expected_revision):
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Qualification inputs must be a versioned object')
    nonce = data.get('owner_nonce', '')
    if not re.fullmatch('[0-9a-f]{32}', nonce) or os.environ.get('WORKCHORD_ANDROID_QUALIFICATION_OWNER') != nonce:
        raise ValueError('Explicit environment ownership must match the input manifest')
    if not re.fullmatch('emulator-[0-9]{4,5}', data.get('device_serial', '')):
        raise ValueError('Only an explicitly selected disposable emulator is supported')
    if data.get('signing_mode') != 'disposable_qualification' or data.get('fresh_app_storage') is not True:
        raise ValueError('A fresh installation with disposable qualification signing is required')
    if data.get('source_sha256') != expected_source or data.get('candidate_revision') != expected_revision:
        raise ValueError('Qualification inputs do not identify the executing source')
    if not re.fullmatch('[0-9a-f]{32}', data.get('fixture_nonce', '')):
        raise ValueError('A fixture nonce is required')
    for field in ('api_origin', 'browser_origin', 'issuer_origin'):
        value = data.get(field, '')
        parsed = urlsplit(value)
        if (parsed.scheme != 'https' or parsed.hostname != 'localhost' or parsed.username or parsed.password
                or parsed.path not in ('', '/') or parsed.query or parsed.fragment or not parsed.port
                or not 1024 <= parsed.port <= 65535):
            raise ValueError('Owned qualification requires HTTPS localhost origins with explicit unprivileged ports')
        data[field] = value.rstrip('/')
    if data['api_origin'] != data['browser_origin']:
        raise ValueError('The native API and browser must use the same owned HTTPS origin')
    if type(data.get('fixture_parent_id')) is not int or data['fixture_parent_id'] <= 0:
        raise ValueError('A seeded relationship parent is required')
    if data.get('trust_mode') != 'owned_emulator_system_ca' or not re.fullmatch('[0-9a-f]{64}', data.get('ca_sha256', '')):
        raise ValueError('Trust must be provisioned only into the owned emulator system store')
    ca = Path(data.get('ca_file', '')).resolve(strict=True)
    if not ca.is_file() or not re.fullmatch(r'(?:/system/etc/security/cacerts|/apex/com.android.conscrypt/cacerts)/[0-9a-f]{8}\.0', data.get('emulator_ca_path', '')):
        raise ValueError('A public CA and exact system-store certificate path are required')
    digest = hashlib.sha256(ssl.PEM_cert_to_DER_cert(ca.read_text())).hexdigest()
    if digest != data['ca_sha256']:
        raise ValueError('CA fingerprint differs from qualification inputs')
    data['ca_file'] = str(ca)
    try:
        if len(base64.b64decode(data.get('tls_spki_sha256', ''), validate=True)) != 32:
            raise ValueError('A pinned fixture TLS public key is required for the owned browser')
    except (ValueError, TypeError) as error:
        raise ValueError('A pinned fixture TLS public key is required for the owned browser') from error
    if platform.machine().lower() not in {'arm64', 'aarch64'}:
        raise ValueError('Release qualification requires a native ARM64 host')
    return data


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Qualification fixture redirects are not allowed')


def fixture_probe(data):
    opener = build_opener(HTTPSHandler(context=ssl.create_default_context(cafile=data['ca_file'])), NoRedirect())
    def read(origin, path, nonce=True):
        with opener.open(origin + path, timeout=5) as response:
            if nonce and response.headers.get('X-WorkChord-Fixture') != data['fixture_nonce']:
                raise ValueError('Fixture nonce differs; no writes or installs are allowed')
            return json.load(response)
    read(data['api_origin'], '/api/auth/me')
    capabilities = read(data['api_origin'], '/api/tasks/capabilities')
    if capabilities.get('ready') is not True: raise ValueError('The owned fixture backfill must be ready')
    if capabilities.get('legacy_task_versions_required') is not True or capabilities.get('aggregate_revisions_required') is not True:
        raise ValueError('The owned fixture must enable strict mutation versions')
    discovery = read(data['issuer_origin'], '/.well-known/openid-configuration', False)
    if discovery.get('issuer') != data['issuer_origin'] or any(not str(discovery.get(field, '')).startswith(data['issuer_origin'] + '/')
            for field in ('authorization_endpoint', 'token_endpoint', 'jwks_uri')):
        raise ValueError('Only the owned synthetic HTTPS issuer is supported')
    return capabilities


def required_cases(project):
    result = []
    for name in ('CredentialIsolationTest', 'ReleaseBehaviorTest', 'LiveCompanionTest'):
        path = project / f'app/src/androidTest/java/com/workchord/android/{name}.kt'
        source = path.read_text()
        methods = re.findall(r'@Test\s+(?:@[^\n]+\s+)*fun\s+(\w+)\s*\(', source)
        if not methods: raise ValueError('Required instrumentation inventory is empty: ' + name)
        result += [(APP + '.' + name, method) for method in methods]
    return result


def executed_case(output, classname, method):
    events = []; current = {}
    for line in output.splitlines():
        if line.startswith('INSTRUMENTATION_STATUS: '):
            key, separator, value = line[len('INSTRUMENTATION_STATUS: '):].partition('=')
            if separator: current[key] = value
        elif line.startswith('INSTRUMENTATION_STATUS_CODE: '):
            code = int(line.split(':', 1)[1]); events.append((code, current)); current = {}
    matching = [code for code, values in events if values.get('class') == classname and values.get('test') == method]
    if matching != [1, 0] or any(code < 0 for code, _ in events) or not re.search(r'INSTRUMENTATION_CODE:\s*-1\s*$', output.strip()):
        raise ValueError('Missing, failed or skipped required instrumentation: ' + classname + '#' + method)
    return {'classname': classname, 'name': method}


def manifest_flags(text):
    result = {}
    for name in ('allowBackup', 'usesCleartextTraffic', 'debuggable'):
        match = re.search(r'android:' + name + r'(?:\([^)]*\))?\s*=\s*\(type 0x12\)0x([0-9a-f]+)', text)
        if match is None:
            if name == 'debuggable': result[name] = False; continue
            raise ValueError('Missing explicit release manifest policy: ' + name)
        result[name] = int(match.group(1), 16) != 0
    if any(result.values()): raise ValueError('Release artifact weakens network, backup or debugging policy')
    return result


class Qualification:
    def __init__(self, run, project, scratch, env, data, sdk):
        self.run, self.project, self.scratch, self.env, self.data = run, project, scratch, env, data
        self.adb = [str(sdk / 'platform-tools/adb'), '-s', data['device_serial']]
        self.tools = sdk / 'build-tools/34.0.0'; self.installed = {}; self.reversed = []
        self.cases = required_cases(project); self.executed = []
        self.controller_errors = []
        self.controller_stop = threading.Event()
        self.controller_thread = None
        run.cleanups.insert(0, self.cleanup)
        run.validators.append(self.validate_results)

    def adb_read(self, *args):
        return subprocess.check_output([*self.adb, *args], text=True, timeout=10).strip()

    def owner(self):
        if self.adb_read('shell', 'getprop', 'debug.workchord.qualification_owner') != self.data['owner_nonce']:
            raise ValueError('Selected emulator ownership changed')

    def prepare(self):
        self.owner()
        if not self.env.get('JAVA_HOME'):
            raise ValueError('Qualification requires an explicit native JDK 17 JAVA_HOME')
        for tool in (Path(self.adb[0]), self.tools/'aapt2', Path(self.env['JAVA_HOME'])/'bin/java'):
            details = subprocess.check_output(['file', '-L', str(tool)], text=True, timeout=10)
            if not re.search(r'arm64|aarch64|ARM aarch64', details):
                raise ValueError('Qualification requires native ARM64 SDK tools: ' + str(tool))
        self.env['ORG_GRADLE_PROJECT_android.aapt2FromMavenOverride'] = str(self.tools/'aapt2')
        if self.adb_read('shell','getprop','ro.kernel.qemu') != '1' or self.adb_read('shell','getprop','ro.product.cpu.abi') != 'arm64-v8a':
            raise ValueError('Only the owned native ARM64 emulator is supported')
        if int(self.adb_read('shell','getprop','ro.build.version.sdk')) < 33:
            raise ValueError('Every required scenario needs emulator API 33 or newer')
        pem = self.adb_read('shell','cat',self.data['emulator_ca_path'])
        if hashlib.sha256(ssl.PEM_cert_to_DER_cert(pem)).hexdigest() != self.data['ca_sha256']:
            raise ValueError('Owned emulator system trust differs from manifest')
        for package in (APP, TEST_APP):
            if self.adb_read('shell','pm','path',package):
                raise ValueError('Qualification refuses to overwrite existing application storage')
        for port in sorted({urlsplit(self.data[field]).port for field in ('api_origin','issuer_origin')}):
            if self.reverse_mapping(port) is not None: raise ValueError('An existing reverse mapping is not owned by this run')
            self.run.run('reverse-'+str(port),[*self.adb,'reverse','--no-rebind','tcp:'+str(port),'tcp:'+str(port)],cwd=self.project,env=self.env,timeout=15)
            self.reversed.append(port)
        fixture_probe(self.data)
        key = self.scratch / 'qualification.p12'
        self.env.update(WORKCHORD_ANDROID_RELEASE_QUALIFICATION='true',WORKCHORD_ANDROID_QUALIFICATION_KEYSTORE=str(key),
                        WORKCHORD_QUALIFICATION_KEY_PASSWORD=secrets.token_hex(32))
        java_home = Path(self.env['JAVA_HOME'])
        self.run.run('qualification-signing',[str(java_home/'bin/keytool'),'-genkeypair','-keystore',str(key),'-storetype','PKCS12',
            '-storepass:env','WORKCHORD_QUALIFICATION_KEY_PASSWORD','-keypass:env','WORKCHORD_QUALIFICATION_KEY_PASSWORD',
            '-alias','workchord-qualification','-keyalg','RSA','-keysize','2048','-validity','2','-dname','CN=WorkChord disposable qualification'],
            cwd=self.project,env=self.env,timeout=30)
        certificate=self.scratch/'qualification.der'
        self.run.run('qualification-public-certificate',[str(java_home/'bin/keytool'),'-exportcert','-keystore',str(key),
            '-storepass:env','WORKCHORD_QUALIFICATION_KEY_PASSWORD','-alias','workchord-qualification','-file',str(certificate)],
            cwd=self.project,env=self.env,timeout=30)
        self.certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest()

    def command(self, label, argv, timeout=30):
        self.owner(); self.run.run(label,argv,cwd=self.project,env=self.env,timeout=timeout)
        return (self.run.output/(label+'.log')).read_text()

    def installed_hash(self, package, label):
        path = self.adb_read('shell','pm','path',package)
        if not path.startswith('package:') or '\n' in path: raise ValueError('Expected one installed base APK')
        destination = self.scratch/(label+'.apk')
        subprocess.run([*self.adb,'pull',path[len('package:'):],str(destination)],check=True,stdout=subprocess.DEVNULL,timeout=30)
        return hashlib.sha256(destination.read_bytes()).hexdigest()

    def exercise(self, collect_results):
        collect_results()
        apks = list((self.project/'app/build/outputs/apk/release').glob('*.apk'))
        tests = list((self.project/'app/build/outputs/apk/androidTest/release').glob('*.apk'))
        if len(apks) != 1 or len(tests) != 1: raise ValueError('Exactly one release app and instrumentation APK is required')
        apk, test = apks[0], tests[0]; first = hashlib.sha256(apk.read_bytes()).hexdigest()
        self.command('release-rebuild',[str(self.project/'gradlew'),'--no-daemon','--max-workers=1','--no-build-cache','clean','assembleRelease','assembleReleaseAndroidTest'],600)
        if first != hashlib.sha256(apk.read_bytes()).hexdigest(): raise ValueError('Release artifact is not reproducible with the same source/toolchain/signing identity')
        flags = manifest_flags(self.command('manifest-inspection',[str(self.tools/'aapt2'),'dump','xmltree',str(apk),'--file','AndroidManifest.xml']))
        cert = self.command('certificate-inspection',[str(self.tools/'apksigner'),'verify','--verbose','--print-certs',str(apk)])
        fingerprints = re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]{64})',cert)
        if len(fingerprints) != 1 or fingerprints[0].lower()!=self.certificate_sha256: raise ValueError('Expected the generated qualification certificate')
        test_certificate=self.command('instrumentation-certificate-inspection',[str(self.tools/'apksigner'),'verify','--verbose','--print-certs',str(test)])
        if re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]{64})',test_certificate) != fingerprints:
            raise ValueError('Instrumentation and exact release APK must share the qualification certificate')
        self.run.data['release_artifact'] = {'sha256':first,'certificate_sha256':fingerprints[0].lower(),'signing_mode':'disposable_qualification',
            'manifest':flags,'reproducible_same_identity':True,'emulator':self.data['device_serial'],'physical_device_verified':False}
        import shutil
        shutil.copy2(apk,self.run.output/'release.apk');shutil.copy2(test,self.run.output/'release-instrumentation.apk')
        for package, path in ((APP,apk),(TEST_APP,test)):
            self.command('install-'+package,[*self.adb,'install','--no-streaming',str(path)],60)
            digest=hashlib.sha256(path.read_bytes()).hexdigest();self.installed[package]=digest
            if self.installed_hash(package,'installed-'+package) != digest: raise ValueError('Installed artifact differs from exact built APK')
        for index,(classname,method) in enumerate(self.cases):
            self.command('process-boundary-'+str(index),[*self.adb,'shell','am','force-stop',APP])
            thread=None
            self.controller_stop.clear()
            if method in ('networkInterruptionLocksCurrentWorkAndRecoversLocalInputs','actualWebEditorAndNativeDraftProduceRecoverableConflict'):
                thread=threading.Thread(target=self.controller,args=(method,),daemon=True);self.controller_thread=thread;thread.start()
            argv=[*self.adb,'shell','am','instrument','-w','-r','-e','class',classname+'#'+method,
                '-e','fixtureOrigin',self.data['api_origin'],'-e','browserOrigin',self.data['browser_origin'],
                '-e','fixtureNonce',self.data['fixture_nonce'],'-e','fixtureParentId',str(self.data['fixture_parent_id']),
                '-e','releaseQualification','true','-e','networkControl','enabled','-e','webPeerControl','enabled','-e','presentationControl','enabled',RUNNER]
            try:
                output=self.command('instrumentation-'+str(index),argv,150)
                if thread:thread.join(timeout=10)
            finally:
                self.stop_controller()
            if self.controller_errors: raise ValueError('Scenario controller failed: '+str(self.controller_errors))
            self.executed.append(executed_case(output,classname,method))
        self.command('instrumentation-artifacts', [*self.adb, 'pull', '/sdcard/Android/data/'+APP+'/files',
            str(self.run.output/'instrumentation-artifacts')], 60)
        self.run.data['integration_coverage']=True

    def marker(self, name, value=None):
        path='/sdcard/Android/data/'+APP+'/files/'+name
        if value is None:
            result=subprocess.run([*self.adb,'shell','cat',path],text=True,capture_output=True,timeout=5)
            return result.stdout.strip() if result.returncode==0 else ''
        if not re.fullmatch('[a-z0-9_]+',value):raise ValueError('Invalid control stage')
        self.owner();subprocess.run([*self.adb,'shell',f'printf %s {value} > {path}'],check=True,timeout=5)

    def await_marker(self,name,predicate,timeout=90):
        deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            if self.controller_stop.is_set():raise ValueError('Scenario controller cancelled')
            self.run.check_budget();value=self.marker(name)
            if predicate(value):return value
            self.controller_stop.wait(.2)
        raise ValueError('Required controlled stage did not arrive: '+name)

    def controller(self, method):
        try:
            if method.startswith('networkInterruption'):
                name='network-stage.txt';port=urlsplit(self.data['api_origin']).port
                self.await_marker(name,lambda value:value=='ready')
                self.remove_reverse(port)
                try:
                    self.marker(name,'offline');self.await_marker(name,lambda value:value=='observed_offline')
                finally:
                    if not self.controller_stop.is_set():
                        self.owner()
                        if self.reverse_mapping(port) is not None:raise ValueError('Reverse mapping changed while offline')
                        subprocess.run([*self.adb,'reverse','--no-rebind','tcp:'+str(port),'tcp:'+str(port)],check=True,timeout=10)
                self.marker(name,'restored');self.await_marker(name,lambda value:value=='done')
            else:
                value=self.await_marker('web-peer-stage.txt',lambda value:value.isdigit())
                fixture_probe(self.data)
                node=self.env.get('WORKCHORD_QUALIFICATION_NODE','node')
                from ci_runtime import stop_process_group
                argv=[node,str(self.scratch/'browser/android_web_peer.mjs'),self.data['browser_origin'],value,self.data['fixture_nonce']]
                log=self.run.output/'web-peer.log'
                with log.open('w') as handle:
                    process=subprocess.Popen(argv,cwd=self.project,env=self.env,stdout=handle,stderr=subprocess.STDOUT,start_new_session=True)
                    try:
                        deadline=time.monotonic()+90
                        while process.poll() is None and time.monotonic()<deadline:
                            if self.controller_stop.wait(.2):raise ValueError('Scenario controller cancelled')
                        if process.poll() != 0:raise ValueError('Owned browser peer failed')
                    finally:stop_process_group(process)
                self.run.data['web_peer_controller']={'status':'passed','argv':argv,'log':'web-peer.log'}
                self.marker('web-peer-stage.txt','saved')
        except Exception as error:self.controller_errors.append(str(error))

    def validate_results(self):
        if self.executed != [{'classname':c,'name':m} for c,m in self.cases]: raise ValueError('Every declared required instrumentation case must execute')
        root=ET.Element('testsuite',tests=str(len(self.executed)),failures='0',errors='0',skipped='0')
        for case in self.executed:ET.SubElement(root,'testcase',**case)
        ET.ElementTree(root).write(self.run.output/'instrumentation.xml',encoding='unicode')
        for directory in ('unit-results','release-unit-results'):
            for path in (self.run.output/directory).glob('TEST-*.xml'):
                if int(ET.parse(path).getroot().get('skipped',0)):raise ValueError('Required release unit variants cannot skip cases')

    def reverse_mapping(self, port):
        source = 'tcp:'+str(port)
        matches = []
        for row in self.adb_read('reverse','--list').splitlines():
            fields = row.split()
            if len(fields) != 3:
                raise ValueError('Reverse mapping inventory is malformed')
            if fields[1] == source:
                matches.append(fields[2])
        if len(matches) > 1:raise ValueError('Reverse mapping inventory is ambiguous')
        return matches[0] if matches else None

    def remove_reverse(self, port):
        self.owner()
        destination = self.reverse_mapping(port)
        if destination is None:return
        if destination != 'tcp:'+str(port):raise ValueError('Reverse mapping changed; refusing to remove unrelated mapping')
        subprocess.run([*self.adb,'reverse','--remove','tcp:'+str(port)],check=True,timeout=10)

    def stop_controller(self):
        self.controller_stop.set()
        if self.controller_thread:
            self.controller_thread.join(timeout=20)
            if self.controller_thread.is_alive():raise ValueError('Scenario controller did not stop; cleanup is held')
            self.controller_thread = None

    def cleanup(self):
        self.stop_controller()
        if not self.installed and not self.reversed:return
        self.owner()
        errors=[]
        for package,digest in list(self.installed.items()):
            try:
                if self.installed_hash(package,'cleanup-'+package) != digest:raise ValueError('Application changed; refusing to remove unrelated artifact')
                self.owner()
                subprocess.run([*self.adb,'uninstall',package],check=True,timeout=30,stdout=subprocess.DEVNULL)
                del self.installed[package]
            except Exception as error:errors.append(str(error))
        for port in list(self.reversed):
            try:
                self.remove_reverse(port)
                self.reversed.remove(port)
            except Exception as error:errors.append(str(error))
        if errors:raise ValueError('Owned cleanup incomplete: '+ '; '.join(errors))
