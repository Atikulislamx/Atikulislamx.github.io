/**
 * scripts/lib/shared-style.js
 *
 * Loads prompts/_style-constraints.json once and exposes it to every
 * generation script, so the Trusted Slate palette and the "avoid" rules
 * (no neon/hacker/Matrix/padlock/hoodie/stock-cybersecurity aesthetics)
 * are enforced centrally — a single edit here updates every future prompt,
 * rather than needing to touch dozens of individual spec files.
 */

const fs = require('fs');
const path = require('path');

let cached = null;

function loadStyleConstraints() {
  if (cached) return cached;
  const filePath = path.join(__dirname, '..', '..', 'prompts', '_style-constraints.json');
  const raw = fs.readFileSync(filePath, 'utf-8');
  cached = JSON.parse(raw);
  return cached;
}

module.exports = { loadStyleConstraints };
