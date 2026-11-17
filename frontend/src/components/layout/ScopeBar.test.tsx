import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { useScopeStore } from '../../features/scope/scopeStore';
import { ScopeBar } from './ScopeBar';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/projectService', () => ({ projectService: projectServiceMock }));

const iteration = (id: number, name: string, project_id: number | null, start_date: string, end_date: string) => ({
    id, name, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
    project: project_id === null ? null : { id: project_id, name: project_id === 1 ? 'Agdash' : 'Beacon', status: 'active', health: 'green' },
});

// Today is 2026-11-16, so Sprint 2 of Agdash is the current iteration.
const ITERATIONS = [
    iteration(11, 'Sprint 1', 1, '2026-10-01', '2026-10-31'),
    iteration(12, 'Sprint 2', 1, '2026-11-01', '2026-11-30'),
    iteration(21, 'Launch', 2, '2026-09-01', '2026-09-30'),
];

const project = (id: number, name: string, sort_order: number, initiative: string | null) => ({
    id, name, sort_order, initiative: initiative === null ? null : { id: 100 + id, name: initiative },
});

const PROJECTS = [
    project(1, 'Agdash', 1, 'Platform'),
    project(2, 'Beacon', 2, 'Growth'),
    project(3, 'Cinder', 3, 'Platform'),
    project(4, 'Drift', 4, null),
];

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const locationText = () => screen.getByTestId('location').textContent;
const projectPicker = () => screen.getByRole('combobox', { name: 'Project' });
const iterationPicker = () => screen.getByRole('combobox', { name: 'Iteration' });
/** Lets the iterations load and the scope settle. */
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));

const renderBar = async (entry: string) => {
    const view = renderWithProviders(<><ScopeBar /><LocationProbe /></>, { initialEntries: [entry] });
    await waitFor(() => expect(screen.getByTestId('scope-bar')).not.toHaveTextContent('Loading'));
    await settle();
    return view;
};

describe('ScopeBar', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getAll.mockResolvedValue(PROJECTS);
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        vi.useRealTimers();
        useScopeStore.setState({ project: null, iteration: null });
    });

    describe('with the keyboard alone', () => {
        it('opens the Project picker, searches it and chooses a project, announcing the value', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=12');
            expect(projectPicker()).toHaveValue('Agdash');
            expect(projectPicker()).toHaveAttribute('aria-expanded', 'false');

            await user.tab();
            expect(projectPicker()).toHaveFocus();
            await user.keyboard('{ArrowDown}');
            expect(projectPicker()).toHaveAttribute('aria-expanded', 'true');
            expect(screen.getByRole('listbox', { name: 'Project' })).toBeInTheDocument();

            await user.keyboard('bea');
            expect(screen.getAllByRole('option').map(option => option.textContent)).toEqual(['Beacon']);
            expect(projectPicker()).toHaveAttribute('aria-activedescendant', screen.getByRole('option', { name: 'Beacon' }).id);

            await user.keyboard('{Enter}');
            await settle();
            expect(projectPicker()).toHaveAttribute('aria-expanded', 'false');
            expect(projectPicker()).toHaveValue('Beacon');
            expect(iterationPicker()).toHaveValue('Launch');
            expect(locationText()).toBe('/tasks?project=2&iteration=21');
        });

        it('opens the Iteration picker, searches it and chooses an iteration, announcing the value', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=12');
            expect(iterationPicker()).toHaveValue('Sprint 2');

            await user.tab();
            await user.tab();
            expect(iterationPicker()).toHaveFocus();
            await user.keyboard('{ArrowDown}');
            expect(iterationPicker()).toHaveAttribute('aria-expanded', 'true');

            await user.keyboard('sprint 1');
            expect(screen.getAllByRole('option').filter(option => !option.className.includes('scope-picker-action')).map(option => option.textContent))
                .toEqual([expect.stringContaining('Sprint 1')]);
            await user.keyboard('{Enter}');
            await settle();

            expect(iterationPicker()).toHaveValue('Sprint 1');
            expect(locationText()).toBe('/tasks?project=1&iteration=11');
        });

        it('moves with the arrow keys, closes with Escape without choosing, and chooses Backlog', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=12');
            await user.tab();
            await user.tab();
            await user.keyboard('{ArrowDown}');
            await user.keyboard('{ArrowDown}');
            await user.keyboard('{Escape}');
            expect(iterationPicker()).toHaveAttribute('aria-expanded', 'false');
            expect(iterationPicker()).toHaveValue('Sprint 2');
            expect(locationText()).toBe('/tasks?project=1&iteration=12');

            await user.keyboard('{ArrowDown}');
            await user.keyboard('{Home}{Enter}');
            await settle();
            expect(iterationPicker()).toHaveValue('Backlog');
            expect(locationText()).toBe('/tasks?project=1&iteration=backlog');
        });

        it('opens Plan from New iteration and Manage iterations', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=12');
            await user.tab();
            await user.tab();
            await user.keyboard('{ArrowDown}{End}{Enter}');
            await settle();
            expect(locationText()).toBe('/plan?panel=iterations&project=1&iteration=12');

            await user.keyboard('{ArrowDown}{End}{ArrowUp}{Enter}');
            await settle();
            expect(locationText()).toBe('/plan?create=1&project=1&iteration=12');
        });
    });

    describe('lists', () => {
        it('groups projects by initiative after All projects, and filters them by search', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=12');
            await user.click(projectPicker());

            const listbox = screen.getByRole('listbox', { name: 'Project' });
            expect(within(listbox).getAllByRole('option').map(option => option.textContent))
                .toEqual(['All projects', 'Beacon', 'Agdash', 'Cinder', 'Drift']);
            expect(within(listbox).getByRole('group', { name: 'Growth' })).toBeInTheDocument();
            expect(within(listbox).getByRole('group', { name: 'Platform' })).toBeInTheDocument();
            expect(within(listbox).getByRole('group', { name: 'No initiative' })).toBeInTheDocument();
            expect(within(listbox).getByRole('option', { name: 'Agdash' })).toHaveAttribute('aria-selected', 'true');

            await user.keyboard('platform');
            expect(within(listbox).getAllByRole('option').map(option => option.textContent)).toEqual(['Agdash', 'Cinder']);
        });

        it('lists Backlog, then the project\'s iterations with dates and a marker on the current one', async () => {
            const { user } = await renderBar('/tasks?project=1&iteration=11');
            await user.click(iterationPicker());

            const options = within(screen.getByRole('listbox', { name: 'Iteration' })).getAllByRole('option');
            expect(options.map(option => option.textContent)).toEqual([
                expect.stringMatching(/^Backlog/),
                expect.stringMatching(/^Sprint 2Current.*2026/),
                expect.stringMatching(/^Sprint 1.*2026/),
                'New iteration',
                'Manage iterations',
            ]);
            expect(within(options[1]!).getByText('Current')).toBeInTheDocument();
            expect(within(options[2]!).queryByText('Current')).not.toBeInTheDocument();
            expect(options[2]).toHaveAttribute('aria-selected', 'true');
        });

        it('names the project of each iteration when All projects is chosen', async () => {
            const { user } = await renderBar('/tasks?project=all&iteration=12');
            expect(iterationPicker()).toHaveValue('Sprint 2 · Agdash');
            await user.click(iterationPicker());
            expect(screen.getByRole('option', { name: /Launch · Beacon/ })).toBeInTheDocument();
        });
    });

    describe('where the scope is only shown', () => {
        it('renders text, with no combobox, on a workspace-wide page', async () => {
            await renderBar('/my-work?project=1&iteration=12');
            expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
            const bar = screen.getByTestId('scope-bar');
            expect(bar).toHaveAttribute('data-read-only', 'true');
            expect(bar).toHaveTextContent('Agdash');
            expect(bar).toHaveTextContent('Sprint 2');
        });
    });

    describe('a copied link', () => {
        it('opens the same scope in a browser that remembered a different one', async () => {
            // The first browser chooses Sprint 1 of Agdash and copies the address.
            const first = await renderBar('/analytics?project=1&iteration=12');
            await first.user.click(iterationPicker());
            await first.user.click(screen.getByRole('option', { name: /Sprint 1/ }));
            await settle();
            const copied = locationText()!;
            expect(copied).toBe('/analytics?project=1&iteration=11');
            first.unmount();

            // The second browser remembered Beacon, and opens the copied link.
            useScopeStore.setState({ project: 2, iteration: 21 });
            await renderBar(copied);

            expect(projectPicker()).toHaveValue('Agdash');
            expect(iterationPicker()).toHaveValue('Sprint 1');
            expect(locationText()).toBe(copied);
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 11 });
        });

        it('remembers the scope of a page without parameters and writes it into the address', async () => {
            useScopeStore.setState({ project: 2, iteration: 21 });
            await renderBar('/gantt');
            expect(projectPicker()).toHaveValue('Beacon');
            expect(iterationPicker()).toHaveValue('Launch');
            expect(locationText()).toBe('/gantt?project=2&iteration=21');
        });
    });
});
