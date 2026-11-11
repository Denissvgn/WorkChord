import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { UnsavedLeaveGuard } from '../common/UnsavedLeaveGuard';

/**
 * Says a settings panel has unsaved changes, keeps Save and Discard in reach,
 * and asks before leaving the page or closing the tab.
 */
export const SettingsUnsavedBar = ({ dirty, saving = false, onSave, onDiscard, hint }: {
    dirty: boolean; saving?: boolean; onSave?: () => void; onDiscard?: () => void; hint?: string;
}) => {
    const { t } = useTranslation();
    return <>
        <UnsavedLeaveGuard when={dirty} title={t('settings.unsaved.leaveTitle')} description={t('settings.unsaved.leaveBody')}
            leaveLabel={t('settings.unsaved.leave')} stayLabel={t('settings.unsaved.stay')} closeLabel={t('actions.close')} />
        {dirty && <div role="region" aria-label={t('settings.unsaved.title')}
            className="sticky bottom-0 z-10 flex flex-wrap items-center justify-between gap-3 rounded-md border border-border bg-surface-card px-4 py-3 shadow-lg">
            <p className="text-sm"><strong>{t('settings.unsaved.title')}</strong>{hint && <span className="text-content-secondary"> · {hint}</span>}</p>
            <div className="flex flex-wrap gap-2">
                {onDiscard && <Button type="button" size="sm" variant="secondary" disabled={saving} onClick={onDiscard}>{t('settings.unsaved.discard')}</Button>}
                {onSave && <Button type="button" size="sm" isLoading={saving} disabled={saving} onClick={onSave}>{t('settings.unsaved.save')}</Button>}
            </div>
        </div>}
    </>;
};
