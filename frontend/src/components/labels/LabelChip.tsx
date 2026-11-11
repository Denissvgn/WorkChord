import type { ReactNode } from 'react';
import clsx from 'clsx';

/**
 * A label is an attribute, not a state: a neutral chip with the label's own
 * color only as a small swatch, so label colors never read as status or alarm.
 */
export const LabelChip = ({ color, children, size = 'sm' }: { color?: string | null; children: ReactNode; size?: 'sm' | 'md' }) => (
    <span className={clsx('inline-flex items-center gap-1.5 rounded-full border border-border bg-surface-subtle px-2 text-content-primary',
        size === 'md' ? 'py-1 text-sm' : 'py-0.5')}>
        {color && <span aria-hidden="true" className="h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: color }} />}
        {children}
    </span>
);
