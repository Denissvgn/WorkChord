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
  await page.goto(`/projects/${projects[0].id}`);
  await page.getByRole('button', { name: 'Add backlog task', exact: true }).click();
  await page.getByRole('textbox', { name: 'Task Title', exact: false }).fill('Canonical browser work');
  await page.getByRole('textbox', { name: 'Goal', exact: true }).fill('Capture and deliver urgent human work');
  await page.getByRole('textbox', { name: 'Context', exact: true }).fill('The task starts without a forecast or an invented estimate.');
  await page.getByRole('textbox', { name: 'Scope', exact: true }).fill('One independently checked result');
  await page.getByRole('button', { name: 'Add criterion', exact: true }).click();
  await page.getByRole('textbox', { name: 'Criterion 1', exact: true }).fill('The result can be inspected independently');
  await page.getByRole('textbox', { name: 'Verification approach', exact: true }).fill('Inspect the delivered result');
  await page.getByLabel('Owner', { exact: true }).selectOption({ label: 'Shared owner' });
  const captured = page.waitForResponse(response => response.url().endsWith(`/api/projects/${projects[0].id}/backlog`) && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Create Task', exact: true }).click();
  const captureResponse = await captured;
  assert.equal(captureResponse.status(), 201, await captureResponse.text());
  const capturedTask = await captureResponse.json();
  assert.equal(capturedTask.effort_hours, null);
  assert.equal(capturedTask.iteration_id, null);
  assert.equal(capturedTask.owner_profile_id, me.profile.id);
  await page.getByRole('button', { name: 'Canonical browser work', exact: true }).click();
  await page.getByRole('textbox', { name: 'Goal', exact: true }).waitFor();
  await page.getByRole('textbox', { name: 'Goal', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: '/artifacts/canonical-brief-desktop.png', fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('textbox', { name: 'Criterion 1', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: '/artifacts/canonical-brief-mobile.png', fullPage: true });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  await page.setViewportSize({ width: 1440, height: 1000 });
  const workCommand = async action => {
    await page.getByLabel('Action', { exact: true }).selectOption(action);
    await page.getByRole('textbox', { name: 'Reason for the action or review', exact: true }).fill('Deliver the explicit human workflow');
    const pending = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/commands`) && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Apply action', exact: true }).click();
    const result = await pending;
    assert.equal(result.status(), 200, await result.text());
  };
  await workCommand('start_manual');
  await page.getByRole('textbox', { name: 'Evidence', exact: true }).fill('Discard this evidence draft');
  await closeDirty();
  await page.getByRole('button', { name: 'Canonical browser work', exact: true }).click();
  await page.getByRole('textbox', { name: 'Evidence', exact: true }).waitFor();
  assert.equal(await page.getByRole('textbox', { name: 'Evidence', exact: true }).inputValue(), '');
  await page.getByLabel('The result can be inspected independently', { exact: true }).selectOption('completed');
  await page.getByRole('textbox', { name: 'Evidence', exact: true }).fill('A reviewer can reproduce and inspect the result.');
  assert.equal(await page.getByRole('textbox', { name: 'Task Title', exact: false }).isDisabled(), true);
  assert.equal(await page.getByLabel('Action', { exact: true }).isDisabled(), true);
  const progressSaved = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/progress`) && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Save progress', exact: true }).click();
  assert.equal((await progressSaved).status(), 200);
  await workCommand('resolve_manual');
  assert.equal(await page.getByRole('button', { name: 'Accept work', exact: true }).isDisabled(), true);
  const implemented = await (await context.request.get(`/api/tasks/${capturedTask.id}`)).json();
  assert.equal(implemented.start_date, null);
  assert.equal(implemented.status, 'resolved');
  assert.equal(implemented.is_accepted, false);
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();

  const reviewerContext = await browser.newContext({ baseURL, locale: 'en-US', viewport: { width: 1440, height: 1000 } });
  const reviewerPage = await reviewerContext.newPage();
  reviewerPage.on('pageerror', error => errors.push(error.message));
  await reviewerPage.goto(`/projects/${projects[0].id}`);
  await reviewerPage.getByRole('link', { name: 'Sign in', exact: true }).click();
  await reviewerPage.getByRole('link', { name: 'Continue as Charlie' }).click();
  await reviewerPage.getByRole('button', { name: 'Canonical browser work', exact: true }).click();
  await reviewerPage.getByRole('textbox', { name: 'Reason for the action or review', exact: true }).fill('Independently inspected the criterion evidence');
  const accepted = reviewerPage.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/review`) && response.request().method() === 'POST');
  await reviewerPage.getByRole('button', { name: 'Accept work', exact: true }).click();
  const verdict = await accepted;
  assert.equal(verdict.status(), 200, await verdict.text());
  assert.equal((await verdict.json()).is_accepted, true);
  await reviewerPage.getByRole('dialog').getByText('Accepted', { exact: true }).waitFor();
  await reviewerPage.getByText('Loading data...', { exact: true }).waitFor({ state: 'hidden' });
  await reviewerPage.screenshot({ path: '/artifacts/canonical-review-desktop.png', fullPage: true });
  await reviewerContext.close();
  check('Unestimated backlog capture, durable owner, structured criteria, manual execution, persisted evidence, and independent human acceptance');
  await page.getByRole('button', { name: 'Add backlog task', exact: true }).click();
  await page.getByRole('textbox', { name: 'Task Title', exact: false }).fill('Preserve the structured intake');
  await page.getByRole('textbox', { name: 'Goal', exact: true }).fill('Keep the draft through triage');
  await page.getByRole('textbox', { name: 'Context', exact: true }).fill('Context must survive the handoff.');
  await page.getByRole('button', { name: 'Add criterion', exact: true }).click();
  await page.getByRole('textbox', { name: 'Criterion 1', exact: true }).fill('The criterion keeps its identity');
  const intakeSaved = page.waitForResponse(response => response.url().endsWith('/api/triage') && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Send to Triage', exact: false }).click();
  const intakeResponse = await intakeSaved;
  assert.equal(intakeResponse.status(), 201, await intakeResponse.text());
  const intake = await intakeResponse.json();
  assert.equal(intake.brief.context, 'Context must survive the handoff.');
  const refreshedMe = await (await context.request.get('/api/auth/me')).json();
  const converted = await context.request.post(`/api/triage/${intake.id}/convert-to-backlog`, { headers: { 'X-CSRF-Token': refreshedMe.csrf_token, Origin: baseURL }, data: { project_id: projects[0].id } });
  assert.equal(converted.status(), 200, await converted.text());
  assert.equal((await converted.json()).task.brief.acceptance_criteria[0].id, intake.brief.acceptance_criteria[0].id);
  check('Explicit evidence discard stays discarded; structured triage handoff preserves canonical content and criterion identity');


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
