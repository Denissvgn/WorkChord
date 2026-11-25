import clsx from 'clsx';
import {
    MessageSquare
} from 'lucide-react';
import type {
    TriageItem
} from '../../types/triage';
import { formatDateTime } from '../../utils/formatDate';
import { StatusPill } from './StatusPill';

import { isDueSnoozed, t } from './triageUtils';
interface TriageRowProps {
    item: TriageItem;
    isSelected: boolean;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    onSelect: (id: number) => void;
}

export const TriageRow = ({
    item,
    isSelected,
    projectsById,
    iterationsById,
    onSelect,
}: TriageRowProps) => {
    return (
        <tr
            className={clsx(
                'cursor-pointer border-b border-border-subtle hover:bg-surface-muted',
                isSelected && 'bg-action-muted/70 hover:bg-action-muted'
            )}
            tabIndex={0}
            aria-selected={isSelected}
            onClick={() => onSelect(item.id)}
            onKeyDown={event => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    onSelect(item.id);
                }
            }}
        >
            <td className="px-4 py-3">
                <div className="flex min-w-0 flex-col gap-1">
                    <div className="flex items-center gap-2">
                        <span className="min-w-0 wrap-break-word font-medium text-content-primary">{item.title}</span>
                        {isDueSnoozed(item) && (
                            <span className="rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs font-medium text-feedback-warning-foreground">{t('surfaces.triagePage.due')}</span>
                        )}
                        {(item.request_count ?? 0) > 0 && (
                            <span className="inline-flex items-center gap-1 rounded-full bg-surface-muted px-2 py-0.5 text-xs font-medium text-content-secondary">
                                <MessageSquare className="h-3 w-3" />
                                {item.request_count}
                            </span>
                        )}
                    </div>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-content-secondary">
                        <span>{item.source || 'triage'}{item.external_key ? ` / ${item.external_key}` : ''}</span>
                        {item.snoozed_until && <span>{t('surfaces.triagePage.snoozedAt', { date: formatDateTime(item.snoozed_until) })}</span>}
                    </div>
                </div>
            </td>
            <td className="px-4 py-3">
                <StatusPill status={item.status} />
            </td>
            <td className="px-4 py-3 text-sm text-content-primary">{item.priority_hint || '-'}</td>
            <td className="px-4 py-3">
                <div className="flex max-w-[160px] flex-wrap gap-1">
                    {item.labels.slice(0, 3).map(label => (
                        <span key={label} className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">{label}</span>
                    ))}
                    {item.labels.length > 3 && <span className="text-xs text-content-tertiary">+{item.labels.length - 3}</span>}
                    {item.labels.length === 0 && <span className="text-xs text-content-tertiary">-</span>}
                </div>
            </td>
            <td className="px-4 py-3 text-sm text-content-secondary">
                <div className="max-w-[160px] truncate">
                    {item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'}
                </div>
                <div className="max-w-[160px] truncate text-xs text-content-tertiary">
                    {item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : ''}
                </div>
            </td>
        </tr>
    );
};

