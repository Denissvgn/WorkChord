import { execFile } from 'node:child_process';
import { isAbsolute } from 'node:path';
import { promisify } from 'node:util';

export async function dispatchInbox() {
  const python = process.env.WORKCHORD_BROWSER_PYTHON;
  if (!python || !isAbsolute(python)) throw new Error('Inbox dispatch requires the harness absolute Python executable');
  if (!/^sqlite\+aiosqlite:\/\/\/.*\/workchord_test_browser\.db$/.test(process.env.DATABASE_URL || '') || !process.env.WORKCHORD_FIXTURE_NONCE) {
    throw new Error('Inbox dispatch requires the owned disposable database and nonce');
  }
  return promisify(execFile)(python, ['-m', 'app.cli.worker', '--once'], {
    env: { ...process.env, DATABASE_PROCESS_ROLE: 'delivery_worker', DATABASE_POOL_SIZE: '8', DATABASE_MAX_OVERFLOW: '2', OUTBOUND_DELIVERY_WORKER_ENABLED: 'true' },
    timeout: 30000,
  });
}

export async function backupBrowserDatabase() {
  const python = process.env.WORKCHORD_BROWSER_PYTHON;
  if (!isAbsolute(python || '') || !/^sqlite\+aiosqlite:\/\/\/.*\/workchord_test_browser\.db$/.test(process.env.DATABASE_URL || '')
      || !/^[0-9a-f]{32}$/.test(process.env.WORKCHORD_FIXTURE_NONCE || '')) throw new Error('Owned disposable restore inputs required');
  const script = `
import hashlib,json,os,sqlite3,tempfile
from pathlib import Path
from urllib.parse import quote
from tests.support.database import assert_safe_test_database_url
source=Path(assert_safe_test_database_url(os.environ['DATABASE_URL']).database).resolve(strict=True)
def rows(connection):
    result={}
    for (name,) in connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        quoted='"'+name.replace('"','""')+'"'
        result[name]=sorted(connection.execute('SELECT * FROM '+quoted).fetchall(),key=repr)
    return result
with tempfile.TemporaryDirectory(prefix='workchord-sqlite-restore-',dir=source.parent) as directory:
    target=Path(directory)/'workchord_test_restored.db'
    with sqlite3.connect('file:'+quote(str(source))+'?mode=ro',uri=True) as original:
        original.execute('BEGIN');before=rows(original)
        with sqlite3.connect(target) as restored: original.backup(restored)
        assert rows(original)==before
    with sqlite3.connect(target) as restored:
        after=rows(restored);assert before==after
        assert restored.execute('PRAGMA foreign_key_check').fetchall()==[]
        ledger=restored.execute('SELECT id,project_id,task_id,principal_id,minutes,version,voided FROM time_entries ORDER BY id').fetchall()
        revisions=restored.execute('SELECT entry_id,version,minutes,voided FROM time_entry_revisions ORDER BY entry_id,version').fetchall()
        assert ledger and revisions
    print(json.dumps({'status':'passed','full_catalog_equal':True,'tables':len(before),'allocation_state_equal':before.get('sqlite_sequence')==after.get('sqlite_sequence'),
        'ledger':ledger,'revisions':revisions,'independent_target':True,'synthetic':True}))
`;
  const result = await promisify(execFile)(python, ['-c', script], { env: process.env, timeout: 30000 });
  return result.stdout;
}
