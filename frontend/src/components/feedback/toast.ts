import { createContext, useContext } from 'react';

export type ToastTone = 'success' | 'error' | 'info';

export interface ToastInput {
    message: string;
    title?: string;
    tone?: ToastTone;
    dedupeKey?: string;
    durationMs?: number;
}

export type ToneToastOptions = Omit<ToastInput, 'message' | 'tone'>;

export interface ToastApi {
    showToast: (input: ToastInput) => number;
    success: (message: string, options?: ToneToastOptions) => number;
    error: (message: string, options?: ToneToastOptions) => number;
    info: (message: string, options?: ToneToastOptions) => number;
    dismiss: (id: number) => void;
}

export const ToastContext = createContext<ToastApi | null>(null);

export const useToast = () => {
    const context = useContext(ToastContext);
    if (!context) throw new Error('useToast must be used within ToastProvider');
    return context;
};
