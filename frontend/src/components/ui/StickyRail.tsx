import type { ReactNode } from 'react';
import clsx from 'clsx';

/** A complementary landmark beside the page content; the label names it for screen readers. */
export const StickyRail = ({
    children,
    className,
    label,
}: {
    children: ReactNode;
    className?: string;
    label: string;
}) => (
    <aside className={clsx('sticky-rail', className)} aria-label={label}>
        {children}
    </aside>
);
