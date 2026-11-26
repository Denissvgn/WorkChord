import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    CheckCircle2,
    Clock3,
    CopyCheck,
    ExternalLink,
    Inbox,
    MessageCircleQuestion,
    Send,
    XCircle
} from 'lucide-react';
import { triageService } from '../../services/triageService';
import type {
    TriageDuplicateSuggestion,
    TriageItem
} from '../../types/triage';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import { sourceLinkHref } from '../../utils/safeUrl';
import { Button } from '../common/Button';
import { RequestSourceLinksPanel } from '../requestSources/RequestSourceLinksPanel';
import { OverflowMenu } from '../ui';
import { StatusPill } from './StatusPill';

import { ClassificationPanel, DuplicateSuggestionsPanel } from './TriageSuggestions';
import { t, type TriageLifecycleAction } from './triageUtils';
interface TriageDetailPanelProps {
    item: TriageItem | null;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    canConvert: boolean;
    onAction: (action: TriageLifecycleAction, item: TriageItem) => void;
    onMarkSuggestion: (item: TriageItem, suggestion: TriageDuplicateSuggestion) => void;
    onConvert: (item: TriageItem) => void;
    onRequestLinksChanged: () => void;
}

export const TriageDetailPanel = ({
    item,
    projectsById,
    iterationsById,
    canConvert,
    onAction,
    onMarkSuggestion,
    onConvert,
    onRequestLinksChanged,
}: TriageDetailPanelProps) => {
    const queryClient = useQueryClient();
    const suggestionItemId = item?.id ?? 0;
    const {
        data: duplicateSuggestions,
        isLoading: isLoadingDuplicateSuggestions,
        isError: isDuplicateSuggestionsError,
        error: duplicateSuggestionsError,
        refetch: refetchDuplicateSuggestions,
    // feedback-policy: query loading,error,retry,empty - suggestion panels show loading, inline retry and empty states.
    } = useQuery({
        queryKey: ['triage', 'duplicate-suggestions', suggestionItemId],
        queryFn: () => triageService.getDuplicateSuggestions(suggestionItemId),
        enabled: suggestionItemId > 0,
    });

    const {
        data: classificationSuggestions,
        isLoading: isLoadingClassification,
        isError: isClassificationError,
        error: classificationError,
        refetch: refetchClassification,
    // feedback-policy: query loading,error,retry,empty - suggestion panels show loading, inline retry and empty states.
    } = useQuery({
        queryKey: ['triage', 'classification-suggestions', suggestionItemId],
        queryFn: () => triageService.getClassificationSuggestions(suggestionItemId),
        enabled: suggestionItemId > 0,
    });

    // feedback-policy: mutation pending,inline - Classify is busy during the request and failures stay in its panel.
    const classifyMutation = useMutation({
        mutationFn: () => triageService.classify(suggestionItemId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['triage', 'classification-suggestions', suggestionItemId] });
        },
    });

    if (!item) {
        return (
            <div className="flex h-full flex-col items-center justify-center rounded-lg border border-border bg-surface-card p-8 text-center text-content-secondary">
                <Inbox className="mb-3 h-8 w-8 text-content-tertiary" />
                <p className="font-medium text-content-primary">{t('surfaces.triagePage.noIntakeSelected')}</p>
                <p className="mt-1 text-sm">{t('surfaces.triagePage.selectAnItemFromTheInbox')}</p>
            </div>
        );
    }

    const convertDisabled = item.status === 'converted' || !canConvert;

    return (
        <aside className="flex h-full flex-col rounded-lg border border-border bg-surface-card" aria-labelledby={`triage-detail-title-${item.id}`}>
            <div className="border-b border-border p-5">
                <div className="mb-3 flex items-start justify-between gap-3">
                    <h2 id={`triage-detail-title-${item.id}`} className="text-lg font-semibold leading-6 text-content-primary">{item.title}</h2>
                    <StatusPill status={item.status} />
                </div>
                <div className="flex flex-wrap gap-2">
                    <Button
                        size="sm"
                        variant="secondary"
                        onClick={() => onConvert(item)}
                        disabled={convertDisabled}
                        title={!canConvert ? t('surfaces.triagePage.convertDisabledTooltip') : undefined}
                    >
                        <Send className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.convert')}
                    </Button>
                    <Button size="sm" variant="secondary" onClick={() => onAction('accept', item)}>
                        <CheckCircle2 className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.accept')}
                    </Button>
                    <OverflowMenu
                        label={t('actions.moreActions')}
                        items={[
                            {
                                label: t('surfaces.triagePage.snooze'),
                                icon: <Clock3 className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onAction('snooze', item),
                            },
                            {
                                label: t('surfaces.triagePage.askForClarification'),
                                icon: <MessageCircleQuestion className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onAction('clarify', item),
                            },
                            {
                                label: t('surfaces.triagePage.markDuplicate'),
                                icon: <CopyCheck className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onAction('duplicate', item),
                            },
                            {
                                label: t('surfaces.triagePage.decline'),
                                icon: <XCircle className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onAction('decline', item),
                                tone: 'danger',
                            },
                        ]}
                    />
                </div>
            </div>

            <div className="flex-1 space-y-5 overflow-y-auto p-5">
                <section>
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.rawIntake')}</h3>
                    <p className="whitespace-pre-wrap rounded-md border border-border bg-surface-muted p-3 text-sm text-content-primary">
                        {item.description || t('surfaces.triagePage.noDescriptionProvided')}
                    </p>
                </section>

                <section className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                    <InfoBlock label={t('surfaces.triagePage.source')} value={item.source || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.externalKey')} value={item.external_key || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.priorityHint')} value={item.priority_hint ? String(item.priority_hint) : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.requests')} value={String(item.request_count ?? 0)} />
                    <InfoBlock label={t('surfaces.triagePage.assigneeHint')} value={item.assignee_hint || '-'} />
                    <InfoBlock label={t('surfaces.triagePage.projectHint')} value={item.project_hint_id ? projectsById[item.project_hint_id] || `#${item.project_hint_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.iterationHint')} value={item.iteration_hint_id ? iterationsById[item.iteration_hint_id] || `#${item.iteration_hint_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.created')} value={formatDateTime(item.created_at)} />
                    <InfoBlock label={t('surfaces.triagePage.updated')} value={formatDateTime(item.updated_at)} />
                </section>

                {item.source_url && (
                    <a
                        href={sourceLinkHref(item.source_url)}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-sm font-medium text-action hover:text-action"
                    >
                        <ExternalLink className="h-4 w-4" />
                        {t('surfaces.triagePage.openSource')}
                    </a>
                )}

                <RequestSourceLinksPanel
                    targetType="triage_item"
                    targetId={item.id}
                    initialCount={item.request_count ?? 0}
                    title={t('surfaces.triagePage.requestSources')}
                    compact
                    onChanged={onRequestLinksChanged}
                />

                <section>
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.labels')}</h3>
                    <div className="flex flex-wrap gap-2">
                        {item.labels.length > 0 ? item.labels.map(label => (
                            <span key={label} className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">{label}</span>
                        )) : (
                            <span className="text-sm text-content-secondary">{t('surfaces.triagePage.noLabels')}</span>
                        )}
                    </div>
                </section>

                <section className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                    <InfoBlock label={t('surfaces.triagePage.snoozedUntil')} value={formatDateTime(item.snoozed_until)} />
                    <InfoBlock label={t('surfaces.triagePage.duplicateOf')} value={item.duplicate_of_id ? `Triage #${item.duplicate_of_id}` : item.duplicate_task_id ? `Task #${item.duplicate_task_id}` : '-'} />
                    <InfoBlock label={t('surfaces.triagePage.convertedTask')} value={item.converted_task_id ? `Task #${item.converted_task_id}` : '-'} />
                </section>

                <DuplicateSuggestionsPanel
                    suggestions={duplicateSuggestions}
                    isLoading={isLoadingDuplicateSuggestions}
                    isError={isDuplicateSuggestionsError}
                    error={duplicateSuggestionsError}
                    onRetry={() => void refetchDuplicateSuggestions()}
                    projectsById={projectsById}
                    iterationsById={iterationsById}
                    onMarkSuggestion={suggestion => onMarkSuggestion(item, suggestion)}
                />

                <ClassificationPanel
                    suggestions={classificationSuggestions}
                    isLoading={isLoadingClassification}
                    isError={isClassificationError}
                    error={classificationError}
                    onRetry={() => void refetchClassification()}
                    onClassify={() => classifyMutation.mutate()}
                    isClassifying={classifyMutation.isPending}
                    classifyError={classifyMutation.isError
                        ? getApiErrorMessage(classifyMutation.error, t('surfaces.triagePage.classificationFailed'))
                        : null}
                />
            </div>
        </aside>
    );
};

export const InfoBlock = ({ label, value }: { label: string; value: string }) => (
    <div className="rounded-md border border-border bg-surface-card p-3">
        <p className="text-xs font-medium uppercase tracking-wide text-content-secondary">{label}</p>
        <p className="mt-1 wrap-break-word text-content-primary">{value}</p>
    </div>
);

