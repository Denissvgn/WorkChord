import { forwardRef } from 'react';
import type { InputHTMLAttributes } from 'react';
import clsx from 'clsx';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className, label, error, ...props }, ref) => {
        const hasLeadingIcon = typeof className === 'string' && /\bpl-(8|9|10|11|12)\b/.test(className);
        return (
            <div className="field w-full">
                {label && (
                    <label className="field-lbl">
                        {label}
                    </label>
                )}
                <input
                    ref={ref}
                    aria-label={label}
                    className={clsx(
                        'input',
                        hasLeadingIcon && 'with-leading-icon',
                        error && 'error',
                        className
                    )}
                    {...props}
                />
                {error && <p className="field-error">{error}</p>}
            </div>
        );
    }
);

Input.displayName = 'Input';
