import { act, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import { IterationForm } from './IterationForm';

const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planningMock }));

const iterationServiceMock = vi.hoisted(() => ({
    create: vi.fn(),
    createSeries: vi.fn(),
    update: vi.fn(),
}));

const projectServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const calendarServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const iterationStoreMock = vi.hoisted(() => ({
    setSelectedIterationId: vi.fn(),
}));

vi.mock('../../services/iterationService', () => ({
    iterationService: iterationServiceMock,
}));

vi.mock('../../services/projectService', () => ({
    projectService: projectServiceMock,
}));

vi.mock('../../services/calendarService', () => ({
    calendarService: calendarServiceMock,
}));

vi.mock('../../store/iterationStore', () => ({
    useIterationStore: () => ({
        setSelectedIterationId: iterationStoreMock.setSelectedIterationId,
    }),
}));

const iterationFixture = (overrides: Partial<Iteration> = {}): Iteration => ({
    id: 17,
    name: 'August plan',
    calendar_id: 1,
    project_id: 42,
    project: {
        id: 42,
        name: 'Launch',
        status: 'active',
        health: 'green',
    },
    start_date: '2026-08-03',
    end_date: '2026-08-14',
    manager_email: 'manager@example.com',
    working_days: 10,
    ...overrides,
});

describe('IterationForm hardening', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture(), resource_id: 17, expected_revisions: { 17: 4 }, complete: true });
        projectServiceMock.getAll.mockResolvedValue([]);
        calendarServiceMock.getAll.mockResolvedValue([
            { id: 1, name: 'Company calendar', year: 2026, holidays: [], weekend_days: [5, 6], short_days: [] },
            { id: 2, name: 'Berlin calendar', year: 2026, holidays: [], weekend_days: [5, 6], short_days: [] },
        ]);
        iterationServiceMock.create.mockResolvedValue(iterationFixture({ project_id: null }));
        iterationServiceMock.createSeries.mockResolvedValue({
            iterations: [iterationFixture({ project_id: null })],
        });
        iterationServiceMock.update.mockImplementation(async (_id, payload) => (
            iterationFixture(payload)
        ));
    });

    it('shows no conflict prompt when the server copy matches the opened iteration', async () => {
        renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByDisplayValue('August plan');
        expect(screen.queryByRole('button', { name: 'Load latest version' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Keep draft with current version' })).not.toBeInTheDocument();
        expect(screen.queryByText('Current server values')).not.toBeInTheDocument();
    });

    it('names the fields that changed on the server when it differs from the opened iteration', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ end_date: '2026-08-21', name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(await screen.findByText(/This was changed on the server after you opened it: Name, End\./)).toBeVisible();
        expect(screen.getByRole('button', { name: 'Load latest version' })).toBeVisible();
        expect(screen.getByRole('button', { name: 'Keep draft with current version' })).toBeVisible();
    });

    it('keeps the opened draft when asked to, and loads the server values only when asked to', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ end_date: '2026-08-21', name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByText(/changed on the server after you opened it: Name, End\./);
        expect(screen.getByLabelText('Iteration name')).toHaveValue('August plan');
        expect(screen.queryByDisplayValue('August plan v2')).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await waitFor(() => expect(screen.queryByRole('button', { name: 'Keep draft with current version' })).not.toBeInTheDocument());
        expect(screen.getByLabelText('Iteration name')).toHaveValue('August plan');
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));
        await waitFor(() => expect(iterationServiceMock.update).toHaveBeenCalledWith(17, expect.objectContaining({ name: 'August plan', end_date: '2026-08-14' }), { 17: 5 }));
    });

    it('names a newer server change instead of keeping the draft against it', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByText(/changed on the server after you opened it: Name\./);
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2', end_date: '2026-08-28' }), resource_id: 17, expected_revisions: { 17: 6 }, complete: true });

        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        expect(await screen.findByText(/changed on the server again while you were deciding: End\./)).toBeVisible();
        expect(screen.getByText(/changed on the server after you opened it: Name, End\./)).toBeVisible();
        expect(screen.getByRole('button', { name: 'Keep draft with current version' })).toBeVisible();

        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await waitFor(() => expect(screen.queryByRole('button', { name: 'Keep draft with current version' })).not.toBeInTheDocument());
        expect(screen.queryByText(/changed on the server again/)).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));
        await waitFor(() => expect(iterationServiceMock.update).toHaveBeenCalledWith(17, expect.objectContaining({ name: 'August plan', end_date: '2026-08-14' }), { 17: 6 }));
    });

    it('does not update while the conflict prompt waits for a choice', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByText(/changed on the server after you opened it: Name\./);
        const update = screen.getByRole('button', { name: 'Update iteration' });
        expect(update).toBeDisabled();
        expect(screen.getByText('Choose Load latest version or Keep draft with current version before you update.')).toBeVisible();
        await user.click(update);
        expect(iterationServiceMock.update).not.toHaveBeenCalled();

        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await waitFor(() => expect(screen.getByRole('button', { name: 'Update iteration' })).toBeEnabled());
        expect(screen.queryByText(/before you update/)).not.toBeInTheDocument();
    });

    it('does not update after a newer server change while the draft is not kept yet', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByText(/changed on the server after you opened it: Name\./);
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2', end_date: '2026-08-28' }), resource_id: 17, expected_revisions: { 17: 6 }, complete: true });
        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await screen.findByText(/changed on the server again while you were deciding: End\./);
        const update = screen.getByRole('button', { name: 'Update iteration' });
        expect(update).toBeDisabled();
        await user.click(update);
        expect(iterationServiceMock.update).not.toHaveBeenCalled();
    });

    it('does not update again after a refused save until a conflict choice is made', async () => {
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByDisplayValue('August plan');
        iterationServiceMock.update.mockRejectedValueOnce({ response: { status: 409, data: { detail: 'Out of date' } } });
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'Changed elsewhere' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));
        await screen.findByRole('button', { name: 'Load latest version' });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Update iteration' })).toBeDisabled());
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));
        expect(iterationServiceMock.update).toHaveBeenCalledTimes(1);
    });

    it('fills the form with the server values after Load latest version', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'August plan v2' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByText(/changed on the server after you opened it: Name\./);
        expect(screen.getByLabelText('Iteration name')).toHaveValue('August plan');
        await user.click(screen.getByRole('button', { name: 'Load latest version' }));
        expect(await screen.findByDisplayValue('August plan v2')).toBeVisible();
        expect(screen.queryByRole('button', { name: 'Load latest version' })).not.toBeInTheDocument();
    });

    it('names a calendar or manager change made on the server', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ calendar_id: 2, manager_email: 'lead@example.com' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(await screen.findByText(/changed on the server after you opened it: Calendar, Manager email\./)).toBeVisible();
    });

    it('asks what to do when a save is refused as out of date', async () => {
        const { user } = renderWithProviders(<IterationForm initialData={iterationFixture()} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByDisplayValue('August plan');
        expect(screen.queryByRole('button', { name: 'Load latest version' })).not.toBeInTheDocument();
        iterationServiceMock.update.mockRejectedValueOnce({ response: { status: 409, data: { detail: 'Out of date' } } });
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ name: 'Changed elsewhere' }), resource_id: 17, expected_revisions: { 17: 5 }, complete: true });
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));
        expect(await screen.findByRole('button', { name: 'Load latest version' })).toBeVisible();
        expect(screen.getByText(/changed on the server after you opened it: Name\./)).toBeVisible();
    });

    it('keeps the calendar under More: the default is not sent, a chosen one is', async () => {
        const { user } = renderWithProviders(<IterationForm onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(screen.queryByLabelText('Calendar')).not.toBeInTheDocument();
        await user.type(screen.getByLabelText('Iteration name'), 'August plan');
        await user.type(screen.getByLabelText('Start date'), '2026-08-03');
        await user.type(screen.getByLabelText('End date'), '2026-08-14');
        await user.click(screen.getByRole('button', { name: 'Save iteration' }));
        await waitFor(() => expect(iterationServiceMock.create).toHaveBeenCalledTimes(1));
        expect(iterationServiceMock.create.mock.calls[0][0]).not.toHaveProperty('calendar_id');
    });

    it('sends the calendar chosen under More', async () => {
        const { user } = renderWithProviders(<IterationForm onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await user.type(screen.getByLabelText('Iteration name'), 'August plan');
        await user.type(screen.getByLabelText('Start date'), '2026-08-03');
        await user.type(screen.getByLabelText('End date'), '2026-08-14');
        await user.click(screen.getByRole('button', { name: 'More' }));
        await screen.findByRole('option', { name: 'Berlin calendar' });
        await user.selectOptions(screen.getByLabelText('Calendar'), 'Berlin calendar');
        await user.click(screen.getByRole('button', { name: 'Save iteration' }));
        await waitFor(() => expect(iterationServiceMock.create).toHaveBeenCalledTimes(1));
        expect(iterationServiceMock.create.mock.calls[0][0]).toMatchObject({ calendar_id: 2 });
    });

    it('omits a hidden project scope when updating an existing iteration', async () => {
        const onSuccess = vi.fn();
        const { user } = renderWithProviders(
            <IterationForm
                initialData={iterationFixture()}
                hideProjectScope
                onSuccess={onSuccess}
                onCancel={vi.fn()}
            />,
        );

        const nameInput = await screen.findByLabelText('Iteration name');
        await user.clear(nameInput);
        await user.type(nameInput, 'August delivery plan');
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));

        await waitFor(() => {
            expect(iterationServiceMock.update).toHaveBeenCalledOnce();
        });
        const [iterationId, payload] = iterationServiceMock.update.mock.calls[0];
        expect(iterationId).toBe(17);
        expect(payload).not.toHaveProperty('project_id');
        expect(payload).toEqual(expect.objectContaining({
            name: 'August delivery plan',
            start_date: '2026-08-03',
            end_date: '2026-08-14',
        }));
    });

    it('sends an explicit null when an existing manager email is cleared', async () => {
        const { user } = renderWithProviders(
            <IterationForm
                initialData={iterationFixture()}
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );

        await user.clear(await screen.findByLabelText('Manager email (for notifications)'));
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));

        await waitFor(() => {
            expect(iterationServiceMock.update).toHaveBeenCalledOnce();
        });
        expect(iterationServiceMock.update.mock.calls[0][1]).toEqual(
            expect.objectContaining({ manager_email: null }),
        );
    });

    it('sends an explicit null when an existing calendar is changed to the default calendar', async () => {
        planningMock.readInitial.mockResolvedValue({ resource: iterationFixture({ calendar_id: 2 }), resource_id: 17, expected_revisions: { 17: 4 }, complete: true });
        const { user } = renderWithProviders(
            <IterationForm
                initialData={iterationFixture({ calendar_id: 2 })}
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );

        // More is already open because the fixture carries a manager email.
        await screen.findByRole('option', { name: 'Berlin calendar' });
        await user.selectOptions(screen.getByLabelText('Calendar'), 'Default calendar');
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));

        await waitFor(() => expect(iterationServiceMock.update).toHaveBeenCalledOnce());
        expect(iterationServiceMock.update.mock.calls[0][1]).toEqual(
            expect.objectContaining({ calendar_id: null }),
        );
    });

    it('sends another calendar when an existing calendar is changed and omits it when unchanged', async () => {
        const first = renderWithProviders(
            <IterationForm
                initialData={iterationFixture({ calendar_id: 1 })}
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );
        await screen.findByRole('option', { name: 'Berlin calendar' });
        await first.user.selectOptions(screen.getByLabelText('Calendar'), 'Berlin calendar');
        await first.user.click(screen.getByRole('button', { name: 'Update iteration' }));
        await waitFor(() => expect(iterationServiceMock.update).toHaveBeenCalledOnce());
        expect(iterationServiceMock.update.mock.calls[0][1]).toEqual(
            expect.objectContaining({ calendar_id: 2 }),
        );
        first.unmount();

        iterationServiceMock.update.mockClear();
        const second = renderWithProviders(
            <IterationForm
                initialData={iterationFixture({ calendar_id: 1 })}
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );
        const name = await screen.findByLabelText('Iteration name');
        await second.user.type(name, ' v2');
        await second.user.click(screen.getByRole('button', { name: 'Update iteration' }));
        await waitFor(() => expect(iterationServiceMock.update).toHaveBeenCalledOnce());
        expect(iterationServiceMock.update.mock.calls[0][1]).not.toHaveProperty('calendar_id');
    });

    it('reports changes from either draft even after switching editor modes', async () => {
        const onStateChange = vi.fn();
        const { user } = renderWithProviders(
            <IterationForm
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
                onStateChange={onStateChange}
            />,
        );
        const latestState = () => onStateChange.mock.calls.at(-1)?.[0];

        await waitFor(() => {
            expect(latestState()).toEqual({ dirty: false, pending: false });
        });

        await user.click(screen.getByRole('button', { name: 'More' }));
        await user.click(screen.getByRole('button', { name: 'Repeating series' }));
        await user.type(screen.getByLabelText('Base name'), 'Sprint');
        await user.click(screen.getByRole('button', { name: 'Single period' }));

        await waitFor(() => {
            expect(latestState()).toEqual({ dirty: true, pending: false });
        });

        await user.click(screen.getByRole('button', { name: 'Repeating series' }));
        await user.clear(screen.getByLabelText('Base name'));
        await user.click(screen.getByRole('button', { name: 'Single period' }));

        await waitFor(() => {
            expect(latestState()).toEqual({ dirty: false, pending: false });
        });
    });

    it('reports pending state and freezes every control until a save settles', async () => {
        let resolveCreate: ((iteration: Iteration) => void) | undefined;
        iterationServiceMock.create.mockImplementation(() => (
            new Promise<Iteration>(resolve => {
                resolveCreate = resolve;
            })
        ));
        const onStateChange = vi.fn();
        const onCancel = vi.fn();
        const onSuccess = vi.fn();
        const { user } = renderWithProviders(
            <IterationForm
                hideProjectScope
                onSuccess={onSuccess}
                onCancel={onCancel}
                onStateChange={onStateChange}
            />,
        );
        const latestState = () => onStateChange.mock.calls.at(-1)?.[0];

        await user.type(await screen.findByLabelText('Iteration name'), 'September plan');
        await user.type(screen.getByLabelText('Start date'), '2026-09-01');
        await user.type(screen.getByLabelText('End date'), '2026-09-14');
        await user.click(screen.getByRole('button', { name: 'Save iteration' }));

        await waitFor(() => {
            expect(iterationServiceMock.create).toHaveBeenCalledOnce();
            expect(latestState()).toEqual({ dirty: true, pending: true });
        });

        const form = (await screen.findByLabelText('Iteration name')).closest('form');
        expect(form).not.toBeNull();
        expect(form).toHaveAttribute('aria-busy', 'true');
        for (const control of within(form!).getAllByRole('button')) {
            expect(control).toBeDisabled();
        }
        for (const control of form!.querySelectorAll('input, select, textarea')) {
            expect(control).toBeDisabled();
        }

        await user.click(screen.getByRole('button', { name: 'Cancel' }));
        expect(onCancel).not.toHaveBeenCalled();

        await act(async () => {
            resolveCreate?.(iterationFixture({
                name: 'September plan',
                project_id: null,
                manager_email: undefined,
                start_date: '2026-09-01',
                end_date: '2026-09-14',
            }));
        });

        await waitFor(() => {
            expect(onSuccess).toHaveBeenCalledOnce();
            expect(latestState()).toEqual({ dirty: false, pending: false });
        });
        expect(form).toHaveAttribute('aria-busy', 'false');
        expect(screen.getByRole('button', { name: 'Cancel' })).toBeEnabled();
    });

    it('announces mutation failures without discarding the draft', async () => {
        iterationServiceMock.update.mockRejectedValue(new Error('Server rejected the update'));
        const { user } = renderWithProviders(
            <IterationForm
                initialData={iterationFixture()}
                hideProjectScope
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );

        const nameInput = await screen.findByLabelText('Iteration name');
        await user.clear(nameInput);
        await user.type(nameInput, 'Still here after failure');
        await user.click(screen.getByRole('button', { name: 'Update iteration' }));

        expect(await screen.findByRole('alert')).toHaveTextContent('Failed to save iteration');
        expect(nameInput).toHaveValue('Still here after failure');
        expect(nameInput).toBeEnabled();
    });

    it('shows which kind is chosen, says why Save is unavailable, and asks before discarding changes', async () => {
        const onCancel = vi.fn();
        const { user } = renderWithProviders(<IterationForm onSuccess={vi.fn()} onCancel={onCancel} />);
        await user.click(await screen.findByRole('button', { name: 'More' }));
        const single = await screen.findByRole('button', { name: 'Single period' });
        expect(single).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('button', { name: 'Repeating series' })).toHaveAttribute('aria-pressed', 'false');
        const save = screen.getByRole('button', { name: /Save/ });
        expect(save).toBeDisabled();
        expect(save).toHaveAccessibleDescription('Enter a name to save.');

        await user.click(screen.getByRole('button', { name: 'Repeating series' }));
        expect(screen.getByRole('button', { name: 'Repeating series' })).toHaveAttribute('aria-pressed', 'true');
        await user.click(screen.getByRole('button', { name: 'Cancel' }));
        expect(onCancel).not.toHaveBeenCalled();
        await user.click(await screen.findByRole('button', { name: 'Keep editing' }));
        expect(onCancel).not.toHaveBeenCalled();
        await user.click(screen.getByRole('button', { name: 'Cancel' }));
        await user.click(await screen.findByRole('button', { name: 'Discard changes' }));
        expect(onCancel).toHaveBeenCalledOnce();
    });

    it('keeps name, project, start and end on the first screen and the rest under More', async () => {
        projectServiceMock.getAll.mockResolvedValue([{ id: 42, name: 'Launch' }]);
        const { user } = renderWithProviders(<IterationForm onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(await screen.findByLabelText('Iteration name')).toBeVisible();
        expect(screen.getByRole('combobox', { name: 'Project scope' })).toBeVisible();
        expect(screen.getByLabelText('Start date')).toBeVisible();
        expect(screen.getByLabelText('End date')).toBeVisible();
        const more = screen.getByRole('button', { name: 'More' });
        expect(more).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByRole('button', { name: 'Repeating series' })).not.toBeInTheDocument();
        expect(screen.queryByLabelText('Manager email (for notifications)')).not.toBeInTheDocument();

        await user.click(more);
        expect(more).toHaveAttribute('aria-expanded', 'true');
        expect(screen.getByRole('button', { name: 'Repeating series' })).toBeVisible();
        expect(screen.getByLabelText('Manager email (for notifications)')).toBeVisible();
    });

    it('creates a repeating series from the series fields under More', async () => {
        const { user } = renderWithProviders(<IterationForm hideProjectScope onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await user.click(await screen.findByRole('button', { name: 'More' }));
        await user.click(screen.getByRole('button', { name: 'Repeating series' }));
        await user.type(screen.getByLabelText('Base name'), 'Sprint 1');
        expect(screen.queryByLabelText('End date')).not.toBeInTheDocument();
        expect(screen.getByLabelText('Duration (calendar days)')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Create series' }));
        await waitFor(() => expect(iterationServiceMock.createSeries).toHaveBeenCalledOnce());
        expect(iterationServiceMock.createSeries.mock.calls[0][0]).toEqual(expect.objectContaining({ base_name: 'Sprint 1', duration_days: 14 }));
    });
});
