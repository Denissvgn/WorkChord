import type { ReactNode } from 'react';
import { useEffect, useRef } from 'react';
import { MotionConfig } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useThemeStore } from '../../store/themeStore';
import { RouteErrorBoundary } from './RouteErrorBoundary';
import { AppTopNav } from './AppTopNav';
import { AppSidebar } from './AppSidebar';
import { DocumentMetadata } from './DocumentMetadata';
import { CommandMenu } from './CommandMenu';

// Full-height routes where the main area must not scroll itself
// (the inner component controls overflow).
const SCROLL_LOCK_PATHS = ['/gantt', '/plan/master', '/tasks', '/triage'];

export const AppShell = ({ children }: { children: ReactNode }) => {
    const { theme } = useThemeStore();
    const location = useLocation();
    const { t } = useTranslation();
    const workspaceMainRef = useRef<HTMLElement>(null);
    const previousPathnameRef = useRef(location.pathname);

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    useEffect(() => {
        const previousPathname = previousPathnameRef.current;
        previousPathnameRef.current = location.pathname;

        if (previousPathname !== location.pathname) {
            workspaceMainRef.current?.focus();
        }
    }, [location.pathname]);

    const scrollLock = SCROLL_LOCK_PATHS.some(p => location.pathname.startsWith(p));

    return (
        <MotionConfig reducedMotion="user">
            <div className="wc app">
                <DocumentMetadata />
                <CommandMenu />
                <a className="skip-link" href="#workspace-main">
                    {t('nav.skipToContent')}
                </a>
                <AppTopNav />
                <div className="workspace">
                    <AppSidebar />
                    <main
                        ref={workspaceMainRef}
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
        </MotionConfig>
    );
};
