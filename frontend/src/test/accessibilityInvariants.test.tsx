import { act, waitFor } from '@testing-library/react';
import { getRoles } from '@testing-library/dom';
import { computeAccessibleName } from 'dom-accessibility-api';
import { afterEach, describe, expect, it, vi } from 'vitest';
import App from '../App';
import { getDestinationForPath } from '../navigation/destinations';
import { mapLegacyPath } from '../navigation/legacyPaths';
import {
    accessibleNameViolations,
    headingOrderViolations,
    summaryNameViolations,
} from './accessibilityInvariants';
import { renderWithProviders } from './renderWithProviders';
import { routeRegistry } from './routeRegistry';
import { installWorkspaceApi } from './workspaceApi';

afterEach(() => { vi.restoreAllMocks(); });

describe('accessibility invariants', () => {
    // These cases write markup straight into the body; the route cases below render through React.
    afterEach(() => { document.body.innerHTML = ''; });

    it('reports empty and duplicate names within the same role', () => {
        document.body.innerHTML = `
            <button aria-label="Refresh"></button>
            <button>Refresh</button>
            <a href="/one"></a>
        `;

        expect(accessibleNameViolations(document.body)).toEqual([
            { role: 'button', names: ['Refresh', 'Refresh'] },
            { role: 'link', names: [''] },
        ]);
    });

    it('keeps equal names valid when their roles differ', () => {
        document.body.innerHTML = `
            <nav aria-label="Planning"></nav>
            <aside aria-label="Planning"></aside>
            <button>Refresh</button>
            <a href="/refresh">Open refresh</a>
        `;

        expect(accessibleNameViolations(document.body)).toEqual([]);
    });

    it('accepts equal link names only when the links lead to the same place', () => {
        document.body.innerHTML = `
            <a href="/projects">Projects</a>
            <a href="/projects">Projects</a>
        `;
        expect(accessibleNameViolations(document.body)).toEqual([]);

        document.body.innerHTML = `
            <a href="/projects">Projects</a>
            <a href="/projects/1">Projects</a>
        `;
        expect(accessibleNameViolations(document.body)).toEqual([
            { role: 'link', names: ['Projects', 'Projects'] },
        ]);
    });

    it('checks disclosure summaries outside the role map', () => {
        document.body.innerHTML = `
            <details><summary>Runtime details</summary></details>
            <details><summary>Runtime details</summary></details>
        `;

        expect(summaryNameViolations(document.body)).toEqual([
            'Runtime details',
        ]);
    });

    it('reports headings that skip a level', () => {
        document.body.innerHTML = '<h1>Page</h1><h2>Section</h2><h4>Detail</h4><h2>Next</h2><h3>Part</h3>';

        expect(headingOrderViolations(document.body)).toEqual(['h4 Detail']);
    });
});

// A concrete path for a route pattern, so `/projects/:projectId` is opened as `/projects/1`.
const samplePath = (pattern: string) => pattern.replace(/:[^/]+/g, match => (match === ':publicId' ? 'shared-plan' : '1'));

const PAGE = { has_more: false, next_after_id: null, upper_id: 0 };
const TRIAGE_ITEM = {
    id: 1, title: 'Export the weekly report', description: null, source: 'email', status: 'new', labels: [], metadata_json: {},
    request_count: 0, created_at: '2026-08-01T00:00:00Z', updated_at: '2026-08-01T00:00:00Z',
};

/** What the shell and the pages read beyond the shared workspace: the session, the inbox and the setup lists. */
const SHELL_AND_PAGE_READS: Array<[RegExp, () => unknown]> = [
    [/^\/session\/whoami$/, () => ({
        id: 1, public_id: 'guest0001', display_name: 'Guest', authenticated: false, principal_id: null,
        created_at: '2026-08-01T00:00:00Z', last_seen_at: '2026-08-01T00:00:00Z',
    })],
    [/^\/triage$/, () => [TRIAGE_ITEM]],
    [/^\/triage\/\d+\/(duplicate-suggestions|classification-suggestions)$/, () => []],
    [/^\/request-source-links$/, () => []],
    [/^\/initiatives$/, () => []],
    [/^\/projects\/portfolio-summaries\/page$/, () => ({ ...PAGE, items: [] })],
    [/^\/calendars$/, () => [{ id: 1, name: 'Default', year: 2026, holidays: [], weekend_days: [5, 6], short_days: [] }]],
    [/^\/tasks\/planning-inputs\/calendar\/\d+\/context$/, () => ({})],
    [/^\/team-member-profiles$/, () => []],
    [/^\/tasks\/my-work$/, () => ({ state: 'ready', queues: {}, has_more: false, next_after_id: null })],
    [/^\/(tasks\/review-queue|notifications)$/, () => ({ ...PAGE, items: [] })],
];

/** Pages that open outside the workspace shell, without its sidebar and top bar. */
const BARE_ROUTES = new Set(['/welcome', '/plan/share/:publicId', '/mobile/connect']);

describe('accessibility invariants on every route', () => {
    it.each(routeRegistry)('route $path names its landmarks and controls and keeps one h1', async ({ path }) => {
        const { unplanned } = installWorkspaceApi(SHELL_AND_PAGE_READS);
        const sample = samplePath(path === '*' ? '/missing' : path);
        const { container } = renderWithProviders(<App />, { initialEntries: [sample] });

        await waitFor(() => expect(container.querySelector('[data-testid="page-header"]')).not.toBeNull(), { timeout: 20_000 });
        // Late reads (counters, suggestions) settle before the page is read.
        await act(() => new Promise(resolve => setTimeout(resolve, 100)));

        const page = document.body;
        expect(unplanned).toEqual([]);
        expect(Array.from(page.querySelectorAll('h1')).map(heading => heading.textContent?.trim())).toHaveLength(1);
        expect(headingOrderViolations(page)).toEqual([]);
        expect(getRoles(page).main ?? []).toHaveLength(1);
        expect(accessibleNameViolations(page)).toEqual([]);
        expect(summaryNameViolations(page)).toEqual([]);
        expect(Array.from(page.querySelectorAll('[tabindex]'))
            .filter(element => Number(element.getAttribute('tabindex')) > 0)).toEqual([]);

        if (BARE_ROUTES.has(path)) return;

        // The shell: a banner, the named sidebar and its navigation, and the current destination marked.
        const roles = getRoles(page);
        // A header is a banner only outside sectioning content, which the role map does not consider.
        const banners = Array.from(page.querySelectorAll('header, [role="banner"]'))
            .filter(element => element.getAttribute('role') === 'banner' || !element.parentElement?.closest('article, aside, main, nav, section'));
        expect(banners).toHaveLength(1);
        const navigationNames = (roles.navigation ?? []).map(element => computeAccessibleName(element));
        expect(navigationNames).toContain('Primary navigation');
        // An old path opens the destination it redirects to.
        const opened = (mapLegacyPath(sample, '') ?? sample).split('?')[0];
        const destination = getDestinationForPath(opened);
        const current = Array.from(page.querySelectorAll('[data-testid="app-sidebar"] [aria-current="page"]'))
            .map(element => element.getAttribute('data-destination'));
        expect(current).toEqual(destination ? [destination.id] : []);
    }, 30_000);
});
