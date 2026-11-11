import { forwardRef, useId } from 'react';
import type { ReactNode, SelectHTMLAttributes } from 'react';
import clsx from 'clsx';
import { RequiredIndicator } from './Input';

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
    label?: ReactNode;
    help?: ReactNode;
    error?: string;
}

/** A select with the same label, required, help and error contract as `Input`. */
export const Select = forwardRef<HTMLSelectElement, SelectProps>(
    ({ className, label, help, error, id, required, children, 'aria-describedby': ariaDescribedBy, ...props }, ref) => {
        const generatedId = useId();
        const selectId = id ?? generatedId;
        const helpId = help ? `${selectId}-help` : undefined;
        const errorId = error ? `${selectId}-error` : undefined;
        const describedBy = [ariaDescribedBy, helpId, errorId].filter(Boolean).join(' ') || undefined;
        return (
            <div className="field w-full">
                {label && (
                    <label className="field-lbl" htmlFor={selectId}>
                        {label}
                        {required && <RequiredIndicator />}
                    </label>
                )}
                <select ref={ref} id={selectId} aria-describedby={describedBy} aria-invalid={Boolean(error) || undefined}
                    required={required} className={clsx('input', error && 'error', className)} {...props}>
                    {children}
                </select>
                {help && <p id={helpId} className="text-xs text-content-secondary">{help}</p>}
                {error && <p id={errorId} className="field-error" role="alert">{error}</p>}
            </div>
        );
    },
);

Select.displayName = 'Select';
