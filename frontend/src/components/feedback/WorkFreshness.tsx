import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';

/** Display update age and recovery state for a caller-owned work query. */
export const WorkFreshness = ({ updatedAt, stale, refreshing, onRefresh }: {
    updatedAt: number; stale: boolean; refreshing: boolean; onRefresh: () => void;
}) => {
    const { t, i18n } = useTranslation();
    return <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-content-secondary" role="status" aria-live="polite">
        <span>{stale ? t('workFreshness.stale') : updatedAt
            ? t('workFreshness.updated', { time: new Intl.DateTimeFormat(i18n.language, { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(updatedAt) })
            : t('workFreshness.loading')}</span>
        <Button size="sm" variant="ghost" disabled={refreshing} onClick={onRefresh}>{t('workFreshness.refresh')}</Button>
    </div>;
};
