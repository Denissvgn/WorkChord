import { useTranslation } from 'react-i18next';
import { Button } from '../../components/common/Button';
import { clearAdminApiKey } from '../../utils/adminAccess';

export const OperatorIdentityNotice = () => {
    const { t } = useTranslation();
    return <div className="flex flex-wrap items-center gap-3 rounded-md border border-border p-4 text-sm">
        <p className="min-w-0 flex-1">{t('identity.adminKeyReplacesPerson')}</p>
        <Button size="sm" variant="secondary" onClick={clearAdminApiKey}>{t('identity.lock')}</Button>
    </div>;
};
