import { beforeEach, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import { TimeEntriesPanel } from './TimeEntriesPanel';

const service = vi.hoisted(() => ({ capabilities: vi.fn(), list: vi.fn(), create: vi.fn(), correct: vi.fn(), void: vi.fn(), get: vi.fn(), history: vi.fn() }));
vi.mock('../../services/timeEntryService', async importOriginal => ({ ...await importOriginal<typeof import('../../services/timeEntryService')>(), timeEntryService: service }));
const row = (version = 1) => ({ id: 7, project_id: 2, task_id: 42, task_title: 'Work', principal_id: 1,
    version, work_date: '2026-10-07', timezone: 'Europe/Madrid', minutes: 15, note: 'Private saved note', voided: false });
const renderPanel = (parentSubmit?: () => void) => renderWithProviders(<IdentityContext.Provider value={{ identity: {
    mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Sam' },
    profile: null, workspace_role: 'member', projects: { '2': 'manager' }, csrf_token: null,
}, refresh: vi.fn(), signOut: async () => undefined }}><form onSubmit={event => { event.preventDefault(); parentSubmit?.(); }}><input aria-label="Parent title" required defaultValue="Work" /><TimeEntriesPanel projectId={2} taskId={42} draftKey="time-test" onDirty={vi.fn()} onPending={vi.fn()} /><button type="submit">Save parent task</button></form></IdentityContext.Provider>);
beforeEach(() => {
    sessionStorage.clear(); vi.resetAllMocks();
    service.capabilities.mockResolvedValue({ schema_version: 1, enabled: true });
    service.list.mockResolvedValue({ items: [row()], has_more: false, next_after_id: null, upper_id: 7 });
    service.history.mockResolvedValue({ items: [], has_more: false, next_after_version: null });
});
it('hides optional time controls when disabled', async () => {
    service.capabilities.mockResolvedValue({ schema_version: 1, enabled: false });
    renderPanel();
    await waitFor(() => expect(service.capabilities).toHaveBeenCalled());
    expect(screen.queryByRole('button', { name: 'Time entries' })).not.toBeInTheDocument();
    expect(service.list).not.toHaveBeenCalled();
});
it('keeps the creation request identity and draft through a failed retry', async () => {
    service.create.mockRejectedValueOnce(new Error('Temporary failure')).mockResolvedValueOnce(row());
    const { user } = renderPanel();
    await user.click(await screen.findByRole('button', { name: 'Time entries' }));
    await user.type(await screen.findByRole('spinbutton', { name: 'Minutes' }), '25');
    await user.type(screen.getByRole('textbox', { name: 'Private note (optional)' }), 'Retained inputs');
    await user.click(screen.getByRole('button', { name: 'Record time' }));
    await screen.findByRole('alert');
    expect(screen.getByRole('textbox', { name: 'Private note (optional)' })).toHaveValue('Retained inputs');
    await user.click(screen.getByRole('button', { name: 'Record time' }));
    await waitFor(() => expect(service.create).toHaveBeenCalledTimes(2));
    expect(service.create.mock.calls[0][2]).toBe(service.create.mock.calls[1][2]);
    expect(service.create.mock.calls[1][3]).toMatchObject({ minutes: 25, note: 'Retained inputs' });
});
it('requires explicit current-version adoption after a correction conflict', async () => {
    service.correct.mockRejectedValueOnce(new Error('Version conflict'));
    service.get.mockResolvedValue({ ...row(2), note: 'Another correction' });
    const { user } = renderPanel();
    await user.click(await screen.findByRole('button', { name: 'Time entries' }));
    await user.click(await screen.findByRole('button', { name: 'Correct entry' }));
    await user.type(screen.getByRole('textbox', { name: 'Reason for correction or void' }), 'Reconciled work');
    await user.click(screen.getByRole('button', { name: 'Save correction' }));
    await user.click(await screen.findByRole('button', { name: 'Reload current entry' }));
    await user.click(await screen.findByRole('button', { name: 'Keep draft with current version' }));
    service.correct.mockResolvedValue(row(3));
    await user.click(screen.getByRole('button', { name: 'Save correction' }));
    await waitFor(() => expect(service.correct).toHaveBeenLastCalledWith({ id: 7, version: 2 }, expect.objectContaining({ note: 'Private saved note' }), 'Reconciled work'));
});
it('hides cached private rows immediately after an authorization failure', async () => {
    service.create.mockRejectedValue({ response: { status: 403, data: { detail: 'Permission revoked' } } });
    const { user } = renderPanel();
    await user.click(await screen.findByRole('button', { name: 'Time entries' }));
    expect(await screen.findByText('Private saved note')).toBeInTheDocument();
    await user.type(screen.getByRole('spinbutton', { name: 'Minutes' }), '10');
    await user.click(screen.getByRole('button', { name: 'Record time' }));
    await screen.findByRole('alert');
    expect(screen.queryByText('Private saved note')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Correction history' })).not.toBeInTheDocument();
});

it('isolates required time controls from native validation of the parent task', async () => {
    const submit = vi.fn(); const { user } = renderPanel(submit);
    await user.click(await screen.findByRole('button', { name: 'Time entries' }));
    const minutes = await screen.findByRole('spinbutton', { name: 'Minutes' });
    expect(minutes).toBeRequired();
    const parent = screen.getByRole('textbox', { name: 'Parent title' }).closest('form')!;
    expect((minutes as HTMLInputElement).form).not.toBe(parent);
    expect(parent.checkValidity()).toBe(true);
    await user.click(screen.getByRole('button', { name: 'Save parent task' }));
    expect(submit).toHaveBeenCalledTimes(1);
    expect(service.create).not.toHaveBeenCalled();
});
