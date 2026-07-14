import type { ReactNode, RefObject } from 'react';
import clsx from 'clsx';
import { useDialogLayer } from './dialogLayer';

export const FullscreenWorkspace = ({
    open,
    onClose,
    ariaLabel,
    children,
    className,
    fullscreenClassName,
    initialFocusRef,
}: {
    open: boolean;
    onClose: () => void;
    ariaLabel: string;
    children: ReactNode;
    className?: string;
    fullscreenClassName?: string;
    initialFocusRef?: RefObject<HTMLElement | null>;
}) => {
    const { dialogRef } = useDialogLayer<HTMLDivElement>({ open, onClose, initialFocusRef });

    return (
        <div
            ref={dialogRef}
            role={open ? 'dialog' : undefined}
            aria-modal={open ? 'true' : undefined}
            aria-label={open ? ariaLabel : undefined}
            tabIndex={open ? -1 : undefined}
            data-fullscreen-workspace={open ? 'true' : undefined}
            className={clsx(
                open
                    ? 'fixed inset-0 z-50 flex h-screen w-screen flex-col overflow-hidden bg-surface-card'
                    : className,
                open && fullscreenClassName,
            )}
        >
            {children}
        </div>
    );
};
