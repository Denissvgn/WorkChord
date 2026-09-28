import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { chromium } from 'playwright';

const baseURL = process.env.BROWSER_BASE_URL;
const artifacts = process.env.BROWSER_ARTIFACTS_DIR || '/artifacts';
if (!['http://localhost:4173', 'http://frontend:4173'].includes(baseURL)) throw new Error('Only the disposable frontend is allowed');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ baseURL, locale: 'en-US' });
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
try {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try {
      const projects = await context.request.get('/api/projects', { timeout: 1000 });
      if (projects.ok() && Array.isArray(await projects.json())) break;
      if (attempt === 59) throw new Error(`API not ready: ${projects.status()}`);
    } catch (error) {
      if (attempt === 59) throw error;
    }
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  if (process.env.WORKCHORD_FIXTURE_NONCE) {
    const fixture = await context.request.get('/api/auth/me');
    assert.equal(fixture.headers()['x-workchord-fixture'], process.env.WORKCHORD_FIXTURE_NONCE);
  }
  await page.goto('/projects');
  await page.getByRole('heading', { name: 'Projects', exact: true }).waitFor();
  await page.getByRole('link', { name: 'Orchard', exact: true }).waitFor();
  await page.getByRole('link', { name: 'Harbor', exact: true }).waitFor();
  const name = 'Browser delivery readback';
  await page.getByRole('button', { name: 'New Project', exact: true }).click();
  await page.getByRole('textbox', { name: 'Project Name', exact: true }).fill(name);
  const saved = page.waitForResponse(response => response.url().endsWith('/api/projects') && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Create Project', exact: true }).click();
  const response = await saved;
  assert.equal(response.status(), 201);
  const created = await response.json();
  assert.equal(created.name, name);
  const independent = await browser.newContext({ baseURL, locale: 'en-US' });
  const readback = await independent.request.get(`/api/projects/${created.id}`);
  assert.equal(readback.status(), 200);
  assert.equal((await readback.json()).name, name);
  const other = await independent.newPage();
  await other.goto('/projects');
  await other.getByRole('link', { name, exact: true }).waitFor();
  await other.reload();
  await other.getByRole('link', { name, exact: true }).waitFor();
  await other.screenshot({ path: join(artifacts, 'browser-readback.png'), fullPage: true });
  assert.deepEqual(errors, []);
  await writeFile(join(artifacts, 'browser.json'), JSON.stringify({
    status: 'passed', browser: browser.version(), node: process.version,
    renderedFixtureProjects: ['Orchard', 'Harbor'], createdProject: created.id,
    writeStatus: response.status(), independentReadStatus: readback.status(), reloadVerified: true,
  }, null, 2));
  await independent.close();
} catch (error) {
  await page.screenshot({ path: join(artifacts, 'browser-failure.png'), fullPage: true }).catch(() => {});
  throw error;
} finally {
  await browser.close();
}
