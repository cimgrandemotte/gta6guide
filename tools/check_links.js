#!/usr/bin/env node
/**
 * QA S6 — vérifie que tous les liens internes (href/src) des fichiers HTML
 * pointent vers un fichier existant. Aucune dépendance npm.
 * Usage : npm run check:links
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SKIP = new Set(['.git', 'node_modules', '.github', 'tools', '_site', 'out']);

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const files = walk(ROOT);
const broken = [];
let checked = 0;

for (const file of files) {
  const html = fs.readFileSync(file, 'utf8');
  const refs = [...html.matchAll(/(?:href|src)\s*=\s*["']([^"']+)["']/gi)].map(m => m[1]);
  for (const ref of refs) {
    if (/^(https?:|mailto:|tel:|#|data:|javascript:)/i.test(ref)) continue;
    const clean = decodeURIComponent(ref.split(/[?#]/)[0]);
    if (!clean) continue;
    checked++;
    const target = clean.startsWith('/')
      ? path.join(ROOT, clean.slice(1))
      : path.resolve(path.dirname(file), clean);
    if (!fs.existsSync(target)) {
      broken.push(`${path.relative(ROOT, file)} → ${ref}`);
    }
  }
}

console.log(`QA liens : ${files.length} fichiers HTML, ${checked} références internes.`);
if (broken.length) {
  console.error(`\n❌ ${broken.length} lien(s) cassé(s) :`);
  broken.forEach(b => console.error('   ' + b));
  process.exit(1);
}
console.log('✅ 0 lien interne cassé.');
