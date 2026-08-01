import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, Menu, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { triageService } from '../../services/triageService';
import { usePlanningReadiness } from '../../features/planningMasters/usePlanningReadiness';
import { getWorkspaceForPath, WORKSPACES } from '../../navigation/workspaces';
import type { WorkspaceMetadata } from '../../navigation/workspaces';
import { warmRouteModule } from '../../navigation/routeModules';
import { useDialogLayer } from '../common/dialogLayer';
import { UserSessionBadge } from '../UserSessionBadge';
import { SidebarContent } from './AppSidebar';

interface WorkspaceAttention {
    badge: string;
    label: string;
    to: string;
    isError?: boolean;
}

const WorkspaceSwitchLink = ({
    workspace,
    active,
    className,
    onNavigate,
    attention,
}: {
    workspace: WorkspaceMetadata;
    active: boolean;
    className: string;
    onNavigate?: () => void;
    attention?: WorkspaceAttention;
}) => {
    const { t } = useTranslation();
    const Icon = workspace.icon;
    const label = t(workspace.labelKey, workspace.defaultLabel);
    const target = attention?.to ?? workspace.defaultPath;

    return (
        <Link
            to={target}
            className={className}
            aria-current={active ? 'location' : undefined}
            aria-label={attention?.label ?? label}
            title={attention?.label}
            onClick={onNavigate}
            onFocus={() => { void warmRouteModule(target); }}
            onMouseEnter={() => { void warmRouteModule(target); }}
        >
            <Icon aria-hidden="true" className="h-4 w-4 shrink-0" />
            <span>{label}</span>
            {attention && (
                <span className={`nb-attention${attention.isError ? ' error' : ''}`} aria-hidden="true">
                    {attention.isError ? <AlertTriangle className="h-3 w-3" /> : attention.badge}
                </span>
            )}
        </Link>
    );
};

export const AppTopNav = () => {
    const { iterations, ready } = usePlanningReadiness();
    const { t } = useTranslation();
    const location = useLocation();
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

    const pendingSteps = Math.max(0, ready.total - ready.done);
    const isEmpty = iterations.length === 0;
    const inboxCount = triageItems.length;
    const currentWorkspace = getWorkspaceForPath(location.pathname);
    const actionablePendingSteps = isEmpty ? 0 : pendingSteps;
    const deliveryAttention: WorkspaceAttention | undefined = triageError
        ? {
            badge: '!',
            label: t('nav.deliveryAttentionUnavailable'),
            to: '/triage',
            isError: true,
        }
        : inboxCount > 0 && actionablePendingSteps > 0
            ? {
                badge: String(inboxCount + actionablePendingSteps),
                label: t('nav.deliveryAttentionCombined', {
                    planning: actionablePendingSteps,
                    inbox: inboxCount,
                }),
                to: '/triage',
            }
            : inboxCount > 0
                ? {
                    badge: String(inboxCount),
                    label: t('nav.deliveryAttentionIntake', { count: inboxCount }),
                    to: '/triage',
                }
                : actionablePendingSteps > 0
                    ? {
                        badge: String(actionablePendingSteps),
                        label: t('nav.deliveryAttentionPlanning', { count: actionablePendingSteps }),
                        to: '/plan/master',
                    }
                    : undefined;

    useEffect(() => {
        if (typeof window === 'undefined' || !window.matchMedia) return undefined;

        const drawerBreakpoint = window.matchMedia('(max-width: 1024px)');
        const closeDrawerOnDesktop = (event: MediaQueryListEvent) => {
            if (!event.matches) setMobileMenuOpen(false);
        };

        drawerBreakpoint.addEventListener('change', closeDrawerOnDesktop);
        return () => drawerBreakpoint.removeEventListener('change', closeDrawerOnDesktop);
    }, []);

    return (
        <header className="topnav" data-testid="app-navbar">
            <Link
                to="/"
                className="brand"
                aria-label={t('nav.home', { appName: t('common.appName') })}
                onFocus={() => { void warmRouteModule('/'); }}
                onMouseEnter={() => { void warmRouteModule('/'); }}
            >
                <div className="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="1" y="1" width="22" height="22" rx="6" fill="var(--accent)" />
                        <rect x="6" y="7" width="11" height="2.6" rx="1.3" fill="var(--wc-accent-on)" />
                        <rect x="6" y="11" width="7" height="2.6" rx="1.3" fill="var(--wc-accent-on)" opacity="0.78" />
                        <rect x="6" y="15" width="9" height="2.6" rx="1.3" fill="var(--wc-accent-on)" opacity="0.56" />
                    </svg>
                </div>
                <span className="brand-label">{t('common.appName')}</span>
            </Link>

            <nav className="nav-tabs workspace-switcher" aria-label={t('nav.workspaceSelector')}>
                {WORKSPACES.map(workspace => (
                    <WorkspaceSwitchLink
                        key={workspace.key}
                        workspace={workspace}
                        active={workspace.key === currentWorkspace.key}
                        className="nav-tab nav-workspace-tab"
                        attention={workspace.key === 'delivery' ? deliveryAttention : undefined}
                    />
                ))}
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
                            <nav className="mobile-workspace-switcher" aria-label={t('nav.workspaceSelector')}>
                                {WORKSPACES.map(workspace => (
                                    <WorkspaceSwitchLink
                                        key={workspace.key}
                                        workspace={workspace}
                                        active={workspace.key === currentWorkspace.key}
                                        className="mobile-workspace-link"
                                        onNavigate={() => setMobileMenuOpen(false)}
                                        attention={workspace.key === 'delivery' ? deliveryAttention : undefined}
                                    />
                                ))}
                            </nav>
                            <nav aria-label={t(currentWorkspace.labelKey, currentWorkspace.defaultLabel)}>
                                <SidebarContent onNavigate={() => setMobileMenuOpen(false)} />
                            </nav>
                        </div>
                    </aside>
                </div>
            )}
        </header>
    );
};
