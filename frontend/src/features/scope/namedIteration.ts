import { parseScope } from '../../navigation/scopeParams';

const bareSearch = (search: string) => (search.startsWith('?') ? search.slice(1) : search);

// The URL the shell last completed with the scope because it named no iteration. It is kept
// in memory only, so after a reload or in a copied link every iteration in the URL counts as named.
let completedSearch: string | null = null;

/** The shell records the search it wrote after adding the scope to a URL that named no iteration. */
export const recordCompletedSearch = (search: string) => {
    completedSearch = bareSearch(search);
};

/** The shell forgets the record once the URL has moved on to another search. */
export const forgetCompletedSearchUnless = (search: string) => {
    if (bareSearch(search) !== completedSearch) completedSearch = null;
};

/**
 * True when the URL names the iteration itself: a link, a reload or a scope already chosen.
 * False when it names none, or when the iteration was only added by the shell from the
 * remembered scope or the default rule. Context that is not the scope (a task in the URL, for
 * example) may move the scope only when this is false.
 */
export const urlNamesIteration = (search: string): boolean => (
    parseScope(search).iteration !== undefined && bareSearch(search) !== completedSearch
);
