import { beforeEach, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { QuickCapture } from './QuickCapture';

const services = vi.hoisted(() => ({
    task: { create: vi.fn(), delete: vi.fn() },
    triage: { create: vi.fn() },
    iteration: { getById: vi.fn() },
}));
vi.mock('../../services/taskService', () => ({ taskService: services.task }));
vi.mock('../../services/triageService', () => ({ triageService: services.triage }));
vi.mock('../../services/iterationService', () => ({ iterationService: services.iteration }));

beforeEach(() => {
    vi.clearAllMocks();
    services.iteration.getById.mockResolvedValue({ id: 3, revision: 7 });
    services.task.create.mockResolvedValue({ id: 11, title: 'Fix login', version: 1 });
    services.triage.create.mockResolvedValue({ id: 5, title: 'Customer email' });
});

it('captures a task from a title and Enter, against the current plan revision and without a priority', async () => {
    const { user } = renderWithProviders(<QuickCapture target={{ kind: 'task', iterationId: 3 }} onExpand={vi.fn()} />);
    const input = screen.getByRole('textbox', { name: 'Quick add a task' });
    await user.type(input, 'Fix login{Enter}');
    await waitFor(() => expect(services.task.create).toHaveBeenCalledWith(3, { title: 'Fix login', effort_days: null, depends_on: [], expected_revision: 7 }));
    await waitFor(() => expect(input).toHaveValue(''));
    expect(input).toHaveFocus();
});

it('keeps the title and says so when the capture fails', async () => {
    services.task.create.mockRejectedValueOnce({ response: { status: 500, data: {} } });
    const { user } = renderWithProviders(<QuickCapture target={{ kind: 'task', iterationId: 3 }} onExpand={vi.fn()} />);
    const input = screen.getByRole('textbox', { name: 'Quick add a task' });
    await user.type(input, 'Fix login{Enter}');
    expect(await screen.findByRole('alert')).toBeInTheDocument();
    expect(input).toHaveValue('Fix login');
});

it('ignores an empty title and hands the typed title to the full form', async () => {
    const onExpand = vi.fn();
    const { user } = renderWithProviders(<QuickCapture target={{ kind: 'triage' }} onExpand={onExpand} />);
    const input = screen.getByRole('textbox', { name: 'Quick add an intake item' });
    await user.type(input, '   {Enter}');
    expect(services.triage.create).not.toHaveBeenCalled();
    await user.clear(input);
    await user.type(input, 'Customer email');
    await user.click(screen.getByRole('button', { name: 'More fields' }));
    expect(onExpand).toHaveBeenCalledWith('Customer email');
    expect(input).toHaveValue('');
});

it('captures an intake item into triage', async () => {
    const { user } = renderWithProviders(<QuickCapture target={{ kind: 'triage' }} onExpand={vi.fn()} />);
    await user.type(screen.getByRole('textbox', { name: 'Quick add an intake item' }), 'Customer email{Enter}');
    await waitFor(() => expect(services.triage.create).toHaveBeenCalledWith({ title: 'Customer email' }));
    expect(services.task.create).not.toHaveBeenCalled();
});
