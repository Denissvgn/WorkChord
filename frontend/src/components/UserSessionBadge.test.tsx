import { screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../test/renderWithProviders';
import { UserSessionBadge } from './UserSessionBadge';

const sessionServiceMock = vi.hoisted(() => ({
    getWhoAmI: vi.fn(),
}));

vi.mock('../services/sessionService', () => ({
    sessionService: sessionServiceMock,
}));

describe('UserSessionBadge', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        sessionServiceMock.getWhoAmI.mockResolvedValue({
            id: 1,
            public_id: 'workspace-abcdef12',
            display_name: 'Guest',
            created_at: '2026-08-04T09:00:00Z',
            last_seen_at: '2026-08-04T10:00:00Z',
        });
    });

    it('labels browser ownership identity without claiming authority', async () => {
        renderWithProviders(<UserSessionBadge />);

        const badge = await screen.findByLabelText(
            'Workspace identity: Guest CDEF12',
        );

        expect(badge).toHaveTextContent('Guest CDEF12');
        expect(badge).toHaveAttribute(
            'title',
            expect.stringContaining('does not grant admin or agent access'),
        );
    });
});
