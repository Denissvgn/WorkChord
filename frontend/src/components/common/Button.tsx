import { forwardRef } from 'react';
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
        variant = 'primary',
        size = 'md',
        isLoading = false,
        disabled,
        children,
        'aria-busy': ariaBusy,
        ...props
    }, ref) => {
        return (
            <button
                {...props}
                ref={ref}
                className={clsx(
                    'btn',
                    {
                        primary: variant === 'primary',
                        'btn-primary': variant === 'primary',
                        secondary: variant === 'secondary',
                        'btn-secondary': variant === 'secondary',
                        danger: variant === 'danger',
                        'btn-danger': variant === 'danger',
                        warning: variant === 'warning',
                        ghost: variant === 'ghost',
                        'btn-ghost': variant === 'ghost',
                        outline: variant === 'outline',
                        'btn-outline': variant === 'outline',
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
