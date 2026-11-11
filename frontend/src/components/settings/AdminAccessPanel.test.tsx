import { screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import {
    createTestQueryClient,
    renderWithProviders,
} from '../../test/renderWithProviders';
import { AdminAccessPanel } from './AdminAccessPanel';

const adminAccessHookMock = vi.hoisted(() => ({
    useAdminAccess: vi.fn(),
}));

const adminAccessStorageMock = vi.hoisted(() => ({
    setAdminApiKey: vi.fn(),
    clearAdminApiKey: vi.fn(),
}));

const schedulingRulesMock = vi.hoisted(() => ({
    schedulingRulesService: { getRules: vi.fn() },
}));

vi.mock('../../hooks/useAdminAccess', () => adminAccessHookMock);
vi.mock('../../utils/adminAccess', () => adminAccessStorageMock);
vi.mock('../../services/schedulingRulesService', () => schedulingRulesMock);

const PROTECTED_QUERY_PREFIXES = [
    'system-settings',
    'scheduling-rules',
    'email-settings',
    'outbound-webhook-targets',
    'outbound-webhook-deliveries',
    'agent-capabilities',
    'agent-actor-roster',
    'agent-model-catalog',
    'agent-model-bindings',
    'agent-profile-skill-catalog',
    'routing-assessment',
    'routing-preview',
    'agent-assignments',
    'agent-pipeline',
    'agent-team-setup',
    'task-timeline',
    'agent-run-detail',
] as const;

describe('AdminAccessPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessHookMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
        schedulingRulesMock.schedulingRulesService.getRules.mockResolvedValue({ rules: {}, source: 'defaults' });
    });

    it('purges protected caches before refreshing with a replacement key', async () => {
        const queryClient = createTestQueryClient();
        const removeQueries = vi.spyOn(queryClient, 'removeQueries');
        const invalidateQueries = vi.spyOn(queryClient, 'invalidateQueries');
        const { user } = renderWithProviders(<AdminAccessPanel />, { queryClient });

        expect(screen.getByRole('status')).toHaveTextContent(
            i18n.t('settings.adminAccessConfigured'),
        );
        expect(screen.getByRole('status')).toHaveClass(
            'border-feedback-info-border',
        );
        expect(screen.getByRole('status')).not.toHaveClass(
            'border-feedback-success-border',
        );

        await user.type(
            screen.getByLabelText(i18n.t('settings.adminAccessField')),
            'replacement-admin-key',
        );
        await user.click(screen.getByRole('button', {
            name: i18n.t('settings.adminAccessSave'),
        }));

        expect(adminAccessStorageMock.setAdminApiKey).toHaveBeenCalledWith(
            'replacement-admin-key',
        );
        expect(await screen.findByText(i18n.t('settings.adminAccessAccepted'))).toBeInTheDocument();
        PROTECTED_QUERY_PREFIXES.forEach(queryKey => {
            expect(removeQueries).toHaveBeenCalledWith({
                queryKey: [queryKey],
            });
            expect(invalidateQueries).toHaveBeenCalledWith({
                queryKey: [queryKey],
            });
        });
    });

    it('purges protected caches when the key is cleared', async () => {
        const queryClient = createTestQueryClient();
        const removeQueries = vi.spyOn(queryClient, 'removeQueries');
        const { user } = renderWithProviders(<AdminAccessPanel />, { queryClient });

        await user.click(screen.getByRole('button', {
            name: i18n.t('settings.adminAccessClear'),
        }));

        expect(adminAccessStorageMock.clearAdminApiKey).toHaveBeenCalledOnce();
        PROTECTED_QUERY_PREFIXES.forEach(queryKey => {
            expect(removeQueries).toHaveBeenCalledWith({
                queryKey: [queryKey],
            });
        });
    });

    it('does not keep a key the server rejects', async () => {
        schedulingRulesMock.schedulingRulesService.getRules.mockRejectedValue(
            Object.assign(new Error('Unauthorized'), { isAxiosError: true, response: { status: 401, data: {} } }),
        );
        const { user } = renderWithProviders(<AdminAccessPanel />, { queryClient: createTestQueryClient() });

        await user.type(screen.getByLabelText(i18n.t('settings.adminAccessField')), 'wrong-key');
        await user.click(screen.getByRole('button', { name: i18n.t('settings.adminAccessSave') }));

        expect(await screen.findByText(i18n.t('settings.adminAccessRejected'))).toBeInTheDocument();
        expect(adminAccessStorageMock.clearAdminApiKey).toHaveBeenCalledOnce();
        expect(screen.getByLabelText(i18n.t('settings.adminAccessField'))).toHaveValue('wrong-key');
    });
});
