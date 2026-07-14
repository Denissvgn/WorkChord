import { NavLink } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Sparkles, TriangleAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { savedViewService } from '../../services/savedViewService';
import { savedViewDisplay } from '../../i18n/seedDisplay';
import type { SavedView } from '../../types/savedView';
import { WORKSPACES } from '../../navigation/workspaces';
import type { NavItem } from '../../navigation/workspaces';
import { SidebarIterationCard } from './SidebarIterationCard';

const SYSTEM_VIEW_ORDER = [
    'tasks_unassigned', 'tasks_blocked', 'tasks_overdue', 'tasks_high_priority',
    'tasks_ready_for_agent', 'tasks_active_this_iteration',
    'triage_needs_triage', 'projects_at_risk',
];

const systemOrderIndex = (view: SavedView) => {
    const index = SYSTEM_VIEW_ORDER.indexOf(view.seed_key ?? '');
    return index === -1 ? SYSTEM_VIEW_ORDER.length : index;
};

const systemViews = (views: SavedView[]) => (
    views
        .filter(view => view.scope === 'system' && view.seed_key)
        .sort((left, right) => systemOrderIndex(left) - systemOrderIndex(right) || left.name.localeCompare(right.name))
);

const viewPath = (view: SavedView) => {
    if (view.view_type === 'tasks') return `/tasks?view=${view.id}`;
    if (view.view_type === 'triage') return `/triage?view=${view.id}`;
    return `/projects?view=${view.id}`;
};

const SidebarNavItem = ({ item }: { item: NavItem }) => {
    const { t } = useTranslation();
    const label = t(item.labelKey, item.defaultLabel);
    const Icon = item.icon;
    return (
        <NavLink
            to={item.to}
            end={item.to === '/'}
            className="sb-item"
            aria-label={label}
            title={label}
        >
            <Icon aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
            <span className="sb-label">{label}</span>
        </NavLink>
    );
};

export const AppSidebar = () => {
    const { t } = useTranslation();
    const {
        data: savedViewGroups = { tasks: [], triage: [], projects: [] },
        error: savedViewsError,
        isLoading: savedViewsLoading,
        refetch: refetchSavedViews,
    } = useQuery({
        queryKey: ['saved-views', 'system-shortcuts'],
        queryFn: async () => {
            const [tasks, triage, projects] = await Promise.all([
                savedViewService.getAll({ view_type: 'tasks' }),
                savedViewService.getAll({ view_type: 'triage' }),
                savedViewService.getAll({ view_type: 'projects' }),
            ]);
            return { tasks: systemViews(tasks), triage: systemViews(triage), projects: systemViews(projects) };
        },
        staleTime: 60000,
    });

    const allViews = [...savedViewGroups.tasks, ...savedViewGroups.triage, ...savedViewGroups.projects];

    return (
        <aside className="sidebar" data-testid="app-sidebar" aria-label={t('nav.primaryNavigation')}>
            {WORKSPACES.map(workspace => (
                <div key={workspace.key} className="contents">
                    <div className="sb-group-lbl">{t(workspace.labelKey, workspace.defaultLabel)}</div>
                    {workspace.items.map(item => <SidebarNavItem key={item.to} item={item} />)}
                </div>
            ))}

            {allViews.length > 0 && (
                <>
                    <div className="sb-group-lbl">{t('nav.views')}</div>
                    {allViews.slice(0, 6).map(view => {
                        const label = savedViewDisplay(view).name;
                        const WarningIcon = view.seed_key === 'tasks_overdue' || view.seed_key === 'projects_at_risk'
                            ? TriangleAlert
                            : Sparkles;
                        return (
                            <NavLink key={view.id} to={viewPath(view)} className="sb-item" aria-label={label} title={label}>
                                <WarningIcon aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                                <span className="sb-label">{label}</span>
                            </NavLink>
                        );
                    })}
                </>
            )}
            {savedViewsLoading && <div className="sb-item" role="status"><span className="sb-label">{t('nav.loadingSystemViews')}</span></div>}
            {savedViewsError && (
                <button type="button" className="sb-item" onClick={() => { void refetchSavedViews(); }}>
                    <span className="sb-label">{t('nav.systemViewsLoadFailed')}</span>
                </button>
            )}
            {!savedViewsLoading && !savedViewsError && allViews.length === 0 && (
                <div className="sb-item"><span className="sb-label">{t('nav.noSystemViews')}</span></div>
            )}

            <div className="sb-spacer" />
            <SidebarIterationCard />
        </aside>
    );
};
