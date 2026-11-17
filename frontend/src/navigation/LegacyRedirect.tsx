import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { mapLegacyPath } from './legacyPaths';

export function LegacyRedirect({ children }: { children?: ReactNode }) {
    const { pathname, search, hash } = useLocation();
    const path = pathname.length > 1 ? pathname.replace(/\/$/, '') : pathname;
    const destination = mapLegacyPath(path, search);
    return destination ? <Navigate to={`${destination}${hash}`} replace /> : <>{children}</>;
}
