import { forwardRef } from 'react';
import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import type { LinkProps } from 'react-router-dom';
import { buttonClassName, type ButtonSize, type ButtonVariant } from './buttonStyles';

type ButtonLinkProps = Omit<LinkProps, 'className' | 'children'> & {
    variant?: ButtonVariant;
    size?: ButtonSize;
    className?: string;
    children: ReactNode;
};

export const ButtonLink = forwardRef<HTMLAnchorElement, ButtonLinkProps>(
    ({ variant = 'primary', size = 'md', className, children, ...props }, ref) => (
        <Link {...props} ref={ref} data-page-chrome-control="button" className={buttonClassName(variant, size, className)}>{children}</Link>
    ),
);

ButtonLink.displayName = 'ButtonLink';
