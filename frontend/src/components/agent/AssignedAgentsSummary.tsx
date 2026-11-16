import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { agentService } from '../../services/agentService';
import type { AgentAssignmentReadItem } from '../../types/agent';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { QueryEmptyState, QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

const KNOWN_PURPOSES = new Set(['execution', 'verification']);
const KNOWN_STATES = new Set(['queued', 'accepted', 'fulfilled', 'cancelled']);

/** Who holds a task, read with the person's own access: no agent key, no routing evidence. */
export const AssignedAgentsSummary = ({ taskId }: { taskId: number }) => {
    const { t } = useTranslation();
    // feedback-policy: query loading,error,retry,empty
    const assignments = useQuery({
        queryKey: ['agent-assignments', 'person', taskId],
        queryFn: ({ signal }) => agentService.listTaskAssignmentsAsPerson(taskId, signal),
        retry: protectedQueryRetry,
    });
    const name = (row: AgentAssignmentReadItem) => row.actor?.display_name || row.actor?.name
        || t('taskRouting.assignedUnknownActor', { id: row.actor_id });
    return (
        <section className="space-y-2" aria-labelledby={`assigned-agents-${taskId}`}>
            <h4 id={`assigned-agents-${taskId}`} className="text-sm font-semibold text-content-primary">{t('taskRouting.assignedTitle')}</h4>
            {assignments.isPending ? <QueryLoadingState />
                : assignments.isError ? (
                    <QueryErrorState error={assignments.error} fallback={t('taskRouting.assignedLoadFailed')}
                        onRetry={() => { void assignments.refetch(); }} />
                )
                    : assignments.data.length === 0 ? <QueryEmptyState title={t('taskRouting.assignedEmpty')} />
                        : (
                            <ul className="space-y-2">
                                {assignments.data.map(row => (
                                    <li key={row.id} className="text-sm">
                                        <span className="font-medium">{name(row)}</span>
                                        {' · '}
                                        {KNOWN_PURPOSES.has(row.purpose) ? t(`taskRouting.assignedPurpose_${row.purpose}`) : row.purpose}
                                        {' · '}
                                        {KNOWN_STATES.has(row.state) ? t(`taskRouting.assignedState_${row.state}`) : row.state}
                                        {row.model && (
                                            <span className="block text-content-secondary">
                                                {t('taskRouting.assignedModel', { model: row.model.configured_model_alias })}
                                                {row.model_binding_status === 'stale' && <> · {t('taskRouting.assignedModelStale')}</>}
                                            </span>
                                        )}
                                    </li>
                                ))}
                            </ul>
                        )}
        </section>
    );
};
