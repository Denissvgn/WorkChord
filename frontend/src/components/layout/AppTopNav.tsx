import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Command, Menu, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { getDestinationForPath } from '../../navigation/destinations';
import { metadataForPath, warmRouteModule } from '../../navigation/routeModules';
import { useDialogLayer } from '../common/dialogLayer';
import { AccountMenuRowContext } from '../../features/identity/accountMenuRow';
import { UserSessionBadge } from '../UserSessionBadge';
import { SidebarContent } from './AppSidebar';
import { openCommandMenu } from './commandMenuEvents';
import { ContextHelp } from './ContextHelp';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { ScopeBar } from './ScopeBar';

import { Button } from '../../components/common/Button';
import { BrandMark } from './BrandMark';
const MOBILE_NAV_TITLE_ID = 'mobile-primary-navigation-title';

const PHONE_QUERY = '(max-width: 767px)';

/** True while the top bar has no room for the scope bar, so the drawer carries it. */
const usePhoneWidth = () => {
    const [phone, setPhone] = useState(
        () => typeof window !== 'undefined' && !!window.matchMedia && window.matchMedia(PHONE_QUERY).matches,
    );
    useEffect(() => {
        if (typeof window === 'undefined' || !window.matchMedia) return undefined;
        const query = window.matchMedia(PHONE_QUERY);
        const update = () => setPhone(query.matches);
        update();
        query.addEventListener('change', update);
        return () => query.removeEventListener('change', update);
    }, []);
    return phone;
};

export const AppTopNav = () => {
    const phoneWidth = usePhoneWidth();
    const { t } = useTranslation();
    const location = useLocation();
    const scopeLink = useScopeLink();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [accountMenuRow, setAccountMenuRow] = useState<HTMLElement | null>(null);
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

        const drawerBreakpoint = window.matchMedia('(max-width: 1023px)');
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
                <BrandMark />
                <span className="brand-label">{t('common.appName')}</span>
            </Link>

            <div className="topnav-center">
                {/* Below 1024px the sidebar folds into the drawer; the bar still names where you are. */}
                <p className="topnav-location" data-testid="topnav-location">{currentPageName}</p>
                <div className="topnav-scope" data-slot="scope-bar" data-testid="topnav-scope-slot">
                    <ScopeBar />
                </div>
            </div>

            <div className="nav-right">
                <Button
                    type="button"
                    className="command-menu-trigger"
                    aria-label={t('commandMenu.trigger')}
                    aria-keyshortcuts="Meta+K Control+K"
                    onClick={openCommandMenu}
                 variant="plain">
                    <Command aria-hidden="true" className="h-4 w-4" />
                    <span>{t('commandMenu.triggerLabel')}</span>
                    <kbd>{t('commandMenu.openShortcut')}</kbd>
                </Button>
                <ContextHelp />
                <Button
                    type="button"
                    className="mobile-nav-trigger"
                    aria-label={t('nav.openMenu')}
                    aria-expanded={mobileMenuOpen}
                    aria-controls="mobile-primary-navigation"
                    onClick={openMobileMenu}
                 variant="plain">
                    <Menu aria-hidden="true" className="h-5 w-5" />
                    <span className="mobile-nav-trigger-label">{t('nav.navigationMenu')}</span>
                </Button>
                <AccountMenuRowContext.Provider value={accountMenuRow}>
                    <UserSessionBadge />
                </AccountMenuRowContext.Provider>
            </div>
            <div ref={setAccountMenuRow} className="topnav-account-row" />

            {mobileMenuOpen && (
                <div className="mobile-nav-layer">
                    <Button
                        type="button"
                        className="mobile-nav-backdrop"
                        tabIndex={-1}
                        aria-hidden="true"
                        onClick={requestClose}
                        variant="plain"
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
                            <Button type="button"  aria-label={t('actions.close')} title={t('actions.close')} onClick={requestClose} variant="ghost" iconOnly>
                                <X aria-hidden="true" className="h-4 w-4" />
                            </Button>
                        </div>
                        <div className="mobile-nav-content">
                            {phoneWidth && (
                                <div className="mobile-nav-scope" data-testid="mobile-nav-scope">
                                    <ScopeBar />
                                </div>
                            )}
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
