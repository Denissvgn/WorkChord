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

vi.mock('../../hooks/useAdminAccess', () => adminAccessHookMock);
vi.mock('../../utils/adminAccess', () => adminAccessStorageMock);

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
    'task-timeline',
    'agent-run-detail',
] as const;

describe('AdminAccessPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessHookMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
    });

    it('purges protected caches before refreshing with a replacement key', async () => {
        const queryClient = createTestQueryClient();
        const removeQueries = vi.spyOn(queryClient, 'removeQueries');
        const { user } = renderWithProviders(<AdminAccessPanel />, { queryClient });

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
        PROTECTED_QUERY_PREFIXES.forEach(queryKey => {
            expect(removeQueries).toHaveBeenCalledWith({
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
});
