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
        const elements = roles[role] ?? [];
        const names = elements.map(element => (
            computeAccessibleName(element).trim()
        ));
        // Links that share a name and lead to the same place are one destination
        // offered twice, for example in the sidebar and in the breadcrumbs.
        const targets = elements.map(element => (
            role === 'link' ? element.getAttribute('href') : null
        ));
        const duplicates = names.filter((name, index) => {
            if (name.length === 0) return true;
            const first = names.indexOf(name);
            return first !== index && (targets[first] === null || targets[first] !== targets[index]);
        });
        return duplicates.length > 0 ? [{ role, names }] : [];
    });
};

/** Heading levels that skip a level on the way down, in document order. */
export const headingOrderViolations = (container: HTMLElement): string[] => {
    let previous = 0;
    return Array.from(container.querySelectorAll('h1, h2, h3, h4, h5, h6')).flatMap(heading => {
        const level = Number(heading.tagName[1]);
        const skipped = level > previous + 1;
        previous = level;
        return skipped ? [`h${level} ${heading.textContent?.trim() ?? ''}`] : [];
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
