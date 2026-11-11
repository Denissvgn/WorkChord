/**
 * Where things are in the manifest editor: the line of each JSON path, so a
 * problem can say "line 12" and the editor can jump there.
 */

export interface EditorIssue {
    line: number | null;
    path: string | null;
    message: string;
}

const lineAt = (text: string, position: number) => text.slice(0, Math.max(0, position)).split('\n').length;

/** Paths such as `workers[0].role` mapped to the 1-based line where their key or value starts. */
export const manifestPathLines = (text: string): Map<string, number> => {
    const lines = new Map<string, number>();
    type Frame = { kind: 'object'; key: string | null } | { kind: 'array'; index: number };
    const stack: Frame[] = [];
    let line = 1;
    const pathOf = (extra?: string | number) => {
        const parts = stack.map(frame => frame.kind === 'object' ? frame.key : frame.index);
        if (extra !== undefined) parts.push(extra);
        return parts.filter(part => part !== null && part !== -1).reduce<string>((path, part) => (
            typeof part === 'number' ? `${path}[${part}]` : path ? `${path}.${part}` : String(part)), '');
    };
    const beginValue = () => {
        const top = stack[stack.length - 1];
        if (top?.kind === 'array') {
            top.index += 1;
            lines.set(pathOf(), line);
        }
    };
    let expectKey = false;
    for (let i = 0; i < text.length; i += 1) {
        const char = text[i];
        if (char === '\n') { line += 1; continue; }
        if (char === '"') {
            let end = i + 1;
            while (end < text.length && text[end] !== '"') end += text[end] === '\\' ? 2 : 1;
            const value = text.slice(i + 1, end);
            const top = stack[stack.length - 1];
            if (expectKey && top?.kind === 'object') {
                top.key = value;
                lines.set(pathOf(), line);
                expectKey = false;
            } else {
                beginValue();
            }
            i = end;
            continue;
        }
        if (char === '{') { beginValue(); stack.push({ kind: 'object', key: null }); expectKey = true; continue; }
        if (char === '[') { beginValue(); stack.push({ kind: 'array', index: -1 }); continue; }
        if (char === '}' || char === ']') { stack.pop(); continue; }
        if (char === ',') { if (stack[stack.length - 1]?.kind === 'object') expectKey = true; continue; }
        if (/[-0-9tfn]/.test(char)) {
            beginValue();
            while (i + 1 < text.length && /[-+.0-9a-zA-Z]/.test(text[i + 1])) i += 1;
        }
    }
    return lines;
};

/** The line of a path, or of its nearest parent that exists in the text. */
export const lineForPath = (text: string, path: string): number | null => {
    const lines = manifestPathLines(text);
    let candidate = path;
    while (candidate) {
        const found = lines.get(candidate);
        if (found !== undefined) return found;
        const cut = Math.max(candidate.lastIndexOf('.'), candidate.lastIndexOf('['));
        candidate = cut > 0 ? candidate.slice(0, cut) : '';
    }
    return null;
};

/**
 * Engines that report no position quote about ten characters on each side of
 * the bad token instead; find that excerpt in the text.
 */
const excerptLine = (text: string, message: string): number | null => {
    if (/unexpected end/i.test(message)) return text.trimEnd().split('\n').length;
    const match = /Unexpected token '(.+?)', (\.\.\.)?"([\s\S]*?)"(?:\.\.\.)? is not valid JSON/.exec(message);
    if (!match) return null;
    const [, token, leading, excerpt] = match;
    const start = text.indexOf(excerpt);
    if (start < 0) return null;
    return lineAt(text, start + (leading ? 10 : Math.max(0, excerpt.indexOf(token))));
};

/** A JSON syntax error with the line it happened on, when the browser reports a position. */
export const syntaxIssue = (text: string, error: unknown): EditorIssue | null => {
    if (!(error instanceof SyntaxError)) return null;
    const lineColumn = /line (\d+) column (\d+)/i.exec(error.message);
    const position = /position (\d+)/i.exec(error.message);
    const line = lineColumn ? Number(lineColumn[1]) : position ? lineAt(text, Number(position[1])) : excerptLine(text, error.message);
    return { line, path: null, message: error.message };
};

/** The secret check names a JSON path such as `$.workers[0].token`. */
export const pathIssue = (text: string, message: string): EditorIssue => {
    const match = /\$\.([\w.[\]-]+)/.exec(message);
    const path = match ? match[1] : null;
    return { line: path ? lineForPath(text, path) : null, path, message };
};

/** FastAPI field errors: `loc` such as ["body", "manifest", "workers", 0, "role"]. */
export const fieldIssues = (text: string, detail: unknown): EditorIssue[] => {
    if (!Array.isArray(detail)) return [];
    return detail.flatMap(item => {
        if (!item || typeof item !== 'object' || !Array.isArray((item as { loc?: unknown }).loc)) return [];
        const loc = ((item as { loc: Array<string | number> }).loc).filter(part => part !== 'body' && part !== 'manifest');
        const path = loc.reduce<string>((value, part) => typeof part === 'number' ? `${value}[${part}]` : value ? `${value}.${part}` : String(part), '');
        return [{ line: path ? lineForPath(text, path) : null, path: path || null, message: String((item as { msg?: unknown }).msg ?? '') }];
    });
};

/** Character offsets of a 1-based line, to select it in a textarea. */
export const lineRange = (text: string, line: number): [number, number] => {
    const rows = text.split('\n');
    const start = rows.slice(0, line - 1).reduce((sum, row) => sum + row.length + 1, 0);
    return [start, start + (rows[line - 1]?.length ?? 0)];
};
