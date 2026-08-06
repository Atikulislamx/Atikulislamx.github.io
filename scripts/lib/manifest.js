/**
 * scripts/lib/manifest.js
 *
 * Builds assets-manifest.json from the asset records collected during a
 * build.run — one entry per output file, with a checksum so a future build
 * (or a CI check) can detect drift between what the manifest claims exists
 * and what's actually on disk.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

let sharp;
try {
  sharp = require('sharp');
} catch (e) {
  sharp = null;
}

const PROJECT_ROOT = path.join(__dirname, '..', '..');

function sha256(filePath) {
  return crypto.createHash('sha256').update(fs.readFileSync(filePath)).digest('hex');
}

function svgDimensions(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const match = content.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  return match ? { width: parseFloat(match[1]), height: parseFloat(match[2]) } : null;
}

async function fileDimensions(filePath, fallback) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.svg') {
    return svgDimensions(filePath) || fallback || null;
  }
  if (sharp) {
    try {
      const meta = await sharp(filePath).metadata();
      return { width: meta.width, height: meta.height };
    } catch (e) {
      return fallback || null;
    }
  }
  return fallback || null;
}

async function buildManifest(records, outputPath) {
  const manifest = {
    generatedAt: new Date().toISOString(),
    assetCount: 0,
    assets: [],
  };

  for (const record of records) {
    for (const filePath of record.outputFiles || []) {
      if (!fs.existsSync(filePath)) continue;
      const dimensions = await fileDimensions(filePath, record.dimensions);
      manifest.assets.push({
        id: record.id,
        category: record.category,
        file: path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/'),
        format: path.extname(filePath).replace('.', ''),
        dimensions,
        promptSource: record.promptSource || 'deterministic — no AI prompt (see prompts/README.md exceptions)',
        status: record.status,
        deferred: !!record.deferred,
        checksumSha256: sha256(filePath),
        fileSizeKb: Math.round((fs.statSync(filePath).size / 1024) * 10) / 10,
        generatedAt: record.generatedAt || null,
      });
    }
  }

  manifest.assetCount = manifest.assets.length;
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(manifest, null, 2));
  return manifest;
}

module.exports = { buildManifest, sha256 };
