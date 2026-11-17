import type { ReactNode } from 'react';
import clsx from 'clsx';

export const InlineEmptyState = ({
    icon,
    title,
    description,
    actions,
    children,
    className,
    headingLevel = 3,
}: {
    icon?: ReactNode;
    title?: ReactNode;
    description?: ReactNode;
    actions?: ReactNode;
    children?: ReactNode;
    className?: string;
    /** The level of the title heading: 2 under a page heading that has no section yet. */
    headingLevel?: 2 | 3;
}) => {
    const Heading = headingLevel === 2 ? 'h2' : 'h3';
    return (
        <div className={clsx('inline-empty', className)}>
            <div className="inline-empty-main">
                {icon && <span className="inline-empty-icon">{icon}</span>}
                <div className="inline-empty-content">
                    {title && <Heading className="inline-empty-title">{title}</Heading>}
                    {description && <p className="inline-empty-copy">{description}</p>}
                    {children && <div className="inline-empty-copy">{children}</div>}
                </div>
            </div>
            {actions && <div className="inline-empty-actions">{actions}</div>}
        </div>
    );
};
