import { act, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { Label, LabelGroup } from '../../types/label';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TemplateLabelSettings } from './TemplateLabelSettings';

const labelServiceMock = vi.hoisted(() => ({
    getGroups: vi.fn(),
    getLabels: vi.fn(),
    createGroup: vi.fn(),
    updateGroup: vi.fn(),
    createLabel: vi.fn(),
    updateLabel: vi.fn(),
}));

const templateServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
    getById: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
}));

const toastMock = vi.hoisted(() => ({
    success: vi.fn(),
    error: vi.fn(),
}));

vi.mock('../../services/labelService', () => ({
    labelService: labelServiceMock,
}));

vi.mock('../../services/templateService', () => ({
    templateService: templateServiceMock,
}));

vi.mock('../feedback/toast', async (importOriginal) => {
    const actual = await importOriginal<typeof import('../feedback/toast')>();
    return {
        ...actual,
        useToast: () => toastMock,
    };
});

const labelFixture = (overrides: Partial<Label> = {}): Label => ({
    id: 101,
    slug: 'planning',
    name: 'Planning',
    group_id: 1,
    description: null,
    color: '#2563eb',
    is_active: true,
    sort_order: 10,
    seed_key: null,
    created_at: '2026-07-01T10:00:00Z',
    updated_at: '2026-07-01T10:00:00Z',
    ...overrides,
});

const groupFixture = (overrides: Partial<LabelGroup> = {}): LabelGroup => ({
    id: 1,
    key: 'workflow',
    name: 'Workflow',
    description: null,
    color: '#2563eb',
    is_active: true,
    sort_order: 10,
    seed_key: null,
    labels: [
        labelFixture(),
        labelFixture({
            id: 102,
            slug: 'delivery',
            name: 'Delivery',
            sort_order: 20,
        }),
    ],
    created_at: '2026-07-01T10:00:00Z',
    updated_at: '2026-07-01T10:00:00Z',
    ...overrides,
});

const groupsFixture = () => [
    groupFixture(),
    groupFixture({
        id: 2,
        key: 'governance',
        name: 'Governance',
        color: '#7c3aed',
        sort_order: 20,
        labels: [],
    }),
];

const openLabels = async () => {
    const labelsTab = await screen.findByRole('tab', { name: 'Labels' });
    await act(async () => {
        labelsTab.click();
    });
    expect(await screen.findByRole('tabpanel', { name: 'Labels' })).toBeInTheDocument();
    expect(await screen.findByRole('heading', { name: 'Workflow' })).toBeInTheDocument();
};

/** Rows keep their actions in one menu: open it, then choose the action. */
const rowAction = async (user: ReturnType<typeof renderWithProviders>['user'], row: string, action: string) => {
    await user.click(screen.getByRole('button', { name: `Actions for ${row}` }));
    await user.click(screen.getByRole('menuitem', { name: action }));
};

describe('TemplateLabelSettings hardening', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        templateServiceMock.getAll.mockResolvedValue([]);
        labelServiceMock.getGroups.mockResolvedValue(groupsFixture());
        labelServiceMock.updateGroup.mockImplementation(async (id: number, data: Partial<LabelGroup>) => ({
            ...groupsFixture().find(group => group.id === id)!,
            ...data,
        }));
        labelServiceMock.updateLabel.mockImplementation(async (id: number, data: Partial<Label>) => ({
            ...groupFixture().labels.find(label => label.id === id)!,
            ...data,
        }));
    });

    it('keeps an unrelated group draft and locks the label workspace while archiving', async () => {
        let resolveArchive: ((group: LabelGroup) => void) | undefined;
        labelServiceMock.updateGroup.mockImplementationOnce(() => (
            new Promise<LabelGroup>(resolve => {
                resolveArchive = resolve;
            })
        ));

        const { user } = renderWithProviders(<TemplateLabelSettings />);
        await openLabels();

        await rowAction(user, 'Workflow', 'Edit group');
        const nameField = screen.getByRole('textbox', { name: 'Name' });
        await user.clear(nameField);
        await user.type(nameField, 'Workflow draft');

        await rowAction(user, 'Governance', 'Archive group');

        expect(nameField).toBeDisabled();
        expect(screen.getByRole('tab', { name: 'Templates' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Actions for Workflow' }));
        expect(screen.getByRole('menuitem', { name: 'Archive group' })).toHaveAttribute('aria-disabled', 'true');
        await user.keyboard('{Escape}');

        await act(async () => {
            resolveArchive?.({
                ...groupsFixture()[1],
                is_active: false,
            });
        });

        await waitFor(() => expect(nameField).toBeEnabled());
        expect(nameField).toHaveValue('Workflow draft');
    });

    it('keeps an unrelated label draft when another label is archived', async () => {
        const { user } = renderWithProviders(<TemplateLabelSettings />);
        await openLabels();

        await rowAction(user, 'Planning', 'Edit label');
        const nameField = screen.getByRole('textbox', { name: 'Name' });
        await user.clear(nameField);
        await user.type(nameField, 'Planning draft');

        await rowAction(user, 'Delivery', 'Archive label');

        await waitFor(() => {
            expect(labelServiceMock.updateLabel).toHaveBeenCalledWith(102, {
                is_active: false,
            });
        });
        expect(nameField).toHaveValue('Planning draft');
    });

    it('associates every manual editor label with its control', async () => {
        const { user } = renderWithProviders(<TemplateLabelSettings />);

        await user.click(await screen.findByRole('button', { name: 'New template' }));
        expect(screen.getByLabelText('Type')).toBeInTheDocument();
        expect(screen.getByLabelText('Description')).toBeInTheDocument();
        expect(screen.getByLabelText('Default description')).toBeInTheDocument();
        expect(screen.getByLabelText('Checklist')).toBeInTheDocument();
        expect(screen.getByLabelText('Default payload JSON')).toBeInTheDocument();

        await openLabels();
        await rowAction(user, 'Workflow', 'Edit group');
        expect(screen.getByLabelText('Description')).toBeInTheDocument();

        await rowAction(user, 'Planning', 'Edit label');
        const labelEditor = screen.getByRole('heading', { name: 'Edit label' })
            .closest('.border-t') as HTMLElement | null;
        if (!labelEditor) throw new Error('Label editor not found');
        expect(within(labelEditor).getByLabelText('Group')).toBeInTheDocument();
        expect(within(labelEditor).getByLabelText('Description')).toBeInTheDocument();
    });

    it('waits for every reorder request before reporting failure and refetching', async () => {
        let resolveFirstUpdate: ((group: LabelGroup) => void) | undefined;
        let rejectSecondUpdate: ((reason: Error) => void) | undefined;
        labelServiceMock.updateGroup
            .mockImplementationOnce(() => new Promise<LabelGroup>(resolve => {
                resolveFirstUpdate = resolve;
            }))
            .mockImplementationOnce(() => new Promise<LabelGroup>((_resolve, reject) => {
                rejectSecondUpdate = reject;
            }));

        const { user } = renderWithProviders(<TemplateLabelSettings />);
        await openLabels();
        expect(labelServiceMock.getGroups).toHaveBeenCalledTimes(1);

        await rowAction(user, 'Workflow', 'Move down');

        await act(async () => {
            rejectSecondUpdate?.(new Error('ordering conflict'));
            await Promise.resolve();
        });
        expect(toastMock.error).not.toHaveBeenCalled();
        expect(labelServiceMock.getGroups).toHaveBeenCalledTimes(1);

        await act(async () => {
            resolveFirstUpdate?.(groupsFixture()[1]);
        });

        await waitFor(() => {
            expect(toastMock.error).toHaveBeenCalledWith(expect.stringMatching(
                /groupOrderSaveFailed|group order/i,
            ));
            expect(labelServiceMock.getGroups.mock.calls.length).toBeGreaterThan(1);
        });
    });

    it('keeps 23 labels under 40 buttons and lets an archive be undone', async () => {
        const labels = Array.from({ length: 23 }, (_, index) => labelFixture({ id: 200 + index, slug: `label-${index}`, name: `Label ${index}`, sort_order: index }));
        labelServiceMock.getGroups.mockResolvedValue([groupFixture({ labels })]);
        const { user } = renderWithProviders(<TemplateLabelSettings />);
        await openLabels();
        const panel = screen.getByRole('tabpanel', { name: 'Labels' });
        expect(within(panel).getAllByRole('button').length).toBeLessThan(40);

        await rowAction(user, 'Label 3', 'Archive label');
        await waitFor(() => expect(toastMock.success).toHaveBeenCalledWith('Archived label “Label 3”.', expect.objectContaining({ actionLabel: 'Undo' })));
        const [, options] = toastMock.success.mock.calls.find(([message]) => message === 'Archived label “Label 3”.')!;
        await act(async () => { await options.onAction(); });
        expect(labelServiceMock.updateLabel).toHaveBeenLastCalledWith(203, { is_active: true });
    });

    it('switches a template off with a labelled Active switch and edits it in the drawer', async () => {
        templateServiceMock.getAll.mockResolvedValue([{ id: 9, name: 'Bug report', description: null, template_type: 'task', is_active: true, sort_order: 10,
            seed_key: null, default_priority: null, default_effort_days: null, default_labels: [], default_description: null, default_checklist: [], default_payload: {},
            created_at: '2026-07-01T10:00:00Z', updated_at: '2026-07-01T10:00:00Z' }]);
        templateServiceMock.update.mockResolvedValue({});
        const { user } = renderWithProviders(<TemplateLabelSettings />);
        const active = await screen.findByRole('switch', { name: 'Active' });
        expect(active).toBeChecked();
        await user.click(active);
        await waitFor(() => expect(templateServiceMock.update).toHaveBeenCalledWith(9, { is_active: false }));
        await user.click(screen.getByRole('button', { name: 'Edit template: Bug report' }));
        expect(await screen.findByRole('dialog', { name: 'Edit template' })).toBeInTheDocument();
    });
});
