// @vitest-environment jsdom
import { execFileSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { FilterBar } from './FilterBar';
import type { FilterBarFilter } from './FilterBar';
import { PageToolbar } from './PageToolbar';
import { ViewSwitch } from './ViewSwitch';

const css = readFileSync(resolve(__dirname, '../../styles/planning-masters.css'), 'utf8');
const tokens = readFileSync(resolve(__dirname, '../../styles/globals.css'), 'utf8');

const filter = (id: string): FilterBarFilter => ({
    id,
    label: `Filter ${id}`,
    value: '',
    options: [{ value: 'a', label: 'Option A' }, { value: 'b', label: 'Option B' }],
});

const FullToolbar = () => (
    <PageToolbar
        label="Controls"
        search={<input className="input" aria-label="Search" placeholder="Search" />}
        filters={
            <FilterBar
                filters={['one', 'two', 'three', 'four', 'five', 'six'].map(filter)}
                onChange={() => {}}
                onClear={() => {}}
            />
        }
        viewSwitch={
            <ViewSwitch
                label="View"
                value="list"
                onChange={() => {}}
                options={[{ value: 'list', label: 'List' }, { value: 'board', label: 'Board' }, { value: 'calendar', label: 'Calendar' }]}
            />
        }
        viewOptions={<button type="button" className="btn">Density</button>}
    />
);

const chromePath = [process.env.CHROME_BIN, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium']
    .find((path): path is string => Boolean(path) && existsSync(path as string));

type Box = { name: string; left: number; right: number; top: number; bottom: number };

const measureSlots = (markup: string, contentWidth: number): Box[] => {
    const dir = mkdtempSync(join(tmpdir(), 'toolbar-layout-'));
    try {
        const page = `<!doctype html><html><head><meta charset="utf-8"><style>${tokens}\n${css}
html,body{margin:0}</style></head><body><div class="wc"><div id="host" style="width:${contentWidth}px">${markup}</div></div>
<script>
const boxes=[];
const pick=(name,sel)=>document.querySelectorAll(sel).forEach(el=>{const r=el.getBoundingClientRect();boxes.push({name,left:r.left,right:r.right,top:r.top,bottom:r.bottom});});
pick('search','.wc-page-toolbar-search');
pick('filters','.wc-page-toolbar-filters');
pick('end','.wc-page-toolbar-end');
pick('filter-control','.wc-filter-controls > *');
pick('end-control','.wc-page-toolbar-end button');
const out=document.createElement('pre');out.id='measure';out.textContent=JSON.stringify(boxes);document.body.appendChild(out);
</script></body></html>`;
        const file = join(dir, 'page.html');
        writeFileSync(file, page);
        const dom = execFileSync(chromePath as string, [
            '--headless=new', '--disable-gpu', '--no-sandbox', `--user-data-dir=${join(dir, 'profile')}`,
            `--window-size=${contentWidth + 40},900`, '--virtual-time-budget=2000', '--dump-dom', `file://${file}`,
        ], { encoding: 'utf8', timeout: 60000, stdio: ['ignore', 'pipe', 'ignore'] });
        const match = /<pre id="measure">([\s\S]*?)<\/pre>/.exec(dom);
        if (!match) throw new Error('Chrome did not report a measurement');
        return JSON.parse(match[1].replace(/&quot;/g, '"').replace(/&amp;/g, '&')) as Box[];
    } finally {
        rmSync(dir, { recursive: true, force: true });
    }
};

const overlaps = (a: Box, b: Box) => a.left < b.right - 0.5 && b.left < a.right - 0.5 && a.top < b.bottom - 0.5 && b.top < a.bottom - 0.5;

describe('PageToolbar layout with every slot filled', () => {
    it('lets the filter controls wrap inside their slot instead of running into the view controls', () => {
        const rule = (selector: string) => new RegExp(`\\.wc ${selector.replace('.', '\\.')} \\{([^}]*)\\}`).exec(css)?.[1] ?? '';
        expect(rule('.wc-filter-controls')).toContain('flex-wrap: wrap');
        expect(rule('.wc-filter-controls')).not.toContain('nowrap');
        // The stacked arrangement must already apply at the 960px content width of a 1024px viewport.
        const breakpoint = Number(/@container \(max-width: (\d+)px\)\s*\{\s*\.wc \.wc-page-toolbar-search/.exec(css)?.[1]);
        expect(breakpoint).toBeGreaterThanOrEqual(960);
    });

    it.skipIf(!chromePath)('keeps search, filters and view controls from overlapping from 800px to 1600px of content width', () => {
        const { container } = renderWithProviders(<FullToolbar />);
        expect(screen.getByRole('group', { name: 'Controls' })).toBeInTheDocument();
        expect(container.querySelectorAll('.wc-filter-select')).toHaveLength(5);
        const markup = container.innerHTML;

        for (const width of [800, 960, 1100, 1190, 1280, 1600]) {
            const boxes = measureSlots(markup, width);
            const slots = boxes.filter(box => ['search', 'filters', 'end'].includes(box.name));
            expect(slots.map(box => box.name).sort()).toEqual(['end', 'filters', 'search']);
            for (let i = 0; i < slots.length; i++) {
                for (let j = i + 1; j < slots.length; j++) {
                    expect(overlaps(slots[i], slots[j]), `${slots[i].name} overlaps ${slots[j].name} at ${width}px`).toBe(false);
                }
            }
            // Every control sits inside its slot and none spills past the toolbar's right edge.
            for (const box of boxes) expect(box.right, `${box.name} spills out at ${width}px`).toBeLessThanOrEqual(width + 0.5);
            const controls = boxes.filter(box => box.name === 'filter-control' || box.name === 'end-control');
            for (let i = 0; i < controls.length; i++) {
                for (let j = i + 1; j < controls.length; j++) {
                    expect(overlaps(controls[i], controls[j]), `controls ${i} and ${j} overlap at ${width}px`).toBe(false);
                }
            }
        }
    }, 120000);
});
