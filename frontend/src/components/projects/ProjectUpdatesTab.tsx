import clsx from 'clsx';
import { useTranslation } from 'react-i18next';
import { TimeEntriesReport } from './TimeEntriesReport';

import {
    Pill,
    SectionCard
} from '../ui';
import type {
    ProjectUpdateEntry
} from '../../types/project';
import { formatDateTime } from '../../utils/formatDate';

import { healthDotClass, healthLabelKeys, healthToTone, updateDetailFields } from './projectDetailShared';

export const ProjectUpdatesTab = ({ projectId, updates: projectUpdates, isLoading: areUpdatesLoading }: {
    projectId: number; updates: ProjectUpdateEntry[]; isLoading: boolean;
}) => {
    const { t } = useTranslation(); return (<div className="space-y-5"><SectionCard title={t('surfaces.projectDetail.updateHistory')} description={t('surfaces.projectDetail.newestFirst')}>
        {areUpdatesLoading ? (
            <div className="py-8 text-center text-sm text-content-secondary">{t('surfaces.projectDetail.loadingUpdates')}</div>
        ) : projectUpdates.length === 0 ? (
            <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">{t('surfaces.projectDetail.noProjectUpdatesYet')}</div>
        ) : (
            <ol className="relative space-y-4 pl-5 before:absolute before:bottom-1 before:left-1.5 before:top-1.5 before:w-px before:bg-surface-hover">
                {projectUpdates.map(update => {
                    const details = updateDetailFields(update);
                    return (
                        <li key={update.id} className="relative">
                            <span className={clsx('absolute -left-[18px] top-1 h-3 w-3 rounded-full ring-4 ring-surface-card', healthDotClass(update.health))} />
                            <div className="flex flex-wrap items-center gap-2">
                                <Pill tone={healthToTone(update.health)} icon={<span className={clsx('h-1.5 w-1.5 rounded-full', healthDotClass(update.health))} />}>
                                    {t(healthLabelKeys[update.health])}
                                </Pill>
                                <span className="text-xs tabular-nums text-content-secondary">{formatDateTime(update.created_at)}</span>
                            </div>
                            <p className="mt-1.5 text-sm font-medium text-content-primary">{update.summary}</p>
                            {details.length > 0 && (
                                <div className="mt-2 grid grid-cols-1 gap-2 text-sm md:grid-cols-2">
                                    {details.map(field => (
                                        <div key={field.label}>
                                            <span className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{field.label}: </span>
                                            <span className="text-content-primary">{field.value}</span>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </li>
                    );
                })}
            </ol>
        )}</SectionCard><TimeEntriesReport projectId={projectId} /></div>);
};
