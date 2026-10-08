import { useState } from 'react';
import { screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PlanningInputBoundary } from './PlanningInputBoundary';
const reader = vi.hoisted(() => vi.fn());
vi.mock('../../services/planningInputService', () => ({ planningInputService: { readInitial: reader } }));
const initial = { kind: 'project', resource_id: 7, resource: { id: 7, name: 'Current server name' }, complete: true, expected_revisions: { 1: 4, 2: 8 } };
beforeEach(() => { vi.clearAllMocks(); reader.mockResolvedValue(initial); });
const Editor = ({ name, save }: { name: string; save: (value: string) => void }) => {
    const [draft, setDraft] = useState(name);
    return <><input aria-label="Project name" value={draft} onChange={event => setDraft(event.target.value)} /><button onClick={() => save(draft)}>Save draft</button></>;
};
it('pins complete initial context and retains input during explicit comparison, then reloads only on request', async () => {
    const save = vi.fn();
    const { user } = renderWithProviders(<PlanningInputBoundary<{ id: number; name: string }> kind="project" resourceId={7}>
        {(observed, controls) => <>{controls}<Editor name={observed.resource.name} save={value => save(value, observed.expected_revisions)} /></>}
    </PlanningInputBoundary>);
    const input = await screen.findByRole('textbox', { name: 'Project name' });
    await user.clear(input); await user.type(input, 'Retained user name');
    reader.mockResolvedValue({ ...initial, resource: { id: 7, name: 'Peer name' }, expected_revisions: { 1: 5, 2: 9, 3: 1 } });
    await user.click(screen.getByRole('button', { name: 'Save draft' }));
    expect(save).toHaveBeenLastCalledWith('Retained user name', { 1: 4, 2: 8 });
    expect(reader).toHaveBeenCalledTimes(1);
    await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
    await waitFor(() => expect(input).toBeEnabled());
    expect(input).toHaveValue('Retained user name');
    await user.click(screen.getByRole('button', { name: 'Save draft' }));
    expect(save).toHaveBeenLastCalledWith('Retained user name', { 1: 5, 2: 9, 3: 1 });
    await user.click(screen.getByRole('button', { name: 'Load latest version' }));
    await waitFor(() => expect(screen.getByRole('textbox', { name: 'Project name' })).toHaveValue('Peer name'));
});
it('removes server values when retained comparison loses permission', async () => {
    const { user } = renderWithProviders(<PlanningInputBoundary<{ id: number; name: string }> kind="project" resourceId={7}>
        {(observed, controls) => <>{controls}<Editor name={observed.resource.name} save={() => undefined} /></>}
    </PlanningInputBoundary>);
    await screen.findByRole('textbox', { name: 'Project name' });
    reader.mockRejectedValue({ response: { status: 403, data: { detail: 'Permission changed' } } });
    await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
    await waitFor(() => expect(screen.queryByRole('textbox')).toBeNull());
    expect(screen.queryByText('Current server name')).toBeNull();
});
