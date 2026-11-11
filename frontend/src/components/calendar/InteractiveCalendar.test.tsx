import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { InteractiveCalendar } from './InteractiveCalendar';

const renderCalendar = () => {
    const handlers = {
        onYearChange: vi.fn(), onMonthChange: vi.fn(), onAddHoliday: vi.fn(), onRemoveHoliday: vi.fn(),
        onAddShortDay: vi.fn(), onRemoveShortDay: vi.fn(), onToggleWeekend: vi.fn(),
    };
    const view = renderWithProviders(<InteractiveCalendar year={2026} month={0} holidays={['2026-01-01']} shortDays={[]}
        weekendDays={[5, 6]} {...handlers} />);
    return { ...view, handlers };
};

describe('calendar day editing without right-click', () => {
    it('names each day with its full date and state', () => {
        renderCalendar();
        expect(screen.getByRole('button', { name: 'Thursday, 1 January 2026: holiday' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Saturday, 3 January 2026: weekend' })).toBeInTheDocument();
    });

    it('marks a short day with a left click after choosing the mode', async () => {
        const { user, handlers } = renderCalendar();
        await user.click(screen.getByRole('radio', { name: 'Short day' }));
        await user.click(screen.getByRole('button', { name: 'Friday, 2 January 2026: working day' }));
        expect(handlers.onAddShortDay).toHaveBeenCalledWith('2026-01-02');
        expect(handlers.onAddHoliday).not.toHaveBeenCalled();
    });

    it('moves between days with the arrow keys and marks with Enter', async () => {
        const { user, handlers } = renderCalendar();
        const first = screen.getByRole('button', { name: 'Thursday, 1 January 2026: holiday' });
        first.focus();
        await user.keyboard('{ArrowDown}');
        expect(screen.getByRole('button', { name: 'Thursday, 8 January 2026: working day' })).toHaveFocus();
        await user.keyboard('{Enter}');
        expect(handlers.onAddHoliday).toHaveBeenCalledWith('2026-01-08');
    });
});
