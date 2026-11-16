import { useCallback, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { parseScope } from '../../navigation/scopeParams';
import { useScopeStore } from './scopeStore';
import { isCompleteScope, scopedLink, type PartialWorkScope } from './workScope';

/**
 * Builds links that carry the current scope to scoped pages. It reads the URL, then the
 * remembered scope, which useWorkScope keeps checked; it loads nothing itself, so every
 * navigation item can use it.
 */
export const useScopeLink = (): ((to: string) => string) => {
    const { search } = useLocation();
    const rememberedProject = useScopeStore(state => state.project);
    const rememberedIteration = useScopeStore(state => state.iteration);
    const scope = useMemo(() => {
        const fromUrl = parseScope(search);
        const candidate: PartialWorkScope = {
            project: fromUrl.project ?? rememberedProject,
            iteration: fromUrl.iteration ?? rememberedIteration,
        };
        return isCompleteScope(candidate) ? candidate : undefined;
    }, [rememberedIteration, rememberedProject, search]);
    return useCallback((to: string) => scopedLink(to, scope), [scope]);
};
