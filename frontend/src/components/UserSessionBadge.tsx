import { useEffect, useState } from 'react';
import { User, Loader2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { sessionService, type UserSession } from '../services/sessionService';

export const UserSessionBadge = () => {
    const { t } = useTranslation();
    const [session, setSession] = useState<UserSession | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const data = await sessionService.getWhoAmI();
                setSession(data);
            } catch (error) {
                console.error('Failed to fetch session:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSession();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center gap-2 px-3 py-1.5 bg-content-secondary rounded-lg text-sm text-content-emphasis">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>{t('common.loading')}</span>
            </div>
        );
    }

    if (!session) return null;

    return (
        <div
            className="flex items-center gap-2 px-4 py-2 bg-action hover:bg-action-hover rounded-lg text-sm text-content-emphasis shadow-md transition-colors cursor-default"
            title={t('session.guestDiagnostic', { code: session.public_id })}
        >
            <User className="w-4 h-4" />
            <span className="font-semibold">
                {t('session.guestLabel', { code: session.public_id.slice(-6).toUpperCase() })}
            </span>
        </div>
    );
};
