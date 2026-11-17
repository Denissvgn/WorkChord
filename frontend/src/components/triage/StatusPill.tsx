import clsx from 'clsx';
import type { TriageItemStatus } from '../../types/triage';
import { statusClassName, statusLabelKeys, t } from './triageUtils';

export const StatusPill = ({ status }: { status: TriageItemStatus }) => (
    <span className={clsx('inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium', statusClassName(status))}>
        {t(statusLabelKeys[status])}
    </span>
);



