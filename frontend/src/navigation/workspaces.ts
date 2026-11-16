// Compatibility layer for the shell that still renders three work areas with top-bar tabs.
// Destinations, their labels, icons and paths come from the registry in ./destinations;
// this file only arranges them into the old areas and adds the old view pages as links.
// Delete it once the sidebar, top bar, command menu and help render the registry directly.
import type { LucideIcon } from 'lucide-react';
import {
    Bot,
    Calendar,
    GanttChartSquare,
    Map,
    Network,
    Repeat,
    Settings,
    Truck,
} from 'lucide-react';
import { getDestination, getDestinationForPath, type DestinationId } from './destinations';

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

const destinationItem = (id: DestinationId): NavItem => {
    const destination = getDestination(id);
    return {
        to: destination.path,
        labelKey: destination.labelKey,
        defaultLabel: destination.defaultLabel,
        icon: destination.icon,
    };
};

// Old pages that the registry treats as views or sections of a destination. Until they
// redirect, the current shell keeps a link to each so every page stays reachable.
const VIEW_ITEMS = {
    roadmap: { to: '/roadmap', labelKey: 'nav.roadmap', defaultLabel: 'Roadmap', icon: Map },
    iterations: { to: '/iterations', labelKey: 'nav.iterations', defaultLabel: 'Iterations', icon: Repeat },
    calendar: { to: '/calendar', labelKey: 'nav.calendar', defaultLabel: 'Calendar', icon: Calendar, secondary: true },
    agentPipeline: { to: '/agent-pipeline', labelKey: 'nav.agentPipeline', defaultLabel: 'Agent Pipeline', icon: Bot, secondary: true },
    agentTeamSetup: { to: '/agent-team/setup', labelKey: 'nav.agentTeamSetup', defaultLabel: 'Agent Team Setup', icon: Network },
} as const satisfies Record<string, NavItem>;

export const WORKSPACES: WorkspaceMetadata[] = [
    {
        key: 'delivery',
        labelKey: 'nav.deliveryHub',
        defaultLabel: 'Delivery Hub',
        descriptionKey: 'nav.workAreaDescriptions.delivery',
        defaultDescription: 'Tasks, intake, projects, and delivery flow.',
        icon: Truck,
        defaultPath: '/',
        items: [
            destinationItem('overview'),
            destinationItem('my_work'),
            destinationItem('tasks'),
            destinationItem('triage'),
            destinationItem('projects'),
            VIEW_ITEMS.agentPipeline,
        ],
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
            destinationItem('plan'),
            destinationItem('gantt'),
            VIEW_ITEMS.roadmap,
            VIEW_ITEMS.iterations,
            VIEW_ITEMS.calendar,
        ],
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
            destinationItem('team'),
            destinationItem('analytics'),
            VIEW_ITEMS.agentTeamSetup,
            destinationItem('settings'),
        ],
    },
];

const isWithin = (pathname: string, to: string) => pathname === to || pathname.startsWith(`${to}/`);

/**
 * The old area for a path. An old view page stays in the area that lists it; every other
 * path follows the destination that owns it in the registry.
 */
export const getWorkspaceForPath = (pathname: string): WorkspaceMetadata => {
    const viewArea = WORKSPACES.find(workspace => workspace.items.some(item => (
        Object.values(VIEW_ITEMS).some(view => view.to === item.to) && isWithin(pathname, item.to)
    )));
    if (viewArea) return viewArea;

    const destination = getDestinationForPath(pathname);
    const area = destination
        ? WORKSPACES.find(workspace => workspace.items.some(item => item.to === destination.path))
        : undefined;
    return area ?? WORKSPACES[0]!;
};
