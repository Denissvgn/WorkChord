import { fireEvent, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { GitHubStatusAutomationRule } from '../../types/github';
import { GitHubSettingsPanel } from './GitHubSettingsPanel';

const githubServiceMock = vi.hoisted(() => ({
    getStatusAutomationRules: vi.fn(),
    createStatusAutomationRule: vi.fn(),
    updateStatusAutomationRule: vi.fn(),
    deleteStatusAutomationRule: vi.fn(),
}));

vi.mock('../../services/githubService', () => ({
    githubService: githubServiceMock,
}));

const ruleFixture = (
    id: number,
    overrides: Partial<GitHubStatusAutomationRule> = {},
): GitHubStatusAutomationRule => ({
    id,
    name: `Rule ${id}`,
    description: `Description ${id}`,
    enabled: false,
    github_event_type: 'github_pr_opened',
    from_status: 'planned',
    target_status: 'active',
    reason_template: 'GitHub automation: {github_event_type}',
    sort_order: id * 10,
    created_at: '2026-07-30T09:00:00Z',
    updated_at: '2026-07-30T09:00:00Z',
    ...overrides,
});

const deferred = <T,>() => {
    let resolve!: (value: T) => void;
    const promise = new Promise<T>(next => {
        resolve = next;
    });
    return { promise, resolve };
};

const renderPanel = () => renderWithProviders(<GitHubSettingsPanel />);

const rowFor = (name: string) => {
    const row = screen.getByText(name).closest('tr');
    if (!row) throw new Error(`Missing row for ${name}`);
    return row;
};

describe('GitHubSettingsPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        githubServiceMock.getStatusAutomationRules.mockResolvedValue([
            ruleFixture(1, { name: 'First rule' }),
            ruleFixture(2, { name: 'Second rule' }),
        ]);
        githubServiceMock.createStatusAutomationRule.mockResolvedValue(ruleFixture(3));
        githubServiceMock.updateStatusAutomationRule.mockResolvedValue(ruleFixture(1));
        githubServiceMock.deleteStatusAutomationRule.mockResolvedValue({ success: true });
    });

    it('blocks backend-invalid names and non-integer ordering without losing the draft', async () => {
        const { user } = renderPanel();

        const name = await screen.findByLabelText('Name');
        const order = screen.getByLabelText('Order');
        fireEvent.change(name, { target: { value: 'x'.repeat(256) } });
        fireEvent.change(order, { target: { value: '1.5' } });
        await user.click(screen.getByRole('button', { name: 'Create Rule' }));

        expect(githubServiceMock.createStatusAutomationRule).not.toHaveBeenCalled();
        expect(name).toHaveValue('x'.repeat(256));
        expect(order).toHaveValue(1.5);
        expect(name).toHaveAttribute('maxlength', '255');
        expect(name).toHaveAttribute('aria-invalid', 'true');
        expect(order).toHaveAttribute('aria-invalid', 'true');
    });

    it('freezes the submitted snapshot and all draft-switching controls while saving', async () => {
        const update = deferred<GitHubStatusAutomationRule>();
        githubServiceMock.updateStatusAutomationRule.mockReturnValueOnce(update.promise);
        const { user } = renderPanel();

        await screen.findByText('First rule');
        const firstRow = rowFor('First rule');
        await user.click(within(firstRow).getAllByRole('button')[0]);
        const name = screen.getByLabelText('Name');
        await user.clear(name);
        await user.type(name, 'Frozen draft');
        await user.click(screen.getByRole('button', { name: 'Save Rule' }));

        await waitFor(() => {
            expect(githubServiceMock.updateStatusAutomationRule).toHaveBeenCalledWith(
                1,
                expect.objectContaining({ name: 'Frozen draft' }),
            );
        });
        expect(name).toBeDisabled();
        expect(screen.getByRole('button', { name: 'New Rule' })).toBeDisabled();
        expect(within(rowFor('Second rule')).getAllByRole('button')[0]).toBeDisabled();
        expect(screen.getByText('Saving...')).toBeInTheDocument();

        fireEvent.change(name, { target: { value: 'Late edit' } });
        expect(name).toHaveValue('Frozen draft');
        expect(githubServiceMock.updateStatusAutomationRule.mock.calls[0][1]).toEqual(
            expect.objectContaining({ name: 'Frozen draft' }),
        );

        update.resolve(ruleFixture(1, { name: 'Frozen draft' }));
        await waitFor(() => {
            expect(screen.getByRole('button', { name: 'Create Rule' })).toBeEnabled();
        });
    });

    it('requires explicit confirmation before switching away from an unsaved draft', async () => {
        const { user } = renderPanel();

        await screen.findByText('First rule');
        await user.click(within(rowFor('First rule')).getAllByRole('button')[0]);
        const name = screen.getByLabelText('Name');
        await user.clear(name);
        await user.type(name, 'Keep this draft');
        await user.click(within(rowFor('Second rule')).getAllByRole('button')[0]);

        const dialog = screen.getByRole('dialog');
        expect(name).toHaveValue('Keep this draft');
        await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
        expect(name).toHaveValue('Keep this draft');

        await user.click(within(rowFor('Second rule')).getAllByRole('button')[0]);
        await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Discard changes' }));
        expect(name).toHaveValue('Second rule');
    });

    it('keeps unrelated drafts and scopes pending delete feedback to the affected row', async () => {
        const deletion = deferred<{ success: boolean }>();
        githubServiceMock.deleteStatusAutomationRule.mockReturnValueOnce(deletion.promise);
        const { user } = renderPanel();

        await screen.findByText('First rule');
        const firstRow = rowFor('First rule');
        const secondRow = rowFor('Second rule');
        await user.click(within(firstRow).getAllByRole('button')[0]);
        const name = screen.getByLabelText('Name');
        await user.clear(name);
        await user.type(name, 'Unrelated draft');

        const firstDelete = within(firstRow).getAllByRole('button')[1];
        const secondDelete = within(secondRow).getAllByRole('button')[1];
        await user.click(secondDelete);
        await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Delete' }));

        await waitFor(() => {
            expect(githubServiceMock.deleteStatusAutomationRule).toHaveBeenCalled();
        });
        expect(githubServiceMock.deleteStatusAutomationRule.mock.calls[0][0]).toBe(2);
        expect(secondDelete).toHaveAttribute('aria-busy', 'true');
        expect(firstDelete).not.toHaveAttribute('aria-busy', 'true');
        expect(firstDelete).toBeDisabled();
        expect(name).toHaveValue('Unrelated draft');

        deletion.resolve({ success: true });
        await waitFor(() => {
            expect(secondDelete).not.toHaveAttribute('aria-busy', 'true');
        });
        expect(name).toHaveValue('Unrelated draft');
    });

    it('reconciles a row toggle into the open editor without dropping other draft fields', async () => {
        const { user } = renderPanel();

        await screen.findByText('First rule');
        await user.click(within(rowFor('First rule')).getAllByRole('button')[0]);
        const description = screen.getByLabelText('Description');
        await user.clear(description);
        await user.type(description, 'Keep this description');

        await user.click(screen.getByRole('checkbox', { name: 'Enable First rule' }));

        await waitFor(() => {
            expect(githubServiceMock.updateStatusAutomationRule).toHaveBeenCalledWith(
                1,
                { enabled: true },
            );
        });
        expect(screen.getByRole('checkbox', { name: 'Enabled' })).toBeChecked();
        expect(description).toHaveValue('Keep this description');
    });
});
