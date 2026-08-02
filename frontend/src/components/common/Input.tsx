import { forwardRef, useId } from 'react';
import type { InputHTMLAttributes } from 'react';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

export const RequiredIndicator = () => {
    const { t } = useTranslation();

    return <span className="field-required" aria-hidden="true">{t('common.required')}</span>;
};

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({
        className,
        label,
        error,
        id,
        required,
        'aria-describedby': ariaDescribedBy,
        'aria-label': ariaLabel,
        ...props
    }, ref) => {
        const generatedId = useId();
        const inputId = id ?? generatedId;
        const errorId = error ? `${inputId}-error` : undefined;
        const describedBy = [ariaDescribedBy, errorId].filter(Boolean).join(' ') || undefined;
        const hasLeadingIcon = typeof className === 'string' && /\bpl-(8|9|10|11|12)\b/.test(className);
        return (
            <div className="field w-full">
                {label && (
                    <label className="field-lbl" htmlFor={inputId}>
                        {label}
                        {required && <RequiredIndicator />}
                    </label>
                )}
                <input
                    ref={ref}
                    id={inputId}
                    aria-label={ariaLabel ?? label}
                    aria-describedby={describedBy}
                    aria-invalid={Boolean(error)}
                    required={required}
                    className={clsx(
                        'input',
                        hasLeadingIcon && 'with-leading-icon',
                        error && 'error',
                        className
                    )}
                    {...props}
                />
                {error && <p id={errorId} className="field-error" role="alert">{error}</p>}
            </div>
        );
    }
);

Input.displayName = 'Input';
