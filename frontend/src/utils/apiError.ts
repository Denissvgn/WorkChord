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

export const normalizeApiError = (error: unknown, fallback: string): NormalizedApiError => {
    const apiError = asApiError(error);
    const status = normalizedStatus(apiError.response?.status);
    const payload = responsePayload(apiError.response?.data);

    if (payload) {
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

export const getApiErrorStatus = (error: unknown) => (
    normalizedStatus(asApiError(error).response?.status)
);

export const getApiFieldErrors = (error: unknown, fallback: string) => (
    normalizeApiError(error, fallback).fieldErrors
);
