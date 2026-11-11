import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';

/**
 * Recovery for a caller-owned work query: silent while its data is current (the shell
 * says when data may be out of date), and a stale notice with Refresh when a refresh failed.
 */
export const WorkFreshness = ({ stale, refreshing, onRefresh }: {
    updatedAt?: number; stale: boolean; refreshing: boolean; onRefresh: () => void;
}) => {
    const { t } = useTranslation();
    if (!stale) return null;
    return <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-content-secondary" role="status" aria-live="polite">
        <span>{t('workFreshness.stale')}</span>
        <Button size="sm" variant="ghost" disabled={refreshing} onClick={onRefresh}>{t('workFreshness.refresh')}</Button>
    </div>;
};
