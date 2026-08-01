import { screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { SystemSettings } from '../../types/systemSettings';
import { renderWithProviders } from '../../test/renderWithProviders';
import { RuntimeConfigSettings } from './RuntimeConfigSettings';

const adminAccessMock = vi.hoisted(() => ({
    useAdminAccess: vi.fn(),
}));

const systemSettingsServiceMock = vi.hoisted(() => ({
    getSettings: vi.fn(),
    updateApp: vi.fn(),
    updateLLM: vi.fn(),
    updateGitHub: vi.fn(),
    updateWebIntake: vi.fn(),
}));

vi.mock('../../hooks/useAdminAccess', () => adminAccessMock);
vi.mock('../../services/systemSettingsService', () => ({
    systemSettingsService: systemSettingsServiceMock,
}));

const settingsFixture = (): SystemSettings => ({
    app: {
        ui_language: 'en',
        ai_language_mode: 'auto',
        field_sources: {},
    },
    llm: {
        provider: 'openai',
        api_url: 'https://api.openai.com/v1',
        model: 'gpt-5',
        temperature: 0.2,
        max_output_tokens: 3000,
        has_api_key: true,
        field_sources: {},
    },
    github: {
        api_url: 'https://api.github.com',
        request_timeout_seconds: 10,
        webhook_create_triage_for_unmatched: false,
        has_token: true,
        has_webhook_secret: true,
        field_sources: {},
    },
    web_intake: {
        rate_limit_per_minute: 30,
        has_token: true,
        field_sources: {},
    },
    restart_required: [],
});

const renderRuntimeSettings = () => renderWithProviders(<RuntimeConfigSettings />);

describe('RuntimeConfigSettings', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        const settings = settingsFixture();
        adminAccessMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
        systemSettingsServiceMock.getSettings.mockResolvedValue(settings);
        systemSettingsServiceMock.updateApp.mockResolvedValue(settings.app);
        systemSettingsServiceMock.updateLLM.mockResolvedValue(settings.llm);
        systemSettingsServiceMock.updateGitHub.mockResolvedValue(settings.github);
        systemSettingsServiceMock.updateWebIntake.mockResolvedValue(settings.web_intake);
    });

    it('keeps all save actions disabled until their own settings change', async () => {
        renderRuntimeSettings();

        await screen.findByRole('heading', { name: 'LLM Provider' });

        expect(screen.getByRole('button', { name: 'Save AI Language' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Save LLM' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Save GitHub' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Save Web Intake' })).toBeDisabled();
    });

    it('blocks invalid required, URL, and backend-bound numeric values without losing the draft', async () => {
        const { user } = renderRuntimeSettings();

        const model = await screen.findByLabelText('Model');
        const apiUrl = screen.getByLabelText('API URL override');
        const temperature = screen.getByLabelText('Temperature');
        const maxOutputTokens = screen.getByLabelText('Max output tokens');

        await user.clear(model);
        await user.clear(apiUrl);
        await user.type(apiUrl, 'not-a-url');
        await user.clear(temperature);
        await user.type(temperature, '3');
        await user.clear(maxOutputTokens);
        await user.type(maxOutputTokens, '255');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        expect(systemSettingsServiceMock.updateLLM).not.toHaveBeenCalled();
        expect(model).toHaveValue('');
        expect(apiUrl).toHaveValue('not-a-url');
        expect(temperature).toHaveValue(3);
        expect(maxOutputTokens).toHaveValue(255);
        expect(model).toHaveAttribute('aria-invalid', 'true');
        expect(apiUrl).toHaveAttribute('aria-invalid', 'true');
        expect(screen.getAllByRole('alert').some(alert => (
            alert.textContent?.includes('Review the highlighted fields before saving.')
        ))).toBe(true);

        const githubTimeout = screen.getByLabelText('Request timeout seconds');
        const rateLimit = screen.getByLabelText('Rate limit per minute');
        await user.clear(githubTimeout);
        await user.type(githubTimeout, '121');
        await user.click(screen.getByRole('button', { name: 'Save GitHub' }));
        await user.clear(rateLimit);
        await user.type(rateLimit, '10001');
        await user.click(screen.getByRole('button', { name: 'Save Web Intake' }));

        expect(systemSettingsServiceMock.updateGitHub).not.toHaveBeenCalled();
        expect(systemSettingsServiceMock.updateWebIntake).not.toHaveBeenCalled();
        expect(githubTimeout).toHaveAttribute('aria-invalid', 'true');
        expect(rateLimit).toHaveAttribute('aria-invalid', 'true');
    });

    it('requires an API key action before changing the LLM endpoint host and never sends conflicting secret intent', async () => {
        const { user } = renderRuntimeSettings();

        const apiUrl = await screen.findByLabelText('API URL override');
        const apiKey = screen.getByLabelText('Replace API key');
        const clearApiKey = screen.getByRole('checkbox', { name: 'Clear runtime API key override' });

        await user.clear(apiUrl);
        await user.type(apiUrl, 'https://llm.example.test/v1');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        expect(systemSettingsServiceMock.updateLLM).not.toHaveBeenCalled();
        expect(apiKey).toHaveAttribute('aria-invalid', 'true');
        expect(apiUrl).toHaveValue('https://llm.example.test/v1');

        await user.type(apiKey, 'rotated-key');
        expect(clearApiKey).not.toBeChecked();
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        await waitFor(() => {
            expect(systemSettingsServiceMock.updateLLM).toHaveBeenCalled();
        });
        expect(systemSettingsServiceMock.updateLLM.mock.calls[0][0]).toEqual(expect.objectContaining({
                api_url: 'https://llm.example.test/v1',
                api_key: 'rotated-key',
                clear_api_key: false,
        }));
    });

    it('requires a credential decision when a default provider endpoint becomes custom', async () => {
        const settings = settingsFixture();
        settings.llm.api_url = '';
        systemSettingsServiceMock.getSettings.mockResolvedValueOnce(settings);
        const { user } = renderRuntimeSettings();

        await user.selectOptions(await screen.findByLabelText('Provider'), 'custom');
        const apiUrl = screen.getByLabelText('API URL override');
        await user.type(apiUrl, 'https://custom-llm.example.test/v1');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        expect(systemSettingsServiceMock.updateLLM).not.toHaveBeenCalled();
        expect(screen.getByLabelText('Replace API key')).toHaveAttribute('aria-invalid', 'true');
    });

    it('requires a credential decision for a provider-only change', async () => {
        const { user } = renderRuntimeSettings();

        await user.selectOptions(await screen.findByLabelText('Provider'), 'openrouter');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        expect(systemSettingsServiceMock.updateLLM).not.toHaveBeenCalled();
        expect(screen.getByLabelText('Replace API key')).toHaveAttribute('aria-invalid', 'true');
    });

    it('clears and disables replacement secrets, then submits an explicit clear without the secret value', async () => {
        const { user } = renderRuntimeSettings();

        const apiKey = await screen.findByLabelText('Replace API key');
        const clearApiKey = screen.getByRole('checkbox', { name: 'Clear runtime API key override' });
        await user.type(apiKey, 'temporary-key');
        await user.click(clearApiKey);

        expect(apiKey).toBeDisabled();
        expect(apiKey).toHaveValue('');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        await waitFor(() => {
            expect(systemSettingsServiceMock.updateLLM).toHaveBeenCalled();
        });
        expect(systemSettingsServiceMock.updateLLM.mock.calls[0][0]).toEqual(expect.objectContaining({
            clear_api_key: true,
        }));
        expect(systemSettingsServiceMock.updateLLM.mock.calls[0][0]).not.toHaveProperty('api_key');

        const githubApiUrl = screen.getByLabelText('GitHub API URL');
        const githubToken = screen.getByLabelText('Replace GitHub token');
        const githubClearToken = screen.getAllByRole('checkbox', { name: 'Clear runtime token override' })[0];
        await user.clear(githubApiUrl);
        await user.type(githubApiUrl, 'https://github.example.test/api/v3');
        await user.click(screen.getByRole('button', { name: 'Save GitHub' }));

        expect(systemSettingsServiceMock.updateGitHub).not.toHaveBeenCalled();
        expect(githubToken).toHaveAttribute('aria-invalid', 'true');

        await user.type(githubToken, 'temporary-github-token');
        await user.click(githubClearToken);

        expect(githubToken).toBeDisabled();
        expect(githubToken).toHaveValue('');
        await user.click(screen.getByRole('button', { name: 'Save GitHub' }));

        await waitFor(() => {
            expect(systemSettingsServiceMock.updateGitHub).toHaveBeenCalled();
        });
        expect(systemSettingsServiceMock.updateGitHub.mock.calls[0][0]).toEqual(expect.objectContaining({
            clear_token: true,
        }));
        expect(systemSettingsServiceMock.updateGitHub.mock.calls[0][0]).not.toHaveProperty('token');
    });

    it('keeps a failed mutation draft visible in the accessible error summary', async () => {
        systemSettingsServiceMock.updateLLM.mockRejectedValueOnce({
            response: { status: 500, data: { detail: 'The endpoint rejected this model.' } },
        });
        const { user } = renderRuntimeSettings();

        const model = await screen.findByLabelText('Model');
        await user.clear(model);
        await user.type(model, 'gpt-5.6');
        await user.click(screen.getByRole('button', { name: 'Save LLM' }));

        expect((await screen.findAllByText('The endpoint rejected this model.')).length).toBeGreaterThan(0);
        expect(model).toHaveValue('gpt-5.6');
        expect(screen.getByRole('button', { name: 'Save LLM' })).toBeEnabled();
    });
});
