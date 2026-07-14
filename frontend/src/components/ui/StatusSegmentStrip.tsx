import type { ReactNode } from 'react';
import clsx from 'clsx';
import type { PillTone } from './tone';
import { toneVar } from './tone';

export type StatusSegment = {
    key: string;
    label: ReactNode;
    value: ReactNode;
    tone?: PillTone;
};

export const StatusSegmentStrip = ({
    segments,
    columnsClassName = 'grid-cols-2 md:grid-cols-4',
    className,
}: {
    segments: StatusSegment[];
    columnsClassName?: string;
    className?: string;
}) => (
    <div className={clsx('kpi-grid', columnsClassName, className)}>
        {segments.map((segment) => (
            <div key={segment.key} className="kpi">
                <div className="kpi-lbl" style={{ textTransform: 'uppercase', letterSpacing: '0.04em', fontSize: '10.5px', fontWeight: 600 }}>
                    <span style={{ width: 6, height: 6, borderRadius: '50%', background: toneVar[segment.tone ?? 'gray'], display: 'inline-block' }} />
                    {segment.label}
                </div>
                <p className="tnum" style={{ margin: '4px 0 0', fontSize: 18, fontWeight: 600, color: 'var(--ink)' }}>{segment.value}</p>
            </div>
        ))}
    </div>
);
