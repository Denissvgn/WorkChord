import { forwardRef, useId } from 'react';
import type { ReactNode, TextareaHTMLAttributes } from 'react';
import clsx from 'clsx';
import { RequiredIndicator } from './Input';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: ReactNode;
    help?: ReactNode;
    error?: string;
}

/** A textarea with the same label, required, help and error contract as `Input`. */
export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, label, help, error, id, required, 'aria-describedby': ariaDescribedBy, ...props }, ref) => {
        const generatedId = useId();
        const textareaId = id ?? generatedId;
        const helpId = help ? `${textareaId}-help` : undefined;
        const errorId = error ? `${textareaId}-error` : undefined;
        const describedBy = [ariaDescribedBy, helpId, errorId].filter(Boolean).join(' ') || undefined;
        return (
            <div className="field w-full">
                {label && (
                    <label className="field-lbl" htmlFor={textareaId}>
                        {label}
                        {required && <RequiredIndicator />}
                    </label>
                )}
                <textarea ref={ref} id={textareaId} aria-describedby={describedBy} aria-invalid={Boolean(error) || undefined}
                    required={required} className={clsx('input h-auto min-h-24 py-2', error && 'error', className)} {...props} />
                {help && <p id={helpId} className="text-xs text-content-secondary">{help}</p>}
                {error && <p id={errorId} className="field-error" role="alert">{error}</p>}
            </div>
        );
    },
);

Textarea.displayName = 'Textarea';
