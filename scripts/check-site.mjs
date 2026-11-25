// scripts/check-site.mjs — zero-dependency pre-publish checks for atikulislam.me
//
//   node scripts/check-site.mjs        (exit code 1 when any error is found)
//
// Covers: local references, canonical/og:url agreement, sitemap ↔ pages,
// @graph validity (@context on every block, stable @ids that resolve), Open
// Graph + Twitter completeness, JSON parsing, one <h1>, heading order, image
// alt/size, link safety, id references, email obfuscation, banned copy,
// internal-document leakage (files, robots and links), security.txt, manifest.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://atikulislam.me';
const SKIP_DIRS = new Set(['.git', 'node_modules']);
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
const jsonFiles = files.filter(
  (f) => (f.endsWith('.json') || f.endsWith('.webmanifest')) && !rel(f).startsWith('.vscode/'),
);

/* Map a URL path (e.g. /about/) to a repo file. */
function pathToFile(urlPath) {
  const clean = urlPath.split('#')[0].split('?')[0] || '/';
  const target = path.join(ROOT, clean);
  if (clean.endsWith('/')) return path.join(target, 'index.html');
  return target;
}

const decode = (s) =>
  s.replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<')
   .replace(/&gt;/g, '>').replace(/&amp;/g, '&');

const CORE_ENTITIES = ['WebSite', 'Organization', 'Person', 'WebPage'];
// Schema.org page subtypes that still satisfy the "main page entity" requirement.
const PAGE_TYPES = new Set(['WebPage', 'CollectionPage', 'ProfilePage', 'ContactPage',
  'AboutPage', 'FAQPage', 'ItemPage', 'SearchResultsPage']);
const REQUIRED_ID_TYPES = new Set([
  'WebSite', 'Organization', 'Person', 'WebPage', 'ProfilePage', 'CollectionPage',
  'Article', 'Service', 'BreadcrumbList', 'FAQPage', 'ContactPage',
]);
const BANNED_COPY = [/\bAI-assisted\b/i, /Python \(learning\)/i, /\bstudent\b/i, /\baspiring\b/i, /\bfresher\b/i];
const INTERNAL_PATHS = ['/docs/', '/prompts/', '/scripts/', '/design/', '/data/', '/_source/'];

/* 1. Every HTML file -------------------------------------------------------- */
const htmlUrlPaths = new Map(); // urlPath -> file, for indexable pages
const titles = new Map();
const descriptions = new Map();

for (const file of htmlFiles) {
  const where = rel(file);
  const html = fs.readFileSync(file, 'utf8');
  if (!/<html[\s>]/i.test(html)) continue; // plain verification files untouched
  const noindex = /<meta name="robots" content="[^"]*noindex/i.test(html);
  const redirectStub = /http-equiv="refresh"/i.test(html);

  if (/REPLACE-WITH/.test(html)) err(where, 'placeholder text "REPLACE-WITH" present');
  if (!/<html lang="[a-z-]+"/i.test(html)) err(where, 'missing lang attribute on <html>');
  if (!/<title>[^<]+<\/title>/.test(html)) err(where, 'missing <title>');

  for (const re of BANNED_COPY) {
    const hit = html.match(re);
    if (hit) err(where, `banned junior framing in copy: "${hit[0]}"`);
  }

  const title = decode(((html.match(/<title>([^<]*)<\/title>/) || [])[1] || ''));
  if (title.length > 65) warn(where, `title is ${title.length} characters`);
  if (title) {
    if (titles.has(title)) err(where, `duplicate title with ${titles.get(title)}`);
    else titles.set(title, where);
  }
  const descMatch = html.match(/<meta name="description" content="([^"]*)"/);
  const desc = descMatch ? decode(descMatch[1]) : undefined;
  if (desc === undefined) err(where, 'missing meta description');
  else if (desc.length < 70 || desc.length > 160) warn(where, `meta description is ${desc.length} characters`);
  if (desc) {
    if (descriptions.has(desc)) err(where, `duplicate meta description with ${descriptions.get(desc)}`);
    else descriptions.set(desc, where);
  }

  if (!redirectStub) {
    const h1s = html.match(/<h1[\s>]/g) || [];
    if (h1s.length !== 1) err(where, `expected one <h1>, found ${h1s.length}`);
  }

  let last = 0;
  for (const m of html.matchAll(/<h([1-6])[\s>]/g)) {
    const level = Number(m[1]);
    if (last && level > last + 1) err(where, `heading jumps from h${last} to h${level}`);
    last = level;
  }

  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\salt="/.test(m[0])) err(where, `image without alt: ${m[0].slice(0, 90)}`);
    if (!/\swidth="/.test(m[0]) || !/\sheight="/.test(m[0])) {
      warn(where, `image without width/height: ${m[0].slice(0, 90)}`);
    }
  }

  for (const m of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) {
    if (!/rel="[^"]*noopener[^"]*"/.test(m[0]) || !/rel="[^"]*noreferrer[^"]*"/.test(m[0])) {
      err(where, `target="_blank" without rel="noopener noreferrer": ${m[0].slice(0, 90)}`);
    }
  }

  if (/\son[a-z]+="/i.test(html)) err(where, 'inline event handler attribute found');
  if (/href="mailto:/i.test(html)) err(where, 'raw mailto: link — email must stay obfuscated');

  for (const p of INTERNAL_PATHS) {
    if (html.includes(p)) err(where, `links to an internal path that must not be published: ${p}`);
  }
  if (/href="[^"]*(README|RELEASE)\.md"/.test(html)) err(where, 'links to an internal markdown file');

  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dupes.length) err(where, `duplicate ids: ${[...new Set(dupes)].join(', ')}`);
  const idSet = new Set(ids);
  for (const m of html.matchAll(/\s(aria-labelledby|aria-describedby|aria-controls|for)="([^"]+)"/g)) {
    if (m[1] === 'for') {
      if (!idSet.has(m[2])) err(where, `label for="${m[2]}" has no matching id`);
      continue;
    }
    for (const id of m[2].split(/\s+/)) if (!idSet.has(id)) err(where, `${m[1]} references missing id "${id}"`);
  }
  for (const m of html.matchAll(/\shref="#([^"]+)"/g)) {
    if (!idSet.has(m[1])) err(where, `in-page link to missing id "#${m[1]}"`);
  }

  for (const m of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    const ref = m[1];
    if (/^(https?:|mailto:|tel:|data:|#|javascript:)/i.test(ref)) continue;
    const target = pathToFile(ref.startsWith('/') ? ref : '/' + path.posix.join(path.posix.dirname(rel(file)), ref));
    if (!fs.existsSync(target.split('#')[0])) err(where, `missing local file for "${ref}"`);
  }

  for (const m of html.matchAll(/https:\/\/atikulislam\.me(\/[^"'\s<>)\\]*)?/g)) {
    const urlPath = (m[1] || '/').split('#')[0];
    if (!fs.existsSync(pathToFile(urlPath))) err(where, `absolute URL points to missing file: ${m[0]}`);
  }

  // One consolidated stylesheet and one script, both local.
  const sheets = [...html.matchAll(/<link rel="stylesheet" href="([^"]+)"/g)].map((m) => m[1]);
  if (!redirectStub) {
    if (sheets.length !== 1) err(where, `expected one stylesheet, found ${sheets.length}: ${sheets.join(' ')}`);
    else if (sheets[0] !== '/css/site.css') err(where, `unexpected stylesheet ${sheets[0]}`);
  }

  // Canonical, og:url and robots agreement.
  const expected = rel(file) === 'index.html'
    ? '/'
    : (rel(file) === '404.html' ? null : `/${path.posix.dirname(rel(file))}/`);
  const canonical = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
  const ogUrl = (html.match(/<meta property="og:url" content="([^"]+)"/) || [])[1];
  if (noindex && canonical && !redirectStub) {
    err(where, 'noindex page must not declare a canonical');
  }
  if (!noindex) {
    if (!canonical) err(where, 'indexable page without canonical');
    else if (expected && canonical !== SITE + expected) err(where, `canonical ${canonical} does not match ${SITE + expected}`);
    if (ogUrl && canonical && ogUrl !== canonical) err(where, 'og:url differs from canonical');
    if (expected) htmlUrlPaths.set(expected, file);
  }

  // Open Graph + Twitter completeness.
  if (!redirectStub) {
    const ogImage = (html.match(/<meta property="og:image" content="([^"]+)"/) || [])[1];
    const twitterImage = (html.match(/<meta name="twitter:image" content="([^"]+)"/) || [])[1];
    const required = [
      ['og:type', /<meta property="og:type" content="[^"]+"/],
      ['og:site_name', /<meta property="og:site_name" content="[^"]+"/],
      ['og:title', /<meta property="og:title" content="[^"]+"/],
      ['og:description', /<meta property="og:description" content="[^"]+"/],
      ['og:url', /<meta property="og:url" content="[^"]+"/],
      ['og:image', /<meta property="og:image" content="[^"]+"/],
      ['og:image:type', /<meta property="og:image:type" content="image\/jpe?g"/],
      ['og:image:width', /<meta property="og:image:width" content="1200"/],
      ['og:image:height', /<meta property="og:image:height" content="630"/],
      ['og:image:alt', /<meta property="og:image:alt" content="[^"]+"/],
      ['twitter:card', /<meta name="twitter:card" content="summary_large_image"/],
      ['twitter:site', /<meta name="twitter:site" content="@atikulislamx"/],
      ['twitter:title', /<meta name="twitter:title" content="[^"]+"/],
      ['twitter:description', /<meta name="twitter:description" content="[^"]+"/],
      ['twitter:image', /<meta name="twitter:image" content="[^"]+"/],
    ];
    for (const [name, re] of required) if (!re.test(html)) err(where, `missing or wrong ${name}`);
    if (ogImage && ogImage !== twitterImage) err(where, 'twitter:image differs from og:image');
    if (ogImage && !ogImage.startsWith(SITE + '/')) err(where, `og:image is not an absolute site URL: ${ogImage}`);
    if (!html.includes('GTM-PHVGHCMT')) err(where, 'Google Tag Manager container is missing');
  }

  // JSON-LD: one unified @graph per page, @context everywhere, @ids that resolve.
  const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  if (!redirectStub && blocks.length === 0) err(where, 'no JSON-LD block');
  const declaredIds = new Set();
  const referenceIds = new Set();
  const types = new Set();

  for (const m of blocks) {
    let data;
    try {
      data = JSON.parse(m[1]);
    } catch (e) {
      err(where, `JSON-LD does not parse: ${e.message}`);
      continue;
    }
    if (data['@context'] !== 'https://schema.org') err(where, 'JSON-LD block without "@context": "https://schema.org"');
    const nodes = Array.isArray(data['@graph']) ? data['@graph'] : [data];
    if (!Array.isArray(data['@graph'])) err(where, 'JSON-LD block is not a single @graph');
    for (const node of nodes) {
      const type = Array.isArray(node['@type']) ? node['@type'][0] : node['@type'];
      if (type) types.add(type);
      if (node['@id']) {
        if (declaredIds.has(node['@id'])) err(where, `duplicate @id in graph: ${node['@id']}`);
        declaredIds.add(node['@id']);
      } else if (REQUIRED_ID_TYPES.has(type)) {
        err(where, `@graph node of type ${type} has no stable @id`);
      }
      for (const [key, value] of Object.entries(node)) {
        if (key === '@id') continue;
        for (const value2 of Array.isArray(value) ? value : [value]) {
          if (value2 && typeof value2 === 'object' && value2['@id'] && Object.keys(value2).length === 1) {
            referenceIds.add(value2['@id']);
          }
        }
      }
    }
  }

  for (const ref of referenceIds) {
    if (!ref.includes('#')) continue; // document-level references (e.g. Location) are external
    if (!declaredIds.has(ref)) err(where, `@graph reference does not resolve: ${ref}`);
  }
  if (!noindex && !redirectStub) {
    for (const type of CORE_ENTITIES) {
      if (type === 'WebPage') {
        if (![...types].some((t) => PAGE_TYPES.has(t))) err(where, 'unified @graph is missing a WebPage entity');
      } else if (!types.has(type)) {
        err(where, `unified @graph is missing ${type}`);
      }
    }
  }
}

/* 2. Sitemap ----------------------------------------------------------------- */
const sitemapFile = path.join(ROOT, 'sitemap.xml');
const sitemap = fs.existsSync(sitemapFile) ? fs.readFileSync(sitemapFile, 'utf8') : '';
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
if (!locs.length) err('sitemap.xml', 'no <loc> entries');
const lastmods = [...sitemap.matchAll(/<lastmod>([^<]+)<\/lastmod>/g)].map((m) => m[1]);
if (lastmods.length !== locs.length) err('sitemap.xml', `${locs.length} URLs but ${lastmods.length} lastmod values`);
for (const lm of lastmods) if (!/^\d{4}-\d{2}-\d{2}/.test(lm)) err('sitemap.xml', `bad lastmod ${lm}`);
for (const loc of locs) {
  if (!loc.startsWith(SITE + '/')) err('sitemap.xml', `unexpected host in ${loc}`);
  const p = loc.slice(SITE.length) || '/';
  if (!fs.existsSync(pathToFile(p))) err('sitemap.xml', `entry has no file: ${loc}`);
}
for (const [urlPath, file] of htmlUrlPaths) {
  if (!locs.includes(SITE + urlPath)) err(rel(file), `indexable page missing from sitemap.xml (${SITE + urlPath})`);
}
for (const loc of locs) {
  const p = loc.slice(SITE.length) || '/';
  if (p === '/Atikulislamx/' || p.startsWith('/404')) err('sitemap.xml', `${loc} must not be in the sitemap`);
}
if (/<!--/.test(sitemap)) warn('sitemap.xml', 'contains an HTML comment');
const portraitOg = `${SITE}/assets/img/atikul-islam-rabbi-social-media-security-expert.jpg`;
if (!sitemap.includes('<image:loc>')) err('sitemap.xml', 'no image sitemap entries');
if (!sitemap.includes(portraitOg)) err('sitemap.xml', 'image sitemap does not reference the primary portrait');
if (!/xmlns:image="http:\/\/www\.google\.com\/schemas\/sitemap-image\/1\.1"/.test(sitemap)) {
  err('sitemap.xml', 'image namespace is missing');
}

/* 3. Robots, CNAME, manifest, security.txt ------------------------------------ */
const robots = fs.readFileSync(path.join(ROOT, 'robots.txt'), 'utf8');
if (!robots.includes(`Sitemap: ${SITE}/sitemap.xml`)) err('robots.txt', 'missing Sitemap line for the production sitemap');
for (const p of ['/docs/', '/prompts/', '/scripts/', '/data/', '/design/', '/Atikulislamx/']) {
  if (!robots.includes(`Disallow: ${p}`)) err('robots.txt', `missing Disallow for ${p}`);
}
if (fs.readFileSync(path.join(ROOT, 'CNAME'), 'utf8').trim() !== 'atikulislam.me') err('CNAME', 'unexpected domain');

const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'site.webmanifest'), 'utf8'));
for (const icon of manifest.icons || []) {
  if (!fs.existsSync(path.join(ROOT, icon.src))) err('site.webmanifest', `missing icon ${icon.src}`);
}
if (!manifest.start_url || !manifest.name) err('site.webmanifest', 'missing name/start_url');

const secFile = path.join(ROOT, '.well-known', 'security.txt');
if (!fs.existsSync(secFile)) err('.well-known/security.txt', 'missing');
else {
  const sec = fs.readFileSync(secFile, 'utf8');
  if (!/^Contact:/m.test(sec)) err('.well-known/security.txt', 'missing Contact:');
  const expires = (sec.match(/^Expires:\s*(\S+)/m) || [])[1];
  if (!expires) err('.well-known/security.txt', 'missing Expires:');
  else if (new Date(expires).getTime() < Date.now()) err('.well-known/security.txt', `Expires ${expires} is in the past`);
  if (!/^Canonical:/m.test(sec)) warn('.well-known/security.txt', 'missing Canonical:');
}

/* 4. Publish scope: build inputs stay out of the published tree ---------------- */
const cfg = fs.readFileSync(path.join(ROOT, '_config.yml'), 'utf8');
const excluded = [...cfg.matchAll(/^\s+-\s+(\S+)\s*$/gm)].map((m) => m[1]);
for (const entry of ['docs', 'prompts', 'scripts', 'design', 'data', 'README.md', 'RELEASE.md', 'package.json']) {
  if (!excluded.includes(entry)) err('_config.yml', `exclude list is missing ${entry}`);
}
if (!/include:\s*\n\s+-\s+\.well-known/.test(cfg)) err('_config.yml', '.well-known is not force-included');
for (const dir of ['docs', 'prompts', 'scripts', 'design', 'data']) {
  if (fs.existsSync(path.join(ROOT, dir)) && !excluded.includes(dir)) err('_config.yml', `${dir}/ would ship`);
}

/* 5. CSS url() references, JSON parsing, script contract ----------------------- */
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
  try {
    JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    err(rel(file), `invalid JSON: ${e.message}`);
  }
}
const mainJs = fs.readFileSync(path.join(ROOT, 'js', 'main.js'), 'utf8');
if (!mainJs.includes('youtube-nocookie.com/embed/')) err('js/main.js', 'testimonial embed must use youtube-nocookie');
if (!mainJs.includes("dataLayer.push")) err('js/main.js', 'no dataLayer conversion event');
if (!/generate_lead/.test(mainJs)) err('js/main.js', 'form success must push a generate_lead event');
if (!/437ef875-ee27-44e0-9884-22910c26316b/.test(mainJs)) err('js/main.js', 'Web3Forms access key is missing');

/* 6. Report ------------------------------------------------------------------- */
console.log(
  `checked ${htmlFiles.length} HTML, ${cssFiles.length} CSS, ${jsonFiles.length} JSON files; ` +
  `${locs.length} sitemap URLs; ${titles.size} unique titles`,
);
if (warnings.length) console.log(`warnings (${warnings.length}):\n  ${warnings.join('\n  ')}`);
if (errors.length) {
  console.log(`errors (${errors.length}):\n  ${errors.join('\n  ')}`);
  process.exit(1);
}
console.log('no errors');
