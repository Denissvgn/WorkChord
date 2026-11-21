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

it('keeps the selected year on a failed save and retries with the observed profile revision', async () => {
    let saved: number[] = [];
    api.get.mockImplementation(async (path: string) => ({ data: path === '/calendars'
        ? [{ id: 1, name: 'Current year', year: 2026, timezone: 'UTC' }, { id: 3, name: 'Following year', year: 2027, timezone: 'UTC' }]
        : path.endsWith('/availability') ? {
            version: saved.length ? 2 : 1, calendar_id: 1, additional_calendar_ids: saved,
            calendar_selection_required: false, allocation_calendar_conflicts: [], absences: [],
        } : { days: [], allocations: [], timezone: 'UTC' } }));
    let refuse!: (reason: Error) => void;
    api.put.mockImplementationOnce(() => new Promise((_resolve, reject) => { refuse = reject; }))
        .mockImplementationOnce(async (_path: string, payload: { additional_calendar_ids: number[] }) => {
            saved = [...payload.additional_calendar_ids];
            return { data: {} };
        });
    const view = renderWithProviders(<PersonCapacity profileId={42} startDate="2026-12-28" endDate="2027-01-05" manage />);
    await view.user.click(screen.getByText('My availability'));
    const annual = await screen.findByRole('combobox', { name: 'Working calendar for 2027' });
    const save = screen.getByRole('button', { name: 'Save calendar' });
    expect(annual).toHaveValue('');
    expect(save).toBeDisabled();
    await view.user.selectOptions(annual, '3');
    await view.user.click(save);
    await waitFor(() => expect(save).toBeDisabled());
    expect(annual).toBeDisabled();
    await act(async () => refuse(new Error('Calendar save interrupted')));
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not save. Your draft is still here.');
    expect(annual).toHaveValue('3');
    expect(save).toBeEnabled();
    await view.user.click(save);
    await waitFor(() => expect(saved).toEqual([3]));
    expect(api.put).toHaveBeenNthCalledWith(1, '/team-member-profiles/42/availability', {
        calendar_id: 1, additional_calendar_ids: [3], expected_version: 1,
    });
    expect(api.put).toHaveBeenNthCalledWith(2, '/team-member-profiles/42/availability', {
        calendar_id: 1, additional_calendar_ids: [3], expected_version: 1,
    });
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
});
