import { act, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PersonCapacity } from './PersonCapacity';

const api = vi.hoisted(() => ({ get: vi.fn(), put: vi.fn() }));
vi.mock('../../services/api', () => ({ default: api }));

beforeEach(() => {
    api.get.mockReset(); api.put.mockReset();
    api.get.mockImplementation(async (path: string) => ({ data: path === '/calendars'
        ? [{ id: 1, name: 'Current calendar', year: 2026 }, { id: 2, name: 'Draft calendar', year: 2026 }]
        : path.endsWith('/availability') ? { version: 1, calendar_id: 1, calendar_selection_required: false, allocation_calendar_conflicts: [], absences: [] }
        : { days: [], allocations: [], timezone: 'UTC' } }));
    api.put.mockResolvedValue({ data: {} });
});

it('keeps the opening availability revision when polling advances and requires explicit comparison', async () => {
    const view = renderWithProviders(<PersonCapacity profileId={42} manage />);
    await view.user.click(screen.getByText('My availability'));
    const calendar = await screen.findByRole('combobox');
    await view.user.selectOptions(calendar, '2');
    await act(async () => view.queryClient.setQueryData(['profile-availability', 42], {
        version: 2, calendar_id: 1, calendar_selection_required: false, allocation_calendar_conflicts: [], absences: [],
    }));
    expect(calendar).toHaveValue('2');
    await waitFor(() => expect(screen.getByRole('button', { name: 'Save calendar' })).toBeDisabled());
    await view.user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
    await view.user.click(screen.getByRole('button', { name: 'Save calendar' }));
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/team-member-profiles/42/availability', {
        calendar_id: 2, expected_version: 2,
    }));
});
