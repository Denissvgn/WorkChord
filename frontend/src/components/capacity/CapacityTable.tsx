import { Bot, User } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { UseQueryResult } from '@tanstack/react-query';
import type { MemberWorkload, TeamMember } from '../../types/team';
import { OverflowMenu } from '../ui/OverflowMenu';
import { QueryErrorState } from '../feedback/QueryState';
import { formatDate } from '../../utils/formatDate';
import { formatDecimal } from '../../utils/workNumbers';

export const CapacityTable = ({ members, workloads, onEdit, onTimeOff, onRemove, removing }: {
    members: TeamMember[]; workloads: UseQueryResult<MemberWorkload>[];
    onEdit: (member: TeamMember) => void; onTimeOff: (id: number) => void;
    onRemove: (member: TeamMember) => void; removing: boolean;
}) => {
    const { t, i18n } = useTranslation();
    return <table className="w-full table-fixed text-left text-sm">
        <caption className="sr-only">{t('teamPage.iterationCapacity')}</caption>
        <thead className="text-xs text-content-secondary">
            <tr className="border-b border-border">
                <th scope="col" className="w-1/4 px-2 py-3">{t('capacity.member')}</th>
                <th scope="col" className="w-1/6 px-2 py-3">{t('capacity.availability')}</th>
                <th scope="col" className="w-1/5 px-2 py-3">{t('capacity.hours')}</th>
                <th scope="col" className="px-2 py-3">{t('capacity.timeOff')}</th>
                <th scope="col" className="w-14 px-2 py-3"><span className="sr-only">{t('actions.moreActions')}</span></th>
            </tr>
        </thead>
        <tbody>
            {members.map((member, index) => {
                const query = workloads[index];
                const agent = member.profile?.profile_kind === 'agent';
                const Icon = agent ? Bot : User;
                return <tr key={member.id} className="border-b border-border align-top">
                    <th scope="row" className="break-words px-2 py-4 font-medium">
                        <span className="flex items-start gap-2">
                            <Icon className="mt-0.5 h-4 w-4 shrink-0 text-content-secondary" aria-label={t(agent ? 'capacity.agent' : 'capacity.person')} />
                            <span>{member.profile?.display_name ?? member.name}</span>
                        </span>
                    </th>
                    <td className="px-2 py-4 tabular-nums">{member.availability_percent}%</td>
                    <td className="px-2 py-4 tabular-nums">
                        {query?.isError ? <QueryErrorState error={query.error} onRetry={() => void query.refetch()} />
                            : query?.data?.capacity_hours !== undefined ? t('capacity.hourValue', { hours: formatDecimal(query.data.capacity_hours, i18n.language) })
                                : <span className="text-content-secondary">{query?.isLoading ? t('common.loading') : t('teamCapacity.capacityUnknown')}</span>}
                    </td>
                    <td className="px-2 py-4 text-content-secondary">
                        {member.vacations.length ? <ul className="space-y-1">
                            {member.vacations.map(vacation => <li key={vacation.id}>{formatDate(vacation.start_date, i18n.language)} – {formatDate(vacation.end_date, i18n.language)}</li>)}
                        </ul> : t('capacity.noTimeOff')}
                    </td>
                    <td className="px-2 py-3">
                        <OverflowMenu label={t('capacity.memberActions', { name: member.name })} items={[
                            { label: t('actions.edit'), onSelect: () => onEdit(member) },
                            { label: t('capacity.timeOff'), onSelect: () => onTimeOff(member.id) },
                            { label: t('capacity.remove'), tone: 'danger', disabled: removing, onSelect: () => onRemove(member) },
                        ]} />
                    </td>
                </tr>;
            })}
        </tbody>
    </table>;
};
