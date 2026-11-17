import { Children, forwardRef } from 'react';
import type { ButtonHTMLAttributes } from 'react';
import { Loader2 } from 'lucide-react';
import { buttonClassName, type ButtonSize, type ButtonVariant } from './buttonStyles';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    size?: ButtonSize;
    isLoading?: boolean;
    iconOnly?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({
        className,
        variant,
        size = 'md',
        isLoading = false,
        iconOnly = false,
        disabled,
        children,
        type = 'button',
        'aria-busy': ariaBusy,
        title,
        ...props
    }, ref) => {
        // An icon-only button shows its accessible name as a tooltip for pointer users.
        const hasText = Children.toArray(children).some(child => typeof child === 'string' || typeof child === 'number');
        const inferredVariant = className?.split(/\s+/).find(token => ['primary', 'secondary', 'danger', 'warning', 'ghost', 'plain'].includes(token));
        const effectiveVariant = variant ?? (inferredVariant as ButtonVariant | undefined) ?? 'primary';
        const tooltip = title ?? (!hasText && typeof props['aria-label'] === 'string' ? props['aria-label'] : undefined);
        return (
            <button
                {...props}
                data-page-chrome-control="button"
                title={tooltip}
                ref={ref}
                type={type}
                className={buttonClassName(effectiveVariant, size, `${className ?? ''} ${isLoading || disabled ? 'opacity-70 cursor-not-allowed' : ''}`, iconOnly)}
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
