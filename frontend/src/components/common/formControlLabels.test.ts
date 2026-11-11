/// <reference types="node" />

import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import ts from 'typescript';
import { expect, it } from 'vitest';

const root = resolve(process.cwd(), 'src');
const sources = (dir: string): string[] => readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return sources(path);
    return path.endsWith('.tsx') && !path.includes('.test.') ? [path] : [];
});

// Wrappers that render a <label> around their children.
const LABEL_WRAPPERS = new Set(['label', 'InlineField']);

/**
 * A raw select, textarea or input must be named: by aria-label or aria-labelledby, by an id (trusted to
 * match a label's htmlFor), or by sitting inside a label. File pickers sit behind a labelled button.
 */
it('names every raw form control', () => {
    const missing: string[] = [];
    for (const file of sources(root)) {
        const source = ts.createSourceFile(file, readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
        const visit = (node: ts.Node, insideLabel: boolean) => {
            const opening = ts.isJsxElement(node) ? node.openingElement : ts.isJsxSelfClosingElement(node) ? node : null;
            let labelled = insideLabel;
            if (opening) {
                const tag = opening.tagName.getText();
                if (LABEL_WRAPPERS.has(tag)) labelled = true;
                if (['select', 'textarea', 'input'].includes(tag)) {
                    const props = opening.attributes.properties;
                    const names = props.map(property => property.name?.getText());
                    const type = props.find(property => property.name?.getText() === 'type');
                    const typeText = type && ts.isJsxAttribute(type) ? type.initializer?.getText() ?? '' : '';
                    const exempt = /file|hidden/.test(typeText);
                    const named = labelled || names.some(name => name === 'aria-label' || name === 'aria-labelledby' || name === 'id');
                    if (!exempt && !named) missing.push(`${relative(root, file)}:${source.getLineAndCharacterOfPosition(node.getStart()).line + 1} <${tag}>`);
                }
            }
            ts.forEachChild(node, child => visit(child, labelled));
        };
        visit(source, false);
    }
    expect(missing).toEqual([]);
});
