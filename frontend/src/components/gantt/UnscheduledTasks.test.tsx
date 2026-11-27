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

it('names the postponed work a planned task waits on', async () => {
    const { user } = renderWithProviders(<UnscheduledTasks items={[
        { task_id: 12, task_title: 'Vendor dashboard', reason: 'predecessor_postponed', message: 'server text',
          waiting_on: [{ task_id: 11, task_title: 'Vendor integration' }] },
    ]} />);
    await user.click(screen.getByText('1 planned task stays without dates'));
    expect(screen.getByText(/Waits for the postponed task "Vendor integration" \(#11\)/)).toBeInTheDocument();
    expect(screen.queryByText(/Schedule it first/)).not.toBeInTheDocument();
});

it('falls back to the server message when a postponed wait comes without names', async () => {
    const { user } = renderWithProviders(<UnscheduledTasks items={[
        { task_id: 13, task_title: 'Vendor report', reason: 'predecessor_postponed', message: 'Waiting on postponed task from the server' },
    ]} />);
    await user.click(screen.getByText('1 planned task stays without dates'));
    expect(screen.getByText('Waiting on postponed task from the server')).toBeInTheDocument();
});

it('renders nothing when every planned task got dates', () => {
    renderWithProviders(<UnscheduledTasks items={[]} />);
    expect(screen.queryByText(/stays? without dates/)).not.toBeInTheDocument();
});
