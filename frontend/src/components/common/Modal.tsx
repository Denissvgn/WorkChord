import { useId } from 'react';
import type { ReactNode, RefObject } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import clsx from 'clsx';
import { useDialogLayer } from './dialogLayer';

export interface ModalProps {
    open: boolean;
    title: ReactNode;
    description?: ReactNode;
    children?: ReactNode;
    footer?: ReactNode;
    onClose: () => void;
    closeLabel: string;
    initialFocusRef?: RefObject<HTMLElement | null>;
    closeOnBackdropClick?: boolean;
    closeDisabled?: boolean;
    fullScreen?: boolean;
    className?: string;
    contentClassName?: string;
}

export const Modal = ({
    open,
    title,
    description,
    children,
    footer,
    onClose,
    closeLabel,
    initialFocusRef,
    closeOnBackdropClick = false,
    closeDisabled = false,
    fullScreen = false,
    className,
    contentClassName,
}: ModalProps) => {
    const titleId = useId();
    const descriptionId = useId();
    const hasDescription = description !== undefined && description !== null;
    const { dialogRef, requestClose } = useDialogLayer<HTMLDivElement>({
        open,
        onClose,
        initialFocusRef,
        closeDisabled,
    });

    if (!open || typeof document === 'undefined') return null;

    return createPortal(
        <div className="wc contents">
            <div className={clsx(
                'fixed inset-0 z-50 flex items-center justify-center',
                fullScreen ? 'p-0' : 'p-4',
            )}>
                {closeOnBackdropClick ? (
                    <button
                        type="button"
                        data-dialog-backdrop
                        tabIndex={-1}
                        aria-hidden="true"
                        disabled={closeDisabled}
                        onClick={requestClose}
                        className="absolute inset-0 cursor-default bg-overlay/50"
                    />
                ) : (
                    <div data-dialog-backdrop className="absolute inset-0 bg-overlay/50" />
                )}
                <div
                    ref={dialogRef}
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby={titleId}
                    aria-describedby={hasDescription ? descriptionId : undefined}
                    tabIndex={-1}
                    className={clsx(
                        'relative flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-lg border border-border bg-surface-card shadow-xl',
                        fullScreen && 'h-screen max-h-none max-w-none rounded-none border-0',
                        className,
                    )}
                >
                    <header className="flex items-start gap-4 border-b border-border px-5 py-4">
                        <div className="min-w-0 flex-1">
                            <h2 id={titleId} className="text-lg font-semibold text-content-primary">
                                {title}
                            </h2>
                            {hasDescription && (
                                <div id={descriptionId} className="mt-1 text-sm text-content-secondary">
                                    {description}
                                </div>
                            )}
                        </div>
                        <button
                            type="button"
                            onClick={requestClose}
                            aria-label={closeLabel}
                            disabled={closeDisabled}
                            className="grid h-8 w-8 shrink-0 place-items-center rounded-md bg-transparent p-0 text-content-secondary hover:bg-surface-subtle hover:text-content-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            <X aria-hidden="true" className="h-4 w-4" />
                        </button>
                    </header>
                    {children !== undefined && children !== null && (
                        <div className={clsx('min-h-0 flex-1 overflow-y-auto p-5', contentClassName)}>
                            {children}
                        </div>
                    )}
                    {footer && <footer className="border-t border-border px-5 py-4">{footer}</footer>}
                </div>
            </div>
        </div>,
        document.body,
    );
};
