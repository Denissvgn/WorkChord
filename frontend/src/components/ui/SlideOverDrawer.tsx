import { useId } from 'react';
import type { ReactNode, RefObject } from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';
import { X } from 'lucide-react';
import { twMerge } from 'tailwind-merge';
import { useDialogLayer } from '../common/dialogLayer';

export const SlideOverDrawer = ({
    open,
    title,
    subtitle,
    icon,
    children,
    footer,
    onClose,
    ariaLabel,
    className,
    initialFocusRef,
    restoreFocusRef,
    closeOnBackdropClick = true,
    closeDisabled = false,
    closeLabel: closeLabelProp,
}: {
    open: boolean;
    title: ReactNode;
    subtitle?: ReactNode;
    icon?: ReactNode;
    children: ReactNode;
    footer?: ReactNode;
    onClose: () => void;
    ariaLabel?: string;
    className?: string;
    initialFocusRef?: RefObject<HTMLElement | null>;
    restoreFocusRef?: RefObject<HTMLElement | null>;
    closeOnBackdropClick?: boolean;
    closeDisabled?: boolean;
    closeLabel?: string;
}) => {
    const { t } = useTranslation();
    const titleId = useId();
    const subtitleId = useId();
    const { dialogRef, requestClose } = useDialogLayer<HTMLElement>({
        open,
        onClose,
        initialFocusRef,
        restoreFocusRef,
        closeDisabled,
    });

    if (!open || typeof document === 'undefined') return null;

    const closeLabel = closeLabelProp ?? t('surfaces.slideOver.close');

    return createPortal(
        <div className="wc contents">
            <div className="wc-slide-over-layer fixed inset-0 z-50 flex justify-end">
                {closeOnBackdropClick ? (
                    <button
                        type="button"
                        data-dialog-backdrop
                        tabIndex={-1}
                        aria-hidden="true"
                        disabled={closeDisabled}
                        onClick={requestClose}
                        className="wc-slide-over-backdrop absolute inset-0 cursor-default bg-overlay/35 backdrop-blur-[1px]"
                    />
                ) : (
                    <div
                        data-dialog-backdrop
                        className="wc-slide-over-backdrop absolute inset-0 bg-overlay/35 backdrop-blur-[1px]"
                    />
                )}
                <aside
                    ref={dialogRef}
                    role="dialog"
                    aria-modal="true"
                    aria-label={ariaLabel}
                    aria-labelledby={ariaLabel ? undefined : titleId}
                    aria-describedby={subtitle ? subtitleId : undefined}
                    tabIndex={-1}
                    className={twMerge(
                        'wc-slide-over relative z-10 flex h-screen h-dvh w-full max-w-[480px] flex-col',
                        className,
                    )}
                    style={{ background: 'var(--panel)', borderInlineStart: '1px solid var(--border)' }}
                >
                    <header
                        className="flex min-h-14 items-center gap-3 px-5 py-3"
                        style={{ borderBottom: '1px solid var(--border)' }}
                    >
                        {icon && (
                            <span
                                className="grid h-8 w-8 place-items-center rounded-lg"
                                style={{ background: 'var(--accent-soft)', color: 'var(--accent-ink)' }}
                            >
                                {icon}
                            </span>
                        )}
                        <div className="min-w-0 flex-1">
                            <h2
                                id={titleId}
                                className="wc-slide-over-title text-base font-semibold tracking-tight"
                                style={{ color: 'var(--ink)' }}
                            >
                                {title}
                            </h2>
                            {subtitle && <p id={subtitleId} className="truncate text-xs" style={{ color: 'var(--ink-3)' }}>{subtitle}</p>}
                        </div>
                        <button
                            type="button"
                            onClick={requestClose}
                            aria-label={closeLabel}
                            disabled={closeDisabled}
                            className="btn ghost icon"
                        >
                            <X aria-hidden="true" className="h-4 w-4" />
                        </button>
                    </header>
                    <div className="flex-1 overflow-y-auto">
                        {children}
                    </div>
                    {footer && <footer className="p-4" style={{ borderTop: '1px solid var(--border)' }}>{footer}</footer>}
                </aside>
            </div>
        </div>,
        document.body,
    );
};
