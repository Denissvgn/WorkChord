import { useCallback, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { parseScope } from '../../navigation/scopeParams';
import { useScopeStore, type RememberedScope } from './scopeStore';
import { isCompleteScope, scopedLink, type PartialWorkScope } from './workScope';

/** Builds a link to `to`; values in `override` replace those of the current scope. */
export type ScopeLinkBuilder = (to: string, override?: PartialWorkScope) => string;

/** The scope a link carries: the URL first, then the remembered scope. */
export const linkScope = (search: string, remembered: RememberedScope): PartialWorkScope => {
    const fromUrl = parseScope(search);
    return {
        project: fromUrl.project ?? remembered.project,
        iteration: fromUrl.iteration ?? remembered.iteration,
    };
};

const buildLink = (to: string, scope: PartialWorkScope, override?: PartialWorkScope): string => {
    const target: PartialWorkScope = {
        project: override?.project ?? scope.project,
        iteration: override?.iteration ?? scope.iteration,
    };
    return scopedLink(to, isCompleteScope(target) ? target : undefined);
};

/**
 * Builds links that carry the current scope to scoped pages. It reads the URL, then the
 * remembered scope, which useWorkScope keeps checked; it loads nothing itself, so every
 * link the app builds can use it. Links to other pages are returned unchanged.
 */
export const useScopeLink = (): ScopeLinkBuilder => {
    const scope = useLinkScope();
    return useCallback((to, override) => buildLink(to, scope, override), [scope]);
};

/** The scope that links built on this page carry; it can be incomplete before it is known. */
export const useLinkScope = (): PartialWorkScope => {
    const { search } = useLocation();
    const project = useScopeStore(state => state.project);
    const iteration = useScopeStore(state => state.iteration);
    return useMemo(() => linkScope(search, { project, iteration }), [iteration, project, search]);
};

/** The same link outside React, for example in an error boundary: the page URL, then the remembered scope. */
export const scopeLinkNow = (to: string): string => {
    const { project, iteration } = useScopeStore.getState();
    const search = typeof window === 'undefined' ? '' : window.location.search;
    return buildLink(to, linkScope(search, { project, iteration }));
};

