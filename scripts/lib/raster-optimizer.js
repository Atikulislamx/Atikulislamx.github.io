/**
 * scripts/lib/raster-optimizer.js
 *
 * Wraps sharp to produce a WebP primary + JPEG fallback pair for every
 * raster asset (case study banners, OG images), matching the Design System's
 * "WebP primary, JPEG fallback" image guideline (§29).
 */

const sharp = require('sharp');
const path = require('path');

const JPEG_QUALITY = 80;
const WEBP_QUALITY = 80;
const SIZE_BUDGET_KB = {
  banner: 130,
  og: 150,
};

async function optimizeRaster(inputBuffer, outputPathWithoutExt, { budgetKey = 'banner' } = {}) {
  const webpPath = `${outputPathWithoutExt}.webp`;
  const jpgPath = `${outputPathWithoutExt}.jpg`;

  await sharp(inputBuffer).webp({ quality: WEBP_QUALITY }).toFile(webpPath);
  await sharp(inputBuffer).jpeg({ quality: JPEG_QUALITY, mozjpeg: true }).toFile(jpgPath);

  const fs = require('fs');
  const webpKb = fs.statSync(webpPath).size / 1024;
  const jpgKb = fs.statSync(jpgPath).size / 1024;
  const budget = SIZE_BUDGET_KB[budgetKey] || SIZE_BUDGET_KB.banner;

  if (webpKb > budget || jpgKb > budget) {
    console.warn(
      `[raster-optimizer] Warning: ${path.basename(outputPathWithoutExt)} exceeds the ` +
      `${budget}KB budget (webp: ${webpKb.toFixed(0)}KB, jpg: ${jpgKb.toFixed(0)}KB). ` +
      'Consider a lower quality setting or simpler source artwork.'
    );
  }

  return { webpPath, jpgPath };
}

module.exports = { optimizeRaster };
