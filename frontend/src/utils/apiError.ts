import i18n from '../i18n/i18n';
import type { RefusalNextStep } from '../types/task';

export type ApiErrorKind = 'response' | 'network' | 'unknown';

export interface ApiFieldError {
    field: string | null;
    message: string;
}

export interface NormalizedApiError {
    kind: ApiErrorKind;
    status?: number;
    code?: string;
    message: string;
    fieldErrors: ApiFieldError[];
    details?: unknown;
}

interface ApiErrorShape {
    response?: {
        status?: unknown;
        data?: unknown;
    };
    request?: unknown;
    code?: unknown;
}

type UnknownRecord = Record<string, unknown>;

const isRecord = (value: unknown): value is UnknownRecord => (
    Boolean(value) && typeof value === 'object' && !Array.isArray(value)
);

const asApiError = (error: unknown): ApiErrorShape => isRecord(error) ? error : {};

const normalizedStatus = (value: unknown) => (
    typeof value === 'number' && Number.isFinite(value) ? value : undefined
);

const normalizedCode = (value: unknown) => (
    typeof value === 'string' && value.trim() ? value : undefined
);

const normalizedMessage = (value: unknown) => (
    typeof value === 'string' && value.trim() ? value.trim() : null
);

const fieldPath = (value: unknown): string | null => {
    if (typeof value === 'string' && value.trim()) return value.trim();
    if (!Array.isArray(value)) return null;

    const path = value
        .filter(part => part !== 'body' && part !== 'query' && part !== 'path')
        .map(String)
        .filter(Boolean)
        .join('.');
    return path || null;
};

const fieldErrorsFrom = (value: unknown): ApiFieldError[] => {
    if (!Array.isArray(value)) return [];

    return value.flatMap(item => {
        if (typeof item === 'string' && item.trim()) {
            return [{ field: null, message: item.trim() }];
        }
        if (!isRecord(item)) return [];

        const message = normalizedMessage(item.msg) ?? normalizedMessage(item.message);
        if (!message) return [];
        return [{
            field: fieldPath(item.loc) ?? fieldPath(item.field),
            message,
        }];
    });
};

const formatFieldErrors = (fieldErrors: ApiFieldError[]) => (
    fieldErrors
        .map(item => item.field ? `${item.field}: ${item.message}` : item.message)
        .join('; ')
);

const responsePayload = (
    data: unknown,
): Pick<NormalizedApiError, 'code' | 'message' | 'fieldErrors' | 'details'> | null => {
    if (!isRecord(data)) return null;

    // Optional application/domain envelope: { code, message, details }.
    const domainMessage = normalizedMessage(data.message);
    if (domainMessage) {
        return {
            code: normalizedCode(data.code),
            message: domainMessage,
            fieldErrors: fieldErrorsFrom(data.details),
            details: data.details,
        };
    }

    // FastAPI wraps HTTPException and request-validation failures in `detail`.
    const detail = data.detail;
    const stringDetail = normalizedMessage(detail);
    if (stringDetail) {
        return { message: stringDetail, fieldErrors: [] };
    }

    if (Array.isArray(detail)) {
        const fieldErrors = fieldErrorsFrom(detail);
        if (fieldErrors.length > 0) {
            return {
                message: formatFieldErrors(fieldErrors),
                fieldErrors,
                details: detail,
            };
        }
        return null;
    }

    // Structured HTTPException detail, including optimistic-write conflicts.
    if (isRecord(detail)) {
        const message = normalizedMessage(detail.message);
        if (message) {
            return {
                code: normalizedCode(detail.code),
                message,
                fieldErrors: fieldErrorsFrom(detail.details),
                details: detail.details ?? detail,
            };
        }
    }

    return null;
};


const routingInconsistentMessage = (details: unknown) => {
    const check = isRecord(details) && isRecord(details.routing_check) ? details.routing_check : null;
    const issues = Array.isArray(check?.issues) ? check.issues.filter(isRecord) : [];
    const conflicts = issues.filter(issue => issue.severity === 'conflict' && typeof issue.code === 'string')
        .map(issue => i18n.t(`taskReassign.issues.${issue.code}`, { defaultValue: typeof issue.message === 'string' ? issue.message : String(issue.code) }));
    return i18n.t('taskReassign.routingInconsistent', { conflicts: conflicts.join(' ') }).trim();
};

export const normalizeApiError = (error: unknown, fallback: string): NormalizedApiError => {
    const apiError = asApiError(error);
    const status = normalizedStatus(apiError.response?.status);
    const payload = responsePayload(apiError.response?.data);

    if (payload) {
        // The server's refusal of a reviewer conflict is English; say it in the app's language and say where to resolve it.
        if (payload.code === 'routing_inconsistent') return { kind: 'response', status, ...payload, message: routingInconsistentMessage(payload.details) };
        return { kind: 'response', status, ...payload };
    }

    const isNetworkFailure = !apiError.response && (
        apiError.request !== undefined || apiError.code === 'ERR_NETWORK'
    );
    return {
        kind: isNetworkFailure ? 'network' : 'unknown',
        status,
        message: fallback,
        fieldErrors: [],
    };
};

export const getApiErrorMessage = (error: unknown, fallback: string) => (
    normalizeApiError(error, fallback).message
);

/** The next step a refusal names, from its structured envelope; null when it names none. */
export const getApiNextStep = (error: unknown): RefusalNextStep | null => {
    const data = asApiError(error).response?.data;
    const detail = isRecord(data) && isRecord(data.detail) ? data.detail : data;
    const step = isRecord(detail) ? detail.next_step : null;
    if (!isRecord(step) || typeof step.kind !== 'string' || typeof step.message !== 'string' || !step.message.trim()) return null;
    const commands = isRecord(step.commands)
        ? Object.fromEntries(Object.entries(step.commands).filter((entry): entry is [string, string] => typeof entry[1] === 'string'))
        : {};
    return {
        kind: step.kind, message: step.message, commands,
        authority: typeof step.authority === 'string' ? step.authority : '',
        ui_action: step.ui_action === 'record_provenance' || step.ui_action === 'accept_as_owner' ? step.ui_action : null,
    };
};

export const getApiErrorStatus = (error: unknown) => (
    normalizedStatus(asApiError(error).response?.status)
);

export const getApiFieldErrors = (error: unknown, fallback: string) => (
    normalizeApiError(error, fallback).fieldErrors
);
