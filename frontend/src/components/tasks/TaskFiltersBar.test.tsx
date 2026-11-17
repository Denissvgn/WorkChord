import { useState } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { fireEvent, screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { TaskFiltersBar, type TaskFilters } from './TaskFiltersBar';

vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Ana' }]) } }));
vi.mock('../../services/projectService', () => ({
    projectService: {
        getAll: vi.fn().mockResolvedValue([{ id: 3, name: 'Apollo' }]),
        getRoadmapMilestones: vi.fn().mockResolvedValue({
            items: [{ id: 11, project_id: 3, name: 'Beta' }, { id: 12, project_id: 4, name: 'Launch' }],
            next_cursor: null,
        }),
    },
}));
vi.mock('../../services/labelService', () => ({
    labelService: {
        getGroups: vi.fn().mockResolvedValue([{ key: 'area', name: 'Area', labels: [{ slug: 'backend', name: 'Backend' }, { slug: 'web', name: 'Web' }] }]),
    },
}));

const QUICK = ['Assignee', 'Status', 'Label', 'Milestone', 'Needs attention'];

const Harness = ({ initial = defaultFilters, onChange }: { initial?: TaskFilters; onChange?: (filters: TaskFilters) => void }) => {
    const [filters, setFilters] = useState(initial);
    return <TaskFiltersBar iterationId={1} filters={filters} onFiltersChange={next => { setFilters(next); onChange?.(next); }} />;
};

describe('visible task filters', () => {
    it('shows a removable chip for every active condition, including dates and each label', async () => {
        const onFiltersChange = vi.fn();
        const { user } = renderWithProviders(<TaskFiltersBar iterationId={1} onFiltersChange={onFiltersChange}
            filters={{ ...defaultFilters, isBlocked: true, startDateFrom: '2026-01-05', labelSlugs: ['backend'], priority: 2, status: 'planned', needsAttention: true }} />);
        const chips = screen.getByRole('list', { name: 'Active filters' });
        expect(await within(chips).findByText('Label: Backend · Area')).toBeInTheDocument();
        for (const text of ['Blocked: Yes', 'Priority: 2', 'Status: Planned', 'Needs attention: Yes']) {
            expect(within(chips).getByText(text)).toBeInTheDocument();
        }
        expect(within(chips).getByText(/^Start from: /)).toBeInTheDocument();

        await user.click(within(chips).getByRole('button', { name: /^Remove filter Start from/ }));
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ startDateFrom: '', labelSlugs: ['backend'] }));

        await user.click(within(chips).getByRole('button', { name: 'Remove filter Label: Backend · Area' }));
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ labelSlugs: [], isBlocked: true }));
    });

    it('holds five quick filters in the row and adds labels one at a time', async () => {
        const onFiltersChange = vi.fn();
        const { user } = renderWithProviders(<TaskFiltersBar iterationId={1} onFiltersChange={onFiltersChange}
            filters={{ ...defaultFilters, labelSlugs: ['backend'] }} />);
        const row = screen.getByTestId('filter-bar').querySelector('.wc-filter-controls') as HTMLElement;
        expect(within(row).getAllByRole('combobox').map(control => control.getAttribute('aria-label'))).toEqual(QUICK);
        expect(screen.queryByRole('dialog', { name: 'More filters' })).not.toBeInTheDocument();
        expect(await screen.findByRole('option', { name: 'Ana' })).toBeInTheDocument();
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'Ana');
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ assigneeId: 7 }));

        const labels = screen.getByRole('combobox', { name: 'Label' });
        expect(within(labels).queryByRole('option', { name: 'Backend · Area' })).not.toBeInTheDocument();
        await user.selectOptions(labels, 'Web · Area');
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ labelSlugs: ['backend', 'web'] }));
    });

    it('offers the milestones of the chosen project and names the unknown one by number', async () => {
        const { user } = renderWithProviders(<Harness initial={{ ...defaultFilters, projectId: 3 }} />);
        const milestone = screen.getByRole('combobox', { name: 'Milestone' });
        expect(await within(milestone).findByRole('option', { name: 'Beta' })).toBeInTheDocument();
        expect(within(milestone).queryByRole('option', { name: 'Launch' })).not.toBeInTheDocument();
        await user.selectOptions(milestone, 'Beta');
        expect(within(screen.getByRole('list', { name: 'Active filters' })).getByText('Milestone: Beta')).toBeInTheDocument();
    });

    it('keeps every other filter under More filters and shows each one as a chip', async () => {
        const onChange = vi.fn();
        const { user } = renderWithProviders(<Harness onChange={onChange} />);
        await screen.findByRole('option', { name: 'Ana' });
        await user.click(screen.getByRole('button', { name: /More filters/ }));
        const panel = screen.getByRole('dialog', { name: 'More filters' });

        const selects: [string, string, string][] = [
            ['Planning readiness', 'Missing effort', 'Planning readiness: Missing effort'],
            ['Blocked', 'Yes', 'Blocked: Yes'],
            ['Overdue delivery', 'No', 'Overdue delivery: No'],
            ['Project', 'Apollo', 'Project: Apollo'],
            ['Priority', '4', 'Priority: 4'],
            ['Waits for', 'Yes', 'Waits for: Yes'],
            ['Agent readiness', 'Ready', 'Agent readiness: Ready'],
            ['Iteration overflow', 'Yes', 'Iteration overflow: Yes'],
            ['Label groups', 'Area', 'Label groups: Area'],
        ];
        const names = [...selects.map(([name]) => name), 'Start from', 'Start to', 'End from', 'End to'];
        names.forEach(name => expect(within(panel).getByLabelText(name)).toBeInTheDocument());
        for (const [name, option] of selects) {
            await user.selectOptions(within(panel).getByRole('combobox', { name }), option);
        }
        for (const [name, value] of [['Start from', '2026-02-01'], ['Start to', '2026-02-28'], ['End from', '2026-03-01'], ['End to', '2026-03-31']]) {
            fireEvent.change(within(panel).getByLabelText(name), { target: { value } });
        }

        const chips = screen.getByRole('list', { name: 'Active filters' });
        for (const [, , chip] of selects) expect(within(chips).getByText(chip)).toBeInTheDocument();
        for (const name of ['Start from', 'Start to', 'End from', 'End to']) {
            expect(within(chips).getByText(new RegExp(`^${name}: `))).toBeInTheDocument();
        }
        expect(onChange).toHaveBeenLastCalledWith(expect.objectContaining({
            planningIssue: 'missing-effort', isBlocked: true, isOverdue: false, projectId: 3, priority: 4, hasDependency: true,
            agentReady: true, isIterationOverflow: true, labelGroupKeys: ['area'],
            startDateFrom: '2026-02-01', startDateTo: '2026-02-28', endDateFrom: '2026-03-01', endDateTo: '2026-03-31',
        }));
    });
});
