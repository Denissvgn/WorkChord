import type { LucideIcon } from 'lucide-react';
import {
    LayoutDashboard,
    Calendar,
    Inbox,
    Users,
    ListTodo,
    FolderOpen,
    Map,
    GanttChartSquare,
    Settings,
    Repeat,
    BarChart,
    Bot,
    MapPin,
} from 'lucide-react';

export type WorkspaceKey = 'delivery' | 'planning' | 'resource';

export interface NavItem {
    to: string;
    labelKey: string;
    defaultLabel: string;
    icon: LucideIcon;
}

export interface WorkspaceMetadata {
    key: WorkspaceKey;
    labelKey: string;
    defaultLabel: string;
    icon: LucideIcon;
    defaultPath: string;
    items: NavItem[];
}

export const WORKSPACES: WorkspaceMetadata[] = [
    {
        key: 'delivery',
        labelKey: 'nav.deliveryHub',
        defaultLabel: 'Delivery Hub',
        icon: ListTodo,
        defaultPath: '/',
        items: [
            { to: '/', labelKey: 'nav.overview', defaultLabel: 'Overview', icon: LayoutDashboard },
            { to: '/plan', labelKey: 'nav.planWork', defaultLabel: 'Plan Work', icon: MapPin },
            { to: '/tasks', labelKey: 'nav.tasks', defaultLabel: 'Tasks', icon: ListTodo },
            { to: '/triage', labelKey: 'nav.triage', defaultLabel: 'Triage', icon: Inbox },
            { to: '/projects', labelKey: 'nav.projects', defaultLabel: 'Projects', icon: FolderOpen },
            { to: '/agent-pipeline', labelKey: 'nav.agentPipeline', defaultLabel: 'Agent Pipeline', icon: Bot },
        ]
    },
    {
        key: 'planning',
        labelKey: 'nav.timelinePlanning',
        defaultLabel: 'Timeline & Planning',
        icon: GanttChartSquare,
        defaultPath: '/gantt',
        items: [
            { to: '/gantt', labelKey: 'nav.gantt', defaultLabel: 'Gantt', icon: GanttChartSquare },
            { to: '/roadmap', labelKey: 'nav.roadmap', defaultLabel: 'Roadmap', icon: Map },
            { to: '/iterations', labelKey: 'nav.iterations', defaultLabel: 'Iterations', icon: Repeat },
            { to: '/calendar', labelKey: 'nav.calendar', defaultLabel: 'Calendar', icon: Calendar },
        ]
    },
    {
        key: 'resource',
        labelKey: 'nav.resourceSettings',
        defaultLabel: 'Resource & Settings',
        icon: Settings,
        defaultPath: '/team',
        items: [
            { to: '/team', labelKey: 'nav.team', defaultLabel: 'Team', icon: Users },
            { to: '/analytics', labelKey: 'nav.analytics', defaultLabel: 'Analytics', icon: BarChart },
            { to: '/settings', labelKey: 'nav.settings', defaultLabel: 'Settings', icon: Settings },
        ]
    }
];

export const PRIMARY_NAV_ITEMS = WORKSPACES.flatMap(workspace => workspace.items);

export const getWorkspaceFromPath = (path: string): WorkspaceKey => {
    if (
        path.startsWith('/gantt') ||
        path.startsWith('/roadmap') ||
        path.startsWith('/iterations') ||
        path.startsWith('/calendar')
    ) {
        return 'planning';
    }
    if (
        path.startsWith('/team') ||
        path.startsWith('/analytics') ||
        path.startsWith('/settings')
    ) {
        return 'resource';
    }
    return 'delivery';
};
