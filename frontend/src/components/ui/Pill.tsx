import type { ReactNode } from 'react';
import clsx from 'clsx';
import type { PillTone } from './tone';
import { wcPillClass } from './tone';

export const Pill = ({
    tone = 'gray',
    icon,
    children,
    className,
}: {
    tone?: PillTone;
    icon?: ReactNode;
    children: ReactNode;
    className?: string;
}) => (
    <span className={clsx('pill', wcPillClass[tone], className)} style={{ maxWidth: '100%' }}>
        {icon}
        <span style={{ minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis' }}>{children}</span>
    </span>
);
