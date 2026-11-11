import { expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { UnscheduledTasks } from './UnscheduledTasks';

it('lists planned tasks left without dates with what would schedule them', async () => {
    const { user } = renderWithProviders(<UnscheduledTasks items={[
        { task_id: 4, task_title: 'Agent work', reason: 'no_assignee', message: 'server text' },
        { task_id: 9, task_title: 'Odd case', reason: 'something_new' as never, message: 'Server explains it' },
    ]} />);
    await user.click(screen.getByText('2 planned tasks stay without dates'));
    expect(screen.getByText(/#4 Agent work/)).toBeInTheDocument();
    expect(screen.getByText(/Assign it to a capacity row in this iteration/)).toBeInTheDocument();
    // An unknown cause falls back to the server's own message.
    expect(screen.getByText('Server explains it')).toBeInTheDocument();
});

it('renders nothing when every planned task got dates', () => {
    renderWithProviders(<UnscheduledTasks items={[]} />);
    expect(screen.queryByText(/stays? without dates/)).not.toBeInTheDocument();
});
