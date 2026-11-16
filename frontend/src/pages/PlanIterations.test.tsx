import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { ScopeBar } from '../components/layout/ScopeBar';
import PlanPage from './PlanPage';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/projectService', () => ({ projectService: projectServiceMock }));

const iteration = (id: number, name: string, project_id: number) => ({
    id, name, calendar_id: 1, project_id, start_date: '2026-11-01', end_date: '2026-11-30', working_days: 10,
    project: { id: project_id, name: project_id === 1 ? 'Agdash' : 'Beacon', status: 'active', health: 'green' },
});

const ITERATIONS = [iteration(12, 'Sprint 2', 1), iteration(21, 'Launch', 2)];
const PROJECTS = [
    { id: 1, name: 'Agdash', sort_order: 1, initiative: null },
    { id: 2, name: 'Beacon', sort_order: 2, initiative: null },
];

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));
const formHeading = () => screen.queryByRole('heading', { name: 'Create new iteration' });

describe('Plan iterations opened from the scope bar', () => {
    beforeEach(() => {
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getAll.mockResolvedValue(PROJECTS);
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
    });

    const renderPlan = async (entry: string) => {
        const view = renderWithProviders(
            <><ScopeBar /><PlanPage /><LocationProbe /></>,
            { initialEntries: [entry] },
        );
        await waitFor(() => expect(screen.getByTestId('scope-bar')).not.toHaveTextContent('Loading'));
        await settle();
        return view;
    };

    const chooseAction = async (user: ReturnType<typeof renderWithProviders>['user'], name: string) => {
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name }));
        await settle();
    };

    it('opens the form when New iteration is chosen while Plan already shows the iterations, and closes it on Manage iterations', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        expect(formHeading()).not.toBeInTheDocument();

        await chooseAction(user, 'New iteration');
        expect(screen.getByTestId('location').textContent).toContain('create=1');
        expect(formHeading()).toBeInTheDocument();

        await chooseAction(user, 'Manage iterations');
        expect(screen.getByTestId('location').textContent).not.toContain('create=1');
        expect(formHeading()).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'New iteration' })).toBeEnabled();
    });

    it('starts the new iteration on the project in the scope', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        await chooseAction(user, 'New iteration');
        const formProject = () => screen.getAllByRole('combobox').find(element => element.tagName === 'SELECT');
        await waitFor(() => expect(formProject()).toHaveValue('2'));
        expect(formProject()).toHaveDisplayValue('Beacon');
    });

    it('opens and closes the form from the page itself, keeping the scope in the link', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        await user.click(screen.getByRole('button', { name: 'New iteration' }));
        expect(formHeading()).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Cancel' }));
        expect(formHeading()).not.toBeInTheDocument();
        expect(screen.getByTestId('location').textContent).toBe('/plan?panel=iterations&project=2&iteration=21');
    });
});
