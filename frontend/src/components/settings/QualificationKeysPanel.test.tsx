import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { RoutingQualificationKey, RoutingQualificationKeyRegistry } from '../../types/agent';
import { renderWithProviders } from '../../test/renderWithProviders';
import { QualificationKeysPanel } from './QualificationKeysPanel';

const agentServiceMock = vi.hoisted(() => ({
    getQualificationKeys: vi.fn(),
    getQualificationKey: vi.fn(),
    declareQualificationKey: vi.fn(),
    reviseQualificationKey: vi.fn(),
    retireQualificationKey: vi.fn(),
}));
vi.mock('../../services/agentService', () => ({ agentService: agentServiceMock }));

const key = (overrides: Partial<RoutingQualificationKey> = {}): RoutingQualificationKey => ({
    id: 1,
    key: 'qualified.schema-review',
    label: 'Schema review',
    description: 'Reviews schema changes.',
    state: 'active',
    revision: 2,
    created_at: '2026-11-20T10:00:00Z',
    updated_at: '2026-11-21T10:00:00Z',
    retired_at: null,
    ...overrides,
});

const registry = (keys: RoutingQualificationKey[]): RoutingQualificationKeyRegistry => ({
    builtin_keys: ['backend-python', 'security-review'],
    keys,
});

const receipt = (result: RoutingQualificationKey) => ({
    operation: 'routing_qualification_key.declare',
    actor_id: null,
    target_type: 'routing_qualification_key' as const,
    target_id: result.id,
    idempotency_key: 'ui-1',
    rationale: 'reason',
    correlation_id: 'ui-1',
    authoritative_revision: result.revision,
    invalidated_assignment_ids: [],
    audit_event_ids: [1],
    result,
});

describe('QualificationKeysPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        agentServiceMock.getQualificationKeys.mockResolvedValue(registry([key()]));
    });

    it('lists declared keys beside the fixed built-in keys', async () => {
        renderWithProviders(<QualificationKeysPanel />);
        expect(await screen.findByText('qualified.schema-review')).toBeInTheDocument();
        expect(screen.getByText('Schema review')).toBeInTheDocument();
        expect(screen.getByText('Active')).toBeInTheDocument();
        const builtin = screen.getByRole('region', { name: 'Built-in keys' });
        expect(within(builtin).getByText('backend-python')).toBeInTheDocument();
        expect(agentServiceMock.getQualificationKeys).toHaveBeenCalledWith(false);
    });

    it('declares a key with the reason the server keeps with its revision', async () => {
        agentServiceMock.getQualificationKeys.mockResolvedValue(registry([]));
        agentServiceMock.declareQualificationKey.mockResolvedValue(receipt(key({ key: 'qualified.migrations', revision: 1 })));
        const { user } = renderWithProviders(<QualificationKeysPanel />);
        expect(await screen.findByText('No qualification keys are declared.')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Declare key' }));
        const dialog = screen.getByRole('dialog');
        await user.type(within(dialog).getByLabelText(/^Key/), ' Qualified.Migrations ');
        await user.type(within(dialog).getByLabelText(/^Label/), 'Migrations');
        const submit = within(dialog).getByRole('button', { name: 'Declare key' });
        expect(submit).toBeDisabled();
        await user.type(within(dialog).getByLabelText(/^Reason/), 'Passed the migration trial');
        await user.click(submit);

        await waitFor(() => expect(agentServiceMock.declareQualificationKey).toHaveBeenCalledTimes(1));
        const [data, metadata] = agentServiceMock.declareQualificationKey.mock.calls[0];
        expect(data).toEqual({ key: 'qualified.migrations', label: 'Migrations', description: null });
        expect(metadata.rationale).toBe('Passed the migration trial');
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
    });

    it('shows the entries and tasks that block retiring a key in use', async () => {
        agentServiceMock.retireQualificationKey.mockRejectedValue({
            response: {
                status: 409,
                data: {
                    detail: {
                        code: 'routing_qualification_key_in_use',
                        message: 'Qualification key is held by catalog entries or required by open tasks',
                        catalog_entries: [{ id: 3, key: 'schema-high', enabled: true }],
                        task_ids: [42],
                    },
                },
            },
        });
        const { user } = renderWithProviders(<QualificationKeysPanel />);
        await user.click(await screen.findByRole('button', { name: 'Retire' }));
        const dialog = screen.getByRole('dialog');
        await user.type(within(dialog).getByLabelText(/^Reason/), 'No longer routed');
        await user.click(within(dialog).getByRole('button', { name: 'Retire' }));

        expect(await within(dialog).findByRole('alert')).toHaveTextContent(
            'This key is still named by catalog entries schema-high and tasks #42.',
        );
        expect(agentServiceMock.retireQualificationKey).toHaveBeenCalledWith('qualified.schema-review', 2, expect.anything());
    });

    it('shows a key history with each reason and what names it', async () => {
        agentServiceMock.getQualificationKey.mockResolvedValue({
            ...key(),
            revisions: [
                { revision: 1, action: 'declare', state: 'active', label: 'Schema', description: null, reason: 'Trial passed', actor_type: 'operator', actor_id: null, correlation_id: 'c1', created_at: '2026-11-20T10:00:00Z' },
                { revision: 2, action: 'revise', state: 'active', label: 'Schema review', description: null, reason: 'Clearer name', actor_type: 'operator', actor_id: null, correlation_id: 'c2', created_at: '2026-11-21T10:00:00Z' },
            ],
            usage: { catalog_entries: [{ id: 3, key: 'schema-high', enabled: true }], task_ids: [], catalog_entries_omitted: 0, task_ids_omitted: 0 },
        });
        const { user } = renderWithProviders(<QualificationKeysPanel />);
        await user.click(await screen.findByRole('button', { name: 'History' }));
        const dialog = screen.getByRole('dialog');
        expect(await within(dialog).findByText('Trial passed')).toBeInTheDocument();
        expect(within(dialog).getByText('Clearer name')).toBeInTheDocument();
        expect(within(dialog).getByText('schema-high')).toBeInTheDocument();
        expect(agentServiceMock.getQualificationKey).toHaveBeenCalledWith('qualified.schema-review');
    });

    it('offers to declare a retired key again under the same name', async () => {
        agentServiceMock.getQualificationKeys.mockImplementation(async (includeRetired: boolean) => (
            registry(includeRetired ? [key({ state: 'retired', revision: 3, retired_at: '2026-11-22T10:00:00Z' })] : [])
        ));
        const { user } = renderWithProviders(<QualificationKeysPanel />);
        await screen.findByText('No qualification keys are declared.');
        await user.click(screen.getByRole('checkbox', { name: 'Show retired keys' }));
        expect(await screen.findByText('Retired')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Declare again' }));
        const keyField = within(screen.getByRole('dialog')).getByLabelText(/^Key/);
        expect(keyField).toHaveValue('qualified.schema-review');
        expect(keyField).toBeDisabled();
    });
});
