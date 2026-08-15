import type { ReactNode } from 'react';
import clsx from 'clsx';

export const InlineEmptyState = ({
    icon,
    title,
    description,
    actions,
    children,
    className,
}: {
    icon?: ReactNode;
    title?: ReactNode;
    description?: ReactNode;
    actions?: ReactNode;
    children?: ReactNode;
    className?: string;
}) => (
    <div className={clsx('inline-empty', className)}>
        <div className="inline-empty-main">
            {icon && <span className="inline-empty-icon">{icon}</span>}
            <div className="inline-empty-content">
                {title && <h3 className="inline-empty-title">{title}</h3>}
                {description && <p className="inline-empty-copy">{description}</p>}
                {children && <div className="inline-empty-copy">{children}</div>}
            </div>
        </div>
        {actions && <div className="inline-empty-actions">{actions}</div>}
    </div>
);
