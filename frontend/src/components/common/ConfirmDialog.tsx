import { useRef } from 'react';
import type { ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';
import clsx from 'clsx';
import { Button } from './Button';
import { Modal } from './Modal';

export type ConfirmDialogTone = 'danger' | 'warning';

export interface ConfirmDialogProps {
    open: boolean;
    title: ReactNode;
    description: ReactNode;
    confirmLabel: string;
    cancelLabel: string;
    closeLabel: string;
    onConfirm: () => void;
    onCancel: () => void;
    tone?: ConfirmDialogTone;
    pending?: boolean;
}

const toneTitleClassName: Record<ConfirmDialogTone, string> = {
    danger: 'text-feedback-danger-foreground',
    warning: 'text-feedback-warning-foreground',
};

/**
 * A deliberately small destructive-action contract layered on the shared
 * accessible Modal. All human-readable copy is supplied by the caller so the
 * component never bypasses the active translation namespace.
 */
export const ConfirmDialog = ({
    open,
    title,
    description,
    confirmLabel,
    cancelLabel,
    closeLabel,
    onConfirm,
    onCancel,
    tone = 'danger',
    pending = false,
}: ConfirmDialogProps) => {
    const cancelButtonRef = useRef<HTMLButtonElement>(null);

    return (
        <Modal
            open={open}
            title={(
                <span className={clsx('flex items-center gap-2', toneTitleClassName[tone])}>
                    <AlertTriangle aria-hidden="true" className="h-5 w-5 shrink-0" />
                    <span>{title}</span>
                </span>
            )}
            description={description}
            footer={(
                <div className="flex justify-end gap-3">
                    <Button
                        ref={cancelButtonRef}
                        type="button"
                        variant="secondary"
                        disabled={pending}
                        onClick={onCancel}
                    >
                        {cancelLabel}
                    </Button>
                    <Button
                        type="button"
                        variant={tone}
                        className={tone === 'warning'
                            ? 'border-feedback-warning bg-feedback-warning text-feedback-warning-emphasis hover:bg-feedback-warning/90'
                            : undefined}
                        isLoading={pending}
                        onClick={onConfirm}
                    >
                        {confirmLabel}
                    </Button>
                </div>
            )}
            onClose={onCancel}
            closeLabel={closeLabel}
            closeDisabled={pending}
            initialFocusRef={pending ? undefined : cancelButtonRef}
            className="max-w-lg"
        />
    );
};
