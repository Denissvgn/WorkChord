import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import { metadataForPath } from '../../navigation/routeModules';

export const DocumentMetadata = () => {
    const location = useLocation();
    const { t, i18n } = useTranslation();

    useEffect(() => {
        const pageTitle = t(metadataForPath(location.pathname).titleKey);
        document.title = t('documentTitles.format', {
            page: pageTitle,
            app: t('common.appName'),
        });
    }, [i18n.resolvedLanguage, location.pathname, t]);

    return null;
};
