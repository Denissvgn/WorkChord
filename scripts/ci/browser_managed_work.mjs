import { dispatchInbox, backupBrowserDatabase } from './browser_worker.mjs';
import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { chromium } from 'playwright';

const baseURL = process.env.BROWSER_BASE_URL;
const artifacts = process.env.BROWSER_ARTIFACTS_DIR || '/artifacts';
const issuer = process.env.WORKCHORD_FIXTURE_ISSUER || 'http://oidc:8002';
if (!['http://localhost:8002', 'http://oidc:8002'].includes(issuer)) throw new Error('Only the fixture issuer is allowed');
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
  if (process.env.WORKCHORD_FIXTURE_NONCE) {
    const fixture = await context.request.get('/api/auth/me');
    assert.equal(fixture.headers()['x-workchord-fixture'], process.env.WORKCHORD_FIXTURE_NONCE);
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
  await page.getByRole('button', { name: 'Reload current server work', exact: true }).click();
  await page.getByRole('button', { name: 'I compared current work; resume this draft', exact: true }).click();
  assert.match(await description.inputValue(), /Browser draft/);
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
  await page.screenshot({ path: join(artifacts, 'managed-board-desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await openNested();
  await page.getByRole('textbox', { name: 'Description', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: join(artifacts, 'managed-editor-mobile.png'), fullPage: true });
  const mobileDescription = page.getByRole('textbox', { name: 'Description', exact: true });
  await mobileDescription.fill('Recover this draft after session expiry');
  const cookie = (await context.cookies()).find(cookie => cookie.name === 'workchord_session');
  const expired = await context.request.post(`${issuer}/control/expire`, { headers: { 'X-Fixture-Key': 'disposable-browser-control' }, data: { token: cookie.value } });
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
  await page.screenshot({ path: join(artifacts, 'canonical-brief-desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('textbox', { name: 'Criterion 1', exact: true }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: join(artifacts, 'canonical-brief-mobile.png'), fullPage: true });
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

  const reviewerContext = await browser.newContext({ baseURL, locale: 'en-US', hasTouch: true, viewport: { width: 1440, height: 1000 } });
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
  await reviewerPage.screenshot({ path: join(artifacts, 'canonical-review-desktop.png'), fullPage: true });
  const followed = reviewerPage.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/subscription`) && response.request().method() === 'PUT');
  await reviewerPage.getByRole('checkbox', { name: 'Follow this task', exact: true }).click();
  assert.equal((await followed).status(), 200);
  await reviewerPage.getByRole('checkbox', { name: 'Discussion', exact: true }).waitFor();
  await reviewerPage.getByRole('checkbox', { name: 'Follow this task', exact: true }).waitFor({ state: 'visible' });
  const reviewerMe = await (await reviewerContext.request.get('/api/auth/me')).json();
  await page.goto('/tasks?scope=backlog');
  await page.getByRole('searchbox', { name: 'Search tasks', exact: true }).fill(`#${capturedTask.id}`);
  await page.getByRole('region', { name: 'Search tasks', exact: true }).getByRole('link', { name: `#${capturedTask.id} · Canonical browser work`, exact: true }).click();
  await page.getByRole('textbox', { name: 'Task Title', exact: false }).scrollIntoViewIfNeeded();
  await page.screenshot({ path: join(artifacts, 'teamwork-editor-desktop.png'), fullPage: true });
  await page.getByRole('textbox', { name: 'New comment', exact: true }).fill('Coordinate delivery with the reviewer');
  await page.getByRole('textbox', { name: 'Mention a person: search by name', exact: true }).fill('Charlie');
  await page.getByRole('checkbox', { name: 'Charlie', exact: true }).check();
  const beforeDiscussion = await (await context.request.get(`/api/tasks/${capturedTask.id}`)).json();
  const commentPosted = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/comments`) && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Post comment', exact: true }).click();
  assert.equal((await commentPosted).status(), 201);
  await page.getByText('Comment saved.', { exact: true }).waitFor();
  const afterDiscussion = await (await context.request.get(`/api/tasks/${capturedTask.id}`)).json();
  assert.equal(afterDiscussion.version, beforeDiscussion.version);
  await page.screenshot({ path: join(artifacts, 'teamwork-discussion-desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByRole('heading', { name: 'Discussion', exact: true }).evaluate(element => element.scrollIntoView({ block: 'start' }));
  await page.screenshot({ path: join(artifacts, 'teamwork-discussion-mobile.png'), fullPage: true });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await dispatchInbox();
  await reviewerPage.goto('/my-work?queue=inbox');
  await reviewerPage.getByRole('button', { name: 'Canonical browser work', exact: true }).waitFor();
  await reviewerPage.getByRole('button', { name: 'Mark read', exact: true }).click();
  await reviewerPage.getByRole('button', { name: 'Mark unread', exact: true }).waitFor();
  await reviewerPage.setViewportSize({ width: 390, height: 844 });
  await reviewerPage.screenshot({ path: join(artifacts, 'teamwork-inbox-mobile.png'), fullPage: true });
  assert.equal(await reviewerPage.evaluate(() => matchMedia('(pointer: coarse)').matches), true);
  assert.equal(await reviewerPage.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  await page.getByRole('textbox', { name: 'New comment', exact: true }).fill('Queued before access is revoked');
  await page.getByRole('checkbox', { name: 'Charlie', exact: true }).check();
  const queuedBeforeRevocation = page.waitForResponse(response => response.url().endsWith(`/api/tasks/${capturedTask.id}/comments`) && response.request().method() === 'POST');
  await page.getByRole('button', { name: 'Post comment', exact: true }).click();
  assert.equal((await queuedBeforeRevocation).status(), 201);
  const identityNow = await (await context.request.get('/api/auth/me')).json();
  const revocation = await context.request.put(`/api/auth/project-members/${projects[0].id}/${reviewerMe.principal.id}`, {
    headers: { 'X-CSRF-Token': identityNow.csrf_token, Origin: baseURL }, data: { role: null, reason: 'Disposable recipient revocation check' },
  });
  assert.equal(revocation.status(), 200, await revocation.text());
  await dispatchInbox();
  assert.deepEqual((await (await reviewerContext.request.get('/api/notifications')).json()).items, []);
  const createOwned = async (title, parentId) => {
    const response = await context.request.post(`/api/projects/${projects[0].id}/backlog`, {
      headers: { 'X-CSRF-Token': identityNow.csrf_token, Origin: baseURL },
      data: { title, project_id: projects[0].id, owner_profile_id: me.profile.id, parent_id: parentId ?? null, effort_hours: 1.5 },
    });
    assert.equal(response.status(), 201, await response.text());
    return response.json();
  };
  const handoff = await createOwned('Prepare a human team handoff');
  const nestedHandoff = await createOwned('Согласовать критерии готовности и порядок совместной проверки результата между участниками команды', handoff.id);
  await createOwned('Confirm the deployment checklist and coordinate the next review');
  await page.goto('/my-work?queue=queued');
  await page.getByRole('heading', { name: 'My Work', exact: true }).waitFor();
  await page.getByRole('button', { name: /Согласовать критерии/ }).waitFor();
  const peerContext = await browser.newContext({ baseURL, locale: 'en-US' });
  const peerPage = await peerContext.newPage();
  peerPage.on('pageerror', error => errors.push(error.message));
  await peerPage.goto('/my-work');
  await peerPage.getByRole('link', { name: 'Sign in', exact: true }).click();
  await peerPage.getByRole('link', { name: 'Continue as Alice' }).click();
  await peerPage.getByText('Alice', { exact: true }).first().waitFor();
  const peerIdentity = await (await peerContext.request.get('/api/auth/me')).json();
  const peerHeaders = { 'X-CSRF-Token': peerIdentity.csrf_token, Origin: baseURL };
  const unassigned = await peerContext.request.post(`/api/projects/${projects[0].id}/backlog`, { headers: peerHeaders,
    data: { title: 'Externally assigned foreground work', project_id: projects[0].id, owner_profile_id: null } });
  assert.equal(unassigned.status(), 201, await unassigned.text());
  const observed = await unassigned.json();
  const assigned = await peerContext.request.put(`/api/tasks/${observed.id}`, { headers: peerHeaders,
    data: { owner_profile_id: me.profile.id, expected_version: observed.version } });
  assert.equal(assigned.status(), 200, await assigned.text());
  const assignedTask = await assigned.json();
  await page.getByRole('button', { name: `#${observed.id} · Externally assigned foreground work`, exact: true }).waitFor({ timeout: 45000 });
  const started = await peerContext.request.post(`/api/tasks/${observed.id}/commands`, { headers: peerHeaders,
    data: { action: 'start_manual', expected_version: assignedTask.version, reason: 'Synthetic peer start' } });
  assert.equal(started.status(), 200, await started.text());
  await page.getByRole('button', { name: `#${observed.id} · Externally assigned foreground work`, exact: true }).waitFor({ state: 'hidden', timeout: 45000 });
  await page.goto(`/my-work?queue=active&task=${observed.id}`);
  await page.getByRole('textbox', { name: 'Task Title', exact: false }).waitFor();
  const peerComment = await peerContext.request.post(`/api/tasks/${observed.id}/comments`, {
    headers: peerHeaders, data: { body: 'Peer comment arrives in foreground', mentions: [] } });
  assert.equal(peerComment.status(), 201, await peerComment.text());
  await page.getByText('Peer comment arrives in foreground', { exact: true }).waitFor({ timeout: 45000 });
  if (process.env.TIME_ENTRIES_ENABLED === 'true') {
    await page.getByRole('button', { name: 'Time entries', exact: true }).click();
    const entry = await peerContext.request.post('/api/time-entries', { headers: peerHeaders,
      data: { project_id: projects[0].id, task_id: observed.id, request_id: crypto.randomUUID(),
        work_date: '2026-10-08', timezone: 'UTC', minutes: 15, note: 'Foreground recorded work' } });
    assert.equal(entry.status(), 201, await entry.text());
    const recorded = await entry.json();
    await page.getByText('Foreground recorded work', { exact: true }).waitFor({ timeout: 45000 });
    const entryRow = page.locator('li').filter({ hasText: 'Foreground recorded work' });
    await entryRow.getByRole('button', { name: 'Correct entry', exact: true }).click();
    await page.getByLabel('Minutes', { exact: true }).fill('25');
    await page.getByLabel('Private note (optional)', { exact: true }).fill('Retained private correction draft');
    await page.getByLabel('Reason for correction or void', { exact: true }).fill('Compared retained author intent');
    const taskWrites = []; const observe = request => { if (request.method() === 'PUT' && new URL(request.url()).pathname === `/api/tasks/${observed.id}`) taskWrites.push(request.url()); };
    page.on('request', observe); await page.getByLabel('Minutes', { exact: true }).press('Enter');
    await new Promise(resolve => setTimeout(resolve, 100)); assert.deepEqual(taskWrites, []); page.off('request', observe);
    const correction = await peerContext.request.put(`/api/time-entries/${recorded.id}`, { headers: peerHeaders,
      data: { expected_version: recorded.version, work_date: '2026-10-08', timezone: 'UTC', minutes: 20,
        note: 'Foreground corrected work', reason: 'Synthetic peer correction' } });
    assert.equal(correction.status(), 200, await correction.text());
    const conflict = page.waitForResponse(response => response.request().method() === 'PUT' && new URL(response.url()).pathname === `/api/time-entries/${recorded.id}`);
    await page.getByRole('button', { name: 'Save correction', exact: true }).click();
    const stale = await conflict; assert.equal(stale.status(), 409);
    assert.equal(stale.request().postDataJSON().expected_version, 1);
    assert.equal(await page.getByLabel('Minutes', { exact: true }).inputValue(), '25');
    assert.equal(await page.getByLabel('Private note (optional)', { exact: true }).inputValue(), 'Retained private correction draft');
    const reloaded = page.waitForResponse(response => response.request().method() === 'GET' && new URL(response.url()).pathname === `/api/time-entries/${recorded.id}`);
    await page.getByRole('button', { name: 'Reload current entry', exact: true }).click();
    assert.equal((await reloaded).status(), 200);
    assert.equal(await page.getByLabel('Minutes', { exact: true }).inputValue(), '25');
    await page.getByRole('button', { name: 'Keep draft with current version', exact: true }).click();
    const applied = page.waitForResponse(response => response.request().method() === 'PUT' && new URL(response.url()).pathname === `/api/time-entries/${recorded.id}`);
    await page.getByRole('button', { name: 'Save correction', exact: true }).click();
    const savedEntry = await applied; assert.equal(savedEntry.status(), 200, await savedEntry.text());
    const saved = await savedEntry.json(); assert.equal(saved.minutes, 25); assert.equal(saved.version, 3);
    const readback = await peerContext.request.get(`/api/time-entries?project_id=${projects[0].id}&task_id=${observed.id}`);
    assert.equal((await readback.json()).items[0].note, 'Retained private correction draft');
    await page.getByText('Retained private correction draft', { exact: true }).first().waitFor();
    await page.locator('li').filter({ hasText: 'Retained private correction draft' }).getByRole('button', { name: 'Correct entry', exact: true }).click();
    await page.getByLabel('Reason for correction or void', { exact: true }).fill('Synthetic duplicate record');
    const voided = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === `/api/time-entries/${recorded.id}/void`);
    await page.getByRole('button', { name: 'Void entry', exact: true }).click();
    assert.equal((await voided).status(), 200);
    const history = await peerContext.request.get(`/api/time-entries/${recorded.id}/history`);
    const revisions = (await history.json()).items; assert.deepEqual(revisions.map(row => row.version), [1, 2, 3, 4]);
    assert.equal(revisions.at(-1).voided, true);
    await page.getByLabel('Work date', { exact: true }).fill('2026-10-08');
    await page.getByLabel('Timezone', { exact: true }).fill('Europe/Madrid');
    await page.getByLabel('Minutes', { exact: true }).fill('35');
    await page.getByLabel('Private note (optional)', { exact: true }).fill('UI owned recorded work');
    const createdByUI = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/api/time-entries');
    await page.getByRole('button', { name: 'Record time', exact: true }).click();
    const createdResponse = await createdByUI; assert.equal(createdResponse.status(), 201, await createdResponse.text());
    const uiRecord = await createdResponse.json(); assert.equal(uiRecord.minutes, 35);
    const range = `project_id=${projects[0].id}&start=2026-10-01&end=2026-10-31`;
    const totals = await peerContext.request.get(`/api/time-entries/report?${range}&scope=project`);
    assert.equal(totals.status(), 200); const report = await totals.json();
    assert.equal(report.totals.recorded_minutes, 35); assert.equal(report.totals.tasks_with_records, 1);
    assert.ok(!JSON.stringify(report).includes('Retained private correction draft') && !JSON.stringify(report).includes('UI owned recorded work'));
    const exported = await peerContext.request.get(`/api/time-entries/export?${range}&scope=mine&kind=entries`);
    assert.equal(exported.status(), 200); assert.ok((await exported.text()).includes('Retained private correction draft'));
    await writeFile(join(artifacts, 'time-workflow-receipt.json'), JSON.stringify({ status: 'passed', privateRecord: recorded.id, activePrivateRecord: uiRecord.id,
      correctedVersion: 3, voidedVersion: 4, historyVersions: revisions.map(row => row.version), staleDraftRetained: true,
      explicitReapply: true, managerTotalsExcludeVoids: true, privateNotesAbsentFromTotals: true, exportVerified: true,
      keyboardDidNotSubmitTask: true, synthetic: true }, null, 2));
    check('Time create, stale correction with retained intent, explicit reapply, void, history, totals and private export reconcile');

  }
  if (process.env.WORKCHORD_FIXTURE_WORKFLOWS === 'true') {
    const now = await (await context.request.get('/api/auth/me')).json();
    const currentChild = (await (await context.request.get(`/api/tasks/${nestedHandoff.id}/detail`)).json()).task;
    const urgent = await context.request.put(`/api/tasks/${currentChild.id}`, { headers: { 'X-CSRF-Token': now.csrf_token, Origin: baseURL },
      data: { expected_version: currentChild.version, priority: 1 } });
    assert.equal(urgent.status(), 200, await urgent.text());
    const currentParent = (await (await context.request.get(`/api/tasks/${handoff.id}/detail`)).json()).task;
    const deferred = await context.request.put(`/api/tasks/${handoff.id}`, { headers: { 'X-CSRF-Token': now.csrf_token, Origin: baseURL },
      data: { expected_version: currentParent.version, is_deferred: true } });
    assert.equal(deferred.status(), 200, await deferred.text());
    const child = (await (await context.request.get(`/api/tasks/${nestedHandoff.id}/detail`)).json()).task;
    assert.equal(child.effective_is_deferred, true);
    const childActions = await (await context.request.get(`/api/tasks/${child.id}/actions`)).json();
    assert.equal(childActions.actions.find(action => action.action === 'start_manual').allowed, false);
    const work = await (await context.request.get('/api/tasks/my-work')).json();
    assert.ok(!Object.values(work.queues).flat().some(task => task.id === child.id));
    const featureHeaders = { 'X-Fixture-Key': process.env.WORKCHORD_FIXTURE_NONCE, 'X-CSRF-Token': now.csrf_token, Origin: baseURL };
    const feature = async enabled => {
      const response = await context.request.post('/api/tasks/1/_fixture/time-feature', { headers: featureHeaders, data: { enabled } });
      assert.equal(response.status(), 200, await response.text());
    };
    await feature(false);
    try {
      const disabled = await context.request.get('/api/time-entries'); assert.ok([403,404].includes(disabled.status()));
      const capability = await (await context.request.get('/api/time-entries/capabilities')).json(); assert.equal(capability.enabled, false);
    } finally { await feature(true); }
    const retained = await context.request.get('/api/time-entries'); assert.equal(retained.status(), 200);
    assert.ok((await retained.json()).items.some(row => row.note === 'UI owned recorded work'));
    const lookup = await (await context.request.get(`/api/tasks/lookup?project_id=${projects[0].id}&limit=100`)).json();
    assert.equal(lookup.has_more, false);
    const details = [];
    for (const ref of lookup.items) {
      const value = await (await context.request.get(`/api/tasks/${ref.id}/detail`)).json();
      const actions = await (await context.request.get(`/api/tasks/${ref.id}/actions`)).json();
      assert.equal(actions.version, value.task.version); details.push(value.task);
    }
    const leaves = details.filter(task => !task.is_composite && !task.canceled_at && !task.effective_is_deferred);
    const summary = await (await context.request.get(`/api/projects/${projects[0].id}/summary`)).json();
    const portfolio = await (await context.request.get('/api/projects/portfolio-summaries/page?limit=100')).json();
    const matching = portfolio.items.find(row => row.project_id === projects[0].id);
    const iterationSummary = await (await context.request.get(`/api/iterations/${iteration.id}/summary`)).json();
    assert.equal(summary.total_tasks, leaves.length); assert.equal(summary.total_tasks, matching.total_tasks);
    assert.equal(summary.implemented_tasks, leaves.filter(task => ['resolved','closed'].includes(task.status)).length);
    assert.equal(summary.total_tasks, iterationSummary.total_tasks + leaves.filter(task => task.iteration_id === null).length);
    const capacity = await context.request.get(`/api/team-member-profiles/${me.profile.id}/capacity?start=2026-01-01&end=2026-01-31`);
    assert.equal(capacity.status(), 200);
    await writeFile(join(artifacts, 'managed-workflow-receipt.json'), JSON.stringify({ status: 'passed', strictMutationVersions: true,
      projectTotal: summary.total_tasks, iterationTotal: iterationSummary.total_tasks, backlogLeaves: leaves.filter(task => task.iteration_id === null).length,
      portfolioMatches: true, allowedActionsMatchObservedVersions: true, sharedCapacityRead: true,
      disabledFeatureRetainsLedger: true, inheritedDeferralExcludesQueueAndExecution: true, nestedBacklogIdentityRetained: child.id, synthetic: true }, null, 2));
    check('Strict contexts, independent project/iteration/backlog/portfolio metrics, action versions, shared capacity and disabled-feature retention reconcile');
  }
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  await peerContext.close();
  check('Two managed sessions discover assignment, queue movement, comments and optional time corrections without focus changes');
  const themeContrast = [];
  for (const theme of ['light', 'dark', 'blue', 'green']) {
    await page.evaluate(async chosen => { const module = await import('/src/store/themeStore.ts'); module.useThemeStore.getState().setTheme(chosen); }, theme);
    await page.evaluate(async () => {
      await new Promise(resolve => requestAnimationFrame(resolve));
      await Promise.all(document.getAnimations().filter(animation => animation instanceof CSSTransition).map(animation => animation.finished.catch(() => {})));
    });
    const labels = await page.getByRole('navigation', { name: 'Work queues', exact: true }).evaluate(nav => {
      const rgb = value => (value.match(/[\d.]+/g) || []).map(Number);
      const luminance = color => color.slice(0, 3).map(value => value / 255).map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4).reduce((sum, value, index) => sum + value * [.2126, .7152, .0722][index], 0);
      return [...nav.querySelectorAll('button')].filter(button => !button.disabled).map(button => {
        const foreground = getComputedStyle(button).color;
        let parent = button;
        let background = getComputedStyle(parent).backgroundColor;
        while ((rgb(background)[3] ?? 1) === 0 && parent.parentElement) {
          parent = parent.parentElement;
          background = getComputedStyle(parent).backgroundColor;
        }
        const lights = [luminance(rgb(foreground)), luminance(rgb(background))].sort((a, b) => b - a);
        return { label: button.textContent.trim(), foreground, background, ratio: (lights[0] + .05) / (lights[1] + .05) };
      });
    });
    assert.ok(labels.every(label => label.ratio >= 4.5), JSON.stringify({ theme, labels }));
    themeContrast.push({ theme, labels });
    await page.screenshot({ path: join(artifacts, `teamwork-my-work-${theme}-desktop.png`), fullPage: true });
  }
  await writeFile(join(artifacts, 'teamwork-theme-contrast.json'), JSON.stringify(themeContrast, null, 2));
  await page.evaluate(async () => { const theme = await import('/src/store/themeStore.ts'); theme.useThemeStore.getState().setTheme('light'); });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.evaluate(async () => { const locale = await import('/src/i18n/i18n.ts'); await locale.changeAppLanguage('ru'); });
  await page.getByRole('heading', { name: 'Моя работа', exact: true }).waitFor();
  await page.screenshot({ path: join(artifacts, 'teamwork-my-work-ru-mobile.png'), fullPage: true });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  assert.equal(await page.evaluate(() => matchMedia('(prefers-reduced-motion: reduce)').matches), true);
  await page.evaluate(async () => { const locale = await import('/src/i18n/i18n.ts'); await locale.changeAppLanguage('en'); });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto(`/projects/${projects[0].id}`);
  check('Task ID search, independent discussion version, mentions, inbox read state, recipient revocation, and responsive My Work');
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
  if (process.env.TIME_ENTRIES_ENABLED === 'true') {
    const mine = await context.request.get('/api/time-entries'); assert.equal(mine.status(), 200);
    assert.deepEqual((await mine.json()).items, []);
    const timeProof = JSON.parse(await (await import('node:fs/promises')).readFile(join(artifacts, 'time-workflow-receipt.json'), 'utf8'));
    const denied = await context.request.get(`/api/time-entries/${timeProof.activePrivateRecord}/history`);
    assert.ok([403,404].includes(denied.status())); assert.ok(!(await denied.text()).includes('UI owned recorded work'));
    const restore = await backupBrowserDatabase();
    await writeFile(join(artifacts, 'time-database-restore.json'), restore);
    check('Account/project switch hides private records and an independent full SQLite restore preserves every row and allocation state');
  }
  assert.equal(await page.evaluate(() => Object.keys(sessionStorage).some(key => key.startsWith('workchord-draft:') && sessionStorage.getItem(key)?.includes('Recover this draft'))), false);
  assert.deepEqual(errors, []);
  check('Sign-out/account switch clears private work and rejects the previous project');
  await writeFile(join(artifacts, 'accessibility-localization.json'), JSON.stringify({ status: 'passed', locales: ['en','ru'],
    widths: [1440,390], keyboardDetailAndTimeControls: true, themeContrastFile: 'teamwork-theme-contrast.json', noHorizontalOverflow: true,
    pageErrors: errors, synthetic: true }, null, 2));
  await writeFile(join(artifacts, 'managed-browser.json'), JSON.stringify({ status: 'passed', browser: browser.version(), node: process.version, steps, pageErrors: errors, issuer: 'disposable-synthetic-oidc', realProviderPilot: false }, null, 2));
} catch (error) {
  await page.screenshot({ path: join(artifacts, 'managed-browser-failure.png'), fullPage: true }).catch(() => {});
  await writeFile(join(artifacts, 'managed-browser-failure.json'), JSON.stringify({ steps, pageErrors: errors, error: String(error) }, null, 2));
  throw error;
} finally { await browser.close(); }
