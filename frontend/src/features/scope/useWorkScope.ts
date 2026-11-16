import { useCallback, useEffect, useMemo, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useLocation, useNavigate } from 'react-router-dom';
import { parseScope } from '../../navigation/scopeParams';
import { iterationService } from '../../services/iterationService';
import { useScopeStore, type RememberedScope } from './scopeStore';
import {
    defaultIterationForProject,
    hasScopeParams,
    isCompleteScope,
    isScopedPath,
    resolveWorkScope,
    sameScope,
    scopedLink,
    withScopeSearch,
    type PartialWorkScope,
    type ScopeIteration,
    type ScopeProject,
    type WorkScope,
} from './workScope';

export interface WorkScopeValue {
    /** The scope to show. Until iterations load it is the unchecked URL or remembered value. */
    scope: WorkScope | undefined;
    project: ScopeProject | undefined;
    iteration: ScopeIteration | undefined;
    /** True once the scope is checked against the iterations that exist. */
    isReady: boolean;
    /** True on pages that show the scope without setting it. */
    isReadOnly: boolean;
    /** Sets both values; a project without an iteration opens on its default iteration. */
    setScope: (next: { project: ScopeProject; iteration?: ScopeIteration }) => void;
    /** Changes the project and resets the iteration by the default rule. */
    setProject: (project: ScopeProject) => void;
    /** Changes the iteration; the project follows it unless All projects is chosen. */
    setIteration: (iteration: ScopeIteration) => void;
    /** Adds the current scope to a link that opens a scoped page. */
    linkTo: (to: string) => string;
}

/**
 * The current project and iteration. The URL parameters `project` and `iteration` come
 * first, then the scope this browser remembers, then the default rule. Every change is
 * remembered and replaces the URL in place, so Back leaves the page instead of stepping
 * through scope changes.
 */
export const useWorkScope = (): WorkScopeValue => {
    const location = useLocation();
    const navigate = useNavigate();
    const rememberedProject = useScopeStore(state => state.project);
    const rememberedIteration = useScopeStore(state => state.iteration);
    const remember = useScopeStore(state => state.remember);
    // feedback-policy: query loading,error,retry,empty - the scope stays unchecked until iterations load; pages render their own states.
    const { data: iterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    const { pathname, search, hash } = location;
    const urlScope = useMemo(() => parseScope(search), [search]);
    const remembered = useMemo<RememberedScope>(
        () => ({ project: rememberedProject, iteration: rememberedIteration }),
        [rememberedProject, rememberedIteration],
    );
    const writesUrl = isScopedPath(pathname) || hasScopeParams(search);

    const scope = useMemo<WorkScope | undefined>(() => {
        if (iterations) return resolveWorkScope(urlScope, remembered, iterations);
        const candidate: PartialWorkScope = {
            project: urlScope.project ?? remembered.project,
            iteration: urlScope.iteration ?? remembered.iteration,
        };
        return isCompleteScope(candidate) ? candidate : undefined;
    }, [iterations, urlScope, remembered]);

    const commit = useCallback((target: WorkScope) => {
        const { project, iteration } = useScopeStore.getState();
        if (!sameScope({ project, iteration }, target)) remember(target);
        if (writesUrl && !sameScope(parseScope(search), target)) {
            navigate(
                { pathname, search: withScopeSearch(search, target), hash },
                { replace: true, state: location.state },
            );
        }
    }, [hash, location.state, navigate, pathname, remember, search, writesUrl]);

    // Keeps the URL and the remembered scope in step. A new URL wins; a remembered scope that
    // changed while the URL stayed the same (an older control set it) is written to the URL.
    const lastSeen = useRef<{ search: string; remembered: RememberedScope } | null>(null);
    useEffect(() => {
        if (!iterations) return;
        const previous = lastSeen.current;
        lastSeen.current = { search, remembered };
        const rememberedChangedAlone = previous !== null
            && previous.search === search
            && !sameScope(previous.remembered, remembered);
        commit(rememberedChangedAlone
            ? resolveWorkScope(remembered, {}, iterations)
            : resolveWorkScope(urlScope, remembered, iterations));
    }, [commit, iterations, remembered, search, urlScope]);

    const setScope = useCallback<WorkScopeValue['setScope']>((next) => {
        if (!iterations) {
            remember({ project: next.project, iteration: next.iteration ?? null });
            return;
        }
        commit(resolveWorkScope(
            { project: next.project, iteration: next.iteration ?? defaultIterationForProject(iterations, next.project) },
            {},
            iterations,
        ));
    }, [commit, iterations, remember]);

    const setProject = useCallback((project: ScopeProject) => setScope({ project }), [setScope]);

    const setIteration = useCallback((iteration: ScopeIteration) => {
        const current = scope?.project;
        if (!iterations) {
            remember({ project: current ?? null, iteration });
            return;
        }
        const keepsProject = iteration === 'backlog' || current === 'all';
        commit(resolveWorkScope(
            keepsProject ? { project: current, iteration } : { iteration },
            {},
            iterations,
        ));
    }, [commit, iterations, remember, scope?.project]);

    const linkTo = useCallback((to: string) => scopedLink(to, scope), [scope]);

    return {
        scope,
        project: scope?.project ?? urlScope.project ?? remembered.project ?? undefined,
        iteration: scope?.iteration ?? urlScope.iteration ?? remembered.iteration ?? undefined,
        isReady: iterations !== undefined,
        isReadOnly: !isScopedPath(pathname),
        setScope,
        setProject,
        setIteration,
        linkTo,
    };
};
