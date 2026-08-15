import { act, fireEvent, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { EmailSettings } from '../../types/emailSettings';
import { renderWithProviders } from '../../test/renderWithProviders';
import { EmailSettingsPanel } from './EmailSettingsPanel';

const adminAccessMock = vi.hoisted(() => ({
    useAdminAccess: vi.fn(),
}));

const emailSettingsServiceMock = vi.hoisted(() => ({
    getSettings: vi.fn(),
    updateSettings: vi.fn(),
    testConnection: vi.fn(),
}));

vi.mock('../../hooks/useAdminAccess', () => adminAccessMock);
vi.mock('../../services/emailSettingsService', () => ({
    emailSettingsService: emailSettingsServiceMock,
}));

const settingsFixture = (overrides: Partial<EmailSettings> = {}): EmailSettings => ({
    enabled: true,
    smtp_host: 'smtp.example.com',
    smtp_port: 587,
    smtp_user: 'mailer@example.com',
    smtp_from_email: 'notifications@example.com',
    smtp_use_tls: true,
    has_password: true,
    field_sources: {
        enabled: 'runtime',
        smtp_host: 'runtime',
        smtp_port: 'runtime',
        smtp_password: 'runtime',
        smtp_from_email: 'runtime',
    },
    ...overrides,
});

describe('EmailSettingsPanel', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
        emailSettingsServiceMock.getSettings.mockResolvedValue(settingsFixture());
        emailSettingsServiceMock.updateSettings.mockResolvedValue(settingsFixture());
        emailSettingsServiceMock.testConnection.mockResolvedValue({
            success: true,
            message: 'sent',
        });
    });

    it('blocks invalid enabled SMTP settings with visible, focused field errors', async () => {
        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const hostInput = await screen.findByLabelText('SMTP Host');
        const portInput = screen.getByLabelText('Port');
        const senderInput = screen.getByLabelText('From Email Address');

        await user.clear(hostInput);
        fireEvent.change(portInput, { target: { value: '70000' } });
        await user.clear(senderInput);
        await user.type(senderInput, 'not-an-email');
        await user.click(screen.getByRole('button', { name: 'Save Settings' }));

        expect(emailSettingsServiceMock.updateSettings).not.toHaveBeenCalled();
        expect(hostInput).toHaveFocus();
        expect(hostInput).toHaveAttribute('aria-invalid', 'true');
        expect(portInput).toHaveAttribute('aria-invalid', 'true');
        expect(senderInput).toHaveAttribute('aria-invalid', 'true');
        expect(screen.getByText(
            /Enter an SMTP host\.|surfaces\.emailSettings\.smtpHostRequired/,
        )).toHaveAttribute('role', 'alert');
        expect(screen.getByText(
            /Port must be a whole number from 1 to 65535\.|surfaces\.emailSettings\.smtpPortInvalid/,
        )).toHaveAttribute('role', 'alert');
        expect(screen.getByText(
            /Enter a valid email address\.|surfaces\.emailSettings\.emailAddressInvalid/,
        )).toHaveAttribute('role', 'alert');
    });

    it('still validates a configured host, sender address, and port when notifications are disabled', async () => {
        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const hostInput = await screen.findByLabelText('SMTP Host');
        const portInput = screen.getByLabelText('Port');
        const senderInput = screen.getByLabelText('From Email Address');
        const masterToggle = screen.getByRole('checkbox', {
            name: 'Enable email notifications for task updates',
        });

        await user.clear(hostInput);
        await user.type(hostInput, 'https://smtp.example.com');
        fireEvent.change(portInput, { target: { value: '0' } });
        await user.clear(senderInput);
        await user.type(senderInput, 'not-an-email');
        await user.click(masterToggle);
        await user.click(screen.getByRole('button', { name: 'Save Settings' }));

        expect(masterToggle).not.toBeChecked();
        expect(emailSettingsServiceMock.updateSettings).not.toHaveBeenCalled();
        expect(hostInput).toHaveAttribute('aria-invalid', 'true');
        expect(portInput).toHaveAttribute('aria-invalid', 'true');
        expect(senderInput).toHaveAttribute('aria-invalid', 'true');
    });

    it('allows a disabled configuration to save with a blank host when sender and port remain valid', async () => {
        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const hostInput = await screen.findByLabelText('SMTP Host');
        const masterToggle = screen.getByRole('checkbox', {
            name: 'Enable email notifications for task updates',
        });

        await user.clear(hostInput);
        await user.click(masterToggle);
        await user.click(screen.getByRole('button', { name: 'Save Settings' }));

        await waitFor(() => {
            expect(emailSettingsServiceMock.updateSettings).toHaveBeenCalledOnce();
        });
        expect(emailSettingsServiceMock.updateSettings.mock.calls[0]?.[0]).toEqual(
            expect.objectContaining({
                enabled: false,
                smtp_host: '',
                smtp_port: 587,
                smtp_from_email: 'notifications@example.com',
            }),
        );
    });

    it('makes replacing and clearing the stored password mutually exclusive', async () => {
        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const passwordInput = await screen.findByLabelText('Password / App Password');
        const clearPassword = screen.getByLabelText('Clear runtime password override');

        await user.type(passwordInput, 'replacement-secret');
        expect(clearPassword).not.toBeChecked();

        await user.click(clearPassword);
        expect(clearPassword).toBeChecked();
        expect(passwordInput).toHaveValue('');
        expect(passwordInput).toBeDisabled();

        await user.click(clearPassword);
        expect(clearPassword).not.toBeChecked();
        expect(passwordInput).toBeEnabled();
        await user.type(passwordInput, 'next-secret');
        expect(clearPassword).not.toBeChecked();
    });

    it('disables testing for dirty drafts and freezes configuration controls while saving', async () => {
        let resolveSave: ((settings: EmailSettings) => void) | undefined;
        emailSettingsServiceMock.updateSettings.mockImplementation(() => (
            new Promise<EmailSettings>(resolve => {
                resolveSave = resolve;
            })
        ));

        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const hostInput = await screen.findByLabelText('SMTP Host');
        const masterToggle = screen.getByRole('checkbox', {
            name: 'Enable email notifications for task updates',
        });
        const testRecipient = screen.getByLabelText(
            /Test recipient|surfaces\.emailSettings\.testRecipient/,
        );
        const testButton = screen.getByRole('button', { name: 'Test' });

        await user.clear(hostInput);
        await user.type(hostInput, 'smtp.next.example');

        expect(testButton).toBeDisabled();
        expect(screen.getByText(
            /Save your configuration changes before testing|surfaces\.emailSettings\.testSaveFirst/,
        )).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Save Settings' }));
        await waitFor(() => {
            expect(emailSettingsServiceMock.updateSettings).toHaveBeenCalledOnce();
        });
        expect(hostInput).toBeDisabled();
        expect(masterToggle).toBeDisabled();
        expect(testRecipient).toBeDisabled();

        await act(async () => {
            resolveSave?.(settingsFixture({ smtp_host: 'smtp.next.example' }));
        });

        await waitFor(() => {
            expect(hostInput).toBeEnabled();
            expect(testButton).toBeEnabled();
        });
        expect(screen.getByText(
            /Tests use the last saved email configuration|surfaces\.emailSettings\.testUsesSavedConfiguration/,
        )).toBeInTheDocument();
    });

    it('validates the test recipient locally and falls back to the saved sender address', async () => {
        const { user } = renderWithProviders(<EmailSettingsPanel />);
        const testRecipient = await screen.findByLabelText(
            /Test recipient|surfaces\.emailSettings\.testRecipient/,
        );
        const testButton = screen.getByRole('button', { name: 'Test' });

        await user.type(testRecipient, 'invalid-address');
        await user.click(testButton);

        expect(emailSettingsServiceMock.testConnection).not.toHaveBeenCalled();
        expect(testRecipient).toHaveFocus();
        expect(testRecipient).toHaveAttribute('aria-invalid', 'true');
        expect(screen.getByText(
            /Enter a valid email address\.|surfaces\.emailSettings\.emailAddressInvalid/,
        )).toHaveAttribute('role', 'alert');

        await user.clear(testRecipient);
        await user.click(testButton);

        await waitFor(() => {
            expect(emailSettingsServiceMock.testConnection).toHaveBeenCalledOnce();
        });
        expect(emailSettingsServiceMock.testConnection.mock.calls[0]?.[0]).toBe(
            'notifications@example.com',
        );
    });
});
