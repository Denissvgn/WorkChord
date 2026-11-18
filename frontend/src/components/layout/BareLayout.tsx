import { useEffect, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { useThemeStore } from '../../store/themeStore';
import { DocumentMetadata } from './DocumentMetadata';
import { RouteErrorBoundary } from './RouteErrorBoundary';
import { BrandMark } from './BrandMark';

export function BareLayout({ children }: { children: ReactNode }) {
    const { t } = useTranslation();
    const { theme } = useThemeStore();
    const location = useLocation();
    const scopeLink = useScopeLink();
    useEffect(() => { document.documentElement.setAttribute('data-theme', theme); }, [theme]);
    return (
        <div className="wc app">
            <DocumentMetadata />
            <header className="topnav">
                <Link to={scopeLink('/')} className="brand" aria-label={t('nav.home', { appName: t('common.appName') })}>
                    <BrandMark />
                    <span className="brand-label">{t('common.appName')}</span>
                </Link>
            </header>
            <main className="main">
                <RouteErrorBoundary resetKey={`${location.pathname}${location.search}`} title={t('routeError.title')} description={t('routeError.description')} refreshLabel={t('routeError.refresh')} homeLabel={t('routeError.home')}>
                    {children}
                </RouteErrorBoundary>
            </main>
        </div>
    );
}
