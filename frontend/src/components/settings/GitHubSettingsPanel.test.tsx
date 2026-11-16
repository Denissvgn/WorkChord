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

const editor = (name: string) => screen.getByRole('dialog', { name });

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

        await user.click(await screen.findByRole('button', { name: 'New rule' }));
        const drawer = editor('New rule');
        const name = within(drawer).getByLabelText('Name');
        const order = within(drawer).getByLabelText('Order');
        fireEvent.change(name, { target: { value: 'x'.repeat(256) } });
        fireEvent.change(order, { target: { value: '1.5' } });
        await user.click(within(drawer).getByRole('button', { name: 'Create rule' }));

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
        await user.click(screen.getByRole('button', { name: 'Save rule' }));

        await waitFor(() => {
            expect(githubServiceMock.updateStatusAutomationRule).toHaveBeenCalledWith(
                1,
                expect.objectContaining({ name: 'Frozen draft' }),
            );
        });
        expect(name).toBeDisabled();
        expect(screen.getByRole('button', { name: 'New rule' })).toBeDisabled();
        expect(within(rowFor('Second rule')).getAllByRole('button')[0]).toBeDisabled();
        expect(screen.getByText('Saving…')).toBeInTheDocument();

        fireEvent.change(name, { target: { value: 'Late edit' } });
        expect(name).toHaveValue('Frozen draft');
        expect(githubServiceMock.updateStatusAutomationRule.mock.calls[0][1]).toEqual(
            expect.objectContaining({ name: 'Frozen draft' }),
        );

        update.resolve(ruleFixture(1, { name: 'Frozen draft' }));
        await waitFor(() => {
            expect(screen.queryByRole('dialog')).toBeNull();
        });
        expect(screen.getByRole('button', { name: 'New rule' })).toBeEnabled();
    });

    it('opens New rule and Edit in the drawer and asks before closing an unsaved draft', async () => {
        const { user } = renderPanel();

        await screen.findByText('First rule');
        await user.click(within(rowFor('First rule')).getByRole('button', { name: 'Edit First rule' }));
        const drawer = editor('Edit First rule');
        const name = within(drawer).getByLabelText('Name');
        expect(name).toHaveValue('First rule');
        expect(within(drawer).getByLabelText('Reason template')).toHaveValue('GitHub automation: {github_event_type}');
        await user.clear(name);
        await user.type(name, 'Keep this draft');
        await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));

        const confirm = screen.getByRole('dialog', { name: 'Discard unsaved rule changes?' });
        await user.click(within(confirm).getByRole('button', { name: 'Cancel' }));
        expect(editor('Edit First rule')).toBeInTheDocument();
        expect(name).toHaveValue('Keep this draft');

        await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));
        await user.click(within(screen.getByRole('dialog', { name: 'Discard unsaved rule changes?' })).getByRole('button', { name: 'Discard changes' }));
        expect(screen.queryByRole('dialog')).toBeNull();
        expect(githubServiceMock.updateStatusAutomationRule).not.toHaveBeenCalled();

        await user.click(within(rowFor('Second rule')).getByRole('button', { name: 'Edit Second rule' }));
        expect(within(editor('Edit Second rule')).getByLabelText('Name')).toHaveValue('Second rule');
        await user.click(within(editor('Edit Second rule')).getByRole('button', { name: 'Cancel' }));
        expect(screen.queryByRole('dialog')).toBeNull();

        await user.click(screen.getByRole('button', { name: 'New rule' }));
        const created = editor('New rule');
        await user.type(within(created).getByLabelText('Name'), 'Merged resolves');
        await user.click(within(created).getByRole('button', { name: 'Create rule' }));
        await waitFor(() => expect(githubServiceMock.createStatusAutomationRule).toHaveBeenCalled());
        expect(githubServiceMock.createStatusAutomationRule.mock.calls[0][0]).toEqual(
            expect.objectContaining({ name: 'Merged resolves', sort_order: 100 }),
        );
        await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull());
    });

    it('scopes pending delete feedback to the affected row', async () => {
        const deletion = deferred<{ success: boolean }>();
        githubServiceMock.deleteStatusAutomationRule.mockReturnValueOnce(deletion.promise);
        const { user } = renderPanel();

        await screen.findByText('First rule');
        const firstRow = rowFor('First rule');
        const secondRow = rowFor('Second rule');

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

        deletion.resolve({ success: true });
        await waitFor(() => {
            expect(secondDelete).not.toHaveAttribute('aria-busy', 'true');
        });
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
