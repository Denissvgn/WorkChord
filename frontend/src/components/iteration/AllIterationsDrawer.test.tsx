import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { AxiosError } from 'axios';
import { renderWithProviders } from '../../test/renderWithProviders';
import { useScopeStore } from '../../features/scope/scopeStore';
import { AllIterationsDrawer } from './AllIterationsDrawer';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getPlanningReadiness: vi.fn(), delete: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
const exportMock = vi.hoisted(() => ({ exportIteration: vi.fn(), previewImport: vi.fn(), importIteration: vi.fn(), importIntoIteration: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planningMock }));
vi.mock('../../services/exportService', () => ({ exportService: exportMock }));

const iteration = (id: number, name: string, project_id: number) => ({
    id, name, calendar_id: 1, project_id, start_date: '2026-11-01', end_date: '2026-11-30', working_days: 10,
    project: { id: project_id, name: project_id === 1 ? 'Agdash' : 'Beacon', status: 'active', health: 'green' },
});
const ITERATIONS = [iteration(12, 'Sprint 2', 1), iteration(21, 'Launch', 2)];

const readiness = (id: number, overrides: Record<string, unknown> = {}) => ({
    iteration_id: id, team_member_count: 2, team_capacity_hours: 120, planned_hours: 90, assigned_hours: 80,
    team_members_no_capacity: 0, task_count: 7, tasks_without_assignee: 0, tasks_without_effort: 0,
    has_schedule: true, risk_count: 0, ...overrides,
});

const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));

const renderDrawer = (props: Partial<React.ComponentProps<typeof AllIterationsDrawer>> = {}) => {
    const handlers = { onOpen: vi.fn(), onEdit: vi.fn(), onClose: vi.fn() };
    const view = renderWithProviders(<AllIterationsDrawer {...handlers} {...props} />);
    return { ...view, ...handlers };
};

describe('All iterations drawer', () => {
    beforeEach(() => {
        for (const mock of [iterationServiceMock, projectServiceMock, planningMock, exportMock]) {
            Object.values(mock).forEach(fn => fn.mockReset());
        }
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        iterationServiceMock.getPlanningReadiness.mockImplementation(async (id: number) => readiness(id));
        iterationServiceMock.delete.mockResolvedValue(undefined);
        projectServiceMock.getAll.mockResolvedValue([{ id: 2, name: 'Beacon', sort_order: 1, initiative: null }]);
        planningMock.readInitial.mockImplementation(async (_kind: string, id: number) => ({
            resource: ITERATIONS.find(item => item.id === id), resource_id: id, expected_revisions: { [id]: 4 }, complete: true,
        }));
        useScopeStore.setState({ project: 'all', iteration: 12 });
    });

    afterEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
        vi.restoreAllMocks();
    });

    it('lists every iteration with planned hours, capacity and task count, and a row action set of Open, Edit, Export and Delete', async () => {
        renderDrawer();
        const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
        expect(within(drawer).getByText('Iterations of all projects')).toBeVisible();
        const rows = await within(drawer).findAllByRole('listitem');
        expect(rows).toHaveLength(2);
        await waitFor(() => expect(within(rows[0]).getByText(/Planned 90 h of 120 h/)).toBeVisible());
        expect(within(rows[0]).getByText(/7 tasks/)).toBeVisible();
        for (const name of ['Open Sprint 2', 'Edit Sprint 2', 'Export Sprint 2', 'Delete Sprint 2']) {
            expect(within(rows[0]).getByRole('button', { name })).toBeEnabled();
        }
        expect(within(drawer).getByRole('button', { name: 'Import' })).toBeEnabled();
    });

    it('lists only the iterations of the project it is given, and names the project', async () => {
        renderDrawer({ projectId: 2 });
        const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
        expect(await within(drawer).findByText('Iterations of Beacon')).toBeVisible();
        const rows = await within(drawer).findAllByRole('listitem');
        expect(rows).toHaveLength(1);
        expect(within(rows[0]).getByRole('heading', { name: 'Launch' })).toBeVisible();
    });

    it('hands the row to Open and Edit', async () => {
        const { user, onOpen, onEdit } = renderDrawer();
        await user.click(await screen.findByRole('button', { name: 'Open Launch' }));
        expect(onOpen).toHaveBeenCalledWith(expect.objectContaining({ id: 21 }));
        await user.click(screen.getByRole('button', { name: 'Edit Sprint 2' }));
        expect(onEdit).toHaveBeenCalledWith(expect.objectContaining({ id: 12 }));
    });

    it('says the list could not be loaded, with the server detail and a retry', async () => {
        iterationServiceMock.getAll.mockRejectedValue(new AxiosError('Service Unavailable', '503', undefined, undefined,
            { status: 503, data: { detail: 'Database is unavailable' } } as never));
        renderDrawer();
        const alert = await screen.findByRole('alert', {}, { timeout: 3000 });
        expect(alert).toHaveTextContent('The iteration list could not be loaded.');
        expect(alert).toHaveTextContent('Database is unavailable');
        expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
    });

    it('exports an iteration to a JSON file named after it', async () => {
        const blob = new Blob(['{}']);
        exportMock.exportIteration.mockResolvedValue(blob);
        const createUrl = vi.fn(() => 'blob:export');
        const revokeUrl = vi.fn();
        Object.assign(window.URL, { createObjectURL: createUrl, revokeObjectURL: revokeUrl });
        const clicked: string[] = [];
        vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(function click(this: HTMLAnchorElement) { clicked.push(this.download); });

        const { user } = renderDrawer();
        await user.click(await screen.findByRole('button', { name: 'Export Sprint 2' }));
        await waitFor(() => expect(clicked).toEqual(['Sprint_2_export.json']));
        expect(exportMock.exportIteration).toHaveBeenCalledWith(12);
        expect(createUrl).toHaveBeenCalledWith(blob);
        expect(await screen.findByText('Iteration export is ready.')).toBeVisible();
    });

    it('says when an export fails', async () => {
        exportMock.exportIteration.mockRejectedValue(new Error('offline'));
        const { user } = renderDrawer();
        await user.click(await screen.findByRole('button', { name: 'Export Sprint 2' }));
        expect(await screen.findByText('The iteration could not be exported.')).toBeVisible();
        expect(exportMock.exportIteration).toHaveBeenCalledWith(12);
    });

    it('imports a file only after its preview is read and the person confirms', async () => {
        exportMock.previewImport.mockResolvedValue({ complete: true, expected_revisions: { 0: 1 }, file_sha256: 'abc' });
        exportMock.importIteration.mockResolvedValue({});
        const { user } = renderDrawer();
        const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
        const input = drawer.querySelector('input[type="file"]') as HTMLInputElement;
        const file = new File(['{"iteration":{}}'], 'plan.json', { type: 'application/json' });
        await user.upload(input, file);

        const dialog = await screen.findByRole('dialog', { name: 'Review import' });
        expect(within(dialog).getByText('plan.json')).toBeVisible();
        expect(exportMock.previewImport).toHaveBeenCalledWith(file, undefined, expect.anything());
        expect(exportMock.importIteration).not.toHaveBeenCalled();
        const importButton = within(dialog).getByRole('button', { name: 'Import' });
        await waitFor(() => expect(importButton).toBeEnabled());
        await user.click(importButton);
        await waitFor(() => expect(exportMock.importIteration).toHaveBeenCalledWith(file, { 0: 1 }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Review import' })).not.toBeInTheDocument());
    });

    it('keeps Import unavailable while the preview is incomplete', async () => {
        exportMock.previewImport.mockResolvedValue({ complete: false, expected_revisions: {}, file_sha256: 'abc' });
        const { user } = renderDrawer();
        const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
        await user.upload(drawer.querySelector('input[type="file"]') as HTMLInputElement, new File(['{}'], 'plan.json'));
        const dialog = await screen.findByRole('dialog', { name: 'Review import' });
        await settle();
        expect(within(dialog).getByRole('button', { name: 'Import' })).toBeDisabled();
        expect(exportMock.importIteration).not.toHaveBeenCalled();
    });

    it('deletes only after the confirmation, which names the task count and asks for the name', async () => {
        const { user } = renderDrawer();
        await user.click(await screen.findByRole('button', { name: 'Delete Launch' }));

        const dialog = await screen.findByRole('dialog', { name: 'Delete “Launch”?' });
        expect(within(dialog).getByText('This cannot be undone. 7 tasks and all iteration data will be deleted.')).toBeVisible();
        const confirm = within(dialog).getByRole('button', { name: 'Delete iteration and 7 tasks' });
        expect(confirm).toBeDisabled();
        expect(iterationServiceMock.delete).not.toHaveBeenCalled();

        await user.type(within(dialog).getByLabelText('Type “Launch” to confirm'), 'Launch');
        expect(confirm).toBeEnabled();
        await user.click(confirm);
        await waitFor(() => expect(iterationServiceMock.delete).toHaveBeenCalledWith(21, { 21: 4 }));
        expect(await screen.findByText('Iteration deleted.')).toBeVisible();
    });

    it('asks for no typed name when the iteration has no tasks, and Cancel deletes nothing', async () => {
        iterationServiceMock.getPlanningReadiness.mockImplementation(async (id: number) => readiness(id, { task_count: 0 }));
        const { user } = renderDrawer();
        await user.click(await screen.findByRole('button', { name: 'Delete Launch' }));
        const dialog = await screen.findByRole('dialog', { name: 'Delete “Launch”?' });
        expect(within(dialog).queryByLabelText('Type “Launch” to confirm')).not.toBeInTheDocument();
        await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Delete “Launch”?' })).not.toBeInTheDocument());
        expect(iterationServiceMock.delete).not.toHaveBeenCalled();
    });
});
