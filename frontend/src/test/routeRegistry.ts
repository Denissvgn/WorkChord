import type { RouteModuleKey } from '../navigation/routeModules';

type RouteStatus = { key: RouteModuleKey; status: 'migrated' | 'pending'; path: string };
export const routeRegistry: RouteStatus[] = [
    { key: 'landing', path: '/welcome', status: 'pending' },
    { key: 'overview', path: '/', status: 'pending' },
    { key: 'planMaster', path: '/plan/master', status: 'pending' },
    { key: 'planShare', path: '/plan/share/:publicId', status: 'pending' },
    { key: 'plan', path: '/plan', status: 'migrated' },
    { key: 'calendar', path: '/calendar', status: 'pending' },
    { key: 'iterations', path: '/iterations', status: 'pending' },
    { key: 'team', path: '/team', status: 'pending' },
    { key: 'myWork', path: '/my-work', status: 'pending' },
    { key: 'nativeConnection', path: '/mobile/connect', status: 'pending' },
    { key: 'tasks', path: '/tasks', status: 'migrated' },
    { key: 'triage', path: '/triage', status: 'pending' },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', status: 'pending' },
    { key: 'projectDetail', path: '/projects/:projectId', status: 'pending' },
    { key: 'projects', path: '/projects', status: 'migrated' },
    { key: 'roadmap', path: '/roadmap', status: 'pending' },
    { key: 'gantt', path: '/gantt', status: 'migrated' },
    { key: 'analytics', path: '/analytics', status: 'pending' },
    { key: 'settings', path: '/settings', status: 'migrated' },
    { key: 'agentPipeline', path: '/agent-pipeline', status: 'pending' },
    { key: 'agentTeamSetup', path: '/agent-team/setup', status: 'pending' },
    { key: 'notFound', path: '*', status: 'migrated' },
];
