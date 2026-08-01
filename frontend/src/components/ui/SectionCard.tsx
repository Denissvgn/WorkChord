import type { ReactNode } from 'react';
import clsx from 'clsx';

export const SectionCard = ({
    title,
    description,
    icon,
    count,
    actions,
    children,
    className,
    bodyClassName,
    testId,
}: {
    title?: ReactNode;
    description?: ReactNode;
    icon?: ReactNode;
    count?: ReactNode;
    actions?: ReactNode;
    children: ReactNode;
    className?: string;
    bodyClassName?: string;
    testId?: string;
}) => (
    <section className={clsx('card', className)} data-testid={testId}>
        {(title || actions) && (
            <div className="card-head">
                {icon}
                <div style={{ minWidth: 0, flex: 1 }}>
                    {title && <h3>{title}</h3>}
                    {description && <p className="sub" style={{ margin: '2px 0 0' }}>{description}</p>}
                </div>
                {count}
                {actions}
            </div>
        )}
        <div className={clsx('card-pad', bodyClassName)}>{children}</div>
    </section>
);
