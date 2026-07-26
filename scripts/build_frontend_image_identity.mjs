import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import { relative, resolve } from "node:path";

const [artifactRootArg, sourceRevision, outputArg] = process.argv.slice(2);
if (!artifactRootArg || !sourceRevision || !outputArg) {
  throw new Error(
    "usage: build_frontend_image_identity.mjs ARTIFACT_ROOT SOURCE_REVISION OUTPUT",
  );
}
if (!/^(?:[0-9a-f]{40,64}|unknown)$/.test(sourceRevision)) {
  throw new Error(
    "source revision must be lowercase hex or the non-acceptance value unknown",
  );
}

const artifactRoot = resolve(artifactRootArg);
const output = resolve(outputArg);

async function members(directory) {
  const found = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) {
      found.push(...(await members(path)));
    } else if (entry.isFile()) {
      found.push(path);
    }
  }
  return found;
}

const digest = createHash("sha256");
for (const member of (await members(artifactRoot)).sort()) {
  const memberDigest = createHash("sha256")
    .update(await readFile(member))
    .digest();
  digest.update(relative(artifactRoot, member).replaceAll("\\", "/"));
  digest.update("\0");
  digest.update(memberDigest);
  digest.update("\n");
}

await writeFile(
  output,
  `${JSON.stringify({
    artifact_digest: digest.digest("hex"),
    component: "frontend",
    schema_version: "workchord-build-identity-v1",
    source_revision: sourceRevision,
  })}\n`,
);
