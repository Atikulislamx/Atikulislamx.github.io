#!/usr/bin/env node
/**
 * scripts/build-assets.js
 *
 * Single-command entry point: `npm run generate:assets`
 *
 * Orchestrates, in order:
 *   1. Favicon (deterministic, no AI)
 *   2. Illustrations & banners (AI, via /prompts, excluding og/)
 *   3. OG images (one AI base template + deterministic per-page text)
 *
 * Then: validates every required (non-deferred) launch asset actually
 * produced output, writes assets-manifest.json, and prints a full summary.
 *
 * Flags:
 *   --force              Regenerate everything, ignoring existing files
 *   --include-deferred    Also generate reserved future-phase assets
 *   --type=<category>     Restrict to one category: hero | services | case-studies |
 *                          dividers | cta | portfolio | about | empty-states | og | favicon | all
 *
 * Examples:
 *   npm run generate:assets
 *   npm run generate:assets -- --force
 *   npm run generate:assets -- --type=services
 *   npm run generate:assets -- --type=og --force
 */

require('dotenv').config();
const path = require('path');
const { runIllustrations } = require('./generate-illustrations');
const { runOgImages } = require('./generate-og-images');
const { run: runFavicon } = require('./generate-favicon');
const { buildManifest } = require('./lib/manifest');

const PROJECT_ROOT = path.join(__dirname, '..');
const MANIFEST_PATH = path.join(PROJECT_ROOT, 'assets', 'generated', 'assets-manifest.json');

function parseArgs() {
  const args = process.argv.slice(2);
  return {
    force: args.includes('--force'),
    includeDeferred: args.includes('--include-deferred'),
    typeFilter: (args.find((a) => a.startsWith('--type=')) || '').split('=')[1] || null,
  };
}

async function main() {
  const started = Date.now();
  const { force, includeDeferred, typeFilter } = parseArgs();

  const runFaviconStep = !typeFilter || typeFilter === 'all' || typeFilter === 'favicon';
  const runOgStep = !typeFilter || typeFilter === 'all' || typeFilter === 'og';
  const runIllustrationsStep = !typeFilter || typeFilter === 'all' || (typeFilter !== 'favicon' && typeFilter !== 'og');
  const illustrationTypeFilter = typeFilter && typeFilter !== 'all' ? typeFilter : null;

  console.log('='.repeat(64));
  console.log('Atikul Islam Rabbi — Visual Asset Pipeline');
  console.log(`force=${force}  includeDeferred=${includeDeferred}  type=${typeFilter || 'all'}`);
  console.log('='.repeat(64) + '\n');

  const allRecords = [];

  if (runFaviconStep) {
    allRecords.push(await runFavicon({ force }));
  }

  if (runIllustrationsStep) {
    const records = await runIllustrations({
      force,
      includeDeferred,
      typeFilter: illustrationTypeFilter && illustrationTypeFilter !== 'favicon' ? illustrationTypeFilter : null,
    });
    allRecords.push(...records);
  }

  if (runOgStep) {
    const records = await runOgImages({ force });
    allRecords.push(...records);
  }

  // --- Summary ---
  const generated = allRecords.filter((r) => r.status === 'generated');
  const skippedExisting = allRecords.filter((r) => r.status === 'skipped-existing');
  const skippedDeferred = allRecords.filter((r) => r.status === 'skipped-deferred');
  const failed = allRecords.filter((r) => r.status === 'failed');
  const elapsedSec = ((Date.now() - started) / 1000).toFixed(1);

  console.log('\n' + '-'.repeat(64));
  console.log('SUMMARY');
  console.log('-'.repeat(64));
  console.log(`Generated:          ${generated.length}`);
  console.log(`Skipped (existing): ${skippedExisting.length}`);
  console.log(`Skipped (deferred): ${skippedDeferred.length}`);
  console.log(`Failed:             ${failed.length}`);
  console.log(`Total time:         ${elapsedSec}s`);
  console.log('-'.repeat(64));

  if (failed.length) {
    console.error('\nFailed assets:');
    for (const r of failed) console.error(`  - ${r.category}/${r.id}: ${r.error}`);
  }

  // Manifest includes every record with output files present on disk,
  // whether generated this run or already present from a previous run.
  const manifestable = allRecords.filter((r) => r.outputFiles && r.outputFiles.length);
  const manifest = await buildManifest(manifestable, MANIFEST_PATH);
  console.log(`\nManifest written: ${path.relative(PROJECT_ROOT, MANIFEST_PATH)} (${manifest.assetCount} files)`);

  // --- Fail loudly if any required (non-deferred) launch asset produced no output ---
  const missingRequired = allRecords.filter((r) => !r.deferred && (!r.outputFiles || r.outputFiles.length === 0));
  if (missingRequired.length) {
    console.error('\n' + '!'.repeat(64));
    console.error('BUILD FAILED: required launch assets are missing.');
    console.error('Refusing to substitute placeholders for production assets.');
    console.error('!'.repeat(64));
    for (const r of missingRequired) console.error(`  - ${r.category}/${r.id}${r.error ? `: ${r.error}` : ''}`);
    process.exitCode = 1;
    return;
  }

  if (failed.length) {
    process.exitCode = 1;
    return;
  }

  console.log('\n✔ Asset pipeline completed successfully.');
}

main().catch((err) => {
  console.error(`\n[FATAL] ${err.stack || err.message}`);
  process.exitCode = 1;
});
