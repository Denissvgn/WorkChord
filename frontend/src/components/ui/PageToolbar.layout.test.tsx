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

    it('keeps a compact toolbar on one row at the content width of a 1024px viewport', () => {
        const compactRule = (selector: string) => new RegExp(`\\.wc \\.wc-page-toolbar\\.is-compact ${selector.replace(/\./g, '\\.')} \\{([^}]*)\\}`).exec(css)?.[1] ?? '';
        // Quick filters size to their text, capped, instead of to their longest option.
        expect(compactRule('.wc-filter-controls > .wc-filter-select')).toContain('field-sizing: content');
        expect(compactRule('.wc-filter-controls > .wc-filter-select')).toContain('max-width: 8rem');
        // The controls stay one block, and the chips take their own line under the row.
        expect(compactRule('.wc-filter-controls')).toContain('flex-wrap: nowrap');
        expect(css).toMatch(/\.wc \.wc-page-toolbar\.is-compact \.wc-filter-chips,[^{]*\{[^}]*flex-basis: 100%/);
        // It stacks only below the 992px of content a 1024px viewport leaves, not at the default 1180px.
        const breakpoint = Number(/@container \(max-width: (\d+)px\)\s*\{\s*\.wc \.wc-page-toolbar\.is-compact \.wc-page-toolbar-search/.exec(css)?.[1]);
        expect(breakpoint).toBeLessThan(992);
        expect(breakpoint).toBeGreaterThanOrEqual(800);
    });
});
