import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, Command, Menu, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { triageService } from '../../services/triageService';
import { usePlanningNavigationSummary } from '../../features/planningMasters/usePlanningNavigationSummary';
import { getWorkspaceForPath, WORKSPACES } from '../../navigation/workspaces';
import type { WorkspaceMetadata } from '../../navigation/workspaces';
import { warmRouteModule } from '../../navigation/routeModules';
import { useDialogLayer } from '../common/dialogLayer';
import { UserSessionBadge } from '../UserSessionBadge';
import { SidebarContent } from './AppSidebar';
import { openCommandMenu } from './commandMenuEvents';

interface WorkspaceAttention {
    badge: string;
    label: string;
    to: string;
    isError?: boolean;
}

const WorkspaceSwitchLink = ({
    workspace,
    active,
    variant,
    onNavigate,
    attention,
}: {
    workspace: WorkspaceMetadata;
    active: boolean;
    variant: 'desktop' | 'mobile';
    onNavigate?: () => void;
    attention?: WorkspaceAttention;
}) => {
    const { t } = useTranslation();
    const Icon = workspace.icon;
    const label = t(workspace.labelKey, workspace.defaultLabel);
    const description = t(workspace.descriptionKey, workspace.defaultDescription);
    const homeLabel = t('nav.openWorkAreaHome', { area: label });

    return (
        <span className={variant === 'desktop' ? 'workspace-switch-item' : 'mobile-workspace-item'}>
            <Link
                to={workspace.defaultPath}
                className={variant === 'desktop' ? 'nav-tab nav-workspace-tab' : 'mobile-workspace-link'}
                aria-current={active ? 'location' : undefined}
                aria-label={homeLabel}
                title={t('nav.workAreaHomeHint', { area: label, description })}
                onClick={onNavigate}
                onFocus={() => { void warmRouteModule(workspace.defaultPath); }}
                onMouseEnter={() => { void warmRouteModule(workspace.defaultPath); }}
            >
                <Icon aria-hidden="true" className="h-4 w-4 shrink-0" />
                <span className="workspace-switch-copy">
                    <span>{label}</span>
                    {variant === 'mobile' && <small>{description}</small>}
                </span>
            </Link>
            {attention && (
                <Link
                    to={attention.to}
                    className="workspace-attention-link"
                    aria-label={attention.label}
                    title={attention.label}
                    onClick={onNavigate}
                    onFocus={() => { void warmRouteModule(attention.to); }}
                    onMouseEnter={() => { void warmRouteModule(attention.to); }}
                >
                    <span className={`nb-attention${attention.isError ? ' error' : ''}`} aria-hidden="true">
                        {attention.isError ? <AlertTriangle className="h-3 w-3" /> : attention.badge}
                    </span>
                </Link>
            )}
        </span>
    );
};

export const AppTopNav = () => {
    const {
        iterations,
        ready,
        isIterationsError,
        isReadinessError,
    } = usePlanningNavigationSummary();
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
    const planningAttentionUnavailable = isIterationsError || isReadinessError;
    const deliveryAttention: WorkspaceAttention | undefined = triageError
        ? {
            badge: '!',
            label: t('nav.deliveryAttentionUnavailable'),
            to: '/triage',
            isError: true,
        }
        : inboxCount > 0
            ? {
                badge: String(inboxCount),
                label: t('nav.deliveryAttentionIntake', { count: inboxCount }),
                to: '/triage',
            }
            : undefined;
    const planningAttention: WorkspaceAttention | undefined = planningAttentionUnavailable
        ? {
            badge: '!',
            label: t('nav.planningAttentionUnavailable'),
            to: '/plan/master',
            isError: true,
        }
        : actionablePendingSteps > 0
            ? {
                badge: String(actionablePendingSteps),
                label: t('nav.planningAttention', { count: actionablePendingSteps }),
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
                        <path d="M6 7.5h11M6 12h7M6 16.5h9" stroke="var(--wc-accent-on)" strokeWidth="1.7" strokeLinecap="round" />
                        <circle cx="17" cy="7.5" r="1.5" fill="var(--wc-accent-on)" />
                        <circle cx="13" cy="12" r="1.5" fill="var(--wc-accent-on)" opacity="0.78" />
                        <circle cx="15" cy="16.5" r="1.5" fill="var(--wc-accent-on)" opacity="0.56" />
                    </svg>
                </div>
                <span className="brand-label">{t('common.appName')}</span>
            </Link>

            <nav className="nav-tabs workspace-switcher" aria-label={t('nav.workAreaHomes')}>
                {WORKSPACES.map(workspace => (
                    <WorkspaceSwitchLink
                        key={workspace.key}
                        workspace={workspace}
                        active={workspace.key === currentWorkspace.key}
                        variant="desktop"
                        attention={
                            workspace.key === 'delivery'
                                ? deliveryAttention
                                : workspace.key === 'planning'
                                    ? planningAttention
                                    : undefined
                        }
                    />
                ))}
            </nav>

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
                            <section className="mobile-nav-section" aria-labelledby="mobile-work-area-homes-heading">
                                <div className="mobile-nav-section-copy">
                                    <strong id="mobile-work-area-homes-heading">{t('nav.workAreaHomes')}</strong>
                                    <p>{t('nav.workAreaHomesHelp')}</p>
                                </div>
                                <nav className="mobile-workspace-switcher" aria-label={t('nav.workAreaHomes')}>
                                    {WORKSPACES.map(workspace => (
                                        <WorkspaceSwitchLink
                                            key={workspace.key}
                                            workspace={workspace}
                                            active={workspace.key === currentWorkspace.key}
                                            variant="mobile"
                                            onNavigate={() => setMobileMenuOpen(false)}
                                            attention={
                                                workspace.key === 'delivery'
                                                    ? deliveryAttention
                                                    : workspace.key === 'planning'
                                                        ? planningAttention
                                                        : undefined
                                            }
                                        />
                                    ))}
                                </nav>
                            </section>
                            <nav aria-label={t('nav.areaDestinations', {
                                area: t(currentWorkspace.labelKey, currentWorkspace.defaultLabel),
                            })}>
                                <SidebarContent onNavigate={() => setMobileMenuOpen(false)} />
                            </nav>
                        </div>
                    </aside>
                </div>
            )}
        </header>
    );
};
