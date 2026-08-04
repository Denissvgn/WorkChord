export const captureFocusOrigin = (): HTMLElement | null => (
    typeof document !== 'undefined' && document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null
);

export const focusOwnedTarget = (
    origin: HTMLElement | null,
    target: HTMLElement | null,
): boolean => {
    if (!target?.isConnected || typeof document === 'undefined') return false;

    const activeElement = document.activeElement;
    const originReleasedToBody = activeElement === document.body && (
        origin === null
        || !origin.isConnected
        || origin.matches(':disabled')
    );
    if (activeElement !== origin && !originReleasedToBody) return false;

    target.focus();
    return document.activeElement === target;
};
