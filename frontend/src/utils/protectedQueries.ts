import { getApiErrorStatus } from './apiError';

export const protectedQueryRetry = (failureCount: number, error: unknown) => {
    const status = getApiErrorStatus(error);
    if (status === 401 || status === 503) return false;
    return failureCount < 3;
};
