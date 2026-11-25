import {
    ExternalLink
} from 'lucide-react';
import type {
    TriageItem
} from '../../types/triage';
import { formatDateTime } from '../../utils/formatDate';
import { safeExternalHref } from '../../utils/safeUrl';

import { InfoBlock } from './TriageDetailPanel';
import { t } from './triageUtils';
export const TriageConvertSource = ({ item, projectsById, iterationsById }: { item: TriageItem; projectsById: Record<number, string>; iterationsById: Record<number, string> }) => (
    <div className="flex flex-col h-full bg-surface-muted/50 overflow-y-auto p-6 space-y-6">
        <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.rawIntake')}</h3>
            <div className="mt-2 rounded-lg border border-border bg-surface-card p-4 shadow-xs">
                <h4 className="font-semibold text-content-primary text-base mb-2">{item.title}</h4>
                <p className="whitespace-pre-wrap text-sm text-content-primary leading-relaxed">
                    {item.description || t('surfaces.triagePage.noDescriptionProvided')}
                </p>
            </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
            <InfoBlock label={t('surfaces.triagePage.source')} value={item.source || '-'} />
            <InfoBlock label={t('surfaces.triagePage.externalKey')} value={item.external_key || '-'} />
            <InfoBlock label={t('surfaces.triagePage.priorityHint')} value={item.priority_hint ? String(item.priority_hint) : '-'} />
            <InfoBlock label={t('surfaces.triagePage.requests')} value={String(item.request_count ?? 0)} />
            <InfoBlock label={t('surfaces.triagePage.assigneeHint')} value={item.assignee_hint || '-'} />
            <InfoBlock label={t('surfaces.triagePage.projectHint')} value={item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'} />
            <InfoBlock label={t('surfaces.triagePage.iterationHint')} value={item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : '-'} />
            <InfoBlock label={t('surfaces.triagePage.created')} value={formatDateTime(item.created_at)} />
        </div>

        {item.source_url && (
            <div>
                <a
                    href={safeExternalHref(item.source_url)}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-sm font-medium text-action hover:text-action transition-colors"
                >
                    <ExternalLink className="h-4 w-4" />
                    {t('surfaces.triagePage.openSourceLink')}
                </a>
            </div>
        )}

        <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary mb-2">{t('surfaces.triagePage.originalLabels')}</h3>
            <div className="flex flex-wrap gap-2">
                {item.labels.length > 0 ? item.labels.map(label => (
                    <span key={label} className="rounded-full bg-surface-hover/80 px-2.5 py-1 text-xs font-medium text-content-primary">{label}</span>
                )) : (
                    <span className="text-sm text-content-secondary">{t('surfaces.triagePage.noLabels')}</span>
                )}
            </div>
        </div>
    </div>

);
