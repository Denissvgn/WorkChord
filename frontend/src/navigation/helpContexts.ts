import {
    getDestination,
    getDestinationForPath,
    type DestinationId,
} from './destinations';
import {
    metadataForPath,
    type RouteModuleKey,
} from './routeModules';

// Glossary terms are names from config/workflow-vocabulary.json. Each one has its
// `contextHelp.glossary.<term>` entry in both catalogs, and a test keeps the names equal.
type GlossaryTerm = 'iteration' | 'capacity' | 'blockers' | 'assignee' | 'reviewer' | 'labels'
    | 'waits_for' | 'earliest_start' | 'due_by' | 'request' | 'notifications';

export type WorkflowGuideKey = 'plan' | 'gantt' | 'tasks' | 'settings';

type HelpRelatedLink = {
    to: string;
    labelKey: string;
    defaultLabel: string;
};

type DestinationHelp = {
    /** The text is `contextHelp.destinations.<id>.summary` in both catalogs. */
    glossary: readonly GlossaryTerm[];
    related: readonly DestinationId[];
};

const DESTINATION_HELP: Record<DestinationId, DestinationHelp> = {
    overview: { glossary: ['assignee', 'reviewer'], related: ['my_work', 'triage', 'tasks'] },
    my_work: { glossary: ['assignee', 'reviewer', 'notifications'], related: ['tasks', 'triage'] },
    triage: { glossary: ['request', 'labels'], related: ['tasks', 'projects'] },
    projects: { glossary: ['labels', 'due_by'], related: ['plan', 'tasks'] },
    plan: { glossary: ['iteration', 'capacity', 'blockers'], related: ['gantt', 'team'] },
    gantt: { glossary: ['waits_for', 'earliest_start', 'due_by'], related: ['plan', 'tasks'] },
    tasks: { glossary: ['assignee', 'reviewer', 'waits_for'], related: ['my_work', 'triage'] },
    analytics: { glossary: ['capacity', 'iteration'], related: ['tasks', 'team'] },
    team: { glossary: ['assignee', 'capacity'], related: ['analytics', 'settings'] },
    settings: { glossary: ['iteration', 'capacity'], related: ['team', 'plan'] },
};

// Only these pages open a guide below their summary, and their guide is the page's own.
const WORKFLOW_BY_ROUTE: Partial<Record<RouteModuleKey, WorkflowGuideKey>> = {
    plan: 'plan',
    planShare: 'plan',
    gantt: 'gantt',
    tasks: 'tasks',
    settings: 'settings',
};

// The entry's action reopens the Get started panel on Overview, from any page.
const SETUP_GUIDE_ENTRY = {
    labelKey: 'contextHelp.setupGuide.title',
    defaultLabel: 'Setup guide',
    descriptionKey: 'contextHelp.setupGuide.description',
    actionKey: 'contextHelp.setupGuide.open',
} as const;

const relatedLinkFor = (id: DestinationId): HelpRelatedLink => {
    const destination = getDestination(id);
    return {
        to: destination.path,
        labelKey: destination.labelKey,
        defaultLabel: destination.defaultLabel,
    };
};

export const getHelpContext = (pathname: string) => {
    const route = metadataForPath(pathname);
    // Unknown paths get Overview's help, so no page falls back to a generic hint.
    const destination = getDestinationForPath(pathname) ?? getDestination('overview');
    const help = DESTINATION_HELP[destination.id];

    return {
        routeKey: route.key,
        pageTitleKey: route.titleKey,
        destination,
        summaryKey: `contextHelp.destinations.${destination.id}.summary`,
        workflow: WORKFLOW_BY_ROUTE[route.key],
        glossary: help.glossary,
        relatedLinks: help.related.map(relatedLinkFor),
        setupGuide: SETUP_GUIDE_ENTRY,
    };
};
