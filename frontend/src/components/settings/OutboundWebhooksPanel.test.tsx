import { act, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type {
    OutboundWebhookDelivery,
    OutboundWebhookTarget,
} from '../../types/outboundWebhook';
import { renderWithProviders } from '../../test/renderWithProviders';
import { OutboundWebhooksPanel } from './OutboundWebhooksPanel';

const adminAccessMock = vi.hoisted(() => ({
    useAdminAccess: vi.fn(),
}));

const outboundWebhookServiceMock = vi.hoisted(() => ({
    getTargets: vi.fn(),
    createTarget: vi.fn(),
    updateTarget: vi.fn(),
    deleteTarget: vi.fn(),
    testTarget: vi.fn(),
    getDeliveries: vi.fn(),
    retryDelivery: vi.fn(),
}));

vi.mock('../../hooks/useAdminAccess', () => adminAccessMock);
vi.mock('../../services/outboundWebhookService', () => ({
    outboundWebhookService: outboundWebhookServiceMock,
}));

const targetFixture = (
    id: number,
    overrides: Partial<OutboundWebhookTarget> = {},
): OutboundWebhookTarget => ({
    id,
    name: `Target ${id}`,
    description: `Destination ${id}`,
    url: `https://hooks.example.com/${id}`,
    enabled: true,
    subscribed_events_json: ['task.*'],
    has_secret: true,
    headers_json: {},
    created_at: '2026-07-01T12:00:00Z',
    updated_at: '2026-07-02T12:00:00Z',
    ...overrides,
});

const deliveryFixture = (
    id: number,
    overrides: Partial<OutboundWebhookDelivery> = {},
): OutboundWebhookDelivery => ({
    id,
    target_id: 1,
    event_id: id,
    target_name: 'Target 1',
    target_url: 'https://hooks.example.com/1',
    status: 'failed',
    attempt_count: 1,
    last_http_status: 500,
    last_error: 'Endpoint rejected the request',
    last_attempt_at: '2026-07-02T12:00:00Z',
    created_at: '2026-07-02T12:00:00Z',
    updated_at: '2026-07-02T12:00:00Z',
    event: {
        id,
        event_id: `event-${id}`,
        event_type: 'task.updated',
        entity_type: 'task',
        entity_id: 42,
        payload_json: {},
        occurred_at: '2026-07-02T12:00:00Z',
    },
    ...overrides,
});

describe('OutboundWebhooksPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
        outboundWebhookServiceMock.getTargets.mockResolvedValue([
            targetFixture(1),
            targetFixture(2),
        ]);
        outboundWebhookServiceMock.getDeliveries.mockResolvedValue([]);
        outboundWebhookServiceMock.createTarget.mockResolvedValue(targetFixture(3));
        outboundWebhookServiceMock.updateTarget.mockResolvedValue(targetFixture(1));
        outboundWebhookServiceMock.deleteTarget.mockResolvedValue({ success: true, message: 'deleted' });
        outboundWebhookServiceMock.testTarget.mockResolvedValue({
            delivery: deliveryFixture(10, { status: 'delivered' }),
        });
        outboundWebhookServiceMock.retryDelivery.mockResolvedValue({
            delivery: deliveryFixture(10, { status: 'delivered' }),
        });
    });

    it('blocks blank names and non-HTTP endpoint URLs with associated field errors', async () => {
        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        const name = await screen.findByLabelText('Name');
        const url = screen.getByLabelText('URL');

        await user.type(url, 'ftp://files.example.com/webhook');
        await user.click(screen.getByRole('button', { name: 'Create Target' }));

        expect(outboundWebhookServiceMock.createTarget).not.toHaveBeenCalled();
        expect(name).toHaveAttribute('aria-invalid', 'true');
        expect(url).toHaveAttribute('aria-invalid', 'true');
        expect(screen.getByText('Target name is required')).toHaveAttribute('role', 'alert');
        expect(screen.getByText(
            /Enter a valid HTTP or HTTPS URL|settingsWebhooks\.urlInvalid/,
        )).toHaveAttribute('role', 'alert');
    });

    it('makes replacing and clearing the stored secret mutually exclusive', async () => {
        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        await screen.findByRole('heading', { name: 'Outbound Webhooks' });
        await user.click(screen.getByRole('button', { name: 'Edit: Target 1' }));

        const secret = screen.getByPlaceholderText('Leave unchanged');
        const clearSecret = screen.getByLabelText('Clear stored secret on save');
        await user.type(secret, 'replacement-secret');
        await user.click(clearSecret);

        expect(secret).toBeDisabled();
        expect(secret).toHaveValue('');
        expect(clearSecret).toBeChecked();

        await user.click(screen.getByRole('button', { name: 'Save Target' }));

        await waitFor(() => {
            expect(outboundWebhookServiceMock.updateTarget).toHaveBeenCalledOnce();
        });
        expect(outboundWebhookServiceMock.updateTarget.mock.calls[0]?.[1]).toEqual(
            expect.objectContaining({ secret: null }),
        );
    });

    it('requires explicit discard confirmation before New, Edit, or Cancel replaces a dirty draft', async () => {
        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        await screen.findByRole('heading', { name: 'Outbound Webhooks' });
        await user.click(screen.getByRole('button', { name: 'Edit: Target 1' }));

        const name = screen.getByLabelText('Name');
        await user.clear(name);
        await user.type(name, 'Keep this webhook draft');
        await user.click(screen.getByRole('button', { name: 'Cancel' }));

        let dialog = screen.getByRole('dialog');
        expect(name).toHaveValue('Keep this webhook draft');
        await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
        expect(name).toHaveValue('Keep this webhook draft');

        await user.click(screen.getByRole('button', { name: 'Edit: Target 2' }));
        dialog = screen.getByRole('dialog');
        expect(name).toHaveValue('Keep this webhook draft');
        await user.click(within(dialog).getByRole('button', { name: 'Discard changes' }));
        expect(name).toHaveValue('Target 2');

        await user.clear(name);
        await user.type(name, 'Another dirty draft');
        await user.click(screen.getByRole('button', { name: 'New Target' }));
        dialog = screen.getByRole('dialog');
        expect(name).toHaveValue('Another dirty draft');
        await user.click(within(dialog).getByRole('button', { name: 'Discard changes' }));
        expect(name).toHaveValue('');
    });

    it('reconciles a same-target row toggle into the editor without losing other draft fields', async () => {
        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        await screen.findByRole('heading', { name: 'Outbound Webhooks' });
        await user.click(screen.getByRole('button', { name: 'Edit: Target 1' }));

        const description = screen.getByLabelText('Description');
        await user.clear(description);
        await user.type(description, 'Keep this description');
        await user.click(screen.getByRole('checkbox', { name: 'Target 1: Enabled' }));

        await waitFor(() => {
            expect(outboundWebhookServiceMock.updateTarget.mock.calls[0]?.slice(0, 2)).toEqual([
                1,
                { enabled: false },
            ]);
        });
        expect(screen.getByRole('checkbox', { name: 'Enabled' })).not.toBeChecked();
        expect(description).toHaveValue('Keep this description');

        await user.click(screen.getByRole('button', { name: 'Save Target' }));
        await waitFor(() => expect(outboundWebhookServiceMock.updateTarget).toHaveBeenCalledTimes(2));
        expect(outboundWebhookServiceMock.updateTarget.mock.calls[1]?.[1]).toEqual(
            expect.objectContaining({
                description: 'Keep this description',
                enabled: false,
            }),
        );
    });

    it('treats a reconciled same-target toggle as the editor baseline', async () => {
        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        await screen.findByRole('heading', { name: 'Outbound Webhooks' });
        await user.click(screen.getByRole('button', { name: 'Edit: Target 1' }));
        await user.click(screen.getByRole('checkbox', { name: 'Target 1: Enabled' }));

        await waitFor(() => expect(outboundWebhookServiceMock.updateTarget).toHaveBeenCalled());
        await user.click(screen.getByRole('button', { name: 'New Target' }));

        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByLabelText('Name')).toHaveValue('');
    });

    it('freezes the draft and all target rows while saving', async () => {
        let resolveCreate: ((target: OutboundWebhookTarget) => void) | undefined;
        outboundWebhookServiceMock.createTarget.mockImplementation(() => (
            new Promise<OutboundWebhookTarget>(resolve => {
                resolveCreate = resolve;
            })
        ));

        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        const name = await screen.findByLabelText('Name');
        const url = screen.getByLabelText('URL');
        await user.type(name, 'New destination');
        await user.type(url, 'https://hooks.example.com/new');
        await user.click(screen.getByRole('button', { name: 'Create Target' }));

        await waitFor(() => {
            expect(outboundWebhookServiceMock.createTarget).toHaveBeenCalledOnce();
        });
        expect(name).toBeDisabled();
        expect(url).toBeDisabled();
        expect(screen.getByRole('button', { name: 'New Target' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Send test delivery: Target 1' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Edit: Target 2' })).toBeDisabled();

        await act(async () => {
            resolveCreate?.(targetFixture(3));
        });
        await waitFor(() => expect(screen.getByLabelText('Name')).toBeEnabled());
    });

    it('shows pending feedback only on the active row while locking concurrent row actions', async () => {
        let resolveTest: ((response: { delivery: OutboundWebhookDelivery }) => void) | undefined;
        outboundWebhookServiceMock.testTarget.mockImplementation(() => (
            new Promise<{ delivery: OutboundWebhookDelivery }>(resolve => {
                resolveTest = resolve;
            })
        ));

        const { user } = renderWithProviders(<OutboundWebhooksPanel />);
        const firstTest = await screen.findByRole('button', { name: 'Send test delivery: Target 1' });
        const secondTest = screen.getByRole('button', { name: 'Send test delivery: Target 2' });
        await user.click(firstTest);

        await waitFor(() => expect(outboundWebhookServiceMock.testTarget.mock.calls[0]?.[0]).toBe(1));
        expect(firstTest.querySelector('.animate-spin')).toBeInTheDocument();
        expect(secondTest.querySelector('.animate-spin')).not.toBeInTheDocument();
        expect(firstTest).toBeDisabled();
        expect(secondTest).toBeDisabled();

        await act(async () => {
            resolveTest?.({ delivery: deliveryFixture(10, { status: 'delivered' }) });
        });
        await waitFor(() => expect(secondTest).toBeEnabled());
    });

    it('renders delivery failures without a contradictory empty state', async () => {
        outboundWebhookServiceMock.getDeliveries.mockRejectedValue({
            response: { status: 503, data: { detail: 'Delivery history is unavailable.' } },
        });

        renderWithProviders(<OutboundWebhooksPanel />);

        expect(await screen.findByText('Delivery history is unavailable.')).toBeInTheDocument();
        expect(screen.queryByText('No webhook deliveries yet.')).not.toBeInTheDocument();
    });

    it('explains why delivered or orphaned deliveries cannot be retried', async () => {
        outboundWebhookServiceMock.getDeliveries.mockResolvedValue([
            deliveryFixture(20, { status: 'delivered' }),
            deliveryFixture(21, { target_id: null, target_name: null, status: 'failed' }),
        ]);

        renderWithProviders(<OutboundWebhooksPanel />);

        expect(await screen.findByText(
            /Already delivered; no retry is needed|settingsWebhooks\.retryAlreadyDelivered/,
        )).toBeInTheDocument();
        expect(screen.getByText(
            /Target deleted\. Create a new target for future events|settingsWebhooks\.retryTargetUnavailable/,
        )).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: /Retry delivery/ })).not.toBeInTheDocument();
    });
});
