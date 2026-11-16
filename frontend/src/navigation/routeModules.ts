import { matchPath } from 'react-router-dom';
import { getDestination, type DestinationId } from './destinations';

export const routeModuleLoaders = {
    landing: () => import('../pages/LandingPage'),
    overview: () => import('../pages/OverviewPage'),
    plan: () => import('../pages/PlanPage'),
    // The old checkpoint page is part of Plan; its path redirects there.
    planMaster: () => import('../pages/PlanPage'),
    planShare: () => import('../pages/PlanSharePage'),
    calendar: () => import('../pages/CalendarPage'),
    iterations: () => import('../pages/IterationsPage'),
    team: () => import('../pages/TeamPage'),
    tasks: () => import('../pages/TasksPage'),
    myWork: () => import('../pages/MyWorkPage'),
    nativeConnection: () => import('../pages/NativeConnectionPage'),
    triage: () => import('../pages/TriagePage'),
    projects: () => import('../pages/ProjectsPage'),
    projectDetail: () => import('../pages/ProjectDetailPage'),
    projectReleaseDetail: () => import('../pages/ProjectReleaseDetailPage'),
    // Roadmap is a view of Projects; the old path redirects there.
    roadmap: () => import('../pages/ProjectsPage'),
    gantt: () => import('../pages/GanttPage'),
    analytics: () => import('../pages/AnalyticsPage'),
    settings: () => import('../pages/SettingsPage'),
    agentPipeline: () => import('../pages/AgentPipelinePage'),
    agentTeamSetup: () => import('../pages/AgentTeamSetupMasterPage'),
    notFound: () => import('../pages/NotFoundPage'),
} as const;

export type RouteModuleKey = keyof typeof routeModuleLoaders;

type RouteMetadata = {
    key: RouteModuleKey;
    path: string;
    titleKey: string;
};

// A destination's own page takes its title from the registry, so the document title and the
// sidebar label are the same vocabulary name.
const destinationTitle = (id: DestinationId) => getDestination(id).labelKey;

export const routeMetadata: RouteMetadata[] = [
    { key: 'landing', path: '/welcome', titleKey: 'documentTitles.landing' },
    { key: 'overview', path: '/', titleKey: destinationTitle('overview') },
    { key: 'planMaster', path: '/plan/master', titleKey: destinationTitle('plan') },
    { key: 'planShare', path: '/plan/share/:publicId', titleKey: 'documentTitles.planShare' },
    { key: 'plan', path: '/plan', titleKey: destinationTitle('plan') },
    { key: 'calendar', path: '/calendar', titleKey: 'documentTitles.calendar' },
    { key: 'iterations', path: '/iterations', titleKey: 'documentTitles.iterations' },
    { key: 'team', path: '/team', titleKey: destinationTitle('team') },
    { key: 'myWork', path: '/my-work', titleKey: destinationTitle('my_work') },
    { key: 'nativeConnection', path: '/mobile/connect', titleKey: 'teamwork.connectRoute' },
    { key: 'tasks', path: '/tasks', titleKey: destinationTitle('tasks') },
    { key: 'triage', path: '/triage', titleKey: destinationTitle('triage') },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', titleKey: 'documentTitles.projectReleaseDetail' },
    { key: 'projectDetail', path: '/projects/:projectId', titleKey: 'documentTitles.projectDetail' },
    { key: 'projects', path: '/projects', titleKey: destinationTitle('projects') },
    { key: 'roadmap', path: '/roadmap', titleKey: 'documentTitles.roadmap' },
    { key: 'gantt', path: '/gantt', titleKey: destinationTitle('gantt') },
    { key: 'analytics', path: '/analytics', titleKey: destinationTitle('analytics') },
    { key: 'settings', path: '/settings', titleKey: destinationTitle('settings') },
    { key: 'agentPipeline', path: '/agent-pipeline', titleKey: 'documentTitles.agentPipeline' },
    { key: 'agentTeamSetup', path: '/agent-team/setup', titleKey: 'documentTitles.agentTeamSetup' },
];

export const metadataForPath = (pathname: string): RouteMetadata => (
    routeMetadata.find(route => matchPath({ path: route.path, end: true }, pathname))
    ?? { key: 'notFound', path: '*', titleKey: 'documentTitles.notFound' }
);

export const warmRouteModule = async (pathname: string) => {
    await routeModuleLoaders[metadataForPath(pathname).key]();
};
