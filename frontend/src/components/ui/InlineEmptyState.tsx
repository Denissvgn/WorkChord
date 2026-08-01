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
        <div style={{ display: 'flex', minWidth: 0, alignItems: 'flex-start', gap: 12 }}>
            {icon && <span style={{ marginTop: 2, color: 'var(--ink-3)' }}>{icon}</span>}
            <div style={{ minWidth: 0 }}>
                {title && <h3 className="inline-empty-title">{title}</h3>}
                {description && <p className="inline-empty-copy">{description}</p>}
                {children && <div className="inline-empty-copy">{children}</div>}
            </div>
        </div>
        {actions && <div style={{ display: 'flex', flexShrink: 0, flexWrap: 'wrap', gap: 8 }}>{actions}</div>}
    </div>
);
