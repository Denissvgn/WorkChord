import { useEffect, type ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { useThemeStore } from '../../store/themeStore';
import { DocumentMetadata } from './DocumentMetadata';
import { RouteErrorBoundary } from './RouteErrorBoundary';

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
                    <div className="brand-mark" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="1" y="1" width="22" height="22" rx="6" fill="var(--accent)" />
                            <path d="M6 7.5h11M6 12h7M6 16.5h9" stroke="var(--wc-accent-on)" strokeWidth="1.7" strokeLinecap="round" />
                            <circle cx="17" cy="7.5" r="1.5" fill="var(--wc-accent-on)" />
                            <circle cx="13" cy="12" r="1.5" fill="var(--wc-accent-on)" opacity="0.78" />
                            <circle cx="15" cy="16.5" r="1.5" fill="var(--wc-accent-on)" opacity="0.56" />
                        </svg>
                    </div>
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
