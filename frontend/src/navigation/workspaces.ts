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
    Network,
} from 'lucide-react';

export type WorkspaceKey = 'delivery' | 'planning' | 'resource';

export interface NavItem {
    to: string;
    labelKey: string;
    defaultLabel: string;
    icon: LucideIcon;
    secondary?: boolean;
}

export interface WorkspaceMetadata {
    key: WorkspaceKey;
    labelKey: string;
    defaultLabel: string;
    descriptionKey: string;
    defaultDescription: string;
    icon: LucideIcon;
    defaultPath: string;
    items: NavItem[];
}

export const WORKSPACES: WorkspaceMetadata[] = [
    {
        key: 'delivery',
        labelKey: 'nav.deliveryHub',
        defaultLabel: 'Delivery Hub',
        descriptionKey: 'nav.workAreaDescriptions.delivery',
        defaultDescription: 'Tasks, intake, projects, and delivery flow.',
        icon: ListTodo,
        defaultPath: '/',
        items: [
            { to: '/', labelKey: 'nav.overview', defaultLabel: 'Overview', icon: LayoutDashboard },
            { to: '/tasks', labelKey: 'nav.tasks', defaultLabel: 'Tasks', icon: ListTodo },
            { to: '/triage', labelKey: 'nav.triage', defaultLabel: 'Triage', icon: Inbox },
            { to: '/projects', labelKey: 'nav.projects', defaultLabel: 'Projects', icon: FolderOpen },
            { to: '/agent-pipeline', labelKey: 'nav.agentPipeline', defaultLabel: 'Agent Pipeline', icon: Bot, secondary: true },
        ]
    },
    {
        key: 'planning',
        labelKey: 'nav.timelinePlanning',
        defaultLabel: 'Timeline & Planning',
        descriptionKey: 'nav.workAreaDescriptions.planning',
        defaultDescription: 'Readiness, schedules, roadmaps, periods, and calendars.',
        icon: GanttChartSquare,
        defaultPath: '/plan',
        items: [
            { to: '/plan', labelKey: 'nav.planWork', defaultLabel: 'Plan Work', icon: MapPin },
            { to: '/gantt', labelKey: 'nav.gantt', defaultLabel: 'Gantt', icon: GanttChartSquare },
            { to: '/roadmap', labelKey: 'nav.roadmap', defaultLabel: 'Roadmap', icon: Map },
            { to: '/iterations', labelKey: 'nav.iterations', defaultLabel: 'Iterations', icon: Repeat },
            { to: '/calendar', labelKey: 'nav.calendar', defaultLabel: 'Calendar', icon: Calendar, secondary: true },
        ]
    },
    {
        key: 'resource',
        labelKey: 'nav.resourceSettings',
        defaultLabel: 'Resource & Settings',
        descriptionKey: 'nav.workAreaDescriptions.resource',
        defaultDescription: 'People, analytics, agents, and system settings.',
        icon: Settings,
        defaultPath: '/team',
        items: [
            { to: '/team', labelKey: 'nav.team', defaultLabel: 'Team', icon: Users },
            { to: '/analytics', labelKey: 'nav.analytics', defaultLabel: 'Analytics', icon: BarChart },
            { to: '/agent-team/setup', labelKey: 'nav.agentTeamSetup', defaultLabel: 'Agent Team Setup', icon: Network },
            { to: '/settings', labelKey: 'nav.settings', defaultLabel: 'Settings', icon: Settings },
        ]
    }
];

export const PRIMARY_NAV_ITEMS = WORKSPACES.flatMap(workspace => workspace.items);

export const getWorkspaceFromPath = (pathname: string): WorkspaceKey => {
    const workspace = WORKSPACES.find(candidate => candidate.items.some(item => (
        item.to === '/'
            ? pathname === '/'
            : pathname === item.to || pathname.startsWith(`${item.to}/`)
    )));

    return workspace?.key ?? 'delivery';
};

export const getWorkspaceForPath = (pathname: string): WorkspaceMetadata => (
    WORKSPACES.find(workspace => workspace.key === getWorkspaceFromPath(pathname)) ?? WORKSPACES[0]!
);
