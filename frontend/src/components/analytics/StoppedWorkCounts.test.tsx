import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { IterationSummary } from '../../types/iteration';
import { taskService } from '../../services/taskService';
import { WorkMetricsLine } from '../tasks/WorkMetricsLine';
import { OnTrackSummary } from './OnTrackSummary';
import { StatusDistribution } from './StatusDistribution';

vi.mock('../../services/taskService', () => ({ taskService: { metricMatches: vi.fn() } }));

// The server's counts: total_tasks and the first five states agree; canceled and superseded work is outside them.
const summary = (overrides: Partial<IterationSummary> = {}): IterationSummary => ({
    id: 7, name: 'Sprint 14', start_date: '2026-11-02', end_date: '2026-11-27', working_days: 20,
    total_tasks: 11, completed_tasks: 4, total_effort_days: 30, team_capacity_days: 40, overdue_tasks_count: 0,
    metric_contract_version: 2, accepted_tasks: 2, implemented_tasks: 4, unknown_estimate_tasks: 0, postponed_tasks: 3, canceled_tasks: 2, superseded_tasks: 1,
    status_counts: { planned: 4, active: 2, resolved: 1, closed: 1, postponed: 3, canceled: 2, superseded: 1 }, blocked_tasks: 0,
    remaining_effort_days: 12, scheduled_finish: '2026-11-20', remaining_working_days: 10, ...overrides,
});

beforeEach(async () => {
    vi.clearAllMocks();
    await ensureLanguageResources('en');
    await i18n.changeLanguage('en');
    vi.mocked(taskService.metricMatches).mockImplementation(async ({ metric }) => ({ metric, has_more: false, items: [
        { id: 5, title: 'Stopped task', status: 'active', displayed_state: metric, project_name: 'Orchard', iteration_name: 'Iteration 7' }] }));
});

describe('analytics counts for stopped work', () => {
    it('counts postponed work inside the totals and canceled and superseded work outside them', () => {
        renderWithProviders(<StatusDistribution summary={summary()} />);
        const bar = screen.getByRole('img');
        expect(bar).toHaveAccessibleName('Planned 4, Active 2, Resolved 1, Closed 1, Postponed 3');
        expect(screen.getByText(/Canceled and superseded work \(3\) is not in these totals\./)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Postponed 3' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Canceled 2' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Superseded 1' })).toBeInTheDocument();
        const table = screen.getByRole('table', { hidden: true });
        expect(within(table).getByRole('rowheader', { name: 'Canceled', hidden: true }).parentElement).toHaveTextContent('Outside the totals');
        // The in-total states add up to the server's total.
        const total = ['Planned', 'Active', 'Resolved', 'Closed', 'Postponed'].reduce((sum, name) => (
            sum + Number(within(table).getByRole('rowheader', { name, hidden: true }).parentElement!.querySelector('td')!.textContent)), 0);
        expect(total).toBe(summary().total_tasks);
    });

    it('opens the tasks behind a stopped count and names their state', async () => {
        const { user } = renderWithProviders(<StatusDistribution summary={summary()} />);
        await user.click(screen.getByRole('button', { name: 'Superseded 1' }));
        const dialog = await screen.findByRole('dialog', { name: 'Superseded' });
        expect(await within(dialog).findByText(/Superseded · Orchard/)).toBeInTheDocument();
        expect(taskService.metricMatches).toHaveBeenCalledWith({ iteration_id: 7, metric: 'superseded', after_id: 0 }, expect.anything());
    });

    it('shows a distribution when only withdrawn work exists', () => {
        renderWithProviders(<StatusDistribution summary={summary({ total_tasks: 0, status_counts: { canceled: 2, superseded: 1 } })} />);
        expect(screen.getByRole('button', { name: 'Canceled 2' })).toBeInTheDocument();
        expect(screen.queryByRole('img')).not.toBeInTheDocument();
    });

    it('does not say done while only postponed work remains', () => {
        const { unmount } = renderWithProviders(<OnTrackSummary summary={summary({ total_tasks: 3, status_counts: { resolved: 1, closed: 1, postponed: 1 } })} />);
        expect(screen.getByText('Only postponed work is left:')).toBeInTheDocument();
        expect(screen.queryByText('Done:')).not.toBeInTheDocument();
        unmount();
        renderWithProviders(<OnTrackSummary summary={summary({ total_tasks: 2, status_counts: { resolved: 1, closed: 1, canceled: 2 } })} />);
        // Withdrawn work does not hold an iteration open.
        expect(screen.getByText('Done:')).toBeInTheDocument();
    });

    it('adds the separate counts to iteration and release progress, each opening its tasks', async () => {
        const { user } = renderWithProviders(<WorkMetricsLine metrics={summary()} scope={{ release_id: 4 }} />);
        const list = screen.getByLabelText('Delivery metrics');
        expect(within(list).getByText('Postponed').nextSibling).toHaveTextContent('3');
        expect(within(list).getByText('Canceled').nextSibling).toHaveTextContent('2');
        expect(within(list).getByText('Superseded').nextSibling).toHaveTextContent('1');
        await user.click(within(within(list).getByText('Canceled').nextSibling as HTMLElement).getByRole('button'));
        expect(taskService.metricMatches).toHaveBeenCalledWith({ release_id: 4, metric: 'canceled', after_id: 0 }, expect.anything());
    });

    it('leaves out a stopped count that is zero', () => {
        renderWithProviders(<WorkMetricsLine metrics={summary({ postponed_tasks: 0, canceled_tasks: 0, superseded_tasks: 1 })} scope={null} />);
        expect(screen.queryByText('Postponed')).not.toBeInTheDocument();
        expect(screen.getByText('Superseded')).toBeInTheDocument();
    });

    it('reads in Russian', async () => {
        await ensureLanguageResources('ru');
        await i18n.changeLanguage('ru');
        renderWithProviders(<StatusDistribution summary={summary()} />);
        expect(screen.getByRole('img')).toHaveAccessibleName('Запланировано 4, Активно 2, Решено 1, Закрыто 1, Отложено 3');
        expect(screen.getByRole('button', { name: 'Отменено 2' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Заменено 1' })).toBeInTheDocument();
        expect(screen.getByText(/Отменённые и заменённые задачи \(3\) в эти итоги не входят\./)).toBeInTheDocument();
    });
});
