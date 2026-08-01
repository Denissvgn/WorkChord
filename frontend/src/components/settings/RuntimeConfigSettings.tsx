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
    temperature: string;
    max_output_tokens: string;
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
    request_timeout_seconds: string;
    webhook_secret: string;
    clear_webhook_secret: boolean;
    webhook_create_triage_for_unmatched: boolean;
}

interface WebIntakeForm {
    token: string;
    clear_token: boolean;
    rate_limit_per_minute: string;
}

type RuntimeSection = 'llm' | 'github' | 'webIntake';
type RuntimeErrors = Record<string, string>;

const parseFiniteNumber = (value: string) => {
    const trimmed = value.trim();
    if (!trimmed) return null;
    const parsed = Number(trimmed);
    return Number.isFinite(parsed) ? parsed : null;
};

const parseInteger = (value: string) => {
    const parsed = parseFiniteNumber(value);
    return parsed !== null && Number.isInteger(parsed) ? parsed : null;
};

const isHttpUrl = (value: string) => {
    try {
        const url = new URL(value.trim());
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch {
        return false;
    }
};

const DEFAULT_LLM_ENDPOINTS: Partial<Record<LLMProvider, string>> = {
    openai: 'https://api.openai.com',
    openrouter: 'https://openrouter.ai',
    nvidia: 'https://integrate.api.nvidia.com',
};

const endpointOrigin = (value: string) => {
    try {
        return value.trim() ? new URL(value.trim()).origin : null;
    } catch {
        return null;
    }
};

const llmCredentialDestination = (provider: LLMProvider, apiUrl: string) => {
    const resolvedEndpoint = apiUrl.trim() || DEFAULT_LLM_ENDPOINTS[provider] || '';
    return `${provider}:${endpointOrigin(resolvedEndpoint) ?? 'unresolved'}`;
};

const hasLlmCredentialDestinationChanged = (
    currentProvider: LLMProvider,
    currentUrl: string,
    nextProvider: LLMProvider,
    nextUrl: string,
) => (
    llmCredentialDestination(currentProvider, currentUrl)
    !== llmCredentialDestination(nextProvider, nextUrl)
);

const hasEndpointOriginChanged = (currentUrl: string, nextUrl: string) => (
    endpointOrigin(currentUrl) !== endpointOrigin(nextUrl)
);

const hasNumberChanged = (value: string, current: number) => {
    const parsed = parseFiniteNumber(value);
    return parsed === null || parsed !== current;
};

const sourceClass: Record<RuntimeSettingSource, string> = {
    runtime: 'bg-action-muted text-action border-action',
    environment: 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border',
    default: 'bg-surface-muted text-content-secondary border-border',
};

const SourceBadge = ({ source }: { source?: RuntimeSettingSource }) => {
    const { t } = useTranslation();
    if (!source) return null;
    return (
        <span className={`inline-flex max-w-full items-center break-words rounded-full border px-2 py-0.5 text-center text-xs font-medium ${sourceClass[source]}`}>
            {t(`common.${source}`)}
        </span>
    );
};

const SecretState = ({ configured, source }: { configured: boolean; source?: RuntimeSettingSource }) => {
    const { t } = useTranslation();
    return (
        <div className="flex min-w-0 flex-wrap items-center gap-2 text-sm text-content-secondary">
            <KeyRound aria-hidden="true" className="h-4 w-4" />
            <span className="break-words">{configured ? t('common.configured') : t('common.notConfigured')}</span>
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
    const [formErrors, setFormErrors] = useState<RuntimeErrors>({});
    const [submissionErrors, setSubmissionErrors] = useState<Partial<Record<RuntimeSection, string>>>({});

    const runtimeText = (
        key: string,
        defaultValue: string,
        values: Record<string, string | number> = {},
    ) => t(`settings.${key}`, { defaultValue, ...values });

    const clearFieldError = (field: string, section: RuntimeSection) => {
        setFormErrors(current => {
            if (!current[field]) return current;
            const next = { ...current };
            delete next[field];
            return next;
        });
        setSubmissionErrors(current => {
            if (!current[section]) return current;
            const next = { ...current };
            delete next[section];
            return next;
        });
    };

    const setSectionValidationErrors = (prefix: string, errors: RuntimeErrors, section: RuntimeSection) => {
        setFormErrors(current => {
            const next = Object.fromEntries(
                Object.entries(current).filter(([field]) => !field.startsWith(prefix)),
            ) as RuntimeErrors;
            return { ...next, ...errors };
        });
        setSubmissionErrors(current => {
            if (!current[section]) return current;
            const next = { ...current };
            delete next[section];
            return next;
        });
    };

    const clearSectionErrors = (prefix: string, section: RuntimeSection) => {
        setFormErrors(current => Object.fromEntries(
            Object.entries(current).filter(([field]) => !field.startsWith(prefix)),
        ) as RuntimeErrors);
        setSubmissionErrors(current => {
            if (!current[section]) return current;
            const next = { ...current };
            delete next[section];
            return next;
        });
    };

    const reportMutationError = (section: RuntimeSection, err: unknown, fallback: string) => {
        const message = getAdminAccessErrorMessage(err, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback,
        });
        setSubmissionErrors(current => ({ ...current, [section]: message }));
        toast.error(message);
    };

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
            clearSectionErrors('llm.', 'llm');
            toast.success(t('settings.llmSaved'));
        },
        onError: (err: unknown) => reportMutationError('llm', err, t('settings.llmSaveFailed')),
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
            clearSectionErrors('github.', 'github');
            toast.success(t('settings.githubSaved'));
        },
        onError: (err: unknown) => reportMutationError('github', err, t('settings.githubSaveFailed')),
    });

    const webIntakeMutation = useMutation({
        mutationFn: systemSettingsService.updateWebIntake,
        onSuccess: (web_intake) => {
            refreshSettings({ web_intake });
            setWebIntakeForm(null);
            clearSectionErrors('web_intake.', 'webIntake');
            toast.success(t('settings.webIntakeSaved'));
        },
        onError: (err: unknown) => reportMutationError('webIntake', err, t('settings.webIntakeSaveFailed')),
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
        temperature: String(settings.llm.temperature),
        max_output_tokens: String(settings.llm.max_output_tokens),
        api_key: '',
        clear_api_key: false,
    };
    const effectiveGithubForm: GitHubForm = githubForm ?? {
        api_url: settings.github.api_url,
        token: '',
        clear_token: false,
        request_timeout_seconds: String(settings.github.request_timeout_seconds),
        webhook_secret: '',
        clear_webhook_secret: false,
        webhook_create_triage_for_unmatched: settings.github.webhook_create_triage_for_unmatched,
    };
    const effectiveWebIntakeForm: WebIntakeForm = webIntakeForm ?? {
        token: '',
        clear_token: false,
        rate_limit_per_minute: String(settings.web_intake.rate_limit_per_minute),
    };

    const isAppChanged = effectiveAppForm.ai_language_mode !== settings.app.ai_language_mode;
    const isLlmChanged = (
        effectiveLlmForm.provider !== settings.llm.provider
        || effectiveLlmForm.api_url.trim() !== settings.llm.api_url.trim()
        || effectiveLlmForm.model.trim() !== settings.llm.model.trim()
        || hasNumberChanged(effectiveLlmForm.temperature, settings.llm.temperature)
        || hasNumberChanged(effectiveLlmForm.max_output_tokens, settings.llm.max_output_tokens)
        || Boolean(effectiveLlmForm.api_key.trim())
        || effectiveLlmForm.clear_api_key
    );
    const isGitHubChanged = (
        effectiveGithubForm.api_url.trim() !== settings.github.api_url.trim()
        || hasNumberChanged(effectiveGithubForm.request_timeout_seconds, settings.github.request_timeout_seconds)
        || effectiveGithubForm.webhook_create_triage_for_unmatched !== settings.github.webhook_create_triage_for_unmatched
        || Boolean(effectiveGithubForm.token.trim())
        || effectiveGithubForm.clear_token
        || Boolean(effectiveGithubForm.webhook_secret.trim())
        || effectiveGithubForm.clear_webhook_secret
    );
    const isWebIntakeChanged = (
        hasNumberChanged(effectiveWebIntakeForm.rate_limit_per_minute, settings.web_intake.rate_limit_per_minute)
        || Boolean(effectiveWebIntakeForm.token.trim())
        || effectiveWebIntakeForm.clear_token
    );

    const validateLlm = () => {
        const errors: RuntimeErrors = {};
        const model = effectiveLlmForm.model.trim();
        const apiUrl = effectiveLlmForm.api_url.trim();
        const temperature = parseFiniteNumber(effectiveLlmForm.temperature);
        const maxOutputTokens = parseInteger(effectiveLlmForm.max_output_tokens);

        if (!model) {
            errors['llm.model'] = runtimeText('runtimeModelRequired', 'Enter a model name.');
        }
        if (effectiveLlmForm.provider === 'custom' && !apiUrl) {
            errors['llm.api_url'] = runtimeText('runtimeCustomApiUrlRequired', 'Enter an API URL for a custom provider.');
        } else if (apiUrl && !isHttpUrl(apiUrl)) {
            errors['llm.api_url'] = runtimeText('runtimeApiUrlInvalid', 'Enter a valid http:// or https:// URL.');
        }
        if (temperature === null || temperature < 0 || temperature > 2) {
            errors['llm.temperature'] = runtimeText('runtimeNumberRange', 'Enter a number from {{min}} to {{max}}.', { min: 0, max: 2 });
        }
        if (maxOutputTokens === null || maxOutputTokens < 256 || maxOutputTokens > 12000) {
            errors['llm.max_output_tokens'] = runtimeText('runtimeWholeNumberRange', 'Enter a whole number from {{min}} to {{max}}.', { min: 256, max: 12000 });
        }
        if (
            settings.llm.has_api_key
            && hasLlmCredentialDestinationChanged(
                settings.llm.provider,
                settings.llm.api_url,
                effectiveLlmForm.provider,
                apiUrl,
            )
            && !effectiveLlmForm.api_key.trim()
            && !effectiveLlmForm.clear_api_key
        ) {
            errors['llm.api_key'] = runtimeText(
                'runtimeEndpointSecretRequired',
                'The credential destination changed. Replace or clear the current credential before saving.',
            );
        }

        setSectionValidationErrors('llm.', errors, 'llm');
        if (Object.keys(errors).length > 0) return null;
        return {
            apiUrl,
            model,
            temperature: temperature as number,
            maxOutputTokens: maxOutputTokens as number,
        };
    };

    const validateGitHub = () => {
        const errors: RuntimeErrors = {};
        const apiUrl = effectiveGithubForm.api_url.trim();
        const timeout = parseFiniteNumber(effectiveGithubForm.request_timeout_seconds);

        if (!apiUrl) {
            errors['github.api_url'] = runtimeText('runtimeGitHubApiUrlRequired', 'Enter a GitHub API URL.');
        } else if (!isHttpUrl(apiUrl)) {
            errors['github.api_url'] = runtimeText('runtimeApiUrlInvalid', 'Enter a valid http:// or https:// URL.');
        }
        if (timeout === null || timeout <= 0 || timeout > 120) {
            errors['github.request_timeout_seconds'] = runtimeText('runtimeGreaterThanZeroUpTo', 'Enter a number greater than 0 and up to {{max}}.', { max: 120 });
        }
        if (
            settings.github.has_token
            && hasEndpointOriginChanged(settings.github.api_url, apiUrl)
            && !effectiveGithubForm.token.trim()
            && !effectiveGithubForm.clear_token
        ) {
            errors['github.token'] = runtimeText(
                'runtimeEndpointSecretRequired',
                'The credential destination changed. Replace or clear the current credential before saving.',
            );
        }

        setSectionValidationErrors('github.', errors, 'github');
        if (Object.keys(errors).length > 0) return null;
        return { apiUrl, timeout: timeout as number };
    };

    const validateWebIntake = () => {
        const errors: RuntimeErrors = {};
        const rateLimit = parseInteger(effectiveWebIntakeForm.rate_limit_per_minute);
        if (rateLimit === null || rateLimit < 1 || rateLimit > 10000) {
            errors['web_intake.rate_limit_per_minute'] = runtimeText('runtimeWholeNumberRange', 'Enter a whole number from {{min}} to {{max}}.', { min: 1, max: 10000 });
        }

        setSectionValidationErrors('web_intake.', errors, 'webIntake');
        if (Object.keys(errors).length > 0) return null;
        return { rateLimit: rateLimit as number };
    };

    const saveApp = () => {
        if (!isAppChanged) return;
        const payload: AppRuntimeSettingsUpdate = {
            ui_language: settings.app.ui_language,
            ai_language_mode: effectiveAppForm.ai_language_mode,
        };
        appMutation.mutate(payload);
    };

    const saveLLM = () => {
        if (!isLlmChanged) return;
        const validated = validateLlm();
        if (!validated) return;
        const payload: LLMRuntimeSettingsUpdate = {
            provider: effectiveLlmForm.provider,
            api_url: validated.apiUrl,
            model: validated.model,
            temperature: validated.temperature,
            max_output_tokens: validated.maxOutputTokens,
            clear_api_key: effectiveLlmForm.clear_api_key,
        };
        if (effectiveLlmForm.api_key.trim()) payload.api_key = effectiveLlmForm.api_key.trim();
        llmMutation.mutate(payload);
    };

    const saveGitHub = () => {
        if (!isGitHubChanged) return;
        const validated = validateGitHub();
        if (!validated) return;
        const payload: GitHubRuntimeSettingsUpdate = {
            api_url: validated.apiUrl,
            request_timeout_seconds: validated.timeout,
            webhook_create_triage_for_unmatched: effectiveGithubForm.webhook_create_triage_for_unmatched,
            clear_token: effectiveGithubForm.clear_token,
            clear_webhook_secret: effectiveGithubForm.clear_webhook_secret,
        };
        if (effectiveGithubForm.token.trim()) payload.token = effectiveGithubForm.token.trim();
        if (effectiveGithubForm.webhook_secret.trim()) payload.webhook_secret = effectiveGithubForm.webhook_secret.trim();
        githubMutation.mutate(payload);
    };

    const saveWebIntake = () => {
        if (!isWebIntakeChanged) return;
        const validated = validateWebIntake();
        if (!validated) return;
        const payload: WebIntakeRuntimeSettingsUpdate = {
            rate_limit_per_minute: validated.rateLimit,
            clear_token: effectiveWebIntakeForm.clear_token,
        };
        if (effectiveWebIntakeForm.token.trim()) payload.token = effectiveWebIntakeForm.token.trim();
        webIntakeMutation.mutate(payload);
    };

    const errorMessages = [
        ...Object.entries(formErrors),
        ...Object.entries(submissionErrors),
    ];

    return (
        <div className="max-w-6xl space-y-5">
            {errorMessages.length > 0 && (
                <section
                    aria-label={runtimeText('runtimeValidationSummary', 'Review the highlighted fields before saving.')}
                    aria-live="assertive"
                    className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground"
                    role="alert"
                >
                    <p className="font-medium">{runtimeText('runtimeValidationSummary', 'Review the highlighted fields before saving.')}</p>
                    <ul className="mt-2 list-disc space-y-1 break-words pl-5">
                        {errorMessages.map(([field, message]) => <li key={field}>{message}</li>)}
                    </ul>
                </section>
            )}
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2 2xl:grid-cols-4">
                <fieldset
                    aria-labelledby="runtime-ai-language-heading"
                    className="card min-w-0 space-y-4"
                    disabled={appMutation.isPending}
                >
                    <div className="min-w-0">
                        <h2 id="runtime-ai-language-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <Globe2 aria-hidden="true" className="h-5 w-5 text-feedback-success" />
                            {t('settings.aiOutputLanguage')}
                        </h2>
                        <p className="break-words text-sm text-content-secondary">{t('settings.aiOutputLanguageDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex min-w-0 items-center justify-between gap-2">
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
                    <Button className="w-full sm:w-auto" disabled={!isAppChanged || appMutation.isPending} onClick={saveApp} isLoading={appMutation.isPending}>
                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('settings.saveAiLanguage')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-llm-heading"
                    className="card min-w-0 space-y-4"
                    disabled={llmMutation.isPending}
                >
                    <div className="flex items-start justify-between gap-3">
                        <div className="min-w-0">
                            <h2 id="runtime-llm-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                                <ServerCog aria-hidden="true" className="h-5 w-5 text-action" />
                                {t('settings.llmProvider')}
                            </h2>
                            <p className="break-words text-sm text-content-secondary">{t('settings.llmProviderDescription')}</p>
                        </div>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex min-w-0 items-center justify-between gap-2">
                                <label htmlFor="runtime-llm-provider" className="text-sm font-medium text-content-primary">{t('settings.provider')}</label>
                                <SourceBadge source={fieldSource(settings.llm, 'provider')} />
                            </div>
                            <select
                                id="runtime-llm-provider"
                                value={effectiveLlmForm.provider}
                                onChange={event => {
                                    setLlmForm({ ...effectiveLlmForm, provider: event.target.value as LLMProvider });
                                    clearFieldError('llm.api_url', 'llm');
                                }}
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
                            <Input
                                error={formErrors['llm.model']}
                                label={t('settings.model')}
                                required
                                value={effectiveLlmForm.model}
                                onChange={event => {
                                    setLlmForm({ ...effectiveLlmForm, model: event.target.value });
                                    clearFieldError('llm.model', 'llm');
                                }}
                            />
                        </div>
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'api_url')} /></div>
                            <Input
                                error={formErrors['llm.api_url']}
                                label={t('settings.apiUrlOverride')}
                                placeholder={t('settings.apiUrlPlaceholder')}
                                type="url"
                                value={effectiveLlmForm.api_url}
                                onChange={event => {
                                    setLlmForm({ ...effectiveLlmForm, api_url: event.target.value });
                                    clearFieldError('llm.api_url', 'llm');
                                    clearFieldError('llm.api_key', 'llm');
                                }}
                            />
                        </div>
                        <div className="grid min-w-0 grid-cols-1 gap-3 sm:grid-cols-2">
                            <div>
                                <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'temperature')} /></div>
                                <Input
                                    error={formErrors['llm.temperature']}
                                    label={t('settings.temperature')}
                                    type="number"
                                    min="0"
                                    max="2"
                                    step="0.1"
                                    value={effectiveLlmForm.temperature}
                                    onChange={event => {
                                        setLlmForm({ ...effectiveLlmForm, temperature: event.target.value });
                                        clearFieldError('llm.temperature', 'llm');
                                    }}
                                />
                            </div>
                            <div>
                                <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.llm, 'max_output_tokens')} /></div>
                                <Input
                                    error={formErrors['llm.max_output_tokens']}
                                    label={t('settings.maxOutputTokens')}
                                    type="number"
                                    min="256"
                                    max="12000"
                                    step="100"
                                    value={effectiveLlmForm.max_output_tokens}
                                    onChange={event => {
                                        setLlmForm({ ...effectiveLlmForm, max_output_tokens: event.target.value });
                                        clearFieldError('llm.max_output_tokens', 'llm');
                                    }}
                                />
                            </div>
                        </div>
                        <SecretState configured={settings.llm.has_api_key} source={fieldSource(settings.llm, 'api_key')} />
                        <Input
                            disabled={effectiveLlmForm.clear_api_key}
                            error={formErrors['llm.api_key']}
                            label={t('settings.replaceApiKey')}
                            placeholder={t('settings.keepCurrentKey')}
                            type="password"
                            value={effectiveLlmForm.api_key}
                            onChange={event => {
                                const apiKey = event.target.value;
                                setLlmForm({ ...effectiveLlmForm, api_key: apiKey, clear_api_key: apiKey ? false : effectiveLlmForm.clear_api_key });
                                clearFieldError('llm.api_key', 'llm');
                            }}
                        />
                        <Checkbox
                            checked={effectiveLlmForm.clear_api_key}
                            label={t('settings.clearRuntimeApiKey')}
                            onChange={checked => {
                                setLlmForm({ ...effectiveLlmForm, api_key: checked ? '' : effectiveLlmForm.api_key, clear_api_key: checked });
                                clearFieldError('llm.api_key', 'llm');
                            }}
                        />
                    </div>
                    <Button className="w-full sm:w-auto" disabled={!isLlmChanged || llmMutation.isPending} onClick={saveLLM} isLoading={llmMutation.isPending}>
                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('settings.saveLLM')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-github-heading"
                    className="card min-w-0 space-y-4"
                    disabled={githubMutation.isPending}
                >
                    <div className="min-w-0">
                        <h2 id="runtime-github-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <ServerCog aria-hidden="true" className="h-5 w-5 text-content-primary" />
                            {t('settings.github')}
                        </h2>
                        <p className="break-words text-sm text-content-secondary">{t('settings.githubDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.github, 'api_url')} /></div>
                            <Input
                                error={formErrors['github.api_url']}
                                label={t('settings.githubApiUrl')}
                                required
                                type="url"
                                value={effectiveGithubForm.api_url}
                                onChange={event => {
                                    setGithubForm({ ...effectiveGithubForm, api_url: event.target.value });
                                    clearFieldError('github.api_url', 'github');
                                    clearFieldError('github.token', 'github');
                                }}
                            />
                        </div>
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.github, 'request_timeout_seconds')} /></div>
                            <Input
                                error={formErrors['github.request_timeout_seconds']}
                                label={t('settings.requestTimeout')}
                                type="number"
                                min="0.1"
                                max="120"
                                step="0.1"
                                value={effectiveGithubForm.request_timeout_seconds}
                                onChange={event => {
                                    setGithubForm({ ...effectiveGithubForm, request_timeout_seconds: event.target.value });
                                    clearFieldError('github.request_timeout_seconds', 'github');
                                }}
                            />
                        </div>
                        <SecretState configured={settings.github.has_token} source={fieldSource(settings.github, 'token')} />
                        <Input
                            disabled={effectiveGithubForm.clear_token}
                            error={formErrors['github.token']}
                            label={t('settings.replaceGitHubToken')}
                            placeholder={t('settings.keepCurrentKey')}
                            type="password"
                            value={effectiveGithubForm.token}
                            onChange={event => {
                                const token = event.target.value;
                                setGithubForm({ ...effectiveGithubForm, token, clear_token: token ? false : effectiveGithubForm.clear_token });
                                clearFieldError('github.token', 'github');
                            }}
                        />
                        <Checkbox
                            checked={effectiveGithubForm.clear_token}
                            label={t('settings.clearRuntimeToken')}
                            onChange={checked => {
                                setGithubForm({ ...effectiveGithubForm, token: checked ? '' : effectiveGithubForm.token, clear_token: checked });
                                clearFieldError('github.token', 'github');
                            }}
                        />
                        <SecretState configured={settings.github.has_webhook_secret} source={fieldSource(settings.github, 'webhook_secret')} />
                        <Input
                            disabled={effectiveGithubForm.clear_webhook_secret}
                            label={t('settings.replaceWebhookSecret')}
                            placeholder={t('settings.keepCurrentSecret')}
                            type="password"
                            value={effectiveGithubForm.webhook_secret}
                            onChange={event => {
                                const webhookSecret = event.target.value;
                                setGithubForm({ ...effectiveGithubForm, webhook_secret: webhookSecret, clear_webhook_secret: webhookSecret ? false : effectiveGithubForm.clear_webhook_secret });
                                clearFieldError('github.webhook_secret', 'github');
                            }}
                        />
                        <Checkbox
                            checked={effectiveGithubForm.clear_webhook_secret}
                            label={t('settings.clearWebhookSecret')}
                            onChange={checked => {
                                setGithubForm({ ...effectiveGithubForm, webhook_secret: checked ? '' : effectiveGithubForm.webhook_secret, clear_webhook_secret: checked });
                                clearFieldError('github.webhook_secret', 'github');
                            }}
                        />
                        <Checkbox
                            checked={effectiveGithubForm.webhook_create_triage_for_unmatched}
                            label={t('settings.unmatchedPrTriage')}
                            onChange={checked => {
                                setGithubForm({ ...effectiveGithubForm, webhook_create_triage_for_unmatched: checked });
                                clearFieldError('github.webhook_create_triage_for_unmatched', 'github');
                            }}
                        />
                    </div>
                    <Button className="w-full sm:w-auto" disabled={!isGitHubChanged || githubMutation.isPending} onClick={saveGitHub} isLoading={githubMutation.isPending}>
                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('settings.saveGitHub')}
                    </Button>
                </fieldset>

                <fieldset
                    aria-labelledby="runtime-web-intake-heading"
                    className="card min-w-0 space-y-4"
                    disabled={webIntakeMutation.isPending}
                >
                    <div className="min-w-0">
                        <h2 id="runtime-web-intake-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <ShieldAlert aria-hidden="true" className="h-5 w-5 text-feedback-warning" />
                            {t('settings.webIntake')}
                        </h2>
                        <p className="break-words text-sm text-content-secondary">{t('settings.webIntakeDescription')}</p>
                    </div>
                    <div className="space-y-3">
                        <SecretState configured={settings.web_intake.has_token} source={fieldSource(settings.web_intake, 'token')} />
                        <Input
                            disabled={effectiveWebIntakeForm.clear_token}
                            label={t('settings.replaceIntakeToken')}
                            placeholder={t('settings.keepCurrentKey')}
                            type="password"
                            value={effectiveWebIntakeForm.token}
                            onChange={event => {
                                const token = event.target.value;
                                setWebIntakeForm({ ...effectiveWebIntakeForm, token, clear_token: token ? false : effectiveWebIntakeForm.clear_token });
                                clearFieldError('web_intake.token', 'webIntake');
                            }}
                        />
                        <Checkbox
                            checked={effectiveWebIntakeForm.clear_token}
                            label={t('settings.clearRuntimeIntakeToken')}
                            onChange={checked => {
                                setWebIntakeForm({ ...effectiveWebIntakeForm, token: checked ? '' : effectiveWebIntakeForm.token, clear_token: checked });
                                clearFieldError('web_intake.token', 'webIntake');
                            }}
                        />
                        <div>
                            <div className="mb-1 flex justify-end"><SourceBadge source={fieldSource(settings.web_intake, 'rate_limit_per_minute')} /></div>
                            <Input
                                error={formErrors['web_intake.rate_limit_per_minute']}
                                label={t('settings.rateLimitPerMinute')}
                                type="number"
                                min="1"
                                max="10000"
                                step="1"
                                value={effectiveWebIntakeForm.rate_limit_per_minute}
                                onChange={event => {
                                    setWebIntakeForm({ ...effectiveWebIntakeForm, rate_limit_per_minute: event.target.value });
                                    clearFieldError('web_intake.rate_limit_per_minute', 'webIntake');
                                }}
                            />
                        </div>
                    </div>
                    <Button className="w-full sm:w-auto" disabled={!isWebIntakeChanged || webIntakeMutation.isPending} onClick={saveWebIntake} isLoading={webIntakeMutation.isPending}>
                        <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('settings.saveWebIntake')}
                    </Button>
                </fieldset>
            </div>

            <section className="card min-w-0 space-y-3">
                <h2 className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                    <RefreshCcw aria-hidden="true" className="h-5 w-5 text-content-secondary" />
                    {t('settings.restartRequired')}
                </h2>
                <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
                    {settings.restart_required.length === 0 && (
                        <QueryEmptyState className="md:col-span-2" title={t('queryFeedback.emptyTitle')} />
                    )}
                    {settings.restart_required.map(item => (
                        <div key={item.key} className="min-w-0 rounded-md border border-border bg-surface-muted px-3 py-2">
                            <div className="break-all font-mono text-sm font-semibold text-content-primary">{item.key}</div>
                            <div className="break-words text-sm text-content-secondary">{item.description}</div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};
