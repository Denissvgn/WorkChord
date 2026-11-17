import {
    CopyCheck,
    Loader2,
    Sparkles
} from 'lucide-react';
import type {
    TriageClassificationSuggestion,
    TriageDuplicateSuggestion,
    TriageDuplicateSuggestionsResponse
} from '../../types/triage';
import { formatDateTime } from '../../utils/formatDate';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';

import { formatSuggestionScore, t } from './triageUtils';
interface DuplicateSuggestionsPanelProps {
    suggestions?: TriageDuplicateSuggestionsResponse;
    isLoading: boolean;
    isError: boolean;
    error?: unknown;
    onRetry: () => void;
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    onMarkSuggestion: (suggestion: TriageDuplicateSuggestion) => void;
}

export const DuplicateSuggestionsPanel = ({
    suggestions,
    isLoading,
    isError,
    error,
    onRetry,
    projectsById,
    iterationsById,
    onMarkSuggestion,
}: DuplicateSuggestionsPanelProps) => {
    const triageSuggestions = suggestions?.triage_items ?? [];
    const taskSuggestions = suggestions?.tasks ?? [];
    const hasSuggestions = triageSuggestions.length > 0 || taskSuggestions.length > 0;

    return (
        <section className="space-y-3">
            <div className="flex items-center justify-between gap-2">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('surfaces.triagePage.likelyDuplicates')}</h3>
                {isLoading && <Loader2 className="h-4 w-4 animate-spin text-content-tertiary" />}
            </div>

            {isError && (
                <QueryErrorState
                    error={error}
                    fallback={t('surfaces.triagePage.couldNotLoadDuplicateSuggestions')}
                    onRetry={onRetry}
                />
            )}

            {!isLoading && !isError && !hasSuggestions && (
                <div className="rounded-md border border-border bg-surface-muted p-3 text-sm text-content-secondary">
                    {t('surfaces.triagePage.noLikelyDuplicatesFound')}
                </div>
            )}

            <DuplicateSuggestionGroup
                title={t('surfaces.triagePage.triageItems')}
                suggestions={triageSuggestions}
                projectsById={projectsById}
                iterationsById={iterationsById}
                onMarkSuggestion={onMarkSuggestion}
            />
            <DuplicateSuggestionGroup
                title={t('surfaces.triagePage.tasks')}
                suggestions={taskSuggestions}
                projectsById={projectsById}
                iterationsById={iterationsById}
                onMarkSuggestion={onMarkSuggestion}
            />
        </section>
    );
};

interface DuplicateSuggestionGroupProps {
    title: string;
    suggestions: TriageDuplicateSuggestion[];
    projectsById: Record<number, string>;
    iterationsById: Record<number, string>;
    onMarkSuggestion: (suggestion: TriageDuplicateSuggestion) => void;
}

const DuplicateSuggestionGroup = ({
    title,
    suggestions,
    projectsById,
    iterationsById,
    onMarkSuggestion,
}: DuplicateSuggestionGroupProps) => {
    if (suggestions.length === 0) {
        return null;
    }

    return (
        <div className="space-y-2">
            <p className="text-xs font-medium text-content-secondary">{title}</p>
            {suggestions.map(suggestion => {
                const iteration = suggestion.iteration_id ? iterationsById[suggestion.iteration_id] || `Iteration #${suggestion.iteration_id}` : null;
                const project = suggestion.project_id ? projectsById[suggestion.project_id] || `Project #${suggestion.project_id}` : null;
                return (
                    <div key={`${suggestion.target_type}-${suggestion.target_id}`} className="rounded-md border border-border bg-surface-card p-3">
                        <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                                <p className="truncate text-sm font-medium text-content-primary">
                                    #{suggestion.target_id} {suggestion.title}
                                </p>
                                <p className="mt-1 text-xs text-content-secondary">
                                    Score {formatSuggestionScore(suggestion.score)}
                                    {suggestion.status ? ` / ${suggestion.status}` : ''}
                                    {iteration ? ` / ${iteration}` : ''}
                                    {project ? ` / ${project}` : ''}
                                </p>
                            </div>
                            <Button size="sm" variant="outline" onClick={() => onMarkSuggestion(suggestion)}>
                                <CopyCheck className="mr-1 h-4 w-4" />
                                {t('surfaces.triagePage.mark')}
                            </Button>
                        </div>
                        {suggestion.signals.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                                {suggestion.signals.map(signal => (
                                    <span key={signal} className="rounded-full bg-surface-muted px-2 py-0.5 text-xs text-content-secondary">
                                        {signal}
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
};

interface ClassificationPanelProps {
    suggestions?: TriageClassificationSuggestion[];
    isLoading: boolean;
    isError: boolean;
    error?: unknown;
    onRetry: () => void;
    onClassify: () => void;
    isClassifying: boolean;
    classifyError: string | null;
}

export const ClassificationPanel = ({
    suggestions,
    isLoading,
    isError,
    error,
    onRetry,
    onClassify,
    isClassifying,
    classifyError,
}: ClassificationPanelProps) => {
    const latest = suggestions?.[0] ?? null;
    const earlierCount = Math.max(0, (suggestions?.length ?? 0) - 1);

    return (
        <section className="space-y-3">
            <div className="flex items-center justify-between gap-2">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">
                    {t('surfaces.triagePage.classification')}
                </h3>
                <div className="flex items-center gap-2">
                    {isLoading && <Loader2 className="h-4 w-4 animate-spin text-content-tertiary" />}
                    <Button size="sm" variant="secondary" onClick={onClassify} isLoading={isClassifying}>
                        <Sparkles className="mr-1 h-4 w-4" />
                        {t('surfaces.triagePage.classify')}
                    </Button>
                </div>
            </div>

            {classifyError && (
                <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                    {classifyError}
                </div>
            )}

            {isError && (
                <QueryErrorState
                    error={error}
                    fallback={t('surfaces.triagePage.couldNotLoadClassificationSuggestions')}
                    onRetry={onRetry}
                />
            )}

            {!isLoading && !isError && !latest && (
                <div className="rounded-md border border-border bg-surface-muted p-3 text-sm text-content-secondary">
                    {t('surfaces.triagePage.classificationEmpty')}
                </div>
            )}

            {latest && (
                <div className="rounded-md border border-border bg-surface-card p-3">
                    <div className="flex items-start justify-between gap-3">
                        <p className="text-xs text-content-secondary">
                            {t('surfaces.triagePage.classificationConfidence', {
                                percent: Math.round((latest.confidence ?? 0) * 100),
                            })}
                            {' / '}
                            {formatDateTime(latest.created_at)}
                        </p>
                        {latest.is_fallback && (
                            <span className="rounded-full bg-surface-muted px-2 py-0.5 text-xs text-content-secondary">
                                {t('surfaces.triagePage.classificationFallback')}
                            </span>
                        )}
                    </div>

                    <div className="mt-2 flex flex-wrap gap-1">
                        {latest.suggested_type_label_slug && (
                            <span className="rounded-full bg-surface-muted px-2 py-0.5 text-xs text-content-secondary">
                                {t('surfaces.triagePage.classificationType')}: {latest.suggested_type_label_slug}
                            </span>
                        )}
                        {latest.suggested_area_label_slug && (
                            <span className="rounded-full bg-surface-muted px-2 py-0.5 text-xs text-content-secondary">
                                {t('surfaces.triagePage.classificationArea')}: {latest.suggested_area_label_slug}
                            </span>
                        )}
                        {latest.suggested_priority != null && (
                            <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">
                                P{latest.suggested_priority}
                            </span>
                        )}
                        {latest.suggested_label_slugs.map(slug => (
                            <span key={slug} className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">
                                {slug}
                            </span>
                        ))}
                        {latest.unmatched_label_text.map(text => (
                            <span key={text} className="rounded-full border border-dashed border-border px-2 py-0.5 text-xs text-content-tertiary">
                                {text}
                            </span>
                        ))}
                    </div>

                    {latest.suggested_assignee_hint && (
                        <p className="mt-2 text-xs text-content-secondary">
                            {t('surfaces.triagePage.classificationAssigneeHint')}: {latest.suggested_assignee_hint}
                        </p>
                    )}

                    {latest.rationale && (
                        <p className="mt-2 whitespace-pre-wrap text-sm text-content-primary">{latest.rationale}</p>
                    )}

                    {earlierCount > 0 && (
                        <p className="mt-2 text-xs text-content-tertiary">
                            {t('surfaces.triagePage.classificationEarlier', { count: earlierCount })}
                        </p>
                    )}
                </div>
            )}
        </section>
    );
};

