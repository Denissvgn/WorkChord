import assert from 'node:assert/strict';
import { readFile, writeFile, mkdtemp, rm } from 'node:fs/promises';
import { join, isAbsolute } from 'node:path';
import { tmpdir } from 'node:os';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { chromium } from 'playwright';
const baseURL = process.env.BROWSER_BASE_URL;
const artifacts = process.env.BROWSER_ARTIFACTS_DIR;
const python = process.env.WORKCHORD_BROWSER_PYTHON;
const source = process.env.WORKCHORD_BROWSER_SOURCE_ROOT;
const nonce = process.env.WORKCHORD_FIXTURE_NONCE;
if (baseURL !== 'http://localhost:4173' || !nonce || !isAbsolute(python || '') || !isAbsolute(source || '')) throw new Error('Owned local runtime required');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ baseURL });
const page = await context.newPage();
const pageErrors = []; page.on('pageerror', error => pageErrors.push(error.message));
const privateState = await mkdtemp(join(tmpdir(), 'workchord-measurement-session-'));
try {
  for (let attempt = 0; attempt < 90; attempt++) {
    try { if ((await context.request.get('/api/auth/me', { timeout: 1000 })).ok()) break; } catch { }
    if (attempt === 89) throw new Error('Owned fixture unavailable');
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  await page.goto('/my-work');
  await page.getByRole('link', { name: 'Sign in', exact: true }).click();
  await page.getByRole('link', { name: 'Continue as Alice', exact: true }).click();
  await page.getByText('Alice', { exact: true }).first().waitFor();
  const proof = await context.request.get('/api/auth/me');
  assert.equal(proof.headers()['x-workchord-fixture'], nonce);
  assert.equal((await proof.json()).authenticated, true);
  const seeded = await context.request.get('/api/tasks/1/_fixture/dataset', { headers: { 'X-Fixture-Key': nonce } });
  assert.equal(seeded.status(), 200);
  const counts = await seeded.json(); assert.equal(counts.actual_task_count, 3009);
  const operations = ['/api/tasks/lookup?iteration_id=1&limit=100', '/api/tasks/9/detail?children_after_id=2560', 'bounded_polling_window',
    '/api/projects/portfolio-summaries/page?limit=100', '/api/tasks/delivery-metrics?iteration_id=3', '/api/iterations/3/tasks',
    '/api/team-member-profiles/1/capacity?start=2026-01-01&end=2026-02-01', '/api/agent/me/work', '/api/agent/me/claims',
    '/api/agent/capabilities', '/api/tasks/delivery-metrics?project_id=1', '/api/iterations/1/tasks'];
  const declaration = { fixture: nonce, declared_before_measurement: true, concurrency: [1, 5, 10], rounds: 3, operations,
    datasets: { ...counts, transport: 'HTTP over native SQLite fixture; distinct from PostgreSQL direct service', running_agent_runs: 0 },
    polling_window: { retained_pages: 4, head_refresh: 1, request_max_per_refresh: 5, page_limit: 100 },
    expected_boundary_rejections: ['collection_limit_exceeded'], unexpected_error_budget: 0,
    latency_budget_ms: { read_p95: 2000, request_max: 10000 } };
  const declarationPath = join(artifacts, 'http-workload-declaration.json');
  await writeFile(declarationPath, JSON.stringify(declaration, null, 2), { flag: 'wx' });
  const state = join(privateState, 'session.json'); await context.storageState({ path: state });
  await page.close();
  const command = await promisify(execFile)(python, ['-m', 'scripts.load.local_baseline', '--base-url', baseURL,
    '--nonce', nonce, '--session-state', state, '--declaration', declarationPath, '--output', join(artifacts, 'http-workset.json')],
    { cwd: source, env: { ...process.env, PYTHONPATH: source + '/backend:' + source }, timeout: 180000 });
  await writeFile(join(artifacts, 'http-measurement.log'), command.stdout + command.stderr, { flag: 'wx' });
  const result = JSON.parse(await readFile(join(artifacts, 'http-workset.json'), 'utf8'));
  assert.equal(result.status, 'passed'); assert.equal(result.samples, 576);
  assert.equal(result.source_binding.before.sha256, result.source_binding.after.sha256);
  assert.deepEqual(pageErrors, []);
  await writeFile(join(artifacts, 'managed-browser.json'), JSON.stringify({ status: 'passed', pageErrors, browser: browser.version(), node: process.version,
    steps: ['Nonce-verified managed OIDC session', 'Separate cookie-free synthetic agent reads', 'Frozen 1/5/10 HTTP workload',
      'Stale contention rejection and independent restored readback', 'Controlled interruption and recovered detail'], realProviderPilot: false }, null, 2));
} finally { await rm(privateState, { recursive: true, force: true }); await browser.close(); }
