import { expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import WorkCalendarSettings from './WorkCalendarSettings';

vi.mock('../../services/calendarService', () => ({ calendarService: { getAll: vi.fn().mockResolvedValue([]) } }));

it('opens a new calendar with the requested year', async () => {
    const queryClient = createTestQueryClient();
    queryClient.setQueryData(['calendars'], []);
    renderWithProviders(<WorkCalendarSettings />, { queryClient, initialEntries: ['/settings?tab=work_calendar&create=1&year=2027'] });
    expect(await screen.findByRole('dialog', { name: 'New calendar' })).toBeVisible();
    expect(screen.getByLabelText('Year')).toHaveValue(2027);
});
