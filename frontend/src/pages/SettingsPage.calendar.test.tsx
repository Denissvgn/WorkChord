import { act, screen, waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { renderWithProviders } from '../test/renderWithProviders';
import SettingsPage from './SettingsPage';

const api = vi.hoisted(() => ({ get: vi.fn(), put: vi.fn() }));
vi.mock('../services/api', () => ({ default: api }));

it('locks calendar changes during a save and ignores an obsolete resource completion', async () => {
    const first = { id: 1, name: 'First calendar', year: 2026, holidays: [], short_days: [], weekend_days: [5, 6], timezone: 'UTC' };
    const second = { ...first, id: 2, name: 'Second calendar', year: 2027 };
    let current = [first, second];
    api.get.mockImplementation(async (path: string) => {
        if (path === '/calendars') return { data: current };
        if (path.includes('/planning-inputs/calendar/')) {
            const id = Number(path.split('/').at(-2));
            return { data: { kind: 'calendar', resource_id: id, resource: id === 1 ? first : second, complete: true, expected_revisions: {} } };
        }
        if (path === '/iterations/page') return { data: { items: [], has_more: false, upper_id: 0, next_after_id: null } };
        return { data: [] };
    });
    let finish!: (value: unknown) => void;
    api.put.mockImplementation(() => new Promise(resolve => { finish = resolve; }));
    const view = renderWithProviders(<SettingsPage />, { initialEntries: ['/settings?tab=calendar'] });
    const save = await screen.findByRole('button', { name: 'Save calendar changes' });
    // Save stays disabled until something changes.
    expect(save).toBeDisabled();
    const [workday] = await screen.findAllByRole('button', { name: /: working day$/ });
    await view.user.click(workday);
    expect(screen.getByText('Unsaved changes')).toBeInTheDocument();
    await waitFor(() => expect(save).toBeEnabled());
    await view.user.click(save);
    await waitFor(() => expect(finish).toBeTypeOf('function'));
    expect(screen.getByRole('combobox', { name: 'Select calendar' })).toBeDisabled();
    current = [second];
    await act(async () => view.queryClient.setQueryData(['calendars'], current));
    await waitFor(() => expect(api.get.mock.calls.some(([path]) => path === '/tasks/planning-inputs/calendar/2/context')).toBe(true));
    await act(async () => finish({ data: first }));
    // The save lock is released once the obsolete completion is ignored.
    await view.user.click(screen.getByRole('button', { name: 'More actions' }));
    await waitFor(() => expect(screen.getByRole('menuitem', { name: 'New calendar' })).toBeEnabled());
    expect(api.get.mock.calls.filter(([path]) => path === '/tasks/planning-inputs/calendar/1/context')).toHaveLength(1);
    expect(screen.queryByText('Calendar settings saved')).not.toBeInTheDocument();
});

it('edits and saves the work calendar from Settings', async () => {
    const calendar = { id: 1, name: 'Workspace', year: 2026, holidays: [], short_days: [], weekend_days: [5, 6], timezone: 'UTC' };
    api.get.mockImplementation(async (path: string) => path === '/calendars' ? { data: [calendar] } :
        path.includes('/planning-inputs/calendar/') ? { data: { kind: 'calendar', resource_id: 1, resource: calendar, complete: true, expected_revisions: {} } } : { data: [] });
    api.put.mockImplementation(async (_path: string, data: object) => ({ data: { ...calendar, ...data } }));
    const view = renderWithProviders(<SettingsPage />, { initialEntries: ['/settings?tab=calendar'] });
    const day = (await screen.findAllByRole('button', { name: /: working day$/ }))[0];
    await view.user.click(day);
    await view.user.click(screen.getByRole('button', { name: 'Save calendar changes' }));
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/calendars/1', expect.objectContaining({ holidays: expect.arrayContaining([expect.any(String)]) }), expect.anything()));
    expect(await screen.findByText('Calendar settings saved')).toBeInTheDocument();
    expect(screen.queryByText('Team vacations')).not.toBeInTheDocument();
});
