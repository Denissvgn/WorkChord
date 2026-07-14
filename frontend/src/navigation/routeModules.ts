import { matchPath } from 'react-router-dom';

export const routeModuleLoaders = {
    overview: () => import('../pages/OverviewPage'),
    plan: () => import('../pages/PlanPage'),
    planMaster: () => import('../pages/PlanMasterPage'),
    calendar: () => import('../pages/CalendarPage'),
    iterations: () => import('../pages/IterationsPage'),
    team: () => import('../pages/TeamPage'),
    tasks: () => import('../pages/TasksPage'),
    triage: () => import('../pages/TriagePage'),
    projects: () => import('../pages/ProjectsPage'),
    projectDetail: () => import('../pages/ProjectDetailPage'),
    projectReleaseDetail: () => import('../pages/ProjectReleaseDetailPage'),
    roadmap: () => import('../pages/RoadmapPage'),
    gantt: () => import('../pages/GanttPage'),
    analytics: () => import('../pages/AnalyticsPage'),
    settings: () => import('../pages/SettingsPage'),
    agentPipeline: () => import('../pages/AgentPipelinePage'),
    notFound: () => import('../pages/NotFoundPage'),
} as const;

export type RouteModuleKey = keyof typeof routeModuleLoaders;

type RouteMetadata = {
    key: RouteModuleKey;
    path: string;
    titleKey: string;
};

export const routeMetadata: RouteMetadata[] = [
    { key: 'overview', path: '/', titleKey: 'documentTitles.overview' },
    { key: 'planMaster', path: '/plan/master', titleKey: 'documentTitles.planMaster' },
    { key: 'plan', path: '/plan', titleKey: 'documentTitles.plan' },
    { key: 'calendar', path: '/calendar', titleKey: 'documentTitles.calendar' },
    { key: 'iterations', path: '/iterations', titleKey: 'documentTitles.iterations' },
    { key: 'team', path: '/team', titleKey: 'documentTitles.team' },
    { key: 'tasks', path: '/tasks', titleKey: 'documentTitles.tasks' },
    { key: 'triage', path: '/triage', titleKey: 'documentTitles.triage' },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', titleKey: 'documentTitles.projectReleaseDetail' },
    { key: 'projectDetail', path: '/projects/:projectId', titleKey: 'documentTitles.projectDetail' },
    { key: 'projects', path: '/projects', titleKey: 'documentTitles.projects' },
    { key: 'roadmap', path: '/roadmap', titleKey: 'documentTitles.roadmap' },
    { key: 'gantt', path: '/gantt', titleKey: 'documentTitles.gantt' },
    { key: 'analytics', path: '/analytics', titleKey: 'documentTitles.analytics' },
    { key: 'settings', path: '/settings', titleKey: 'documentTitles.settings' },
    { key: 'agentPipeline', path: '/agent-pipeline', titleKey: 'documentTitles.agentPipeline' },
];

export const metadataForPath = (pathname: string): RouteMetadata => (
    routeMetadata.find(route => matchPath({ path: route.path, end: true }, pathname))
    ?? { key: 'notFound', path: '*', titleKey: 'documentTitles.notFound' }
);

export const warmRouteModule = async (pathname: string) => {
    await routeModuleLoaders[metadataForPath(pathname).key]();
};
