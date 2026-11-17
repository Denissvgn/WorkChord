import type { RouteModuleKey } from '../navigation/routeModules';

type RouteStatus = { key: RouteModuleKey; status: 'migrated' | 'pending'; path: string };
export const routeRegistry: RouteStatus[] = [
    { key: 'landing', path: '/welcome', status: 'migrated' },
    { key: 'overview', path: '/', status: 'migrated' },
    { key: 'planShare', path: '/plan/share/:publicId', status: 'migrated' },
    { key: 'plan', path: '/plan', status: 'migrated' },
    { key: 'team', path: '/team', status: 'migrated' },
    { key: 'myWork', path: '/my-work', status: 'migrated' },
    { key: 'nativeConnection', path: '/mobile/connect', status: 'migrated' },
    { key: 'tasks', path: '/tasks', status: 'migrated' },
    { key: 'triage', path: '/triage', status: 'migrated' },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', status: 'migrated' },
    { key: 'projectDetail', path: '/projects/:projectId', status: 'migrated' },
    { key: 'projects', path: '/projects', status: 'migrated' },
    { key: 'gantt', path: '/gantt', status: 'migrated' },
    { key: 'analytics', path: '/analytics', status: 'migrated' },
    { key: 'settings', path: '/settings', status: 'migrated' },
    { key: 'notFound', path: '*', status: 'migrated' },
];
