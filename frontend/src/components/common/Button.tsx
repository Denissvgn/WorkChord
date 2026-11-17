import { Children, forwardRef } from 'react';
import type { ButtonHTMLAttributes } from 'react';
import clsx from 'clsx';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'danger' | 'warning' | 'ghost' | 'outline';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({
        className,
        variant,
        size = 'md',
        isLoading = false,
        disabled,
        children,
        type = 'button',
        'aria-busy': ariaBusy,
        title,
        ...props
    }, ref) => {
        // An icon-only button shows its accessible name as a tooltip for pointer users.
        const hasText = Children.toArray(children).some(child => typeof child === 'string' || typeof child === 'number');
        const inferredVariant = className?.split(/\s+/).find(token => ['primary', 'secondary', 'danger', 'warning', 'ghost'].includes(token));
        const effectiveVariant = variant ?? (inferredVariant as ButtonProps['variant'] | undefined) ?? 'primary';
        const tooltip = title ?? (!hasText && typeof props['aria-label'] === 'string' ? props['aria-label'] : undefined);
        return (
            <button
                {...props}
                data-page-chrome-control="button"
                title={tooltip}
                ref={ref}
                type={type}
                className={clsx(
                    'btn',
                    {
                        primary: effectiveVariant === 'primary',
                        'btn-primary': effectiveVariant === 'primary',
                        secondary: effectiveVariant === 'secondary',
                        'btn-secondary': effectiveVariant === 'secondary',
                        danger: effectiveVariant === 'danger',
                        'btn-danger': effectiveVariant === 'danger',
                        warning: effectiveVariant === 'warning',
                        ghost: effectiveVariant === 'ghost',
                        'btn-ghost': effectiveVariant === 'ghost',
                        'btn-outline': effectiveVariant === 'outline',
                        sm: size === 'sm',
                        lg: size === 'lg',
                        'opacity-70 cursor-not-allowed': isLoading || disabled,
                    },
                    className
                )}
                disabled={isLoading || disabled}
                aria-busy={isLoading ? true : ariaBusy}
            >
                {isLoading && <Loader2 aria-hidden="true" className="h-4 w-4 animate-spin" />}
                {children}
            </button>
        );
    }
);

Button.displayName = 'Button';
