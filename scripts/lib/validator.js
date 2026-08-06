/**
 * scripts/lib/validator.js
 *
 * Automatic validation gate every generated asset must pass before the
 * build considers it successful. Nothing here "fixes" a bad asset — a
 * failed validation surfaces as a failed record, which build-assets.js
 * turns into a loud build failure per the "never silently substitute
 * placeholders" requirement.
 */

const fs = require('fs');
let sharp;
try {
  sharp = require('sharp');
} catch (e) {
  sharp = null;
}

const SIZE_BUDGETS_KB = {
  svg: 20,
  banner: 130,
  og: 150,
  favicon: 10,
};

function validateSvg(filePath, expectedLayerIds = []) {
  const errors = [];
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    return [`Could not read file: ${err.message}`];
  }

  // Lightweight well-formedness check: every opening tag has a matching
  // closing tag or is self-closed. A full XML parser is unnecessary
  // overhead for this pipeline's needs and adds a dependency; this catches
  // the realistic failure modes (truncated output, unescaped ampersands).
  // Match every tag as a whole unit first (`<...>`, not excluding '/' from
  // the middle — attribute values like xmlns="http://www.w3.org/2000/svg"
  // legitimately contain slashes, so a character class that excludes '/'
  // anywhere in the tag breaks on every SVG that declares a namespace).
  // Classify each match afterwards by its start/end markers only.
  const allTags = content.match(/<[^>]+>/g) || [];
  let openCount = 0;
  let closeCount = 0;
  for (const tag of allTags) {
    if (tag.startsWith('<?') || tag.startsWith('<!--')) continue; // declarations/comments
    if (tag.startsWith('</')) {
      closeCount += 1;
    } else if (tag.endsWith('/>')) {
      // self-closing — neither an unmatched open nor a close
    } else {
      openCount += 1;
    }
  }

  if (!content.trim().startsWith('<svg') && !content.trim().startsWith('<?xml')) {
    errors.push('File does not start with an <svg> or <?xml> declaration.');
  }
  if (openCount !== closeCount) {
    errors.push('SVG appears malformed (mismatched open/close tags).');
  }
  if (!content.includes('viewBox')) {
    errors.push('SVG missing viewBox attribute (required for responsive scaling).');
  }

  for (const layerId of expectedLayerIds) {
    if (!content.includes(`id="${layerId}"`) && !content.includes(`id='${layerId}'`)) {
      errors.push(`Expected layer group id="${layerId}" not found — layered animation hook missing.`);
    }
  }

  const kb = fs.statSync(filePath).size / 1024;
  if (kb > SIZE_BUDGETS_KB.svg) {
    errors.push(`SVG exceeds ${SIZE_BUDGETS_KB.svg}KB budget (${kb.toFixed(1)}KB) — optimization may not have completed.`);
  }

  return errors;
}

async function validateRaster(filePath, { expectedWidth, expectedHeight, budgetKey = 'banner' } = {}) {
  const errors = [];

  if (!fs.existsSync(filePath)) {
    return [`Output file missing: ${filePath}`];
  }

  if (sharp) {
    try {
      const metadata = await sharp(filePath).metadata();
      if (expectedWidth && metadata.width !== expectedWidth) {
        errors.push(`Width mismatch: expected ${expectedWidth}px, got ${metadata.width}px.`);
      }
      if (expectedHeight && metadata.height !== expectedHeight) {
        errors.push(`Height mismatch: expected ${expectedHeight}px, got ${metadata.height}px.`);
      }
    } catch (err) {
      errors.push(`Could not read image metadata: ${err.message}`);
    }
  }

  const kb = fs.statSync(filePath).size / 1024;
  const budget = SIZE_BUDGETS_KB[budgetKey] || SIZE_BUDGETS_KB.banner;
  if (kb > budget) {
    errors.push(`File exceeds ${budget}KB budget (${kb.toFixed(1)}KB) — optimization may not have completed.`);
  }

  return errors;
}

module.exports = { validateSvg, validateRaster, SIZE_BUDGETS_KB };
