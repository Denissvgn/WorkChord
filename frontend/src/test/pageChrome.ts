import { computeAccessibleName } from 'dom-accessibility-api';

export const expectPageChrome = (container: HTMLElement, options: { status?: 'migrated' | 'pending' } = {}) => {
    if (options.status === 'pending') return;
    const failures: string[] = [];
    if (container.querySelectorAll('[data-testid="page-header"]').length !== 1) failures.push('Expected one PageHeader');
    if (container.querySelectorAll('button.btn-primary').length > 1) failures.push('More than one primary button');
    if (container.querySelectorAll('[data-testid="page-toolbar"]').length > 1) failures.push('More than one PageToolbar');
    for (const control of container.querySelectorAll('button, select')) {
        if (control.tagName === 'SELECT' && /iteration/i.test(`${computeAccessibleName(control)} ${control.id} ${control.getAttribute('name') ?? ''}`)) failures.push('Page has an iteration selector');
        if (control.getAttribute('data-page-chrome-control') !== control.tagName.toLowerCase()) failures.push(`Bare ${control.tagName.toLowerCase()}`);
    }
    let previousLevel = 0;
    for (const heading of container.querySelectorAll('h1, h2, h3, h4, h5, h6')) {
        const level = Number(heading.tagName[1]);
        if (level > previousLevel + 1) failures.push(`Heading level skips to h${level}`);
        previousLevel = level;
    }
    if (failures.length) throw new Error(failures.join('; '));
};
