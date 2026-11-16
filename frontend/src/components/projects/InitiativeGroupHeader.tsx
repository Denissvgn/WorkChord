import clsx from 'clsx';
import { useId } from 'react';
import { useTranslation } from 'react-i18next';
import { Pencil } from 'lucide-react';
import { Button } from '../common/Button';
import { OverflowMenu } from '../ui';
import { formatDate } from '../../utils/formatDate';
import { formatPortfolioOwnerLabel } from '../../utils/teamMemberLabels';
import type { ProjectHealth } from '../../types/project';
import type { InitiativeGroupInfo } from './projectPortfolio';
import { projectHealthBadgeClassName } from './projectStatusStyles';

const healthLabelKeys: Record<ProjectHealth, string> = {
    unknown: 'surfaces.projectsPage.unknown',
    on_track: 'surfaces.projectsPage.onTrack',
    at_risk: 'surfaces.projectsPage.atRisk',
    off_track: 'surfaces.projectsPage.offTrack',
};

/**
 * The header row of one initiative group: its name, owner, health and target
 * date, with Edit at hand. Projects without an initiative get a plain
 * "No initiative" header without actions.
 */
export const InitiativeGroupHeader = ({
    initiative,
    projectCount,
    headingLevel,
    headingId,
    onEdit,
    onDelete,
    className,
}: {
    initiative: InitiativeGroupInfo | null;
    projectCount: number;
    /** A heading in the roadmap rail; plain text inside a table header cell. */
    headingLevel?: 3;
    headingId?: string;
    onEdit?: () => void;
    onDelete?: () => void;
    className?: string;
}) => {
    const { t } = useTranslation();
    const generatedId = useId();
    const nameId = headingId ?? generatedId;
    const name = initiative ? initiative.name : t('surfaces.projectsPage.noInitiative');
    const Name = headingLevel === 3 ? 'h3' : 'span';
    const ownerText = initiative
        ? t('surfaces.projectsPage.ownerValue', {
            value: formatPortfolioOwnerLabel(initiative.owner_profile, initiative.owner, initiative.owner_id, t('surfaces.projectsPage.noOwner')),
        })
        : '';

    return (
        <div className={clsx('projects-group-header', className)}>
            <div className="projects-group-copy">
                <div className="projects-group-title">
                    <Name id={nameId} className="projects-group-name">{name}</Name>
                    {initiative && (
                        <span className={clsx('rounded-full border px-2 py-0.5 text-wc-micro font-medium', projectHealthBadgeClassName(initiative.health))}>
                            {t('surfaces.projectsPage.healthSignal', { value: t(healthLabelKeys[initiative.health]) })}
                        </span>
                    )}
                </div>
                <p className="projects-group-meta">
                    {initiative ? (
                        <>
                            <span title={ownerText}>{ownerText}</span>
                            <span>{t('surfaces.projectsPage.targetValue', { value: formatDate(initiative.target_date) })}</span>
                        </>
                    ) : (
                        <span>{t('surfaces.projectsPage.noInitiativeDescription')}</span>
                    )}
                    <span>{t('surfaces.projectsPage.initiativeProjectCount', { count: projectCount })}</span>
                </p>
            </div>
            {initiative && (onEdit || onDelete) && (
                <div className="projects-group-actions">
                    {onEdit && (
                        <Button variant="ghost" size="sm" onClick={onEdit}
                            aria-label={t('surfaces.projectsPage.editInitiativeNamed', { name: initiative.name })}>
                            <Pencil aria-hidden="true" className="h-3.5 w-3.5" />
                            {t('surfaces.projectsPage.edit')}
                        </Button>
                    )}
                    {onDelete && (
                        <OverflowMenu
                            label={t('surfaces.projectsPage.initiativeActions', { name: initiative.name })}
                            alwaysMenu
                            items={[{ label: t('surfaces.projectsPage.delete'), tone: 'danger', onSelect: onDelete }]}
                        />
                    )}
                </div>
            )}
        </div>
    );
};
