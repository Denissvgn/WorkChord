import { QueryClient } from '@tanstack/react-query';
import { installPlanningNavigationInvalidation } from './planningMasters/planningNavigationInvalidation';
import { installWorkFreshness } from './workQueryFreshness';

export const createWorkspaceQueryClient = (accessKey: string) => new QueryClient({
    defaultOptions: { queries: { retry: 1, staleTime: 15000, refetchOnWindowFocus: true,
        meta: { workspaceAccess: accessKey } } },
});

export const installWorkspaceQueryPolicy = (client: QueryClient) => {
    const stopWork = installWorkFreshness(client);
    const stopPlanning = installPlanningNavigationInvalidation(client);
    return () => {
        stopWork();
        stopPlanning();
        void client.cancelQueries();
        client.clear();
    };
};
