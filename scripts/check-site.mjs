// scripts/check-site.mjs — zero-dependency checks for the static site.
// Usage: node scripts/check-site.mjs      (exit code 1 when errors are found)
// Checks: local references exist, canonicals/sitemap/og:url agree, JSON parses,
// one h1, no skipped heading levels, alt on images, id references, link safety,
// no placeholder domain, font and manifest assets exist.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://atikulislam.me';
const SKIP_DIRS = new Set(['.git', 'node_modules', 'design']);
const errors = [];
const warnings = [];
const err = (where, msg) => errors.push(`${where}: ${msg}`);
const warn = (where, msg) => warnings.push(`${where}: ${msg}`);

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

const rel = (f) => path.relative(ROOT, f).split(path.sep).join('/');
const files = walk(ROOT);
const htmlFiles = files.filter((f) => f.endsWith('.html'));
const cssFiles = files.filter((f) => f.endsWith('.css'));
const jsonFiles = files.filter((f) => (f.endsWith('.json') || f.endsWith('.webmanifest')) && !rel(f).startsWith('.vscode/'));

/* Map a URL path (e.g. /about/) to a repo file. Returns the absolute file path. */
function pathToFile(urlPath) {
  const clean = urlPath.split('#')[0].split('?')[0] || '/';
  const target = path.join(ROOT, clean);
  if (clean.endsWith('/')) return path.join(target, 'index.html');
  return target;
}

/* 1. Every HTML file ----------------------------------------------------------- */
const htmlUrlPaths = new Map(); // urlPath -> file, for indexable pages
for (const file of htmlFiles) {
  const where = rel(file);
  const html = fs.readFileSync(file, 'utf8');
  if (!/<html[\s>]/i.test(html)) continue; // plain verification files (e.g. Search Console) are left untouched
  const noindex = /<meta name="robots" content="[^"]*noindex/i.test(html);

  if (/REPLACE-WITH/.test(html)) err(where, 'placeholder text "REPLACE-WITH" present');
  if (!/<html lang="[a-z-]+"/i.test(html)) err(where, 'missing lang attribute on <html>');
  if (!/<title>[^<]+<\/title>/.test(html)) err(where, 'missing <title>');

  const title = ((html.match(/<title>([^<]*)<\/title>/) || [])[1] || '').replace(/&amp;/g, '&');
  if (title.length > 65) warn(where, `title is ${title.length} characters`);
  const desc = ((html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '').replace(/&amp;/g, '&');
  if (desc === undefined) err(where, 'missing meta description');
  else if (desc.length < 70 || desc.length > 160) warn(where, `meta description is ${desc.length} characters`);

  const h1s = html.match(/<h1[\s>]/g) || [];
  if (h1s.length !== 1) err(where, `expected one <h1>, found ${h1s.length}`);

  // Heading order: no level may jump up by more than one.
  let last = 0;
  for (const m of html.matchAll(/<h([1-6])[\s>]/g)) {
    const level = Number(m[1]);
    if (last && level > last + 1) err(where, `heading jumps from h${last} to h${level}`);
    last = level;
  }

  // Images: alt is required; width/height reduce layout shift.
  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\salt="/.test(m[0])) err(where, `image without alt: ${m[0].slice(0, 90)}`);
    if (!/\swidth="/.test(m[0]) || !/\sheight="/.test(m[0])) warn(where, `image without width/height: ${m[0].slice(0, 90)}`);
  }

  // Links opening new tabs must carry noopener noreferrer.
  for (const m of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) {
    if (!/rel="[^"]*noopener[^"]*"/.test(m[0]) || !/rel="[^"]*noreferrer[^"]*"/.test(m[0])) {
      err(where, `target="_blank" without rel="noopener noreferrer": ${m[0].slice(0, 90)}`);
    }
  }

  // Inline event handlers are not allowed (CSP-friendly, testable).
  if (/\son[a-z]+="/i.test(html)) err(where, 'inline event handler attribute found');

  // Duplicate ids and id references.
  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dupes.length) err(where, `duplicate ids: ${[...new Set(dupes)].join(', ')}`);
  const idSet = new Set(ids);
  for (const m of html.matchAll(/\s(aria-labelledby|aria-describedby|aria-controls|for)="([^"]+)"/g)) {
    if (m[1] === 'for') { if (!idSet.has(m[2])) err(where, `label for="${m[2]}" has no matching id`); continue; }
    for (const id of m[2].split(/\s+/)) if (!idSet.has(id)) err(where, `${m[1]} references missing id "${id}"`);
  }
  for (const m of html.matchAll(/\shref="#([^"]+)"/g)) {
    if (!idSet.has(m[1])) err(where, `in-page link to missing id "#${m[1]}"`);
  }

  // Local references must exist (href, src, use href).
  for (const m of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    const ref = m[1];
    if (/^(https?:|mailto:|tel:|data:|#|javascript:)/i.test(ref)) continue;
    const target = pathToFile(ref.startsWith('/') ? ref : '/' + path.posix.join(path.posix.dirname(rel(file)), ref));
    if (!fs.existsSync(target.split('#')[0])) err(where, `missing local file for "${ref}"`);
  }

  // Absolute site URLs (canonical, og:image, JSON-LD) must point at real files.
  for (const m of html.matchAll(/https:\/\/atikulislam\.me(\/[^"'\s<>)\\]*)?/g)) {
    const urlPath = (m[1] || '/').split('#')[0];
    if (!fs.existsSync(pathToFile(urlPath))) err(where, `absolute URL points to missing file: ${m[0]}`);
  }

  // Canonical and og:url must agree with the file's own URL.
  const urlPath = '/' + path.posix.dirname(rel(file)).replace(/^\.$/, '') ;
  const expected = rel(file) === 'index.html' ? '/' : (rel(file) === '404.html' ? null : `/${path.posix.dirname(rel(file))}/`);
  const canonical = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
  const ogUrl = (html.match(/<meta property="og:url" content="([^"]+)"/) || [])[1];
  if (!noindex) {
    if (!canonical) err(where, 'indexable page without canonical');
    else if (expected && canonical !== SITE + expected) err(where, `canonical ${canonical} does not match ${SITE + expected}`);
    if (ogUrl && canonical && ogUrl !== canonical) err(where, 'og:url differs from canonical');
    if (expected) htmlUrlPaths.set(expected, file);
  } else if (canonical) {
    err(where, 'noindex page should not declare a canonical');
  }

  // JSON-LD must parse.
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(m[1]); } catch (e) { err(where, `JSON-LD does not parse: ${e.message}`); }
  }
}
void 0;

/* 2. Sitemap ------------------------------------------------------------------- */
const sitemapFile = path.join(ROOT, 'sitemap.xml');
const sitemap = fs.existsSync(sitemapFile) ? fs.readFileSync(sitemapFile, 'utf8') : '';
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
if (!locs.length) err('sitemap.xml', 'no <loc> entries');
for (const loc of locs) {
  if (!loc.startsWith(SITE + '/')) err('sitemap.xml', `unexpected host in ${loc}`);
  const p = loc.slice(SITE.length) || '/';
  if (!fs.existsSync(pathToFile(p))) err('sitemap.xml', `entry has no file: ${loc}`);
}
for (const [urlPath, file] of htmlUrlPaths) {
  if (!locs.includes(SITE + urlPath)) err(rel(file), `indexable page missing from sitemap.xml (${SITE + urlPath})`);
}
if (/Master-Blueprint|<!--/.test(sitemap)) warn('sitemap.xml', 'contains a comment or an internal reference');

/* 3. Robots, CNAME, manifest ------------------------------------------------------ */
const robots = fs.readFileSync(path.join(ROOT, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${SITE}/sitemap.xml`)) err('robots.txt', 'missing Sitemap line for the production sitemap');
if (fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim() !== 'atikulislam.me') err('CNAME', 'unexpected domain');

const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'site.webmanifest'), 'utf8'));
for (const icon of manifest.icons || []) {
  if (!fs.existsSync(path.join(ROOT, icon.src))) err('site.webmanifest', `missing icon ${icon.src}`);
}

/* 4. CSS url() references and JSON files ---------------------------------------- */
for (const file of cssFiles) {
  const css = fs.readFileSync(file, 'utf8');
  for (const m of css.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/g)) {
    const ref = m[1];
    if (/^(https?:|data:)/.test(ref)) continue;
    const target = ref.startsWith('/') ? path.join(ROOT, ref) : path.join(path.dirname(file), ref);
    if (!fs.existsSync(target)) err(rel(file), `missing asset ${ref}`);
  }
}
for (const file of jsonFiles) {
  try { JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { err(rel(file), `invalid JSON: ${e.message}`); }
}

/* 5. Report ------------------------------------------------------------------------ */
console.log(`checked ${htmlFiles.length} HTML, ${cssFiles.length} CSS, ${jsonFiles.length} JSON files; ${locs.length} sitemap URLs`);
if (warnings.length) console.log(`warnings (${warnings.length}):\n  ${warnings.join('\n  ')}`);
if (errors.length) {
  console.log(`errors (${errors.length}):\n  ${errors.join('\n  ')}`);
  process.exit(1);
}
console.log('no errors');
