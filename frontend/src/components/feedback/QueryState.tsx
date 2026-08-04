import { AlertTriangle, Inbox, LoaderCircle, RefreshCw } from 'lucide-react';
import type { Ref } from 'react';
import { useTranslation } from 'react-i18next';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';

interface SharedStateProps {
    className?: string;
}

interface QueryLoadingStateProps extends SharedStateProps {
    message?: string;
}

interface QueryErrorStateProps extends SharedStateProps {
    error?: unknown;
    fallback?: string;
    headingLevel?: 2 | 3;
    isRetrying?: boolean;
    message?: string;
    onRetry?: () => void;
    retryButtonRef?: Ref<HTMLButtonElement>;
    retryLabel?: string;
    title?: string;
}

interface QueryEmptyStateProps extends SharedStateProps {
    title: string;
    description?: string;
}

interface QueryStaleStateProps extends SharedStateProps {
    message: string;
    onRetry: () => void;
}

export const QueryLoadingState = ({ message, className = '' }: QueryLoadingStateProps) => {
    const { t } = useTranslation();
    return (
        <div
            aria-busy="true"
            aria-live="polite"
            className={`flex min-h-24 items-center justify-center gap-2 rounded-lg border border-border bg-surface-card px-4 py-6 text-sm text-content-secondary ${className}`}
            role="status"
        >
            <LoaderCircle aria-hidden="true" className="h-4 w-4 animate-spin text-action" />
            <span>{message ?? t('queryFeedback.loading')}</span>
        </div>
    );
};

export const QueryErrorState = ({
    error,
    fallback,
    headingLevel,
    isRetrying = false,
    message,
    onRetry,
    retryButtonRef,
    retryLabel,
    title,
    className = '',
}: QueryErrorStateProps) => {
    const { t } = useTranslation();
    const safeFallback = fallback ?? t('queryFeedback.fallback');
    const detail = message ?? getApiErrorMessage(error, safeFallback);
    const Heading = headingLevel === 2 ? 'h2' : 'h3';

    return (
        <div
            className={`rounded-lg border border-feedback-danger/40 bg-surface-card px-4 py-4 text-content-primary ${className}`}
            role="alert"
        >
            <div className="flex items-start gap-3">
                <AlertTriangle aria-hidden="true" className="mt-0.5 h-5 w-5 shrink-0 text-feedback-danger" />
                <div className="min-w-0 flex-1">
                    {headingLevel ? (
                        <Heading className="m-0 text-base font-semibold">
                            {title ?? t('queryFeedback.title')}
                        </Heading>
                    ) : (
                        <p className="font-semibold">{title ?? t('queryFeedback.title')}</p>
                    )}
                    <p className="mt-1 break-words text-sm text-content-secondary">{detail}</p>
                    {onRetry && (
                        <Button
                            ref={retryButtonRef}
                            className="mt-3"
                            isLoading={isRetrying}
                            onClick={onRetry}
                            size="sm"
                            variant="secondary"
                        >
                            {!isRetrying && (
                                <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />
                            )}
                            {retryLabel ?? t('queryFeedback.retry')}
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
};

export const QueryEmptyState = ({ title, description, className = '' }: QueryEmptyStateProps) => (
    <div className={`rounded-lg border border-dashed border-border bg-surface-muted px-4 py-8 text-center ${className}`}>
        <Inbox aria-hidden="true" className="mx-auto h-6 w-6 text-content-tertiary" />
        <p className="mt-2 font-medium text-content-primary">{title}</p>
        {description && <p className="mt-1 text-sm text-content-secondary">{description}</p>}
    </div>
);

export const QueryStaleState = ({ message, onRetry, className = '' }: QueryStaleStateProps) => {
    const { t } = useTranslation();
    return (
        <div
            className={`flex flex-wrap items-center justify-between gap-3 rounded-lg border border-feedback-warning-border bg-feedback-warning-muted px-4 py-3 text-sm text-feedback-warning-foreground ${className}`}
            role="status"
        >
            <span className="flex items-center gap-2">
                <AlertTriangle aria-hidden="true" className="h-4 w-4 shrink-0" />
                {message}
            </span>
            <Button onClick={onRetry} size="sm" variant="secondary">
                <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />
                {t('queryFeedback.retry')}
            </Button>
        </div>
    );
};
