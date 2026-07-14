import { gzipSync } from 'node:zlib';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const BUDGETS = Object.freeze({
  entry: 300 * 1024,
  route: 300 * 1024,
  shared: 400 * 1024,
  css: 250 * 1024,
});

export const classifyChunk = (manifestEntry) => {
  if (manifestEntry.isEntry) return 'entry';
  if (manifestEntry.isDynamicEntry) return 'route';
  return 'shared';
};

export const evaluateBudget = (assets, budgets = BUDGETS) => (
  assets.map(asset => ({
    ...asset,
    budget: budgets[asset.kind],
    overBudget: asset.parsedBytes > budgets[asset.kind],
  }))
);

export const inspectBundle = (distDirectory) => {
  const manifestPath = resolve(distDirectory, '.vite/manifest.json');
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const assets = [];
  const seen = new Set();

  for (const [source, entry] of Object.entries(manifest)) {
    if (entry.file?.endsWith('.js') && !seen.has(entry.file)) {
      const bytes = readFileSync(resolve(distDirectory, entry.file));
      assets.push({
        source,
        file: entry.file,
        kind: classifyChunk(entry),
        parsedBytes: bytes.byteLength,
        gzipBytes: gzipSync(bytes).byteLength,
      });
      seen.add(entry.file);
    }
    for (const cssFile of entry.css ?? []) {
      if (seen.has(cssFile)) continue;
      const bytes = readFileSync(resolve(distDirectory, cssFile));
      assets.push({
        source,
        file: cssFile,
        kind: 'css',
        parsedBytes: bytes.byteLength,
        gzipBytes: gzipSync(bytes).byteLength,
      });
      seen.add(cssFile);
    }
  }

  return evaluateBudget(assets).sort((left, right) => right.parsedBytes - left.parsedBytes);
};

const formatKiB = bytes => `${(bytes / 1024).toFixed(1)} KiB`;

export const run = (distDirectory) => {
  const results = inspectBundle(distDirectory);
  const reportPath = resolve(distDirectory, 'bundle-composition.json');
  writeFileSync(reportPath, `${JSON.stringify({ budgets: BUDGETS, assets: results }, null, 2)}\n`);

  for (const asset of results) {
    const outcome = asset.overBudget ? 'OVER' : 'ok';
    console.log(`${outcome.padEnd(4)} ${asset.kind.padEnd(6)} ${formatKiB(asset.parsedBytes).padStart(10)} parsed ${formatKiB(asset.gzipBytes).padStart(10)} gzip  ${asset.file}`);
  }

  const failures = results.filter(asset => asset.overBudget);
  if (failures.length > 0) {
    throw new Error(`Bundle budget exceeded by ${failures.map(asset => asset.file).join(', ')}`);
  }
  return results;
};

const isCli = process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (isCli) {
  const scriptDirectory = dirname(fileURLToPath(import.meta.url));
  run(resolve(scriptDirectory, '../dist'));
}
