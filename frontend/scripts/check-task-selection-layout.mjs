// Checks in a real browser that every task row shows its selection control at rest and that
// selecting tasks does not move the list. It drives headless Chrome over the DevTools protocol,
// so it needs no extra package.
//
// Start the app with a local workspace that has an iteration with tasks (ideally one with
// subtasks), start Chrome with remote debugging, then run:
//
//   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
//     --remote-debugging-port=9222 --remote-allow-origins='*' --lang=en-US --user-data-dir=<dir>
//   node scripts/check-task-selection-layout.mjs --app http://127.0.0.1:5173 \
//     --path '/tasks?iteration=1' [--devtools http://127.0.0.1:9222] [--shots <dir>] [--max-first-row 200]
//
// For each width (1440 and 1024, at 900 px high), in the page and in the full-screen workspace,
// it records every row's top edge, ticks two tasks with real pointer clicks, waits for the
// selection bar, opens Assign, and fails when any row moved, any row has no visible checkbox, or
// a control in the bar is cut off or covered.
//
// npm run test:run covers the same rule without a browser (TasksPage.toolbar.test.tsx); this script
// confirms it with real layout.

import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const arg = (name, fallback) => {
    const index = process.argv.indexOf(`--${name}`);
    return index > 0 ? process.argv[index + 1] : fallback;
};
const appUrl = arg('app');
const pagePath = arg('path', '/tasks');
const devtoolsUrl = arg('devtools', 'http://127.0.0.1:9222');
const shotsDir = arg('shots');
const maxFirstRow = Number(arg('max-first-row', '200'));
const widths = [1440, 1024];
const height = 900;

if (!appUrl) {
    console.error('Usage: node scripts/check-task-selection-layout.mjs --app <url> [--path <path>] [--devtools <url>] [--shots <dir>]');
    process.exit(2);
}
if (shotsDir) mkdirSync(shotsDir, { recursive: true });

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const openTab = async () => {
    const tab = await (await fetch(`${devtoolsUrl}/json/new?about:blank`, { method: 'PUT' })).json();
    const socket = new WebSocket(tab.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
    let nextId = 0;
    const pending = new Map();
    socket.onmessage = event => {
        const message = JSON.parse(event.data);
        if (message.id && pending.has(message.id)) {
            const { resolve, reject } = pending.get(message.id);
            pending.delete(message.id);
            if (message.error) reject(new Error(message.error.message));
            else resolve(message.result);
        }
    };
    const send = (method, params = {}) => new Promise((resolve, reject) => {
        const id = ++nextId;
        pending.set(id, { resolve, reject });
        socket.send(JSON.stringify({ id, method, params }));
    });
    const evaluate = async expression => {
        const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
        if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
        return result.result.value;
    };
    const close = async () => { socket.close(); await fetch(`${devtoolsUrl}/json/close/${tab.id}`); };
    return { send, evaluate, close };
};

// Reads every row: its top edge, and whether its checkbox shows, is off, and says why.
const READ_ROWS = `(() => [...document.querySelectorAll('[data-task-row]')]
    .filter(row => row.getClientRects().length > 0)
    .map(row => {
        const box = row.querySelector('input[type=checkbox]');
        const rect = box && box.getBoundingClientRect();
        const style = box && getComputedStyle(box);
        const describedBy = box && box.getAttribute('aria-describedby');
        return {
            id: row.getAttribute('data-task-row'),
            title: (box?.getAttribute('aria-label') ?? '').replace(/^[^:]*: /, ''),
            top: row.getBoundingClientRect().top,
            checkboxVisible: Boolean(rect && rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && Number(style.opacity) > 0),
            disabled: Boolean(box && box.disabled),
            reason: describedBy ? document.getElementById(describedBy)?.textContent ?? '' : '',
        };
    }))()`;

const waitFor = async (tab, expression, timeoutMs = 30000) => {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
        if (await tab.evaluate(expression)) return true;
        await sleep(200);
    }
    return false;
};

const click = async (tab, rowId) => {
    const point = await tab.evaluate(`(() => {
        const rect = document.querySelector('[data-task-row="${rowId}"] input[type=checkbox]').getBoundingClientRect();
        return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
    })()`);
    await tab.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: point.x, y: point.y });
    await tab.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: point.x, y: point.y, button: 'left', clickCount: 1 });
    await tab.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: point.x, y: point.y, button: 'left', clickCount: 1 });
};

const screenshot = async (tab, name) => {
    if (!shotsDir) return;
    const { data } = await tab.send('Page.captureScreenshot', { format: 'png' });
    writeFileSync(join(shotsDir, `${name}.png`), Buffer.from(data, 'base64'));
};

const failures = [];
const fail = message => { failures.push(message); console.log(`  FAIL ${message}`); };

const checkScenario = async (width, fullScreen) => {
    const label = `${width}${fullScreen ? '-fullscreen' : ''}`;
    const tab = await openTab();
    try {
        await tab.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
        const url = new URL(pagePath, appUrl);
        if (fullScreen) url.searchParams.set('fullscreen', '1');
        await tab.send('Page.navigate', { url: url.toString() });
        if (!await waitFor(tab, `document.querySelectorAll('[data-task-row]').length > 0`)) {
            fail(`${label}: no task rows rendered at ${url}`);
            return;
        }
        // Let late layout (fonts, counts, the scope bar) settle before the first reading.
        await sleep(1500);
        // The pointer rests away from the rows, so nothing is revealed by hover.
        await tab.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: width - 4, y: height - 4 });
        await sleep(300);

        const before = await tab.evaluate(READ_ROWS);
        await screenshot(tab, `${label}-rest`);
        const firstTop = Math.round(before[0].top);
        console.log(`${label}: ${before.length} rows, first row top ${firstTop} px`);
        if (!fullScreen && width === 1440 && firstTop > maxFirstRow) fail(`${label}: first row starts at ${firstTop} px, over ${maxFirstRow} px`);

        for (const row of before) {
            if (!row.checkboxVisible) fail(`${label}: row "${row.title}" shows no checkbox at rest`);
            if (row.disabled && !row.reason) fail(`${label}: row "${row.title}" has an off checkbox with no reason`);
        }
        const off = before.filter(row => row.disabled);
        console.log(`  checkboxes at rest: ${before.filter(row => row.checkboxVisible).length}/${before.length} (off with a reason: ${off.map(row => `"${row.title}"`).join(', ') || 'none'})`);
        if (off[0]) console.log(`  reason: ${off[0].reason}`);

        const selectable = before.filter(row => !row.disabled);
        const topsBefore = before.map(row => Math.round(row.top));
        console.log(`  tops before: [${topsBefore.join(', ')}]`);
        for (const [step, row] of selectable.slice(0, 2).entries()) {
            await click(tab, row.id);
            const count = step + 1;
            if (!await waitFor(tab, `[...document.querySelectorAll('[data-testid=task-bulk-operations]')].some(bar => bar.getClientRects().length > 0 && bar.textContent.includes('${count}'))`, 5000)) {
                fail(`${label}: the selection bar did not show ${count} selected`);
            }
            await sleep(400);
            const after = await tab.evaluate(READ_ROWS);
            const topsAfter = after.map(item => Math.round(item.top));
            const moved = after.filter((item, index) => before[index]?.id !== item.id || Math.abs(item.top - before[index].top) > 0.5);
            console.log(`  after ticking "${row.title}" (${count} selected): tops [${topsAfter.join(', ')}], moved rows: ${moved.length}`);
            if (after.length !== before.length) fail(`${label}: ${before.length} rows before, ${after.length} after selecting`);
            for (const item of moved) fail(`${label}: row "${item.title}" moved after selecting ${count}`);
            const barBox = await tab.evaluate(`(() => { const bar = [...document.querySelectorAll('[data-testid=task-bulk-operations]')].find(b => b.getClientRects().length > 0); if (!bar) return null; const r = bar.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom) }; })()`);
            if (barBox) {
                console.log(`  selection bar: ${barBox.top}-${barBox.bottom} px`);
                if (barBox.bottom > before[0].top + 0.5) fail(`${label}: the selection bar (bottom ${barBox.bottom}) covers the first row (top ${firstTop})`);
            }
        }
        if (fullScreen) {
            // The bar must leave the way out of full screen in reach (the browser runs in English).
            const exitReachable = await tab.evaluate(`(() => {
                const button = [...document.querySelectorAll('button')].find(b => b.textContent.includes('Exit full screen'));
                if (!button) return false;
                const r = button.getBoundingClientRect();
                return button.contains(document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2));
            })()`);
            console.log(`  Exit full screen reachable while selecting: ${exitReachable}`);
            if (!exitReachable) fail(`${label}: the selection bar covers Exit full screen`);
        }
        await screenshot(tab, `${label}-selected`);

        // Opening an editor makes the bar taller: it must stay on screen and usable, and the rows still must not move.
        const assignPoint = await tab.evaluate(`(() => {
            const bar = [...document.querySelectorAll('[data-testid=task-bulk-operations]')].find(b => b.getClientRects().length > 0);
            const button = bar && [...bar.querySelectorAll('button')].find(b => b.textContent.trim() === 'Assign');
            if (!button) return null;
            const r = button.getBoundingClientRect();
            return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
        })()`);
        if (!assignPoint) {
            fail(`${label}: no Assign button in the selection bar`);
        } else {
            await tab.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: assignPoint.x, y: assignPoint.y });
            await tab.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: assignPoint.x, y: assignPoint.y, button: 'left', clickCount: 1 });
            await tab.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: assignPoint.x, y: assignPoint.y, button: 'left', clickCount: 1 });
            if (!await waitFor(tab, `Boolean(document.querySelector('[data-testid=task-bulk-operations] select[aria-label="Choose assignee"]'))`, 5000)) {
                fail(`${label}: Assign did not open its editor`);
            } else {
                await sleep(400);
                const editor = await tab.evaluate(`(() => {
                    const bar = [...document.querySelectorAll('[data-testid=task-bulk-operations]')].find(b => b.getClientRects().length > 0);
                    const r = bar.getBoundingClientRect();
                    // Every control in the bar must be inside the viewport with nothing outside the bar on top of it.
                    // (An off control such as Apply before a choice takes no pointer events, so the bar itself is hit there.)
                    const hidden = [...bar.querySelectorAll('button, select, input')].filter(control => {
                        const c = control.getBoundingClientRect();
                        if (c.width === 0 || c.height === 0) return false;
                        const x = c.left + c.width / 2, y = c.top + c.height / 2;
                        const inView = c.top >= 0 && c.bottom <= innerHeight && c.left >= 0 && c.right <= innerWidth;
                        const onTop = document.elementFromPoint(x, y);
                        return !inView || !(control.disabled ? bar.contains(onTop) : control.contains(onTop));
                    }).map(control => control.getAttribute('aria-label') || control.textContent.trim());
                    return { top: Math.round(r.top), bottom: Math.round(r.bottom), controls: bar.querySelectorAll('button, select, input').length, hidden };
                })()`);
                console.log(`  with Assign open: bar ${editor.top}-${editor.bottom} px, ${editor.controls} controls, cut off or covered: ${editor.hidden.length ? editor.hidden.join(', ') : 'none'}`);
                if (editor.top < 0 || editor.bottom > height) fail(`${label}: with Assign open the bar runs off screen (${editor.top}-${editor.bottom} px)`);
                for (const name of editor.hidden) fail(`${label}: with Assign open, "${name}" is cut off or covered`);
                const after = await tab.evaluate(READ_ROWS);
                const moved = after.filter((item, index) => before[index]?.id !== item.id || Math.abs(item.top - before[index].top) > 0.5);
                console.log(`  with Assign open: tops [${after.map(item => Math.round(item.top)).join(', ')}], moved rows: ${moved.length}`);
                for (const item of moved) fail(`${label}: row "${item.title}" moved when Assign opened`);
                await screenshot(tab, `${label}-assign`);
            }
        }
    } finally {
        await tab.close();
    }
};

for (const width of widths) {
    for (const fullScreen of [false, true]) await checkScenario(width, fullScreen);
}

if (failures.length > 0) {
    console.log(`\n${failures.length} failure(s)`);
    process.exit(1);
}
console.log('\nPASS: every row shows its checkbox at rest, and selecting tasks moves no row.');
