import type { ReactNode } from 'react';
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useThemeStore } from '../../store/themeStore';
import { RouteErrorBoundary } from './RouteErrorBoundary';
import { AppTopNav } from './AppTopNav';
import { AppSidebar } from './AppSidebar';
import { DocumentMetadata } from './DocumentMetadata';

// Full-height routes where the main area must not scroll itself
// (the inner component controls overflow).
const SCROLL_LOCK_PATHS = ['/gantt', '/plan/master', '/tasks', '/triage'];

export const AppShell = ({ children }: { children: ReactNode }) => {
    const { theme } = useThemeStore();
    const location = useLocation();
    const { t } = useTranslation();

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    const scrollLock = SCROLL_LOCK_PATHS.some(p => location.pathname.startsWith(p));

    return (
        <div className="wc app">
            <DocumentMetadata />
            <a className="skip-link" href="#workspace-main">
                {t('nav.skipToContent')}
            </a>
            <AppTopNav />
            <div className="workspace">
                <AppSidebar />
                <main
                    id="workspace-main"
                    className={`main${scrollLock ? ' scroll-lock' : ''}`}
                    tabIndex={-1}
                >
                    <RouteErrorBoundary
                        resetKey={`${location.pathname}${location.search}`}
                        title={t('routeError.title')}
                        description={t('routeError.description')}
                        refreshLabel={t('routeError.refresh')}
                        homeLabel={t('routeError.home')}
                    >
                        {children}
                    </RouteErrorBoundary>
                </main>
            </div>
        </div>
    );
};
