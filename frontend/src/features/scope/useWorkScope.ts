import { useCallback, useLayoutEffect, useMemo, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useLocation, useNavigate } from 'react-router-dom';
import { parseScope } from '../../navigation/scopeParams';
import { iterationService } from '../../services/iterationService';
import { useScopeStore, type RememberedScope } from './scopeStore';
import { forgetCompletedSearchUnless, recordCompletedSearch } from './namedIteration';
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
    type ScopeIterationRecord,
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

export type WorkScopeCommands = Pick<WorkScopeValue, 'setScope' | 'setProject' | 'setIteration'>;

const useScopeIterations = () => {
    // feedback-policy: query loading,error,retry,empty - the scope stays unchecked until iterations load; pages render their own states.
    const { data } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });
    return data;
};

/**
 * Writes a scope: it is remembered, and on a scoped page it replaces the URL in place.
 * Shared by useWorkScope and useSetWorkScope so every control applies the same rule.
 */
const useCommitScope = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const remember = useScopeStore(state => state.remember);
    const { pathname, search, hash } = location;
    const writesUrl = isScopedPath(pathname) || hasScopeParams(search);

    /** Returns the search it wrote to the URL, or null when the URL stayed as it was. */
    return useCallback((target: WorkScope): string | null => {
        const { project, iteration } = useScopeStore.getState();
        if (!sameScope({ project, iteration }, target)) remember(target);
        if (!writesUrl || sameScope(parseScope(search), target)) return null;
        const nextSearch = withScopeSearch(search, target);
        navigate(
            { pathname, search: nextSearch, hash },
            { replace: true, state: location.state },
        );
        return nextSearch;
    }, [hash, location.state, navigate, pathname, remember, search, writesUrl]);
};

const useScopeCommands = (
    iterations: readonly ScopeIterationRecord[] | undefined,
    commit: (target: WorkScope) => string | null,
    currentProject: ScopeProject | undefined,
): WorkScopeCommands => {
    const remember = useScopeStore(state => state.remember);

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
        if (!iterations) {
            remember({ project: currentProject ?? null, iteration });
            return;
        }
        const keepsProject = iteration === 'backlog' || currentProject === 'all';
        commit(resolveWorkScope(
            keepsProject ? { project: currentProject, iteration } : { iteration },
            {},
            iterations,
        ));
    }, [commit, currentProject, iterations, remember]);

    return useMemo(() => ({ setScope, setProject, setIteration }), [setIteration, setProject, setScope]);
};

/**
 * The commands of useWorkScope for a control inside a page. They follow the same rules:
 * a new project opens on its default iteration, and the URL is replaced in place. The
 * shell's useWorkScope keeps the URL and the remembered scope in step.
 */
export const useSetWorkScope = (): WorkScopeCommands => {
    const { search } = useLocation();
    const iterations = useScopeIterations();
    const commit = useCommitScope();
    const rememberedProject = useScopeStore(state => state.project);
    const urlProject = useMemo(() => parseScope(search).project, [search]);
    return useScopeCommands(iterations, commit, urlProject ?? rememberedProject ?? undefined);
};

/**
 * The current project and iteration. The URL parameters `project` and `iteration` come
 * first, then the scope this browser remembers, then the default rule. Every change is
 * remembered and replaces the URL in place, so Back leaves the page instead of stepping
 * through scope changes.
 */
export const useWorkScope = (): WorkScopeValue => {
    const { pathname, search } = useLocation();
    const rememberedProject = useScopeStore(state => state.project);
    const rememberedIteration = useScopeStore(state => state.iteration);
    const iterations = useScopeIterations();
    const commit = useCommitScope();

    const urlScope = useMemo(() => parseScope(search), [search]);
    const remembered = useMemo<RememberedScope>(
        () => ({ project: rememberedProject, iteration: rememberedIteration }),
        [rememberedProject, rememberedIteration],
    );

    const scope = useMemo<WorkScope | undefined>(() => {
        if (iterations) return resolveWorkScope(urlScope, remembered, iterations);
        const candidate: PartialWorkScope = {
            project: urlScope.project ?? remembered.project,
            iteration: urlScope.iteration ?? remembered.iteration,
        };
        return isCompleteScope(candidate) ? candidate : undefined;
    }, [iterations, urlScope, remembered]);

    // Keeps the URL and the remembered scope in step. A new URL wins; a remembered scope that
    // changed while the URL stayed the same (an older control set it) is written to the URL.
    // It runs as a layout effect, before the effects of the page below the shell, so a page
    // that changes the iteration on opening changes it after the URL is remembered, not before.
    // Writing the URL can land after other updates, such as the iterations refetching. The search that
    // was replaced stays in `staleSearch` until the URL changes, so the remembered scope keeps winning
    // instead of the old URL undoing it.
    const lastSeen = useRef<{ search: string; remembered: RememberedScope } | null>(null);
    const staleSearch = useRef<string | null>(null);
    useLayoutEffect(() => {
        if (!iterations) return;
        forgetCompletedSearchUnless(search);
        const previous = lastSeen.current;
        lastSeen.current = { search, remembered };
        const rememberedChangedAlone = previous !== null
            && previous.search === search
            && !sameScope(previous.remembered, remembered);
        const rememberedWins = rememberedChangedAlone
            || (previous !== null && previous.search === search && staleSearch.current === search);
        const written = commit(rememberedWins
            ? resolveWorkScope(remembered, {}, iterations)
            : resolveWorkScope(urlScope, remembered, iterations));
        staleSearch.current = rememberedWins && written !== null ? search : null;
        if (written !== null && urlScope.iteration === undefined) recordCompletedSearch(written);
    }, [commit, iterations, remembered, search, urlScope]);

    const { setScope, setProject, setIteration } = useScopeCommands(iterations, commit, scope?.project);

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
