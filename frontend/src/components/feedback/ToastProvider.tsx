import {
    useCallback,
    useEffect,
    useMemo,
    useState,
    type ReactNode,
} from 'react';
import { AlertTriangle, CheckCircle2, Info, X } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { ToastContext, type ToastApi, type ToastInput, type ToastTone } from './toast';

interface ToastRecord extends Required<Pick<ToastInput, 'message' | 'tone' | 'durationMs'>> {
    id: number;
    key: string;
    title?: string;
    actionLabel?: string;
    onAction?: () => void | Promise<void>;
}

let nextToastId = 1;

const toastClasses: Record<ToastTone, string> = {
    success: 'border-feedback-success/40 bg-surface-card text-content-primary',
    error: 'border-feedback-danger/40 bg-surface-card text-content-primary',
    info: 'border-feedback-info/40 bg-surface-card text-content-primary',
};

const toastIcons: Record<ToastTone, typeof Info> = {
    success: CheckCircle2,
    error: AlertTriangle,
    info: Info,
};

const iconClasses: Record<ToastTone, string> = {
    success: 'text-feedback-success',
    error: 'text-feedback-danger',
    info: 'text-feedback-info',
};

const ToastItem = ({ toast, dismiss }: { toast: ToastRecord; dismiss: (id: number) => void }) => {
    const { t } = useTranslation();
    const Icon = toastIcons[toast.tone];
    const [actionPending, setActionPending] = useState(false);

    useEffect(() => {
        if (toast.durationMs <= 0 || actionPending) return undefined;
        const timeout = window.setTimeout(() => dismiss(toast.id), toast.durationMs);
        return () => window.clearTimeout(timeout);
    }, [actionPending, dismiss, toast.durationMs, toast.id]);

    const runAction = async () => {
        if (!toast.onAction || actionPending) return;
        setActionPending(true);
        try {
            await toast.onAction();
            dismiss(toast.id);
        } catch {
            setActionPending(false);
        }
    };

    return (
        <div
            className={`pointer-events-auto flex w-full items-start gap-3 rounded-lg border p-4 shadow-lg ${toastClasses[toast.tone]}`}
            data-toast-tone={toast.tone}
            role="status"
        >
            <Icon aria-hidden="true" className={`mt-0.5 h-5 w-5 shrink-0 ${iconClasses[toast.tone]}`} />
            <div className="min-w-0 flex-1">
                {toast.title && <p className="font-semibold">{toast.title}</p>}
                <p className="break-words text-sm text-content-secondary">{toast.message}</p>
                {toast.actionLabel && toast.onAction && (
                    <Button
                        className="mt-2"
                        disabled={actionPending}
                        onClick={() => { void runAction(); }}
                        size="sm"
                        variant="secondary"
                    >
                        {toast.actionLabel}
                    </Button>
                )}
            </div>
            <Button
                aria-label={t('feedback.dismiss')}
                className="h-8 w-8 shrink-0 p-0"
                onClick={() => dismiss(toast.id)}
                variant="ghost"
            >
                <X aria-hidden="true" className="h-4 w-4" />
            </Button>
        </div>
    );
};

export const ToastProvider = ({ children }: { children: ReactNode }) => {
    const { t } = useTranslation();
    const [toasts, setToasts] = useState<ToastRecord[]>([]);

    const dismiss = useCallback((id: number) => {
        setToasts(current => current.filter(toast => toast.id !== id));
    }, []);

    const showToast = useCallback((input: ToastInput) => {
        const tone = input.tone ?? 'info';
        const key = input.dedupeKey ?? `${tone}:${input.title ?? ''}:${input.message}`;
        const id = nextToastId++;

        setToasts(current => {
            if (current.some(toast => toast.key === key)) return current;
            return [...current, {
                id,
                key,
                message: input.message,
                title: input.title,
                tone,
                durationMs: input.durationMs ?? 5000,
                actionLabel: input.actionLabel,
                onAction: input.onAction,
            }];
        });
        return id;
    }, []);

    const value = useMemo<ToastApi>(() => ({
        showToast,
        success: (message, options) => showToast({ ...options, message, tone: 'success' }),
        error: (message, options) => showToast({ ...options, message, tone: 'error' }),
        info: (message, options) => showToast({ ...options, message, tone: 'info' }),
        dismiss,
    }), [dismiss, showToast]);

    return (
        <ToastContext.Provider value={value}>
            {children}
            <section
                aria-label={t('feedback.notifications')}
                aria-live="polite"
                aria-relevant="additions text"
                className="pointer-events-none fixed inset-x-4 bottom-4 z-[200] ml-auto flex max-w-sm flex-col gap-3 sm:left-auto"
            >
                {toasts.map(toast => <ToastItem key={toast.id} toast={toast} dismiss={dismiss} />)}
            </section>
        </ToastContext.Provider>
    );
};
