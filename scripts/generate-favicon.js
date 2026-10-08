// scripts/generate-favicon.js — rebuilds the brand icon set from the committed source.
// Source: assets/brand/favicon.svg (monogram with outlined letterforms; no font needed).
// Outputs: favicon-16.png, favicon-32.png, favicon.ico (16/32/48), apple-touch-icon.png (180),
//          icon-192.png, icon-512.png (square variant for app icons).
// Deterministic: no network, no AI. Requires sharp (devDependency).
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const BRAND = path.join(__dirname, '..', 'assets', 'brand');
const rounded = fs.readFileSync(path.join(BRAND, 'favicon.svg'));
const square = Buffer.from(rounded.toString('utf8').replace(' rx="14"', ''));

async function renderPng(svg, size) {
  return sharp(svg, { density: 1024 }).resize(size, size).png({ compressionLevel: 9 }).toBuffer();
}

// ICO container with PNG frames (supported by all current browsers and Windows Vista+).
function buildIco(frames) {
  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(frames.length, 4);
  const dir = Buffer.alloc(16 * frames.length);
  let offset = 6 + dir.length;
  frames.forEach((f, i) => {
    const o = i * 16;
    const dim = f.size >= 256 ? 0 : f.size;
    dir[o] = dim;
    dir[o + 1] = dim;
    dir.writeUInt16LE(1, o + 4);
    dir.writeUInt16LE(32, o + 6);
    dir.writeUInt32LE(f.buf.length, o + 8);
    dir.writeUInt32LE(offset, o + 12);
    offset += f.buf.length;
  });
  return Buffer.concat([header, dir, ...frames.map((f) => f.buf)]);
}

(async () => {
  const outputs = [
    ['favicon-16.png', rounded, 16],
    ['favicon-32.png', rounded, 32],
    ['apple-touch-icon.png', square, 180],
    ['icon-192.png', square, 192],
    ['icon-512.png', square, 512]
  ];
  for (const [name, svg, size] of outputs) {
    fs.writeFileSync(path.join(BRAND, name), await renderPng(svg, size));
  }
  const frames = [];
  for (const size of [16, 32, 48]) frames.push({ size, buf: await renderPng(rounded, size) });
  fs.writeFileSync(path.join(BRAND, 'favicon.ico'), buildIco(frames));
  console.log('Brand icons written to assets/brand/ (copy favicon.ico to the repo root as well).');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
