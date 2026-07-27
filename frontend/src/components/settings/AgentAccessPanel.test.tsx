import { act, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { AgentCapabilities } from '../../types/agent';
import {
    createTestQueryClient,
    renderWithProviders,
} from '../../test/renderWithProviders';
import { AgentAccessPanel } from './AgentAccessPanel';

const agentAccessHookMock = vi.hoisted(() => ({
    useAgentAccess: vi.fn(),
}));

const agentAccessStorageMock = vi.hoisted(() => ({
    setAgentApiKey: vi.fn(),
    clearAgentApiKey: vi.fn(),
}));

const agentServiceMock = vi.hoisted(() => ({
    getCapabilities: vi.fn(),
}));

vi.mock('../../hooks/useAgentAccess', () => agentAccessHookMock);
vi.mock('../../utils/agentAccess', () => agentAccessStorageMock);
vi.mock('../../services/agentService', () => ({
    agentService: agentServiceMock,
}));

const capabilitiesFixture = (
    name: string,
    displayName: string,
): AgentCapabilities => ({
    server_version: '1.6.2',
    api_contract: 'workchord-agent/v1',
    actor: {
        id: name === 'old-admin' ? 1 : 2,
        name,
        display_name: displayName,
        scopes: ['admin'],
        enabled: true,
        role: 'pm',
        profile_id: null,
        work_policy: 'assigned_only',
        max_parallel_work: 1,
        queue_revision: 1,
        created_at: '2026-07-28T10:00:00Z',
        last_seen_at: '2026-07-28T10:30:00Z',
    },
    scopes: ['admin'],
    lease_limits: {
        minimum_seconds: 60,
        default_seconds: 3600,
        maximum_seconds: 86400,
    },
    features: ['actor-roster-v1'],
    recommended_skills: {},
    lifecycle_actions: [],
    skill_catalog_version: null,
    skill_catalog_url: null,
    skill_discovery_url: null,
});

const PRINCIPAL_QUERY_PREFIXES = [
    'agent-capabilities',
    'agent-actor-roster',
    'agent-model-catalog',
    'agent-model-bindings',
    'agent-profile-skill-catalog',
    'routing-assessment',
    'routing-preview',
    'agent-assignments',
    'agent-pipeline',
    'task-timeline',
    'agent-run-detail',
] as const;

describe('AgentAccessPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        agentAccessHookMock.useAgentAccess.mockReturnValue({ hasAgentKey: true });
    });

    it('removes cached capabilities before validating a replacement key', async () => {
        const oldCapabilities = capabilitiesFixture('old-admin', 'Old Admin');
        const newCapabilities = capabilitiesFixture('new-admin', 'New Admin');
        let resolveReplacement: ((value: AgentCapabilities) => void) | undefined;
        agentServiceMock.getCapabilities
            .mockResolvedValueOnce(oldCapabilities)
            .mockImplementationOnce(() => new Promise<AgentCapabilities>(resolve => {
                resolveReplacement = resolve;
            }));

        const queryClient = createTestQueryClient();
        const { user } = renderWithProviders(<AgentAccessPanel />, { queryClient });

        expect(await screen.findByText('Old Admin')).toBeInTheDocument();
        const otherPrincipalQueries = [
            ['agent-actor-roster', true],
            ['agent-model-catalog', true],
            ['agent-model-bindings', true],
            ['agent-profile-skill-catalog'],
            ['routing-assessment', 41, 2],
            ['routing-preview', 41],
            ['agent-assignments', 41, 'execution', 'queued'],
            ['agent-pipeline'],
            ['task-timeline', 41],
            ['agent-run-detail', 73],
        ] as const;
        otherPrincipalQueries.forEach(queryKey => {
            queryClient.setQueryData([...queryKey], { owner: 'old-admin' });
        });
        await user.type(
            screen.getByLabelText('Agent API key'),
            'replacement-key',
        );
        await user.click(screen.getByRole('button', { name: 'Use actor key' }));

        expect(agentAccessStorageMock.setAgentApiKey).toHaveBeenCalledWith('replacement-key');
        await waitFor(() => {
            expect(screen.queryByText('Old Admin')).not.toBeInTheDocument();
            expect(screen.getByRole('status')).toHaveTextContent('Checking actor access');
            otherPrincipalQueries.forEach(queryKey => {
                expect(queryClient.getQueryData([...queryKey])).toBeUndefined();
            });
        });

        await act(async () => {
            resolveReplacement?.(newCapabilities);
        });
        expect(await screen.findByText('New Admin')).toBeInTheDocument();
    });

    it('does not render a stale green identity after a capabilities error', async () => {
        const queryClient = createTestQueryClient();
        queryClient.setQueryData(
            ['agent-capabilities'],
            capabilitiesFixture('old-admin', 'Old Admin'),
        );
        agentServiceMock.getCapabilities.mockRejectedValue({
            response: {
                status: 401,
                data: { detail: 'The replacement key is invalid.' },
            },
        });

        renderWithProviders(<AgentAccessPanel />, { queryClient });

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'The replacement key is invalid.',
        );
        expect(screen.queryByText('Old Admin')).not.toBeInTheDocument();
        expect(screen.getByRole('status')).toHaveTextContent('Actor access failed');
        expect(screen.getByRole('status')).toHaveClass('border-feedback-danger-border');
        expect(screen.getByRole('status')).not.toHaveClass('border-feedback-success-border');
    });

    it('purges every principal-scoped query family when the key is cleared', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture('old-admin', 'Old Admin'),
        );
        const queryClient = createTestQueryClient();
        const removeQueries = vi.spyOn(queryClient, 'removeQueries');
        const { user } = renderWithProviders(<AgentAccessPanel />, { queryClient });

        expect(await screen.findByText('Old Admin')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Clear' }));

        expect(agentAccessStorageMock.clearAgentApiKey).toHaveBeenCalledOnce();
        PRINCIPAL_QUERY_PREFIXES.forEach(queryKey => {
            expect(removeQueries).toHaveBeenCalledWith({
                queryKey: [queryKey],
            });
        });
    });
});
