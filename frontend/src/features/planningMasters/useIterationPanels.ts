import { useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';

const PANEL_PARAM = 'panel';
const LIST_PANEL = 'iterations';
const CREATE_PARAM = 'create';
const EDIT_PARAM = 'edit';

/**
 * The iteration drawers on Plan live in the link, so Back closes them and a link can open them:
 * `panel=iterations` is the list of iterations, `create=1` the new-iteration form and
 * `edit=<id>` the form of one iteration. The form wins over the list while both are asked for,
 * and the list is there again when the form is closed.
 */
export const useIterationPanels = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const editParam = Number(searchParams.get(EDIT_PARAM));
    const editingId = Number.isInteger(editParam) && editParam > 0 ? editParam : null;
    const creating = searchParams.get(CREATE_PARAM) === '1';
    const listOpen = searchParams.get(PANEL_PARAM) === LIST_PANEL;

    const change = useCallback((apply: (params: URLSearchParams) => void, replace: boolean) => {
        setSearchParams(current => {
            const next = new URLSearchParams(current);
            apply(next);
            return next;
        }, { replace });
    }, [setSearchParams]);

    return {
        listOpen,
        creating,
        editingId,
        openList: useCallback(() => change(params => {
            params.set(PANEL_PARAM, LIST_PANEL);
            params.delete(CREATE_PARAM);
            params.delete(EDIT_PARAM);
        }, false), [change]),
        closeList: useCallback(() => change(params => { params.delete(PANEL_PARAM); }, true), [change]),
        openCreate: useCallback(() => change(params => {
            params.set(CREATE_PARAM, '1');
            params.delete(EDIT_PARAM);
        }, false), [change]),
        openEdit: useCallback((id: number) => change(params => {
            params.set(EDIT_PARAM, String(id));
            params.delete(CREATE_PARAM);
        }, false), [change]),
        closeEditor: useCallback(() => change(params => {
            params.delete(CREATE_PARAM);
            params.delete(EDIT_PARAM);
        }, true), [change]),
    };
};
