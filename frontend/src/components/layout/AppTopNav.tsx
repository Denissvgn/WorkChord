import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Command, Menu, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { getDestinationForPath } from '../../navigation/destinations';
import { metadataForPath, warmRouteModule } from '../../navigation/routeModules';
import { useDialogLayer } from '../common/dialogLayer';
import { UserSessionBadge } from '../UserSessionBadge';
import { SidebarContent } from './AppSidebar';
import { openCommandMenu } from './commandMenuEvents';
import { ContextHelp } from './ContextHelp';
import { useScopeLink } from '../../features/scope/useScopeLink';

const MOBILE_NAV_TITLE_ID = 'mobile-primary-navigation-title';

export const AppTopNav = () => {
    const { t } = useTranslation();
    const location = useLocation();
    const scopeLink = useScopeLink();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const mobileNavRestoreFocusRef = useRef<HTMLElement | null>(null);
    const { dialogRef, requestClose } = useDialogLayer<HTMLElement>({
        open: mobileMenuOpen,
        onClose: () => setMobileMenuOpen(false),
        restoreFocusRef: mobileNavRestoreFocusRef,
    });

    const currentDestination = getDestinationForPath(location.pathname);
    const currentPageName = currentDestination
        ? t(currentDestination.labelKey, currentDestination.defaultLabel)
        : t(metadataForPath(location.pathname).titleKey);

    useEffect(() => {
        if (typeof window === 'undefined' || !window.matchMedia) return undefined;

        const drawerBreakpoint = window.matchMedia('(max-width: 1180px)');
        const closeDrawerOnDesktop = (event: MediaQueryListEvent) => {
            if (event.matches) return;
            setMobileMenuOpen(wasOpen => {
                if (wasOpen) {
                    // The drawer is gone at this width; hand focus to the same place in the sidebar.
                    mobileNavRestoreFocusRef.current = document.querySelector<HTMLElement>(
                        '.sidebar [aria-current="page"]',
                    ) ?? document.querySelector<HTMLElement>('.brand');
                }
                return false;
            });
        };

        drawerBreakpoint.addEventListener('change', closeDrawerOnDesktop);
        return () => drawerBreakpoint.removeEventListener('change', closeDrawerOnDesktop);
    }, []);

    const closeForNavigation = () => {
        mobileNavRestoreFocusRef.current = document.getElementById('workspace-main');
        setMobileMenuOpen(false);
    };

    const openMobileMenu = () => {
        mobileNavRestoreFocusRef.current = null;
        setMobileMenuOpen(true);
    };

    return (
        <header className="topnav" data-testid="app-navbar">
            <Link
                to={scopeLink('/')}
                className="brand"
                aria-label={t('nav.home', { appName: t('common.appName') })}
                onFocus={() => { void warmRouteModule('/'); }}
                onMouseEnter={() => { void warmRouteModule('/'); }}
            >
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

            <div className="topnav-center">
                {/* Below 1180px the sidebar folds into the drawer; the bar still names where you are. */}
                <p className="topnav-location" data-testid="topnav-location">{currentPageName}</p>
                {/* Reserved for the scope bar. */}
                <div className="topnav-scope" data-slot="scope-bar" data-testid="topnav-scope-slot" />
            </div>

            <div className="nav-right">
                <button
                    type="button"
                    className="command-menu-trigger"
                    aria-label={t('commandMenu.trigger')}
                    aria-keyshortcuts="Meta+K Control+K"
                    onClick={openCommandMenu}
                >
                    <Command aria-hidden="true" className="h-4 w-4" />
                    <span>{t('commandMenu.triggerLabel')}</span>
                    <kbd>{t('commandMenu.openShortcut')}</kbd>
                </button>
                <ContextHelp />
                <button
                    type="button"
                    className="mobile-nav-trigger"
                    aria-label={t('nav.openMenu')}
                    aria-expanded={mobileMenuOpen}
                    aria-controls="mobile-primary-navigation"
                    onClick={openMobileMenu}
                >
                    <Menu aria-hidden="true" className="h-5 w-5" />
                    <span className="mobile-nav-trigger-label">{t('nav.navigationMenu')}</span>
                </button>
                <UserSessionBadge />
            </div>

            {mobileMenuOpen && (
                <div className="mobile-nav-layer">
                    <button
                        type="button"
                        className="mobile-nav-backdrop"
                        tabIndex={-1}
                        aria-hidden="true"
                        onClick={requestClose}
                    />
                    <aside
                        id="mobile-primary-navigation"
                        ref={dialogRef}
                        className="mobile-nav-panel"
                        role="dialog"
                        aria-modal="true"
                        aria-labelledby={MOBILE_NAV_TITLE_ID}
                        tabIndex={-1}
                    >
                        <div className="mobile-nav-head">
                            <h2 id={MOBILE_NAV_TITLE_ID}>{t('nav.primaryNavigation')}</h2>
                            <button type="button" className="btn ghost icon" aria-label={t('actions.close')} title={t('actions.close')} onClick={requestClose}>
                                <X aria-hidden="true" className="h-4 w-4" />
                            </button>
                        </div>
                        <div className="mobile-nav-content">
                            <nav aria-label={t('nav.primaryNavigation')}>
                                <SidebarContent onNavigate={closeForNavigation} />
                            </nav>
                        </div>
                    </aside>
                </div>
            )}
        </header>
    );
};
