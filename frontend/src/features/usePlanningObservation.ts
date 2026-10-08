import { useCallback, useEffect, useRef, useState } from 'react';
import { planningInputService, type ObservedPlanningInput, type PlanningInputKind } from '../services/planningInputService';

export const usePlanningObservation = <T,>() => {
    const token = useRef(0);
    const active = useRef(true);
    useEffect(() => { active.current = true; return () => { active.current = false; token.current++; }; }, []);
    const [observation, setObservation] = useState<ObservedPlanningInput<T> | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<unknown>(null);
    const read = useCallback(async (kind: PlanningInputKind, id: number, retain = false) => {
        if (!active.current) return null;
        const current = ++token.current; setLoading(true); setError(null);
        if (!retain) setObservation(null);
        try {
            const value = await planningInputService.readInitial<T>(kind, id);
            if (current !== token.current) return null;
            setObservation(value); return value;
        } catch (cause) { if (current === token.current) setError(cause); return null; }
        finally { if (current === token.current) setLoading(false); }
    }, []);
    return { observation, loading, error, read };
};
