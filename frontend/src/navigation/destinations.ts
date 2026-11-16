import type { LucideIcon } from 'lucide-react';
import {
    BarChart,
    FolderOpen,
    GanttChartSquare,
    Inbox,
    LayoutDashboard,
    ListTodo,
    MapPin,
    Settings,
    UserCheck,
    Users,
} from 'lucide-react';
import { matchPath } from 'react-router-dom';

// The ids match `destinations` in config/workflow-vocabulary.json.
export type DestinationId =
    | 'overview'
    | 'my_work'
    | 'triage'
    | 'projects'
    | 'plan'
    | 'gantt'
    | 'tasks'
    | 'analytics'
    | 'team'
    | 'settings';

export type DestinationGroupId = 'start' | 'plan' | 'deliver' | 'setup';

/**
 * Where a sidebar counter takes its number from.
 * - `none`: the destination shows no counter.
 * - `requestsWaiting`: the number of active Triage requests.
 * - `planProgress`: complete Plan checkpoints out of six, shown only while the plan is incomplete.
 */
export type DestinationCounterSource = 'none' | 'requestsWaiting' | 'planProgress';

export interface Destination {
    id: DestinationId;
    /** The path the sidebar item opens. */
    path: string;
    labelKey: string;
    defaultLabel: string;
    icon: LucideIcon;
    /** Omitted means `none`. */
    counter?: DestinationCounterSource;
    /**
     * Route patterns this destination owns, including its detail pages, its views and the
     * old paths that now belong to it. A pattern also owns the paths below it, except `/`.
     */
    owns: readonly string[];
}

export interface DestinationGroup {
    id: DestinationGroupId;
    /** The first group has no heading. */
    labelKey?: string;
    defaultLabel?: string;
    destinations: readonly Destination[];
}

export const DESTINATION_GROUPS: readonly DestinationGroup[] = [
    {
        id: 'start',
        destinations: [
            {
                id: 'overview',
                path: '/',
                labelKey: 'nav.overview',
                defaultLabel: 'Overview',
                icon: LayoutDashboard,
                // The public landing page sits outside the shell; its links lead into Overview.
                owns: ['/', '/welcome'],
            },
            {
                id: 'my_work',
                path: '/my-work',
                labelKey: 'teamwork.myWork',
                defaultLabel: 'My Work',
                icon: UserCheck,
                // The signed-in person approves their own companion device here.
                owns: ['/my-work', '/mobile/connect'],
            },
            {
                id: 'triage',
                path: '/triage',
                labelKey: 'nav.triage',
                defaultLabel: 'Triage',
                icon: Inbox,
                counter: 'requestsWaiting',
                owns: ['/triage'],
            },
        ],
    },
    {
        id: 'plan',
        labelKey: 'nav.groups.plan',
        defaultLabel: 'Plan',
        destinations: [
            {
                id: 'projects',
                path: '/projects',
                labelKey: 'nav.projects',
                defaultLabel: 'Projects',
                icon: FolderOpen,
                // Roadmap is a view of Projects.
                owns: [
                    '/projects',
                    '/projects/:projectId',
                    '/projects/:projectId/releases/:releaseId',
                    '/roadmap',
                ],
            },
            {
                id: 'plan',
                path: '/plan',
                labelKey: 'nav.planWork',
                defaultLabel: 'Plan',
                icon: MapPin,
                counter: 'planProgress',
                // Iterations and iteration capacity are managed in Plan.
                owns: ['/plan', '/plan/master', '/plan/share/:publicId', '/iterations'],
            },
            {
                id: 'gantt',
                path: '/gantt',
                labelKey: 'nav.gantt',
                defaultLabel: 'Gantt',
                icon: GanttChartSquare,
                owns: ['/gantt'],
            },
        ],
    },
    {
        id: 'deliver',
        labelKey: 'nav.groups.deliver',
        defaultLabel: 'Deliver',
        destinations: [
            {
                id: 'tasks',
                path: '/tasks',
                labelKey: 'nav.tasks',
                defaultLabel: 'Tasks',
                icon: ListTodo,
                // Requests waiting are counted on Triage, not here.
                counter: 'none',
                // The agent pipeline is a layout of Tasks.
                owns: ['/tasks', '/agent-pipeline'],
            },
            {
                id: 'analytics',
                path: '/analytics',
                labelKey: 'nav.analytics',
                defaultLabel: 'Analytics',
                icon: BarChart,
                owns: ['/analytics'],
            },
        ],
    },
    {
        id: 'setup',
        labelKey: 'nav.groups.setup',
        defaultLabel: 'Setup',
        destinations: [
            {
                id: 'team',
                path: '/team',
                labelKey: 'nav.team',
                defaultLabel: 'Team',
                icon: Users,
                // Agent connection and the model catalog are part of Team.
                owns: ['/team', '/agent-team/setup'],
            },
            {
                id: 'settings',
                path: '/settings',
                labelKey: 'nav.settings',
                defaultLabel: 'Settings',
                icon: Settings,
                // The work calendar is a section of Settings.
                owns: ['/settings', '/calendar'],
            },
        ],
    },
];

export const DESTINATIONS: readonly Destination[] = DESTINATION_GROUPS.flatMap(group => group.destinations);

export const getDestination = (id: DestinationId): Destination => {
    const destination = DESTINATIONS.find(candidate => candidate.id === id);
    if (!destination) throw new Error(`Unknown destination: ${id}`);
    return destination;
};

export const getDestinationGroup = (id: DestinationId): DestinationGroup => {
    const group = DESTINATION_GROUPS.find(candidate => candidate.destinations.some(destination => destination.id === id));
    if (!group) throw new Error(`Unknown destination: ${id}`);
    return group;
};

const ownsPath = (pattern: string, pathname: string) => (
    matchPath({ path: pattern, end: pattern === '/' }, pathname) !== null
);

/** Every destination that claims the path; the registry is valid when this is never more than one. */
export const destinationsOwningPath = (pathname: string): Destination[] => (
    DESTINATIONS.filter(destination => destination.owns.some(pattern => ownsPath(pattern, pathname)))
);

export const getDestinationForPath = (pathname: string): Destination | undefined => (
    destinationsOwningPath(pathname)[0]
);

export const getCounterSource = (destination: Destination): DestinationCounterSource => (
    destination.counter ?? 'none'
);

export interface DestinationCounterValues {
    requestsWaiting?: number;
    planProgress?: { done: number; total: number };
}

/** The counter text for a destination, or null when it shows none. */
export const formatDestinationCounter = (
    destination: Destination,
    values: DestinationCounterValues,
): string | null => {
    const source = getCounterSource(destination);
    if (source === 'requestsWaiting') {
        const count = values.requestsWaiting ?? 0;
        return count > 0 ? String(count) : null;
    }
    if (source === 'planProgress') {
        const progress = values.planProgress;
        if (!progress || progress.total <= 0 || progress.done >= progress.total) return null;
        return `${Math.max(0, progress.done)}/${progress.total}`;
    }
    return null;
};
