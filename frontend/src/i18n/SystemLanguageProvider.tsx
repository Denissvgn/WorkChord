import { type ReactNode, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { systemSettingsService } from '../services/systemSettingsService';
import { useAdminAccess } from '../hooks/useAdminAccess';
import { changeAppLanguage } from './i18n';

interface SystemLanguageProviderProps {
    children: ReactNode;
}

export const SystemLanguageProvider = ({ children }: SystemLanguageProviderProps) => {
    const { i18n, t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();

    const { data, error, isError, isLoading, refetch } = useQuery({
        queryKey: ['system-settings'],
        queryFn: systemSettingsService.getSettings,
        enabled: hasAdminKey,
        staleTime: 60000,
    });

    useEffect(() => {
        const language = (i18n.resolvedLanguage || i18n.language || 'en').split('-')[0];
        document.documentElement.lang = language === 'ru' ? 'ru' : 'en';
    }, [i18n.language, i18n.resolvedLanguage]);

    useEffect(() => {
        const language = data?.app?.ui_language;
        if (language) {
            if (i18n.language !== language) {
                void changeAppLanguage(language);
            }
        }
    }, [data?.app?.ui_language, i18n]);

    return (
        <>
            {children}
            {hasAdminKey && isLoading && (
                <QueryLoadingState className="fixed bottom-4 left-4 z-50 min-h-0 py-3" />
            )}
            {hasAdminKey && isError && (
                <QueryErrorState
                    className="fixed bottom-4 left-4 z-50 max-w-md shadow-lg"
                    error={error}
                    fallback={t('queryFeedback.fallback')}
                    onRetry={() => { void refetch(); }}
                    title={t('settingsPage.interfaceLanguage')}
                />
            )}
        </>
    );
};
