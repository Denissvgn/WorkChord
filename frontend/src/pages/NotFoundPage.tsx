import { Home } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { PageHeader, SectionCard } from '../components/ui';

const NotFoundPage = () => {
    const { t } = useTranslation();
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <div className="space-y-6" data-testid="not-found-page">
            <PageHeader
                title={t('notFound.title')}
                subtitle={t('notFound.description')}
            />
            <SectionCard className="mx-auto max-w-2xl" title={t('notFound.code')}>
                <p className="text-sm text-content-secondary">{t('notFound.requestedPath')}</p>
                <code className="mt-2 block break-all rounded-md border border-border bg-surface-muted px-3 py-2 text-sm text-content-primary">
                    {location.pathname}
                </code>
                <Button className="mt-5" onClick={() => navigate('/')}>
                    <Home aria-hidden="true" className="mr-2 h-4 w-4" />
                    {t('notFound.returnHome')}
                </Button>
            </SectionCard>
        </div>
    );
};

export default NotFoundPage;
