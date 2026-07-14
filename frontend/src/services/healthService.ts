import axios from 'axios';

export interface HealthCheckResult {
    state: 'healthy' | 'unhealthy' | 'unavailable';
    statusCode: number | null;
}

const reportsHealthy = (data: unknown) => (
    Boolean(data)
    && typeof data === 'object'
    && !Array.isArray(data)
    && (data as Record<string, unknown>).status === 'ok'
);

export const healthService = {
    check: async (): Promise<HealthCheckResult> => {
        try {
            const response = await axios.get<unknown>('/health', {
                // A reachable non-2xx response is unhealthy, not a network outage.
                validateStatus: () => true,
            });
            const isSuccessful = response.status >= 200 && response.status < 300;
            return {
                state: isSuccessful && reportsHealthy(response.data) ? 'healthy' : 'unhealthy',
                statusCode: response.status,
            };
        } catch {
            // Do not leak transport or host diagnostics to the document surface.
            return { state: 'unavailable', statusCode: null };
        }
    },
};
