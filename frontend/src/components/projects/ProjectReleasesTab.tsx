import clsx from 'clsx';
import {
    Package,
    Plus
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../common/Button';

import {
    SectionCard
} from '../ui';
import type { Release } from '../../types/release';
import { formatDate } from '../../utils/formatDate';

import { releaseBadgeClassName, releaseStatusLabelKeys, t } from './projectDetailShared';
const ReleaseList = ({
    releases,
    emptyText,
}: {
    releases: Release[];
    emptyText: string;
}) => {
    if(releases.length === 0) {
        return (
            <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                {emptyText}
            </div>
        );
    }

    return (
        <div className="divide-y divide-border-subtle rounded-md border border-border">
            {releases.map(release => (
                <Link
                    key={release.id}
                    to={`/projects/${release.project_id}/releases/${release.id}`}
                    className={clsx(
                        'block px-4 py-3 hover:bg-surface-muted',
                        release.status === 'canceled' && 'bg-surface-muted text-content-secondary'
                    )}
                >
                    <div className="flex flex-wrap items-center justify-between gap-3">
                        <div className="min-w-0">
                            <div className="flex flex-wrap items-center gap-2">
                                <span className="truncate font-medium text-content-primary">{release.name}</span>
                                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', releaseBadgeClassName(release.status))}>
                                    {t(releaseStatusLabelKeys[release.status])}
                                </span>
                                {release.version && (
                                    <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-secondary">
                                        {release.version}
                                    </span>
                                )}
                            </div>
                            <p className="mt-1 text-xs text-content-secondary">
                                {t('surfaces.projectDetail.linkedTaskCount', { count: release.tasks.length })}
                                {' '}· {t('surfaces.projectDetail.targetValue', { date: formatDate(release.target_date) })}
                                {release.shipped_at ? ` · ${t('surfaces.projectDetail.shippedValue', { date: formatDate(release.shipped_at) })}` : ''}
                            </p>
                        </div>
                        <span className="text-xs font-medium text-action">{t('surfaces.projectDetail.open')}</span>
                    </div>
                </Link>
            ))}
        </div>
    );
};

export const ProjectReleasesTab = ({
    releases,
    isLoading,
    onCreate,
}: {
    releases: Release[];
    isLoading: boolean;
    onCreate: () => void;
}) => {
    const upcoming = releases.filter(release => (
        release.status === 'planned' || release.status === 'building'
    ));
    const shipped = releases.filter(release => release.status === 'shipped');
    const canceled = releases.filter(release => release.status === 'canceled');

    return (
        <SectionCard
            icon={<Package className="h-4 w-4 text-action" />}
            title={t('surfaces.projectDetail.releases')}
            count={<span className="rounded-full bg-surface-subtle px-1.5 text-wc-micro font-bold tabular-nums text-content-secondary">{releases.length}</span>}
            actions={(
                <Button size="sm" variant="secondary" onClick={onCreate}>
                    <Plus className="mr-2 h-4 w-4" />
                    {t('surfaces.projectDetail.newRelease')}
                </Button>
            )}
        >
            {isLoading ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.loadingReleases')}
                </div>
            ) : releases.length === 0 ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.noReleasesYet')}
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                    <div>
                        <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.upcoming')}</h3>
                        <ReleaseList releases={upcoming} emptyText={t('surfaces.projectDetail.noUpcomingReleases')} />
                    </div>
                    <div>
                        <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.shipped')}</h3>
                        <ReleaseList releases={shipped} emptyText={t('surfaces.projectDetail.noShippedReleases')} />
                    </div>
                    {canceled.length > 0 && (
                        <div className="lg:col-span-2">
                            <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.canceled')}</h3>
                            <ReleaseList releases={canceled} emptyText={t('surfaces.projectDetail.noCanceledReleases')} />
                        </div>
                    )}
                </div>
            )}
        </SectionCard>
    );
};

