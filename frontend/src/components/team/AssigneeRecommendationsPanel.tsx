import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { AlertTriangle, CheckCircle2, UserCheck } from 'lucide-react';
import { taskService } from '../../services/taskService';
import { triageService } from '../../services/triageService';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';

interface AssigneeRecommendationsPanelProps {
    targetType: 'task' | 'triage';
    taskId?: number;
    triageItemId?: number;
    iterationId?: number | null;
    selectedAssigneeId?: number | null;
    onSelectAssignee: (teamMemberId: number) => void;
}

export const AssigneeRecommendationsPanel = ({
    targetType,
    taskId,
    triageItemId,
    iterationId,
    selectedAssigneeId,
    onSelectAssignee,
}: AssigneeRecommendationsPanelProps) => {
    const { t } = useTranslation();
    const enabled = targetType === 'task'
        ? Boolean(taskId)
        : Boolean(triageItemId && iterationId);
    const query = useQuery({
        queryKey: [
            'assigneeRecommendations',
            targetType,
            targetType === 'task' ? taskId : triageItemId,
            iterationId ?? null,
        ],
        queryFn: () => targetType === 'task'
            ? taskService.getAssigneeRecommendations(taskId!)
            : triageService.getAssigneeRecommendations(triageItemId!, iterationId ?? null),
        enabled,
        staleTime: 60_000,
    });

    if (!enabled) {
        return null;
    }

    const recommendations = (query.data ?? []).slice(0, 3);

    return (
        <div data-testid="assignee-recommendations" className="rounded-md border border-feedback-info-border bg-feedback-info-muted p-3">
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-feedback-info-foreground">
                <UserCheck className="h-4 w-4 text-feedback-info" />
                {t('assigneeRecommendations.title')}
            </div>

            {query.isLoading && (
                <p className="text-xs text-feedback-info-foreground">{t('assigneeRecommendations.scoring')}</p>
            )}

            {query.isError && (
                <QueryErrorState
                    className="min-h-0 py-3"
                    error={query.error}
                    onRetry={() => void query.refetch()}
                />
            )}

            {!query.isLoading && !query.isError && recommendations.length === 0 && (
                <p className="text-xs text-feedback-info-foreground">{t('assigneeRecommendations.empty')}</p>
            )}

            <div className="space-y-2">
                {recommendations.map(recommendation => {
                    const isSelected = selectedAssigneeId === recommendation.team_member_id;
                    return (
                        <div key={recommendation.team_member_id} className="rounded-md border border-feedback-info-border bg-surface-card p-2">
                            <div className="flex items-start justify-between gap-2">
                                <div className="min-w-0">
                                    <div className="flex flex-wrap items-center gap-2">
                                        <span className="font-medium text-sm text-content-primary">{recommendation.name}</span>
                                        <span className="rounded-full bg-feedback-info-muted-hover px-2 py-0.5 text-xs text-feedback-info-foreground">
                                            {Math.round(recommendation.score)}%
                                        </span>
                                    </div>
                                    <p className="mt-1 text-xs text-content-secondary">{recommendation.rationale}</p>
                                </div>
                                <Button
                                    type="button"
                                    size="sm"
                                    variant={isSelected ? 'secondary' : 'outline'}
                                    onClick={() => onSelectAssignee(recommendation.team_member_id)}
                                >
                                    {isSelected ? (
                                        <CheckCircle2 className="mr-1 h-3.5 w-3.5" />
                                    ) : null}
                                    {isSelected ? t('assigneeRecommendations.selected') : t('assigneeRecommendations.use')}
                                </Button>
                            </div>

                            {(recommendation.matched_skills.length > 0 || recommendation.weakness_matches.length > 0) && (
                                <div className="mt-2 flex flex-wrap gap-1">
                                    {recommendation.matched_skills.slice(0, 4).map(skill => (
                                        <span key={skill} className="rounded-full bg-feedback-success-muted px-2 py-0.5 text-xs text-feedback-success-foreground">
                                            {skill}
                                        </span>
                                    ))}
                                    {recommendation.weakness_matches.slice(0, 3).map(skill => (
                                        <span key={skill} className="inline-flex items-center rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">
                                            <AlertTriangle className="mr-1 h-3 w-3" />
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            )}

                            {recommendation.workload_warnings.length > 0 && (
                                <p className="mt-2 text-xs text-feedback-warning-foreground">
                                    {recommendation.workload_warnings.join(' · ')}
                                </p>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
