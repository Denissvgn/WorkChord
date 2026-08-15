import { getRoles } from '@testing-library/dom';
import { computeAccessibleName } from 'dom-accessibility-api';

const UNIQUE_NAME_ROLES = [
    'button',
    'checkbox',
    'combobox',
    'complementary',
    'link',
    'navigation',
    'progressbar',
    'region',
    'textbox',
] as const;

interface AccessibleNameViolation {
    names: string[];
    role: string;
}

export const accessibleNameViolations = (
    container: HTMLElement,
): AccessibleNameViolation[] => {
    const roles = getRoles(container);

    return UNIQUE_NAME_ROLES.flatMap(role => {
        const names = (roles[role] ?? []).map(element => (
            computeAccessibleName(element).trim()
        ));
        const duplicates = names.filter((name, index) => (
            name.length === 0 || names.indexOf(name) !== index
        ));
        return duplicates.length > 0 ? [{ role, names }] : [];
    });
};

export const summaryNameViolations = (container: HTMLElement): string[] => {
    const names = Array.from(container.querySelectorAll('summary')).map(summary => (
        computeAccessibleName(summary).trim()
    ));
    return names.filter((name, index) => (
        name.length === 0 || names.indexOf(name) !== index
    ));
};
