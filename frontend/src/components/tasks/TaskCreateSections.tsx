import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { CollapsibleSection } from '../common/CollapsibleSection';

/** The short create form shared by task capture and request conversion. */
export const TaskCreateSections = ({ title, assignee, effort, brief, assistance, context, more, moreOpen, onMoreOpenChange }: {
    title: ReactNode; assignee: ReactNode; effort: ReactNode; brief: ReactNode;
    assistance?: ReactNode; context?: ReactNode; more: ReactNode;
    moreOpen?: boolean; onMoreOpenChange?: (open: boolean) => void;
}) => {
    const { t } = useTranslation();
    return <>
        {title}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">{assignee}{effort}</div>
        {brief}
        {assistance}
        {context}
        <CollapsibleSection title={t('assigneePicker.more')} open={moreOpen} onOpenChange={onMoreOpenChange}>
            {more}
        </CollapsibleSection>
    </>;
};
