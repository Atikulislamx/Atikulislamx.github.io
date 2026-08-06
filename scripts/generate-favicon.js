/**
 * scripts/generate-favicon.js
 *
 * Deterministic (non-AI) favicon generation. A generative image model
 * cannot reliably guarantee pixel-perfect legibility of "AIR" at 16x16px —
 * this is a documented engineering decision (see prompts/README.md
 * "Two intentional exceptions"), not an oversight or a workaround for a
 * missing capability.
 */

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { optimizeSvg } = require('./lib/svg-optimizer');
const { validateSvg, validateRaster } = require('./lib/validator');

const PROJECT_ROOT = path.join(__dirname, '..');
const OUT_DIR = path.join(PROJECT_ROOT, 'assets', 'generated', 'favicon');

const MONOGRAM_SVG = `
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <g id="layer-mark">
    <rect width="64" height="64" rx="12" fill="#0F2A4A"/>
    <text x="32" y="42" text-anchor="middle" font-family="Fraunces, serif" font-size="26" font-weight="600" fill="#F8FAFC">AIR</text>
  </g>
</svg>
`.trim();

async function run({ force = false } = {}) {
  const svgPath = path.join(OUT_DIR, 'favicon.svg');
  const png16 = path.join(OUT_DIR, 'favicon-16.png');
  const png32 = path.join(OUT_DIR, 'favicon-32.png');
  const appleTouch = path.join(OUT_DIR, 'apple-touch-icon.png');
  const outputFiles = [svgPath, png16, png32, appleTouch];

  const record = {
    id: 'favicon-set',
    category: 'favicon',
    promptSource: 'deterministic — no AI prompt (see prompts/README.md exceptions)',
    deferred: false,
    dimensions: { width: 64, height: 64, note: 'exported at 16, 32, and 180px' },
    outputFiles: [],
    status: null,
    generatedAt: null,
    error: null,
  };

  if (!force && outputFiles.every(fs.existsSync)) {
    record.outputFiles = outputFiles;
    record.status = 'skipped-existing';
    console.log('[skip:exists]    favicon/favicon-set');
    return record;
  }

  try {
    fs.mkdirSync(OUT_DIR, { recursive: true });
    const optimized = optimizeSvg(MONOGRAM_SVG);
    fs.writeFileSync(svgPath, optimized, 'utf-8');

    const svgBuffer = Buffer.from(optimized);
    await sharp(svgBuffer).resize(16, 16).png().toFile(png16);
    await sharp(svgBuffer).resize(32, 32).png().toFile(png32);
    await sharp(svgBuffer).resize(180, 180).png().toFile(appleTouch);

    const errors = [
      ...validateSvg(svgPath, ['layer-mark']),
      ...(await validateRaster(png16, { expectedWidth: 16, expectedHeight: 16, budgetKey: 'favicon' })),
      ...(await validateRaster(png32, { expectedWidth: 32, expectedHeight: 32, budgetKey: 'favicon' })),
      ...(await validateRaster(appleTouch, { expectedWidth: 180, expectedHeight: 180, budgetKey: 'favicon' })),
    ];
    if (errors.length) throw new Error(errors.join('; '));

    record.outputFiles = outputFiles;
    record.status = 'generated';
    record.generatedAt = new Date().toISOString();
    console.log('[generated]      favicon/favicon-set (deterministic, no AI call)');
  } catch (err) {
    record.status = 'failed';
    record.error = err.message;
    console.log(`[FAILED]         favicon/favicon-set — ${err.message}`);
  }

  return record;
}

if (require.main === module) {
  run({ force: process.argv.includes('--force') }).then((record) => {
    if (record.status === 'failed') process.exitCode = 1;
  });
}

module.exports = { run };
