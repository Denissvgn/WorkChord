import { act, screen, waitFor } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { renderWithProviders } from '../test/renderWithProviders';
import CalendarPage from './CalendarPage';

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
    const view = renderWithProviders(<CalendarPage />);
    const save = await screen.findByRole('button', { name: 'Save settings' });
    await waitFor(() => expect(save).toBeEnabled());
    await view.user.click(save);
    await waitFor(() => expect(finish).toBeTypeOf('function'));
    expect(screen.getByRole('combobox', { name: 'Select calendar' })).toBeDisabled();
    current = [second];
    await act(async () => view.queryClient.setQueryData(['calendars'], current));
    await waitFor(() => expect(api.get.mock.calls.some(([path]) => path === '/tasks/planning-inputs/calendar/2/context')).toBe(true));
    await act(async () => finish({ data: first }));
    await waitFor(() => expect(save).toBeEnabled());
    expect(api.get.mock.calls.filter(([path]) => path === '/tasks/planning-inputs/calendar/1/context')).toHaveLength(1);
    expect(screen.queryByText('Calendar settings saved')).not.toBeInTheDocument();
});
