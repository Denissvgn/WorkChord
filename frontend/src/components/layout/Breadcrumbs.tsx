import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';

interface BreadcrumbItem {
    label: string;
    path?: string;  // undefined = current page (no link)
}

interface BreadcrumbsProps {
    items: BreadcrumbItem[];
    label?: string;
}

export const Breadcrumbs = ({ items, label }: BreadcrumbsProps) => {
    const { t } = useTranslation();
    return (
    <nav aria-label={label ?? t('breadcrumbs.navigationLabel')} className="flex items-center gap-2 text-sm text-content-secondary mb-4">
        {items.map((item, index) => (
            <span key={index} className="flex items-center gap-2">
                {index > 0 && <ChevronRight aria-hidden="true" className="h-4 w-4" />}
                {item.path ? (
                    <Link to={item.path} className="hover:text-action transition-colors">
                        {item.label}
                    </Link>
                ) : (
                    <span aria-current="page" className="text-content-primary font-medium">{item.label}</span>
                )}
            </span>
        ))}
    </nav>
    );
};
