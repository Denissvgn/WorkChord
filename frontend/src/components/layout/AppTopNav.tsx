import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Menu, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { triageService } from '../../services/triageService';
import { usePlanningReadiness } from '../../features/planningMasters/usePlanningReadiness';
import { PRIMARY_NAV_ITEMS, WORKSPACES } from '../../navigation/workspaces';
import { warmRouteModule } from '../../navigation/routeModules';
import { useDialogLayer } from '../common/dialogLayer';
import { UserSessionBadge } from '../UserSessionBadge';

const TOP_NAV_PATHS = ['/', '/plan', '/tasks', '/gantt', '/team', '/triage'];

export const AppTopNav = () => {
    const { iterations, ready } = usePlanningReadiness();
    const { t } = useTranslation();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const { dialogRef, requestClose } = useDialogLayer<HTMLElement>({
        open: mobileMenuOpen,
        onClose: () => setMobileMenuOpen(false),
    });

    const { data: triageItems = [], error: triageError } = useQuery({
        queryKey: ['triage', { active: true, limit: 100 }],
        queryFn: () => triageService.getAll({ active: true, limit: 100 }),
        staleTime: 60000,
    });

    const pendingSteps = ready.total - ready.done;
    const isEmpty = iterations.length === 0;
    const inboxCount = triageItems.length;
    const topItems = TOP_NAV_PATHS
        .map(path => PRIMARY_NAV_ITEMS.find(item => item.to === path))
        .filter((item): item is NonNullable<typeof item> => item != null);

    return (
        <header className="topnav" data-testid="app-navbar">
            <div className="brand">
                <div className="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="1" y="1" width="22" height="22" rx="6" fill="var(--accent)" />
                        <rect x="6" y="7" width="11" height="2.6" rx="1.3" fill="var(--wc-accent-on)" />
                        <rect x="6" y="11" width="7" height="2.6" rx="1.3" fill="var(--wc-accent-on)" opacity="0.78" />
                        <rect x="6" y="15" width="9" height="2.6" rx="1.3" fill="var(--wc-accent-on)" opacity="0.56" />
                    </svg>
                </div>
                <span className="brand-label" style={{ color: 'var(--ink)' }}>{t('common.appName')}</span>
            </div>

            <nav className="nav-tabs" aria-label={t('nav.primaryNavigation')}>
                {topItems.map(item => {
                    const Icon = item.icon;
                    const label = t(item.labelKey, item.defaultLabel);
                    const isPlan = item.to === '/plan';
                    const isTriage = item.to === '/triage';
                    const badge = isPlan && !isEmpty && pendingSteps > 0
                        ? pendingSteps
                        : isTriage && inboxCount > 0 ? inboxCount : null;
                    return (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            end={item.to === '/'}
                            className="nav-tab"
                            onFocus={() => { void warmRouteModule(item.to); }}
                            onMouseEnter={() => { void warmRouteModule(item.to); }}
                        >
                            <Icon aria-hidden="true" className="h-[14px] w-[14px]" />
                            <span className="nav-tab-label">{label}</span>
                            {badge != null && <span className="nb-badge">{badge}</span>}
                            {isPlan && isEmpty && <span className="nb-dot" aria-hidden="true" />}
                            {isTriage && triageError && (
                                <span className="nb-dot warn" role="status" aria-label={t('queryFeedback.fallback')} />
                            )}
                        </NavLink>
                    );
                })}
            </nav>

            <div className="nav-right">
                <button
                    type="button"
                    className="mobile-nav-trigger"
                    aria-label={t('nav.openMenu')}
                    aria-expanded={mobileMenuOpen}
                    aria-controls="mobile-primary-navigation"
                    onClick={() => setMobileMenuOpen(true)}
                >
                    <Menu aria-hidden="true" className="h-5 w-5" />
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
                    <nav
                        id="mobile-primary-navigation"
                        ref={dialogRef}
                        className="mobile-nav-panel"
                        role="dialog"
                        aria-modal="true"
                        aria-label={t('nav.primaryNavigation')}
                        tabIndex={-1}
                    >
                        <div className="mobile-nav-head">
                            <strong>{t('nav.navigationMenu')}</strong>
                            <button type="button" className="btn ghost" aria-label={t('actions.close')} onClick={requestClose}>
                                <X aria-hidden="true" className="h-4 w-4" />
                            </button>
                        </div>
                        <div className="mobile-nav-content">
                            {WORKSPACES.map(workspace => (
                                <section key={workspace.key} aria-labelledby={`mobile-nav-${workspace.key}`}>
                                    <h2 id={`mobile-nav-${workspace.key}`} className="mobile-nav-group">
                                        {t(workspace.labelKey, workspace.defaultLabel)}
                                    </h2>
                                    {workspace.items.map(item => {
                                        const Icon = item.icon;
                                        const label = t(item.labelKey, item.defaultLabel);
                                        return (
                                            <NavLink
                                                key={item.to}
                                                to={item.to}
                                                end={item.to === '/'}
                                                className="mobile-nav-item"
                                                onClick={() => setMobileMenuOpen(false)}
                                            >
                                                <Icon aria-hidden="true" className="h-4 w-4" />
                                                <span>{label}</span>
                                            </NavLink>
                                        );
                                    })}
                                </section>
                            ))}
                        </div>
                    </nav>
                </div>
            )}
        </header>
    );
};
