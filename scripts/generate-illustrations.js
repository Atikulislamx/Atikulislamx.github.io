/**
 * scripts/generate-illustrations.js
 *
 * Walks /prompts (excluding og/, which has its own generator), generates
 * every non-deferred, not-already-existing asset via the configured image
 * API, optimizes it, validates it, and writes it to /assets/generated/.
 *
 * Incremental by default: an asset whose output file(s) already exist on
 * disk is skipped unless --force is passed. This is what makes repeated
 * `npm run generate:assets` calls fast and safe during normal development
 * (e.g. after adding one new service page) rather than re-generating and
 * re-billing for all ~40 assets every time.
 *
 * Exported as runIllustrations() so build-assets.js can call it directly;
 * also runnable standalone: `node scripts/generate-illustrations.js --type=services --force`
 */

if (require.main === module) require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { generateImage } = require('./lib/image-generator');
const { optimizeSvg } = require('./lib/svg-optimizer');
const { optimizeRaster } = require('./lib/raster-optimizer');
const { validateSvg, validateRaster } = require('./lib/validator');

const PROMPTS_DIR = path.join(__dirname, '..', 'prompts');
const PROJECT_ROOT = path.join(__dirname, '..');
const SKIP_DIRS = new Set(['og']); // handled by generate-og-images.js
const LAYER_IDS = ['layer-bg', 'layer-mid', 'layer-accent'];

function walkPromptFiles(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      results.push(...walkPromptFiles(path.join(dir, entry.name)));
    } else if (entry.isFile() && entry.name.endsWith('.json') && !entry.name.startsWith('_')) {
      results.push({ specPath: path.join(dir, entry.name), category: path.basename(dir) });
    }
  }
  return results;
}

function outputExists(spec) {
  const destDir = path.join(PROJECT_ROOT, spec.destination);
  if (spec.outputFormat === 'svg') {
    return fs.existsSync(path.join(destDir, spec.outputFilename));
  }
  const base = path.join(destDir, spec.id);
  return fs.existsSync(`${base}.webp`) && fs.existsSync(`${base}.jpg`);
}

function existingOutputs(spec) {
  const destDir = path.join(PROJECT_ROOT, spec.destination);
  if (spec.outputFormat === 'svg') {
    return [path.join(destDir, spec.outputFilename)];
  }
  return [path.join(destDir, `${spec.id}.webp`), path.join(destDir, `${spec.id}.jpg`)];
}

async function processSpec(specPath, category, { force, includeDeferred }) {
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf-8'));
  const record = {
    id: spec.id,
    category,
    promptSource: path.relative(PROJECT_ROOT, specPath),
    deferred: !!spec.deferred,
    dimensions: spec.dimensions,
    outputFiles: [],
    status: null,
    generatedAt: null,
    error: null,
  };

  if (spec.deferred && !includeDeferred) {
    record.status = 'skipped-deferred';
    return record;
  }

  if (!force && outputExists(spec)) {
    record.outputFiles = existingOutputs(spec);
    record.status = 'skipped-existing';
    return record;
  }

  try {
    const { data } = await generateImage({
      prompt: spec.prompt,
      format: spec.outputFormat,
      width: spec.dimensions.width,
      height: spec.dimensions.height,
      layered: !!spec.layered,
    });

    const destDir = path.join(PROJECT_ROOT, spec.destination);
    fs.mkdirSync(destDir, { recursive: true });

    if (spec.outputFormat === 'svg') {
      const optimized = optimizeSvg(data);
      const outPath = path.join(destDir, spec.outputFilename);
      fs.writeFileSync(outPath, optimized, 'utf-8');
      const errors = validateSvg(outPath, spec.layered ? LAYER_IDS : []);
      if (errors.length) throw new Error(`Validation failed: ${errors.join('; ')}`);
      record.outputFiles = [outPath];
    } else {
      const buffer = Buffer.from(data, 'base64');
      const outputPathWithoutExt = path.join(destDir, spec.id);
      const { webpPath, jpgPath } = await optimizeRaster(buffer, outputPathWithoutExt, { budgetKey: 'banner' });
      const errors = await validateRaster(jpgPath, {
        expectedWidth: spec.dimensions.width,
        expectedHeight: spec.dimensions.height,
        budgetKey: 'banner',
      });
      if (errors.length) throw new Error(`Validation failed: ${errors.join('; ')}`);
      record.outputFiles = [webpPath, jpgPath];
    }

    record.status = 'generated';
    record.generatedAt = new Date().toISOString();
  } catch (err) {
    record.status = 'failed';
    record.error = err.message;
  }

  return record;
}

function logRecord(record) {
  const prefix = {
    generated: '[generated]     ',
    'skipped-existing': '[skip:exists]   ',
    'skipped-deferred': '[skip:deferred] ',
    failed: '[FAILED]        ',
  }[record.status] || '[?]';
  console.log(`${prefix}${record.category}/${record.id}${record.error ? ` — ${record.error}` : ''}`);
}

async function runIllustrations({ force = false, includeDeferred = false, typeFilter = null } = {}) {
  const all = walkPromptFiles(PROMPTS_DIR);
  const filtered = typeFilter ? all.filter((e) => e.category === typeFilter) : all;

  const records = [];
  for (const { specPath, category } of filtered) {
    const record = await processSpec(specPath, category, { force, includeDeferred });
    records.push(record);
    logRecord(record);
  }
  return records;
}

if (require.main === module) {
  const force = process.argv.includes('--force');
  const includeDeferred = process.argv.includes('--include-deferred');
  const typeArg = process.argv.find((a) => a.startsWith('--type='));
  const typeFilter = typeArg ? typeArg.split('=')[1] : null;

  runIllustrations({ force, includeDeferred, typeFilter }).then((records) => {
    if (records.some((r) => r.status === 'failed')) process.exitCode = 1;
  });
}

module.exports = { runIllustrations };
