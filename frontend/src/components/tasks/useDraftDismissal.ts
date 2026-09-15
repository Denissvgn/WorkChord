import { useCallback, useEffect, useRef, useState } from 'react';

export const useDraftDismissal = (onClose: () => void) => {
    const status = useRef({ dirty: false, pending: false });
    const action = useRef(onClose);
    const cancelAction = useRef<(() => void) | undefined>(undefined);
    const clearDraft = useRef<(() => void) | null>(null);
    const onDiscardReady = useCallback((handler: (() => void) | null) => { clearDraft.current = handler; }, []);
    const close = useRef(onClose);
    useEffect(() => { close.current = onClose; }, [onClose]);
    const [promptOpen, setPromptOpen] = useState(false);
    const [pending, setPendingState] = useState(false);
    const setDirty = useCallback((dirty: boolean) => { status.current.dirty = dirty; }, []);
    const setPending = useCallback((value: boolean) => {
        status.current.pending = value;
        setPendingState(value);
    }, []);
    const request = useCallback((next: () => void, cancel?: () => void) => {
        if (status.current.pending) return;
        if (status.current.dirty) {
            action.current = next;
            cancelAction.current = cancel;
            setPromptOpen(true);
        } else next();
    }, []);
    const cancel = useCallback(() => {
        setPromptOpen(false);
        cancelAction.current?.();
    }, []);
    const requestClose = useCallback(() => request(() => close.current()), [request]);
    const complete = useCallback(() => {
        clearDraft.current?.();
        status.current = { dirty: false, pending: false };
        setPromptOpen(false);
        close.current();
    }, []);
    const discard = useCallback(() => {
        if (status.current.pending) return;
        status.current.dirty = false;
        clearDraft.current?.();
        setPromptOpen(false);
        action.current();
    }, []);
    useEffect(() => {
        const beforeUnload = (event: BeforeUnloadEvent) => {
            if (status.current.dirty || status.current.pending) {
                event.preventDefault();
                event.returnValue = '';
            }
        };
        window.addEventListener('beforeunload', beforeUnload);
        const beforeSignOut = (event: Event) => {
            if (status.current.dirty || status.current.pending) {
                event.preventDefault();
                event.stopImmediatePropagation();
                request((event as CustomEvent<() => void>).detail);
            }
        };
        window.addEventListener('workchord-before-signout', beforeSignOut);
        return () => {
            window.removeEventListener('beforeunload', beforeUnload);
            window.removeEventListener('workchord-before-signout', beforeSignOut);
        };
    }, [request]);
    return { status, setDirty, setPending, onDiscardReady, request, requestClose, complete, discard, cancel, promptOpen, pending };
};
