import clsx from 'clsx';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'warning' | 'ghost' | 'outline' | 'plain';
export type ButtonSize = 'sm' | 'md' | 'lg';

export const buttonClassName = (variant: ButtonVariant = 'primary', size: ButtonSize = 'md', className?: string, iconOnly = false) => variant === 'plain' ? clsx(
    'focus-visible:outline-solid focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus',
    className,
) : clsx(
    'btn',
    { primary: variant === 'primary', 'btn-primary': variant === 'primary', secondary: variant === 'secondary', 'btn-secondary': variant === 'secondary', danger: variant === 'danger', 'btn-danger': variant === 'danger', warning: variant === 'warning', ghost: variant === 'ghost', 'btn-ghost': variant === 'ghost', 'btn-outline': variant === 'outline', sm: size === 'sm', lg: size === 'lg', icon: iconOnly },
    className,
);
