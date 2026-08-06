/**
 * scripts/generate-og-images.js
 *
 * Open Graph images = ONE AI-generated base template (prompts/og/base-template.json)
 * + each real page's title, composited deterministically with sharp + an SVG
 * text overlay. See prompts/og/base-template.json "usage" field for the full
 * reasoning (generative models don't reliably render pixel-accurate text).
 *
 * Incremental by default (per-page skip if its OG image already exists),
 * supports --force and is invoked by build-assets.js with --type=og.
 */

if (require.main === module) require('dotenv').config();
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { generateImage } = require('./lib/image-generator');
const { validateRaster } = require('./lib/validator');

const PROJECT_ROOT = path.join(__dirname, '..');
const PAGES_PATH = path.join(PROJECT_ROOT, 'data', 'pages.json');
const BASE_SPEC_PATH = path.join(PROJECT_ROOT, 'prompts', 'og', 'base-template.json');
const BASE_OUTPUT_PATH = path.join(PROJECT_ROOT, 'assets', 'generated', 'og', '_base', 'og-base-template.jpg');
const OG_OUTPUT_DIR = path.join(PROJECT_ROOT, 'assets', 'generated', 'og');

const OG_WIDTH = 1200;
const OG_HEIGHT = 630;

function titleOverlaySvg(title) {
  const escaped = String(title).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return Buffer.from(`
    <svg width="${OG_WIDTH}" height="${OG_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <foreignObject x="80" y="120" width="900" height="320">
        <div xmlns="http://www.w3.org/1999/xhtml"
             style="font-family:Fraunces,serif;font-size:56px;font-weight:600;color:#F8FAFC;line-height:1.15;">
          ${escaped}
        </div>
      </foreignObject>
      <text x="80" y="560" font-family="Inter, sans-serif" font-size="22" font-weight="500" fill="#2EC4B6">
        Atikul Islam Rabbi — Cyber Infinity
      </text>
    </svg>
  `);
}

async function ensureBaseTemplate({ force }) {
  if (fs.existsSync(BASE_OUTPUT_PATH) && !force) {
    console.log('[skip:exists]    og/_base (base template)');
    return BASE_OUTPUT_PATH;
  }

  console.log('[generated]      og/_base (base template — one call, reused for every page)');
  const spec = JSON.parse(fs.readFileSync(BASE_SPEC_PATH, 'utf-8'));
  const { data } = await generateImage({
    prompt: spec.prompt,
    format: 'jpg',
    width: spec.dimensions.width,
    height: spec.dimensions.height,
    layered: false,
  });

  fs.mkdirSync(path.dirname(BASE_OUTPUT_PATH), { recursive: true });
  fs.writeFileSync(BASE_OUTPUT_PATH, Buffer.from(data, 'base64'));
  return BASE_OUTPUT_PATH;
}

async function compositeForPage(baseImagePath, page, { force }) {
  fs.mkdirSync(OG_OUTPUT_DIR, { recursive: true });
  const outPath = path.join(OG_OUTPUT_DIR, `og-${page.slug}.jpg`);

  const record = {
    id: `og-${page.slug}`,
    category: 'og',
    promptSource: `${path.relative(PROJECT_ROOT, BASE_SPEC_PATH)} + data/pages.json (title composited deterministically)`,
    deferred: false,
    dimensions: { width: OG_WIDTH, height: OG_HEIGHT },
    outputFiles: [],
    status: null,
    generatedAt: null,
    error: null,
  };

  if (fs.existsSync(outPath) && !force) {
    record.outputFiles = [outPath];
    record.status = 'skipped-existing';
    console.log(`[skip:exists]    og/${record.id}`);
    return record;
  }

  try {
    await sharp(baseImagePath)
      .resize(OG_WIDTH, OG_HEIGHT)
      .composite([{ input: titleOverlaySvg(page.title), top: 0, left: 0 }])
      .jpeg({ quality: 82, mozjpeg: true })
      .toFile(outPath);

    const errors = await validateRaster(outPath, {
      expectedWidth: OG_WIDTH,
      expectedHeight: OG_HEIGHT,
      budgetKey: 'og',
    });
    if (errors.length) throw new Error(`Validation failed: ${errors.join('; ')}`);

    record.outputFiles = [outPath];
    record.status = 'generated';
    record.generatedAt = new Date().toISOString();
    console.log(`[generated]      og/${record.id}`);
  } catch (err) {
    record.status = 'failed';
    record.error = err.message;
    console.log(`[FAILED]         og/${record.id} — ${err.message}`);
  }

  return record;
}

async function runOgImages({ force = false } = {}) {
  const baseImagePath = await ensureBaseTemplate({ force });
  const pages = JSON.parse(fs.readFileSync(PAGES_PATH, 'utf-8'));

  const records = [];
  records.push(
    await compositeForPage(
      baseImagePath,
      { slug: 'default', title: 'Atikul Islam Rabbi — Social Media Security & Recovery Specialist' },
      { force }
    )
  );

  for (const page of pages) {
    records.push(await compositeForPage(baseImagePath, page, { force }));
  }

  return records;
}

if (require.main === module) {
  const force = process.argv.includes('--force');
  runOgImages({ force }).then((records) => {
    if (records.some((r) => r.status === 'failed')) process.exitCode = 1;
  });
}

module.exports = { runOgImages };
