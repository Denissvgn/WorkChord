import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
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

export const CapacitySection = ({ iteration, iterations, members, primary }: {
    iteration: Iteration; iterations: Iteration[]; members: TeamMember[]; primary: boolean;
}) => {
    const { t } = useTranslation();
    const client = useQueryClient();
    const [editing, setEditing] = useState<TeamMember | null>(null);
    const [formState, setFormState] = useState({ dirty: false, pending: false });
    const [importing, setImporting] = useState(false);
    const [importingVacations, setImportingVacations] = useState(false);
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
    return <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
            <PlanQuickAddCapacity iteration={iteration} members={members} primary={primary} />
            {previous && <Button variant="secondary" onClick={() => copy.mutate()} disabled={copy.isPending} isLoading={copy.isPending}>{t('capacity.copyPrevious')}</Button>}
            <OverflowMenu className="ml-auto" label={t('capacity.sectionActions')} alwaysMenu items={[
                { label: t('teamPage.importCapacity'), onSelect: () => setImporting(true) },
                { label: t('teamVacations.importCsv'), onSelect: () => setImportingVacations(true) },
            ]} />
        </div>
        {copy.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(copy.error, t('capacity.copyFailed'))}</p>}
        {copy.isSuccess && <p role="status" className="text-sm text-content-secondary">{t('capacity.copied')}</p>}
        {importingVacations && <VacationCsvImport iterationId={iteration.id} onSuccess={() => { setImportingVacations(false); void refreshCapacity(client); }} />}
        <TeamList iterationId={iteration.id} onEdit={setEditing} layout="table" />
        {editing && <SlideOverDrawer open title={t('teamPage.editCapacity')} subtitle={editing.name} closeDisabled={formState.pending} onClose={() => setEditing(null)}>
            <div className="p-5"><TeamForm iterationId={iteration.id} initialData={editing} onStateChange={setFormState}
                onCancel={() => setEditing(null)} onSuccess={() => { setEditing(null); void refreshCapacity(client); }} /></div>
        </SlideOverDrawer>}
        {importing && <ImportTeamModal iterationId={iteration.id} onClose={() => setImporting(false)} onSuccess={() => { setImporting(false); void refreshCapacity(client); }} />}
    </div>;
};
