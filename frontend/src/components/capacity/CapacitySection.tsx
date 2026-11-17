import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { OverflowMenu } from '../ui/OverflowMenu';
import { VacationCsvImport } from '../team/VacationCsvImport';
import { ImportTeamModal } from '../team/ImportTeamModal';
import { teamService } from '../../services/teamService';
import type { Iteration } from '../../types/iteration';
import type { TeamMember } from '../../types/team';
import { getApiErrorMessage } from '../../utils/apiError';
import { TeamList } from './TeamList';
import { TeamForm } from './TeamForm';
import { PlanQuickAddCapacity } from './PlanQuickAddCapacity';
import { addCapacityRows, refreshCapacity } from './capacityMutations';
import { useIdentity } from '../../features/identity/identityContext';
import { ConnectAgentSteps } from '../team/ConnectAgentSteps';

const CONNECT_PARAM = 'connect';

export const CapacitySection = ({ iteration, iterations, members, primary }: {
    iteration: Iteration; iterations: Iteration[]; members: TeamMember[]; primary: boolean;
}) => {
    const { t } = useTranslation();
    const client = useQueryClient();
    const [editing, setEditing] = useState<TeamMember | null>(null);
    const [formState, setFormState] = useState({ dirty: false, pending: false });
    const [importing, setImporting] = useState(false);
    const [importingVacations, setImportingVacations] = useState(false);
    // The open drawer lives in the address: unlocking editing inside it remounts the page, and the drawer stays open.
    const [searchParams, setSearchParams] = useSearchParams();
    const connecting = searchParams.get(CONNECT_PARAM) === '1';
    const setConnecting = (open: boolean) => setSearchParams(previous => {
        const next = new URLSearchParams(previous);
        if (open) { next.set(CONNECT_PARAM, '1'); next.set('step', 'team'); } else next.delete(CONNECT_PARAM);
        return next;
    }, { replace: true });
    // A connected agent is a new profile: Add capacity offers it once the drawer closes.
    const closeConnect = () => {
        setConnecting(false);
        void client.invalidateQueries({ queryKey: ['teamMemberProfiles'] });
        void refreshCapacity(client);
    };
    const previous = iterations.filter(candidate => candidate.id !== iteration.id
        && (candidate.project_id ?? null) === (iteration.project_id ?? null)
        && candidate.end_date < iteration.start_date)
        .sort((left, right) => right.end_date.localeCompare(left.end_date) || right.id - left.id)[0];
    // feedback-policy: mutation pending,inline
    const copy = useMutation({
        mutationFn: async () => {
            const rows = await teamService.getByIteration(previous!.id);
            await addCapacityRows(iteration.id, rows.map(row => ({
                name: row.name, position: row.position, email: row.email, profile_id: row.profile_id,
                availability_percent: row.availability_percent,
                professionalism_coefficient: row.professionalism_coefficient,
                operational_utilization: row.operational_utilization,
            })));
        },
        onSettled: () => refreshCapacity(client),
    });
    // The profile this session works as can add itself in one step, as a person with full availability.
    const me = useIdentity()?.identity?.profile ?? null;
    const meOnIteration = me !== null && members.some(member => member.profile_id === me.id);
    // feedback-policy: mutation pending,inline
    const addMe = useMutation({
        mutationFn: (profile: { id: number; display_name: string }) => addCapacityRows(iteration.id, [{
            name: profile.display_name,
            position: t('plan.quickCapacity.personRole'),
            profile_id: profile.id,
            availability_percent: 100,
            professionalism_coefficient: 1,
            operational_utilization: 20,
        }]),
        onSettled: () => refreshCapacity(client),
    });
    return <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
            <PlanQuickAddCapacity iteration={iteration} members={members} primary={primary} />
            {me && !meOnIteration && <Button variant="secondary" onClick={() => addMe.mutate(me)} disabled={addMe.isPending} isLoading={addMe.isPending}>{t('identity.addMe')}</Button>}
            <Button variant="secondary" onClick={() => setConnecting(true)}>{t('teamPage.connectAgent')}</Button>
            {previous && <Button variant="secondary" onClick={() => copy.mutate()} disabled={copy.isPending} isLoading={copy.isPending}>{t('capacity.copyPrevious')}</Button>}
            <OverflowMenu className="ml-auto" label={t('capacity.sectionActions')} alwaysMenu items={[
                { label: t('teamPage.importCapacity'), onSelect: () => setImporting(true) },
                { label: t('teamVacations.importCsv'), onSelect: () => setImportingVacations(true) },
            ]} />
        </div>
        {addMe.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(addMe.error, t('plan.quickCapacity.addFailed'))}</p>}
        {copy.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(copy.error, t('capacity.copyFailed'))}</p>}
        {copy.isSuccess && <p role="status" className="text-sm text-content-secondary">{t('capacity.copied')}</p>}
        {importingVacations && <VacationCsvImport iterationId={iteration.id} onSuccess={() => { setImportingVacations(false); void refreshCapacity(client); }} />}
        <TeamList iterationId={iteration.id} onEdit={setEditing} layout="table" />
        {editing && <SlideOverDrawer open title={t('teamPage.editCapacity')} subtitle={editing.name} closeDisabled={formState.pending} onClose={() => setEditing(null)}>
            <div className="p-5"><TeamForm iterationId={iteration.id} initialData={editing} onStateChange={setFormState}
                onCancel={() => setEditing(null)} onSuccess={() => { setEditing(null); void refreshCapacity(client); }} /></div>
        </SlideOverDrawer>}
        {connecting && <SlideOverDrawer open title={t('teamPage.connectAgent')} onClose={closeConnect}>
            <div className="p-5"><ConnectAgentSteps /></div>
        </SlideOverDrawer>}
        {importing && <ImportTeamModal iterationId={iteration.id} onClose={() => setImporting(false)} onSuccess={() => { setImporting(false); void refreshCapacity(client); }} />}
    </div>;
};
