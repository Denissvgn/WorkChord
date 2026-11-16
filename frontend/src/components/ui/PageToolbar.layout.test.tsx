// @vitest-environment jsdom
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

const css = readFileSync(resolve(__dirname, '../../styles/planning-masters.css'), 'utf8');

describe('PageToolbar layout rules', () => {
    it('lets the filter controls wrap inside their slot instead of running into the view controls', () => {
        const rule = (selector: string) => new RegExp(`\\.wc ${selector.replace('.', '\\.')} \\{([^}]*)\\}`).exec(css)?.[1] ?? '';
        expect(rule('.wc-filter-controls')).toContain('flex-wrap: wrap');
        expect(rule('.wc-filter-controls')).not.toContain('nowrap');
        // The stacked arrangement must already apply at the 960px content width of a 1024px viewport.
        const breakpoint = Number(/@container \(max-width: (\d+)px\)\s*\{\s*\.wc \.wc-page-toolbar-search/.exec(css)?.[1]);
        expect(breakpoint).toBeGreaterThanOrEqual(960);
    });
});
