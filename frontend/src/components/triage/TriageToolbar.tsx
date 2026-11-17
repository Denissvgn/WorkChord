import { Search } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Input } from '../common/Input';
import { FilterBar, PageToolbar, ViewSwitch } from '../ui';
import { AGENT_SOURCE_LABEL_KEYS, statusLabelKeys, statusOptions } from './triageUtils';

export const TriageToolbar = ({ search, source, status, label, activeOnly, sources, labels, onSearch, onFilter, onView, onClear }: {
    search: string; source: string; status: string; label: string; activeOnly: boolean; sources: string[]; labels: string[];
    onSearch: (value: string) => void; onFilter: (id: string, value: string) => void;
    onView: (activeOnly: boolean) => void; onClear: () => void;
}) => {
    const { t } = useTranslation();
    return <PageToolbar compact
        search={<div className="relative">
            <Search aria-hidden="true" className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
            <Input value={search} onChange={event => onSearch(event.target.value)} className="pl-9"
                placeholder={t('surfaces.triagePage.searchTitleDescriptionSourceKey')} aria-label={t('surfaces.triagePage.searchIntake')} />
        </div>}
        filters={<FilterBar filters={[
            { id: 'status', label: t('surfaces.triagePage.status'), value: status, options: statusOptions.map(value => ({ value, label: t(statusLabelKeys[value]) })) },
            { id: 'source', label: t('surfaces.triagePage.source'), value: source, options: sources.map(value => ({ value, label: AGENT_SOURCE_LABEL_KEYS[value] ? t(AGENT_SOURCE_LABEL_KEYS[value]) : value })) },
            { id: 'label', label: t('surfaces.triagePage.labels'), value: label, options: labels.map(value => ({ value, label: value })) },
        ]} onChange={onFilter} onClear={onClear} />}
        viewSwitch={<ViewSwitch label={t('surfaces.triagePage.show')} value={activeOnly ? 'waiting' : 'all'}
            options={[{ value: 'waiting', label: t('surfaces.triagePage.waiting') }, { value: 'all', label: t('surfaces.triagePage.all') }]}
            onChange={value => onView(value === 'waiting')} />}
    />;
};
