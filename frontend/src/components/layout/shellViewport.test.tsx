/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppTopNav } from './AppTopNav';
import { AppSidebar } from './AppSidebar';
import { Button } from '../common/Button';

const planningSummaryMock = vi.hoisted(() => ({ usePlanningNavigationSummary: vi.fn() }));

vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => planningSummaryMock);
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../navigation/routeModules', async importOriginal => ({
    ...await importOriginal<typeof import('../../navigation/routeModules')>(),
    warmRouteModule: vi.fn(),
}));
vi.mock('../UserSessionBadge', () => ({
    UserSessionBadge: () => <Button type="button" variant="secondary">Account menu</Button>,
}));

const css = readFileSync(resolve(process.cwd(), 'src/styles/planning-masters.css'), 'utf8');

const matchingBlock = (condition: string, width: number) => {
    const min = /min-width:\s*(\d+)px/.exec(condition);
    const max = /max-width:\s*(\d+)px/.exec(condition);
    if (!min && !max) return false;
    return (!min || width >= Number(min[1])) && (!max || width <= Number(max[1]));
};

/** The stylesheet with every top-level width media block either unwrapped (it applies at this width) or dropped. */
const stylesheetAtWidth = (width: number) => {
    let out = '';
    let index = 0;
    while (index < css.length) {
        const at = css.indexOf('@media', index);
        if (at === -1) { out += css.slice(index); break; }
        out += css.slice(index, at);
        const open = css.indexOf('{', at);
        let depth = 1;
        let cursor = open + 1;
        while (depth > 0 && cursor < css.length) {
            if (css[cursor] === '{') depth += 1;
            if (css[cursor] === '}') depth -= 1;
            cursor += 1;
        }
        if (matchingBlock(css.slice(at + 6, open), width)) out += css.slice(open + 1, cursor - 1);
        index = cursor;
    }
    return out;
};

const setViewport = (width: number) => {
    window.matchMedia = ((query: string) => ({
        matches: matchingBlock(query, width),
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        addListener: vi.fn(),
        removeListener: vi.fn(),
        onchange: null,
        dispatchEvent: vi.fn(),
    })) as typeof window.matchMedia;
    const style = document.createElement('style');
    style.dataset.viewport = String(width);
    style.textContent = stylesheetAtWidth(width);
    document.head.appendChild(style);
};

const display = (element: Element) => window.getComputedStyle(element).display;

describe('shell at fixed viewport widths', () => {
    const originalMatchMedia = window.matchMedia;

    beforeEach(() => {
        planningSummaryMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { done: 2, total: 6, pct: 33 },
            isPlanProgressKnown: true,
        });
    });

    afterEach(() => {
        window.matchMedia = originalMatchMedia;
        document.querySelectorAll('style[data-viewport]').forEach(node => node.remove());
    });

    const renderShell = () => renderWithProviders(
        <div className="wc">
            <AppTopNav />
            <div className="workspace"><AppSidebar /></div>
        </div>,
        { initialEntries: ['/plan'] },
    );

    it('shows the sidebar with the Plan counter and no menu button at 1024 x 768', () => {
        setViewport(1024);
        renderShell();

        const sidebar = document.querySelector('.sidebar')!;
        expect(display(sidebar)).not.toBe('none');
        expect(within(sidebar as HTMLElement).getByRole('link', { name: 'Plan' })).toHaveTextContent('2/6');
        expect(display(document.querySelector('.mobile-nav-trigger')!)).toBe('none');
    });

    it('hides the sidebar and offers the menu button at 1023 px', () => {
        setViewport(1023);
        renderShell();

        expect(display(document.querySelector('.sidebar')!)).toBe('none');
        expect(display(screen.getByRole('button', { name: 'Open navigation menu' }))).not.toBe('none');
    });
});
