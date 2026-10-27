#!/usr/bin/env node
// install.mjs — glasspring skill installer (Phase 3 distribution entry).
// Copies this skill folder into a target project's .agents/skills/glasspring/
// and verifies the installed structure. Zero dependencies (node:fs).
//
// Usage:
//   node install.mjs --target <project-dir> [--dry-run]
//   node install.mjs --selftest
//
// `npx glasspring` registry packaging is a later step; this script is the
// same logic the package would call.

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, lstatSync, renameSync, realpathSync } from "node:fs";
import { basename, dirname, join, resolve, relative, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { tmpdir } from "node:os";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(scriptDir, "..");

const EXCLUDE = /(^|[\\/])(__pycache__|\.DS_Store)$|\.pyc$/;

function listFiles(dir, base = dir, acc = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (EXCLUDE.test(p)) continue;
    if (lstatSync(p).isSymbolicLink()) throw new Error(`source symlink requires manual review: ${p}`);
    if (statSync(p).isDirectory()) listFiles(p, base, acc);
    else acc.push(p.slice(base.length + 1));
  }
  return acc;
}

function canonicalizeAllowingMissingTail(path) {
  let probe = resolve(path);
  const tail = [];
  while (true) {
    try {
      // Canonicalize the existing prefix so OS aliases such as macOS /var
      // do not look like user-created destination symlinks.
      const prefix = realpathSync(probe);
      return resolve(prefix, ...tail);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      try {
        if (lstatSync(probe).isSymbolicLink()) {
          throw new Error(`target path contains a dangling symlink: ${probe}`);
        }
      } catch (statError) {
        if (statError.code !== "ENOENT") throw statError;
      }
      const parent = dirname(probe);
      if (parent === probe) throw error;
      tail.unshift(basename(probe));
      probe = parent;
    }
  }
}

function sourceRevision() {
  // Skill copies drift from their source (Skill Constellations finding:
  // copied skills rarely track upstream). Printing the source commit makes
  // an install reproducible and auditable.
  try {
    return execSync("git rev-parse HEAD", { cwd: skillRoot, stdio: ["ignore", "pipe", "ignore"] })
      .toString().trim();
  } catch {
    return "not-a-git-checkout";
  }
}

function install(targetDir, dryRun, host = "codex", replace = false) {
  if (!["codex", "claude", "generic"].includes(host)) throw new Error("host must be codex, claude, or generic");
  const target = canonicalizeAllowingMissingTail(targetDir);
  const dest = join(target, host === "claude" ? ".claude" : ".agents", "skills", "glasspring");
  const rel = relative(realpathSync(skillRoot), dest);
  if (!rel || (!rel.startsWith("..") && !isAbsolute(rel))) throw new Error("destination must be outside the source skill");
  // Reject destination symlinks/junctions, including intermediate components.
  for (let p = dest; ; p = dirname(p)) {
    try {
      if (lstatSync(p).isSymbolicLink()) throw new Error(`destination symlink requires manual review: ${p}`);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    if (p === dirname(p)) break;
  }
  const files = listFiles(skillRoot);
  if (!files.includes("SKILL.md")) {
    throw new Error("skill root is missing SKILL.md — refusing to install");
  }
  console.log(`source : ${skillRoot}`);
  console.log(`dest   : ${dest}`);
  console.log(`files  : ${files.length}`);
  if (dryRun) {
    for (const f of files) console.log(`  would copy ${f}`);
    console.log("dry-run: no files written");
    return { dest, count: files.length };
  }
  if (existsSync(dest) && !replace) throw new Error("destination exists; use --replace to retain a backup and replace it");
  mkdirSync(dirname(dest), { recursive: true });
  const stamp = `${Date.now()}-${process.pid}`;
  const staging = `${dest}.staging-${stamp}`;
  const backup = `${dest}.backup-${stamp}`;
  let backedUp = false;
  try {
    cpSync(skillRoot, staging, { recursive: true, filter: (p) => !EXCLUDE.test(p) });
    const refs = verifyStructure(staging);
    for (const file of files) {
      if (!readFileSync(join(skillRoot, file)).equals(readFileSync(join(staging, file)))) throw new Error(`copy differs: ${file}`);
    }
    if (existsSync(dest)) { renameSync(dest, backup); backedUp = true; }
    renameSync(staging, dest);
    console.log(`installed: ${files.length} files, ${refs} references verified for ${host}; restart the host and verify discovery separately`);
    console.log(`source revision: ${sourceRevision()} — record it with this install for reproducibility`);
    if (backedUp) console.log(`backup: ${backup}`);
    return { dest, count: files.length, backup: backedUp ? backup : null };
  } catch (e) {
    if (backedUp && !existsSync(dest)) renameSync(backup, dest);
    throw e;
  } finally { rmSync(staging, { recursive: true, force: true }); }
}

function verifyStructure(dest) {
  if (!existsSync(join(dest, "SKILL.md")) || !existsSync(join(dest, "scripts", "check_contrast.py"))) {
    throw new Error("installation verification failed: expected files missing at destination");
  }
  // G1 file-map integrity at the DESTINATION: every references|scripts|assets
  // path mentioned in the installed SKILL.md must exist. Catches renamed or
  // moved references that a tree copy alone would silently ship broken.
  const skill = readFileSync(join(dest, "SKILL.md"), "utf8");
  const refs = [...new Set([...skill.matchAll(/(?:references|scripts|assets)\/[\w\-./]+/g)].map((m) => m[0]))];
  const missing = refs.filter((r) => !existsSync(join(dest, ...r.split("/"))));
  if (missing.length) {
    throw new Error(`installation verification failed: ${missing.length} SKILL.md-referenced file(s) missing at destination: ${missing.join(", ")}`);
  }
  return refs.length;
}

function selftest() {
  // temp dir OUTSIDE skillRoot — copying a tree into its own descendant fails
  const tmp = join(tmpdir(), `glasspring-install-selftest-${Date.now()}`);
  try {
    const { dest, count } = install(tmp, false);
    const ok = existsSync(join(dest, "SKILL.md")) && existsSync(join(dest, "scripts", "check_contrast.py")) && count > 10;
    console.log(`  [${ok ? "PASS" : "FAIL"}] self-install to temp: ${count} files, structure + file-map verified`);
    if (!ok) return 1;
    // discriminating anchor: a destination whose SKILL.md references a missing file must FAIL verification
    const broken = join(tmpdir(), `glasspring-install-broken-${Date.now()}`);
    mkdirSync(join(broken, "scripts"), { recursive: true });
    cpSync(join(dest, "SKILL.md"), join(broken, "SKILL.md"));
    cpSync(join(dest, "scripts", "check_contrast.py"), join(broken, "scripts", "check_contrast.py"));
    let threw = false;
    try { verifyStructure(broken); } catch { threw = true; }
    console.log(`  [${threw ? "PASS" : "FAIL"}] broken destination (references present in SKILL.md, files absent) is rejected`);
    rmSync(broken, { recursive: true, force: true });
    if (!threw) return 1;
    console.log("SELFTEST PASSED");
    return 0;
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}

const args = process.argv.slice(2);
if (args.includes("--selftest")) {
  process.exit(selftest());
}
const ti = args.indexOf("--target");
const target = ti >= 0 ? args[ti + 1] : undefined;
const dryRun = args.includes("--dry-run");
try {
  if (!target || target.startsWith("--")) throw new Error("explicit --target <project-dir> is required");
  const hi = args.indexOf("--host");
  const host = hi >= 0 ? args[hi + 1] : "codex";
  const known = new Set(["--target", "--host", "--dry-run", "--replace"]);
  for (let i = 0; i < args.length; i++) {
    if (!known.has(args[i])) throw new Error(`unknown argument: ${args[i]}`);
    if (["--target", "--host"].includes(args[i])) i++;
  }
  install(target, dryRun, host, args.includes("--replace"));
} catch (e) {
  console.error(`install failed: ${e.message}`);
  process.exit(1);
}
