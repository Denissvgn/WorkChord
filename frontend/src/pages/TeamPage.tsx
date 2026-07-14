import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { TeamList } from '../components/team/TeamList';
import { TeamForm } from '../components/team/TeamForm';
import { ImportTeamModal } from '../components/team/ImportTeamModal';
import { TeamProfileManager } from '../components/team/TeamProfileManager';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { iterationService } from '../services/iterationService';
import { teamService } from '../services/teamService';
import { useIterationStore } from '../store/iterationStore';
import { PageHeader, PageLayout } from '../components/ui';
import type { TeamMember, TeamMemberProfile } from '../types/team';

type TeamPageAction = 'assign' | 'import';

const parseTeamPageAction = (value: string | null): TeamPageAction | null => {
    if (value === 'assign' || value === 'import') return value;
    return null;
};

const parseIterationIntent = (value: string | null) => {
    if (!value) return null;
    const parsed = Number(value);
    return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
};

const TeamPage = () => {
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const [searchParams, setSearchParams] = useSearchParams();
    const [isCreating, setIsCreating] = useState(false);
    const [isImporting, setIsImporting] = useState(false);
    const [editingMember, setEditingMember] = useState<TeamMember | null>(null);
    const [assignmentProfile, setAssignmentProfile] = useState<TeamMemberProfile | null>(null);
    const { t } = useTranslation();
    const intentAction = parseTeamPageAction(searchParams.get('action'));
    const intentIterationId = parseIterationIntent(searchParams.get('iterationId'));
    const hasTeamIntent = searchParams.has('action') || searchParams.has('iterationId');

    const {
        data: iterations,
        error: iterationsError,
        isError: isIterationsError,
        isLoading: isLoadingIterations,
        refetch: refetchIterations,
    } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    const hasIterations = (iterations?.length ?? 0) > 0;
    const selectedIteration = iterations?.find(i => i.id === selectedIterationId) ?? null;
    const hasSelectedIteration = hasIterations && selectedIteration !== null;
    const isManagingIterationMember = (isCreating || !!editingMember) && hasSelectedIteration;

    const {
        data: currentIterationMembers = [],
        error: currentMembersError,
        isError: isCurrentMembersError,
        isLoading: isLoadingCurrentMembers,
        refetch: refetchCurrentMembers,
    } = useQuery({
        queryKey: ['team', selectedIterationId],
        queryFn: () => teamService.getByIteration(selectedIterationId),
        enabled: hasSelectedIteration,
    });

    const assignedProfileIds = currentIterationMembers
        .map(m => m.profile_id)
        .filter((id): id is number => id !== null && id !== undefined);
    const canRenderTeamWorkspace = !isLoadingIterations
        && !isIterationsError
        && (!hasSelectedIteration || (!isLoadingCurrentMembers && !isCurrentMembersError));

    useEffect(() => {
        if (!iterations) return;
        if (iterations.length === 0) { if (selectedIterationId !== 0) setSelectedIterationId(0); return; }
        const exists = iterations.some(i => i.id === selectedIterationId);
        if (selectedIterationId === 0 || !exists) setSelectedIterationId(iterations[0].id);
    }, [iterations, selectedIterationId, setSelectedIterationId]);

    useEffect(() => {
        if (!iterations || !hasTeamIntent) return;

        const clearTeamIntent = () => {
            const nextParams = new URLSearchParams(searchParams);
            nextParams.delete('action');
            nextParams.delete('iterationId');
            setSearchParams(nextParams, { replace: true });
        };

        const targetIteration = intentIterationId
            ? iterations.find(iteration => iteration.id === intentIterationId) ?? null
            : null;

        const timeoutId = window.setTimeout(() => {
            if (!intentAction || !targetIteration) {
                setIsCreating(false);
                setIsImporting(false);
                setEditingMember(null);
                setAssignmentProfile(null);
                clearTeamIntent();
                return;
            }

            setSelectedIterationId(targetIteration.id);
            setEditingMember(null);
            setAssignmentProfile(null);

            if (intentAction === 'assign') {
                setIsImporting(false);
                setIsCreating(true);
            } else {
                setIsCreating(false);
                setIsImporting(true);
            }

            clearTeamIntent();
        }, 0);

        return () => window.clearTimeout(timeoutId);
    }, [
        hasTeamIntent,
        intentAction,
        intentIterationId,
        iterations,
        searchParams,
        setSearchParams,
        setSelectedIterationId,
    ]);

    return (
        <PageLayout>
            <PageHeader
                title={t('teamPage.title')}
                subtitle={selectedIteration ? t('teamPage.capacityBelongsTo', {iteration: selectedIteration.name}) : t('teamPage.description')}
                actions={hasIterations && (
                    <>
                        <select className="input" style={{width:'auto'}}
                            value={selectedIterationId}
                            onChange={e => setSelectedIterationId(parseInt(e.target.value))}
                            disabled={isCreating || !!editingMember}>
                            {iterations?.map(it => <option key={it.id} value={it.id}>{it.name}</option>)}
                        </select>
                        <button className="btn" onClick={() => setIsImporting(true)}
                            disabled={isCreating || !!editingMember || selectedIterationId === 0}>
                            ↑ {t('teamPage.importCapacity')}
                        </button>
                        <button className="btn primary"
                            onClick={() => { setAssignmentProfile(null); setIsCreating(true); }}
                            disabled={isCreating || !!editingMember || selectedIterationId === 0}>
                            + {t('teamPage.assignProfile')}
                        </button>
                    </>
                )}
            />

            {isLoadingIterations && (
                <div className="banner">{t('teamPage.loadingCapacity')}</div>
            )}

            {isIterationsError && (
                <QueryErrorState
                    error={iterationsError}
                    fallback={t('queryFeedback.fallback')}
                    onRetry={() => { void refetchIterations(); }}
                />
            )}

            {!isLoadingIterations && !isIterationsError && !hasIterations && (
                <div className="empty">
                    <h4>{t('teamPage.noIterationTitle')}</h4>
                    <p>{t('teamPage.noIterationBody')}</p>
                    <div className="empty-actions">
                        <a href="/iterations" className="btn primary">{t('tasks.goToIterations')}</a>
                    </div>
                </div>
            )}

            {hasSelectedIteration && isLoadingCurrentMembers && (
                <QueryLoadingState message={t('teamPage.loadingCapacity')} />
            )}

            {hasSelectedIteration && isCurrentMembersError && (
                <QueryErrorState
                    error={currentMembersError}
                    fallback={t('queryFeedback.fallback')}
                    onRetry={() => { void refetchCurrentMembers(); }}
                    title={t('teamPage.iterationCapacity')}
                />
            )}

            {canRenderTeamWorkspace && (
                <>
                    {isImporting && hasSelectedIteration && (
                        <ImportTeamModal iterationId={selectedIterationId} onClose={() => setIsImporting(false)}/>
                    )}

                    {isManagingIterationMember ? (
                        <div className="card card-pad" style={{maxWidth:640}}>
                            <h2 style={{margin:'0 0 20px', fontSize:16, fontWeight:600}}>
                                {editingMember ? t('teamPage.editCapacity') : t('teamPage.addProfile')}
                            </h2>
                            <TeamForm
                                iterationId={selectedIterationId}
                                initialData={editingMember ?? undefined}
                                initialProfile={assignmentProfile ?? undefined}
                                onSuccess={() => { setIsCreating(false); setEditingMember(null); setAssignmentProfile(null); }}
                                onCancel={() => { setIsCreating(false); setEditingMember(null); setAssignmentProfile(null); }}
                            />
                        </div>
                    ) : (
                        <>
                            {hasSelectedIteration && (
                                <section style={{display:'flex', flexDirection:'column', gap:12}}>
                                    <div>
                                        <h2 style={{fontSize:15, fontWeight:600, margin:'0 0 4px'}}>{t('teamPage.iterationCapacity')}</h2>
                                    </div>
                                    <TeamList
                                        iterationId={selectedIterationId}
                                        onEdit={member => { setAssignmentProfile(null); setEditingMember(member); }}
                                    />
                                </section>
                            )}
                            <TeamProfileManager
                                currentIterationId={hasSelectedIteration ? selectedIterationId : null}
                                currentIterationName={selectedIteration?.name ?? null}
                                assignedProfileIds={assignedProfileIds}
                                onAssignProfile={hasSelectedIteration
                                    ? profile => { setEditingMember(null); setAssignmentProfile(profile); setIsCreating(true); }
                                    : undefined}
                            />
                        </>
                    )}
                </>
            )}
        </PageLayout>
    );
};

export default TeamPage;
