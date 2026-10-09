import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';

export const LiveWindowStatus = ({ window }: { window: {
    outsideWindow: boolean; headError: boolean; isFetching: boolean; restart: () => Promise<void>;
} }) => {
    const { t } = useTranslation();
    if (!window.outsideWindow) return null;
    return <div role="status" className="flex flex-wrap items-center gap-2 text-sm text-content-secondary">
        <p>{t(window.headError ? 'teamwork.headRefreshFailed' : 'teamwork.retainedWindow')}</p>
        <Button type="button" size="sm" variant="secondary" disabled={window.isFetching} onClick={() => void window.restart()}>{t('teamwork.latestWindow')}</Button>
    </div>;
};
