// The picture that tastes of one ingredient — entry point (Node 22, stdlib only).
//
// The picture itself is rendered deterministically by generate.py into
// entry.png (1024x1024, well under 1 MiB). This program only places that
// finished picture at /output/entry.png, the path the grader reads.
//
// It never deletes the /output folder itself: it creates the folder when
// missing and removes only stale files inside it, then copies the image.
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png is missing next to main.ts");
}

mkdirSync(outDir, { recursive: true });
for (const name of readdirSync(outDir)) {
  const p = join(outDir, name);
  if (p !== target) rmSync(p, { recursive: true, force: true });
}
copyFileSync(source, target);
const bytes = statSync(target).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
}
console.log(`wrote /output/entry.png (${bytes} bytes)`);
