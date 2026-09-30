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
