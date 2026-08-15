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

        await user.click(screen.getByRole('button', { name: 'Edit group: Workflow' }));
        const nameField = screen.getByRole('textbox', { name: 'Name' });
        await user.clear(nameField);
        await user.type(nameField, 'Workflow draft');

        await user.click(screen.getByRole('button', { name: 'Archive group: Governance' }));

        expect(nameField).toBeDisabled();
        expect(screen.getByRole('tab', { name: 'Templates' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Archive group: Workflow' })).toBeDisabled();

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

        await user.click(screen.getByRole('button', { name: 'Edit label: Planning' }));
        const nameField = screen.getByRole('textbox', { name: 'Name' });
        await user.clear(nameField);
        await user.type(nameField, 'Planning draft');

        await user.click(screen.getByRole('button', { name: 'Archive label: Delivery' }));

        await waitFor(() => {
            expect(labelServiceMock.updateLabel).toHaveBeenCalledWith(102, {
                is_active: false,
            });
        });
        expect(nameField).toHaveValue('Planning draft');
    });

    it('associates every manual editor label with its control', async () => {
        const { user } = renderWithProviders(<TemplateLabelSettings />);

        await user.click(await screen.findByRole('button', { name: 'New Template' }));
        expect(screen.getByLabelText('Type')).toBeInTheDocument();
        expect(screen.getByLabelText('Description')).toBeInTheDocument();
        expect(screen.getByLabelText('Default Description')).toBeInTheDocument();
        expect(screen.getByLabelText('Checklist')).toBeInTheDocument();
        expect(screen.getByLabelText('Default Payload JSON')).toBeInTheDocument();

        await openLabels();
        await user.click(screen.getByRole('button', { name: 'Edit group: Workflow' }));
        expect(screen.getByLabelText('Description')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Edit label: Planning' }));
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

        await user.click(screen.getByRole('button', { name: 'Move group down: Workflow' }));

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
});
