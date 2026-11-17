import { useEffect, useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { usePlanningObservation } from '../../features/usePlanningObservation';
import type { MemberPlanningIntent, ObservedPlanningInput, PlanningInputKind } from '../../services/planningInputService';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

const WATCHED_FIELDS = ['name', 'display_name', 'position', 'start_date', 'end_date', 'status', 'health', 'availability_percent', 'operational_utilization', 'professionalism_coefficient'];

const DRAFT_FIELDS = [...WATCHED_FIELDS, 'calendar_id', 'project_id', 'manager_email'];

export const PlanningInputBoundary = <T,>({ kind, resourceId, creatingMember = false, getIntent, onCancel, draft, children }: {
    /** The record the form was opened with; when given, the conflict prompt shows only if the server's copy differs from it. */
    draft?: object;
    kind: PlanningInputKind; resourceId: number; creatingMember?: boolean;
    onCancel?: () => void;
    getIntent?: () => MemberPlanningIntent;
    /** `reloaded` is true once the person chose to load the server's latest version into the form. */
    children: (observation: ObservedPlanningInput<T>, controls: ReactNode, onSaved: () => void, onConflict: () => void, reloaded: boolean) => ReactNode;
}) => {
    const { t } = useTranslation();
    const context = usePlanningObservation<T>();
    const read = context.read;
    const [generation, setGeneration] = useState(0);
    const [initialIntent] = useState(() => getIntent?.());
    useEffect(() => { void read(kind, resourceId, false, creatingMember, initialIntent); }, [kind, resourceId, creatingMember, read, initialIntent]);
    const [acknowledged, setAcknowledged] = useState<Record<string, unknown> | null>(null);
    const [conflicted, setConflicted] = useState(false);
    const fields = draft ? DRAFT_FIELDS : WATCHED_FIELDS;
    const baseline = acknowledged ?? (draft as Record<string, unknown> | undefined);
    const changedFields = baseline && context.observation
        ? fields.filter(key => {
            const server = (context.observation!.resource as Record<string, unknown>)[key];
            return server !== undefined && String(server ?? '') !== String(baseline[key] ?? '');
        })
        : [];
    const acknowledge = (value: { resource: unknown } | null) => { if (value) { setConflicted(false); if (draft) setAcknowledged(value.resource as Record<string, unknown>); } };
    // A save the server refused as out of date is a conflict even when no shown field differs.
    const showControls = !draft || changedFields.length > 0 || conflicted;
    const controls = !showControls ? null : <div className="space-y-2">
        {draft && <p role="status" className="text-sm">{changedFields.length > 0
            ? t('planningInput.changedFields', { fields: changedFields.map(key => t(`planningInput.fields.${key}`)).join(', ') })
            : t('planningInput.changedElsewhere')}</p>}
        {context.loading && <p role="status">{t('common.loading')}</p>}
        {Boolean(context.error) && <QueryErrorState error={context.error} onRetry={() => void read(kind, resourceId, true, creatingMember, getIntent?.())} />}
        {context.observation && <details className="text-sm">
            <summary>{t('taskEditor.compareCurrent')}</summary>
            <dl className="grid grid-cols-2 gap-2">
                {Object.entries(context.observation.resource as Record<string, unknown>)
                    .filter(([key, value]) => fields.includes(key) && value !== null)
                    .map(([key, value]) => <div key={key}><dt>{t(`planningInput.fields.${key}`)}</dt><dd>{String(value)}</dd></div>)}
            </dl>
        </details>}
        <div className="flex flex-wrap gap-2">
            <Button type="button" size="sm" variant="secondary" disabled={context.loading} onClick={() => {
                void read(kind, resourceId, true, creatingMember, getIntent?.()).then(value => { if (value) { setGeneration(value => value + 1); acknowledge(value); } });
            }}>{t('taskEditor.reload')}</Button>
            <Button type="button" size="sm" variant="secondary" disabled={context.loading}
                onClick={() => void read(kind, resourceId, true, creatingMember, getIntent?.()).then(acknowledge)}>{t('taskEditor.keepDraftWithCurrentVersion')}</Button>
        </div>
    </div>;
    if (!context.observation) return <div className="space-y-3">
        {!context.error ? <QueryLoadingState /> : <QueryErrorState error={context.error} onRetry={() => void read(kind, resourceId, false, creatingMember)} />}
        {onCancel && <Button type="button" variant="ghost" onClick={onCancel}>{t('actions.cancel')}</Button>}
    </div>;
    return <fieldset key={generation} disabled={context.loading} className="m-0 min-w-0 border-0 p-0">
        {children(context.observation, controls, () => { void read(kind, resourceId, true, creatingMember); }, () => { setConflicted(true); void read(kind, resourceId, true, creatingMember, getIntent?.()); }, generation > 0)}
    </fieldset>;
};
