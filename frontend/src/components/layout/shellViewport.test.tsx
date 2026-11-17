/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppTopNav } from './AppTopNav';
import { AppSidebar } from './AppSidebar';
import { Button } from '../common/Button';

const planningSummaryMock = vi.hoisted(() => ({ usePlanningNavigationSummary: vi.fn() }));
const scopeServiceMocks = vi.hoisted(() => ({
    iterations: { getAll: vi.fn() },
    projects: { getAll: vi.fn() },
}));

vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => planningSummaryMock);
vi.mock('../../services/iterationService', () => ({ iterationService: scopeServiceMocks.iterations }));
vi.mock('../../services/projectService', () => ({ projectService: scopeServiceMocks.projects }));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../navigation/routeModules', async importOriginal => ({
    ...await importOriginal<typeof import('../../navigation/routeModules')>(),
    warmRouteModule: vi.fn(),
}));
vi.mock('../UserSessionBadge', () => ({
    UserSessionBadge: () => <Button type="button" variant="secondary">Account menu</Button>,
}));

const css = readFileSync(resolve(process.cwd(), 'src/styles/planning-masters.css'), 'utf8');

type Viewport = { width: number; height: number };

/** Whether a width/height media condition holds at this viewport; other media features never match. */
const matchingBlock = (condition: string, { width, height }: Viewport) => {
    const bound = (feature: string) => {
        const found = new RegExp(`${feature}:\\s*(\\d+)px`).exec(condition);
        return found ? Number(found[1]) : undefined;
    };
    const limits = [
        [bound('min-width'), width, 1], [bound('max-width'), width, -1],
        [bound('min-height'), height, 1], [bound('max-height'), height, -1],
    ] as const;
    if (limits.every(([limit]) => limit === undefined)) return false;
    return limits.every(([limit, actual, sign]) => limit === undefined || (actual - limit) * sign >= 0);
};

/** The stylesheet with every top-level size media block either unwrapped (it applies at this viewport) or dropped. */
const stylesheetAt = (viewport: Viewport) => {
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
        if (matchingBlock(css.slice(at + 6, open), viewport)) out += css.slice(open + 1, cursor - 1);
        index = cursor;
    }
    return out;
};

const setViewport = (width: number, height = 768) => {
    const viewport = { width, height };
    vi.stubGlobal('innerWidth', width);
    vi.stubGlobal('innerHeight', height);
    window.matchMedia = ((query: string) => ({
        matches: matchingBlock(query, viewport),
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
    style.textContent = stylesheetAt(viewport);
    document.head.appendChild(style);
};

const display = (element: Element) => window.getComputedStyle(element).display;

/** No element from this one up to the document is display: none or visibility: hidden. */
const isRendered = (element: Element | null) => {
    for (let node = element; node; node = node.parentElement) {
        const style = window.getComputedStyle(node);
        if (style.display === 'none' || style.visibility === 'hidden') return false;
    }
    return true;
};

describe('shell at fixed viewport widths', () => {
    const originalMatchMedia = window.matchMedia;

    beforeEach(() => {
        planningSummaryMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { done: 2, total: 6, pct: 33 },
            isPlanProgressKnown: true,
        });
        scopeServiceMocks.projects.getAll.mockResolvedValue([]);
        scopeServiceMocks.iterations.getAll.mockResolvedValue([]);
    });

    afterEach(() => {
        window.matchMedia = originalMatchMedia;
        document.querySelectorAll('style[data-viewport]').forEach(node => node.remove());
    });

    const renderShell = (path = '/plan') => renderWithProviders(
        <div className="wc">
            <AppTopNav />
            <div className="workspace"><AppSidebar /></div>
        </div>,
        { initialEntries: [path] },
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

    it('changes Project and Iteration from the navigation drawer at 375 x 812', async () => {
        scopeServiceMocks.projects.getAll.mockResolvedValue([
            { id: 1, name: 'Agdash', sort_order: 1, initiative: null },
            { id: 2, name: 'Beacon', sort_order: 2, initiative: null },
        ]);
        const sprint = (id: number, name: string, projectId: number, start: string, end: string) => ({
            id, name, calendar_id: 1, project_id: projectId, start_date: start, end_date: end, working_days: 10,
            project: { id: projectId, name: projectId === 1 ? 'Agdash' : 'Beacon', status: 'active', health: 'green' },
        });
        scopeServiceMocks.iterations.getAll.mockResolvedValue([
            sprint(11, 'Sprint 1', 1, '2026-10-01', '2026-10-31'),
            sprint(21, 'Launch', 2, '2026-09-01', '2026-09-30'),
        ]);
        setViewport(375, 812);
        expect([window.innerWidth, window.innerHeight]).toEqual([375, 812]);
        const { user } = renderShell('/plan?project=all&iteration=backlog');

        // The bar shows the page name instead of the scope, and the sidebar is folded away.
        expect(display(screen.getByTestId('topnav-scope-slot'))).toBe('none');
        expect(display(screen.getByTestId('topnav-location'))).toBe('block');
        expect(display(document.querySelector('.sidebar')!)).toBe('none');

        const menu = screen.getByRole('button', { name: 'Open navigation menu' });
        expect(display(menu)).toBe('inline-flex');
        await user.click(menu);

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        const scope = within(drawer).getByTestId('mobile-nav-scope');
        const projectPicker = () => within(scope).getByRole('combobox', { name: 'Project' });
        const iterationPicker = () => within(scope).getByRole('combobox', { name: 'Iteration' });
        await waitFor(() => expect(projectPicker()).toHaveValue('All projects'));

        // The drawer's pickers are the only ones a phone user can reach, and their labels show.
        expect(screen.getAllByRole('combobox', { name: 'Project' })).toEqual([projectPicker()]);
        expect(screen.getAllByRole('combobox', { name: 'Iteration' })).toEqual([iterationPicker()]);
        for (const [picker, name] of [[projectPicker(), 'Project'], [iterationPicker(), 'Iteration']] as const) {
            expect(isRendered(picker)).toBe(true);
            const label = picker.closest('.scope-picker')!.querySelector('.scope-picker-label')!;
            expect(label).toHaveTextContent(name);
            expect(window.getComputedStyle(label).position).toBe('static');
            expect(isRendered(label)).toBe(true);
        }

        await user.click(projectPicker());
        await user.click(await within(scope).findByRole('option', { name: /Beacon/ }));
        await waitFor(() => expect(projectPicker()).toHaveValue('Beacon'));
        // Choosing a project moves Iteration to that project's current iteration; change it from there.
        await waitFor(() => expect(iterationPicker()).toHaveValue('Launch'));

        await user.click(iterationPicker());
        await user.click(await within(scope).findByRole('option', { name: /Backlog/ }));
        await waitFor(() => expect(iterationPicker()).toHaveValue('Backlog'));
        expect(isRendered(drawer)).toBe(true);
    });
});
