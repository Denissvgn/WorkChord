import { act, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import { IterationForm } from './IterationForm';

const iterationServiceMock = vi.hoisted(() => ({
    create: vi.fn(),
    createSeries: vi.fn(),
    update: vi.fn(),
}));

const projectServiceMock = vi.hoisted(() => ({
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
        projectServiceMock.getAll.mockResolvedValue([]);
        iterationServiceMock.create.mockResolvedValue(iterationFixture({ project_id: null }));
        iterationServiceMock.createSeries.mockResolvedValue({
            iterations: [iterationFixture({ project_id: null })],
        });
        iterationServiceMock.update.mockImplementation(async (_id, payload) => (
            iterationFixture(payload)
        ));
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

        const nameInput = screen.getByLabelText('Iteration Name');
        await user.clear(nameInput);
        await user.type(nameInput, 'August delivery plan');
        await user.click(screen.getByRole('button', { name: 'Update Iteration' }));

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

        await user.clear(screen.getByLabelText('Manager Email (for notifications)'));
        await user.click(screen.getByRole('button', { name: 'Update Iteration' }));

        await waitFor(() => {
            expect(iterationServiceMock.update).toHaveBeenCalledOnce();
        });
        expect(iterationServiceMock.update.mock.calls[0][1]).toEqual(
            expect.objectContaining({ manager_email: null }),
        );
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

        await user.type(screen.getByLabelText('Iteration Name'), 'September plan');
        await user.type(screen.getByLabelText('Start Date'), '2026-09-01');
        await user.type(screen.getByLabelText('End Date'), '2026-09-14');
        await user.click(screen.getByRole('button', { name: 'Save Iteration' }));

        await waitFor(() => {
            expect(iterationServiceMock.create).toHaveBeenCalledOnce();
            expect(latestState()).toEqual({ dirty: true, pending: true });
        });

        const form = screen.getByLabelText('Iteration Name').closest('form');
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

        const nameInput = screen.getByLabelText('Iteration Name');
        await user.clear(nameInput);
        await user.type(nameInput, 'Still here after failure');
        await user.click(screen.getByRole('button', { name: 'Update Iteration' }));

        expect(await screen.findByRole('alert')).toHaveTextContent('Failed to save iteration');
        expect(nameInput).toHaveValue('Still here after failure');
        expect(nameInput).toBeEnabled();
    });
});
