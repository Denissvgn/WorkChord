import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle2, CircleHelp, RefreshCw } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { healthService } from '../../services/healthService';
import { Button } from '../common/Button';

type VisibleHealthState = 'notChecked' | 'checking' | 'healthy' | 'unhealthy' | 'unavailable';

const stateClasses: Record<VisibleHealthState, string> = {
    notChecked: 'border-border bg-surface-muted text-content-secondary',
    checking: 'border-feedback-info-border bg-feedback-info-muted text-feedback-info-foreground',
    healthy: 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground',
    unhealthy: 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground',
    unavailable: 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground',
};

const stateIcons = {
    notChecked: CircleHelp,
    checking: RefreshCw,
    healthy: CheckCircle2,
    unhealthy: AlertTriangle,
    unavailable: AlertTriangle,
} satisfies Record<VisibleHealthState, typeof CircleHelp>;

export const SystemHealthPanel = () => {
    const { t } = useTranslation();
    const healthQuery = useQuery({
        queryKey: ['system-health'],
        queryFn: healthService.check,
        enabled: false,
        retry: false,
    });

    let state: VisibleHealthState = 'notChecked';
    if (healthQuery.isFetching) state = 'checking';
    else if (healthQuery.isError) state = 'unavailable';
    else if (healthQuery.data?.state === 'healthy') state = 'healthy';
    else if (healthQuery.data?.state === 'unhealthy') state = 'unhealthy';
    else if (healthQuery.data?.state === 'unavailable') state = 'unavailable';

    const Icon = stateIcons[state];
    const hasChecked = healthQuery.isFetched || healthQuery.isError;

    return (
        <div className="space-y-4">
            <p className="text-sm text-content-secondary">{t('healthStatus.description')}</p>
            <div
                aria-atomic="true"
                aria-live="polite"
                className={`flex items-start gap-3 rounded-lg border px-4 py-3 ${stateClasses[state]}`}
                data-health-state={state}
                role={state === 'unhealthy' || state === 'unavailable' ? 'alert' : 'status'}
            >
                <Icon
                    aria-hidden="true"
                    className={`mt-0.5 h-5 w-5 shrink-0 ${state === 'checking' ? 'animate-spin' : ''}`}
                />
                <span>{t(`healthStatus.${state}`)}</span>
            </div>
            <Button
                disabled={healthQuery.isFetching}
                isLoading={healthQuery.isFetching}
                onClick={() => void healthQuery.refetch()}
                variant="secondary"
            >
                {!healthQuery.isFetching && <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />}
                {t(hasChecked ? 'healthStatus.retry' : 'healthStatus.check')}
            </Button>
        </div>
    );
};
