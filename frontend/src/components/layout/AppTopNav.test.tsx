import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppTopNav } from './AppTopNav';
import { AppSidebar } from './AppSidebar';

import { Button } from '../../components/common/Button';
const planningSummaryMock = vi.hoisted(() => ({
    usePlanningNavigationSummary: vi.fn(),
}));

const triageServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const scopeServiceMocks = vi.hoisted(() => ({
    iterations: { getAll: vi.fn() },
    projects: { getAll: vi.fn() },
}));

vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => planningSummaryMock);
vi.mock('../../services/iterationService', () => ({ iterationService: scopeServiceMocks.iterations }));
vi.mock('../../services/projectService', () => ({ projectService: scopeServiceMocks.projects }));
vi.mock('../../services/triageService', () => ({ triageService: triageServiceMock }));
vi.mock('../../navigation/routeModules', async importOriginal => ({
    ...await importOriginal<typeof import('../../navigation/routeModules')>(),
    warmRouteModule: vi.fn(),
}));
vi.mock('../UserSessionBadge', () => ({
    UserSessionBadge: () => <Button type="button" variant="secondary">Account menu</Button>,
}));

const DESTINATION_NAMES = [
    'Overview', 'My Work', 'Triage',
    'Projects', 'Plan', 'Gantt',
    'Tasks', 'Analytics',
    'Team', 'Settings',
];

describe('AppTopNav', () => {
    beforeEach(() => {
        planningSummaryMock.usePlanningNavigationSummary.mockReset();
        planningSummaryMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { done: 6, total: 6, pct: 100 },
        });
        triageServiceMock.getAll.mockReset();
        triageServiceMock.getAll.mockResolvedValue([]);
        scopeServiceMocks.iterations.getAll.mockReset();
        scopeServiceMocks.iterations.getAll.mockResolvedValue([]);
        scopeServiceMocks.projects.getAll.mockReset();
        scopeServiceMocks.projects.getAll.mockResolvedValue([]);
    });

    it('holds the brand, a scope slot, Commands, Help and the account menu, left to right, with no tabs', () => {
        renderWithProviders(<AppTopNav />, { initialEntries: ['/roadmap'] });

        const bar = screen.getByTestId('app-navbar');
        const brand = screen.getByRole('link', { name: 'Go to WorkChord overview' });
        const slot = screen.getByTestId('topnav-scope-slot');
        const commands = screen.getByRole('button', { name: 'Open command menu' });
        const help = screen.getByRole('button', { name: 'Open help for Roadmap' });
        const account = screen.getByRole('button', { name: 'Account menu' });

        expect(brand).toHaveAttribute('href', '/');
        expect(within(slot).getByTestId('scope-bar')).toBeInTheDocument();
        expect(slot).toHaveAttribute('data-slot', 'scope-bar');
        const inOrder = [brand, slot, commands, help, account];
        for (let index = 1; index < inOrder.length; index += 1) {
            expect(
                inOrder[index - 1]!.compareDocumentPosition(inOrder[index]!) & Node.DOCUMENT_POSITION_FOLLOWING,
                `${index}`,
            ).toBeTruthy();
        }

        expect(within(bar).queryByRole('navigation')).not.toBeInTheDocument();
        expect(screen.queryByText('Delivery Hub')).not.toBeInTheDocument();
        expect(screen.queryByText('Timeline & Planning')).not.toBeInTheDocument();
        expect(screen.queryByText('Resource & Settings')).not.toBeInTheDocument();
    });

    it.each([
        ['/tasks', 'Tasks'],
        ['/roadmap', 'Projects'],
        ['/projects/9', 'Projects'],
        ['/plan/master', 'Plan'],
        ['/calendar', 'Settings'],
    ])('names the current destination on %s', (pathname, name) => {
        renderWithProviders(<AppTopNav />, { initialEntries: [pathname] });

        expect(screen.getByTestId('topnav-location')).toHaveTextContent(new RegExp(`^${name}$`));
    });

    it('names the page for a path no destination owns', () => {
        renderWithProviders(<AppTopNav />, { initialEntries: ['/missing'] });

        expect(screen.getByTestId('topnav-location').textContent).not.toBe('');
    });

    it('opens a drawer that lists the same ten destinations in one scroll', async () => {
        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        expect(within(drawer).getByRole('heading', { level: 2, name: 'Primary navigation' })).toBeVisible();
        expect(drawer.querySelectorAll('nav')).toHaveLength(1);
        expect(within(drawer).getAllByRole('link').map(link => link.textContent)).toEqual(DESTINATION_NAMES);
        expect(within(drawer).getAllByRole('group').map(group => group.getAttribute('aria-labelledby')
            && document.getElementById(group.getAttribute('aria-labelledby')!)?.textContent))
            .toEqual(['Plan', 'Deliver', 'Setup']);
        expect(within(drawer).getByRole('link', { name: 'Tasks' })).toHaveAttribute('aria-current', 'page');
        expect(within(drawer).queryByText('Work area homes')).not.toBeInTheDocument();
        expect(within(drawer).queryByText('Views')).not.toBeInTheDocument();
    });

    it('moves focus into the drawer, tabs through the destinations in order and wraps back to Close', async () => {
        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        const close = within(drawer).getByRole('button', { name: 'Close' });
        expect(close).toHaveFocus();

        const visited: string[] = [];
        for (let index = 0; index < DESTINATION_NAMES.length; index += 1) {
            await user.tab();
            visited.push(document.activeElement?.textContent ?? '');
        }
        expect(visited).toEqual(DESTINATION_NAMES);

        await user.tab();
        expect(close).toHaveFocus();
        await user.tab({ shift: true });
        expect(within(drawer).getByRole('link', { name: 'Settings' })).toHaveFocus();
    });

    it('closes on Escape and returns focus to the button that opened it', async () => {
        const { user } = renderWithProviders(<AppTopNav />, { initialEntries: ['/tasks'] });
        const trigger = screen.getByRole('button', { name: 'Open navigation menu' });
        await user.click(trigger);
        expect(trigger).toHaveAttribute('aria-expanded', 'true');

        await user.keyboard('{Escape}');

        expect(screen.queryByRole('dialog', { name: 'Primary navigation' })).not.toBeInTheDocument();
        expect(trigger).toHaveAttribute('aria-expanded', 'false');
        expect(trigger).toHaveFocus();
    });

    it('closes on navigating and moves focus to the page content', async () => {
        const { user } = renderWithProviders(
            <>
                <AppTopNav />
                <main id="workspace-main" tabIndex={-1}>Workspace</main>
            </>,
            { initialEntries: ['/tasks'] },
        );
        const trigger = screen.getByRole('button', { name: 'Open navigation menu' });
        await user.click(trigger);

        await user.click(within(screen.getByRole('dialog', { name: 'Primary navigation' }))
            .getByRole('link', { name: 'Analytics' }));

        expect(screen.queryByRole('dialog', { name: 'Primary navigation' })).not.toBeInTheDocument();
        await waitFor(() => expect(screen.getByRole('main')).toHaveFocus());
        expect(trigger).not.toHaveFocus();
    });

    it('shows the plan counter on the Plan item in the drawer and nowhere else', async () => {
        planningSummaryMock.usePlanningNavigationSummary.mockReturnValue({
            iterations: [{ id: 1 }],
            ready: { done: 2, total: 6, pct: 33 },
            isPlanProgressKnown: true,
        });
        const { user } = renderWithProviders(
            <>
                <AppTopNav />
                <AppSidebar />
            </>,
            { initialEntries: ['/gantt'] },
        );
        expect(screen.getAllByText('2/6')).toHaveLength(1);
        expect(screen.getByTestId('app-navbar').textContent).not.toMatch(/\d\/6/);
        await user.click(screen.getByRole('button', { name: 'Open navigation menu' }));

        const drawer = screen.getByRole('dialog', { name: 'Primary navigation' });
        expect(within(drawer).getByRole('link', { name: 'Plan' })).toHaveTextContent('2/6');
        expect(screen.getAllByText('2/6')).toHaveLength(2);
    });
});
