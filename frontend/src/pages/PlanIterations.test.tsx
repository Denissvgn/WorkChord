import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { ScopeBar } from '../components/layout/ScopeBar';
import PlanPage from './PlanPage';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getPlanningReadiness: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));

vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../services/planningInputService', () => ({ planningInputService: planningMock }));

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
        iterationServiceMock.getPlanningReadiness.mockReset();
        iterationServiceMock.getPlanningReadiness.mockRejectedValue(new Error('not needed'));
        planningMock.readInitial.mockReset();
        planningMock.readInitial.mockImplementation(async (_kind: string, id: number) => ({
            resource: ITERATIONS.find(item => item.id === id), resource_id: id, expected_revisions: { [id]: 1 }, complete: true,
        }));
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

    it('shows the new iteration form in the slide-over drawer, not in the page', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        await user.click(screen.getByRole('button', { name: 'New iteration' }));
        const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
        expect(drawer).toHaveAttribute('aria-modal', 'true');
        expect(within(drawer).getByLabelText('Iteration name')).toBeVisible();
        expect(within(drawer).getByRole('combobox', { name: 'Project scope' })).toBeVisible();
        expect(within(drawer).getByLabelText('Start date')).toBeVisible();
        expect(within(drawer).getByLabelText('End date')).toBeVisible();
        // The rest of the form waits under More.
        expect(within(drawer).getByRole('button', { name: 'More' })).toHaveAttribute('aria-expanded', 'false');
        expect(within(drawer).queryByRole('button', { name: 'Repeating series' })).not.toBeInTheDocument();
        expect(within(drawer).queryByLabelText('Manager email (for notifications)')).not.toBeInTheDocument();
        await user.click(within(drawer).getByRole('button', { name: 'More' }));
        expect(within(drawer).getByRole('button', { name: 'Repeating series' })).toBeVisible();
        expect(within(drawer).getByLabelText('Manager email (for notifications)')).toBeVisible();
        // No inline card: the list stays on the page behind the drawer.
        expect(screen.getByText('Launch')).toBeInTheDocument();
    });

    it('removes create=1 and keeps the scope when the drawer is closed', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21&create=1');
        const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        await settle();
        expect(formHeading()).not.toBeInTheDocument();
        expect(screen.getByTestId('location').textContent).toBe('/plan?panel=iterations&project=2&iteration=21');

        await user.click(screen.getByRole('button', { name: 'New iteration' }));
        await screen.findByRole('dialog', { name: 'Create new iteration' });
        await user.keyboard('{Escape}');
        await settle();
        expect(formHeading()).not.toBeInTheDocument();
        expect(screen.getByTestId('location').textContent).not.toContain('create=1');
    });

    it('asks before closing the drawer with unsaved changes', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21&create=1');
        const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
        await user.type(within(drawer).getByLabelText('Iteration name'), 'Draft');
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        await user.click(await screen.findByRole('button', { name: 'Keep editing' }));
        expect(screen.getByRole('dialog', { name: 'Create new iteration' })).toBeInTheDocument();
        await user.click(within(screen.getByRole('dialog', { name: 'Create new iteration' })).getByRole('button', { name: 'Close' }));
        await user.click(await screen.findByRole('button', { name: 'Discard changes' }));
        await settle();
        expect(formHeading()).not.toBeInTheDocument();
        expect(screen.getByTestId('location').textContent).not.toContain('create=1');
    });

    it('opens Edit in the drawer with the iteration and closes it again', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        await user.click(await screen.findByRole('button', { name: 'Edit' }));
        const drawer = await screen.findByRole('dialog', { name: 'Edit iteration' });
        await waitFor(() => expect(within(drawer).getByLabelText('Iteration name')).toHaveValue('Launch'));
        await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Edit iteration' })).not.toBeInTheDocument());
        expect(screen.getByTestId('location').textContent).toBe('/plan?panel=iterations&project=2&iteration=21');
    });

    it('lists only the iterations of the project in the scope bar, and all of them for All projects', async () => {
        const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
        expect(screen.getByRole('heading', { name: 'Launch' })).toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Sprint 2' })).not.toBeInTheDocument();

        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /Agdash/ }));
        await settle();
        expect(screen.getByRole('heading', { name: 'Sprint 2' })).toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Launch' })).not.toBeInTheDocument();

        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /^All projects/ }));
        await settle();
        expect(screen.getByRole('heading', { name: 'Sprint 2' })).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: 'Launch' })).toBeInTheDocument();
    });
});
