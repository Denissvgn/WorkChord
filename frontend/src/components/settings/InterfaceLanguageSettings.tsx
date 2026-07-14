import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Globe2, Save } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { systemSettingsService } from '../../services/systemSettingsService';
import { getAdminAccessErrorMessage } from '../../utils/adminAccess';
import type { AppRuntimeSettingsUpdate, LanguageCode, RuntimeSettingSource, SystemSettings } from '../../types/systemSettings';

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

const fieldSource = (settings: { field_sources: Record<string, RuntimeSettingSource> }, field: string) => (
    settings.field_sources?.[field]
);

export const InterfaceLanguageSettings = () => {
    const { i18n, t } = useTranslation();
    const queryClient = useQueryClient();
    const [languageDraft, setLanguageDraft] = useState<LanguageCode | null>(null);
    const toast = useToast();

    const { data: settings, isLoading, error, isError, refetch } = useQuery({
        queryKey: ['system-settings'],
        queryFn: systemSettingsService.getSettings,
    });

    const languageMutation = useMutation({
        mutationFn: systemSettingsService.updateApp,
        onSuccess: (app) => {
            queryClient.setQueryData<SystemSettings>(['system-settings'], (current) => (
                current ? { ...current, app } : current
            ));
            queryClient.invalidateQueries({ queryKey: ['system-settings'] });
            setLanguageDraft(null);
            void i18n.changeLanguage(app.ui_language);
            document.documentElement.lang = app.ui_language;
            const nextT = i18n.getFixedT(app.ui_language);
            toast.success(nextT('settingsPage.interfaceLanguageSaved'));
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsPage.interfaceLanguageSaveFailed'),
            }));
        },
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
                message={message}
                onRetry={() => { void refetch(); }}
                title={t('settingsPage.interfaceLanguage')}
            />
        );
    }

    const selectedLanguage = languageDraft ?? settings.app.ui_language;
    const isUnchanged = selectedLanguage === settings.app.ui_language;

    const saveLanguage = () => {
        const payload: AppRuntimeSettingsUpdate = {
            ui_language: selectedLanguage,
            ai_language_mode: settings.app.ai_language_mode,
        };
        languageMutation.mutate(payload);
    };

    return (
        <section className="card space-y-4">
            <div>
                <h2 className="flex items-center gap-2 text-xl font-semibold text-content-primary">
                    <Globe2 className="h-5 w-5 text-feedback-success" />
                    {t('settingsPage.interfaceLanguage')}
                </h2>
                <p className="mt-1 text-sm text-content-secondary">{t('settingsPage.interfaceLanguageDescription')}</p>
            </div>

            <div>
                <div className="mb-1 flex items-center justify-between">
                    <label htmlFor="interface-language" className="text-sm font-medium text-content-primary">
                        {t('settingsPage.interfaceLanguageField')}
                    </label>
                    <SourceBadge source={fieldSource(settings.app, 'ui_language')} />
                </div>
                <select
                    id="interface-language"
                    value={selectedLanguage}
                    onChange={event => setLanguageDraft(event.target.value as LanguageCode)}
                    disabled={languageMutation.isPending}
                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="en">{t('common.language.en')}</option>
                    <option value="ru">{t('common.language.ru')}</option>
                </select>
            </div>

            <Button type="button" onClick={saveLanguage} isLoading={languageMutation.isPending} disabled={isUnchanged || languageMutation.isPending}>
                <Save className="mr-2 h-4 w-4" />
                {t('settingsPage.saveInterfaceLanguage')}
            </Button>
        </section>
    );
};
