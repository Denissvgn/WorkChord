import { getApiErrorStatus } from '../utils/apiError';
import { useCallback, useEffect, useRef, useState } from 'react';
import { planningInputService, type ObservedPlanningInput, type PlanningInputKind, type MemberPlanningIntent } from '../services/planningInputService';

export const usePlanningObservation = <T,>() => {
    const token = useRef(0);
    const active = useRef(true);
    useEffect(() => { active.current = true; const counter = token; return () => { active.current = false; counter.current++; }; }, []);
    const [observation, setObservation] = useState<ObservedPlanningInput<T> | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<unknown>(null);
    const read = useCallback(async (kind: PlanningInputKind, id: number, retain = false, creatingMember = false, intent?: MemberPlanningIntent) => {
        if (!active.current) return null;
        const current = ++token.current; setLoading(true); setError(null);
        if (!retain) setObservation(null);
        try {
            const value = await planningInputService.readInitial<T>(kind, id, creatingMember, intent);
            if (current !== token.current) return null;
            setObservation(value); return value;
        } catch (cause) { if (current === token.current) { setError(cause); if ([401, 403].includes(getApiErrorStatus(cause) ?? 0)) setObservation(null); } return null; }
        finally { if (current === token.current) setLoading(false); }
    }, []);
    const reset = useCallback(() => { token.current++; if (!active.current) return; setObservation(null); setLoading(false); setError(null); }, []);
    return { observation, loading, error, read, reset };
};
