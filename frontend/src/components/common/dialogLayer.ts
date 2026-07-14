import { useCallback, useEffect, useRef } from 'react';
import type { RefObject } from 'react';

const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
].join(',');

const dialogLayerStack: symbol[] = [];
let scrollLockCount = 0;
let previousBodyOverflow = '';

const removeFromStack = (layerId: symbol) => {
    const index = dialogLayerStack.lastIndexOf(layerId);
    if (index >= 0) dialogLayerStack.splice(index, 1);
};

interface DialogLayerOptions {
    open: boolean;
    onClose: () => void;
    initialFocusRef?: RefObject<HTMLElement | null>;
    closeDisabled?: boolean;
}

/**
 * Share modal-layer behavior without coupling a dialog to a visual layout.
 * Centered dialogs and right-side drawers use the same stack so only the
 * topmost layer handles Escape and contains focus.
 */
export const useDialogLayer = <T extends HTMLElement>({
    open,
    onClose,
    initialFocusRef,
    closeDisabled = false,
}: DialogLayerOptions) => {
    const dialogRef = useRef<T>(null);
    const layerIdRef = useRef(Symbol('dialog-layer'));
    const onCloseRef = useRef(onClose);
    const closeDisabledRef = useRef(closeDisabled);

    useEffect(() => {
        onCloseRef.current = onClose;
        closeDisabledRef.current = closeDisabled;
    }, [closeDisabled, onClose]);

    const isTopLayer = useCallback(
        () => dialogLayerStack.at(-1) === layerIdRef.current,
        [],
    );

    const requestClose = useCallback(() => {
        if (isTopLayer() && !closeDisabledRef.current) onCloseRef.current();
    }, [isTopLayer]);

    useEffect(() => {
        if (!open) return;

        const layerId = layerIdRef.current;
        const previouslyFocused = document.activeElement instanceof HTMLElement
            ? document.activeElement
            : null;

        dialogLayerStack.push(layerId);
        if (scrollLockCount === 0) {
            previousBodyOverflow = document.body.style.overflow;
            document.body.style.overflow = 'hidden';
        }
        scrollLockCount += 1;

        const focusableElements = () => (
            Array.from(
                dialogRef.current?.querySelectorAll<HTMLElement>(focusableSelector) ?? [],
            ).filter(element => element.getAttribute('aria-hidden') !== 'true')
        );
        const focusInitialElement = () => {
            const target = initialFocusRef?.current
                ?? focusableElements()[0]
                ?? dialogRef.current;
            target?.focus();
        };

        focusInitialElement();

        const handleKeyDown = (event: KeyboardEvent) => {
            if (!isTopLayer()) return;

            if (event.key === 'Escape') {
                if (!closeDisabledRef.current) {
                    event.preventDefault();
                    onCloseRef.current();
                }
                return;
            }
            if (event.key !== 'Tab') return;

            const elements = focusableElements();
            if (elements.length === 0) {
                event.preventDefault();
                dialogRef.current?.focus();
                return;
            }

            const first = elements[0];
            const last = elements[elements.length - 1];
            const activeElement = document.activeElement;
            if (event.shiftKey && (activeElement === first || !dialogRef.current?.contains(activeElement))) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && (activeElement === last || !dialogRef.current?.contains(activeElement))) {
                event.preventDefault();
                first.focus();
            }
        };

        const handleFocusIn = (event: FocusEvent) => {
            if (!isTopLayer() || dialogRef.current?.contains(event.target as Node)) return;
            focusInitialElement();
        };

        document.addEventListener('keydown', handleKeyDown);
        document.addEventListener('focusin', handleFocusIn);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            document.removeEventListener('focusin', handleFocusIn);
            removeFromStack(layerId);

            scrollLockCount = Math.max(0, scrollLockCount - 1);
            if (scrollLockCount === 0) {
                document.body.style.overflow = previousBodyOverflow;
            }

            if (previouslyFocused?.isConnected) previouslyFocused.focus();
        };
    }, [initialFocusRef, isTopLayer, open]);

    return {
        dialogRef,
        isTopLayer,
        requestClose,
    };
};
