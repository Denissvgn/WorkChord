import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Globe2, KeyRound, RefreshCcw, Save, ServerCog, ShieldAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import { QueryEmptyState, QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { systemSettingsService } from '../../services/systemSettingsService';
import { getAdminAccessErrorMessage } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import type {
    AILanguageMode,
    AppRuntimeSettingsUpdate,
    GitHubRuntimeSettingsUpdate,
    LLMProvider,
    LLMRuntimeSettingsUpdate,
    RuntimeSettingSource,
    SystemSettings,
    WebIntakeRuntimeSettingsUpdate,
} from '../../types/systemSettings';

interface LLMForm {
    provider: LLMProvider;
    api_url: string;
    model: string;
    temperature: number;
    max_output_tokens: number;
    api_key: string;
    clear_api_key: boolean;
}

interface AppForm {
    ai_language_mode: AILanguageMode;
}

interface GitHubForm {
    api_url: string;
    token: string;
    clear_token: boolean;
    request_timeout_seconds: number;
    webhook_secret: string;
    clear_webhook_secret: boolean;
    webhook_create_triage_for_unmatched: boolean;
}

interface WebIntakeForm {
    token: string;
    clear_token: boolean;
    rate_limit_per_minute: number;
}

const sourceClass: Record<RuntimeSettingSource, string> = {
    runtime: 'bg-action-muted text-action border-action',
    environment: 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border',
    default: 'bg-surface-muted text-content-secondary border-border',
};

const SourceBadge = ({ source }: { source?: RuntimeSettingSource }) => {
    const { t } = useTranslation();
    if (!source) return null;
    return (
        <span className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${sourceClass[source]}`}>
            {t(`common.${source}`)}
        </span>
    );
};

const SecretState = ({ configured, source }: { configured: boolean; source?: RuntimeSettingSource }) => {
    const { t } = useTranslation();
    return (
        <div className="flex items-center gap-2 text-sm text-content-secondary">
            <KeyRound className="h-4 w-4" />
            <span>{configured ? t('common.configured') : t('common.notConfigured')}</span>
            <SourceBadge source={source} />
        </div>
    );
};

const fieldSource = (settings: { field_sources: Record<string, RuntimeSettingSource> }, field: string) => (
    settings.field_sources?.[field]
);

export const RuntimeConfigSettings = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const toast = useToast();
    const [appForm, setAppForm] = useState<AppForm | null>(null);
    const [llmForm, setLlmForm] = useState<LLMForm | null>(null);
    const [githubForm, setGithubForm] = useState<GitHubForm | null>(null);
    const [webIntakeForm, setWebIntakeForm] = useState<WebIntakeForm | null>(null);

    const { data: settings, isLoading, error, isError, refetch } = useQuery({
        queryKey: ['system-settings'],
        queryFn: systemSettingsService.getSettings,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
    });

    const refreshSettings = (updated?: Partial<SystemSettings>) => {
        queryClient.setQueryData<SystemSettings>(['system-settings'], (current) => (
            current ? { ...current, ...updated } : current
        ));
        queryClient.invalidateQueries({ queryKey: ['system-settings'] });
    };

    const llmMutation = useMutation({
        mutationFn: systemSettingsService.updateLLM,
        onSuccess: (llm) => {
            refreshSettings({ llm });
            setLlmForm(null);
            toast.success(t('settings.llmSaved'));
        },
        onError: (err: unknown) => toast.error(getAdminAccessErrorMessage(err, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.llmSaveFailed'),
        })),
    });

    const appMutation = useMutation({
        mutationFn: systemSettingsService.updateApp,
        onSuccess: (app) => {
            refreshSettings({ app });
            setAppForm(null);
            toast.success(t('settings.aiLanguageSaved'));
        },
        onError: (err: unknown) => toast.error(getAdminAccessErrorMessage(err, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.aiLanguageSaveFailed'),
        })),
    });

    const githubMutation = useMutation({
        mutationFn: systemSettingsService.updateGitHub,
        onSuccess: (github) => {
            refreshSettings({ github });
            setGithubForm(null);
            toast.success(t('settings.githubSaved'));
        },
        onError: (err: unknown) => toast.error(getAdminAccessErrorMessage(err, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.githubSaveFailed'),
        })),
    });

    const webIntakeMutation = useMutation({
        mutationFn: systemSettingsService.updateWebIntake,
        onSuccess: (web_intake) => {
            refreshSettings({ web_intake });
            setWebIntakeForm(null);
            toast.success(t('settings.webIntakeSaved'));
        },
        onError: (err: unknown) => toast.error(getAdminAccessErrorMessage(err, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.webIntakeSaveFailed'),
        })),
    });

    if (isLoading) {
        return <QueryLoadingState message={t('common.loadingRuntimeSettings')} />;
    }

    if (isError || !settings) {
        const message = getAdminAccessErrorMessage(error, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.failedLoad'),
        });
        return (
            <QueryErrorState
                className="max-w-2xl"
                message={message}
                onRetry={() => { void refetch(); }}
                title={t('settings.runtimeConfig')}
            />
        );
    }

    const effectiveAppForm: AppForm = appForm ?? {
        ai_language_mode: settings.app.ai_language_mode,
    };
    const effectiveLlmForm: LLMForm = llmForm ?? {
        provider: settings.llm.provider,
        api_url: settings.llm.api_url,
        model: settings.llm.model,
        temperature: settings.llm.temperature,
        max_output_tokens: settings.llm.max_output_tokens,
        api_key: '',
        clear_api_key: false,
    };
    const effectiveGithubForm: GitHubForm = githubForm ?? {
        api_url: settings.github.api_url,
        token: '',
        clear_token: false,
        request_timeout_seconds: settings.github.request_timeout_seconds,
        webhook_secret: '',
        clear_webhook_secret: false,
        webhook_create_triage_for_unmatched: settings.github.webhook_create_triage_for_unmatched,
    };
    const effectiveWebIntakeForm: WebIntakeForm = webIntakeForm ?? {
        token: '',
        clear_token: false,
        rate_limit_per_minute: settings.web_intake.rate_limit_per_minute,
    };

    const saveApp = () => {
        const payload: AppRuntimeSettingsUpdate = {
            ui_language: settings.app.ui_language,
            ai_language_mode: effectiveAppForm.ai_language_mode,
        };
        appMutation.mutate(payload);
    };

    const saveLLM = () => {
        const payload: LLMRuntimeSettingsUpdate = {
            provider: effectiveLlmForm.provider,
            api_url: effectiveLlmForm.api_url,
            model: effectiveLlmForm.model,
            temperature: effectiveLlmForm.temperature,
            max_output_tokens: effectiveLlmForm.max_output_tokens,
            clear_api_key: effectiveLlmForm.clear_api_key,
        };
        if (effectiveLlmForm.api_key.trim()) payload.api_key = effectiveLlmForm.api_key.trim();
        llmMutation.mutate(payload);
    };

    const saveGitHub = () => {
        const payload: GitHubRuntimeSettingsUpdate = {
            api_url: effectiveGithubForm.api_url,
            request_timeout_seconds: effectiveGithubForm.request_timeout_seconds,
            webhook_create_triage_for_unmatched: effectiveGithubForm.webhook_create_triage_for_unmatched,
            clear_token: effectiveGithubForm.clear_token,
            clear_webhook_secret: effectiveGithubForm.clear_webhook_secret,
        };
        if (effectiveGithubForm.token.trim()) payload.token = effectiveGithubForm.token.trim();
        if (effectiveGithubForm.webhook_secret.trim()) payload.webhook_secret = effectiveGithubForm.webhook_secret.trim();
        githubMutation.mutate(payload);
    };

    const saveWebIntake = () => {
        const payload: WebIntakeRuntimeSettingsUpdate = {
            rate_limit_per_minute: effectiveWebIntakeForm.rate_limit_per_minute,
            clear_token: effectiveWebIntakeForm.clear_token,
        };
        if (effectiveWebIntakeForm.token.trim()) payload.token = effectiveWebIntakeForm.token.trim();
        webIntakeMutation.mutate(payload);
    };

    return (
        <div className="max-w-6xl space-y-5">
            <div className="grid grid-cols-1 gap-5 xl:grid-cols-4">
                <fieldset
                    aria-labelledby="runtime-ai-language-heading"
                    className="card space-y-4"
                    disabled={appMutation.isPending}
                >
                    <div>
                        <h2 id="runtime-ai-language-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <Globe2 className="h-5 w-5 text-feedback-success" />
                            {t('settings.aiOutputLanguage')}
                        </h2>
                        <p className="text-sm text-content-secondary">{t('settings.aiOutputLanguageDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex items-center justify-between">
                                <label htmlFor="ai-language-mode" className="text-sm font-medium text-content-primary">{t('settings.aiLanguageMode')}</label>
                                <SourceBadge source={fieldSource(settings.app, 'ai_language_mode')} />
                            </div>
                            <select
                                id="ai-language-mode"
                                value={effectiveAppForm.ai_language_mode}
                                onChange={event => setAppForm({ ...effectiveAppForm, ai_language_mode: event.target.value as AILanguageMode })}
                                className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                <option value="auto">{t('common.language.auto')}</option>
                                <option value="en">{t('common.language.en')}</option>
                                <option value="ru">{t('common.language.ru')}</option>
                            </select>
                            <p className="mt-1 text-xs text-content-secondary">{t('settings.aiLanguageHelp')}</p>
                        </div>
                    </div>
                    <Button onClick={saveApp} isLoading={appMutation.isPending}>
                        <Save className="mr-2 h-4 w-4" />
                        {t('settings.saveAiLanguage')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-llm-heading"
                    className="card space-y-4"
                    disabled={llmMutation.isPending}
                >
                    <div className="flex items-start justify-between gap-3">
                        <div>
                            <h2 id="runtime-llm-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                                <ServerCog className="h-5 w-5 text-action" />
                                {t('settings.llmProvider')}
                            </h2>
                            <p className="text-sm text-content-secondary">{t('settings.llmProviderDescription')}</p>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex items-center justify-between">
                                <label className="text-sm font-medium text-content-primary">{t('settings.provider')}</label>
                                <SourceBadge source={fieldSource(settings.llm, 'provider')} />
                            </div>
                            <select
                                value={effectiveLlmForm.provider}
                                onChange={event => setLlmForm({ ...effectiveLlmForm, provider: event.target.value as LLMProvider })}
                                className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                <option value="openai">{t('surfaces.runtimeConfig.openai')}</option>
                                <option value="openrouter">{t('surfaces.runtimeConfig.openrouter')}</option>
                                <option value="nvidia">NVIDIA</option>
                                <option value="custom">{t('surfaces.runtimeConfig.custom')}</option>
                            </select>
                        </div>
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'model')} /></div>
                            <Input label={t('settings.model')} value={effectiveLlmForm.model} onChange={event => setLlmForm({ ...effectiveLlmForm, model: event.target.value })} />
                        </div>
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'api_url')} /></div>
                            <Input label={t('settings.apiUrlOverride')} value={effectiveLlmForm.api_url} onChange={event => setLlmForm({ ...effectiveLlmForm, api_url: event.target.value })} placeholder={t('settings.apiUrlPlaceholder')} />
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'temperature')} /></div>
                                <Input
                                    label={t('settings.temperature')}
                                    type="number"
                                    min="0"
                                    max="2"
                                    step="0.1"
                                    value={effectiveLlmForm.temperature}
                                    onChange={event => setLlmForm({ ...effectiveLlmForm, temperature: Number(event.target.value) })}
                                />
                            </div>
                            <div>
                                <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'max_output_tokens')} /></div>
                                <Input
                                    label={t('settings.maxOutputTokens')}
                                    type="number"
                                    min="256"
                                    max="12000"
                                    step="100"
                                    value={effectiveLlmForm.max_output_tokens}
                                    onChange={event => setLlmForm({ ...effectiveLlmForm, max_output_tokens: Number(event.target.value) || 3000 })}
                                />
                            </div>
                        </div>
                        <SecretState configured={settings.llm.has_api_key} source={fieldSource(settings.llm, 'api_key')} />
                        <Input type="password" label={t('settings.replaceApiKey')} value={effectiveLlmForm.api_key} onChange={event => setLlmForm({ ...effectiveLlmForm, api_key: event.target.value })} placeholder={t('settings.keepCurrentKey')} />
                        <Checkbox label={t('settings.clearRuntimeApiKey')} checked={effectiveLlmForm.clear_api_key} onChange={checked => setLlmForm({ ...effectiveLlmForm, clear_api_key: checked })} />
                    </div>
                    <Button onClick={saveLLM} isLoading={llmMutation.isPending}>
                        <Save className="mr-2 h-4 w-4" />
                        {t('settings.saveLLM')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-github-heading"
                    className="card space-y-4"
                    disabled={githubMutation.isPending}
                >
                    <div>
                        <h2 id="runtime-github-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <ServerCog className="h-5 w-5 text-content-primary" />
                            {t('settings.github')}
                        </h2>
                        <p className="text-sm text-content-secondary">{t('settings.githubDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.github, 'api_url')} /></div>
                            <Input label={t('settings.githubApiUrl')} value={effectiveGithubForm.api_url} onChange={event => setGithubForm({ ...effectiveGithubForm, api_url: event.target.value })} />
                        </div>
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.github, 'request_timeout_seconds')} /></div>
                            <Input label={t('settings.requestTimeout')} type="number" value={effectiveGithubForm.request_timeout_seconds} onChange={event => setGithubForm({ ...effectiveGithubForm, request_timeout_seconds: Number(event.target.value) || 1 })} />
                        </div>
                        <SecretState configured={settings.github.has_token} source={fieldSource(settings.github, 'token')} />
                        <Input type="password" label={t('settings.replaceGitHubToken')} value={effectiveGithubForm.token} onChange={event => setGithubForm({ ...effectiveGithubForm, token: event.target.value })} placeholder={t('settings.keepCurrentKey')} />
                        <Checkbox label={t('settings.clearRuntimeToken')} checked={effectiveGithubForm.clear_token} onChange={checked => setGithubForm({ ...effectiveGithubForm, clear_token: checked })} />
                        <SecretState configured={settings.github.has_webhook_secret} source={fieldSource(settings.github, 'webhook_secret')} />
                        <Input type="password" label={t('settings.replaceWebhookSecret')} value={effectiveGithubForm.webhook_secret} onChange={event => setGithubForm({ ...effectiveGithubForm, webhook_secret: event.target.value })} placeholder={t('settings.keepCurrentSecret')} />
                        <Checkbox label={t('settings.clearWebhookSecret')} checked={effectiveGithubForm.clear_webhook_secret} onChange={checked => setGithubForm({ ...effectiveGithubForm, clear_webhook_secret: checked })} />
                        <Checkbox label={t('settings.unmatchedPrTriage')} checked={effectiveGithubForm.webhook_create_triage_for_unmatched} onChange={checked => setGithubForm({ ...effectiveGithubForm, webhook_create_triage_for_unmatched: checked })} />
                    </div>
                    <Button onClick={saveGitHub} isLoading={githubMutation.isPending}>
                        <Save className="mr-2 h-4 w-4" />
                        {t('settings.saveGitHub')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-web-intake-heading"
                    className="card space-y-4"
                    disabled={webIntakeMutation.isPending}
                >
                    <div>
                        <h2 id="runtime-web-intake-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <ShieldAlert className="h-5 w-5 text-feedback-warning" />
                            {t('settings.webIntake')}
                        </h2>
                        <p className="text-sm text-content-secondary">{t('settings.webIntakeDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <SecretState configured={settings.web_intake.has_token} source={fieldSource(settings.web_intake, 'token')} />
                        <Input type="password" label={t('settings.replaceIntakeToken')} value={effectiveWebIntakeForm.token} onChange={event => setWebIntakeForm({ ...effectiveWebIntakeForm, token: event.target.value })} placeholder={t('settings.keepCurrentKey')} />
                        <Checkbox label={t('settings.clearRuntimeToken')} checked={effectiveWebIntakeForm.clear_token} onChange={checked => setWebIntakeForm({ ...effectiveWebIntakeForm, clear_token: checked })} />
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.web_intake, 'rate_limit_per_minute')} /></div>
                            <Input label={t('settings.rateLimitPerMinute')} type="number" value={effectiveWebIntakeForm.rate_limit_per_minute} onChange={event => setWebIntakeForm({ ...effectiveWebIntakeForm, rate_limit_per_minute: Number(event.target.value) || 1 })} />
                        </div>
                    </div>
                    <Button onClick={saveWebIntake} isLoading={webIntakeMutation.isPending}>
                        <Save className="mr-2 h-4 w-4" />
                        {t('settings.saveWebIntake')}
                    </Button>
                </fieldset>
            </div>

            <section className="card space-y-3">
                <h2 className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                    <RefreshCcw className="h-5 w-5 text-content-secondary" />
                    {t('settings.restartRequired')}
                </h2>
                <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
                    {settings.restart_required.length === 0 && (
                        <QueryEmptyState className="md:col-span-2" title={t('queryFeedback.emptyTitle')} />
                    )}
                    {settings.restart_required.map(item => (
                        <div key={item.key} className="rounded-md border border-border bg-surface-muted px-3 py-2">
                            <div className="font-mono text-sm font-semibold text-content-primary">{item.key}</div>
                            <div className="text-sm text-content-secondary">{item.description}</div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};
