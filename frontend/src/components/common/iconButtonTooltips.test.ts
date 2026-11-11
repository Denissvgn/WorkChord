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

/** Visible text inside a JSX element: literal text or a plain expression (not a nested element or condition). */
const hasVisibleText = (element: ts.JsxElement) => {
    let found = false;
    const visit = (node: ts.Node) => {
        if (found) return;
        if (ts.isJsxText(node) && node.text.trim()) found = true;
        else if (ts.isJsxExpression(node) && node.expression && !ts.isJsxElement(node.expression) && !ts.isJsxSelfClosingElement(node.expression)
            && !ts.isConditionalExpression(node.expression) && !ts.isBinaryExpression(node.expression)) found = true;
        else ts.forEachChild(node, visit);
    };
    element.children.forEach(visit);
    return found;
};

// The shared Button adds the tooltip itself; a raw <button> that shows only an icon must carry a title.
it('gives every raw icon-only button a tooltip', () => {
    const missing: string[] = [];
    for (const file of sources(root)) {
        const source = ts.createSourceFile(file, readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
        const visit = (node: ts.Node) => {
            if (ts.isJsxElement(node) && node.openingElement.tagName.getText() === 'button') {
                const names = node.openingElement.attributes.properties.map(property => property.name?.getText());
                if (names.includes('aria-label') && !names.includes('title') && !hasVisibleText(node)) {
                    missing.push(`${relative(root, file)}:${source.getLineAndCharacterOfPosition(node.getStart()).line + 1}`);
                }
            }
            ts.forEachChild(node, visit);
        };
        visit(source);
    }
    expect(missing).toEqual([]);
});
