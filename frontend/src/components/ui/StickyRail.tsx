import type { ReactNode } from 'react';
import clsx from 'clsx';

export const StickyRail = ({
    children,
    className,
}: {
    children: ReactNode;
    className?: string;
}) => (
    <aside className={clsx('sticky-rail', className)}>
        {children}
    </aside>
);
