import { readFileSync } from 'node:fs';
import { readdir, readFile } from 'node:fs/promises';
import { extname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const semanticRoots = new Set([
    'surface', 'content', 'border', 'action', 'focus', 'status', 'feedback', 'overlay', 'terminal',
]);
const colorUtilityPrefixes = [
    'ring-offset',
    'drop-shadow',
    'border-x', 'border-y', 'border-t', 'border-r', 'border-b', 'border-l', 'border-s', 'border-e',
    'divide-x', 'divide-y',
    'placeholder', 'decoration', 'outline', 'shadow', 'accent', 'caret', 'stroke', 'fill',
    'border', 'divide', 'ring', 'from', 'via', 'to', 'text', 'bg',
].sort((left, right) => right.length - left.length);
const colorUtilitySource = colorUtilityPrefixes.join('|');
const semanticRootSource = [...semanticRoots].join('|');
const paletteSource = 'white|black|gray|grey|slate|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose';
const variantSource = '(?:[a-z0-9_-]+:)*';
const semanticClassPattern = new RegExp(`(?<![\\w-])(${variantSource}(?:${colorUtilitySource})-(?:${semanticRootSource})(?:-[a-z0-9_-]+)*(?:\\/[a-z0-9_[\\].%-]+)?)`, 'gi');
const legacyClassPattern = new RegExp(`(?<![\\w-])(${variantSource}(?:bg-bg-[a-z0-9_-]+|text-text-[a-z0-9_-]+|border-border-primary|bg-border-primary|border-bg-primary|(?:bg|ring)-cta|(?:${colorUtilitySource})-(?:primary(?:-foreground)?|background|text)(?:\\/[a-z0-9_[\\].%-]+)?))(?![\\w-])`, 'gi');
const rawPaletteClassPattern = new RegExp(`(?<![\\w-])(${variantSource}(?:${colorUtilitySource})-(?:${paletteSource})(?:-[0-9]{2,3})?(?:\\/[0-9]{1,3})?)(?![\\w-])`, 'gi');
const darkVariantClassPattern = new RegExp(`(?<![\\w-])(${variantSource}dark:${variantSource}(?:${colorUtilitySource})-[a-z0-9_[\\]./%-]+)(?![\\w-])`, 'gi');
const arbitraryColorClassPattern = new RegExp(`(?<![\\w-])(${variantSource}(?:${colorUtilitySource})-\\[(?:#|rgba?\\(|hsla?\\(|oklch\\(|color:)[^\\]\\s]+\\])(?![\\w-])`, 'gi');
const translucentSemanticTextPattern = new RegExp(`(?<![\\w-])(${variantSource}text-(?:${semanticRootSource})(?:-[a-z0-9_-]+)*\\/[a-z0-9_[\\].%-]+)(?![\\w-])`, 'gi');

// The semantic colours are the --color-* names in the @theme blocks of globals.css (Tailwind 4 CSS-first theme).
export const themeColorNames = (stylesheet) => {
    const names = new Set();
    for (const block of stylesheet.matchAll(/@theme\b[^{]*\{([^}]*)\}/g)) {
        for (const match of block[1].matchAll(/--color-([a-z0-9-]+)\s*:/g)) names.add(match[1]);
    }
    return names;
};

const globalsCss = readFileSync(new URL('../src/styles/globals.css', import.meta.url), 'utf8');
export const semanticColorNames = new Set(
    [...themeColorNames(globalsCss)].filter(name => semanticRoots.has(name.split('-')[0])),
);

const baseUtility = (className) => className.split(':').at(-1) ?? className;
const colorNameFromUtility = (utility) => {
    const prefix = colorUtilityPrefixes.find(candidate => utility.startsWith(`${candidate}-`));
    return prefix ? utility.slice(prefix.length + 1).split('/')[0] : null;
};

export const findInvalidSemanticClasses = (source, validColorNames = semanticColorNames) => {
    const failures = new Set();

    for (const match of source.matchAll(legacyClassPattern)) failures.add(match[1]);
    for (const match of source.matchAll(rawPaletteClassPattern)) failures.add(match[1]);
    for (const match of source.matchAll(darkVariantClassPattern)) failures.add(match[1]);
    for (const match of source.matchAll(arbitraryColorClassPattern)) failures.add(match[1]);
    for (const match of source.matchAll(translucentSemanticTextPattern)) failures.add(match[1]);
    for (const match of source.matchAll(semanticClassPattern)) {
        const className = match[1];
        const colorName = colorNameFromUtility(baseUtility(className));
        if (colorName && !validColorNames.has(colorName)) {
            failures.add(className);
        }
    }

    return [...failures].sort();
};

const sourceFiles = async (root) => {
    const entries = await readdir(root, { withFileTypes: true });
    const files = [];
    for (const entry of entries) {
        const path = resolve(root, entry.name);
        if (entry.isDirectory()) {
            files.push(...await sourceFiles(path));
        } else if (
            ['.ts', '.tsx', '.js', '.jsx'].includes(extname(entry.name))
            && !entry.name.includes('.test.')
            && !entry.name.includes('.spec.')
        ) {
            files.push(path);
        }
    }
    return files;
};

export const validateFiles = async (files) => {
    const failures = [];
    for (const file of files) {
        const invalidClasses = findInvalidSemanticClasses(await readFile(file, 'utf8'));
        for (const className of invalidClasses) failures.push({ file, className });
    }
    return failures;
};

const main = async () => {
    const requestedFiles = process.argv.slice(2).map(path => resolve(path));
    const files = requestedFiles.length > 0
        ? requestedFiles
        : await sourceFiles(resolve('src'));
    const failures = await validateFiles(files);

    if (failures.length > 0) {
        console.error('Non-semantic or undefined Tailwind color classes:');
        for (const failure of failures) {
            console.error(`${failure.file}: ${failure.className}`);
        }
        process.exitCode = 1;
        return;
    }

    console.log(`Semantic Tailwind class guard passed (${files.length} source files).`);
};

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
    await main();
}
