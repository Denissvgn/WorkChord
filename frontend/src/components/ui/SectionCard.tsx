import type { ReactNode } from 'react';
import clsx from 'clsx';

export const SectionCard = ({
    title,
    headingLevel = 3,
    headingId,
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
    headingLevel?: 2 | 3 | 4;
    headingId?: string;
    description?: ReactNode;
    icon?: ReactNode;
    count?: ReactNode;
    actions?: ReactNode;
    children: ReactNode;
    className?: string;
    bodyClassName?: string;
    testId?: string;
}) => {
    const Heading = `h${headingLevel}` as 'h2' | 'h3' | 'h4';

    return (
        <section
            className={clsx('card', className)}
            data-testid={testId}
            aria-labelledby={title && headingId ? headingId : undefined}
        >
            {(title || actions) && (
                <div className="card-head">
                    {icon}
                    <div style={{ minWidth: 0, flex: 1 }}>
                        {title && <Heading id={headingId}>{title}</Heading>}
                        {description && <p className="sub" style={{ margin: '2px 0 0' }}>{description}</p>}
                    </div>
                    {count}
                    {actions}
                </div>
            )}
            <div className={clsx('card-pad', bodyClassName)}>{children}</div>
        </section>
    );
};
