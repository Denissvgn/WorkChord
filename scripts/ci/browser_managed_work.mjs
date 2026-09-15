import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { chromium } from 'playwright';

const baseURL = process.env.BROWSER_BASE_URL;
if (baseURL !== 'http://localhost:4173') throw new Error('Only the disposable managed frontend is allowed');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ baseURL, locale: 'en-US', viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const errors = [];
const steps = [];
page.on('pageerror', error => errors.push(error.message));
page.on('dialog', dialog => dialog.accept());
const check = label => { steps.push(label); console.log(label); };
const signedIn = async name => {
  const inEditor = page.getByRole('dialog').getByRole('link', { name: 'Sign in', exact: true });
  await (await inEditor.count() ? inEditor : page.getByRole('link', { name: 'Sign in', exact: true })).click();
  await page.getByRole('link', { name: `Continue as ${name}` }).click();
  await page.getByText(name, { exact: true }).first().waitFor();
};
const openNested = async () => {
  const board = page.getByRole('button', { name: 'Open task: Nested leaf', exact: true });
  if (new URL(page.url()).searchParams.get('layout') === 'board' || await board.count()) {
    await board.waitFor();
    await board.click();
  }
  else {
    await page.getByText('Parent', { exact: true }).first().waitFor();
    const expand = page.getByRole('button', { name: /Expand: Parent/i });
    if (await expand.count()) await expand.click();
    await page.getByRole('button', { name: 'Edit Task: Nested leaf', exact: true }).click();
  }
  await page.getByRole('textbox', { name: 'Description', exact: true }).waitFor();
};
const closeDirty = async () => {
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  await page.getByRole('button', { name: 'Discard changes', exact: true }).click();
};
try {
  for (let attempt = 0; attempt < 90; attempt++) {
    try {
      if ((await context.request.get('/api/auth/me', { timeout: 1000 })).ok()) break;
    } catch { /* Wait only for this disposable application. */ }
    if (attempt === 89) throw new Error('Disposable application did not start');
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  assert.equal((await context.request.get('/api/projects')).status(), 401);
  await page.goto('/tasks');
  await page.getByRole('heading', { name: 'Sign in to WorkChord' }).waitFor();
  await signedIn('Alice');
  const me = await (await context.request.get('/api/auth/me')).json();
  assert.equal(me.authenticated, true);
  assert.equal(me.profile.display_name, 'Shared owner');
  const projects = await (await context.request.get('/api/projects')).json();
  assert.deepEqual(projects.map(project => project.name), ['Orchard']);
  const iterations = await (await context.request.get('/api/iterations')).json();
  const iteration = iterations[0];
  const tasks = await (await context.request.get(`/api/iterations/${iteration.id}/tasks`)).json();
  const nested = tasks.find(task => task.title === 'Parent').children[0];
  const headers = { 'X-CSRF-Token': me.csrf_token, Origin: baseURL };
  check('Real OIDC login, profile link, cookie integrity, and project isolation');

  await openNested();
  const description = page.getByRole('textbox', { name: 'Description', exact: true });
  await description.fill('Browser draft preserved through dismissal and conflict');
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  await page.getByRole('button', { name: 'Keep editing', exact: true }).click();
  assert.equal(await description.inputValue(), 'Browser draft preserved through dismissal and conflict');
  await page.keyboard.press('Escape');
  await page.getByRole('button', { name: 'Keep editing', exact: true }).click();
  assert.match(await description.inputValue(), /Browser draft/);
  await page.route(`**/api/tasks/${nested.id}`, async route => {
    if (route.request().method() === 'PUT') await route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ detail: 'Disposable injected save failure' }) });
    else await route.continue();
  });
  await page.getByRole('button', { name: 'Update Task', exact: true }).click();
  await page.getByText('Disposable injected save failure', { exact: true }).waitFor();
  assert.match(await description.inputValue(), /Browser draft/);
  await page.unroute(`**/api/tasks/${nested.id}`);
  check('Dirty Cancel/Escape and failed save preserve description');

  const changed = await context.request.put(`/api/tasks/${nested.id}`, { headers, data: { title: 'Nested leaf', description: 'Other writer changed the work', expected_version: nested.version } });
  assert.equal(changed.status(), 200, await changed.text());
  const saveConflict = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${nested.id}`) && response.request().method() === 'PUT');
  await page.getByRole('button', { name: 'Update Task', exact: true }).click();
  assert.equal((await saveConflict).status(), 409);
  await page.getByText('This task changed while you were editing', { exact: true }).waitFor();
  await page.getByRole('button', { name: 'Keep draft with current version', exact: true }).click();
  await page.getByText('Current version loaded. Your draft is unchanged; review it before saving.', { exact: true }).waitFor();
  assert.match(await description.inputValue(), /Browser draft/);
  const saved = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${nested.id}`) && response.request().method() === 'PUT');
  await page.getByRole('button', { name: 'Update Task', exact: true }).click();
  assert.equal((await saved).status(), 200);
  await description.waitFor({ state: 'hidden' });
  const readback = await context.request.get(`/api/tasks/${nested.id}`);
  assert.match((await readback.json()).description, /Browser draft/);
  check('Two-client stale write returns 409; explicit current revision reapply succeeds');

  await page.getByRole('button', { name: 'Board', exact: true }).click();
  await page.getByRole('button', { name: 'Open task: Nested leaf', exact: true }).waitFor();
  await page.getByRole('button', { name: 'Move task: Nested leaf', exact: true }).focus();
  assert.equal(await page.evaluate(() => document.activeElement?.getAttribute('aria-label')), 'Move task: Nested leaf');
  await page.screenshot({ path: '/artifacts/managed-board-desktop.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await openNested();
  await page.getByRole('textbox', { name: 'Description', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: '/artifacts/managed-editor-mobile.png', fullPage: true });
  const mobileDescription = page.getByRole('textbox', { name: 'Description', exact: true });
  await mobileDescription.fill('Recover this draft after session expiry');
  const cookie = (await context.cookies()).find(cookie => cookie.name === 'workchord_session');
  const expired = await context.request.post('http://oidc:8002/control/expire', { headers: { 'X-Fixture-Key': 'disposable-browser-control' }, data: { token: cookie.value } });
  assert.equal((await expired.json()).expired, 1);
  await page.getByRole('button', { name: 'Update Task', exact: true }).click();
  await page.getByText('Your session expired. Sign in again to continue.', { exact: false }).first().waitFor();
  assert.equal(await mobileDescription.inputValue(), 'Recover this draft after session expiry');
  await signedIn('Alice');
  await openNested();
  assert.equal(await page.getByRole('textbox', { name: 'Description', exact: true }).inputValue(), 'Recover this draft after session expiry');
  await closeDirty();
  check('Nested Board keyboard detail path and same-account draft recovery after real session expiry');

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.getByLabel('Account and access').click();
  await page.getByRole('button', { name: 'Sign out', exact: true }).click();
  await page.getByRole('heading', { name: 'Sign in to WorkChord' }).waitFor();
  await signedIn('Bob');
  await page.goto('/tasks?layout=board');
  await page.getByRole('button', { name: 'Open task: Harbor leaf', exact: true }).waitFor();
  assert.equal(await page.getByRole('button', { name: 'Open task: Nested leaf', exact: true }).count(), 0);
  const otherProjects = await (await context.request.get('/api/projects')).json();
  assert.deepEqual(otherProjects.map(project => project.name), ['Harbor']);
  assert.equal((await context.request.get(`/api/tasks/${nested.id}`)).status(), 404);
  assert.equal(await page.evaluate(() => Object.keys(sessionStorage).some(key => key.startsWith('workchord-draft:') && sessionStorage.getItem(key)?.includes('Recover this draft'))), false);
  assert.deepEqual(errors, []);
  check('Sign-out/account switch clears private work and rejects the previous project');
  await writeFile('/artifacts/managed-browser.json', JSON.stringify({ status: 'passed', browser: browser.version(), node: process.version, steps, pageErrors: errors, issuer: 'disposable-synthetic-oidc', realProviderPilot: false }, null, 2));
} catch (error) {
  await page.screenshot({ path: '/artifacts/managed-browser-failure.png', fullPage: true }).catch(() => {});
  await writeFile('/artifacts/managed-browser-failure.json', JSON.stringify({ steps, pageErrors: errors, error: String(error) }, null, 2));
  throw error;
} finally { await browser.close(); }
