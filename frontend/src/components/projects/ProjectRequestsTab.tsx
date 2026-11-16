import { useTranslation } from 'react-i18next';
import { RequestSourceLinksPanel } from '../requestSources/RequestSourceLinksPanel';
export const ProjectRequestsTab = ({ projectId, count, onChanged }: { projectId: number; count: number; onChanged: () => void }) => {
    const { t } = useTranslation();
    return <RequestSourceLinksPanel targetType="project" targetId={projectId} initialCount={count} title={t('surfaces.projectDetail.projectRequests')} onChanged={onChanged} />;
};
